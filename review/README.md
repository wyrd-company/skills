# review

The skill an agent uses to judge work someone else delivered: a pull request, a task's result, a document, a design or instructions for agents. The reviewer decides whether the work meets its contract and shows the executor exactly where it does not, without fixing it.

How much review the work gets scales with its risk. Triage sets a level, `low`, `normal` or `high`, and `high` adds lenses: fresh reviewers that each read the work for one question. Findings carry a severity from P0 to P3, or Q for a question, and P0 and P1 block acceptance. A task can also ask for a council, where several models from different providers give the verdict. The reviewer merges only when the task authorizes it. Reviewing your own work before handing it over is in `executing`, and the rules work is held to are in `standards`.

| File | What it is for |
|---|---|
| [SKILL.md](SKILL.md) | Levels, the round from claim to handoff, findings and severity, results, merging |
| [references/triage.md](references/triage.md) | Setting the level from the work's risk |
| [references/code.md](references/code.md) | Reviewing code, tests, scripts, configuration and CI |
| [references/documents.md](references/documents.md) | Reviewing prose: documentation, designs, specifications and agent instructions |
| [references/lenses.md](references/lenses.md) | Running lenses at `high`, and their catalogue |
| [references/task-audit.md](references/task-audit.md) | Reading a task's log and transcript for what the operator should still scrutinize |
| [references/council.md](references/council.md) | Running a council |
| [references/surfaces.md](references/surfaces.md) | Checking, commenting on and deciding a GitHub pull request or a `gitpr` review |
| [references/epic.md](references/epic.md) | The reviewer's part in an epic |
| [assets/review-handoff.md](assets/review-handoff.md) | The template for the review handoff |

## Sources

The skill is written in our own words. These works shaped it; nothing is copied from them. Each link is to the commit we read.

| Source | License | What we drew on |
|---|---|---|
| [t3dotgg/tstack](https://github.com/t3dotgg/tstack/tree/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/council): `council` | MIT | Council: one strong model from each of three providers at high effort, reporting a missing member instead of substituting, read-only members, scores in a table in the pull request description with `no score` never invented, and holding repeated rounds to the scope. |
| [google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model/tree/e9e1f06aa4e26e95cd4ed37210a0632202c429e9/agents) | Apache-2.0 | Lenses: a fresh, read-only reviewer that knows nothing of the work's history, and the questions behind the Comprehension, Design critic, Readiness, Zoom out, False compromise and Fit lenses. |
| [cursor/plugins](https://github.com/cursor/plugins/tree/3dbd22ff12742fb28c9700b9760baa29ed41dc13/pstack/skills/blast-radius): `pstack`'s `blast-radius` | MIT | The Blast radius lens, and proving at `high` the one fact a change's safety rests on by running it. |
| [sanyuan0704/sanyuan-skills](https://github.com/sanyuan0704/sanyuan-skills/tree/08b6572ef108f22d4e8a3ecf9182a4bbef097744/skills/code-review-expert): `code-review-expert` | MIT | Through our earlier `code-review` skill, which carried its checklists: the P0 to P3 severity scale, and what to look for in code (correctness, failure, security, removal). |
| [Leonxlnx/cook](https://github.com/Leonxlnx/cook/tree/b23cac6fd9439dfddcab61b14808e7bf72549b46) | MIT | The Visual lens: critics who see only the shots, their references and the rubric, at least one from another provider, with the median score taken per dimension. |

The rest is our own. Our earlier `code-review` and `user-acceptance-testing` skills supplied the round, results such as "change approved, rebase expected", merge authority, the review surfaces and the reviewer's part in an epic. The draft of this skill supplied the task audit, and scaling review to risk with triage's signals.

Formats and tools the skill uses, rather than drew on:

| Source | License | Use |
|---|---|---|
| [google-labs-code/design.md](https://github.com/google-labs-code/design.md) | Apache-2.0 | The `@google/design.md` linter, which a reviewed `DESIGN.md` must pass. |
