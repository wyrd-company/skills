---
name: task-ownership
description: Use when you claim a kanban-md task, work on one, block it, hand it off, resume it or close it. Only covers what is specific to kanban-md tasks.
---

This skill _supplements_ the [executing](../executing/SKILL.md) skill, it does not replace it. It provides you the instructions to manage a _task_ record during execution.

You own a task from the moment you claim it until you release it. While you hold it, keep one thing true: another agent, or a person, can pick the work up from the task record and the git history alone. Your session can end without warning.

The task is the ticket for the work. The goal belongs to the GitHub issues it links.

People do not read tasks or the board. When people take part in the work (`hitl`), the agent assigned to help claims the task, notifies each of them when their part is needed (a `work` person when the task is ready to start), keeps the log and moves the task through its statuses.

Read the task, the issues it links, its log and the branch history before you start. Read the latest log entries first: they say where the work stopped.

```bash
kanban-md show $TASK_ID --dir $BOARD_DIR
```

## Claim

Claim the task and put the full thread id in your first log entry, so that anyone can see who holds the task and reach you.

```bash
kanban-md edit $TASK_ID --dir $BOARD_DIR --claim $THREAD --assignee $OPERATOR --timestamp --append-body "${BODY}"
```

Never take a claim another holder still has. Escalate because this may be a thread race condition.

## Log

A claim lapses when the task goes without an update. Each log entry renews it.

```bash
kanban-md edit $TASK_ID --dir $BOARD_DIR --claim $THREAD --timestamp --append-body "${BODY}"
```

Keep the log true. If the work diverged from what an entry says, fix the entry.

## Blocked

```bash
kanban-md edit $TASK_ID --dir $BOARD_DIR --block $REASON --claim $THREAD --release
```

## Hand off for a review round

```bash
kanban-md handoff $TASK_ID --dir $BOARD_DIR --timestamp --claim $THREAD --release --note "${HANDOFF}"
```

## Receive review

```bash
kanban-md edit $TASK_ID --dir $BOARD_DIR --status in-progress --timestamp --claim $THREAD --append-body "REVIEW ROUND {N} TRIAGE"
```

## Resume

```bash
kanban-md edit $TASK_ID --dir $BOARD_DIR --status in-progress --timestamp --claim $THREAD --append-body "TASK RESUMED"
```

Take the claim, then read the last handoff or blocked entry. Clear the blocked mark only when the blocker has gone, and say in the log what cleared it.

```bash
kanban-md edit $TASK_ID --dir $BOARD_DIR --timestamp --claim $THREAD --unblock --append-body "BLOCK CLEARED:\n${WHAT}"
```

## Finish

Add a final log entry listing what was done, release the claim, and mark the task done.

```bash
kanban-md edit $TASK_ID --dir $BOARD_DIR --timestamp --claim $THREAD --release --completed YYYY-MM-DD --status done --append-body "${FINAL_LOG_MESSAGE}"
```
