#!/usr/bin/env bash
# Admission to the workspace's thread limit, for everyone who starts a thread:
# the manager, epic orchestrators, and executors starting their reviewer.
# Counting threads and then starting one leaves a gap in which another
# dispatcher counts the same free place; taking a place here closes it.
#
# Usage:
#   admit.sh take <label>     Take a place for the thread you are about to start.
#                             The label names the work, such as renovate:<owner>/<repo>.
#   admit.sh release <label>  Give it back once delegate_task has returned: the new
#                             thread then counts itself. Also when the start failed.
#
# take counts, under a lock, the agent threads running now (running, starting,
# preparing or queued, your own included) and the places taken and not yet
# released, against "Agent threads running at once" in the manager task's
# Limits section, or the template's value when the workspace has no manager
# task. Below the limit, take records the place and exits 0. At the limit, it
# exits 3, printing the count. A label that already holds a place is refused
# with exit 5: the same work is being started twice.
#
# A place is held for the thread that took it (T3CODE_THREAD_ID). It lapses
# when that thread has stopped running and 10 minutes have passed, or after 6
# hours in any case, so a dispatcher that died does not hold it for ever.
#
# Environment:
#   T3CODE_THREAD_ID  the dispatching thread's id
#   MANAGER_BOARD     the workspace board (default: /tasks)
# Exit: 0 done; 1 the threads or the limit could not be read; 3 at the limit;
# 4 a lock was not free in time; 5 the label already holds a place.
set -euo pipefail
# shellcheck source=manager-lib.sh source-path=SCRIPTDIR
source "$(dirname "${BASH_SOURCE[0]}")/manager-lib.sh"

BOARD=${MANAGER_BOARD:-/tasks}
PLACES="$BOARD/.admissions.json"
COMMAND=${1:?usage: admit.sh take <label> | release <label>}
LABEL=${2:?usage: admit.sh take <label> | release <label>}
SELF=${T3CODE_THREAD_ID:-unknown}
NOW=$(date -u +%s)
TEMPLATE="$(dirname "${BASH_SOURCE[0]}")/../assets/manager-task.md"

limits() { section Limits | sed -nE 's/^\| *Agent threads running at once[^|]*\| *([0-9]+) *\|.*/\1/p' | head -1; }

if [ "$COMMAND" = take ]; then
  # Read the limit once any takeover under way has finished, then let go of
  # the manager's lock.
  manager_lock "$BOARD" || {
    echo "the manager lock on $BOARD was not free within 10 minutes" >&2
    exit 4
  }
  rc=0
  body=$(manager_body "$BOARD" 2>/dev/null) || rc=$?
  exec 9>&-
  if [ "$rc" -eq 2 ]; then
    limit=$(limits <"$TEMPLATE")
  elif [ "$rc" -ne 0 ] || ! state=$(standing_state <<<"$body") || ! limit=$(limits <<<"$state") || [ -z "$limit" ]; then
    echo "the thread limit cannot be read from the manager task: start nothing" >&2
    exit 1
  fi
fi

exec 8>"$BOARD/.admit.lock"
flock -w 60 8 || {
  echo "the admission lock on $BOARD was not free within a minute" >&2
  exit 4
}
save() {
  printf '%s\n' "$1" >"$PLACES.tmp"
  mv "$PLACES.tmp" "$PLACES"
}
places='[]'
[ ! -s "$PLACES" ] || places=$(cat "$PLACES")

if [ "$COMMAND" = release ]; then
  save "$(jq -c --arg label "$LABEL" 'map(select(.label != $label))' <<<"$places")"
  exit 0
fi
[ "$COMMAND" = take ] || {
  echo "unknown command: $COMMAND" >&2
  exit 1
}

threads=$(t3c --json thread list 2>/dev/null | jq -ce '[.data[] | select(.deletedAt == null and .archivedAt == null
    and (.status | IN("running", "starting", "preparing", "queued"))) | .id]') || {
  echo "t3c thread list failed: the running threads cannot be counted" >&2
  exit 1
}
places=$(jq -c --argjson now "$NOW" --argjson live "$threads" '
  map(select(.at > $now - 21600 and ((.thread as $t | $live | index($t)) or .at > $now - 600)))' <<<"$places")
if jq -e --arg label "$LABEL" 'any(.[]; .label == $label)' >/dev/null <<<"$places"; then
  echo "$LABEL already holds a place: the same work is being started twice" >&2
  exit 5
fi
running=$(jq length <<<"$threads")
taken=$(jq length <<<"$places")
if [ $((running + taken)) -ge "$limit" ]; then
  echo "at the limit: $running running and $taken places taken, of $limit"
  exit 3
fi
save "$(jq -c --arg label "$LABEL" --arg thread "$SELF" --argjson now "$NOW" \
  '. + [{label: $label, thread: $thread, at: $now}]' <<<"$places")"
echo "admitted: $((running + taken + 1)) of $limit"
