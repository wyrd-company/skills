# Chain

Reach a measurable goal one link at a time. A link is a task sized to one session, and each link starts from where the last one finished. Links are written as the chain goes, so the work does not have to be planned up front, although it can be. The orchestrator supervises the chain.

## How to choose

### Advantages

- The work does not have to be planned up front.
- The chain reacts to problems as they come up, by adding a link.
- Serial work avoids merge conflicts.

### Disadvantages

- The remaining work is hard to estimate.
- Serial work takes longer.

### When to use

- A hill climb: the effort needed to reach the goal is not known up front, and the chain discovers and adjusts as it goes.
- Keeping work going matters more than when it is delivered. An operator may ask for a chain when there is subscription usage that would otherwise go to waste.

### When NOT to use

- Delivery time matters.
- The work is well defined and knowable: plan it as a [Project](project.md).
- The work would benefit from running in parallel: a [Project](project.md) or [Map-Reduce](map-reduce.md).

## Planning

### Pre-requisites

A goal that:

- says when the chain is complete, by a check that can be measured: a count, a passing suite, an empty queue;
- says when to stop if the goal turns out to be out of reach: a number of links, a number of links without progress, a date;
- decides which links belong to the chain. A link that does not move the chain towards the goal is not part of it.

### Phase: Epic task

Write the epic task from the [epic template](../assets/epic.md). Under **Pattern**, add:

- the completion check and the stop condition;
- how a link chooses its slice: the queue it takes from, the order (foundations first, for example), or the rule it uses when there is no queue.

```bash
kanban-md create "$TITLE" --dir "$BOARD" --tags epic --status backlog --body "$BODY"
```

### Phase: First links

Write the first two links with [task-authoring](../../task-authoring/SKILL.md). Each link's context says how it moves the chain towards the goal.

1. **Setup.** Everything the chain needs before its first slice that the orchestrator does not set up itself (it opens the epic branch): test fixtures or profiles, and, when the slices are not known yet, the queue itself (an inventory of what is missing, for example).
2. **The first slice.** It depends on the setup link.

```bash
kanban-md create "$TITLE" --dir "$BOARD" --parent "$EPIC" --status backlog --body "$BODY"
kanban-md create "$TITLE" --dir "$BOARD" --parent "$EPIC" --depends-on "$SETUP" --status backlog --body "$BODY"
```

Later links are written by the chain as it runs, not by you.
