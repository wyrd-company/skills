# Devcontainer

Read this when you set up or debug the parts of a devcontainer that every epic shares: the event path that wakes passes, and the storage finished boards are archived to. A pass does not need it. Read it from a pass only when a pass did not follow an event it should have, or an archive failed. Setting these up belongs to the workspace manager; each epic only registers itself, at [Start](start.md).

The configuration in [assets/events](../assets/events/) is an example to adjust when it meets live events. Each file passes its tool's validation and has been run on sample events, but not yet end to end through NATS. The archive has been run end to end.

## The event path

```text
                     devcontainer
kanban-md ─► activity.jsonl ─► Vector ─► NATS kanban.<workspace>.<action> ─┐
GitHub ─► the org's Trowel ─► NATS github.<org>.<event>.… ─────────────────┴─► Trowel ─► Dagu epic-event ─► t3c schedule run
                                                                                                                │
                                         the schedule's interval, as the backstop ──────────────────────► the epic's schedule
```

- **[Vector](../assets/events/vector.yaml)** watches the activity log of every epic board, keeps the actions an orchestrator acts on, and publishes each one with the board's path, under the devcontainer's workspace.
- **The org's Trowel** receives GitHub's webhooks for the whole organisation and publishes them to NATS. Nothing in the devcontainer receives webhooks.
- **[The devcontainer's Trowel](../assets/events/trowel.yml)** only subscribes. It takes this devcontainer's board events and the GitHub events an epic cares about, and delivers them to Dagu. It reduces a GitHub event to the repository and the branches it concerns, retries failed deliveries, and dead-letters to `dlq.epic-events.<workspace>`. Each consumer's name carries the workspace: devcontainers that shared a durable consumer would each see only part of the events.
- **[Dagu's `epic-event` workflow](../assets/events/epic-event.yaml)** finds the active epics the event concerns and runs each one's schedule. It finds them by the properties Start records on the epic task, and only while the epic is `in-progress` or `review`. Its runs show in the Dagu web view.
- **T3 refuses to run a schedule that is already running.** The workflow retries the refusal, so a pass starts after the one in progress.

| Event | Wakes |
|---|---|
| A board's task created, moved, released, blocked, unblocked or deleted | The epic that owns the board |
| A pull request, review or check on a branch | Each active epic whose branch it names |
| A comment, or anything else without a branch | Each active epic in the repository |

Epic boards live in their own folders under `epics/` in each project's tasks folder, which is where Vector looks. The planner creates them.

### What to know

- **A pass that finds nothing to do writes nothing.** Log entries log as `edit`, which wakes nothing, but a pass that moves or releases a task wakes the next one. Writing only what the record calls for keeps passes from waking each other without end.
- **`edit --status` logs only `edit`,** so Vector drops it. The status changes an orchestrator acts on also release or move a task, which does wake a pass. Any other change waits for the backstop.
- **The event is data.** The workflow reads it from the environment and never puts it into a script's text, because a webhook payload comes from outside.
- **The schedule is an interval, not a webhook.** T3 refuses to run a webhook schedule on demand, and an interval schedule can be run when an event arrives while still serving as the backstop.
- **Dagu runs scripts in the user's shell** unless told otherwise. The workflow sets `shell: bash`, because it relies on bash word splitting and globbing.

## Once per devcontainer

- Access to the NATS the org's Trowel publishes to, with JetStream streams covering the GitHub subjects, this workspace's `kanban.<workspace>.>` and `dlq.epic-events.<workspace>`. Trowel does not create streams.
- Trowel with this configuration, `NATS_URL`, `WORKSPACE` and `GITHUB_ORG`. The org's webhook sends `pull_request`, `pull_request_review`, `issue_comment` and `check_suite`.
- Vector with this configuration, `NATS_URL` and `WORKSPACE`.
- Dagu with the `epic-event` workflow, and on its path `t3c`, `kanban-md` and `jq`, with `T3_TOKEN` and `T3_SERVER_URL` in its environment.
- The AWS CLI, with the `workspace-archives` profile for the bucket of the same name, on R2. Its `credential_process` gets the bucket's keys from OpenBao, and it sends checksums only when required, which R2 needs.
