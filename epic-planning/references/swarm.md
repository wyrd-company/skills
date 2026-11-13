# Swarm

Autonomous, specialised drones coordinate among themselves without top-down control. A drone takes the next task it is suited to, and control passes through direct handoffs, messages or shared state, following local rules. The orchestrator sets the conditions, and decides when the swarm has finished.

## How to choose

### Advantages

- Less orchestration: no central plan of every step.
- Modular: each drone, and each kind of drone, can be tested on its own.
- No central bottleneck: the swarm keeps moving when one part is slow.
- Autonomy can grow over time, as the swarm proves itself.

### Disadvantages

- Harder to predict and to trace than a planned epic.
- Drones can duplicate or undo each other's work unless their boundaries are clear.
- Coordination costs messages and attention, and grows with the size of the swarm.

### When to use

- Work across several domains with clear handoff boundaries between them, like an assembly line.
- The sequence of steps cannot be predicted beforehand, so the drone doing the work decides the next step.
- One agent holding every instruction and tool would be overloaded: specialists keep each context small.

### When NOT to use

- Step B must always follow step A: a [Chain](chain.md) or a [Project](project.md).
- The work cannot be undone, or is high risk.
- One agent with a few tools could do it.

## Planning

### Phase: Shape

Decide whether the swarm is partitioned, and how:

- `by-module`: the modules to be changed or created.
- `by-component`: the distinct components of the epic.
- `by-directory`: the top-level directories of the target path.
- `by-expert`: drones that are specialists.
- `by-team`: teams within the swarm.
- `manual`: when none of these fit, find what does and use it to draw the boundaries.

Strategies combine (teams led by an expert, modules by component) and need not be mutually exclusive. A swarm can run several at once, and its strategies can change over time.

Decide whether there are leaders, and whether leaders write their own subtasks.

Decide how the swarm communicates, if at all:

- Which drones may talk to their peers: all of them, or a subset? What defines a peer?
- Is the swarm one group or several?
- Unicast or multicast: `t3_thread_send` to one thread, or `ntfy pub <topic>` to a group.

### Phase: Race

A swarm can also race drones on identical tasks, alone or mixed with a partition. A race ends on a condition. When the point is to compare the candidates and synthesise the best of them, run an [Arena](arena.md) instead. For a race, choose how it ends: `first pass`, `rank all`, or `best-of`. For `rank all` and `best-of`, state the selection criteria. For a race between models, name each arm's model.

### Phase: Epic task

Write the epic task from the [epic template](../assets/epic.md). Under **Pattern**, add:

- how many drones run at once (N): the operator's number when given, otherwise derived from the shape;
- how drones get their tasks: assigned, or claimed by each drone, and whether that changes in phases;
- how partition and race tasks are dispatched;
- the shape, the communication rules, and the race's end condition and criteria;
- the epic branch, when the swarm partitions or races with `rank all` or `best-of`.

```bash
kanban-md create "$TITLE" --dir "$BOARD" --tags epic --status backlog --body "$BODY"
```

### Phase: Leader tasks

One task per leader, as a child of the epic. It says how many of its team's tasks may run at once, within the epic's N, and whether the leader writes its team's tasks. A leader works in rounds: it writes a round of its team's tasks, waits on them, and writes the next round or closes its task.

### Phase: Drone tasks

Write the drone tasks for the shape you chose, with [task-authoring](../../task-authoring/SKILL.md), as children of the epic or of a leader's task.

- A drone reads and does only what its task says, so each task is complete on its own. Point to the skills and context it must read; do not copy them in.
- When drones claim their own tasks, tag each task with the speciality that suits it. Drones pick by that tag.
- For a race, write the same task once per arm.
- Set each task's `complexity`. For a race between models, also set each arm's `model` and `effort`, from [models.yml](~/models.yml).

```bash
kanban-md create "$TITLE" --dir "$BOARD" --parent "$EPIC" --status backlog \
  --set-property model='"claude/opus-5.5"' --set-property effort='"high"' --body "$BODY"
```
