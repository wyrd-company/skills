# Repository Standards

These are our current repository standards. Linked files provides detailed standards:

- [AGENTS.md](agents_dot_md.md) in the root.
- [README.md](readme_dot_md.md) in the root.
- `CODE_OF_CONDUCT.md`: The org/account's `.github` repo must contain the standard code of conduct requirements.
- [CONTRIBUTING.md](contributing_dot_md.md): The `.github` repo must contain the account/org's standard contribution guidelines. CONTRIBUTING.md is created for repos only when they need to deviate from the standard guidelines.
- [LICENSE](license.md) in the root.
- `Taskfile.yml`: We use [Task](../../skills/taskfile-automation/SKILL.md) as our automation tool.
- `.intentional/config.yml`: We use [Intentional](../../skills/intentional/SKILL.md) for versioning/changeset management. Do not hand edit CHANGESET.md files unless onboarding a repository with version history to intentional.
- `.config/lefthook.yml`: We use [Lefthook](../../skills/lefthook/SKILL.md) to create and manage git hooks. 
- `.gitignore`: Always make sure we have a proper git ignore file
- `.gitattributes`:
- `.editorconfig`
- `.github/workflows/ci.yml`
- Release workflows come from the toha template in the `.github` repo and should be applied/updated from those.
- Linter/formatter configs.
- `.devcontainer/devcontainer.json`. Even though we use our workspace devcontainers, we must provide a standard container for either us to use with a single repo or for external contributors.
- [`renovate.json`](renovate.json): A simple renovate config that points to a central config in `.github`.
- `scripts/`: Local Python scripts.
- `LICENSES/`: Third-party licenses
- `docs/`: This is where our project documentation lives.
- `tests/`: The standard place for tests, unless a tech stack dictates otherwise.
- `DESIGN.md`:
- `CHANGELOG.md`: Do not edit
- `.config/.ryl.toml`

## Forks

Forked repos serve generally have 1 of 2 intents:

- A repo forked to submit upstream PRs.
- A repo forked to intentionally diverge from upstream.

When operating in a forked repo for submission to upstream PRs we _ALWAYS_ conform to the explicit and implicit standards of the repo. Where a CONTRIBUTING.md or other documentation exists we follow the standards/expectations described. Where there is no explicit instruction, we implicitly follow the standards by observing code, issue descriptions, pr descriptions, documentation, organization, etc to follow the implied standards. Any PR being raised will ensure it follows those standards, and will list the implied standards it followed and how it determined them.

All other forks are must be made to conform to these standards. Any existing documentation or implementation in the fork that contradicts our standards must be adapted either immediately when it is low cost/risk, or raised as issues to address.

## Scope

This standard only applies to our published git repositories. Non-git repositories or repositories intentionally without are not in the scope of this document.