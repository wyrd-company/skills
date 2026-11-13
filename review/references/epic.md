# Epic

Read this when the task you review is a child of an epic. The orchestrator dispatches reviews one at a time per epic branch, and keeps the order in the epic task's log. What it expects of the orchestrator is in [review and merge](../../epic-orchestration/references/review-and-merge.md); this is the reviewer's side.

## The dispatch

The prompt names the task, the epic task, the base and its head, and whether you merge on acceptance. "Merge on acceptance: yes" is your merge authority. It comes from the epic task's **Authority** section, and nothing else grants it.

Never write to the epic task. Only its holder does. What the orchestrator needs from you goes in the child's handoff, and your release wakes the next pass.

## Order

- **The merge queue is in the epic task's log.** Read it. Start the final checks, the surface check and the merge gates, only once the merge ahead of yours has landed.
- **A task that must not merge yet** is approved and rejected as rebase expected, naming the task it waits on: `Rejected: change approved, rebase expected after <task>`. The next round checks only the rebase.
- **A swarm's drone undoing or duplicating another's work** is rejected with that reason: the swarm's boundaries are not clear, and the orchestrator escalates it.
- **A race's arms:** a `first pass` arm is reviewed as it finishes, and the first one accepted merges. Arms of a `rank all` or `best-of` race wait for the race's ruling, and the orchestrator queues only the winner.

## After you merge

The merge is not finished until the epic pull request shows it. When the children target the default branch, there is no epic pull request: the child's own pull request is the record, so close the task.

1. **Push the epic branch,** fast-forward only, if the merge did not already. Check the remote head equals the merge. The scan of what the push makes public is a merge gate, so it happened before the merge.
2. **Add one line under `## What landed`** in the epic pull request's description: what the change does for the epic's outcome. Edit only that section.
3. **Comment on the epic pull request:** what changed and why, the notable decisions, the validation, and the merged commit range.

Then close the task, as the skill's handoff says. If an epic pull request is expected but does not exist yet, or the push is refused, do not improvise: log the merge as unpublished in the handoff, and escalate.

## Deferred findings

When the executor defers a finding, recommend where it goes: into the epic, as a new child task, when it serves the epic's goal; outside it, as an issue, when it does not. Give the reason in the handoff. The orchestrator escalates the decision and logs the ruling.
