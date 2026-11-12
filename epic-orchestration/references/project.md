# Project

Read this on every pass of an epic whose **Pattern** section names Project. A project is a dependency graph of tasks, and the graph lives in the children's dependencies, so the board says what is ready. The pass dispatches what is ready, keeps the merges in order, and escalates when the graph stops matching the work. How the graph was set up is in [planning's Project](../../epic-planning/references/project.md).

## How it moves

1. A child is ready when it is in `todo`, unclaimed, not blocked, and every task it depends on is `done`.
2. The pass dispatches every ready child on the head of the epic branch.
3. Each child releases for review. The reviewer merges it into the epic branch and closes it.
4. The merge wakes a pass. The children that depended on the merged one may now be ready, and they start from a head that holds what they depend on.

A dependency is met only at `done`, after the merge, so a child never starts on work that has not landed.

```bash
kanban-md list --dir "$BOARD" --parent "$EPIC" --status todo --unblocked --unclaimed --not-blocked --json
```

## At Start

Release every child to `todo`. Its dependencies keep it waiting until it is ready.

## Dispatching

Dispatch every ready child, unless the **Pattern** section limits how many run at once: then dispatch up to the limit, in the order of `list`. Children running at once share a base and cannot see each other's work, so name the surfaces in play in each prompt, as [dispatch](dispatch.md) describes.

A checkpoint is dispatched like any other child. Its work is to run the combined branches end to end. When it carries an acceptance goal, notify the operator once it is ready for them.

## Review and merge

Several children can be released for review at once. Queue them, one review in flight, as [review and merge](review-and-merge.md) describes. Put first the child that the most waiting children depend on, and otherwise keep the order they were released in.

## On each pass

| The record shows | Do |
|---|---|
| A ready child | Dispatch it |
| A child released for review | Queue its review |
| Every child `done`, checkpoints included | Go to [acceptance](acceptance.md) |
| Children in `todo`, none ready, and nothing in flight | Escalate: the graph is stuck, on a cycle or on a dependency that cannot finish |
| An executor, reviewer or checkpoint reports that the way the graph assumed does not hold | Escalate to re-plan |

## Findings

A finding that an escalation takes into the epic becomes a child of its own, with the dependencies the escalation rules. When a waiting child must take it first, make that child depend on it too:

```bash
kanban-md edit "$WAITING" --dir "$BOARD" --add-dep "$FINDING"
```

## Re-planning

A discovery can invalidate part of the graph. Re-planning is judgment, so it belongs to an escalation, with planning's Project reference. It adds children, and changes dependencies with `--add-dep` and `--remove-dep`. It does not edit or remove a child that is claimed. It logs the ruling on the epic task.

A dependency on a task that no longer exists counts as met. Before removing a child, move its dependents onto whatever replaces it, or they become ready at once.
