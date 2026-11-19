# workspace-management

The skill an agent uses to run a workspace's manager: the role that knows what work is under way in the workspace, starts epics and ready tasks within the workspace's WIP limits, settles threads whose work is finished, cleans up what they left behind, and keeps the workspace healthy. It also tells other agents how to reach the manager, such as a planner handing over an epic.

The manager runs as shifts. A T3 schedule starts each shift in a new thread every 6 hours, so no context lives long enough to drift from the record. The record is a kanban-md task on the workspace board at `/tasks`: its claim names the current shift, its body holds the limits and duties, and its log carries what each shift did to the next. It follows the pattern of `epic-orchestration`'s passes, applied to the whole workspace instead of one epic.

| File | What it is for |
|---|---|
| [SKILL.md](SKILL.md) | The record, shifts and their rotation, the sweep, authority, and how other agents reach the manager |
| [references/setup.md](references/setup.md) | Setting up the board, the manager task and the rotation schedule, and changing them |
| [references/threads.md](references/threads.md) | Settling finished threads, threads waiting on a person, failed threads, stalled work and ledgers |
| [references/dispatch.md](references/dispatch.md) | The WIP limits, starting epics, dispatching ready tasks, and requests |
| [references/resources.md](references/resources.md) | Worktrees, sandboxes, containers and scratch files that no ledger holds |
| [references/maintenance.md](references/maintenance.md) | Health, fast-forwarding default branches, skills sync, the event path and the observation review |
| [assets/manager-task.md](assets/manager-task.md) | The manager task's body: schedule, limits, duties, requests and holds |
| [scripts/survey.sh](scripts/survey.sh) | The survey each sweep starts from: threads, boards, ledgers and health |

## Sources

The skill is written in our own words. It draws on no third-party skill. It applies the passes of `epic-orchestration` (a fresh context for each run, the record as memory, one actor at a time by claim) to the workspace, and draws its cleanup rules from what the workspace's worktree reviews and stalled epics recorded in memory.

Formats and tools the skill uses, rather than drew on:

| Source | License | Use |
|---|---|---|
| [antopolskiy/kanban-md](https://github.com/antopolskiy/kanban-md), version 0.39.0 | MIT | The workspace board, the manager task, its claim and log. |
| [wyrd-company/t3code-client](https://github.com/wyrd-company/t3code-client): `t3c` | MIT | Thread lists, status and reads, and the rotation schedule. |
| `wyrd-company/workspace-dotfiles`: `docs/ledger.md` | Ours | The `ledger` CLI the cleanup works from. |
