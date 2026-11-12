# Acceptance

Read this when every child is merged into the epic branch and no executor is still active, or when an acceptance task has closed. It takes the epic from merged children to pull requests ready for the default branch.

Acceptance runs as a task of its own, a child of the epic tagged `acceptance`. Its agent claims that task, not the epic task, logs its result there and closes it, so the epic task stays with this thread.

| The record shows | Do |
|---|---|
| No acceptance task since the last merge | Move the epic task to `review`. Write an acceptance task with [task-authoring](../../task-authoring/SKILL.md): run acceptance as the epic task's **Acceptance** section says, with [user-acceptance-testing](../../executing/references/user-acceptance-testing.md), and close with ACCEPTED or the problems found. Dispatch it. |
| An acceptance task open | Nothing: it is running |
| The latest acceptance task closed with problems | Each problem is a new child, which the acceptance agent wrote with task-authoring. Return the epic task to `in-progress`; the children run as the pattern says. After they merge, acceptance runs again, with a new task. |
| The latest acceptance task closed ACCEPTED | Mark the epic pull requests ready, and notify the operator. Merge them into the default branch only if the epic task's **Authority** section delegates it. Otherwise the operator reviews and merges, and the merge wakes the next pass. |

An acceptance task is a child like any other, so the pattern's "every child is done" includes it. Read the latest acceptance task before starting another.

When the children targeted the default branch, there is no epic pull request: the children are already merged. Once accepted, notify the operator and go straight to [finalize](finalize.md).
