#!/usr/bin/env bash
# Survey the workspace for a shift of the workspace manager.
#
# Prints threads, boards, ledgers and health as plain text, in that order. Each
# section either lists what it found or says UNAVAILABLE with the reason. The
# last line is "survey complete" only when every section ran; otherwise it is
# "survey incomplete" and the exit status is 1. Never read a missing section as
# "nothing to do".
#
# Environment:
#   SURVEY_LIMIT  rows listed per group (default 25); counts are always complete
#   TASK_ROOTS    space-separated folders holding boards
#                 (default: /tasks and every /workspace/*/tasks)
# jq programs are single-quoted on purpose: q passes them to jq.
# shellcheck disable=SC2016
set -uo pipefail

LIMIT=${SURVEY_LIMIT:-25}
SELF=${T3CODE_THREAD_ID:-}
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
FAILED=0

unavailable() {
  echo "UNAVAILABLE: $*"
  FAILED=1
}

q() { # jq for a section's output; a failed query marks the survey incomplete
  jq "$@" || unavailable "jq query failed in the section above"
}

# --- Threads -----------------------------------------------------------------
echo "# Threads"
if t3c --json thread list >"$TMP/threads.json" 2>"$TMP/threads.err" &&
  jq -e '.data | type == "array"' "$TMP/threads.json" >/dev/null 2>&1; then
  jq --arg self "$SELF" '
    [.data[] | select(.deletedAt == null and .archivedAt == null)]
    | map(. + {
        settled: (.settledAt != null),
        pinned: (.pinnedAt != null),
        snoozed: (.snoozedUntil != null and (.snoozedUntil | sub("\\.[0-9]+"; "") | fromdateiso8601) > now),
        last: (.latestRunCompletedAt // .updatedAt),
        open_prs: ([.pullRequests[]? | select(.snapshot.state == "open")] | length),
        self: (.id == $self)
      })' "$TMP/threads.json" >"$TMP/live.json" || unavailable "reading the thread list"

  q -r '
    (map(select(.settled | not))) as $u
    | "unsettled: \($u | length) of \(length)",
      "by status: \($u | group_by(.status) | map("\(.[0].status)=\(length)") | join(" "))",
      "agent threads running now (for limits, excluding this one): \(map(select((.self | not) and (.status | IN("running", "starting", "preparing", "queued")))) | length)"
  ' "$TMP/live.json"

  row='"\(.last) \(.id) [\(.createdBy)] \(.title)\(if .open_prs > 0 then " (open PRs: \(.open_prs))" else "" end)"'

  echo
  echo "## Waiting on a person: a pending question or approval"
  q -r "map(select(.pendingRuntimeRequest != null)) | sort_by(.pendingRuntimeRequest.createdAt) | .[] | \"\(.pendingRuntimeRequest.createdAt) \(.pendingRuntimeRequest.kind) \(.id) \(.title)\"" "$TMP/live.json"

  echo
  echo "## Failed or interrupted, not settled"
  q -r "map(select((.settled | not) and (.status | IN(\"failed\", \"interrupted\")))) | sort_by(.last) | .[] | $row + \" \(.lastError // \"\" | tostring | .[0:120])\"" "$TMP/live.json"

  echo
  echo "## Candidates to settle: completed or idle, not settled, pinned, snoozed or waiting (oldest $LIMIT)"
  q -r "map(select((.settled | not) and (.pinned | not) and (.snoozed | not) and (.self | not)
      and .pendingRuntimeRequest == null and (.pendingBackgroundTasks | length) == 0
      and (.status | IN(\"completed\", \"idle\")))) as \$c
    | \"count: \(\$c | length)\", (\$c | sort_by(.last) | .[:$LIMIT][] | $row)" "$TMP/live.json"
else
  unavailable "t3c thread list failed: $(head -c 300 "$TMP/threads.err")"
fi

# --- Boards ------------------------------------------------------------------
echo
echo "# Boards"
ROOTS=${TASK_ROOTS:-"/tasks $(find /workspace -mindepth 2 -maxdepth 2 -name tasks -type d 2>/dev/null | sort | tr '\n' ' ')"}
: >"$TMP/boards.txt"
for root in $ROOTS; do
  [ -d "$root" ] || continue
  find "$root" -maxdepth 4 -name config.yml -not -path '*/.git/*' 2>/dev/null |
    while read -r cfg; do grep -q '^statuses:' "$cfg" && dirname "$cfg"; done >>"$TMP/boards.txt"
done
sort -u -o "$TMP/boards.txt" "$TMP/boards.txt"

if [ ! -s "$TMP/boards.txt" ]; then
  echo "no boards under: $ROOTS"
else
  : >"$TMP/tasks.jsonl"
  while read -r dir; do
    if kanban-md --json list --dir "$dir" >"$TMP/board.json" 2>"$TMP/board.err"; then
      case "$dir" in */epics/*) kind=epic ;; *) kind=board ;; esac
      jq -c --arg dir "$dir" --arg kind "$kind" '.[] | . + {dir: $dir, kind: $kind}' "$TMP/board.json" >>"$TMP/tasks.jsonl" || unavailable "reading $dir"
      q -r --arg dir "$dir" '
        "\($dir): " + (group_by(.status) | map("\(.[0].status)=\(length)") | join(" "))
        + " | todo unclaimed=\(map(select(.status == "todo" and .claimed_by == null)) | length)"' "$TMP/board.json"
    else
      unavailable "kanban-md list --dir $dir: $(head -c 200 "$TMP/board.err")"
    fi
  done <"$TMP/boards.txt"

  jq -s '.' "$TMP/tasks.jsonl" >"$TMP/tasks.json" || unavailable "combining the boards"
  [ -f "$TMP/live.json" ] || echo '[]' >"$TMP/live.json"

  echo
  echo "## Epics: tasks without a parent on boards under epics/"
  q -r 'map(select(.kind == "epic" and .parent == null)) | sort_by(.status)
    | .[] | "\(.status) \(.dir) #\(.id) \(.title) claim=\(.claimed_by // "none")"' "$TMP/tasks.json"
  q -r '"epics in progress (for limits): \(map(select(.kind == "epic" and .parent == null and (.status | IN("in-progress", "review")))) | length)"' "$TMP/tasks.json"

  echo
  echo "## Ready to dispatch: todo, unclaimed, not blocked, dependencies done (boards outside epics/)"
  q -r '
    (map({key: "\(.dir)#\(.id)", value: .status}) | from_entries) as $st
    | map(select(.kind == "board" and .status == "todo" and .claimed_by == null and (.blocked // false | not)
        and (.dir as $d | all((.depends_on // [])[]; $st["\($d)#\(.)"] == "done"))))
    | sort_by(.dir, .id) | .[] | "\(.dir) #\(.id) [\(.priority)] \(.title)"' "$TMP/tasks.json"

  echo
  echo "## Tasks in progress per board outside epics/ (for limits)"
  q -r 'map(select(.kind == "board" and .status == "in-progress")) | group_by(.dir) | .[] | "\(.[0].dir): \(length)"' "$TMP/tasks.json"

  echo
  echo "## Claims whose thread is not running: in-progress or review tasks, epic tasks left out"
  q -r --slurpfile live "$TMP/live.json" '
    ($live[0] | map({key: (.id | ascii_downcase), value: .status}) | from_entries) as $th
    | map(select(.claimed_by != null and (.status | IN("in-progress", "review"))
        and ((.kind == "epic" and .parent == null) | not)))
    | map(. + {thread: ($th[.claimed_by | ascii_downcase] // "not a known thread")})
    | map(select(.thread | IN("running", "starting", "preparing", "queued") | not))
    | .[] | "\(.dir) #\(.id) \(.status) claim=\(.claimed_by) thread=\(.thread) \(.title)"' "$TMP/tasks.json"
fi

# --- Ledgers -----------------------------------------------------------------
echo
echo "# Ledgers"
if ledger list --all --json >"$TMP/ledgers.json" 2>"$TMP/ledgers.err"; then
  [ -f "$TMP/live.json" ] || echo '[]' >"$TMP/live.json"
  q -r --slurpfile live "$TMP/live.json" '
    ($live[0] | map({key: (.id | ascii_downcase), value: (if .settled then "settled" else .status end)}) | from_entries) as $th
    | group_by(.db) | map({db: .[0].db, n: length, thread: ($th[.[0].db] // (if (.[0].db | startswith("task-")) then "task" else "unknown" end))})
    | "ledgers with resources: \(length)",
      (.[] | "\(.db) resources=\(.n) owner=\(.thread)")' "$TMP/ledgers.json"
else
  unavailable "ledger list --all: $(head -c 200 "$TMP/ledgers.err")"
fi

# --- Health ------------------------------------------------------------------
echo
echo "# Health"
df -h /workspace /tmp 2>/dev/null | awk 'NR == 1 || $NF ~ /^\// {print}' || unavailable "df"
if [ -r /sys/fs/cgroup/pids.max ]; then
  echo "processes: $(cat /sys/fs/cgroup/pids.current 2>/dev/null || ps -e --no-headers | wc -l) of $(cat /sys/fs/cgroup/pids.max)"
else
  echo "processes: $(ps -e --no-headers | wc -l) (no cgroup limit readable)"
fi
free -h 2>/dev/null | awk 'NR <= 2' || unavailable "free"

echo
if [ "$FAILED" -eq 0 ]; then
  echo "survey complete"
else
  echo "survey incomplete"
  exit 1
fi
