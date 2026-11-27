# designing

The skill an agent uses to decide what to build, and how, before anything is built. It frames the outcome with the operator, charts the decisions between that goal and a plan, and records each decision in the repository's design documents, so that planning and building start from settled ground.

It covers technical design (modules, interfaces, data and state), product design (jobs, personas, and trade-offs between scope and experience), and interface design (what a person sees and operates, and its visual language in `DESIGN.md`). It hands over to `review`, then to `epic-planning` or a single task. How a document is worded, and the rules a built interface is held to, are in `standards`.

| File | What it is for |
|---|---|
| [SKILL.md](SKILL.md) | The steps: frame, chart, write, hand over |
| [references/framing.md](references/framing.md) | Framing an outcome with the operator |
| [references/charting.md](references/charting.md) | Resolving the decisions, and decision tasks for large designs |
| [references/documents.md](references/documents.md) | Which document a decision belongs in, where it goes, and how specification metadata and raw definitions sit together |
| [references/technical.md](references/technical.md) | Designs that shape code |
| [references/product.md](references/product.md) | Designs that shape what users get |
| [references/interface.md](references/interface.md) | Designs that shape an interface, alternatives for a judge to choose from, and `DESIGN.md` |
| [references/excalidash-mood-boards.md](references/excalidash-mood-boards.md) | Create mood boards and collect operator diagrams with the ExcaliDash REST API |
| [scripts/excalidash-board.py](scripts/excalidash-board.py) | List, read, publish, and add images using a key from OpenBao |

## Sources

The skill is written in our own words. These works shaped it; nothing is copied from them. Each link is to the commit we read.

| Source | License | What we drew on |
|---|---|---|
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable/tree/a90602e9f6fed600d6d9b18cf78275d66cac7a6c/skill) | Apache-2.0 | Interface: naming what success is on each surface, refining an incumbent look versus replacing it, the operator's brief over the designer's taste, and `DESIGN.md` as the record of a visual language. |
| [cursor/plugins](https://github.com/cursor/plugins/tree/3dbd22ff12742fb28c9700b9760baa29ed41dc13/pstack/skills): `pstack`'s `architect`, `principle-foundational-thinking`, `principle-model-the-domain`, `principle-redesign-from-first-principles`, `principle-experience-first` | MIT | Technical and product: usage before signatures, the data's shape before the logic, the domain in structure, redesigning rather than bolting on, and experience first. |
| [Leonxlnx/cook](https://github.com/Leonxlnx/cook/tree/b23cac6fd9439dfddcab61b14808e7bf72549b46) | MIT | Interface: references as the floor the work must reach, not inspiration, with what to take from each. |
| [benjitaylor/skills](https://github.com/benjitaylor/skills/tree/299140fafd08df55a9c234e610c3f64af3f45531/stageshow): `stageshow` | MIT | Interface: the best existing examples as the bar, held beside the work. |
| `wyrd-company/astro-template`: `design-prototyping` | Ours | Interface: alternatives of style and copy, each at its own address with a switcher, for a judge to choose from. |
| [mattpocock/skills](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering): `codebase-design`, `improve-codebase-architecture`, `wayfinder` | MIT | Technical: deep modules and designing it twice. Charting: a design tracked as a map of decision tasks. |
| [wyrd-company/deck](https://github.com/wyrd-company/deck/tree/2ed4796f22c8bac154239b0e5134ab3b5d75d002/docs): `specifications/assets/grpc-api/deck/v1/deck.proto`, `check.sh` | Apache-2.0 | Specification definitions: preserving the proto package's native tree and filenames under a slug-named module root, verified with the pinned buf build and lint checks. |

Formats and tools the skill uses, rather than drew on:

| Source | License | Use |
|---|---|---|
| [google-labs-code/design.md](https://github.com/google-labs-code/design.md) | Apache-2.0 | The `DESIGN.md` format, and the `@google/design.md` linter and exporter. |
| `wyrd-company/refinery-ontology` | Ours | The schemas of the design documents. |
| [ExcaliDash](https://github.com/ZimengXiong/ExcaliDash/tree/c1013c0de630b3efeea6a11851adc039c2d2afe3) | LGPL-3.0 | Drawing REST endpoints and editor for mood boards and design diagrams. |
