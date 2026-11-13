# Dispatch

Read this when a task is ready for its next agent: to implement, remediate, review or accept it. It covers the check before you send anyone, the prompt, the model, and keeping siblings that run in parallel from colliding.

## Before every dispatch

Read the record yourself, not a summary of it: the status, the claim, the blocked mark, and the task's own gates (`hitl`, `council`, its dependencies, and anything its Definition of Done says about order or approval). If these do not add up to one clear next step, do not dispatch: escalate.

Confirm that any handoff before this one is complete and that the previous agent has stopped.

## The prompt

Dispatch each task to its own agent session, which outlives the pass. Keep the prompt minimal and do not paste the task into it:

```text
<Implement|Remediate|Review|Accept> task <id> on board <dir>. Epic task: <id>.
Base: <epic branch> at <sha>
Merge on acceptance: <yes, as the Authority section delegates | no: accept and hand off> (reviews only)
Surfaces in play: <for parallel siblings: what else is being touched, and by which task>
```

Choose the model and effort from the task's `complexity`, or its `model` and `effort` when set, and [models.yml](~/models.yml). For a review, choose from the task's `risk` instead: a `low` review suits a cheap model, and a `high` one a strong model from a different family than the executor's. Send remediation back to the executor's own session: it holds the context, and its claim names its thread.

## Siblings in parallel

When siblings run in parallel off one base, they cannot see each other's work, and collide on the same shared surfaces: command wiring, exported names, shared scripts and CI, plugin directories, schemas and fixtures, test tooling and its configuration. Name the surfaces in play in each sibling's prompt.

- When siblings must ship the same file, have an escalation rule one reference commit, and have the others take it with `git cherry-pick`. Two independently written copies conflict; a cherry-picked one drops out at the rebase.
- When one task produces something and a parallel task consumes it, name the task that owns the end-to-end test. Each side's tests pass without the other, so it can merge half-wired.
