# boat

The skill an agent uses to run a check on a clean, disposable machine: a [Boat](https://boat.dev) sandbox. It covers when a sandbox proves more than the workspace can, `boat run` for one command and `boat new` for several steps or a URL a person can try, the plan's cost, keeping secrets off the sandbox, and deleting every sandbox it made. `executing` and `review` point to it from proving work, user-acceptance testing and cleanup.

The workspace installs the CLI and its OpenBao-backed wrapper through `workspace-dotfiles`; see its [Boat](https://github.com/wyrd-company/workspace-dotfiles/blob/main/docs/boat.md) document.

| File | What it is for |
|---|---|
| [SKILL.md](SKILL.md) | When to use a sandbox, the safe defaults, running, hosting, evidence and cleanup |

## Sources

The skill is written in our own words. It draws on no other skill.

Formats and tools the skill uses, rather than drew on:

| Source | License | Use |
|---|---|---|
| [Boat CLI](https://docs.boat.dev/cli-reference), version 1.0.100 | Proprietary | The commands and options the skill names, read from the CLI's `--help`. |
| `wyrd-company/workspace-dotfiles`: [docs/boat.md](https://github.com/wyrd-company/workspace-dotfiles/blob/0b46c2cdc46f60dfe071950229a6a1250d0e90f7/docs/boat.md) | Ours | How the CLI is installed and gets its API key. |
