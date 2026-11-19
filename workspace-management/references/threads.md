# Threads

Read this when the survey lists threads to settle, threads that wait on a person, failed threads, stalled claims, or ledgers to clean up. Settling a thread says its work is finished: it leaves the list people watch, and its ledger can be cleaned up. A thread settled too early hides work that is still open, so settle only on evidence.

## Finished threads

The survey lists the candidates, oldest first: threads that are completed or idle, and not settled, pinned, snoozed or waiting on anyone. Take them in that order, as many as the shift can finish.

A thread is finished when all of these hold:

- **Its last message ends the work:** it reports the result, hands the work off, or reports a block that someone else now owns. A last message that asks a question, promises a next step or stops part way is not an end.
- **No live claim names it.** A task it still holds means its work is still open: see [Stalled work](#stalled-work).
- **Nothing it owns is waiting on it:** a pull request it opened is merged, closed, or handed to a task's ledger, as [ledger](../../ledger/SKILL.md#hand-off) says.
- **Its children are finished.** Settle a parent's children with it, and never a parent before its children.
- **A thread a person started has been idle for a day.** People leave their own threads open while they read the result. Pin a thread to keep it open: the survey leaves pinned threads out.

Read each candidate with `t3c thread read <id>`, or its last messages when the transcript is long. When you cannot tell from the thread itself, escalate the question instead of settling. To read many threads, delegate them in batches to a cheap model, with this brief, and decide from what comes back:

```text
For each thread id in <file>, read its last messages with `t3c thread read <id>`. Return one line per thread: id, finished | open | unclear, and the line of the thread that shows it. Change nothing.
```

Settle each finished thread with `t3_thread_organize` (`settle`), then clean up its ledger, as [below](#ledgers). Log each batch on the manager task as one entry: how many you settled, and the threads you left open and why.

## Threads waiting on a person

A pending question or approval is addressed to that thread's operator, and the manager does not answer it, as [authority](../SKILL.md#authority) says. Notify them once, with [contact](../../contact/SKILL.md): link the thread, quote the question, and say how long it has waited. Log the notification with the thread's id, so later shifts read it and do not notify again.

## Failed and interrupted threads

Read the end of the thread. Then:

- **It holds a task's claim:** handle it as [stalled work](#stalled-work).
- **It failed for a reason that a retry clears,** such as a provider error or the workspace running out of processes, and its work matters still: send `Continue` to the same thread, once, and log it.
- **Otherwise:** notify the operator the thread works for, once, and log it.

A provider that refused the content, as a safety flag does, will refuse it again. Do not retry: notify.

## Stalled work

Work stalls without any event to say so. Check both kinds on every sweep.

- **A claim whose thread is not running.** The survey lists each task in `in-progress` or `review` whose claim names a thread that is not working. When the task is an epic's child, leave it: the epic's pass recovers it, as `epic-orchestration` says. When it is not, read the thread's end. A session that died, such as from a provider error, resumes in the same thread: send it `Resume task <id> on board <dir>.`, so the claim stays valid. When it stopped for any other reason, or stalls again after you resumed it, notify the operator.
- **An epic that is not running.** For each epic task in `in-progress` or `review`, its `schedule` property names its schedule. Check it with `t3c schedule show <id>`. When it is enabled and has not run within its interval, run it with `t3c schedule run <id>`. When it is missing or disabled, notify the operator: you do not run the passes yourself.

## Ledgers

The survey lists every ledger that still holds resources, with its owner: a thread's status, `settled`, or `task`.

- **A settled thread's ledger:** clean it up, as [ledger](../../ledger/SKILL.md#clean-up) says, with `--db <thread id>`. Hand off to the task's ledger whatever a task still needs, such as a branch whose pull request is open.
- **A task's ledger** (`task-<id>`): clean it up once the task is `done` or `archived`. Task ids repeat across boards, so find the task by its ledger's resources and logs before you clean, and leave the ledger when you cannot tell which task it is.
- **An unsettled thread's ledger:** leave it. The thread cleans up its own ledger when it finishes.

What a cleanup cannot remove, and each set of instructions it prints, follow the [authority](../SKILL.md#authority) rules: do it when it is reversible, and notify the operator when it is not.
