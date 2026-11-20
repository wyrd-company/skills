#!/usr/bin/env bash
# Take the workspace manager's claim for this thread, rolling the manager task
# forward when it is due, and record the shift in the pointer file.
#
# Usage: takeover.sh <expected holder>
#   <expected holder> is the thread you saw holding the claim and waited for,
#   or "-" when no thread held it.
#
# Run it after the expected holder's turn has ended. One takeover runs at a
# time, under a lock on the board. A takeover cut short leaves a progress file;
# running again finishes it, and any later takeover picks up what it recorded.
#
# 1. Finishes what a cut-short takeover or roll left: a manager task closed but
#    not archived, or more than one open manager task (the newest is current).
# 2. Refuses, with exit 3, when the claim has moved to a thread other than the
#    expected holder: another shift took over first.
# 3. Rolls forward when the current task is older than the "Roll forward every"
#    line of its standing state (default 1 day): creates a successor with the
#    standing state, claims it, and closes and archives the old task. A standing
#    state missing a section is not rolled: the summary says why.
# 4. Otherwise takes the claim on the current task.
# 5. Logs the takeover, writes <board>/manager.json, and removes the progress
#    file.
#
# Prints a JSON summary: task; previous_threads, the shifts to settle (empty for
# the first shift); rolled_from, null when no roll happened; roll_skipped, the
# reason a due roll did not happen, or null.
#
# Environment:
#   T3CODE_THREAD_ID  this shift's thread id (required)
#   MANAGER_BOARD     the workspace board (default: /tasks)
#   WORKSPACE         the workspace's name (default: from /etc/workspace/config.yml)
# Exit: 0 done; 1 a step failed; 2 the board has no manager task; 3 another
# shift holds the claim; 4 the lock was not free within 10 minutes.
set -euo pipefail
# shellcheck source=manager-lib.sh source-path=SCRIPTDIR
source "$(dirname "${BASH_SOURCE[0]}")/manager-lib.sh"

EXPECTED=${1:?usage: takeover.sh <expected holder, or - for none>}
[ "$EXPECTED" != "-" ] || EXPECTED=""
BOARD=${MANAGER_BOARD:-/tasks}
SELF=${T3CODE_THREAD_ID:?T3CODE_THREAD_ID is not set}
POINTER="$BOARD/manager.json"
PROGRESS="$BOARD/.takeover.json"
TODAY=$(date -u +%F)
NOW=$(date -u +%FT%TZ)

kb() { kanban-md "$@" --dir "$BOARD"; }

exec 9>"$BOARD/.manager.lock"
flock -w 600 9 || {
  echo "another takeover holds $BOARD/.manager.lock" >&2
  exit 4
}

# A manager task closed by a cut-short roll but not archived.
for id in $(kb --json list --tag workspace-manager --status "done" | jq -r '.[].id'); do
  kb archive "$id" >/dev/null
done

tasks=$(kb --json list --tag workspace-manager --status backlog,todo,in-progress,review --sort id)
if [ "$(jq length <<<"$tasks")" -eq 0 ]; then
  echo "no manager task on $BOARD: set the manager up first" >&2
  exit 2
fi
current=$(jq -r '.[-1].id' <<<"$tasks")
older=$(jq -r '.[:-1][].id' <<<"$tasks")
holder=$(jq -r --arg self "$SELF" '[.[] | .claimed_by // empty | select(. != $self)] | last // ""' <<<"$tasks")

# What a cut-short takeover recorded: its own thread, the shifts it had to
# settle, and the roll it started.
progress='{}'
[ ! -f "$PROGRESS" ] || progress=$(cat "$PROGRESS")
progress_thread=$(jq -r '.thread // ""' <<<"$progress")

if [ -n "$holder" ] && [ "$holder" != "$EXPECTED" ] && [ "$holder" != "$progress_thread" ]; then
  echo "the claim is held by $holder, not ${EXPECTED:-nobody}: another shift took over" >&2
  jq -n --arg holder "$holder" '{holder: $holder}'
  exit 3
fi

previous=$(jq -c --arg self "$SELF" --arg holder "$holder" --arg cut "$progress_thread" '
  [(.previous // [])[], $holder, (if $cut != $self then $cut else empty end)]
  | map(select(. != "" and . != $self)) | unique' <<<"$progress")
rolled_from=$(jq -r '.rolled_from // "null"' <<<"$progress")
[ -z "$older" ] || rolled_from=$(tail -1 <<<"$older") # a roll cut short after the successor was made

save_progress() {
  jq -n --arg thread "$SELF" --argjson previous "$previous" --argjson rolled "$rolled_from" \
    '{thread: $thread, previous: $previous, rolled_from: $rolled}' >"$PROGRESS.tmp"
  mv "$PROGRESS.tmp" "$PROGRESS"
}
save_progress

roll_skipped=null
if [ -z "$older" ]; then
  body=$(kb --json show "$current" | jq -r .body)
  every=$(standing_state <<<"$body" | sed -nE 's/^- Roll forward every: ([0-9]+) days?[[:space:]]*$/\1/p' | head -1) || true
  created=$(kb --json show "$current" | jq -r '.created | sub("\\.[0-9]+"; "") | fromdateiso8601')
  if [ $(($(date -u +%s) - created)) -ge $((${every:-1} * 86400)) ]; then
    if ! state=$(standing_state <<<"$body"); then
      roll_skipped='"the task has no ## Log heading outside a code block"'
    elif missing=$(missing_sections <<<"$state") && [ -n "$missing" ]; then
      roll_skipped=$(jq -Rn --arg m "$missing" '"the standing state lacks: " + ($m | split("\n") | join(", "))')
    else
      state=$(sed -E "s/^- Previous task: .*/- Previous task: #$current/" <<<"$state")
      successor=$(kb --json create "Workspace manager $TODAY" --status todo --tags workspace-manager \
        --body "$(printf '%s\n## Log\n' "$state")" | jq -r .id)
      [ -n "$successor" ] && [ "$successor" != null ] || {
        echo "creating the successor task failed" >&2
        exit 1
      }
      rolled_from=$current
      save_progress
      older=$current
      current=$successor
    fi
  fi
fi

# Take the claim on the current task.
status=$(kb --json show "$current" | jq -r .status)
claimed=$(kb --json show "$current" | jq -r '.claimed_by // ""')
if [ "$status" != "in-progress" ]; then
  kb move "$current" in-progress --claim "$SELF" >/dev/null
elif [ "$claimed" != "$SELF" ]; then
  [ -z "$claimed" ] || kb edit "$current" --release >/dev/null
  kb edit "$current" --claim "$SELF" >/dev/null
fi

for id in $older; do
  kb edit "$id" --append-body "Rolled forward to #$current by $SELF." --timestamp \
    --release --status "done" --completed "$TODAY" >/dev/null
  kb archive "$id" >/dev/null
done

if ! kb --json show "$current" | jq -e --arg e "Takeover by $SELF" '.body | contains($e)' >/dev/null; then
  entry="Takeover by $SELF from $(jq -r 'if length == 0 then "no previous shift" else join(", ") end' <<<"$previous")."
  [ "$rolled_from" = null ] || entry="$entry Rolled forward from #$rolled_from."
  kb edit "$current" --append-body "$entry" --timestamp --claim "$SELF" >/dev/null
fi

workspace=${WORKSPACE:-$(sed -nE 's/^workspace: *"?([^"]+)"?$/\1/p' /etc/workspace/config.yml 2>/dev/null | head -1)}
jq -n --arg thread "$SELF" --argjson task "$current" --arg board "$BOARD" --arg since "$NOW" --arg workspace "$workspace" \
  '{thread_id: $thread, task_id: $task, board: $board, since: $since, workspace: $workspace}' >"$POINTER.tmp"
mv "$POINTER.tmp" "$POINTER"
rm -f "$PROGRESS"

jq -n --argjson task "$current" --argjson previous "$previous" --argjson rolled "$rolled_from" --argjson skipped "$roll_skipped" \
  '{task: $task, previous_threads: $previous, rolled_from: $rolled, roll_skipped: $skipped}'
