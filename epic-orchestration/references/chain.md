# Chain

Read this on every pass of an epic whose **Pattern** section names Chain. A chain reaches its goal one link at a time, and each link writes the next, so the pass has little to do. It dispatches the next link once the last one has merged, and notices when the chain is done or should stop. How the chain was set up is in [planning's Chain](../../epic-planning/references/chain.md).

## How it moves

1. A link is dispatched on the head of the epic branch.
2. It does its slice, then runs the chain's completion check and logs the result on its own task.
3. If the check does not pass, it writes the next link: a child of the epic task, in `todo`, depending on itself, with its slice chosen as the **Pattern** section says.
4. It releases its task for review. The reviewer merges it into the epic branch and closes it.
5. The merge wakes a pass. The next link is now ready, and the pass dispatches it on the new head.

The next link waits for the merge so that it starts from where the last one finished, not from a branch beside it. One link is in flight at a time, so there is never a queue for review.

## At Start

Release the setup link and the first slice together: the slice depends on the setup, so it waits. Dispatch the setup link.

## Dispatching

Add this to the [dispatch](dispatch.md) prompt:

```text
Chain link <n>. Before you release this task, run the chain's completion check from the epic task's Pattern section and log its result on this task. If it does not pass, write the next link with task-authoring: a child of the epic task, in todo, depending on this task, with its slice chosen as the Pattern section says.
```

Log the dispatch on the epic task: the link's number, its task and the base it started from. The log is how later passes count links for the stop condition.

## On each pass

| The record shows | Do |
|---|---|
| The last link merged and closed, and one next link in `todo` with its dependency met | Dispatch it |
| The last link logged a passing check and wrote no next link | Go to [acceptance](acceptance.md) |
| The stop condition is met: the number of links, links without progress, or the date | Dispatch no further link, and escalate. A goal out of reach changes the outcome, so it usually goes to the operator. |
| A link released with no next link and no passing check | Escalate: the chain has lost its thread |
| More than one next link waiting | Escalate: a chain runs one link at a time |

## Findings

A finding that an escalation takes into the chain becomes a link of its own. Write it to run next, and make the waiting link depend on it too, so the chain takes it first.

```bash
kanban-md create "$TITLE" --dir "$BOARD" --parent "$EPIC" --depends-on "$LAST" --status todo --body "$BODY"
kanban-md edit "$WAITING" --dir "$BOARD" --add-dep "$FINDING"
```
