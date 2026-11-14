# Documents

Read this to choose the document a decision belongs in, and where it goes. How a document is worded is in [standards](../../standards/references/documentation.md).

## The format

Design documents are YAML, in the formats of the Refinery ontology. Each opens with its type, and the file name is its slug:

```yaml
$schema: https://refinery.systems/ontology/technical-design
relationships:
  assumes:
    - docker-engine-is-the-only-runtime
  mitigates:
    - agent-compromise-exposes-host-container-secrets
objective: >-
  ...
```

Other documents refer to it by that slug, under `relationships`, with the relationship's name as the key. When the repository already has a document of the same type, follow its shape.

One design document is not YAML: a product's visual language is `DESIGN.md`, in its own format. [Interface](interface.md#the-visual-language) covers it.

## Where it goes

- **A component's documents** go in its repository, under `docs/<folder>/<slug>.yml`.
- **A product made of several components** has a product repository. Documents that span its components go there: jobs, personas, concepts, and terms shared across components.
- **The repository's own layout,** and its `AGENTS.md`, win when they say otherwise.

## Which document

| What it holds | Type | Folder | Its main fields |
|---|---|---|---|
| An idea worth keeping, before it is shaped | `idea` | `ideas/` | `statements`: up to five, keyed `A` to `E` |
| A shaped idea: what it is and what it does | `concept` | `concepts/` | `description`; `properties` as noun phrases and `features` as verb phrases, keyed by slug; `open-questions` keyed `Q01`, `Q02`; `exclusions` |
| What users are trying to get done | `job-to-be-done` | `jobs/`, in the product repository | `description`, the job statement; the job map; `outcomes`, ranked |
| Who the users are | `persona` | `personas/`, in the product repository | `description`, `goals`, `frustrations` |
| The domain: its commands, its events, and where consistency is enforced | `domain-model` | `domain-models/` | `description`, `aggregates` |
| A contract that implementations conform to: an API, a format, a command line | `specification` | `specifications/` | `description`, `format`, `validation-criteria`; the definition itself is an asset in its native format, such as OpenAPI or JSON Schema |
| How it will be built | `technical-design` | `technical-designs/` | `objective`, `background`, `design-challenges`, `proposed-design` |
| What a user can do, as scenarios | `feature` | `features/` | `world-schema`, `background`, `rules`, `scenarios` |
| What a module's public contract guarantees, as scenarios | `behavior` | `behaviors/` | `world-schema`, `background`, `scenarios` |
| A question answered by experiment | `spike` | `spikes/` | `objective`, `background`, `ideas`, `environment`, `findings`, `conclusion`, `next-steps` |
| A real trade-off, and why it went the way it did | `decision-record` | `decisions/` | `description`, `considered-options`, `decision-outcome` with `chosen-option` and `justification`, `expected-outcomes` with `positive` and `negative` |
| Something believed but not proven | `assumption` | `assumptions/` | `description`, `evidence`, and `end-descendant-type`: the type of document that will replace it once proven |
| A threat to the outcome | `risk` | `risks/` | `slug`, `title`, `description`, `categories`, `likelihood` and `impact` from 1 to 5, the response, `status` |
| A word with one meaning here | `term` | `terms/` | `title`, `description` |
| A product's visual language and its tokens | `DESIGN.md` | The repository root | Tokens in the front matter; sections in the order the [format](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md) sets |

## Decisions land where they shape the work

Most decisions are not decision records. A choice of storage is part of the technical design; the shape of a response is part of the specification; what an order is belongs in the domain model and its terms. Write each decision into the document it shapes, as a statement of what the thing is.

Write a decision record only for a real trade-off: options that were each viable, where choosing one gave something up, and where a later reader would otherwise reopen the choice. The record names the options, the one chosen and why, and what it costs. The documents it shapes link to it.

## Converging drafts

When several drafts of one document exist, they become one.

1. **Treat the drafts as peers.** The newest is not automatically right: reconcile them section by section.
2. **List where they diverge.** Where one simply has more, fold it in. Where they point in opposite directions, that is a fork.
3. **Take forks to the owner.** Present each with the options and a recommended reconciliation. Do not settle a fork by preference.
4. **Check what you carried over.** A sentence kept from a draft is a claim the converged document now makes. Check each promise it keeps, such as compatibility, ordering or support for older inputs, against the scope that was decided. Cut what the scope does not build, or raise it with the owner.
5. **Retire the drafts.** The converged document is the only one, and shows no trace of the drafts.
