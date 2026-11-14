# Skills

Each top-level folder is a skill. Skills are written to the [instructions standard](standards/references/instructions.md), which says how a skill is laid out and worded, and reviewed by the [checks for instructions](review/references/documents.md#instructions-for-agents).

## Design documents

The documents skills ask agents to write follow the formats and schemas of the Refinery ontology, in `wyrd-company/refinery-ontology`. The skills themselves are Markdown in our own words: we adapt the ontology, and do not adopt Refinery as a whole.

## Sources

Skills are written in our own words. Third-party skills shape them, but are never copied into this repository: keep upstream copies with your references, outside it.

- **Every skill has a `README.md`.** It holds a description for humans, a table of the skill's files, and a **Sources** table. Follow an existing one, such as [designing](designing/README.md).
- **Each source is linked at the commit you read,** with its license and what the skill drew on. Formats and tools the skill uses, rather than drew on, go in a table of their own.
- **Credit the original.** Before crediting a skill, check whether it is a port, a fork or a copy of another, and link the upstream. For example, `pstack-portable` is a port of `pstack` in [cursor/plugins](https://github.com/cursor/plugins/tree/main/pstack).
- **Record a source when you read it,** not after. When a delegate researches for you, ask it to tag each idea with its source.
- **Credit what the text shows.** A source you read that left no trace in the skill is not listed.

## Committing

Worktrees here often hold drafts and upstream copies. Stage only the paths you mean to commit, by name, never with `git add -A` or `git commit -a`, and check `git show --stat` before you push.
