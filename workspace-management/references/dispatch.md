# Dispatch

Read this when an epic is waiting to start, a task is ready, or a request asks for work, and for the WIP limits that every dispatch in the workspace is held to. Epic orchestrators read [Limits](#limits) before each dispatch too.

## Limits

The workspace shares one machine and one pool of usage. Work started past its capacity does not finish sooner: sessions starve, run out of processes and die with their claims live. The manager task's **Limits** section sets how much may run at once.

| Limit | Counted as | The survey line |
|---|---|---|
| Agent threads running at once | Threads in `running`, `starting`, `preparing` or `queued`, except your own | `agent threads running now` |
| Epics in progress at once | Epic tasks in `in-progress` or `review` | `epics in progress` |
| Tasks in progress on one board | Tasks in `in-progress` on a board outside `epics/` | `Tasks in progress per board` |

- **Count before each dispatch, not once a sweep.** Threads start and finish while you work, and other dispatchers start them too.
- **A dispatch that would reach past a limit waits.** Record it in the manager task's **Holds** section once, with the limit that holds it, and take it up on the first sweep under the limit. A hold that lasts is how operators learn to change a limit.
- **Resuming does not count as starting.** Remediation sent back to an executor's own session, and a stalled executor resumed in its thread, continue work already counted.

## Epics waiting to start

An epic is waiting when its epic task, the task without a parent on a board under `epics/`, is in `todo` and unclaimed. Its planner leaves it there, and messages you so you start it sooner than the next sweep.

1. Check that the planner delivered it, as [epic-planning](../../epic-planning/SKILL.md#what-you-deliver) says: the children staged in `backlog`, and the issues with their goal and bar. When something is missing, notify the planner's operator, and leave the epic waiting.
2. Check the epic limit and the thread limit.
3. Dispatch its orchestrator with `delegate_task`, on the cheapest model in [models.yml](~/models.yml) that lists the epic task's `complexity`, `normal` when unset:

   ```text
   Start epic task <id> on board <dir>, with the epic-orchestration skill. Copy the git operator from thread <your thread id>.
   ```

4. Log the dispatch and the orchestrator's thread on the manager task.

From here the epic runs itself. You check that it keeps running, as [threads](threads.md#stalled-work) says, and its orchestrator reports to you when it has finished.

## Tasks ready to dispatch

The survey lists the tasks ready to dispatch: in `todo` on the workspace board or a project's board, unclaimed, not blocked, and with every dependency `done`. An epic's children are left out: their orchestrator dispatches them.

1. Read the task itself. It is ready when an executor could start it without asking anyone, as [task-authoring](../../task-authoring/SKILL.md) defines. When it is not, leave it, and notify the operator who wrote it once.
2. Check the thread limit and the board's limit.
3. Dispatch it with `delegate_task`, highest priority first, then oldest. Use the prompt, the model lookup and the `hitl` rules of epic-orchestration's [dispatch](../../epic-orchestration/references/dispatch.md), without the epic's line, and add `Copy the git operator from thread <your thread id>.` The executor claims the task itself, as [task-ownership](../../task-ownership/SKILL.md) says.
4. Log the dispatch and the executor's thread on the manager task.

A task outside an epic has no orchestrator to queue its review. Its executor dispatches the review, as [executing](../../executing/SKILL.md#independent-review) says.

## Requests

An operator may ask the manager for work in a message. Work that needs a task gets one: write it on the workspace board with [task-authoring](../../task-authoring/SKILL.md), or on the board of the project it belongs to, in `todo`. It is then dispatched like any other ready task, within the limits. A request that changes a limit, a duty or the schedule changes the manager task, as [setup](setup.md#change-the-schedule) says for the schedule.

Record each request in the manager task's **Requests** section until it is done, so it survives the rotation.
