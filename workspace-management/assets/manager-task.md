## Role

The workspace manager's record. The thread that holds this task's claim is the current shift. Shifts run with the `workspace-management` skill, which says how to read and keep this task.

Everything above **Log** is the standing state, which each roll forward carries to the successor task. The log stays with the task it was written on.

- Previous task: {none}

## Schedule

- Rotation schedule: {schedule id}
- Every: 6h
- Roll forward every: 1 day
- Model: {provider instance} {model}
- Git operator: copied from thread {setup thread id}

## Channel

- Workspace channel: {bot}/{channel id}, as `deck --json channels` lists it
- Issues project: {owner}/{project number}

## Budget

Operators set the budget here. The survey reads the daily figure from the row below, in the unit the survey reports spend in.

| Budget | Value |
|---|---|
| Daily budget (USD at list price, all providers) | {amount} |

## Limits

Every dispatch in the workspace is held to these, by the manager and by epic orchestrators alike. Operators change them here.

| Limit | Value |
|---|---|
| Agent threads running at once, across the workspace | 12 |
| Epics in progress at once | 3 |
| Tasks in progress on one board outside `epics/` | 2 |

## Standing work

Work this workspace does on its own. A row is due when its **Last dispatched** is older than its interval. Operators add, remove and retime rows here.

| Name | Every | Complexity | What does it | Last dispatched |
|---|---|---|---|---|

## Duties

A duty that runs each sweep is part of every sweep. Any other duty is due when its **Last done** is older than its interval. Operators add, remove and retime duties here.

| Duty | Every | Last done |
|---|---|---|
| Settle threads and clean up their ledgers | Each sweep | |
| Check running work | Each sweep | |
| Dispatch | Each sweep | |
| Dependency updates | Each sweep | |
| Health | Each sweep | |
| Resources no ledger holds | 1 day | |
| Fast-forward default branches | 1 day | |
| Skills sync | 1 day | |
| Event path | 1 day | |
| Automations | 1 day | |
| Issue triage | 1 day | |
| Issue review | 7 days | |
| Observation review | 7 days | |

## Automations

The automations that do part of the manager's work, one row each. The **Automations** duty checks that each ran within its interval.

| Name | What it does | Where it lives | Runs every |
|---|---|---|---|

## In flight

Delegates the manager is waiting on for a report, such as a repository's dependency updates or an issue triage, one line each: what, the thread, and since when. Remove a line when its report comes back. A later shift does not dispatch the same work again while its line is here.

## Requests

Work an operator or agent asked the manager for that is not finished yet. One line each: who asked, when, the request, and where it stands. Remove a line when the request is done, and log that it is done.

## Holds

Work held back, one line each: what is held, why, and what releases it, such as the budget, a limit or an operator's answer.

## Notices

People the manager notified who have not answered yet, one line each: who, when, what about, and the channel thread. Remove a line when it is answered or no longer matters. A line here is why a later shift does not notify again.

## Log
