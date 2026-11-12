# Recovery

Read this when the work has stopped moving by itself: a task is blocked, a session died or left its claim behind, a handoff looks incomplete, or a reviewer deferred a finding. It says what to check, what to repair, and what to escalate.

- **A blocked task:** check that its blocked entry names the need and the next step, and leave its work surface as it is. Escalate to write the tasks that remove the block, and record the hold. When it clears, resume the original executor, or dispatch a new one with the last handoff as its starting point.
- **A session that died:** read the task, its log and its branch history, and check for unpushed work. Repair the claim, log why, then dispatch. If the evidence is not unambiguous, escalate instead.
- **A claim released with no handoff,** or a status that contradicts the task's own record: return the task to the state its evidence supports, and log why.
- **A handoff that looks incomplete:** do not dispatch onward until it is complete and the previous agent has stopped.
- **A deferred finding** goes into the epic, as a new child written with [task-authoring](../../task-authoring/SKILL.md), or out of it, as an issue. The reviewer recommends; an escalation decides, and the pass logs the ruling on the epic task.

To send the next agent, use [dispatch](dispatch.md).
