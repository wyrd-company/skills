# Review and merge

Read this when a child has been released for review, a review is waiting its turn, or a merge has landed in the epic branch. It keeps the epic branch to one review at a time, in an order the record holds.

Every child gets its own independent review, as in [executing](../../executing/SKILL.md). You dispatch it, in turn, never the executor: an executor of an epic's child releases its task for review and stops.

The merge goes to the reviewer only when the epic task's **Authority** section delegates merging into the branch the children target. Then the acceptance is the authorization, and the reviewer merges at the moment it accepts, when every precondition holds at once, and adds the merge to **What landed** on the epic pull request. Without that authority, the reviewer accepts without merging and hands off. Notify the operator that the merge is theirs, and the merge wakes the next pass. When the children target the default branch, this is a merge into the default branch, and needs authority for that.

- **One review in flight per epic branch,** including remediation rounds. Queue the next until the previous one has merged.
- **The merge queue lives in the epic task's log.** After each merge, log the new head and the remaining order. A reviewer reads it, and starts its final checks only once the merge ahead of it has landed.
- **Ordering is yours to prevent.** If X must not merge before Y, do not dispatch X's review. If you miss it, the reviewer approves the change and rejects the review as "rebase expected", so the next round only checks the rebase.
- **Check after each merge:** the epic branch head, that nothing is unpushed, and that **What landed** was updated.

To dispatch the next review, use [dispatch](dispatch.md).
