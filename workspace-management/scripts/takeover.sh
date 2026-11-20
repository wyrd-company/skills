#!/usr/bin/env bash
# Take the workspace manager's claim for this thread, rolling the manager task
# forward when it is due, and record the shift in the pointer file.
#
# Run it after the previous shift's turn has ended. It is safe to run again: a
# roll cut short is finished on the next run.
#
# 1. Finds the manager tasks: tagged workspace-manager and not done or
#    archived. More than one means a roll was cut short: the newest is current,
#    and the older ones are closed.
# 2. Rolls forward when the current task is older than the "Roll forward every"
#    line of its Schedule section (default 1 day): creates a successor with the
#    body above "## Log", claims it, and closes and archives the old task.
# 3. Otherwise takes the claim on the current task.
# 4. Writes <board>/manager.json, and logs the takeover on the current task.
#
# Prints a JSON summary: task, previous_thread ("" for the first shift, or when
# this thread already held the claim), rolled_from (null when no roll happened).
#
# Environment:
#   T3CODE_THREAD_ID  this shift's thread id (required)
#   MANAGER_BOARD     the workspace board (default: /tasks)
#   WORKSPACE         the workspace's name (default: from /etc/workspace/config.yml)
# Exit: 0 done; 1 a step failed; 2 the board has no manager task.
set -euo pipefail

BOARD=${MANAGER_BOARD:-/tasks}
SELF=${T3CODE_THREAD_ID:?T3CODE_THREAD_ID is not set}
POINTER="$BOARD/manager.json"
TODAY=$(date -u +%F)
NOW=$(date -u +%FT%TZ)

kb() { kanban-md "$@" --dir "$BOARD"; }

tasks=$(kb --json list --tag workspace-manager --status backlog,todo,in-progress,review --sort id)
count=$(jq length <<<"$tasks")
if [ "$count" -eq 0 ]; then
  echo "no manager task on $BOARD: set the manager up first" >&2
  exit 2
fi

current=$(jq -r '.[-1].id' <<<"$tasks")
older=$(jq -r '.[:-1][].id' <<<"$tasks")
# The previous shift holds the newest claim that is not ours.
previous=$(jq -r --arg self "$SELF" '[.[] | .claimed_by // empty | select(. != $self)] | last // ""' <<<"$tasks")

close_old() { # close a manager task that has a successor
  kb edit "$1" --append-body "Rolled forward to #$2 by $SELF." --timestamp \
    --release --status "done" --completed "$TODAY" >/dev/null
  kb archive "$1" >/dev/null
}

claim() {
  local status holder
  status=$(kb --json show "$1" | jq -r .status)
  holder=$(kb --json show "$1" | jq -r '.claimed_by // ""')
  if [ "$status" != "in-progress" ]; then
    kb move "$1" in-progress --claim "$SELF" >/dev/null
  elif [ "$holder" != "$SELF" ]; then
    [ -z "$holder" ] || kb edit "$1" --release >/dev/null
    kb edit "$1" --claim "$SELF" >/dev/null
  fi
}

rolled_from=null
[ -z "$older" ] || rolled_from=$(tail -1 <<<"$older") # finishing a roll cut short
already=$(jq -r --arg self "$SELF" --argjson n "$count" 'if $n == 1 and .[0].claimed_by == $self and .[0].status == "in-progress" then "yes" else "" end' <<<"$tasks")
body=$(kb --json show "$current" | jq -r .body)
every=$(sed -nE 's/^- Roll forward every: ([0-9]+) days?$/\1/p' <<<"$body" | head -1)
created=$(kb --json show "$current" | jq -r '.created | sub("\\.[0-9]+"; "") | fromdateiso8601')
if [ -z "$older" ] && [ $(($(date -u +%s) - created)) -ge $((${every:-1} * 86400)) ]; then
  # The standing state is everything above the log; the log stays with the old task.
  head=$(awk '/^## Log$/ {found = 1; print; exit} {print} END {if (!found) print "\n## Log"}' <<<"$body" |
    sed -E "s/^- Previous task: .*/- Previous task: #$current/")
  successor=$(kb --json create "Workspace manager $TODAY" --status todo --tags workspace-manager --body "$head" | jq -r .id)
  [ -n "$successor" ] && [ "$successor" != null ] || {
    echo "creating the successor task failed" >&2
    exit 1
  }
  older=$current
  rolled_from=$current
  current=$successor
fi

if [ -n "$already" ] && [ "$current" = "$(jq -r '.[0].id' <<<"$tasks")" ] && [ -f "$POINTER" ] &&
  [ "$(jq -r .thread_id "$POINTER")" = "$SELF" ]; then
  # Run again in the same shift: nothing to take over.
  jq -n --argjson task "$current" '{task: $task, previous_thread: "", rolled_from: null}'
  exit 0
fi

claim "$current"
for id in $older; do close_old "$id" "$current"; done

workspace=${WORKSPACE:-$(sed -nE 's/^workspace: *"?([^"]+)"?$/\1/p' /etc/workspace/config.yml 2>/dev/null | head -1)}
jq -n --arg thread "$SELF" --argjson task "$current" --arg board "$BOARD" --arg since "$NOW" --arg workspace "$workspace" \
  '{thread_id: $thread, task_id: $task, board: $board, since: $since, workspace: $workspace}' >"$POINTER.tmp"
mv "$POINTER.tmp" "$POINTER"

entry="Takeover by $SELF from ${previous:-no previous shift}."
[ "$rolled_from" = null ] || entry="$entry Rolled forward from #$rolled_from."
kb edit "$current" --append-body "$entry" --timestamp --claim "$SELF" >/dev/null

jq -n --argjson task "$current" --arg previous "$previous" --argjson rolled "$rolled_from" \
  '{task: $task, previous_thread: $previous, rolled_from: $rolled}'
