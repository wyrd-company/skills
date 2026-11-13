# Task audit

Read this at `normal` and `high`. The review of the change asks whether the work is right. The audit asks how it was done, and what the operator should still scrutinize even when the record is honest.

It is a scan, not a redo of the work. Read:

- the task's log, from the claim to the handoff;
- the executor's thread transcript, when you can read it (`t3_thread_read` with the thread id from the claim);
- the commits, in order.

## What to flag

- **Decisions with weak evidence:** a choice logged with no reason, or a reason the evidence does not support.
- **Verification skipped or claimed without proof:** a check the log says passed with no run in the transcript, a run at an earlier commit, or a failure that went quiet.
- **Risky choices:** work started before a question was answered, scope that grew, a symptom papered over, a test or assertion weakened to get green.
- **Divergence from the record:** the transcript shows something the log does not say, or the log says something the transcript does not show.
- **What a skim would miss:** anything the operator would want to know before relying on the work.

Point each flag at the log entry, commit or moment in the transcript it is about. "No flags" is a valid result.

## Deliver it

On the issue, when there is one, as a comment that does not mention the task or the board:

```markdown
## Task Audit

- <flag, pointing at the commit, the pull request or the moment>

---
Audited by <model>
```

Always in the round's handoff on the task, under **Task audit**. An audit flag that is also a defect in the work is a finding too: report it on the surface with its severity.
