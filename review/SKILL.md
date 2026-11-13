---
name: review
description: Use when you review work someone else delivered (a pull request, a task's result, a document, a design or agent instructions), alone or as a council. Covers setting how much review the work gets from its risk, the reviewer's loop from claim to handoff, findings and their severity, and merging when authorized. Not for reviewing your own work before handing it over (`executing`) or for judging an arena (`epic-orchestration`).
---

You decide whether delivered work meets its contract, and you show the executor exactly where it does not. You do not fix it: a reviewer who edits the work is reviewing their own.

Review runs in rounds. Each round ends with the work accepted or rejected with findings. The executor triages the findings, as [executing](../executing/SKILL.md#triage-review) describes, and hands back. The next round checks how each finding was settled. Rounds continue until nothing that blocks acceptance is left.

## Level

Review costs attention, time and tokens, and a miss costs more the riskier the work. So the review scales with risk. Before you read the change, set its level with [triage](references/triage.md).

| Level | The review |
|---|---|
| `low` | Read the change against the contract. Check that the handoff's evidence came from the handoff commit. Later rounds read only what changed. |
| `normal` | As `low`, plus a [task audit](references/task-audit.md), a look at what the change can break beyond its diff, and the cheapest proof re-run yourself. |
| `high` | As `normal`, plus [lenses](references/lenses.md): fresh reviewers that each read the work for one question. Prove the fact the change's safety rests on by running it. Every remediation round reads the whole change again. |

A [council](references/council.md) is separate from the level. When the task sets `council`, several models from different providers give the verdict, at whatever level the work has.

The task's `risk` sets the lowest level. Raise it when the review shows more risk than it expected, and say why in the handoff. Never review below it.

## The round

1. **Claim the task.** You hold it for the whole round, and release it with the result.

   ```bash
   kanban-md edit $TASK_ID --dir $BOARD_DIR --claim $THREAD --timestamp --append-body "REVIEW ROUND ${N} STARTED by ${THREAD}: level ${LEVEL}, ${SURFACE} at ${HEAD}"
   ```

   Put your full thread id in the entry: the claim is released at the end of the round, and the entry is what points the next round, and the task audit, at your transcript. The round number is one more than the last result entry, `REVIEW ROUND <n>: <result>`, or 1 when there is none. The `STARTED` and `TRIAGE` entries do not count.

2. **Check the surface before reading it.** The head of the review surface matches the head of the task branch, and the base has not moved under the branch. A review of a surface that will never merge is wasted. If either fails, reject the surface, as below, and stop. The [surface](references/surfaces.md) reference has the commands.
3. **Read the contract.** The issue's goal, the task's Definition of Done, its soft claims and constraints, the handoff, and any previous rounds' findings. The [task-authoring](../task-authoring/SKILL.md) skill says what each part of a task promises.
4. **Review the work** at its level, with the reference for its kind:
   - [code](references/code.md): source, tests, scripts, configuration, CI.
   - [documents](references/documents.md): documentation, designs, specifications, and instructions written for agents, such as skills, prompts and `AGENTS.md`.

   Round 1 reads the whole change. Later rounds at `low` and `normal` read what changed since the last round, and at `high` the whole change again. Read more when that change reaches into code you approved. A round after a rebase expected is the exception at every level: it checks what the rebase changed, as below.
5. **Check how the previous round's findings were settled,** as below.
6. **Verify each finding before you report it.** A finding is a claim about the work, and it needs the evidence its severity implies. Point at the line, and for P0 and P1 show the failure: a command, a test, a trace. A finding you could not confirm is a `Q`.
7. **Decide** the result, and deliver it on the surface.
8. **Merge** only when you are authorized and every gate holds.
9. **Hand off.**

## Findings

| Severity | Meaning | Effect |
|---|---|---|
| `P0` | Critical: security hole, data loss, broken correctness | Blocks acceptance |
| `P1` | High: a logic error, a regression, a soft claim not met, a serious design flaw | Blocks acceptance |
| `P2` | Medium: a fragile pattern, missing coverage, a maintainability cost | Fixed, or deferred to an issue, before acceptance |
| `P3` | Low: naming, style, polish | The executor's choice |
| `Q` | A question, not a finding | Answered before acceptance |

Each finding is one problem, anchored to the line it is about, with the fix or the question:

```text
P1: <problem>. <fix>.
```

- Name the exact file, line and symbol.
- Give the reason when the risk is not obvious from the line.
- No praise, no hedging outside a `Q`, no "consider refactoring" without a target.
- A pre-existing problem the change exposes is a finding about the exposure. The rest goes in an issue.

### The previous round

Read every finding of the previous round with the executor's reply:

- **Addressed:** the change is at the current head, and its validation covers the finding.
- **Rejected:** accept the reasoning when its evidence holds. Otherwise say why the finding stands.
- **Deferred:** accept it when it names the issue, why the finding is outside this task, and the risk that remains. In an epic, also recommend whether the follow-up belongs in the epic or outside it. An escalation decides.
- **Answered:** the answer resolves the question. An answer that exposes a defect becomes a finding.

A fix pushed without a reply is not a reply. Record each verdict in the finding's thread, with the head you checked it at.

## Decide

- **Accepted:** no P0 or P1 open, every P2 fixed or deferred, every `Q` answered, every soft claim judged met, and the evidence for each Definition of Done line comes from a run at the reviewed head.
- **Rejected:** anything else. List what blocks.
- **Change approved, rebase expected:** the work is sound, but it must not merge yet. Either a task ahead of it has to merge first, or the base moved during the review. Say so in those words, and give the base head your approval was made against. The next round, at every level, checks only what the rebase changed (`git range-diff` from the old base to the new), and re-runs the checks at the new head, because a clean rebase can still break approved code. This is not a quality finding, and the handoff says so.
- **Surface rejected:** the surface failed the check in step 2 and you did not review the change. Approve nothing: the next round is a full review.

An acceptance holds only for the head you reviewed. A commit after it, a rebase included, needs another round.

Escalate when you cannot decide: a finding the executor and you still disagree on after a second round, a contradiction between the task and its specification, or a question of scope. In an epic, the orchestrator decides. Otherwise, the operator does.

## Merge

You merge only when the dispatch says to merge on acceptance, or the task's **Review** section gives you merge authority. Then you merge at the moment you accept, because only then do all of these hold, each checked by you in this round:

1. The change is accepted.
2. The base head has not moved since you checked the surface.
3. The surface head is the head you reviewed, and matches the task branch.
4. No task has to merge ahead of this one: its dependencies, its blocked mark, and in an epic the merge queue.
5. When the merge makes commits public for the first time, such as a local `gitpr` review merged into a branch of a public repository, those commits hold no secrets and no local or identifying values: machine paths, account names, internal URLs. A pull request on a public repository is already public, so this gate holds for it.

Merge fast-forward only, and do not rebase first: a rebase after acceptance merges code you did not review. If a gate fails, do not merge, and the round's result follows from the gate:

| Gate failed | Result |
|---|---|
| 1 | Rejected |
| 2 or 4 | Change approved, rebase expected |
| 3: the branch has commits after the head you reviewed | Rejected, with a finding naming the commits. The next round reviews them. |
| 5 | Rejected, with a P0 for each value found. Escalate as well. |

Without merge authority, accept and hand off. The operator merges, and closes the task.

## Without a task

Small work can go straight to a pull request, with no task. Then the issue, or the operator's prompt that dispatched you, is the contract, and the pull request's head is the head you review. Skip the claim and the task log. The round's handoff goes on the surface, as the review's summary, and to whoever dispatched you. Merge authority can only come from the dispatch.

## Hand off

Log the round with [the review handoff](assets/review-handoff.md), and release the claim.

- **You merged:** close the task, as [task-ownership](../task-ownership/SKILL.md#finish) describes.
- **Otherwise:** leave it in `review`, released. The entry says what comes next: the executor remediates or rebases, or, once accepted, the operator merges and closes the task.

```bash
kanban-md edit $TASK_ID --dir $BOARD_DIR --claim $THREAD --timestamp --append-body "${HANDOFF}"
kanban-md edit $TASK_ID --dir $BOARD_DIR --claim $THREAD --release
```

Check that the log entry landed before you release. A task left claimed by its reviewer cannot be picked up by anyone else.

Notify whoever dispatched the review. In an epic, the release wakes the next pass.

## What to read

- [Triage](references/triage.md): at the start of every review, to set its level from the work's risk.
- [Code](references/code.md): when the work changes code, tests, scripts, configuration or CI.
- [Documents](references/documents.md): when the work is prose: documentation, a design, a specification, or instructions for agents.
- [Lenses](references/lenses.md): at `high`, to run fresh reviewers that each read the work for one question.
- [Task audit](references/task-audit.md): at `normal` and `high`, to read the task's log and transcript for what the operator should still scrutinize.
- [Council](references/council.md): when the task sets `council`, or the operator asks for one.
- [Surfaces](references/surfaces.md): to check, comment on and decide a GitHub pull request or a `gitpr` review.
- [Epic](references/epic.md): when the task is a child of an epic: the merge queue, publishing to the epic pull request, and what you never write.
