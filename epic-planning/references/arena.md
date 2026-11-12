# Arena

Several gladiators produce competing solutions to the same brief, independently and in parallel. A judge reads every candidate end to end, picks the strongest as the base, grafts the best ideas from the others onto it, and verifies the result.

An arena is a constrained [Swarm](swarm.md) whose purpose is the comparison. To take the first candidate that passes instead of comparing them all, race a swarm.

## How to choose

### Advantages

- Many competing outputs, which explore the solution space broadly.
- A wrong shape is caught by comparison instead of being locked in by the first attempt.
- Models and approaches are compared on the same task.

### Disadvantages

- It costs several times the usage of one attempt, plus the judging.
- Grafting ideas from several candidates can produce an incoherent result, so the synthesis needs its own verification.

### When to use

- One attempt at a non-trivial artifact would lock in the wrong shape.
- The outcome benefits from diverse perspectives worked at the same time.
- Evaluating models.

### When NOT to use

- The problem has a straightforward or well-known solution.
- The work has sequential dependencies between workers: a [Chain](chain.md) or a [Project](project.md).

## Planning

### Pre-requisites

- Every gladiator can be given the same brief, and their outputs can be compared side by side.

### Phase: Artifact

Decide the artifact each gladiator produces: its shape and where it is delivered. Each gladiator works on its own branch. Only the synthesis is merged into the target branch.

### Phase: Rubric

State what success looks like for this artifact, then turn it into three to six criteria that can be graded. Concrete: "Adds a `--dry-run` flag that skips writes". Vague: "the code is correct". The rubric is for the judge. It goes on the epic task, not on the gladiators' tasks: gladiators see only their brief.

### Phase: Gladiators

Choose how the gladiators differ:

- `by-model`: different models or model families, from [models.yml](~/models.yml), on the same brief.
- `by-approach`: distinct approaches to the same problem: a dependency, an architecture, how the gladiator is instructed, or any other change of approach.
- `by-grid`: combine the two into a grid of distinct gladiators.

### Phase: Epic task

Write the epic task from the [epic template](../assets/epic.md). Under **Pattern**, add the shape of the artifact, the rubric, and how to apply the rubric to the candidates. The default is to pick one winner as the base and graft the best ideas of the others onto it. If this arena should do something else, say so.

Decide who judges:

- A person: set `hitl` to the handles of the operators who judge, comma-separated, from `git operator list`.
- A council of agents: set `council` to the number of members. With `hitl` also set, the council is in addition to the people.
- Neither: the orchestrator judges.

```bash
kanban-md create "$TITLE" --dir "$BOARD" --tags epic --status backlog \
  --set-property hitl='"boblangley,iradesa"' --set-property council=3 --body "$BODY"
```

### Phase: Gladiator tasks

Write one task per gladiator, as children of the epic, with [task-authoring](../../task-authoring/SKILL.md).

- A gladiator reads and does only what its task says, so each task is complete on its own. Point to the skills and context it must read; do not copy them in.
- The tasks are identical except where the gladiators are meant to differ: the approach, for `by-approach`.
- Set the model and effort for each gladiator, from [models.yml](~/models.yml).

```bash
kanban-md create "$TITLE" --dir "$BOARD" --parent "$EPIC" --status backlog \
  --set-property model='"claude/opus-5.5"' --set-property effort='"high"' --body "$BODY"
```
