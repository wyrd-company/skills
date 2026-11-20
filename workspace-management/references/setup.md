# Setup

Read this when `/tasks` has no manager task or no rotation schedule, or to change the interval, the model, the git operator, the budget or the channel. Setting up is done once for each workspace, by an operator's thread or an agent working for one: the shifts copy their git operator from that thread.

## Before you start

- **`/tasks` is the workspace's tasks checkout.** `git -C /tasks branch --show-current` prints `workspace/<workspace>`, where `<workspace>` is `workspace` in `/etc/workspace/config.yml`. The workspace definition mounts it. When it is missing, stop and ask the operator: a board made anywhere else is not found by the survey or by other agents.
- **This thread has a git operator,** shown by `git operator`. The shifts copy it, so it must be the operator the manager works for.
- **No manager task exists yet:** `kanban-md --json list --tag workspace-manager --dir /tasks` lists none, archived tasks aside. When one exists, change it instead, as [below](#change-the-schedule).

## Set up

1. **Make the workspace board,** unless `/tasks/config.yml` already exists. Answer no when `init` offers to ignore it: the board is committed. Set the claim timeout longer than the rotation interval, so the claim stays live while a shift is idle and other agents can find the manager.

   ```bash
   echo n | kanban-md init --dir /tasks --name "<Workspace name> workspace"
   kanban-md config set claim_timeout 8h --dir /tasks
   ```

2. **Choose the shift's model** from [models.yml](~/models.yml): the cheapest entry that lists `low` complexity. A shift does what the record settles and escalates the rest, as an epic's pass does.
3. **Create the rotation schedule** in the T3 project for `/workspace`, with a new thread for each run. `t3c schedule create --help` lists the options.

   ```bash
   t3c --json schedule create --title "Workspace manager" --every 6h \
     --thread-mode new_thread --project-path /workspace --root --mode full-access \
     --provider <provider instance> --model <model> \
     --prompt "Run a shift of the workspace manager, with the workspace-management skill. Copy the git operator from thread $T3CODE_THREAD_ID."
   ```

4. **Find the workspace channel:** the text channel in `deck --json channels` named for the workspace. When there is none, ask the operator: without it the manager can reach people only in T3 Code.
5. **Create the workspace's issues project,** unless the operator names one: `gh project create --owner <org> --title "<Workspace name> workspace"`, then add the priority field with `gh project field-create <number> --owner <org> --name Priority --data-type SINGLE_SELECT --single-select-options "High,Medium,Low"`. Its built-in **Status** field needs the options `Backlog`, `Todo`, `In Progress` and `Done`: add the ones it lacks in the project's settings, or ask the operator to. The first issue triage fills it.
6. **Ask the operator for the daily budget.** It is theirs to set: the manager spends up to it. The unit is the one the survey reports spend in.
7. **Create the manager task** from [the template](../assets/manager-task.md), with the schedule's id, this thread's id, the model, the channel, the issues project and the budget filled in. Keep the template's limits and duties unless the operator gave others, and add the standing work the operator names. Leave it unclaimed: the first shift claims it.

   ```bash
   kanban-md create "Workspace manager $(date -u +%F)" --dir /tasks --status todo \
     --tags workspace-manager --body "$(cat manager-task.md)"
   ```

8. **Commit and push the board,** staging its paths by name:

   ```bash
   git -C /tasks add config.yml activity.jsonl tasks
   git -C /tasks commit -m "chore: set up the workspace manager"
   git -C /tasks push
   ```

9. **Start the first shift now,** with `t3c schedule run <id>`, instead of waiting for the interval. When its first turn ends, check that `/tasks/manager.json` names the new thread, the manager task's claim does too, and its log has the takeover.

Setup is done when the manager task names the schedule, a shift holds its claim, `/tasks/manager.json` names that shift, and the board is pushed.

## Change the schedule

Change the schedule with `t3c schedule update <id>`, then change the manager task's **Schedule** section to match, and log the change. The schedule and the task say the same thing, or the next shift acts on the wrong one.

- **The interval:** `--every <interval>`. Keep the board's `claim_timeout` longer than it, and the task's **Roll forward every** at least as long.
- **The model:** `--provider` and `--model`.
- **The git operator:** the shifts copy it from the thread the prompt names. When that thread's registration is lost, such as after the container is rebuilt, the shifts cannot commit. Register the operator again in that thread, or update `--prompt` to name a thread that has one.

The budget, the limits, the standing work, the duties, the channel and the issues project live only in the manager task: change them there, and log the change.

To stop the manager, disable the schedule with `t3c schedule disable <id>`, and log why on the manager task. The last shift's claim lapses, and other agents then leave what they hand over in its place, as [Reach the manager](../SKILL.md#reach-the-manager) says.
