# standards

The rules our work is held to. The agent doing the work follows them, and the agent reviewing it checks them, so both read the same text instead of keeping their own copies. The skill is not a process: `executing` and `review` say how to do and check the work. A repository's own `AGENTS.md` and docs win over these standards for that repository.

| File | What it is for |
|---|---|
| [SKILL.md](SKILL.md) | Which standard covers the work, and what to do when one is missing |
| [references/documentation.md](references/documentation.md) | How design documents are worded |
| [references/instructions.md](references/instructions.md) | How skills, `AGENTS.md` files and briefs to delegates are written |
| [references/interface.md](references/interface.md) | How an interface a person uses is built: usability, accessibility, states, layout, colour, type, motion, copy, platforms and terminal tools |
| [references/stack.md](references/stack.md) | What websites and web applications are built with, and the template a site starts from |
| [references/workspace.md](references/workspace.md) | How the workspace environment is configured, and fitted to one workspace's needs |

## Sources

The standards are written in our own words. These works shaped them; nothing is copied from them. Each link is to the commit we read.

| Source | License | What we drew on |
|---|---|---|
| [dembrandt/dembrandt-skills](https://github.com/dembrandt/dembrandt-skills/tree/8f78f13f74a2356326d0c3c21bc63e5624e6a457/skills) | MIT | Interface: most of the concrete rules. Feedback and loading, states, overlays, forms and errors, status colours, information architecture and navigation, layout, density and alignment, tables, type scale, colour palettes and themes, elevation, responsive paradigms, accessibility thresholds and web performance. |
| [mattpocock/skills](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/productivity/writing-for-agents): `writing-for-agents` | MIT | Instructions: the description as the pointer that decides when material is read, one trigger per case, what every case needs in `SKILL.md` and the rest behind pointers, a topic kept together, criteria that are checkable and exhaustive, saying what to do rather than what not to, leaving to the environment what it says, and cutting sentences that change nothing. |
| [obra/superpowers](https://github.com/obra/superpowers/tree/22f0b463e7a5e579904dd6211a520321035526f7/skills): `writing-skills`, `subagent-driven-development` | MIT | Instructions: fitting the form of a rule to the failure, exceptions as their own conditions, no workflow in a description; and for briefs, one task with no history, files named rather than pasted, a fixed shape for what comes back, when to stop, and no delegating onward. |
| [anthropics/skills](https://github.com/anthropics/skills/tree/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/skill-creator): `skill-creator` | Apache-2.0 | Instructions: reasons rather than capitals, `SKILL.md` under 500 lines, and scripts for code agents keep rewriting. |
| [Anthropic's skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Published guide | Instructions: a default rather than a menu, and references one level deep. |
| [cursor/plugins](https://github.com/cursor/plugins/tree/3dbd22ff12742fb28c9700b9760baa29ed41dc13/pstack/skills/principle-encode-lessons-in-structure): `pstack`'s `principle-encode-lessons-in-structure` | MIT | Instructions: a correction given twice becomes a check. |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable/tree/a90602e9f6fed600d6d9b18cf78275d66cac7a6c/skill) | Apache-2.0 | Interface: the defaults of generated interfaces to avoid, familiarity on work surfaces, iOS and Android conventions, copy and localisation, hardening against extreme content, and checking the rendered result. |
| [emilkowalski/skills](https://github.com/emilkowalski/skills/tree/5206a950b715e0cabe7043ea0b2304332b91494e/skills/animate) | MIT | Interface: motion. Its purpose, duration and easing, no animation on frequent actions, and interruption. |
| [Leonxlnx/cook](https://github.com/Leonxlnx/cook/tree/b23cac6fd9439dfddcab61b14808e7bf72549b46) | MIT | Interface, proving it: shots at fixed framing rendered beside their references, a score for each dimension, critics who see only the shots and the rubric, and every number marked as measured or judged. |
| [benjitaylor/skills](https://github.com/benjitaylor/skills/tree/299140fafd08df55a9c234e610c3f64af3f45531/stageshow): `stageshow` | MIT | Interface, proving it: a handover that says what was not checked. |
| [google-labs-code/design.md](https://github.com/google-labs-code/design.md) | Apache-2.0 | Interface: the `DESIGN.md` linter as one of the checks. |

The documentation standard comes from our earlier `authoring-specifications` skill, the workspace standard from our own workspace repositories, and the stack from our own templates and choices. None has an outside source.
