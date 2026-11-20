# Functions shared by the workspace manager's scripts. Source it; do not run it.
# shellcheck shell=bash

# The sections a manager task's standing state must have, in the template's order.
STANDING_SECTIONS=(Role Schedule Channel Budget Limits "Standing work" Duties Automations "In flight" Requests Holds Notices)

# The awk function that tracks code fences in a Markdown body. fence_check
# returns 1 for a line inside a fence or on one of its fence lines. As
# CommonMark says, a fence closes only with the same character, at least as
# long, and a backtick fence's info string has no backtick, so a line such as
# ```code``` is an inline code span and opens nothing.
# shellcheck disable=SC2016 # an awk program: its $ are awk's
FENCE_AWK='
  function fence_check(line,   m, ch, len, rest) {
    if (match(line, /^ {0,3}(`{3,}|~{3,})/)) {
      m = substr(line, RSTART, RLENGTH); rest = substr(line, RSTART + RLENGTH); sub(/^ +/, "", m)
      ch = substr(m, 1, 1); len = length(m)
      if (!open) {
        if (ch == "`" && index(rest, "`")) return 0
        open = 1; open_ch = ch; open_len = len; return 1
      }
      if (ch == open_ch && len >= open_len && line ~ /^ {0,3}(`+|~+)[[:space:]]*$/) { open = 0; return 1 }
    }
    return open
  }
'

# Print the standing state: a task body read on stdin, above its "## Log"
# heading outside code fences. Fails when the body has no such heading.
standing_state() {
  awk "$FENCE_AWK"'
    { fenced = fence_check($0) }
    !fenced && /^## Log[[:space:]]*$/ { found = 1; exit }
    { print }
    END { exit !found }'
}

# Print the log: a task body read on stdin, below its "## Log" heading.
log_part() {
  awk "$FENCE_AWK"'
    found { print; next }
    { fenced = fence_check($0) }
    !fenced && /^## Log[[:space:]]*$/ { found = 1 }'
}

# Print one section of a standing state read on stdin, without its heading or
# anything inside code fences, which holds examples, not settings.
section() {
  awk -v name="$1" "$FENCE_AWK"'
    { fenced = fence_check($0) }
    fenced { next }
    /^## / { inside = ($0 ~ "^## " name "[[:space:]]*$"); next }
    inside { print }'
}

# Print a standing state read on stdin with its Role section's first
# "- Previous task:" line, outside code fences, set to task $1.
set_previous() {
  awk -v id="$1" "$FENCE_AWK"'
    { fenced = fence_check($0) }
    !fenced && /^## / { role = ($0 ~ /^## Role[[:space:]]*$/) }
    !fenced && role && !done && /^- Previous task: / { print "- Previous task: #" id; done = 1; next }
    { print }'
}

# Print the thread that is the manager now: the thread finishing a takeover
# that was cut short, or else the holder of the claim on the newest open
# manager task. Prints nothing when there is none.
current_holder() {
  local board=$1 cut
  cut=$(jq -r 'select(.status == "running") | .thread // empty' "$board/.takeover.json" 2>/dev/null) || true
  if [ -n "$cut" ]; then
    echo "$cut"
    return
  fi
  kanban-md --json list --tag workspace-manager --status backlog,todo,in-progress,review --sort id --dir "$board" 2>/dev/null |
    jq -r '[.[] | .claimed_by // empty] | last // empty'
}

# Print the sections a standing state on stdin lacks, one per line.
missing_sections() {
  local state name
  state=$(cat)
  for name in "${STANDING_SECTIONS[@]}"; do
    awk -v name="$name" "$FENCE_AWK"'
      { fenced = fence_check($0) }
      !fenced && $0 ~ "^## " name "[[:space:]]*$" { found = 1 }
      END { exit !found }' <<<"$state" || echo "$name"
  done
}

# Print the manager task as kanban-md JSON: the task the pointer file names,
# which must be open, tagged workspace-manager and claimed by the pointer's
# thread; or, before the first takeover has written a pointer, the newest open
# manager task. Returns 2 when the workspace has no manager task at all, and 1,
# with the reason on stderr, when it has one that cannot be read as the pointer
# says.
manager_task() {
  local board=$1 id thread json
  if [ ! -f "$board/manager.json" ]; then
    json=$(kanban-md --json list --tag workspace-manager --status todo,in-progress --sort id --dir "$board" 2>/dev/null |
      jq -ec 'last // empty' 2>/dev/null) || {
      echo "no manager task on $board" >&2
      return 2
    }
    printf '%s\n' "$json"
    return 0
  fi
  id=$(jq -r '.task_id // empty' "$board/manager.json" 2>/dev/null) || true
  thread=$(jq -r '.thread_id // empty' "$board/manager.json" 2>/dev/null) || true
  if [ -z "$id" ]; then
    echo "$board/manager.json names no task" >&2
    return 1
  fi
  if ! json=$(kanban-md --json show "$id" --dir "$board" 2>/dev/null) ||
    ! jq -e --arg thread "$thread" '(.tags // [] | index("workspace-manager")) and .status == "in-progress"
      and .claimed_by == $thread' >/dev/null 2>&1 <<<"$json"; then
    echo "task #$id, named in $board/manager.json, is not the manager task claimed by thread ${thread:-none}" >&2
    return 1
  fi
  printf '%s\n' "$json"
}

# Print the manager task's body. Fails as manager_task does.
manager_body() {
  local json rc=0
  json=$(manager_task "$1") || rc=$?
  [ "$rc" -eq 0 ] || return "$rc"
  jq -r '.body // ""' <<<"$json"
}

# Take the manager's lock on a board, on file descriptor 9, waiting up to 10
# minutes. Takeovers and every write to the manager task hold it.
manager_lock() {
  exec 9>"$1/.manager.lock"
  flock -w 600 9
}
