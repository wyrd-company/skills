# Command-line Interfaces

- Allow dry-runs for mutations (`--dry-run`)
- Embed skills for agents (`--skill` or `--skills`) with an option to extract (`--to-path`) a multi-file skill.
  - Print the SKILL.md to standard out by default
  - Allow a user to extract the entire skill when requested (`--to-path`)
  - Provide a list sub-command when multiple skills are embedded (`--list`). This must include the name, description, and command to output each.