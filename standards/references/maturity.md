# Maturity

Read this when deciding how much ceremony a change needs: a decision record, a migration, hardening, the depth of its tests and its review. The answer depends on the repository's stage, because ceremony buys safety for whoever depends on the work, and costs speed when nobody does yet.

## The stage

The test is: who breaks if we change our mind? While the answer is nobody, a change is an edit. Once products or people depend on the thing, the same change becomes an event with a record.

The version gives the stage by default, read from the repository's latest release tag, or from its `intentional` version when it has no tag:

| Stage | Version | What it is building toward |
|---|---|---|
| Early | before `0.1.0` | Something working in people's hands for real use |
| Pre-stable | `0.1.0` up to `1.0.0` | `1.0.0`: high confidence, built up a release at a time |

The repository's `AGENTS.md` overrides the version when it names a stage. The answer to the test overrides both:

- **A dependent moves the work later.** When you find something that depends on what the change touches, such as another repository, a deployed service or a person using a release, hold that part of the change to the pre-stable rules, whatever the version says.
- **Only the operator moves the work earlier.** You cannot see every dependent, so treat a released repository as early only when its `AGENTS.md` or the operator says nothing depends on it.

## Early: before 0.1.0

- **Designs are living documents.** A settled decision can be questioned and changed. Changing it is an edit to the document it shapes: no decision record, no superseding design, no migration narrative. Write a decision record only when the operator asks for one.
- **Build no migrations, and do not ask about them.** Nothing has been released, so there is nothing to migrate from. The exception is a product whose migration or upgrade is itself a feature: build that feature as its design says.
- **Leave hardening for later, and leave room for it.** Security is relaxed by default, but a design must not block adding it later: keep authentication, authorization and secrets at a seam that can be tightened without a rewrite.
- **Test the golden path, then the likely failures.** The aim is software people can use, not perfect software. Prove the main path end to end, and cover the failures a user is likely to meet.

### Always hardened

Some work is hardened at every stage, because a breach costs someone outside the project from the first day:

- a public service that holds user credentials or third-party service secrets;
- handling money;
- storing sensitive personal information.

Work that touches any of these is hardened and tested for its failure and abuse cases from the start, and its review is `high`.

## Pre-stable: 0.1.0 up to 1.0.0

- **Decision records are routine.** Write one for each real trade-off, as [designing](../../designing/references/documents.md#decisions-land-where-they-shape-the-work) describes. Reversing a decision that something depends on is an event: a decision record that supersedes the old one, and the design rewritten to match.
- **Decide migration explicitly.** SemVer makes no compatibility promise below `1.0.0`, so migration is not built by default. When a change would break compatibility with an earlier release, ask the operator whether to support migrating from it, and record the answer either way.
- **Raise the bar with each minor release.** Every release that is not a patch considers more hardening and more thorough tests. When planning a new minor release, raise with the operator how far to expand the security and testing posture, and record what was decided.
