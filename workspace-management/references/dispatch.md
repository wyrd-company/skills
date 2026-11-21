# Dispatch

Read this for the budget and the WIP limits every dispatch in the workspace is held to, and when an epic is waiting to start, a task is ready, standing work is due, or a request asks for work. Epic orchestrators read [Limits](#limits) before each dispatch too.

## Budget

The workspace has a budget of usage for each period, set in the manager task's **Budget** section. The manager spends it: work left unstarted while budget remains is work the workspace could have done, and spending past it takes from the next period. `bash scripts/budget.sh`, from this skill's folder, shows what the workspace has spent today and the pace: the budget times the share of the day that has passed. Its first line is the state, which the survey's **Budget** section repeats:

- **Below the pace,** start what is ready, in the order of [the work](../SKILL.md#the-work), until the limits stop you or nothing ready is left. When nothing is left, `Medium` issues included, and the spend stays below half the pace, the workspace has more budget than work: tell the operators in [the channel](../SKILL.md#the-channel), once for the period, so they can bring work to it.
- **Above the pace,** start only operators' work and security updates. The rest waits for the pace to catch up.
- **At the budget,** start nothing new. Record the hold in the **Holds** section, and tell the operators once for the period: only an operator may spend past the budget. Work already running continues.
- **Unknown,** because some of today's usage has no price yet: act as above the pace. When it stays unknown for a day, tell the operators once.
- **Unset:** the manager task has no budget. Start only operators' work, and ask the operator for a budget once.
- **Unavailable:** usage could not be read. Start nothing new until it can, and tell the operators once when it stays unavailable for a day.

Epic orchestrators check the budget too, before each dispatch, and hold at the budget.

Count the budget before each dispatch, as the limits are counted.

## Limits

The workspace shares one machine. Work started past its capacity does not finish sooner: sessions starve, run out of processes and die with their claims live. The manager task's **Limits** section sets how much may run at once, whatever the budget allows.

| Limit | Counted as | The survey line |
|---|---|---|
| Agent threads running at once | Threads in `running`, `starting`, `preparing` or `queued`, your own included | `agent threads running now` |
| Epics in progress at once | Epic tasks in `in-progress` or `review` | `epics in progress` |
| Tasks in progress on one board | Tasks in `in-progress` on a board outside `epics/` | `Tasks in progress per board` |

- **Take a place before you start a thread,** with `bash scripts/admit.sh take <label>`, from this skill's folder, where the label names the work, such as `renovate:<owner>/<repo>` or `review:<board>#<id>`. Everyone who starts a thread in the workspace takes one: the manager, epic orchestrators, and an executor starting its reviewer. A review of work already under way may start at the budget, since that work continues, but it still takes a place. Under a lock, it counts the threads running, yours included, and the places other dispatchers have taken, so two dispatchers cannot both take the last place. Exit 3 means the workspace is at the limit. Exit 5 means that label already holds a place: the same work is being started twice, so start nothing. Exit 1 means the limit or the running threads cannot be read: start nothing. Once `delegate_task` has returned, or the start failed, give the place back with `admit.sh release <label>`: the new thread counts itself from then on.
- **Count the epic and board limits before each dispatch, not once a sweep,** from a fresh survey or `kanban-md list`: tasks start and finish while you work.
- **A dispatch that would reach past a limit waits.** Record it in the manager task's **Holds** section once, with the limit that holds it, and take it up on the first sweep under the limit. A hold that lasts is how operators learn to change a limit.
- **Resuming takes a thread, not a new start.** Remediation sent back to an executor's own session, and a stalled executor resumed in its thread, make that thread run: take a place for them as for a start, but they need none under the epic or board limits, which already count their task.

## Record before you launch

A shift can lose the manager's claim between checking it and starting work, and a dispatched executor claims its task only once it starts. So before every dispatch, write its **In flight** line first, with `manager.sh set-state`: what it is (for a task, `<board> #<id>`), and since when. Launch only when that write succeeds. When it exits 3, you are no longer the manager: give back the place you took, and forward the work to the new manager instead. Then add the delegate's thread to the line.

Never dispatch what has an **In flight** line: the survey marks such a ready task `(in flight)`. Remove a task's line once its executor or orchestrator has claimed it, and any other line when its report comes back. A line older than a day with no claim and no report needs a look: read its thread with `t3c thread status`. While the thread is running or waiting on a person, it is still at work: leave the line. Only when the thread failed, stopped without a result, or never started, remove the line and dispatch again.

## Epics waiting to start

An epic is waiting when its epic task, the task without a parent on a board under `epics/`, is in `todo` and unclaimed. Its planner leaves it there, and messages you so you start it sooner than the next sweep.

1. Check that the planner delivered it, as [epic-planning](../../epic-planning/SKILL.md#what-you-deliver) says: the children staged in `backlog`, and the issues with their goal and bar. When something is missing, notify the planner's operator, and leave the epic waiting.
2. Check the budget, the epic limit and the thread limit.
3. Dispatch its orchestrator with `delegate_task`, on the cheapest model in [models.yml](~/models.yml) that lists the epic task's `complexity`, `normal` when unset:

   ```text
   Start epic task <id> on board <dir>, with the epic-orchestration skill. Copy the git operator from thread <your thread id>.
   ```

4. Log the dispatch and the orchestrator's thread on the manager task. A planner starting the epic because the workspace has no manager takes a place with `admit.sh`, checks the epic limit against the survey's count and the value in [the template](../assets/manager-task.md)'s **Limits** section, and logs on the epic task instead.

From here the epic runs itself. You check that it keeps running, as [threads](threads.md#stalled-work) says, and its orchestrator reports to you when it has finished.

## Tasks ready to dispatch

The survey lists the tasks ready to dispatch: in `todo` on the workspace board or a project's board, unclaimed, not blocked, and with every dependency `done`. An epic's children are left out: their orchestrator dispatches them.

1. Read the task itself. It is ready when an executor could start it without asking anyone, as [task-authoring](../../task-authoring/SKILL.md) defines. When it is not, leave it, and notify the operator who wrote it once.
2. Check the budget, the thread limit and the board's limit.
3. Dispatch it with `delegate_task`, highest priority first, then oldest. Use the prompt, the model lookup and the `hitl` rules of epic-orchestration's [dispatch](../../epic-orchestration/references/dispatch.md), without the epic's line, and add `Copy the git operator from thread <your thread id>.` The executor claims the task itself, as [task-ownership](../../task-ownership/SKILL.md) says.
4. Log the dispatch and the executor's thread on the manager task.

A task outside an epic has no orchestrator to queue its review. Its executor dispatches the review, as [executing](../../executing/SKILL.md#independent-review) says.

## Standing work

The manager task's **Standing work** section lists what this workspace does on its own, one row each: what it is, how often it runs, and what does it, which is a prompt, a task to create, or an automation. A row is due when its **Last dispatched** is older than its interval.

1. Check the budget and the thread limit.
2. Dispatch it as its row says:
   - **A prompt:** send it with `delegate_task`, adding `Copy the git operator from thread <your thread id>.`, on the model the row names, or the cheapest in [models.yml](~/models.yml) that lists the row's complexity, `normal` when unset.
   - **A task to create:** write it on the board the row names, with [task-authoring](../../task-authoring/SKILL.md), then dispatch it as a [ready task](#tasks-ready-to-dispatch).
   - **An automation:** dispatch nothing. Check that it ran, as [automations](automations.md#check-the-automations) says.
3. Set the row's **Last dispatched** to now, and log the dispatch with the thread.

A row that runs the same steps every time, with no judgment in them, is a candidate for an [automation](automations.md#propose-an-automation).

## Requests

An operator may ask the manager for work in a message, in T3 Code or in the channel. Work that needs a task gets one: write it on the workspace board with [task-authoring](../../task-authoring/SKILL.md), or on the board of the project it belongs to, in `todo`. It is then dispatched like any other ready task, within the budget and the limits. A request that changes the budget, a limit, a duty, the standing work or the schedule changes the manager task, as [setup](setup.md#change-the-schedule) says for the schedule.

Record each request in the manager task's **Requests** section until it is done, so it survives the rotation.
