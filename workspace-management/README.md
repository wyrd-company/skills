# workspace-management

The skill an agent uses to run a workspace's manager: the role that keeps a workspace productive within its budget of usage. It starts operators' epics and tasks, dependency updates, high-priority issues and the workspace's standing work, within the budget and the WIP limits; it settles threads whose work is finished, cleans up what they left behind, and keeps the workspace healthy. It also tells other agents how to reach the manager, such as a planner handing over an epic.

The manager is a session and a set of automations. The session runs as shifts: a T3 schedule starts each one in a new thread every 6 hours, so no context lives long enough to drift from the record. The record is a kanban-md task on the workspace board at `/tasks`: its claim names the current shift, its body holds the budget, limits, standing work, duties and automations, and its log carries what each shift did to the next. The task rolls forward daily, so no task grows without end, and `/tasks/manager.json` names the current shift for scripts and workflows. Open issues are ranked in a GitHub project for the workspace. Operators talk to it in the workspace's Discord channel. The automations (Dagu workflows, Trowel and Vector events, T3 schedules) take over what runs the same way every time. It follows the pattern of `epic-orchestration`'s passes, applied to the whole workspace instead of one epic.

| File | What it is for |
|---|---|
| [SKILL.md](SKILL.md) | The record, shifts and their rotation, the sweep, authority, and how other agents reach the manager |
| [references/setup.md](references/setup.md) | Setting up the board, the manager task and the rotation schedule, and changing them |
| [references/threads.md](references/threads.md) | Settling finished threads, threads waiting on a person, failed threads, stalled work and ledgers |
| [references/dispatch.md](references/dispatch.md) | The budget and the WIP limits, starting epics, dispatching ready tasks and standing work, and requests |
| [references/dependencies.md](references/dependencies.md) | Renovate pull requests in the workspace's repositories: release notes, fixing CI, merging |
| [references/issues.md](references/issues.md) | Ranking open issues in the workspace's project, reviewing the ranking, and starting high-priority issues |
| [references/resources.md](references/resources.md) | Worktrees, sandboxes, containers and scratch files that no ledger holds |
| [references/maintenance.md](references/maintenance.md) | Health, fast-forwarding default branches, skills sync, the event path and the observation review |
| [references/automations.md](references/automations.md) | The automations alongside the session: the parts, proven techniques, proposing one and checking they ran |
| [assets/manager-task.md](assets/manager-task.md) | The manager task's body: schedule, channel, budget, limits, standing work, duties, automations, requests, holds, notices and the log |
| [scripts/survey.sh](scripts/survey.sh) | The survey each sweep starts from: threads, boards, dependency updates, issues, ledgers, the budget and health |
| [scripts/takeover.sh](scripts/takeover.sh) | A shift's takeover, one at a time: the claim, rolling the manager task forward, and the pointer file |
| [scripts/budget.sh](scripts/budget.sh) | Today's spend against the budget, for the survey and for epic orchestrators |
| [scripts/manager.sh](scripts/manager.sh) | Every read of the manager and write to the manager task, under the takeover's lock |
| [scripts/manager-lib.sh](scripts/manager-lib.sh) | What the scripts share: the lock, reading the manager task, and parsing its standing state |

## Sources

The skill is written in our own words. It draws on no third-party skill. It applies the passes of [epic-orchestration](../epic-orchestration/SKILL.md), in this repository, to the workspace: a fresh context for each run, the record as memory, one actor at a time by claim. Its cleanup and dispatch rules draw on observations recorded in memory up to 2026-11-20 (notes `workspace-survey-2026-11-19-unanswered-thread-questions-unen-e559b0c0`, `toolchain-devcontainer-runs-vector-trowel-and-dagu-but-none--3f3ce247`, `epic-planning-hand-off-the-workspace-manager-is-undefined-an-54954b54` and `workspace-manager-gaps-2026-11-20-usage-limits-unsupported-d-8a3a802a`). Its budget, dependency, issue and rotation rules are the operator's decisions of that date (note `workspace-manager-decisions-renovate-via-release-note-review-8ddc5b9e`). Its takeover's lock and recovery answer the reviews of [#33](https://github.com/wyrd-company/skills/pull/33).

Formats and tools the skill uses, rather than drew on:

| Source | License | Use |
|---|---|---|
| [antopolskiy/kanban-md](https://github.com/antopolskiy/kanban-md), version 0.39.0 | MIT | The workspace board, the manager task, its claim and log. |
| [wyrd-company/t3code-client](https://github.com/wyrd-company/t3code-client): `t3c`, version 0.2.3 | MIT | Thread lists, status and reads, the rotation schedule, and usage for the budget. |
| [wyrd-company/deck](https://github.com/wyrd-company/deck), version 0.1.2 | Apache-2.0 | The workspace channel in Discord. |
| [Renovate](https://github.com/renovatebot/renovate) | AGPL-3.0 | The dependency update pull requests the manager has checked and merged. Used, not run or bundled. |
| `wyrd-company/workspace-dotfiles`: `docs/ledger.md` | Ours | The `ledger` CLI the cleanup works from. |
