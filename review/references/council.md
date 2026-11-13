# Council

Read this when the task sets `council`, or the operator asks for one. A council puts the verdict in the hands of several strong models from different providers. Different models miss different things, and in matters of taste one model's sensibility is not enough.

You run the council: you form it, brief it, combine what it returns, and hold the round as you would alone. The level still decides how deep the review goes. The council decides the verdict.

## Form it

- **Members:** the number the task's `council` sets, three when it gives none. One strong model from each provider, at high effort, unless the task or the operator names the members.
- **Resolve them** with `orchestrator_capabilities`, and start each with `delegate_task`, in parallel. If a named member or a third provider is not available, say so to whoever dispatched you. Do not substitute.
- **Read-only.** Members review and report. They do not comment on the surface, change the work, or write to the task.

Give each member the surface and its head, the contract, the level and the [skill](../SKILL.md) to review with, and ask for findings with severity, a verdict, and a score out of 10 when the task asks for scores. Do not give them each other's results.

## Combine

- **Verify each finding yourself** before it goes on the surface, as you would a lens's. Merge duplicates, and keep the member who raised each.
- **The verdict is accepted only when every member accepts.** When members disagree on a finding, put both readings in the handoff and decide whether it blocks. When you cannot, escalate as the skill says.
- **Report a member that did not return** as `not run`. It is not an acceptance.
- **Keep the scope.** Each round, members find more to want. A finding outside the contract is an issue, not a reason to reject. Holding the council to the contract is your job.

## Rounds and scores

A fresh review after remediation is a new round, with the same members. When the task asks for scores, keep them in a table in the pull request description, before the attribution line. Edit the description; do not post a comment for it.

```markdown
## Council review

Rounds: 2

| Member | Round 1 | Round 2 |
| --- | --- | --- |
| <model> | 7/10 | 9/10 |
| <model> | 8/10 | 10/10 |
| <model> | 7/10 | no score |
```

Write `no score` when a member gives none. Never invent one. With no pull request, the table goes in the handoff.
