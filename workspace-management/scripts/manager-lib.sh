# Functions shared by the workspace manager's scripts. Source it; do not run it.
# shellcheck shell=bash

# The sections a manager task's standing state must have, in the template's order.
STANDING_SECTIONS=(Role Schedule Channel Budget Limits "Standing work" Duties Automations "In flight" Requests Holds Notices)

# The awk function that tracks code fences in a Markdown body. fence_check
# returns 1 for a line inside a fence or on one of its fence lines. A fence
# closes only with the same character, at least as long, as CommonMark says.
FENCE_AWK='
  function fence_check(line,   m, ch, len) {
    if (match(line, /^ {0,3}(`{3,}|~{3,})/)) {
      m = substr(line, RSTART, RLENGTH); sub(/^ +/, "", m)
      ch = substr(m, 1, 1); len = length(m)
      if (!open) { open = 1; open_ch = ch; open_len = len; return 1 }
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

# Print one section of a standing state read on stdin, without its heading.
section() {
  awk -v name="$1" "$FENCE_AWK"'
    { fenced = fence_check($0) }
    !fenced && /^## / { inside = ($0 ~ "^## " name "[[:space:]]*$"); next }
    inside { print }'
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

# Print the manager task, as the pointer file names it, as kanban-md JSON.
# Fails, with the reason on stderr, when the pointer is missing or names a task
# that is not an open manager task.
manager_task() {
  local board=$1 id json
  id=$(jq -r '.task_id // empty' "$board/manager.json" 2>/dev/null) || true
  if [ -z "$id" ]; then
    echo "no manager task: $board/manager.json is missing or names none" >&2
    return 1
  fi
  if ! json=$(kanban-md --json show "$id" --dir "$board" 2>/dev/null) ||
    ! jq -e '(.tags // [] | index("workspace-manager")) and (.status | IN("todo", "in-progress"))' \
      >/dev/null 2>&1 <<<"$json"; then
    echo "task #$id, named in $board/manager.json, is not an open manager task" >&2
    return 1
  fi
  printf '%s\n' "$json"
}

# Print the manager task's body. Fails as manager_task does.
manager_body() {
  local json
  json=$(manager_task "$1") || return 1
  jq -r '.body // ""' <<<"$json"
}

# Take the manager's lock on a board, on file descriptor 9, waiting up to 10
# minutes. Takeovers and every write to the manager task hold it.
manager_lock() {
  exec 9>"$1/.manager.lock"
  flock -w 600 9
}
