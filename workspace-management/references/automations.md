# Automations

Read this when the **Automations** duty is due, or when a shift does the same steps by hand each time and they could run without it.

The manager is a session and a set of automations. The session decides: what is ready, what is finished, what needs a person. Automations do the rest:

- **What runs the same way every time.** A fast-forward of a default branch needs no judgment, and a session spends budget doing it.
- **What must happen between shifts.** A shift wakes every 6 hours, or when a message arrives. An event that needs an answer sooner, such as a push upstream or a board's task moving, needs something listening for it.

Build the automations up over time. When a duty or a standing work row runs the same steps on every run and its log shows no judgment in them, propose an automation for it. Once the automation runs, the row names it, and the shift only checks that it ran.

## The parts

| Part | What it does | Where it is |
|---|---|---|
| T3 schedules | Start a thread on an interval, or on demand with `t3c schedule run`. The rotation and each epic's passes run this way. | `t3c schedule list` |
| `t3c` | From a script: start a thread (`t3c thread start`), message one (`t3c thread send`), wait on one, or run a schedule. | `t3c --help` |
| Dagu | Runs workflows on a schedule, on an event, or on demand, with retries and a run history. | The `workflows` repository: `/workflows/local` for this workspace, `/workflows/main` for what every workspace shares. Runs: `dagu history <workflow>` and the Dagu web view. |
| Trowel | Subscribes to NATS and delivers to Dagu: the organisation's GitHub webhooks, which the org's Trowel publishes, and this workspace's own subjects. | `/etc/trowel` |
| Vector | Watches files, such as a board's `activity.jsonl`, and publishes what it keeps to NATS. | `/etc/vector` |
| `deck` | Posts to the workspace channel and reads replies, from a session or a script. | [contact](../../contact/SKILL.md) |

They connect in one shape: a source (a file Vector watches, a GitHub webhook, a time) reaches Dagu through NATS and Trowel, or on Dagu's own schedule, and the workflow does the work in a script, or wakes a thread with `t3c` when the work needs judgment. Keep the judgment in the thread: a workflow that decides is a session without a record.

## Techniques

What is proven in this workspace, to reuse:

- **Wake a thread on an event.** Epics' event path: Vector and Trowel turn board and GitHub events into a Dagu run that runs the epic's schedule, with the interval as the backstop. See epic-orchestration's [devcontainer](../../epic-orchestration/references/devcontainer.md).
- **Apply an upstream change when it lands.** The shared workflows in `/workflows/main/sub-dags`: `fork-sync` rebases a fork when its upstream's default branch moves, and the `workspace-update-*` workflows reapply the dotfiles, Ansible and workflows after a push to their repositories.

Add a technique here, by a pull request to this skill, once an automation built on it has run in a workspace.

## Propose an automation

1. **Write a task for it** on the workspace board, with [task-authoring](../../task-authoring/SKILL.md): what the automation replaces, the steps from the shift's log, its trigger, and what the shift should see when it fails. The work goes in the `workflows` repository, as `/workflows/local/AGENTS.md` says: on the workspace's branch, or on `main` when every workspace can use it.
2. **Dispatch it** like any ready task, within the budget and the limits.
3. **When it is merged and running,** add it to the manager task's **Automations** section, and change the duty or standing work row to name it.

## Check the automations

For each row of the manager task's **Automations** section, check that it ran within its interval and its last runs did not fail. For a Dagu workflow: `dagu history <workflow> --last <interval>`, and `--status failed`. For a schedule: `t3c schedule show <id>`. Report what did not run or failed to the operator once, and do its work by hand meanwhile when it is a duty. Set the duty's **Last done**, and log what you found.
