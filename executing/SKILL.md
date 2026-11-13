---
name: executing
description: >
  Use whenever you are performing work, of any kind. Covers understanding the work, working in verifiable units, when to decide and when to ask, proving the result, and handing it over. Hint words from the user or task: `complete`, `do`, `execute`, `implement`, `perform`. Not for just answering questions.
---

Complete the work end to end: from understanding why it exists to a result that someone else can check without asking you.

## Understand

If you do not know why the work has been requested, you cannot make good decisions or judge when it is done.

- Why is the work being performed?
- What is the definition of done?
- How will the output be used, and by whom?

The GitHub issue, when there is one, answers these questions; otherwise the operator's prompt has to carry the context. A task is a ticket to do work, not what, why, or how that allows you to understand. The task may provide additional detail on how to measure done but you should not need it to understand.

Read what already exists before you start: repository documentation, issues, earlier notes on the task, the branch history, and the repository's own instructions. If something is ambiguous and the context does not settle it, report the ambiguity with the reading you chose. Do not guess silently.

## Tasks

- Tasks are the normal "ticket" for doing more than trivial work. You should [expect one](../task-ownership/SKILL.md) or [write one](../task-authoring/SKILL.md).
- Anything else that is low risk and can be accomplished in a few turns does not need a task.
- The sections above the log are agreed scope. Do not change them without approval.

## Scope and authority

- The task and/or the user's prompt is the contract. If the contract is wrong, say so and get it changed by whoever wrote it.
- Do not edit the goal or definition of done to match what you built. 
- The repository's rules are part of the contract. In a fork this includes the fork's own boundary: read its rules and find the check that enforces them before you design anything. If the work cannot be done inside the boundary, stop and ask; do not widen the boundary to fit the design.
- Base the work on the branch it will integrate into, which is not always `main`, and confirm the base is current before substantive work.

## Sequence work into verifiable units

Order the work as a sequence of small units, each ending in a state you can check, and do not advance until the current one is verified.

A problem caught at the unit that caused it is cheap to find. A problem caught after a batch is buried, and you have already built further on a broken base. The same sequence, delivered as commits, lets a reviewer replay the work instead of trusting it.

- Pick the smallest unit that ends in a check.
- Verify before advancing: known-good state, one change, run the check, then proceed. Never defer verification to a final batch.
- Order the units so the sequence builds confidence on its own, for you while executing and for a reviewer reading it afterwards.

When available, track the units in the todo list your harness provides (e.g. `update_plan`,`TodoWrite`,`TaskCreate`).

## Commit each unit

Commit when a small, logical step is complete. Use the conventional commit format. Your git operator must be set before you commit.

- One type of work per commit: a refactor, a behaviour change, or a cleanup. If the message needs "and", split the commit.
- Each commit leaves the work in a valid state: checks pass and nothing is half-wired.
- Stage by explicit path. Tools that format, generate or test can change files you did not edit, so read `git status` after running them and before staging. A change you did not make on purpose is a finding: undo it, or keep it and say so in the commit message.

## Keep track of resources

As you provision resources to implement the work, keep track of what you have provisioned:

- Temp files and folders
- Docker artifacts (containers, volumes, networks, etc)
- VMs
- Running processes (record the process IDs)
- Worktrees and branches
- Threads you have launched

Log to the task. When available, use your built-in todo tracking tools to remind you to cleanup later.

## When to decide and when to ask

The default is to proceed. People supervise asynchronously, most work is reversible and reviewable, and a wrong decision usually costs less to correct than stalled work costs to unblock. Do the work, show the result, and explain the decisions you made along the way so they can be corrected afterwards.

Bring a human in when:

- **They asked to be.** The task, the issue or the operator said to check in at this point, or reserved this decision.
- **It cannot be undone.** Deleting data, force-pushing, releasing, publishing, sending messages outside the company, spending money.
- **It needs something only they have.** Credentials, access, or an account you were not given. Do not look for another way in.
- **It changes the goal.** Product direction and the definition of done come from the people who own them. How to get there is yours.

Everything else is yours to decide, including choices between valid options with no clear winner: pick one, say so out loud, record why on the task, and keep going. 

If the question is still open after real investigation, record what you investigated. While a question is open, carry on with whatever does not depend on the answer, and write anything that does depend on it as pending, not as settled.

When you do ask, make the question cheap to answer:

- Test any claim the question rests on first, and quote the result. The answer will be built on the claim, so an untested claim becomes the contract.
- Trace each option through every rule and document it touches, found by search and not from memory, and state what each option changes. A person can only rule on the consequences you show.
- Give your recommendation.

## Being blocked

We cant anticipate everything up front. When you run into an obstacle, try what you can first.

This is not a mandate to operate unethically or outside the spirit of the work, but to be resourceful.

If you are still stuck after real investigation, [record what you tried](assets/blocked.md) along with the [hand-off](assets/handoff.md), [mark the task blocked](../task-ownership/SKILL.md#blocked), and hand off.

Commit the work in progress, push the branch and remove the worktree, as for a handoff. Name the branch and commit in the log entry.

Notify the thread's operator or agent with delegated authority. How people are notified, and when a person must be brought in at all, is settled in another skill; until it is, use `contact`.

## Be visible

Anywhere where `log`, `report`, or `record` is mentioned refers to this sections instructions.

Record progress as it happens, as units land, at these levels:

- The thread itself.
- `update_plan`, `TodoWrite`, `TaskUpdate`
- **Commits** record each step.
- **The task** is the working log. [Append an entry](../task-ownership/SKILL.md#log) as each unit lands: what landed, the commit, the state of verification, and what is next. Another agent must be able to resume from the task and the git history alone.
- **The GitHub issue or pull request** gets significant progress on the deliverable, written for the people who follow it. It is not a working log. An issue may be served by several tasks/work efforts, so say which part your update covers.

- Every record maps to a real action, and its linked evidence shows what the record claims. 
- Record the forks, pivots and abandoned approaches that shaped the work. 
- Record what you observed. Mark a conclusion as a conclusion.
- A cause or mechanism added after the task was written/work started is executed like the contract, so it carries the same duty: state whether it is measured, inferred or assumed. See [definition-of-done.md](references/definition-of-done.md).
- Link issues to pull requests.
- Add the pull request to the task, when it exists.
- Review findings and replies stay on the pull request; the record links them and records how each was settled.

## Prove it is done

Before starting a unit or a task, ask: "How will I prove this worked?" Then verify the real thing directly. Do not infer from proxies, self-reports, or "it compiles".

- Use the result the way its user will, as close to their experience as you can get.
- Read the actual value, not a cached or derived copy. When verification fails, suspect the method of observation before the system.
- Take each result from the run that produced it, at the commit you are handing over. A skipped check is not a pass, and a run that went quiet has not finished. If a check cannot run, record what you tried and what remains unverified.
- Anything you build that reports an outcome starts as failed and says pass only when a marker shows the run completed. An empty run or a crash must not read as success.
- When verifying delegated work, inspect the output itself (the diff, the file, the behaviour), not the delegate's summary.
- The strongest proof is a script that re-runs the comparison. Keep its output where a reviewer can re-run it.

**Prove the guards.** A passing suite shows a guard is present, not that it works. A check your change relies on for correctness or safety is proved when breaking it makes a test fail. Prove it with the repository's mutation testing tool, as you would write any other test, and hand over the tool's report so the reviewer can accept it without repeating the run.

**Acceptance.** Working is not the same as meeting the user's need. When the bar includes a judgement only the user can make, or the issue or operator asks for it, the work also needs [user-acceptance testing](references/user-acceptance-testing.md). Run it yourself, as the user, before you ask anyone. Acceptance happens only when what you deliver can be used by its user on its own. A part that cannot, such as one child of an epic, is accepted with the whole, where the epic's plan says.

**Say what you observed, not what you concluded.** When you report a cause, name the evidence that rules out the alternatives. A claim that something is absent, or that a list is complete, needs a search, not a list built from the files you happened to open. Count a number yourself before you repeat it.

## Work you discover

Work inside the contract is yours to do. For anything outside it, search the board and issues first, then:

- when it must happen now for this task to finish: Write a task (see `task-authoring`) and record the dependency;
- otherwise raise an issue with its goal and bar, and link it from the log. Do not park it on the board.

If the task and/or issue already exists, update dependencies as appropriate and add/log a comment providing the context of how the task/issue relates to the current work.

## Once work is complete

Every Definition of Done element is met and no decision the work depends on is open at the commit you will be delivering.

Check to see if the target branch moved. If it has, rebase now and correct any merge conflicts.

### Review your own work, then run the expensive checks

Use focused tests and cheap static checks while the work can still change. Read your own diff, tests and prose cold, commit every final change, and only then run the full, live or slow checks, once, on the settled commit. If a file changes afterwards, the earlier result no longer proves the current state: rerun what the change affects.

Hand over for review only when the checks passed at the commit you are handing over and no decision you need is still open; otherwise hand over as blocked, with the failure and the exact question.

### Prepare the review surface

Write the [handoff](assets/handoff.md).

Reread the handoff against its evidence. Each result quoted comes from a run at the handoff commit.

Work is reviewed after the fact, so include evidence that lets a person see the outcome without running anything or reading the transcript: screenshots, recordings, terminal captures, the output of the proving script.

Keep the evidence where the reviewer will look: linked in the pull request, issue and task. Commit it only when it will be reused elsewhere. Upload media to the public R2 bucket `assets-wyrd-foo` using the AWS CLI profile of the same name. Use `<repo>/pr-<number>/...` or `<repo>/issue-<number>/...` as the object path, and link the corresponding `https://assets.wyrd.foo/<object-path>` URL in GitHub descriptions and comments. For example:

```sh
aws --profile assets-wyrd-foo s3 cp ./login.png s3://assets-wyrd-foo/example-repo/pr-123/login.png
```

The public URL is `https://assets.wyrd.foo/example-repo/pr-123/login.png`.

Name a skipped check as unverified. Do not report it as passed.

Note the target branch for the PR: Epics often use an epic branch as the target. Stand-alone work the default is `main`. If you are unsure, ask.

- GitHub PR review (default):
  - Push the branch
  - Open a GitHub PR
- gitpr review (local):
  - create the PR using gitpr
- Non-git review surfaces will be added as they are needed.

### Independent review

Self-review is not a substitute; the point is eyes you cannot bring yourself.

When the task is a child of an epic, do not dispatch the review yourself: release the task for review and stop. The epic's orchestrator dispatches reviews one at a time, in the order it keeps, and sends remediation back to your session.

Otherwise, use `delegate_task` to dispatch the independent review with handoff. Use a different [model family](~/models.yml), when available, than your own. Include the task/definition of done, any issues, the review surface, and whether the reviewer merges on acceptance. The reviewer follows [review](../review/SKILL.md), at the level the task's `risk` sets.

The reviewer may ask questions, answer them directly so they can finish their review.

### Triage Review

The reviewer will return the review surface with a result: Accepted or rejected with findings.

For each finding from the reviewer decide:

- Accept: You will remediate the finding as part of this work.
- Reject: The finding is incorrect, answer the reviewers thread with why the finding is rejected.
- Defer: The finding is correct, but does not need to be addressed as part of this work. Explain why. If the work is part of an epic, recommend if the work is part of the epic or not. Epic may be a task and/or an issue, out of epic is always an issue.

## When the review closes without you

When you find the pull request was merged or closed while you were still working, or the review ended the work rather than asking for changes: do not push, merge or reopen. Leave your local commits where they are. Report which commits the review did not include and whether each looks covered already. Then stop. Whoever dispatched the work decides what happens to the rest. A review round that rejects with findings is not this: triage it, as above.

## Merge

By default you do not have merge authority. 

If you have been granted merge authority perform the merge.

- SSH fast-foward merge GitHub PRs so they close as merged.
- `gitpr merge`

Do not change the branch between approval and merge: a rebase or a late commit means the merged change is not the reviewed one.

## Finalize

When available, check your plan/todo/task built-in tool for outstanding items.

Cean up what you provisioned that is no longer needed: 

- settle launched threads
- remove local branches
- remove worktrees
- stop processes
- remove docker artifacts
- delete scratch files
- Anything else not covered that is no longer needed.

If it is needed beyond your work, it probably should be checked in or documented and provisioned as part of our workspace definition through a raised PR.

Fetch and fast forward main.

Provide a final report listing what was done.

When the task delivers only part of its issue, comment on the issue with what remains. A pull request that closes an issue should close it only when the goal is met.

If you were dispatched by another thread, let them know the work has been completed. If it was the user, notify them.
