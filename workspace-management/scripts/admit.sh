#!/usr/bin/env bash
# Admission to the workspace's thread limit, for everyone who starts a thread:
# the manager and epic orchestrators alike. Counting threads and then starting
# one leaves a gap in which another dispatcher counts the same free place;
# taking a place here closes it.
#
# Usage:
#   admit.sh take <label>     Take a place for the thread you are about to start.
#   admit.sh release <label>  Give it back once delegate_task has returned: the new
#                             thread then counts itself. Also when the start failed.
#
# take counts, under a lock, the agent threads running now (running, starting,
# preparing or queued, your own included) and the places taken and not yet
# released, against "Agent threads running at once" in the manager task's
# Limits section, or the template's value when there is no manager. A place
# not released lapses after 15 minutes. Below the limit, take records the place
# and exits 0. At the limit, it exits 3, printing the count.
#
# Environment:
#   MANAGER_BOARD  the workspace board (default: /tasks)
# Exit: 0 done; 1 the running threads could not be counted; 3 at the limit;
# 4 the lock was not free within a minute.
set -euo pipefail
# shellcheck source=manager-lib.sh source-path=SCRIPTDIR
source "$(dirname "${BASH_SOURCE[0]}")/manager-lib.sh"

BOARD=${MANAGER_BOARD:-/tasks}
PLACES="$BOARD/.admissions.json"
COMMAND=${1:?usage: admit.sh take <label> | release <label>}
LABEL=${2:?usage: admit.sh take <label> | release <label>}
NOW=$(date -u +%s)

exec 8>"$BOARD/.admit.lock"
flock -w 60 8 || {
  echo "the admission lock on $BOARD was not free within a minute" >&2
  exit 4
}

places='[]'
[ ! -s "$PLACES" ] || places=$(jq -c --argjson now "$NOW" 'map(select(.at > $now - 900))' "$PLACES")
save() {
  printf '%s\n' "$1" >"$PLACES.tmp"
  mv "$PLACES.tmp" "$PLACES"
}

if [ "$COMMAND" = release ]; then
  save "$(jq -c --arg label "$LABEL" 'map(select(.label != $label))' <<<"$places")"
  exit 0
fi
[ "$COMMAND" = take ] || {
  echo "unknown command: $COMMAND" >&2
  exit 1
}

limits() { section Limits | sed -nE 's/^\| *Agent threads running at once[^|]*\| *([0-9]+) *\|.*/\1/p' | head -1; }
limit=""
if body=$(manager_body "$BOARD" 2>/dev/null); then
  limit=$(standing_state <<<"$body" | limits) || true
fi
[ -n "$limit" ] || limit=$(limits <"$(dirname "${BASH_SOURCE[0]}")/../assets/manager-task.md")

running=$(t3c --json thread list 2>/dev/null |
  jq -e '[.data[] | select(.deletedAt == null and .archivedAt == null
    and (.status | IN("running", "starting", "preparing", "queued")))] | length') || {
  echo "t3c thread list failed: the running threads cannot be counted" >&2
  exit 1
}
taken=$(jq length <<<"$places")
if [ $((running + taken)) -ge "$limit" ]; then
  echo "at the limit: $running running and $taken places taken, of $limit"
  exit 3
fi
save "$(jq -c --arg label "$LABEL" --argjson now "$NOW" 'map(select(.label != $label)) + [{label: $label, at: $now}]' <<<"$places")"
echo "admitted: $((running + taken + 1)) of $limit"
