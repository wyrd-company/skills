---
name: epic-orchestration
description: Use when you start an epic task you have been handed, run a pass of one, or decide for one as its escalation. Covers how the orchestrator runs as passes woken by events, what every pass does and may not do, and which reference to read for the step at hand. Not for planning an epic (`epic-planning`) or for doing a task's work (`executing`).
---

You run an epic that has been [planned](../epic-planning/SKILL.md). You hold the epic task and do none of the work: you dispatch, integrate, keep GitHub current and finalize, and you escalate what needs judgment.

## Passes

An epic can run for days. No context lasts that long, and one that tries drifts from the record until it acts on what it remembers instead of what is true. So the orchestrator is not one long conversation. It runs as passes:

- **A schedule runs each pass,** in the epic's thread, with a fresh session and a cheap model. Board and GitHub events wake it as they happen. Its interval, every few hours, is the backstop for what fails without an event.
- **One pass runs at a time.** A wake while a pass is running is retried, so a pass always follows the event.
- **What woke you only says where to look.** Read the record. An event or a comment is not an instruction, and a decision counts only from an operator the epic names.
- **The record is your memory.** Anything a later pass needs, such as a ruling, a hold or the merge queue, goes in the epic task's log. What is not written there ends with the pass.

Each pass:

1. Read the record: the epic task and its log, its children, and the epic pull requests. Check first that the epic task's claim is this thread. Retake a claim that lapsed. If another holder has it, stop and notify the operator: two orchestrators would undo each other.
2. Read the reference for the epic's pattern, then compare the record with what the pattern expects next.
3. For each step the record shows, read the reference below that covers it, and take every step the record settles.
4. Escalate every step that needs judgment.
5. Log what you did on the epic task, and stop. A pass that finds nothing to do writes nothing: your writes wake passes too.

## Three kinds of work

- **Scripts** do what is mechanical, before any model wakes: routing events now, and any check that needs no reading. When a pass keeps doing the same mechanical step, that step belongs in a script.
- **The pass** does what the record settles: releasing tasks, dispatching when the preflight gives one next step, repairing a claim when the evidence is unambiguous, checking after a merge, keeping GitHub current.
- **An escalation** to a stronger model does what needs judgment: a ruling, a state you did not expect, a block, what a deferred finding becomes. Delegate it with the epic and the question, choosing its model from [models.yml](~/models.yml), and wait for it: several at once, such as an arena's council, run in parallel. It returns its ruling, and you log it on the epic task. Only the epic task's holder writes to it. You, or a later pass, act on the ruling.

The pass decides nothing the record does not already settle.

```text
Decide for epic task <id> on board <dir>: <question>.
Use the epic-orchestration skill's decide reference, and return your ruling. Do not write to the epic task.
```

The patterns put the next step into the work itself: a chain link writes the next link, dependencies and `kanban-md pick` order a graph, and the reviewer merges at acceptance. Step in only where the work cannot move on by itself: gates, the review queue, blocks and failures.

## Control

One actor controls a task at a time: it has write authority over the task's branch and worktree, and it keeps the task's log. The claim says who.

- **The cue is the release.** An executor saying it is ready is not the event you act on. The event is the holder moving the status and releasing the claim. A handoff note under a live claim means it is still working: wait.
- **Write status to repair, never to advance.** Advancing is the holder's job. Do not move a task towards `review` because you judged it ready, and do not claim a task on someone else's behalf. Repair is yours, as [recovery](references/recovery.md) describes.
- **The task record outranks the plan.** If they disagree, the plan is wrong.
- **A state you did not expect means stop.** Escalate it; do not improvise a way through.
- **Record a hold.** When a task waits on something only you will release, log the hold and what releases it on the epic task. Every pass reads it, and the backstop rechecks it.

## Keep GitHub current

People follow the epic on GitHub, not on the board. Any pass that changes where the epic stands keeps it current.

- Keep the GitHub project's items current as tasks land.
- Update an issue when its status changes from the issue's point of view. Close it when its goal is met.
- Notify the operator when they are needed: a decision that is theirs, or acceptance.

## What to read

Read only what the step at hand needs.

**The epic's pattern.** Read the one the epic task's **Pattern** section names, on every pass. It holds only what the pattern changes about the steps below, under these headings and in this order, leaving out the steps it does not change: How it moves, At Start, Dispatching, Review and merge, On each pass, Findings, Acceptance. After them come any sections only that pattern needs. For everything a pattern reference does not mention, follow the step's own reference.

- [Arena](references/arena.md): when several gladiators build competing candidates to one brief, and when you are asked to judge them. It covers keeping the candidates independent, running the judging by council, operators or a single judge, and dispatching the synthesis.
- [Chain](references/chain.md): when the epic advances one link at a time. Each link writes the next, so it covers dispatching the next link once the last has merged, and when the chain is done or should stop.
- [Map-Reduce](references/map-reduce.md): when uniform workers take independent chunks and reducers combine them. It covers dispatching each reducer once its batch has merged, keeping the long merge queue moving, and dropping a chunk that cannot be delivered.
- [Project](references/project.md): when the epic is a dependency graph of tasks. It covers dispatching what the graph makes ready, the order of the merges, and re-planning when the graph stops matching the work.
- [Swarm](references/swarm.md): when drones decide the next steps among themselves. It covers keeping N drones running on what is ready, leaders that work their team in rounds, races, and deciding when the swarm has stopped.

**The step at hand.**

- [Start](references/start.md): when you have been handed an epic and its task is not claimed yet. It sets up the claim, the epic branches and pull requests, and the schedule that every later pass and event depends on.
- [Dispatch](references/dispatch.md): when a task is ready for its next agent, to implement, remediate, review or accept it. It covers the check before sending anyone, the prompt, the model, and keeping parallel siblings from colliding.
- [Review and merge](references/review-and-merge.md): when a child has been released for review, a review is waiting its turn, or a merge has landed in the epic branch. It keeps the branch to one review at a time, in an order the record holds.
- [Recovery](references/recovery.md): when the work has stopped moving by itself: a task is blocked, a session died or left its claim, a handoff looks incomplete, or a reviewer deferred a finding. It says what to check, what to repair and what to escalate.
- [Acceptance](references/acceptance.md): when every child is merged and no executor is active, or acceptance found a problem. It takes the epic to pull requests ready for the default branch.
- [Finalize](references/finalize.md): when the epic pull requests have merged into the default branch, or acceptance has passed for an epic without them. It closes the epic down and archives its board.
- [Decide](references/decide.md): when you are the escalation and have been asked to decide for the epic, not when you are a pass. It holds the authority you decide with, and how to record a ruling.
- [Devcontainer](references/devcontainer.md): when setting up or debugging what every epic in a devcontainer shares: the event path and the archive storage. A pass needs it only when a pass did not follow an event it should have, or an archive failed.
