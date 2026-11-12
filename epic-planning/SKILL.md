---
name: epic-planning
description: Use when work needs more than one task. Covers choosing how an epic will be run, setting it up as tasks, issues and a GitHub project, and handing it over for dispatch. Not for ordering the units of a single task; `executing` covers that.
---

An epic is work that needs more than one task. As the planner you do not do the work. You choose the pattern or patterns the epic will run on, set up the conditions for it and for the agent that orchestrates it, and hand it over.

## The goal comes first

The operator sets the goal, through the issues, the prompt or the skills. How the epic reaches it is yours to decide. When the goal is clear, plan and proceed: the plan does not need approval unless the issue or the operator asked to review it.

- The goal is defined by selected GitHub issues, or by a clearly defined goal in the prompt. Issues when we know what needs to be built; the prompt when the epic is finding that out.
- A bar is set for the epic as a whole, for each issue, or both. Refuse an epic without a bar: tell the operator what is missing.
- When a goal is a user-facing need, the issue states the problem apart from any solution, the invariants every solution must keep, the requirements and observable success criteria, and one end-to-end acceptance scenario from the user's point of view. If any of these is missing, the goal is not clear yet: return it to design with the operator instead of inferring it from the request.
- When the goal is clear but the way to it is not, the epic is not ready to plan. Chart the way first: that is design work (see `designing`), and its output is the decisions planning starts from.

Read the issues or the prompt, the documentation for the patterns you are considering, and related observations in memory before you choose.

## The patterns

Use one or more of these to shape the epic. Each reference says when to choose the pattern and how to set it up. Running it is the orchestrator's job. New patterns are added here once proven, by us or by others.

- [Arena](references/arena.md): several workers independently produce competing solutions to the same brief. A judge, council, benchmark or tournament compares them, often blind, and picks a winner or grafts the best of the others onto it.
- [Chain](references/chain.md): one link at a time, each link's output the input of the next, with a check at every boundary. For work whose size is not known up front.
- [Map-Reduce](references/map-reduce.md): independent chunks worked in parallel by uniform workers, then reconciled into one deliverable by reducers.
- [Project](references/project.md): a dependency graph of tasks with their own sub-goals, worked in order and in parallel where the graph allows, with the orchestrator supervising the assembly. A traditional project.
- [Swarm](references/swarm.md): autonomous, specialised workers coordinate among themselves through handoffs, messages or shared state, without top-down control. The orchestrator decides when the swarm has finished.

## What you deliver

- **The epic's board.** Each epic has a board of its own, so its tasks do not contend with other work for the board's task ids, and the whole epic can be committed and archived as one folder. Create it under `epics/` in the tasks folder for the epic's scope. Answer no when `init` offers to ignore it: the board is committed.

  ```bash
  echo n | kanban-md init --dir "$TASKS/epics/<name>" --name "<name>"
  ```

- **The epic task.** The epic is a `kanban-md` task on the epic's board. Its children are the tasks that do the work, written with [task-authoring](../task-authoring/SKILL.md) and staged in `backlog` for the orchestrator to release. Tasks and issues need not match one to one: several tasks may serve one issue, and one task may close several.
- **Every child maps to the goal.** Each child serves a requirement, a success criterion, a step of the acceptance scenario, or coordination the epic needs. Reconcile any child that maps to nothing, and any criterion that no child covers, before you hand over.
- **The issues, ready.** Each issue states its goal and its bar.
- **The GitHub project.** People follow an epic on GitHub, not on the board. For an epic with one issue, that issue is what they follow. For several issues, use an existing GitHub project or create one for the epic. The orchestrator keeps it current.
- **The acceptance plan.** When the issues call for [user-acceptance testing](../executing/references/user-acceptance-testing.md), decide where it happens before the epic starts: at the earliest points where a user can accept part of the work, such as a prototype or the first end-to-end slice, as a goal of that task or a task of its own; otherwise as the review stage of the epic task. The final acceptance covers the combined result, not only its parts.

In an epic of any size, the merge from the epic branch into the default branch is too large to review line by line. Quality rests on the review of each child into the epic branch. The final merge checks the combined result: the full checks on the merged state, acceptance, and that nothing reached the epic branch unreviewed. Plan for that: every child gets its own review, and the acceptance plan covers the whole.

Hand the epic to the workspace manager, which dispatches it.
