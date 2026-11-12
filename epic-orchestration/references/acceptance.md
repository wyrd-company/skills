# Acceptance

Read this when every child is merged into the epic branch and no executor is still active, or when acceptance has found a problem. It takes the epic from merged children to pull requests ready for the default branch.

1. Move the epic task to `review`, and dispatch acceptance as the epic task's **Acceptance** section says, with [user-acceptance-testing](../../executing/references/user-acceptance-testing.md).
2. A problem found becomes a new child, written with [task-authoring](../../task-authoring/SKILL.md). Return the epic to `in-progress`, and run acceptance again on the new head once the child has merged.
3. Once accepted, mark the epic pull requests ready, and notify the operator.
4. Merge them into the default branch only if the epic task's **Authority** section delegates it. Otherwise the operator reviews and merges, and the merge wakes the next pass.
