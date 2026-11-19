## Role

The workspace manager's record. The thread that holds this task's claim is the current shift. Shifts run with the `workspace-management` skill, which says how to read and keep this task.

## Schedule

- Rotation schedule: {schedule id}
- Every: 6h
- Model: {provider instance} {model}
- Git operator: copied from thread {setup thread id}

## Limits

Every dispatch in the workspace is held to these, by the manager and by epic orchestrators alike. Operators change them here.

| Limit | Value |
|---|---|
| Agent threads running at once, across the workspace | 12 |
| Epics in progress at once | 3 |
| Tasks in progress on one board outside `epics/` | 2 |

## Duties

A duty that runs each sweep is part of every sweep, and is not logged as done. Any other duty is due when the log has no entry `Duty <name>: done` within its interval. Operators add, remove and retime duties here.

| Duty | Every |
|---|---|
| Settle threads and clean up their ledgers | Each sweep |
| Check running work | Each sweep |
| Dispatch | Each sweep |
| Health | Each sweep |
| Resources no ledger holds | 1 day |
| Fast-forward default branches | 1 day |
| Skills sync | 1 day |
| Event path | 1 day |
| Observation review | 7 days |

## Requests

Work an operator or agent asked the manager for that is not finished yet. One line each: who asked, when, the request, and where it stands. Remove a line when the request is done, and log that it is done.

## Holds

Work held back, one line each: what is held, why, and what releases it, such as a limit or an operator's answer.
