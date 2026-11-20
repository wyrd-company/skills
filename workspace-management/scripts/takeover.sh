#!/usr/bin/env bash
# Take the workspace manager's claim for this thread, rolling the manager task
# forward when it is due, and record the shift in the pointer file.
#
# Usage: takeover.sh <expected holder>
#   <expected holder> is the thread you saw holding the claim and waited for,
#   or "-" when no thread held it.
#
# Run it after the expected holder's turn has ended. It holds the manager's
# lock throughout, as manager.sh does for every write, so no shift writes to the
# manager task while a takeover runs. Progress is kept in <board>/.takeover.json:
# a takeover cut short is finished by running it again, and a later shift's
# takeover settles what it recorded.
#
# 1. Finishes what a cut-short roll left: a manager task closed but not
#    archived, or more than one open manager task (the newest is current).
# 2. Refuses, with exit 3, when the claim is held by a thread other than the
#    expected holder: another shift took over first.
# 3. Rolls forward when the current task is older than the "Roll forward every"
#    line of its Schedule section (default 1 day): creates a successor with the
#    standing state, claims it, and closes and archives the old task. A
#    standing state missing a section is not rolled: the summary says why.
# 4. Otherwise takes the claim on the current task.
# 5. Logs the takeover, writes <board>/manager.json, and marks the progress done.
#
# Prints a JSON summary: task; previous_threads, the shifts to settle (empty for
# the first shift); rolled_from, null when no roll happened; roll_skipped, the
# reason a due roll did not happen, or null. Run again by the same thread after
# it finished, it prints the same summary and changes nothing.
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

kb() { kanban-md "$@" --dir "$BOARD"; }

manager_lock "$BOARD" || {
  echo "the manager lock on $BOARD was not free within 10 minutes" >&2
  exit 4
}

progress='{}'
[ ! -f "$PROGRESS" ] || progress=$(cat "$PROGRESS")
# Run again after finishing: repeat the summary, if the pointer still agrees.
if jq -e --arg self "$SELF" '.thread == $self and .status == "done"' >/dev/null <<<"$progress" &&
  jq -e --arg self "$SELF" --argjson task "$(jq '.summary.task' <<<"$progress")" \
    '.thread_id == $self and .task_id == $task' "$POINTER" >/dev/null 2>&1; then
  jq '.summary' <<<"$progress"
  exit 0
fi
# Another thread's takeover, finished or not: that thread and the shifts it took
# over from are ours to settle. It may have stopped before settling them, and
# settling a thread twice does no harm. A takeover it left running is the
# manager until this one replaces it.
other=$(jq -c --arg self "$SELF" 'if .thread != null and .thread != $self then . else {} end' <<<"$progress")
cut=$(jq -c '[(.thread // empty), (.previous // [])[]]' <<<"$other")
own=$(jq -c --arg self "$SELF" 'if .thread == $self then . else {} end' <<<"$progress")
running=$(jq -r 'select(.status == "running") | .thread // empty' <<<"$other")

# A manager task closed by a cut-short roll but not archived.
closed=$(kb --json list --tag workspace-manager --status "done" | jq -r '.[].id')
for id in $closed; do kb archive "$id" >/dev/null; done

tasks=$(kb --json list --tag workspace-manager --status backlog,todo,in-progress,review --sort id)
if [ "$(jq length <<<"$tasks")" -eq 0 ]; then
  echo "no manager task on $BOARD: set the manager up first" >&2
  exit 2
fi
current=$(jq -r '.[-1].id' <<<"$tasks")
older=$(jq -r '.[:-1][].id' <<<"$tasks")
holder=$(jq -r --arg self "$SELF" '[.[] | .claimed_by // empty | select(. != $self)] | last // ""' <<<"$tasks")
[ -z "$running" ] || holder=$running

if [ -n "$holder" ] && [ "$holder" != "$EXPECTED" ]; then
  echo "the claim is held by $holder, not ${EXPECTED:-nobody}: another shift took over" >&2
  jq -n --arg holder "$holder" '{holder: $holder}'
  exit 3
fi

previous=$(jq -nc --arg self "$SELF" --arg holder "$holder" --argjson cut "$cut" --argjson own "$own" \
  '[($own.previous // [])[], $cut[], $holder] | map(select(. != "" and . != $self)) | unique')
rolled_from=$(jq -r '.rolled_from // "null"' <<<"$own")
[ "$rolled_from" != null ] || [ -z "$running" ] || rolled_from=$(jq -r '.rolled_from // "null"' <<<"$other")
[ -z "$older" ] || rolled_from=$(tail -1 <<<"$older") # a roll cut short after the successor was made

logged=$(jq -r '.logged // false' <<<"$own")
save_progress() { # status, then the summary when done
  jq -n --arg status "$1" --arg thread "$SELF" --argjson previous "$previous" --argjson rolled "$rolled_from" \
    --argjson logged "$logged" --argjson summary "${2:-null}" \
    '{status: $status, thread: $thread, previous: $previous, rolled_from: $rolled, logged: $logged, summary: $summary}' \
    >"$PROGRESS.tmp"
  mv "$PROGRESS.tmp" "$PROGRESS"
}
save_progress running

roll_skipped=null
if [ -z "$older" ]; then
  body=$(kb --json show "$current" | jq -r .body)
  every=$(standing_state <<<"$body" | section Schedule |
    sed -nE 's/^- Roll forward every: ([0-9]+) days?[[:space:]]*$/\1/p' | head -1) || true
  created=$(kb --json show "$current" | jq -r '.created | sub("\\.[0-9]+"; "") | fromdateiso8601')
  if [ $(($(date -u +%s) - created)) -ge $((${every:-1} * 86400)) ]; then
    if ! state=$(standing_state <<<"$body"); then
      roll_skipped='"the task has no ## Log heading outside a code block"'
    elif missing=$(missing_sections <<<"$state") && [ -n "$missing" ]; then
      roll_skipped=$(jq -Rn --arg m "$missing" '"the standing state lacks: " + ($m | split("\n") | join(", "))')
    else
      state=$(set_previous "$current" <<<"$state")
      successor=$(kb --json create "Workspace manager $TODAY" --status todo --tags workspace-manager \
        --body "$(printf '%s\n## Log\n' "$state")" | jq -r .id)
      [ -n "$successor" ] && [ "$successor" != null ] || {
        echo "creating the successor task failed" >&2
        exit 1
      }
      rolled_from=$current
      save_progress running
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

if [ "$logged" != true ]; then
  entry="Takeover by $SELF from $(jq -r 'if length == 0 then "no previous shift" else join(", ") end' <<<"$previous")."
  [ "$rolled_from" = null ] || entry="$entry Rolled forward from #$rolled_from."
  kb edit "$current" --append-body "$entry" --timestamp --claim "$SELF" >/dev/null
  logged=true
  save_progress running
fi

if ! jq -e --arg self "$SELF" --argjson task "$current" '.thread_id == $self and .task_id == $task' "$POINTER" >/dev/null 2>&1; then
  workspace=${WORKSPACE:-$(sed -nE 's/^workspace: *"?([^"]+)"?$/\1/p' /etc/workspace/config.yml 2>/dev/null | head -1)}
  jq -n --arg thread "$SELF" --argjson task "$current" --arg board "$BOARD" --arg since "$(date -u +%FT%TZ)" \
    --arg workspace "$workspace" \
    '{thread_id: $thread, task_id: $task, board: $board, since: $since, workspace: $workspace}' >"$POINTER.tmp"
  mv "$POINTER.tmp" "$POINTER"
fi

summary=$(jq -n --argjson task "$current" --argjson previous "$previous" --argjson rolled "$rolled_from" \
  --argjson skipped "$roll_skipped" '{task: $task, previous_threads: $previous, rolled_from: $rolled, roll_skipped: $skipped}')
save_progress "done" "$summary"
printf '%s\n' "$summary"
