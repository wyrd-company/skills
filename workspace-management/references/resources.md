# Resources

Read this when the **Resources no ledger holds** duty is due. Ledgers are the first place cleanup looks, as [threads](threads.md#ledgers) says. This finds what no ledger holds: worktrees, sandboxes, containers and scratch files that work left behind before ledgers existed, or without recording them.

## The rule

Remove a resource yourself only when it holds nothing that exists nowhere else, and nothing live uses it: the sections below say how to tell, for each kind. This is the only removal of what no ledger holds that the manager's [authority](../SKILL.md#authority) allows. Anything else goes to the operator in one report for the shift, with what holds each one back. A worktree removed with an unpushed commit or an untracked file in it is lost for good, and a list costs the operator a minute to read.

Before removing anything, check that no ledger holds it (`ledger list --all`), and leave it to its ledger when one does.

## Worktrees

For each repository folder under `/workspace/<project>/`, list the worktrees with `git -C <repo folder>/main worktree list --porcelain`, after `git fetch --prune`. Leave each repository's default-branch worktree (`main`, or `fork` for a fork). A worktree can go when all of these hold:

- **No thread or claim uses it.** No thread that is not settled has it as its worktree, as `t3c --json thread list | jq -r '.data[] | select(.settledAt == null) | .worktreePath // empty'` lists them. No live claim names a task whose branch it holds.
- **Nothing is uncommitted:** `git -C <worktree> status --porcelain` prints nothing, untracked files included, and `--ignored` adds only build output that can be made again, such as `node_modules`, `.venv` or `dist`. Evidence and decks are often kept in ignored folders such as `.tmp`, and they count.
- **Its commits are on the remote:** `git -C <worktree> branch -r --contains HEAD` lists a remote branch.

Remove it with `git worktree remove <path>`, then delete its local branch only when it is merged into the default branch. Leave its remote branch: an open pull request may still use it.

## Other resources

- **Boat sandboxes** are shared by the account across workspaces. List them with `boat list`, and report those no ledger holds instead of deleting them: another workspace may be using one.
- **Docker:** remove dangling images and build cache with `docker image prune -f` and `docker builder prune -f`. Report stopped containers and named volumes: their data may be wanted.
- **Scratch files** in `/tmp` older than 7 days and no longer open, `find /tmp -mindepth 1 -maxdepth 1 -mtime +7`: remove those owned by `vscode` that no process holds open (`fuser`), and report the rest.

## Done

Log on the manager task what you removed, as one entry, and send the operator the report of what you kept, once. Log `Duty Resources no ledger holds: done`.
