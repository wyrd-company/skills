# task-authoring

The skill an agent uses to write a task: the ticket for one executor to do one piece of work. A task says what will be delivered, how completion is judged, and where the knowledge is. The goal stays on the GitHub issue, or in the operator's prompt, and how to do the work stays with the executor.

The skill sets the boundary between an issue, a task and a pull request, and when work needs none of them. It covers searching the board before writing, the contract a task holds and where the author stops, sizing, hard and soft claims in a Definition of Done, pointing the executor and reviewer at context, and what each metadata field is for. Claiming and working a task is in `task-ownership`; planning an epic's tasks is in `epic-planning`.

| File | What it is for |
|---|---|
| [SKILL.md](SKILL.md) | The issue, task and pull request boundary, the contract, size, Definition of Done, context and metadata |
| [assets/template.md](assets/template.md) | The template a task is written from |

## Sources

The skill is our own. It distils our earlier `task-authoring` skill, which grew from May to October 2026 in our previous skills repository: the six questions of the contract, the template's sections, searching the board before authoring, and stating counts as a change from the base. No third-party skill shaped it.

Formats and tools the skill uses, rather than drew on:

| Source | License | Use |
|---|---|---|
| [antopolskiy/kanban-md](https://github.com/antopolskiy/kanban-md) | MIT | The board tasks live on, and its metadata fields. |
