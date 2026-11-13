---
name: task-authoring
description: Use when writing a task, the ticket to do a piece of work, or when deciding whether work needs a task, a GitHub issue or both.
---

A task is the ticket to do a piece of work. It says what one executor will deliver, how completion is judged, and where the work stands. It does not define the goal: a GitHub issue or the operator's prompt does that.

Tasks live on a `kanban-md` board in a workspace project's `/workspace/{project}/tasks` folder or the workspaces tasks folder `/tasks`. Each tasks folder has a `default` board for its scope, and each epic has its own board under `epics/`, which the [planner](../epic-planning/SKILL.md) creates. The `kanban-md` skill covers the commands. The workspace's `AGENTS.md` files say which tasks folder serves which scope.

## Issue, task, pull request

| Record | Answers | Holds |
|---|---|---|
| GitHub issue | What is wanted, and why? | The bug, feature or improvement; the deliverable and its bar; reproduction; discussion; priority |
| Task | Who is doing which piece, and where does it stand? | The contract for one piece of work, the claim, status, log, blockers, handoff |
| Pull request | Is this change right? | The diff, review findings and replies, checks, approval, merge |

- **The issue owns the goal.** A task links its issue and says which part of the goal it delivers. It does not restate the goal. A task may deliver less than the issue asks, but it may not contradict it.
- **Change the goal on the issue.** When the work shows the goal or its bar is wrong, the issue is changed first, by someone with authority over it, and then the task. The wording for who holds that authority is being settled elsewhere; until then it is the thread's operator.
- **Links run one way.** The task links to issues and pull requests. Issues and pull requests link to each other and never to a task, because their readers may not have the board.
- **The counts vary.** One issue may need several tasks, and one task may close several issues.
- **Small work needs neither.** A fix that a few turns can finish and one pull request can explain goes straight to the pull request, from an issue or from nothing. Write a task when requested, the work will outlast a few turns, pass to another agent, or need coordinating with other work. Raise an issue when the goal needs agreeing, or will not be met today.
- **Work with no issue.** For anything larger, raise the issue first when the work fixes a bug in a repository, or adds or improves something its users will notice, or is a formal spike, whose report is committed to the repository. Chores, workspace maintenance and direct requests that finish where they started need no issue: the task states the goal itself. A quick spike made while answering a question or doing other work needs neither an issue nor a task.
- **Deferred work is an issue.** A board is a short-term place to organise work that is under way or about to start. The `backlog` status has one use: a planner puts an epic's tasks there, and the orchestrator moves them to `todo` as it launches the epic. Record anything to be done later as an issue, with its goal and bar.

## Before writing

Search the board for a task that already covers the outcome, by subject and by the files it would touch. Two tasks for one defect put two executors in the same files, and nobody notices until one of them has committed. Work that is new has nothing to collide with; search when the task comes from an issue, a review finding or a report.

## The contract

A task is ready when an executor can answer these without asking anyone:

1. What outcome is wanted? (The issue, when there is one.)
2. How is completion judged?
3. What must not change or be assumed?
4. Which artifacts and earlier decisions matter?
5. What access, resources or coordination does the work need?
6. Who can do it, and how is it reviewed?

Use [the template](assets/template.md).

### Stop at the contract

The author says what is wanted, how it will be judged, and where the knowledge is. How to do it belongs to the executor, who will have read the code when the author has not. An approach written into a task arrives with the task's authority, and executors follow it even when it is wrong.

- **Write down what you know. Do not investigate to fill the task in.** If you would have to read the code to write a line, leave the line out. The two exceptions are the search for an existing task and running a tool that a Definition of Done line depends on: both test whether the contract can be met, not how.
- **Describe results, not changes.** "The command exits non-zero on a missing file" is a contract. "Add a check in `load()`" is an implementation. A Definition of Done that lists files to edit or functions to add has been executed in the author's head.
- **A task is not where design lives.** Tasks are short-lived and people do not read them. Anything that should still be true and findable after the task is done belongs in the repository's docs, or on the issue when it is about the goal: how a feature behaves, an interface, a schema, a decision and its reasons. The task links it. Ask of each paragraph: will anyone need this once the task is closed? If so, it is in the wrong place.
- **Refer to the specification; do not restate it.** "Retries behave as `docs/sync.md` (Retries) specifies" is a Definition of Done line. Copying the retry rules into the task makes a second specification that will disagree with the first.
- **When the specification is missing, do not write it in the task.** Either the work includes writing it, as a Definition of Done line naming the document, or a design task produces it first and this task waits for it. A Definition of Done that needs paragraphs to describe the behaviour is a sign of a missing specification.
- **When you cannot write the contract without investigating, the investigation is the task.** Write a spike, or hand the question to the executor as part of the work.
- **Authoring is cheap.** A task that takes more than a small part of the effort of doing the work is doing the work.

## Size

A task fits one focused session and yields one coherent, validated result. Split it when:

- it has two Definitions of Done that do not depend on each other;
- validation needs unrelated systems;
- one part is design or research and another is implementation;
- a rollback would revert only part of it;
- the parts need different roles.

Do not split work to create more tickets. One executor touching several files for one Definition of Done is one task.

An epic is a task whose children do the work. Epics are planned, not authored here: see [epic-planning](../epic-planning/SKILL.md).

## Definition of Done

Definition of Done has hard claims, and soft claims. "Works correctly" and "refactor as needed" are neither hard nor soft claims: nobody can check them or disagree with them. With an issue, each line traces to the issue's bar or to a constraint of this piece of work.

Each hard claim is a line that a named check can show to be false.

- **Name the fallback.** When a check may not run where the executor works, say what to try first and what evidence is acceptable in its place.
- **State counts as a change from the base.** Write "no new diagnostic, and the named one removed", not "170 to 169". The base moves between writing and starting.
- **Run the tool first.** When a line needs a tool to behave in a specific way on a specific shape, run it on that shape and record the result in the task.
- **Order lines that depend on another task.** When a line changes something that another task's data must first match, say which task goes first and what holds in between.
- **Settle exceptions before dispatch.** A waived criterion or a split scope is recorded as a decision by someone with authority over the goal, with the evidence that counts as done and the owner of what remains. Do not leave a proposed exception for the executor or reviewer to read as approval.

Three cases need more care, covered in [definition-of-done.md](../executing/references/definition-of-done.md): a line that rests on a suspected cause, a line that asks for an assertion, and a property that only shows across an event such as a restart.

A soft claim is one that only judgement can settle: the user documentation still describes what the product does, the change fits the design around it, the output is something its user can act on. No check passes or fails it, which is why the work has a reviewer and not only CI. Soft is not vague. "Docs are good" gives a reviewer nothing to disagree with; a soft claim gives them something specific to judge.

- **Name what is judged.** Point at the artifact and the part of it: the README's install section, the error messages of the new command, the public API of the module. A reviewer should know where to look without reading the whole change.
- **Name what it is judged against.** A standard, an existing pattern in the repository, an example, or the reader it is for: "a new user can install from the README alone", "follows the retry pattern in `client/`". Without a reference, the judgement is the reviewer's taste.
- **Say who judges** when it is not the ordinary reviewer: a council, the operator, the user in [acceptance testing](../executing/references/user-acceptance-testing.md).
- **Do not turn it into a check that proves less.** "The README mentions the new flag" can be checked and can pass while the README is wrong. When the check would be a stand-in for the judgement, leave the claim soft. When a real check is cheap, write the hard claim.
- **Do not repeat standing standards.** What every change in the repository owes (docs in step, changelog, conventions) applies without being written here. Name a standard only when this task touches it in a way the executor might miss; the template's Artifact Impact section is where those go.
- **Keep them few.** Each soft claim costs a reviewer's attention. Write the ones where a wrong judgement would mean the goal was not met.

The executor answers a soft claim in the handoff by saying what they did and where to look. The reviewer decides it.

## Context

The author usually knows where the relevant material is. Put that in the task, so the executor and the reviewer start from the right context and do not have to crawl the repository to find it.

Point at whatever bears on the work:

- the repository's `docs/**`: designs, specifications, decision records, user documentation the change must agree with;
- the project's `references/` folder: reference implementations and dependency sources;
- the code where the work starts, when you already know it: an entry point, not a list of what to change;
- external resources: library or API documentation, a standard, an upstream issue;
- earlier work: tasks, pull requests, issues and memories that explain why things are as they are.

For each pointer:

- **Say what it is for.** One clause on what to take from it: "the retry policy this change must follow", "the upstream behaviour we copy". A bare path gets skimmed or skipped.
- **Be precise.** A heading, a symbol or a line range inside the file. For an external resource, the version it applies to, and a permanent link where one exists.
- **Separate what must be read from background.** The executor reads the first group before starting. The second is there when a question comes up.
- **Name what a claim is judged against.** When a soft claim in the Definition of Done refers to a standard, a pattern or an example, it is listed here.
- **Record the gaps you know of.** "There is no design document for the sync path" or "the README section on this is out of date" saves the search and stops the executor trusting a stale page.

Link, do not copy: pasted content goes stale and hides its source. Check that each path and link resolves before the task is dispatched. List only what you know is relevant. The executor still investigates, and a long list is as much work as no list.

## Metadata

The board's configuration owns the allowed values. This is what each field is for.

| Field | Purpose |
|---|---|
| `issue` | The issue or issues this task serves, as `owner/repo#123` |
| `assignee` | The operator who does the work, when a person leads it |
| `hitl` | The operators who take part in the task, and in what role: doing some or all of the work, judging an arena, accepting the result |
| `council` | The task will be reviewed by a council |
| `complexity` | Guide the choice of model and effort at dispatch |
| `risk` | How much review the work gets: `low`, `normal` or `high`. Set it from what a miss would cost, as [review's triage](../review/references/triage.md) describes. The reviewer may raise it, never lower it |
| `priority`, `parent`, dependencies | Order of work and structure |

Status and the claim belong to whoever is working the task: see [task-ownership](../task-ownership/SKILL.md).
