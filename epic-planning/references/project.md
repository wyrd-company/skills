# Project

Map the work as a dependency graph of tasks, each with its own sub-goal, and work it in order: in parallel where the graph allows, in sequence where it does not. The orchestrator supervises the assembly.

## How to choose

### Advantages

- The whole route is visible before work starts, so progress can be measured against it.
- Work runs in parallel wherever the graph allows.
- Each task is small and reviewed on its own.

### Disadvantages

- It needs the way to be known up front. A discovery mid-epic can invalidate part of the graph, and the orchestrator has to re-plan.
- Parallel branches into one base produce merge conflicts where tasks touch the same code.
- Planning costs more before the first result arrives.

### When to use

- The issues say what to build and the way to build it is clear.
- The work splits into tasks whose dependencies you can name now.

### When NOT to use

- The way is not known: chart it first, as design work, or climb towards a measurable goal with a [Chain](chain.md).
- One attempt would lock in the wrong shape: run an [Arena](arena.md).
- The work is many uniform, independent chunks: use [Map-Reduce](map-reduce.md).

## Planning

### Pre-requisites

- The goal and bar are set (see [The goal comes first](../SKILL.md#the-goal-comes-first)).
- You have read the code and the documentation the work touches. Do not write code while planning; the plan is the output.

### Phase: Dependency graph

Map what depends on what: data before its readers, a shared contract before the work on either side of it, foundations before what is built on them. The order of work follows the graph from the bottom up.

### Phase: Tasks

Write one task per node of the graph, with [task-authoring](../../task-authoring/SKILL.md). Record each dependency on the task, so the board knows what is ready.

```bash
kanban-md create "$TITLE" --dir "$BOARD" --parent "$EPIC" --depends-on "$IDS" --status backlog --body "$BODY"
```

- Each task leaves the epic's branch in a valid state: checks pass and nothing is half-wired.
- Put the riskiest and least certain tasks early, so the plan fails fast if it is going to.
- Where parallel tasks share a contract (an API, a schema, a file format), make defining the contract its own task, and make the tasks on either side depend on it.
- Run in sequence what changes shared state: migrations, shared configuration, renames across the codebase.

### Phase: Checkpoints

Add a checkpoint where several branches of the graph come together: a task whose definition of done is that the combined work runs end to end on the epic's branch. Problems between tasks are found there, not at the end.

Look for the earliest point where a user could accept part of the work, such as a prototype or the first end-to-end slice, and make acceptance a goal of that task. See [user-acceptance-testing](../../executing/references/user-acceptance-testing.md).

### Phase: Epic task

Write the epic task from the [epic template](../assets/epic.md). Under **Pattern**, name the checkpoint tasks. The graph lives in the children's dependencies; do not restate it in the body.
