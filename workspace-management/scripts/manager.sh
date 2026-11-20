#!/usr/bin/env bash
# The one way a shift reads the manager or writes to the manager task. Every
# command that checks or writes holds the same lock as takeover.sh, so none of
# them runs while a takeover is under way: a shift that has been superseded
# finds out, and nothing it writes is lost in a roll.
#
# Usage:
#   manager.sh holder            Print the manager now: {"holder": <thread>}.
#                                During a takeover cut short, the thread taking over.
#   manager.sh state             Print the manager task's standing state.
#   manager.sh log <text>        Append <text> to the manager task's log.
#   manager.sh set-state <file>  Replace the standing state with <file>'s; the log is kept.
#
# log and set-state act only for the manager: T3CODE_THREAD_ID must be the
# holder. Otherwise they exit 3 and print {"holder": <thread>}, so the caller can
# forward what it meant to record.
#
# Environment:
#   T3CODE_THREAD_ID  this thread's id (required for log and set-state)
#   MANAGER_BOARD     the workspace board (default: /tasks)
# Exit: 0 done; 1 failed, such as a standing state missing a section; 2 the
# workspace has no manager; 3 you are not the manager; 4 the lock was not free
# within 10 minutes.
set -euo pipefail
# shellcheck source=manager-lib.sh source-path=SCRIPTDIR
source "$(dirname "${BASH_SOURCE[0]}")/manager-lib.sh"

BOARD=${MANAGER_BOARD:-/tasks}
COMMAND=${1:?usage: manager.sh holder | state | log <text> | set-state <file>}

if [ "$COMMAND" = state ]; then
  body=$(manager_body "$BOARD") || exit 2
  standing_state <<<"$body" || {
    echo "the manager task has no ## Log heading outside a code block" >&2
    exit 1
  }
  exit 0
fi

[ -f "$BOARD/manager.json" ] || {
  echo "no $BOARD/manager.json: the workspace has no manager" >&2
  exit 2
}
manager_lock "$BOARD" || {
  echo "the manager lock on $BOARD was not free within 10 minutes" >&2
  exit 4
}

# The manager: the thread finishing a takeover that was cut short, or else the
# holder of the claim on the task the pointer names.
holder=$(jq -r 'select(.status == "running") | .thread // empty' "$BOARD/.takeover.json" 2>/dev/null) || true
if [ -z "$holder" ]; then
  task=$(manager_task "$BOARD") || exit 2
  holder=$(jq -r '.claimed_by // ""' <<<"$task")
fi

if [ "$COMMAND" = holder ]; then
  jq -n --arg holder "$holder" '{holder: $holder}'
  exit 0
fi

SELF=${T3CODE_THREAD_ID:?T3CODE_THREAD_ID is not set}
task=$(manager_task "$BOARD") || exit 2
id=$(jq -r .id <<<"$task")
if [ "$holder" != "$SELF" ] || [ "$(jq -r '.claimed_by // ""' <<<"$task")" != "$SELF" ]; then
  jq -n --arg holder "$holder" '{holder: $holder}'
  exit 3
fi

case "$COMMAND" in
log)
  text=${2:?usage: manager.sh log <text>}
  kanban-md edit "$id" --append-body "$text" --timestamp --claim "$SELF" --dir "$BOARD" >/dev/null
  ;;
set-state)
  file=${2:?usage: manager.sh set-state <file>}
  state=$(cat "$file")
  if standing_state <<<"$state" >/dev/null; then
    echo "$file has a ## Log heading: give the standing state only" >&2
    exit 1
  fi
  missing=$(missing_sections <<<"$state")
  if [ -n "$missing" ]; then
    echo "$file lacks the sections: $(paste -sd, <<<"$missing")" >&2
    exit 1
  fi
  log=$(jq -r '.body // ""' <<<"$task" | log_part)
  kanban-md edit "$id" --body "$(printf '%s\n## Log\n%s' "$state" "$log")" --claim "$SELF" --dir "$BOARD" >/dev/null
  ;;
*)
  echo "unknown command: $COMMAND" >&2
  exit 1
  ;;
esac
