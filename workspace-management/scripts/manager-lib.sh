# Functions shared by the workspace manager's scripts. Source it; do not run it.
# shellcheck shell=bash

# The sections a manager task's standing state must have, in the template's order.
STANDING_SECTIONS=(Role Schedule Channel Budget Limits "Standing work" Duties Automations "In flight" Requests Holds Notices)

# Print the standing state: a task body read on stdin, above its "## Log"
# heading. Headings inside code fences do not count. Fails when the body has no
# such heading.
standing_state() {
  awk '
    /^[[:space:]]*(```|~~~)/ { fence = !fence }
    !fence && /^## Log[[:space:]]*$/ { found = 1; exit }
    { print }
    END { exit !found }'
}

# Print the sections a standing state on stdin lacks, one per line.
missing_sections() {
  local state section
  state=$(cat)
  for section in "${STANDING_SECTIONS[@]}"; do
    grep -qE "^## ${section}[[:space:]]*$" <<<"$state" || echo "$section"
  done
}

# Print the current manager task's body, as the pointer file names it. Fails,
# with the reason on stderr, when the pointer or its task cannot be read.
manager_body() {
  local board=$1 id
  id=$(jq -r '.task_id // empty' "$board/manager.json" 2>/dev/null) || true
  if [ -z "$id" ]; then
    echo "no manager task: $board/manager.json is missing or names none" >&2
    return 1
  fi
  kanban-md --json show "$id" --dir "$board" 2>/dev/null | jq -er '.body // empty' 2>/dev/null || {
    echo "manager task #$id, named in $board/manager.json, cannot be read" >&2
    return 1
  }
}
