#!/usr/bin/env bash
# The one way a shift reads the manager or writes to the manager task. Every
# command that checks or writes holds the same lock as takeover.sh, so none of
# them runs while a takeover is under way: a shift that has been superseded
# finds out, and nothing it writes is lost in a roll.
#
# Usage:
#   manager.sh holder                  Print the manager now: {"holder": <thread>}.
#                                      During a takeover cut short, the thread taking over.
#   manager.sh state                   Print the manager task's standing state.
#   manager.sh log <text>              Append <text> to the manager task's log.
#   manager.sh set-state <new> <old>   Replace the standing state with file <new>'s,
#                                      keeping the log, only if it is still file <old>'s:
#                                      the state you read with `state` and edited.
#
# log and set-state act only for the manager: T3CODE_THREAD_ID must be the
# holder. Otherwise they exit 3 and print {"holder": <thread>}, so the caller
# can forward what it meant to record.
#
# Environment:
#   T3CODE_THREAD_ID  this thread's id (required for log and set-state)
#   MANAGER_BOARD     the workspace board (default: /tasks)
# Exit: 0 done; 1 failed, such as a state missing a section or a manager task
# that cannot be read; 2 the workspace has no manager; 3 you are not the manager; 4 the lock was not free within 10
# minutes; 5 your own takeover is unfinished: run takeover.sh again; 6 the state
# changed since you read it: read it again and redo your change.
set -euo pipefail
# shellcheck source=manager-lib.sh source-path=SCRIPTDIR
source "$(dirname "${BASH_SOURCE[0]}")/manager-lib.sh"

BOARD=${MANAGER_BOARD:-/tasks}
COMMAND=${1:?usage: manager.sh holder | state | log <text> | set-state <new> <old>}

if [ "$COMMAND" = state ]; then
  rc=0
  body=$(manager_body "$BOARD") || rc=$?
  [ "$rc" -eq 0 ] || exit "$rc"
  state=$(standing_state <<<"$body") || {
    echo "the manager task has no ## Log heading outside a code block: ask an operator to repair it" >&2
    exit 1
  }
  printf '%s\n' "$state"
  exit 0
fi

manager_lock "$BOARD" || {
  echo "the manager lock on $BOARD was not free within 10 minutes" >&2
  exit 4
}
holder=$(current_holder "$BOARD")
if [ -z "$holder" ]; then
  echo "the workspace has no manager: no takeover under way and no claim on a manager task" >&2
  exit 2
fi

if [ "$COMMAND" = holder ]; then
  jq -n --arg holder "$holder" '{holder: $holder}'
  exit 0
fi

SELF=${T3CODE_THREAD_ID:?T3CODE_THREAD_ID is not set}
if [ "$holder" != "$SELF" ]; then
  jq -n --arg holder "$holder" '{holder: $holder}'
  exit 3
fi
if jq -e --arg self "$SELF" '.status == "running" and .thread == $self' "$BOARD/.takeover.json" >/dev/null 2>&1; then
  echo "your takeover is unfinished: run takeover.sh again, then retry" >&2
  exit 5
fi
task=$(manager_task "$BOARD") || exit 2
id=$(jq -r .id <<<"$task")
if [ "$(jq -r '.claimed_by // ""' <<<"$task")" != "$SELF" ]; then
  echo "the pointer names task #$id, which you do not hold: run takeover.sh again" >&2
  exit 5
fi

case "$COMMAND" in
log)
  text=${2:?usage: manager.sh log <text>}
  kanban-md edit "$id" --append-body "$text" --timestamp --claim "$SELF" --dir "$BOARD" >/dev/null
  ;;
set-state)
  new=${2:?usage: manager.sh set-state <new> <old>}
  old=${3:?usage: manager.sh set-state <new> <old>}
  body=$(jq -r '.body // ""' <<<"$task")
  current=$(standing_state <<<"$body") || {
    echo "the manager task has no ## Log heading outside a code block: ask an operator to repair it" >&2
    exit 1
  }
  if [ "$current" != "$(cat "$old")" ]; then
    echo "the standing state changed since you read it: read it again and redo your change" >&2
    exit 6
  fi
  state=$(cat "$new")
  missing=$(missing_sections <<<"$state")
  if [ -n "$missing" ]; then
    echo "$new lacks the sections: $(paste -sd, <<<"$missing")" >&2
    exit 1
  fi
  log=$(log_part <<<"$body")
  merged=$(printf '%s\n## Log\n%s' "$state" "$log")
  # The new state must read back exactly, with the log below it: an unclosed
  # code fence or a ## Log heading in it would hide or swallow the log.
  if [ "$(standing_state <<<"$merged")" != "$state" ] || [ "$(log_part <<<"$merged")" != "$log" ]; then
    echo "$new does not read back as a standing state: check for an unclosed code fence or a ## Log heading" >&2
    exit 1
  fi
  kanban-md edit "$id" --body "$merged" --claim "$SELF" --dir "$BOARD" >/dev/null
  ;;
*)
  echo "unknown command: $COMMAND" >&2
  exit 1
  ;;
esac
