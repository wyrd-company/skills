# standards

The rules our work is held to. The agent doing the work follows them, and the agent reviewing it checks them, so both read the same text instead of keeping their own copies. The skill is not a process: `executing` and `review` say how to do and check the work. A repository's own `AGENTS.md` and docs win over these standards for that repository.

| File | What it is for |
|---|---|
| [SKILL.md](SKILL.md) | Which standard covers the work, and what to do when one is missing |
| [references/documentation.md](references/documentation.md) | How design documents are worded |
| [references/interface.md](references/interface.md) | How an interface a person uses is built: usability, accessibility, states, layout, colour, type, motion, copy, platforms and terminal tools |
| [references/stack.md](references/stack.md) | What websites and web applications are built with, and the template a site starts from |
| [references/workspace.md](references/workspace.md) | How the workspace environment is configured, and fitted to one workspace's needs |

## Sources

The standards are written in our own words. These works shaped them; nothing is copied from them. Each link is to the commit we read.

| Source | License | What we drew on |
|---|---|---|
| [dembrandt/dembrandt-skills](https://github.com/dembrandt/dembrandt-skills/tree/8f78f13f74a2356326d0c3c21bc63e5624e6a457/skills) | MIT | Interface: most of the concrete rules. Feedback and loading, states, overlays, forms and errors, status colours, information architecture and navigation, layout, density and alignment, tables, type scale, colour palettes and themes, elevation, responsive paradigms, accessibility thresholds and web performance. |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable/tree/a90602e9f6fed600d6d9b18cf78275d66cac7a6c/skill) | Apache-2.0 | Interface: the defaults of generated interfaces to avoid, familiarity on work surfaces, iOS and Android conventions, copy and localisation, hardening against extreme content, and checking the rendered result. |
| [emilkowalski/skills](https://github.com/emilkowalski/skills/tree/5206a950b715e0cabe7043ea0b2304332b91494e/skills/animate) | MIT | Interface: motion. Its purpose, duration and easing, no animation on frequent actions, and interruption. |
| [Leonxlnx/cook](https://github.com/Leonxlnx/cook/tree/b23cac6fd9439dfddcab61b14808e7bf72549b46) | MIT | Interface, proving it: shots at fixed framing rendered beside their references, a score for each dimension, critics who see only the shots and the rubric, and every number marked as measured or judged. |
| [benjitaylor/skills](https://github.com/benjitaylor/skills/tree/299140fafd08df55a9c234e610c3f64af3f45531/stageshow): `stageshow` | MIT | Interface, proving it: a handover that says what was not checked. |
| [google-labs-code/design.md](https://github.com/google-labs-code/design.md) | Apache-2.0 | Interface: the `DESIGN.md` linter as one of the checks. |

The documentation standard comes from our earlier `authoring-specifications` skill, the workspace standard from our own workspace repositories, and the stack from our own templates and choices. None has an outside source.
