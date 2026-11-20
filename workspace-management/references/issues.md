# Issues

Read this when the **Issue triage** or **Issue review** duty is due, or when the survey's **Issues** section lists high-priority issues to start.

The workspace's open issues are its list of wanted work, and the workspace project ranks them. The project is a GitHub project for this workspace, recorded in the manager task's **Channel** section as **Issues project**. Every open issue in the workspace's repositories is an item in it, with a **Priority** (`High`, `Medium` or `Low`) and a **Status**. The workspace's repositories are the ones [dependencies](dependencies.md#which-repositories) defines. People follow the work on GitHub, so the ranking lives there and not on a board.

## Priority

| Priority | When |
|---|---|
| `High` | A security problem, data loss or corruption, a defect that blocks work in this workspace or its users, or what an operator has asked for soon |
| `Medium` | A defect with a workaround, or an improvement an operator or a user asked for |
| `Low` | Everything else: polish, ideas, work nobody is waiting on |

An operator's priority stands: when an operator set an item's priority, or said on the issue how urgent it is, a review leaves it as they said.

## Triage

**Issue triage** adds the issues not yet in the project and ranks them. Dispatch it with `delegate_task`, on the cheapest model in [models.yml](~/models.yml) that lists `normal` complexity:

```text
Triage the open issues in these repositories that are not yet items of GitHub project <owner>/<number>: <repositories>. For each one, add it to the project, and set its Priority (High, Medium or Low) by this rule: <the Priority table from the workspace-management skill's issues reference>. Leave a priority an operator set. Set its Status to Todo when an executor could start it from the issue alone: its goal, its bar and, for a defect, how to reproduce it. Otherwise set it to Backlog, and comment on the issue once with the question that would make it ready, saying you are an agent. Close nothing. Return, for each issue: its priority, its status, and the question you asked when you asked one.
```

Set the duty's **Last done** when the report comes back, and log the issues it ranked `High`.

## Review

**Issue review** looks at the whole ranking again, because priorities go stale: a bug's workaround stops working, an operator's request is answered elsewhere, a `Backlog` question gets its answer. Dispatch it like triage, with this prompt:

```text
Review the open items of GitHub project <owner>/<number>. For each one whose Priority or Status no longer fits the rule below, change it, and say why in one line. Rule: <the Priority table>. Leave a priority an operator set. Move a Backlog item to Todo when its question was answered. List the issues that look finished, duplicated or no longer wanted, with the reason for each, but close none: closing is for an operator. Return the changes you made and that list.
```

Post the list of issues that look finished or unwanted in [the channel](../SKILL.md#the-channel), once, so an operator can close them. Set the duty's **Last done**.

## Start high-priority issues

The survey lists the project's items with Priority `High` and Status `Todo`. They are the third kind of [work](../SKILL.md#the-work), after operators' work and dependency updates.

1. **Check that nobody has started it:** no open pull request links it, and no task on a board names it in its `issue` field.
2. **Check the budget and the limits.**
3. **Write a task for it** on the board of the project its repository belongs to, with [task-authoring](../../task-authoring/SKILL.md): the task links the issue, which owns the goal. An issue too large for one task needs an epic: write a request for a planner in the **Requests** section instead, and notify the operator.
4. **Dispatch the task** as a [ready task](dispatch.md#tasks-ready-to-dispatch), and set the item's Status to `In Progress`, so the next sweep does not start it again.
5. **Log the dispatch** with the issue and the thread.

When `High` runs out and the budget is still below the pace, `Medium` items with Status `Todo` come next, oldest first.
