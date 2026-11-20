# workspace-management

The skill an agent uses to run a workspace's manager: the role that keeps a workspace productive within its budget of usage. It starts operators' epics and tasks, dependency updates and the workspace's standing work, within the budget and the WIP limits; it settles threads whose work is finished, cleans up what they left behind, and keeps the workspace healthy. It also tells other agents how to reach the manager, such as a planner handing over an epic.

The manager is a session and a set of automations. The session runs as shifts: a T3 schedule starts each one in a new thread every 6 hours, so no context lives long enough to drift from the record. The record is a kanban-md task on the workspace board at `/tasks`: its claim names the current shift, its body holds the budget, limits, standing work, duties and automations, and its log carries what each shift did to the next. Operators talk to it in the workspace's Discord channel. The automations (Dagu workflows, Trowel and Vector events, T3 schedules) take over what runs the same way every time. It follows the pattern of `epic-orchestration`'s passes, applied to the whole workspace instead of one epic.

| File | What it is for |
|---|---|
| [SKILL.md](SKILL.md) | The record, shifts and their rotation, the sweep, authority, and how other agents reach the manager |
| [references/setup.md](references/setup.md) | Setting up the board, the manager task and the rotation schedule, and changing them |
| [references/threads.md](references/threads.md) | Settling finished threads, threads waiting on a person, failed threads, stalled work and ledgers |
| [references/dispatch.md](references/dispatch.md) | The budget and the WIP limits, starting epics, dispatching ready tasks and standing work, and requests |
| [references/dependencies.md](references/dependencies.md) | Renovate pull requests in the workspace's repositories: release notes, fixing CI, merging |
| [references/resources.md](references/resources.md) | Worktrees, sandboxes, containers and scratch files that no ledger holds |
| [references/maintenance.md](references/maintenance.md) | Health, fast-forwarding default branches, skills sync, the event path and the observation review |
| [references/automations.md](references/automations.md) | The automations alongside the session: the parts, proven techniques, proposing one and checking they ran |
| [assets/manager-task.md](assets/manager-task.md) | The manager task's body: schedule, channel, budget, limits, standing work, duties, automations, requests and holds |
| [scripts/survey.sh](scripts/survey.sh) | The survey each sweep starts from: threads, boards, dependency updates, ledgers, the budget and health |

## Sources

The skill is written in our own words. It draws on no third-party skill. It applies the passes of `epic-orchestration` (a fresh context for each run, the record as memory, one actor at a time by claim) to the workspace, and draws its cleanup rules from what the workspace's worktree reviews and stalled epics recorded in memory.

Formats and tools the skill uses, rather than drew on:

| Source | License | Use |
|---|---|---|
| [antopolskiy/kanban-md](https://github.com/antopolskiy/kanban-md), version 0.39.0 | MIT | The workspace board, the manager task, its claim and log. |
| [wyrd-company/t3code-client](https://github.com/wyrd-company/t3code-client): `t3c` | MIT | Thread lists, status and reads, the rotation schedule, and usage for the budget. |
| [wyrd-company/deck](https://github.com/wyrd-company/deck) | Ours | The workspace channel in Discord. |
| [Renovate](https://github.com/renovatebot/renovate) | AGPL-3.0 | The dependency update pull requests the manager has checked and merged. Used, not run or bundled. |
| `wyrd-company/workspace-dotfiles`: `docs/ledger.md` | Ours | The `ledger` CLI the cleanup works from. |
