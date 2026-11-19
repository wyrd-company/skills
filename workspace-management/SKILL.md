---
name: workspace-management
description: >
  Use when you run a shift as the workspace manager, set up or change the workspace manager, or need to reach it: to hand it an epic or a request, or to report finished work. Covers shifts and their rotation, the manager's record, what a shift may decide, dispatch under the workspace's WIP limits, settling threads, cleaning up resources, and maintenance. Not for running an epic (`epic-orchestration`), cleaning up after your own thread (`ledger`), or doing a task's work (`executing`).
---

The workspace manager keeps the work in a workspace moving and the workspace tidy. It knows what is under way, starts what is ready, settles threads whose work is finished, cleans up what they left behind, and keeps the workspace healthy. It does none of the work itself: it dispatches, checks, and escalates what needs judgment.

## The record

The manager's record is the manager task: the task tagged `workspace-manager` on the workspace board at `/tasks`. `/tasks` is the workspace's own checkout of the tasks repository, on its `workspace/<workspace>` branch, beside the projects' `tasks` folders.

- **Its claim names the current shift.** Whichever thread holds it is the manager, and other agents find the manager by it.
- **Its body holds the standing state:** the rotation schedule, the WIP limits, the duties and how often each runs, the open requests and the holds. Operators change the limits and duties there.
- **Its log is the history:** each takeover, dispatch, settlement batch, duty run, notification and ruling, as it happens.

```bash
kanban-md --json list --tags workspace-manager --dir /tasks \
  | jq -r '.[] | "\(.id) \(.claimed_by // "unclaimed")"'   # the task's id, then its holder
```

The commands below call the task's id `$MANAGER`.

## Shifts

The manager runs for as long as the workspace does. No context lasts that long, and a context that tries drifts from the record until it acts on what it remembers instead of what is true. So the manager is not one long conversation. It runs as shifts:

- **The rotation schedule starts each shift in a new thread,** every 6 hours. A shift is the manager from the moment it takes the claim until the next shift takes it. Between those two points, messages wake it.
- **One shift at a time.** The claim says which. A shift that finds another shift still running waits for it, so two shifts never act at once.
- **The record is your memory.** Anything a later shift needs (a request, a hold, a ruling, a duty you ran, a person you notified) goes on the manager task as it happens. A shift can end at any moment, so there is no handover to write at the end: when the record is current, the handover is already done.
- **What woke you only says where to look.** A message from an agent is a report to check against the record. A request counts as a decision only when it comes from an operator.
- **Rotate early when your context is heavy,** such as after a long sweep or a compaction: run the rotation schedule now, with `t3c schedule run <id>`, and stop.

### Start a shift

1. **Register the git operator** the schedule's prompt names, with `git operator set --from <thread>`. When that fails, carry on without committing and notify the operator: the board is on a persistent mount, so the commit is the backup and not the record.
2. **Read the manager task:** its body, and its log back to the previous takeover.
3. **Take over from the previous shift.** The previous shift is the thread that holds the claim. Check it with `t3c thread status <id>`. While it is running, wait for its turn to end with `t3c thread wait <id> --timeout 30m`. If it is still running after that, stop and notify the operator: interrupting it could cut off a dispatch half made. Then take the claim:

   ```bash
   kanban-md edit "$MANAGER" --release --dir /tasks
   kanban-md edit "$MANAGER" --claim "$T3CODE_THREAD_ID" --dir /tasks
   ```

   The first shift finds the task in `todo` and unclaimed: it claims it with `kanban-md move "$MANAGER" in-progress --claim "$T3CODE_THREAD_ID" --dir /tasks`, and skips the next step.

4. **Settle the previous shift.** Move what its ledger still holds to yours, as [ledger](../ledger/SKILL.md#hand-off) says: `ledger --db <its thread id> list`, then `ledger --db <its thread id> handoff --to "$T3CODE_THREAD_ID" <keys>`. Then settle its thread. The delegates it dispatched report to its thread, which forwards their reports to you (see [each wake](#each-wake)).
5. **Log the takeover** on the manager task, naming the previous shift, then commit and push the board, staging its paths by name: `git -C /tasks add config.yml activity.jsonl tasks`, then commit with `chore: manager shift <thread id>` and push.
6. **Run a sweep.**

### Each wake

On each message, first check that the claim is still yours. When it is not, a later shift has taken over: forward the message to the thread that holds the claim with `t3_thread_send`, and stop.

Otherwise, handle what the message asks within your [authority](#authority), log it, and stop. Write a request you cannot finish now into the task's **Requests** section, so it survives the rotation. Run a sweep when the message asks for one.

## The sweep

A shift sweeps once when it starts. Each sweep:

1. **Survey** with `bash scripts/survey.sh`, from this skill's folder. It lists threads, boards, ledgers and the workspace's health. Read its last line: anything but `survey complete` means a section is missing, and a missing section is not "nothing to do". Read the reference for each section only when the section lists something.
2. **Settle the threads whose work is finished, and clean up after them,** as [threads](references/threads.md) says.
3. **Check that the running work is moving:** each epic has a live schedule, and each claim's thread is working, as [threads](references/threads.md#stalled-work) says.
4. **Dispatch what is ready,** within the limits, as [dispatch](references/dispatch.md) says.
5. **Run each duty that is due,** as [maintenance](references/maintenance.md) says.
6. **Log what you did.** A sweep that changed nothing writes nothing.

Keep each sweep to what one shift can finish. A backlog, such as hundreds of unsettled threads, drains over several shifts: take the oldest first, and leave the rest for the next shift.

## Authority

The manager decides what the record settles, escalates what needs judgment, and brings a person in for what only a person may decide.

- **Do on your own:** settle threads whose work is finished, clean up ledgers whose thread is settled or whose task is closed, start epics and dispatch ready tasks within the limits, resume a stalled executor in its own thread, and run the duties.
- **Escalate** what needs judgment, such as whether a thread's work is finished when its record does not say, or whether a resource no ledger holds may go. Delegate it with the question and the evidence, choosing its model from [models.yml](~/models.yml), and act on the ruling.
- **Bring the operator in, with [contact](../contact/SKILL.md),** for what cannot be undone or is theirs to decide: removing work that is not pushed or not merged, deleting what no ledger holds, closing a pull request, spending money, changing a limit, and a state you do not understand. Notify once, log the notification, and leave it to later shifts to read the log instead of notifying again.

Three things stay with others, even when doing them yourself looks quicker:

- **Answer no thread's question or approval.** It is addressed to that thread's operator, and an answer from you would be read as theirs. Notify the operator instead.
- **Do no task's work, and claim no task but the manager task.** A task's claim names the thread that does its work. A manager that takes a task holds up the shift's other duties, and its claim lapses with the rotation.
- **Run no epic.** The epic's own schedule and orchestrator run it. You check that they run.

## Reach the manager

Read this section when another skill sends you to the manager, such as to hand it an epic or report that one has finished.

1. Find the manager task's holder, as in [The record](#the-record).
2. Message that thread with `t3_thread_send`, saying what you hand it: the epic task's id and board, the request, or the result.
3. When `/tasks` has no manager task, the workspace has no manager: do the step yourself, as the skill that sent you says. When the task exists but no thread holds its claim, the next shift reads the record and acts: leave what you hand over in its place, such as the epic task in `todo`, and log that you did.

## What to read

- [Setup](references/setup.md): when `/tasks` has no manager task or no rotation schedule, or to change the interval, the model or the git operator.
- [Threads](references/threads.md): when the survey lists threads to settle, threads that wait on a person, failed threads, stalled claims or ledgers to clean up.
- [Resources](references/resources.md): when you look for what no ledger holds: worktrees, sandboxes, containers and scratch files left behind.
- [Dispatch](references/dispatch.md): when an epic is waiting to start, a task is ready, or a request asks for work, and for the WIP limits every dispatch in the workspace is held to.
- [Maintenance](references/maintenance.md): when a duty in the manager task's **Duties** section is due.
