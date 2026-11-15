# ledger

The skill an agent uses to keep a record of what its thread or task acquires (sandboxes, worktrees, branches, processes, deployments) together with how to remove each one, so that whoever cleans up later works from a list instead of a transcript. It covers recording a resource, handing it off to the ledger now responsible for it, and cleaning up a ledger. `executing` points to it from keeping track of resources and finalizing, and `boat` from its cleanup.

The workspace installs the `ledger` CLI through `workspace-dotfiles`; see its [ledger](https://github.com/wyrd-company/workspace-dotfiles/blob/main/docs/ledger.md) document. Ledgers are Skate databases in the workspace's `state/charm`, mounted by `workspace-template`.

| File | What it is for |
|---|---|
| [SKILL.md](SKILL.md) | Which ledger, recording, handing off and cleaning up |

## Sources

The skill is written in our own words. It draws on no other skill.

Formats and tools the skill uses, rather than drew on:

| Source | License | Use |
|---|---|---|
| [Skate](https://github.com/charmbracelet/skate), version 1.1.0 | MIT | The key-value store the ledgers are kept in. |
| `wyrd-company/workspace-dotfiles`: `docs/ledger.md` | Ours | The `ledger` CLI the skill names. |
