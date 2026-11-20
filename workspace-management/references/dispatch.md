# Dispatch

Read this for the budget and the WIP limits every dispatch in the workspace is held to, and when an epic is waiting to start, a task is ready, standing work is due, or a request asks for work. Epic orchestrators read [Limits](#limits) before each dispatch too.

## Budget

The workspace has a budget of usage for each period, set in the manager task's **Budget** section. The manager spends it: work left unstarted while budget remains is work the workspace could have done, and spending past it takes from the next period. The survey's **Budget** section shows what the workspace has spent in the period so far, and the pace: the budget times the share of the period that has passed.

- **Below the pace,** start what is ready, in the order of [the work](../SKILL.md#the-work), until the limits stop you or nothing ready is left. When nothing is left and the spend stays below half the pace, the workspace has more budget than work: tell the operators in [the channel](../SKILL.md#the-channel), once for the period, so they can bring work to it.
- **Above the pace,** start only operators' work and security updates. The rest waits for the pace to catch up.
- **At the budget,** start nothing new. Record the hold in the **Holds** section, and tell the operators once for the period: only an operator may spend past the budget. Work already running continues.

Count the budget before each dispatch, as the limits are counted.

## Limits

The workspace shares one machine. Work started past its capacity does not finish sooner: sessions starve, run out of processes and die with their claims live. The manager task's **Limits** section sets how much may run at once, whatever the budget allows.

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
2. Check the budget, the epic limit and the thread limit.
3. Dispatch its orchestrator with `delegate_task`, on the cheapest model in [models.yml](~/models.yml) that lists the epic task's `complexity`, `normal` when unset:

   ```text
   Start epic task <id> on board <dir>, with the epic-orchestration skill. Copy the git operator from thread <your thread id>.
   ```

4. Log the dispatch and the orchestrator's thread on the manager task.

From here the epic runs itself. You check that it keeps running, as [threads](threads.md#stalled-work) says, and its orchestrator reports to you when it has finished.

## Tasks ready to dispatch

The survey lists the tasks ready to dispatch: in `todo` on the workspace board or a project's board, unclaimed, not blocked, and with every dependency `done`. An epic's children are left out: their orchestrator dispatches them.

1. Read the task itself. It is ready when an executor could start it without asking anyone, as [task-authoring](../../task-authoring/SKILL.md) defines. When it is not, leave it, and notify the operator who wrote it once.
2. Check the budget, the thread limit and the board's limit.
3. Dispatch it with `delegate_task`, highest priority first, then oldest. Use the prompt, the model lookup and the `hitl` rules of epic-orchestration's [dispatch](../../epic-orchestration/references/dispatch.md), without the epic's line, and add `Copy the git operator from thread <your thread id>.` The executor claims the task itself, as [task-ownership](../../task-ownership/SKILL.md) says.
4. Log the dispatch and the executor's thread on the manager task.

A task outside an epic has no orchestrator to queue its review. Its executor dispatches the review, as [executing](../../executing/SKILL.md#independent-review) says.

## Standing work

The manager task's **Standing work** section lists what this workspace does on its own, one row each: what it is, how often it runs, and what does it, which is a prompt, a task to create, or an automation. A row is due when the log has no entry `Standing <name>: dispatched` within its interval.

1. Check the budget and the thread limit.
2. Dispatch it as its row says:
   - **A prompt:** send it with `delegate_task`, adding `Copy the git operator from thread <your thread id>.`, on the model the row names, or the cheapest in [models.yml](~/models.yml) that lists the row's complexity, `normal` when unset.
   - **A task to create:** write it on the board the row names, with [task-authoring](../../task-authoring/SKILL.md), then dispatch it as a [ready task](#tasks-ready-to-dispatch).
   - **An automation:** dispatch nothing. Check that it ran, as [automations](automations.md#check-the-automations) says.
3. Log `Standing <name>: dispatched`, with the thread.

A row that runs the same steps every time, with no judgment in them, is a candidate for an [automation](automations.md#propose-an-automation).

## Requests

An operator may ask the manager for work in a message, in T3 Code or in the channel. Work that needs a task gets one: write it on the workspace board with [task-authoring](../../task-authoring/SKILL.md), or on the board of the project it belongs to, in `todo`. It is then dispatched like any other ready task, within the budget and the limits. A request that changes the budget, a limit, a duty, the standing work or the schedule changes the manager task, as [setup](setup.md#change-the-schedule) says for the schedule.

Record each request in the manager task's **Requests** section until it is done, so it survives the rotation.
