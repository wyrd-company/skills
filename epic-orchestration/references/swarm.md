# Swarm

Read this on every pass of an epic whose **Pattern** section names Swarm. A swarm has no plan of every step. The drone doing the work decides the next step and writes it as a task for whichever drone suits it. The pass keeps the swarm's conditions: how many drones run, what merges, and when it has finished. How the shape, the leaders and the communication were set up is in [planning's Swarm](../../epic-planning/references/swarm.md).

## How it moves

1. Each drone session takes one task: the task it is dispatched with, or, when drones claim their own, the next one it suits.
2. It does the task. Next steps it finds go on the board as new tasks, children of the epic or of its leader's task, tagged for the drone that suits them. Next steps are not done in the same session.
3. It releases its task for review. The reviewer merges it into the epic branch and closes it.
4. The release and the merge wake passes. While fewer than N drones are running and tasks are ready, the pass dispatches more.

One task per session keeps every drone's context small, and makes the board the swarm's shared state. Drones talk to each other as the **Pattern** section allows, but a message is not the record. What another drone or a later session needs goes on a task.

A leader works its team the way a chain link does. It writes its team's tasks under its own task, makes its task depend on them, and returns its task to `todo`. Once its team's tasks are `done`, its task is ready again, and the leader is dispatched to write the next round, or to close its task when its team's part is done.

```bash
kanban-md edit "$LEADER_TASK" --dir "$BOARD" --add-dep "$TEAM_TASKS"
kanban-md edit "$LEADER_TASK" --dir "$BOARD" --release --status todo
```

## At Start

Release every leader and drone task to `todo`. Dispatch what is ready, up to N.

## Dispatching

Count the drones running: the children of the epic, and of its leaders, that are `in-progress`. Leaders count towards N, and a leader's team stays within the number its leader's task allows. Dispatch from the ready tasks, up to N:

```bash
kanban-md list --dir "$BOARD" --status todo --unblocked --unclaimed --not-blocked --json
```

When drones are assigned, dispatch each ready task to a drone with its task's model, as [dispatch](dispatch.md) describes. When drones claim their own, dispatch one drone for each ready task, with no task named, for the speciality the task's tag names. Add this to its prompt:

```text
Drone, <speciality>. Take your task with kanban-md pick --claim <thread> --tags <speciality> --status todo --move in-progress. If none is ready, stop. Write the next steps you find as tasks, tagged for the drone that suits them; do not do them in this session.
```

A dispatched drone that finds nothing to pick stops without writing anything.

## Review and merge

Every drone's task merges into the epic branch on its own, through the queue in [review and merge](review-and-merge.md). A reviewer who finds a drone undoing or duplicating another's work rejects it and says so: the swarm's boundaries are not clear.

## On each pass

| The record shows | Do |
|---|---|
| Fewer than N drones running, and tasks ready | Dispatch up to N |
| A task released for review | Queue its review, unless it is an arm of a race still waiting for its ruling |
| No open task under the epic, and no drone running | The swarm has stopped: go to [acceptance](acceptance.md), which checks whether the goal is met |
| Drones undoing or duplicating each other's work | Escalate: the ruling redraws the boundaries |
| Tasks being written faster than they close, or the same task written twice | Escalate: the swarm is not converging |
| A race's end condition met | Stop the race, as below |

## Races

Arms of a race run the same task. Each delivers on its own branch.

- **`first pass`:** arms release for review as they finish. The first one accepted merges. Then stop the other arms' sessions, archive their tasks with the reason, and delete their branches.
- **`rank all` and `best-of`:** arms release for review once delivered, but their reviews wait for the ruling. Once every arm is in `review`, escalate once to rank them against the criteria in the **Pattern** section, and log the RACE RULING. Then queue the winner's review, archive the other arms with the ruling, and delete their branches. For `rank all`, the ruling keeps the whole ranking, which is the point of a race between models.

```text
Rank the race of epic task <id> on board <dir> against the criteria in its Pattern section, and log the RACE RULING on the epic task.
```
