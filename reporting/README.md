# reporting

The skill an agent uses when someone asks it to explain something, or for a report, brief, summary or deck. It starts from the reader and their question, chooses the smallest form that answers it, checks every claim and figure against its source, and delivers the result in the thread, through Postplan, on a page served from the workspace, through Discord or through the public assets bucket.

Everyday replies are covered by the core instructions in `workspace-dotfiles`; this skill takes over when the request is for an explanation, report, brief or deck. A pull request's handoff is in `executing`. Both use `public-assets` for media at a public URL. Charts are in `dataviz` when it is installed.

| File | What it is for |
|---|---|
| [SKILL.md](SKILL.md) | The reader and question, shape, checking, and the choice of case and delivery channel |
| [references/text-figures.md](references/text-figures.md) | Pseudocode, trees, shape diffs and Mermaid in a reply |
| [references/walkthroughs.md](references/walkthroughs.md) | Explaining code along one path |
| [references/changes.md](references/changes.md) | Explaining a change that exists, and proposing one |
| [references/briefs.md](references/briefs.md) | Briefs for a reader outside the work, and evidence roles |
| [references/diagrams.md](references/diagrams.md) | Diagrams that stand on their own |
| [references/interactive.md](references/interactive.md) | When a page should be interactive, and building it |
| [references/decks.md](references/decks.md) | Deck sources and the build script |
| [references/postplan.md](references/postplan.md) | Publishing to and reading from Postplan |
| [references/workspace-site.md](references/workspace-site.md) | Serving a page through the workspace's Caddy |
| [scripts/build-deck.py](scripts/build-deck.py) | Builds a reveal.js deck from a source fragment and uploads it to Postplan |
| [assets/deck/VERSIONS.md](assets/deck/VERSIONS.md) | The vendored reveal.js and highlight.js files, and their versions |

## Sources

The skill is written in our own words. These works shaped it; nothing is copied from them. Each link is to the commit we read.

| Source | License | What we drew on |
|---|---|---|
| [humanlayer/humanlayer](https://github.com/humanlayer/humanlayer/tree/2f5b58d3dfd18b13f4456b67ab0787df44233231/apps/riptide-humanlayer-claude-plugin/skills/show-me): `show-me` | Apache-2.0 | The smallest view that answers the question; pseudocode, call trees, component and file trees, and diffs of each shape; HTML only when it is too dense for Mermaid. |
| [analyticalmonk/explain-this](https://github.com/analyticalmonk/explain-this/tree/f64dab456ca23a351fe4d932c4e73bc91d3f2c52/skills): `creating-explainers`, `explaining-codebases`, `fact-checking-explainers` | MIT | Supporting, correcting or cutting each claim; code as the source of truth; an outline before an interactive page; figures that pay off the text; interactive figure kinds. |
| [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/tree/3027f20f3181758385a1bb8c022d4041dfb4de84/commands): `explain-pr-changes`, `explain-changes-mental-model` | MIT | Grouping a change by purpose, naming public-interface changes, and diagrams only where an interaction or state changes. |
| [mattpocock/skills](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/improve-codebase-architecture): `improve-codebase-architecture` | MIT | A proposed change's files, problem, change, benefit, before-and-after figure and recommendation strength; recorded decisions reopened only for real friction. |
| [tt-a1i/archify](https://github.com/tt-a1i/archify/tree/8509a3d63e763b4d454ea9aafa1f939545fcb1ea/archify) | Apache-2.0 | Diagram relationships grounded in repository evidence, and leading with the conclusion. |
| [luffy666code/diagram-design-skill](https://github.com/luffy666code/diagram-design-skill/tree/82562d5b9f0a0240def81a3b77a4c2bbe9549b54) | MIT | Choosing the diagram type by what the reader traces, one layout per figure, and offline fonts. |
| [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/797337f33f73e35d08d82f840e21c4b8c4932d88/skills/add-educational-comments): `add-educational-comments` | MIT | Depth set by what the reader already knows. |
| [blader/humanizer](https://github.com/blader/humanizer/tree/0ef9fe5bc3572734fd3ae6c448fe00a30cd5dcf0) | MIT | A final pass that cuts filler and inflated claims without changing meaning. |
| `postplan` npm package, version 0.0.6: `html-communication`, `postplan-read` | MIT | Postplan's publishing steps, its sandbox rules, the receipt, and reading a URL with `curl`. |
| Earlier operator skills: `brief-deck`, `postplan`, `architecture-delta-briefing` | Ours | The deck source rules and build script, and evidence roles in a brief. |

Formats and tools the skill uses, rather than drew on:

| Source | License | Use |
|---|---|---|
| [Postplan](https://postplan.dev) CLI, version 0.0.6 | MIT | Publishing and reading pages. |
| [reveal.js](https://revealjs.com) 5.1.0, [highlight.js](https://highlightjs.org) 11.11.1 | MIT, BSD-3-Clause | The deck runtime, vendored under `assets/deck`. |
| [Caddy](https://caddyserver.com) | Apache-2.0 | Serving pages from the workspace. |
