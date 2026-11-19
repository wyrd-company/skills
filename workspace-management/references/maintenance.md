# Maintenance

Read this when a duty in the manager task's **Duties** section is due. A duty with an interval is due when the log has no `Duty <name>: done` entry within it. Log that entry when you finish a duty, and log a duty you could not finish with what stopped it, so the next shift does not read silence as success.

The duties that run on each sweep (settling threads, checking running work and dispatch) are in [threads](threads.md) and [dispatch](dispatch.md). The duty **Resources no ledger holds** is in [resources](resources.md). A duty that operators add without a section here or a reference says in its own row what to do. When it does not, ask the operator who added it.

## Health

On each sweep, read the survey's **Health** section. Notify the operator once when a measure crosses its line, and log it:

- a filesystem more than 85% full;
- processes above half of the cgroup's limit;
- available memory below 10%.

Processes running out ended executor sessions with their claims live before: when processes are high, start nothing new until they fall, and record the hold.

## Fast-forward default branches

Each repository folder's default-branch worktree (`main`, or `fork` for a fork) only follows its remote. Fast-forward each one:

```bash
for wt in /workspace/*/*/main /workspace/*/*/fork; do
  [ -e "$wt/.git" ] || continue
  git -C "$wt" pull --ff-only --quiet || echo "not fast-forwarded: $wt"
done
```

A worktree that cannot fast-forward has local changes or commits, which someone made against the rule that it is only pulled. Report it to the operator: do not reset it, because its changes may be the only copy.

## Skills sync

Run `skills sync`. It updates the base clone and rebuilds the skills every agent reads, as the [workspace standard](../../standards/references/workspace.md#skill-overlays) says. When it fails, the previous build stays in place: report the failure and the paths it names.

## Event path

Check that the event path that wakes epic passes is set up and healthy, as epic-orchestration's [devcontainer](../../epic-orchestration/references/devcontainer.md) reference describes: Dagu has the `epic-event` workflow and its runs in the last day did not fail, and the dead-letter subject `dlq.epic-events.<workspace>` holds no new messages. Report what is missing or failing. Without the event path, epics move only on their backstop interval.

## Observation review

Agents record what they learn about the process, the tools and the skills as observations in memory. A review reads them together and decides what a series of them calls for: a skill, an instruction or a lever. Dispatch it with `delegate_task`, on the cheapest model in [models.yml](~/models.yml) that lists `high` complexity, within the thread limit:

```text
Review the observations recorded in memory since <date of the last review>: notes tagged `observation`, across every vault. Group the related ones, and for each group decide whether it calls for a change to a skill, an instruction or a check, or for nothing yet. Propose each change as a pull request or an issue in the repository it belongs to, linking the observations. Return the list of groups, with what you proposed for each. Copy the git operator from thread <your thread id>.
```

Log the dispatch, and the duty as done when its report comes back.
