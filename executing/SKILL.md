---
name: executing
description: >
  Use whenever you are carrying out a task yourself, of any kind: code, design, research, content, configuration. Covers understanding the task, working in verifiable units, when to decide and when to ask, proving the result, and handing it over. Hint words from the user or task: `complete`, `do`, `execute`, `implement`, `perform`
---

Work the task end to end: from understanding why it exists to a result that someone else can check without asking you.

## Understand

If you do not know why the task exists, you cannot make good decisions or judge when it is done.

- Why is the work being performed? The GitHub issue, when there is one, defines the goal or deliverable; the task is the ticket to do the work.
- What is the definition of done?
- How will the output be used, and by whom?

Read what already exists before you start: earlier notes on the task, the branch history, and the repository's own instructions. If something is ambiguous and the context does not settle it, record the ambiguity on the task with the reading you chose. Do not guess silently.

## Scope and authority

- The task is the contract. Do not edit its goal or definition of done to match what you built. If the contract is wrong, say so on the task and get it changed by whoever wrote it.
- The repository's rules are part of the contract. In a fork this includes the fork's own boundary: read its rules and find the check that enforces them before you design anything. If the task cannot be done inside the boundary, stop and ask; do not widen the boundary to fit the design.
- Base the work on the branch it will integrate into, which is not always `main`, and confirm the base is current before substantive work.

## Sequence work into verifiable units

Order the work as a sequence of small units, each ending in a state you can check, and do not advance until the current one is verified.

A problem caught at the unit that caused it is cheap to find. A problem caught after a batch is buried, and you have already built further on a broken base. The same sequence, delivered as commits, lets a reviewer replay the work instead of trusting it.

- Pick the smallest unit that ends in a check.
- Verify before advancing: known-good state, one change, run the check, then proceed. Never defer verification to a final batch.
- Order the units so the sequence builds confidence on its own, for you while executing and for a reviewer reading it afterwards.

Track the units in the task list your harness provides, so the plan and its progress are visible while you work.

## Commit each unit

Commit when a small, logical step is complete. Use the conventional commit format. Your git operator must be set before you commit.

- One type of work per commit: a refactor, a behaviour change, or a cleanup. If the message needs "and", split the commit.
- Each commit leaves the work in a valid state: checks pass and nothing is half-wired.
- Stage by explicit path. Tools that format, generate or test can change files you did not edit, so read `git status` after running them and before staging. A change you did not make on purpose is a finding: undo it, or keep it and say so in the commit message.

## When to decide and when to ask

The default is to proceed. People supervise asynchronously, most work is reversible and reviewable, and a wrong decision usually costs less to correct than a stalled task costs to unblock. Do the work, show the result, and explain the decisions you made along the way so they can be corrected afterwards.

Bring a human in when:

- **They asked to be.** The task, the issue or the operator said to check in at this point, or reserved this decision.
- **It cannot be undone.** Deleting data, force-pushing, releasing, publishing, sending messages outside the company, spending money.
- **It needs something only they have.** Credentials, access, or an account you were not given. Do not look for another way in.
- **It changes the goal.** Product direction and the definition of done come from the people who own them. How to get there is yours.

Everything else is yours to decide, including choices between valid options with no clear winner: pick one, record why on the task, and keep going. If you are stuck after real investigation, that is a blocker to record on the task and hand off, not a reason to wait in silence.

While a question is open, carry on with whatever does not depend on the answer, and write anything that does depend on it as pending, not as settled.

When you do ask, make the question cheap to answer:

- Test any claim the question rests on first, and quote the result. The answer will be built on the claim, so an untested claim becomes the contract.
- Trace each option through every rule and document it touches, found by search and not from memory, and state what each option changes. A person can only rule on the consequences you show.
- Give your recommendation.

## Be visible

A session can end at any moment, and the moment it most often ends is between finishing the work and reporting it. Record progress as it happens, at three levels:

- **Commits** record each step.
- **The task** is the working log. Append an entry as each unit lands: what landed, the commit, the state of verification, and what is next. Another agent must be able to resume from the task and the git history alone.
- **The GitHub issue or pull request** gets significant progress on the deliverable, written for the people who follow it. It is not a working log.

Keep the log true. Every entry maps to a real action, and its evidence shows what the entry claims. Log the forks, pivots and abandoned approaches that shaped the work. If the work diverged from what an entry says, fix the entry.

## Prove it is done

Before starting a unit or a task, ask: "How will I prove this worked?" Then verify the real thing directly. Do not infer from proxies, self-reports, or "it compiles".

- Use the result the way its user will, as close to their experience as you can get.
- Read the actual value, not a cached or derived copy. When verification fails, suspect the method of observation before the system.
- Take each result from the run that produced it, at the commit you are handing over. A skipped check is not a pass, and a run that went quiet has not finished. If a check cannot run, record what you tried and what remains unverified.
- Anything you build that reports an outcome starts as failed and says pass only when a marker shows the run completed. An empty run or a crash must not read as success.
- When verifying delegated work, inspect the output itself (the diff, the file, the behaviour), not the delegate's summary.
- The strongest proof is a script that re-runs the comparison. Keep its output where a reviewer can re-run it.

**Prove the guards.** A passing suite shows a guard is present, not that it works. A check your change relies on for correctness or safety is proved when breaking it makes a test fail. Prove it with the repository's mutation testing tool, as you would write any other test, and hand over the tool's report so the reviewer can accept it without repeating the run.

**Say what you observed, not what you concluded.** When you report a cause, name the evidence that rules out the alternatives. A claim that something is absent, or that a list is complete, needs a search, not a list built from the files you happened to open. Count a number yourself before you repeat it.

## Review your own work, then run the expensive checks

Use focused tests and cheap static checks while the work can still change. Read your own diff, tests and prose cold, commit every final change, and only then run the full, live or slow checks, once, on the settled commit. If a file changes afterwards, the earlier result no longer proves the current state: rerun what the change affects.

## Independent review

Before handing over, have the work reviewed by an agent on a different model family from the one that did it. Self-review is not a substitute; the point is eyes you cannot bring yourself.

Point the reviewer at the task and any issue, and give it your thread id. Answer every finding: addressed, rejected with a reason, deferred with a destination, or answered.

## Show your work

Work is reviewed after the fact, so leave evidence that lets a person see the outcome without running anything or reading the transcript: screenshots, recordings, terminal captures, the output of the proving script.

Keep the evidence where the reviewer will look: attached to the pull request, the issue or the task. Commit it only when it will be reused elsewhere.

## Hand over

A handover is complete when someone else can check the result or resume the work from the task record and the git history. Hand over for review only when the checks passed at the commit you are handing over and no decision you need is still open; otherwise hand over as blocked, with the failure and the exact question. Once the work is merged, clean up what you created: branches, worktrees, processes and scratch files.
