# Map-Reduce

Read this on every pass of an epic whose **Pattern** section names Map-Reduce. Mappers work independent chunks, and reducers reconcile them, a batch at a time. Each reducer depends on the tasks below it, so the board says what is ready, and the pass dispatches everything. How the split, the batches and the output formats were set up is in [planning's Map-Reduce](../../epic-planning/references/map-reduce.md).

## How it moves

1. Every mapper is ready from the start. The pass dispatches each one on the head of the epic branch.
2. Each mapper delivers its output in the format the **Pattern** section defines, and releases for review. The reviewer merges it into the epic branch and closes it.
3. A reducer is ready once every task it depends on is `done`: the mappers of its batch, or the batch reducers below it. The pass dispatches it on the epic head, which now holds every output it reconciles.
4. The reducer reconciles them as its definition of done says, and releases for review, to be merged like any child.
5. Once the top reducer has merged, the epic goes to acceptance.

A reducer reconciles its whole batch once, never a part of it. Reconciling finds duplicates and conflicts across the batch, so a partial reduce would be redone when the rest arrived. To reduce sooner, plan smaller batches.

```bash
kanban-md list --dir "$BOARD" --status todo --unblocked --unclaimed --not-blocked --json
```

## At Start

Release every mapper and reducer to `todo`. The reducers' dependencies keep them waiting.

## Dispatching

Dispatch every ready mapper, unless the **Pattern** section limits how many run at once. Mappers are small and alike, so their `complexity` usually allows a cheap model, and so do their reviews.

Add this to the [dispatch](dispatch.md) prompt of a reducer:

```text
Reducer of batch <name>. The base holds the output of every task this task depends on. Reconcile them as your definition of done says. Chunks ruled missing: <from the epic task's log, or none>.
```

## Review and merge

Many mappers release close together, so the merge queue is long. Put first the mappers of the batch nearest to complete, so that a reducer becomes ready as early as it can. Otherwise keep the order they were released in.

## On each pass

| The record shows | Do |
|---|---|
| A ready mapper or reducer | Dispatch it |
| A mapper or reducer released for review | Queue its review |
| The top reducer `done` | Go to [acceptance](acceptance.md) |
| A mapper that cannot deliver its chunk | Escalate. The ruling retries it, splits it again, or drops it. |
| Mappers that touch the same files, or an output that needs another chunk to make sense | Escalate: the split is not independent, and the ruling may re-split or move the work to another pattern |

## Findings

A finding that an escalation takes into the epic becomes a new mapper in the batch it belongs to, with that batch's reducer depending on it. A reducer already merged is not reopened: the finding gets a reducer of its own.

## Dropping a chunk

When a ruling drops a chunk, the pass archives its mapper with the ruling in its log, and logs the chunk as missing on the epic task. An archived task counts as `done` for its dependents, so the reducer becomes ready, and its prompt names the chunk as missing. Its definition of done says what to do with it.
