# Triage

Read this at the start of every review, before you read the change. It sets the level the review runs at: `low`, `normal` or `high`. What each level does is in the [skill](../SKILL.md#level).

The level answers one question: what does it cost if this work is wrong and the review misses it? Spend review where a miss is expensive. A `high` review of a typo wastes a day of tokens; a `low` review of a permission check ships a hole.

## Where the level comes from

- **The task's `risk`** is the floor. The author set it knowing what the work touches, and you never review below it.
- **Your triage** can raise it. Work it out from what the change touches, the files and the handoff, before the detailed read.
- **What you find** can raise it again during the review.

With no `risk` set and nothing below that applies, the level is `normal`.

## Signals

Read the change's file list, its diff stat, the handoff and the task's **Constraints**. Then take the highest level any signal gives.

### `high`: a miss is expensive or cannot be undone

- **It cannot be undone:** data migrations, deletions, releases, publishing, anything that sends messages or spends money.
- **Security:** authentication, authorization, secrets, crypto, input that crosses a trust boundary, sandboxing, the permissions of agents or tools.
- **Contracts others depend on:** public APIs, schemas, wire and file formats, CLI flags others script against.
- **Shared foundations:** CI and release pipelines, build tooling, infrastructure, devcontainer definitions, code most of the repository calls.
- **Instructions many agents follow:** skills, `AGENTS.md`, prompts and templates other work is generated from. One wrong rule repeats in everything that follows it.
- **Concurrency and state over time:** locks, retries, queues, caches, recovery after a crash or restart.
- **Evidence the executor could not get:** the handoff's **Not verified** list covers something a Definition of Done line depends on.

### `normal`: the usual case

- A feature or a fix within one area, with tests.
- A document people rely on, such as user documentation or a design that is not yet built.
- Anything the `low` list does not plainly cover.

### `low`: a miss is cheap and shows quickly

- Wording, typos and formatting in documentation, comments or messages.
- Tests only, when no production code changes.
- A mechanical change that a tool or the compiler checks: a rename, a dependency bump with no API change, regenerated output.
- Throwaway work: a spike, a script that runs once.

A `low` signal never lowers a `high` one. A typo fix inside a skill is still an instruction many agents follow; read the whole sentence it changes.

## Raising the level during review

Raise it, and say why in the handoff, when:

- you find a P0 or P1;
- the change touches something its task does not name;
- a piece of evidence in the handoff does not hold up when you check it;
- the change is larger than the task implies;
- you cannot work out why the change is safe.

Raising mid-round means doing the new level's extra work this round, not next round.

## Record it

Put the level and the signals that set it in the round's handoff: `Level: high (secrets handling; Not verified covers the rotation path)`. Triage improves only if its record can be read later.

When you find a risk this reference does not name, or a level that turned out wrong, either missing something or costing far more than the work deserved, record it as an observation in memory, tagged `review` and `triage`. Reviews of those observations decide what changes here.
