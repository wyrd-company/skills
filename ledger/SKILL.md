---
name: ledger
description: >
  Use when you create something that has to be removed later (a sandbox, worktree, branch, container, process, deployment or scratch directory), when you hand work and what it holds to another thread or task, or when you clean up after a thread or task. Covers the `ledger` CLI: keys, cleanup commands and instructions, handoff between ledgers, and cleaning up a ledger. Not for running a sandbox (`boat`) or the rest of finishing work (`executing`).
---

Each thread keeps a ledger: a list of everything it acquired, with the command or instructions that remove each one. Whoever cleans up, whether you later, another agent or a person, works from the ledger instead of searching your transcript. `ledger --help` lists the commands; [ledger.md](https://github.com/wyrd-company/workspace-dotfiles/blob/main/docs/ledger.md) in the dotfiles says how it works.

## Which ledger

Your thread's ledger is the default: `ledger` uses `$T3CODE_THREAD_ID`. When a resource belongs to a task rather than to one thread, such as a sandbox the next task in an epic will use, or a branch whose pull request is still open when your thread ends, it belongs in the task's ledger, `task-<id>`: hand it off there (see [Hand off](#hand-off)).

## Record

Record a resource right after you create it, before anything else can fail:

```sh
ledger acquire worktree:/workspace/r/worktrees/x \
  --cleanup "git -C /workspace/r worktree remove --force /workspace/r/worktrees/x" \
  --verify "test -d /workspace/r/worktrees/x || exit 1"
ledger acquire gh:pr/wyrd-company/r/12 --instructions "Close PR #12 if it was not merged, then delete branch feat-x"
```

- **Key.** `kind:name`, naming the resource itself, so that every ledger names it the same way: `boat:sandbox/<id>`, `worktree:<path>`, `branch:<repo-path>/<branch>`, `gh:branch/<owner>/<repo>/<branch>`, `docker:container/<name>`, `process:<pid>`, `dir:<path>`, `thread:<id>`. No whitespace or `@`, and case is ignored.
- **`--cleanup`** is one shell command that removes the resource completely, with absolute paths and explicit ids, because it runs later from any directory. It must be safe to run twice: a resource handed off halfway can end up in two ledgers. Give `--cleanup` whenever a command can do the job.
- **`--instructions`** replaces `--cleanup` when removing the resource needs judgement or a person: closing an unmerged pull request, deleting data someone may still want.
- **`--verify`** is optional. It exits 0 while the resource exists and 1 once it is gone. `ledger clean` uses it to release what was already removed without running the cleanup. Make any other failure exit with another status, so that an error is never read as "gone".

Boat sandboxes record themselves: the `boat` wrapper acquires the sandbox after `boat new` and `boat fork`, and releases it after `boat delete`. Check `ledger list` once after creating one; the wrapper warns rather than fails when it cannot record.

When you remove a resource yourself, rather than through `ledger clean`, run `ledger release <key>`.

## Hand off

When a resource has to outlive your thread, move it to the ledger that is now responsible for it, and say so in the handover:

```sh
ledger handoff --to task-42 boat:sandbox/sbx_123
```

Hand off to the thread or task that will use it next, and when nothing will, to the task the work belongs to. The receiving thread's own work then decides when it is removed.

## Clean up

When the work is finished, which for a thread means it is settled and for a task means it is closed:

1. `ledger list` shows what is left. Hand off anything something else still needs.
2. `ledger clean --dry-run`, then `ledger clean`. It releases each resource that `--verify` shows is gone, and runs the cleanup of the rest, releasing those that succeed.
3. Each resource it keeps is a failed cleanup or a set of instructions. Do what each one says, then `ledger release` it. What you cannot remove, such as a pull request still under review, you hand off to the task's ledger.

The step is done when `ledger list` is empty.

To clean up another thread's or task's ledger, pass `--db <name>`, and only once that thread is settled or that task is closed. `ledger list --all` shows every ledger.
