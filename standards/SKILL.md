---
name: standards
description: >
  Use when doing or reviewing work that one of our standards covers, to know the rules it is held to. Covers how design documents, documentation for users and developers, and instructions for agents are written, how interfaces are built, what they are built with, what every repository holds, and how the workspace environment is configured, including on forks of the workspace repositories. Not for how to do or check the work (`executing`, `review`).
---

A standard is a rule the work is held to. The executor follows it and the reviewer checks it, so both read the same text here instead of each keeping their own copy.

Read the standard for the work at hand:

- [Documentation](references/documentation.md): how design documents are written: vision, specifications, technical designs, decision records and the other design documents.
- [User documentation](references/user-documentation.md): documentation for users of a product and developers who build on it: audiences, tutorials, how-to guides, reference and explanation, generated reference, published links and interface captures.
- [Instructions for agents](references/instructions.md): how skills, `AGENTS.md` files and briefs to delegates are written, and which home each kind of instruction belongs in.
- [Interface](references/interface.md): how an interface a person uses is built: usability, accessibility, states, layout, colour, type, motion, copy, and terminal output.
- [Stack](references/stack.md): what a website or a web application is built with, and the template it starts from.
- [Repository](references/repository.md): what every repository holds, and the templates it starts from: its README, `AGENTS.md`, `CONTRIBUTING.md`, license, automation with Task and Lefthook, configuration and layout, and how a fork is treated.
- [Workspace](references/workspace.md): making project and repo folders and their T3 Code projects, fitting one workspace to its needs, keeping a workspace that runs on forks in step with upstream, where configuration shared by every workspace belongs, how it is applied, and how a change to it is made to last.

When instructions conflict, apply them in this order: the repository's own `AGENTS.md` and docs, then its project's skill overlays, then the workspace's skill overlays, then the base skill or standard. Apply each overlay rule within the workspace or project it names.

## Gaps

These standards are incomplete. When the work needs a rule that is missing here, follow the repository's existing practice, say so in your handoff, and record the gap as an observation in memory.
