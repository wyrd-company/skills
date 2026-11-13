# Documentation

Read this when writing or reviewing a design document: a vision, a concept, a specification, a technical design, a decision record, or another of the types in [designing](../../designing/references/documents.md). The rules apply to the prose in each field. Which document holds what is in `designing`.

The first reader of a design document is an agent that meets it with no other context and builds from it. Write so that reader can build, and give it nothing to fight.

## State what is

- **Write as the only version.** The present tense, describing the system as it is. No "previously", "now", "no longer", "we changed", status banners or changelogs. A draft is a draft until it is published, and its history is in git.
- **Be definite.** "Is", "does", "provides", not "should", "may" or "aims to". Qualify only what genuinely varies in the design, never out of doubt about whether it is built yet.
- **Define the scope by what the thing is.** Describe it precisely enough that its edges are clear. Do not list what was dropped or rejected in the prose: naming an absence invites the reader to argue for it. "The interface is a native API", not "it is not a wire protocol". Fields meant for exclusions, such as a concept's `exclusions`, hold them.

## Give the builder what it needs

- **No hesitation.** Do not frame parts of the work as risky, hard or possibly infeasible in the prose: "careful", "avoid", "may not be possible". A real threat is a risk document. A hard problem goes in the technical design's `design-challenges`, with how the design meets it.
- **No smallness.** "Minimal first", "keep it small" and "don't over-engineer" are habits from teams with little capacity. Describe the full capability the design has.
- **Mechanism, not background.** Give the structure and how it works. Leave out the deliberation and the alternatives considered: a real trade-off has a decision record, and the document links to it.

## Keep the plan out

- **No sequencing:** no phases, milestones, roadmaps, "first" and "later", or carved-out first versions. Order belongs to planning and the board.
- **No acceptance checklists.** Success criteria and Definitions of Done live in the issue and the tasks. A specification's `validation-criteria` says how conformance is checked, not when the work is done.

## Render decisions; do not make them

When you write on someone's behalf, write the decisions they made. Do not add your own view of the product's positioning or direction, and do not frame the product around a comparison made in passing: a reference mentioned in a conversation is not a category the owner chose. When something is undecided, raise it as a question.

## Be precise

- **Mechanism over adjective.** Not "fast prefix scans" but "paths sort lexicographically, so all descendants of a path are contiguous and scan as one range". The reader can build from a mechanism; an adjective is only a mood.
- **Checkable statements.** "Every successful change creates a commit" can be verified. Cut "high-performance", "seamless" and "robust" unless a mechanism or a number follows.
- **Examples hold.** Every example of an API, a format or a command validates against the definition it illustrates. Check it with the definition's own validator before review.

## Hygiene

- **Code, schemas and commands in fenced blocks,** with a language tag. Never as prose.
- **No conversion debris:** escaped characters such as `\[` or `C\#`, smart quotes, doubled spaces. They show the text was never read.
- **A diagram shows structure** that words cannot, and fixes nothing the design has not fixed.
- **One version.** When a document replaces drafts, the drafts go.

## Example

Before:

> Refinery DB is a high-performance, reactive, hierarchical database. Its tree sorts entries so that descendants are guaranteed to sit together on disk. Refinery does **not** target Postgres or MongoDB wire compatibility.

After:

> Refinery DB is a reactive application backend with native query, mutation and subscription APIs. Materialized paths sort lexicographically, so all descendants of a path are contiguous and scan as one range rather than a recursive walk. Applications use Refinery through its own APIs and SDKs.

The adjectives became a mechanism, the guarantee has a reason, and the scope is stated by what it is.
