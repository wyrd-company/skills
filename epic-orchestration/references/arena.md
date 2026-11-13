# Arena

Read this on every pass of an epic whose **Pattern** section names Arena, and when you are asked to judge one. Gladiators build competing candidates to one brief, each on its own branch. Judges grade every candidate against the rubric, a ruling picks the base and the ideas to graft, and a synthesis task builds the result. Only the synthesis merges. How the arena was set up is in [planning's Arena](../../epic-planning/references/arena.md).

## How it moves

1. The pass dispatches every gladiator, each on its own branch from the epic head, with the model and effort its task sets.
2. Each gladiator delivers its candidate on its branch, and closes its task. The judging is its review, so a candidate is neither reviewed nor merged on its own.
3. Once every gladiator is `done`, the pass opens a draft pull request for each candidate into the epic branch, and starts the judging.
4. The judges grade the candidates, and their verdicts are combined into one ruling, logged on the epic task.
5. The pass dispatches the synthesis task with the ruling. The synthesis releases for review and merges like any child.
6. Once it has merged, the pass closes the candidate pull requests with a link to the synthesis, deleting their branches, and the epic goes to acceptance.

The candidates stay independent until the judging: a gladiator sees only its own task, never the epic task, the rubric or another candidate.

## At Start

Release every gladiator and the synthesis task to `todo`. The synthesis depends on the gladiators, so it waits. Dispatch every gladiator.

## Dispatching

A gladiator's [dispatch](dispatch.md) prompt names neither the epic task nor the surfaces in play, since both would point it at the rest of the arena. Add:

```text
Gladiator. Your task is complete on its own: read only what it points to, and no other task on the board. Deliver your candidate on your branch, push it, log where it is, and close your task.
```

Dispatch the synthesis only once the ruling is in the epic task's log. Add to its prompt:

```text
Synthesis. The ruling is the ARENA RULING entry in the epic task's log. Start from the winning candidate's branch, graft the ideas the ruling names, and verify the result against the rubric in the epic task's Pattern section. Before you release this task, remove the gladiators' worktrees and local branches. Leave their remote branches: the candidate pull requests need them until the synthesis has merged.
```

## On each pass

| The record shows | Do |
|---|---|
| A gladiator in `todo`, unclaimed | Dispatch it |
| Every gladiator `done`, and no candidate pull requests | Open them, then start the judging below |
| An operator's verdict still missing | Nothing: the hold is logged |
| An operator's verdict on GitHub | Log it on the epic task, quoted with its link |
| Every verdict in, more than one, and no ruling | Escalate to combine them, with the combining prompt below |
| A ruling, and the synthesis in `todo` | Dispatch the synthesis |
| The synthesis released for review | Queue its review |
| The synthesis `done` | Close the candidate pull requests and delete their branches, then go to [acceptance](acceptance.md) |
| A gladiator that cannot deliver | Escalate: the ruling retries it, or drops it and judges the rest |

Close each candidate pull request with:

```bash
gh pr close "$CANDIDATE_PR" --delete-branch --comment "Synthesised in #$SYNTHESIS_PR."
```

## Starting the judging

Name each candidate pull request by a letter, not by its model or gladiator, so the judges grade the work. Then, from the epic task's properties:

- **`council` set:** escalate once per member, in parallel, each on a different strong model from [models.yml](~/models.yml), with the judging prompt below. Log each verdict as it returns.
- **`hitl` names judges:** notify each person it names with the `judge` role, with the candidate pull requests and the rubric, and ask them to answer on the epic pull request with a winner and the ideas worth grafting. Log the hold.
- **Neither:** escalate once, with the judging prompt. Its verdict is the ruling.

```text
Judge the arena of epic task <id> on board <dir>, with the epic-orchestration skill's arena reference. Return your verdict, and do not write to the epic task.
```

```text
Combine the arena verdicts of epic task <id> on board <dir> into a ruling, with the epic-orchestration skill's arena reference. Return the ruling, and do not write to the epic task.
```

## Judging

Read this when you have been asked to judge an arena.

- **Grade every candidate,** end to end, against each criterion of the rubric in the epic task's **Pattern** section. Cite the evidence for each grade. Do not stop at the first candidate that passes: the comparison is the point.
- **Judge the work, not who made it.** Read the candidates through their pull requests. Do not read the gladiators' tasks, or another judge's verdict.
- **Name the base and the grafts.** Pick the strongest candidate as the base, and list the ideas worth taking from the others, each with where it is. Where a graft conflicts with the base, say which one wins. When the **Pattern** section asks for something other than a base with grafts, judge for that instead.
- **Return it as an ARENA VERDICT,** or as the ARENA RULING when you are the only judge. The pass logs it.

When you are asked to combine verdicts, weigh every one of them, the operators' included. Rule as [decide](decide.md) says, and return the ARENA RULING. A split you cannot settle goes to the operator.
