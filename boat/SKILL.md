---
name: boat
description: >
  Use when a check needs a clean, disposable machine: proving an install, setup steps or a clean clone on a fresh system, running something that would change this workspace, or giving a person an HTTPS URL to try a result. Covers Boat sandboxes: `boat run` and `boat new`, getting the work onto one, hosting a port, cost, secrets and deleting what you made. Not for deciding what to prove (`executing`) or how acceptance runs (`executing`'s user-acceptance-testing).
---

A Boat sandbox is a Linux VM that starts in seconds and holds nothing from this workspace. A result there shows what someone starting from nothing gets, not what this machine happens to have installed.

## When to use one

- **The claim is about a fresh machine:** an installer, a bootstrap script, setup instructions, "works from a clean clone".
- **The check would change this workspace:** system packages, the home directory, services you would have to undo.
- **A person needs to try the result:** an app on a URL, for [user-acceptance testing](../executing/references/user-acceptance-testing.md).

A check that runs in a worktree, such as tests or a linter, stays there: a sandbox adds cost and proves nothing more.

## Before you start

- `boat` on `PATH` is a wrapper that reads the API key from OpenBao on each call, as [Boat](https://github.com/wyrd-company/workspace-dotfiles/blob/main/docs/boat.md) in the dotfiles describes. A 403 is the Wyrwood policy: report it, as for any secret.
- **Cost.** Sandboxes run on the plan's included hours. Run `boat limits --json` first: start only when `canStart` is `true` and `nextStartDollars` is `0`. A start that would cost money beyond the plan is spending money: [ask first](../executing/SKILL.md#when-to-decide-and-when-to-ask).
- **Size.** Use `--type small` unless the check needs more.
- **Secrets.** The sandbox is a machine outside the workspace. Pass `--no-env`, so the account's stored secrets stay off it, and never send it a secret with `-e`, `--file` or a pushed file. A check that cannot run without a secret is not a sandbox check: run it in the workspace, or ask the operator.

## One command: `boat run`

Prefer `boat run` when one command proves the claim. It creates a sandbox, copies a directory in, runs the command, prints its output and cost, and deletes the sandbox. It exits with the command's exit code, so there is nothing to clean up.

```sh
boat run --no-env --type small --timeout 900 --push . ./install.sh
```

`--push` copies the files git tracks or does not ignore, uncommitted changes included. To prove a commit, run it from a clean worktree checked out at that commit, and record the commit with the result.

## Several steps: `boat new`

Use `boat new` when the check takes several commands, or a person needs a URL.

```sh
boat new --no-env --type small --no-snapshots --ttl 3600 --name <task-or-branch> --json
```

- **Use the sandbox's id everywhere.** Take it from the `created` line of the JSON output and pass it to every later command. Your shell does not keep state between tool calls, so `current` and `BOAT_CURRENT_ID` do not reach the next call.
- **Record the id on the task now,** as a provisioned resource (see [executing](../executing/SKILL.md#keep-track-of-resources)), before anything else can fail.
- **Get the work on it:** `boat push <id> <dir>`.
- **Run commands:** `boat exec --timeout <secs> <id> <command>`, with options before the id: anything after the command goes to the command. The default timeout is 30 seconds. For a long run, start it with `--detach` and follow it with `--attach <pid>`. Use `boat ssh -t <id> <command>` when the command needs a terminal.
- `--ttl` is a backstop for a sandbox you forget, not cleanup.

## Let a person try it

`boat host <id> <port>` exposes a port on an HTTPS URL. The URL is private by default, but its token is part of the URL: anyone who has it can open it. Post it only where the people meant to use it will read it. `--public` drops the token; use it only when the operator agrees.

Set the lifetime to cover when the person will look, with `boat extend <id> --hours <n>`. In the brief, say when the sandbox expires and that it will be deleted after the acceptance.

## Evidence

Hand over the command, the machine type, the commit, the output and the cost `boat run` reports. `boat history <id>` lists the commands run in a sandbox that still exists, and `boat history <id> <command-id>` prints one's stored output.

## Clean up

- Delete each sandbox you created once its check is done: `boat delete <id> --yes`. `boat stop` is not cleanup: it keeps a snapshot for 14 days.
- Before you hand over, compare `boat list --json` with the ids you recorded, and delete any of yours that remain. Delete only your own: other sandboxes on the account belong to other work.
- Record each deletion on the task.

## Reference

`boat --help` and `boat <command> --help` are current for the installed version. The [CLI reference](https://docs.boat.dev/cli-reference) covers the rest.
