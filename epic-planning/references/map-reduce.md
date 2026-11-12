# Map-Reduce

Split the work into independent chunks, work them in parallel with uniform mappers, then reconcile the mappers' outputs into one deliverable with reducers.

## How to choose

### Advantages

- High throughput: every chunk runs at the same time.
- Each mapper's task is small and alike, so cheaper models often suffice.
- The reducers find what crosses chunk boundaries, so the mappers do not have to.

### Disadvantages

- The split has to be truly independent. A hidden dependency between chunks surfaces late, at the reduce.
- Each reducer waits for every mapper in its batch.
- The mappers must deliver in one format, or the reduce becomes the real work.

### When to use

- Large analysis that partitions cleanly: an audit across modules, processing many documents.
- Many changes of the same kind across a codebase.
- Chunks are mostly independent, and a reducer can resolve what crosses them.

### When NOT to use

- The work does not partition cleanly: a [Swarm](swarm.md) or a [Project](project.md).
- Chunks depend on each other in sequence: a [Chain](chain.md).
- Competing approaches to the same problem: an [Arena](arena.md).

## Planning

### Pre-requisites

- A target that splits into at least two chunks. If it yields fewer, it is not a map-reduce.

### Phase: Split

Partition the target into chunks:

- `by-module`: the modules to be changed or created, one chunk each.
- `by-deliverable`: the distinct deliverables of the epic, one chunk each.
- `by-directory`: the top-level directories of the target path, one chunk each.
- `manual`: when none of these fit, find what does and use it to draw the boundaries.

The number of chunks is the number of mappers.

### Phase: Batches

A reducer takes at most seven mappers. With more chunks than that, group them into batches, each with its own reducer, and add a reducer above the batch reducers to reconcile their results. Batching can nest as deep as it needs to.

A later generation may split again and run another map-reduce on the result.

### Phase: Output

Define what every mapper delivers and where, so that a reducer can read it without the mapper: the format, and where in the epic branch it lands, such as a file under a path the epic names, or the change itself. Each mapper's output merges into the epic branch like any child's. If the mappers' outputs should not ship, the reducer's definition of done says to remove them. Define what each reducer delivers in the same way.

### Phase: Epic task

Write the epic task from the [epic template](../assets/epic.md). Under **Pattern**, add the split, the batches and the output formats.

```bash
kanban-md create "$TITLE" --dir "$BOARD" --tags epic --status backlog --body "$BODY"
```

### Phase: Reducer and mapper tasks

Write the tasks as a tree, with [task-authoring](../../task-authoring/SKILL.md):

- one reducer task per batch, as a child of the epic, or of the reducer above it;
- one mapper task per chunk, as a child of its batch's reducer task;
- each reducer task depends on the tasks below it.

The tree groups each batch under its reducer, and the dependencies set the order: the orchestrator dispatches the mappers first, and each reducer once every task below it is done, so the reducer starts from an epic branch that holds every output it reconciles. Its definition of done says what reconciling means for this epic: what it does with duplicates, conflicts and a missing chunk.

```bash
kanban-md create "$TITLE" --dir "$BOARD" --parent "$EPIC" --status backlog --body "$BODY"     # reducer
kanban-md create "$TITLE" --dir "$BOARD" --parent "$REDUCER" --status backlog --body "$BODY"  # mapper
kanban-md edit "$REDUCER" --dir "$BOARD" --add-dep "$MAPPERS"                                  # once the mappers exist
```
