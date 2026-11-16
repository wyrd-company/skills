<!-- The front door for agents, read on every turn of every agent working here. Hold only what an agent cannot find by reading the repository. The rules are in the repository standard, under AGENTS.md. -->

# {Repository name}

{What it is, in two to four sentences.}

## Why this exists

<!-- The owner's decision: draft it for the owner's approval, or ask the owner. -->

- {A problem it solves, or an opportunity it creates.}

## Outcomes

<!-- The owner's decision: draft it for the owner's approval, or ask the owner. -->

- {An outcome it must deliver, or an invariant that changes only with the owner's approval.}

## Glossary

<!-- The domain's core terms. Each is defined in docs/terms/<slug>.yml, or in the product repository when it spans components. -->

- [{Term}]({path to its definition}): {its meaning, in one line}

## Orient

<!-- A tree of what is not standard, each entry with what it holds. Then how to run things, by the repository's tasks, and what an agent must not edit. -->

```tree
.
├── {folder}/   # {what it holds}
└── {file}      # {what it does}
```

- Checks: `task {name}`. [CONTRIBUTING.md](CONTRIBUTING.md) has the rest.
- {A path an agent must not edit, such as generated output or vendored code, and why.}

## Thar be Dragons

<!-- Only what a linter, hook or test cannot catch. Omit the section when there is nothing. -->

- {The trap, and what to do instead.}
