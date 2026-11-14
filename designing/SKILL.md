---
name: designing
description: >
  Use when deciding what to build or how to build it, before it is built. Covers the outcome's frame, the decisions between a goal and a plan, and the design documents that record them. Not for splitting the work into tasks (`epic-planning`), reviewing a design someone delivered (`review`), or how a document is worded (`standards`).
---

Design settles what to build and how while a change is still cheap: in a conversation or a document, not in code. What it produces is the decisions that planning and executing start from, written where they will still be found once the work is done: the repository's design documents.

You design with the operator, or as an agent on a task. The outcome is the operator's, so they confirm its frame. Charting the way and writing it down can be an agent's work, on a task whose `complexity` is usually `high`. A decision that belongs to someone else names them in the task's `hitl` with the `judge` role.

## The work

1. **Frame the outcome.** State the problem apart from any solution, the invariants every solution keeps, the requirements and the observable criteria that show each is met, and one end-to-end acceptance scenario from the user's point of view. The frame goes on the GitHub issue, where planning looks for it. Do not discuss solutions until the operator has confirmed it. [Framing](references/framing.md) covers the interview.
2. **Chart the way.** Name the destination: the documents that, once written, leave nothing to decide that blocks a plan. List the decisions between here and there, and resolve them. [Charting](references/charting.md) says how each kind of decision is resolved, and how a design too large for one session is tracked as decision tasks on a board.
3. **Write it down.** Each decision lands in the document it shapes: a specification, a technical design, a domain model, a term. [Documents](references/documents.md) says which type holds what, and where it goes. How a document is worded is in [standards](../standards/references/documentation.md).
4. **Hand it over.** A design is reviewed before anything is built on it, with [review](../review/SKILL.md), at the risk of what will be built on it. Then it goes to [epic-planning](../epic-planning/SKILL.md), or to a single task written with [task-authoring](../task-authoring/SKILL.md) when one task builds it.

Size the work, not the order. A small change may need only a frame the operator confirms in a sentence and a paragraph in the technical design it touches. Skip a step only when what it produces already exists.

## Throughout

- **Look before you ask.** Read the code, the repository's `docs/`, the issue and related memory first. Never ask the operator what the repository already answers, or reopen what they have decided.
- **Decisions about the goal are the operator's.** Scope, positioning, and a trade-off between what users get: present the options with your recommendation, and do not settle them by preference. Decisions about the way are yours, unless the task names a judge.
- **One source of truth.** Each decision lives in one document, and the others link to it. A design that contradicts a document already in the repository changes that document in the same work, or it is wrong.
- **Redesign, do not bolt on.** When a new requirement meets an existing design, ask what you would build had it been there from the start, and change every document that answer touches.
- **Label what is not proven.** An assumption written as fact becomes a requirement nobody chose. Record it as an assumption, with what would prove it.
- **Design is not planning.** Phases, sequencing and task lists belong to planning and the board, not to design documents.

## What to read

- [Framing](references/framing.md): to frame an outcome with the operator, before any solution.
- [Charting](references/charting.md): when the goal is framed and the way to it is not clear.
- [Documents](references/documents.md): to choose the document a decision belongs in, and where it goes.
- [Technical](references/technical.md): when the design shapes code: modules, interfaces, data structures and state.
- [Product](references/product.md): when the design shapes what users get: their jobs, who they are, and trade-offs between scope and experience.
- [Interface](references/interface.md): when the design shapes what a person sees and operates: screens, sites, native applications and terminal tools, and their visual language.
