# AGENTS.md

AGENTS.md files are primarily for agents. [README.md](readme_dot_md.md) are for humans.

## Root AGENT.md Contents

All repositories must have an AGENTS.md file at the root. The root AGENTS.md serves as the front-door for agents into the repo.

While the contents are specific to the context of the repository, they all should have the following general shape to conform to our standards:

- `## <Title>`
- Introduction/Description: A short 2-4 "elevator pitch" that describes the repo
- `## Why this exists`: A list of problems this repo solves, and/or opportunities it creates. This must come from the user, either via an interview you conduct, them directly editing, or you creating and them approving (pick the approach based on how much context you have).
- `## Outcomes`: What are the core outcomes expected or invariants that cannot be changed without approval. This must come from the user, either via an interview you conduct, them directly editing, or you creating and them approving (pick the approach based on how much context you have)
- `## Glossary`: A short glossary of core domain terms for the repo. They should be defined in `docs/terms/*.yml` files as well. This list is for agent consistency and are the terms that should _always_ be understood.
- `## Thar be Dragons`: What are common pitfalls an agent might experience working in the repo. We write stuff here _after_ we exhaust any automated way of preventing the failure. This section should be brief.
- `## Orient`: A high-level orientation as a tree for the _non-standard_ directories in the repo. It must also include links to the account/org's standard CONTRIBUTING.md, SUPPORT.md, ISSUE_TEMPLATE/*, and PULL_REQUEST_TEMPLATE files in the `.github` repo.

## AGENTS.md in other places.

An AGENTS.md may be created in other folders. They should be created to help when building initial understanding via file reads/`rg` to understand build content about the contents of the folder is expensive.

We are balancing the cost of ad-hoc discovery with forced discovery by an AGENTS.md file. A directory that is small and easy to understand will pay the cost of the AGENTS.md always being added to the context, however a complex folder, or one with information that should always be known to reduce failures, may want to pay that cost.

When they are created, they should be _extremely_ brief, with only the following:

- `## Orient`: A tree of what is in the folder, each entry containing a concise descriptions.
- `## Thar be Dragons`. Like above, only add these entries when automating failure prevention is impossible.

## Trees

Example:

```tree
.
├── folder/       # This folder isn't usual - or we need to know what it has in it if we are in this parent folder.
└── file.ext      # Even if we aren't reading this file, we should know it exists, what it does, why it is here.
```

In sub-repository root AGENTS.md, do not go past 1 level. The root may show several levels, but should be selective in what is added.