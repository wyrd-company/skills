---
name: environment
description: >
  Use when understanding, configuring or troubleshooting the shared devcontainer
  workspace environment: where configuration belongs, how it is applied, or how
  to make an environment change persist. Not for application-specific configuration
  inside a product repository.
---

A workspace is a devcontainer dedicated to a product or theme. Agents and direct
SSH/VS Code sessions use the shared `vscode` execution account. Its home-directory
settings are part of the standardized workspace environment. Human operator
identity is selected for Git commits and pushes; it does not select a separate
OS account or configuration profile.

Use the current workspace's `AGENTS.md` for its paths and constraints. For change
work, use [executing](../executing/SKILL.md); this skill supplies the environment
decisions, not a separate delivery process.

## Choose the configuration owner

`workspace-ansible` and `workspace-dotfiles` cooperate to standardize the same
workspace. Their boundary follows configuration ownership:

- Root-owned configuration belongs in `workspace-ansible`.
- Configuration owned by `vscode` belongs in `workspace-dotfiles`.
- Prefer common settings in `/etc/**` when the application supports them. When
  the application requires a user-level file, manage it through dotfiles.

Choose the layer from the application's actual support for the required setting.
A managed configuration layer may reject fields or disable extensions that a
user-level configuration supports. Check those semantics before choosing it.
Common-to-everyone settings can belong in dotfiles: a home-directory setting is
configuration for the execution account, not evidence of a human preference.

## Find the source of the running environment

Inspect the effective configuration, then locate its owning source before editing.
Rendered files show what is running; durable changes belong in the source repo.

| Source | Responsibility |
| --- | --- |
| `devcontainers` | Base images and reusable features: installed system tools and container capabilities. |
| `workspace-template` | Workspace definition, mounts, persistent-state layout, options and workspace-wide `AGENTS.md`. |
| `workspace-ansible` | Root configuration and system helpers, rendered from workspace options. It also orchestrates the dotfiles apply. |
| `workspace-dotfiles` | The shared execution account's configuration and user-installed tools, managed with chezmoi. |

Read the relevant repo's instructions and maintained docs rather than treating
this map as its implementation manual:

- For workspace definitions, paths and provisioning, read
  [Workspaces](https://github.com/wyrd-company/workspace-template/blob/main/docs/workspaces.md)
  and the relevant part of
  [Devcontainers](https://github.com/wyrd-company/workspace-template/blob/main/docs/devcontainers.md).
- For root rendering and apply order, inspect `workspace-ansible/container.yml`
  and its templates. Workspace options are exposed at `/etc/workspace/config.yml`.
- For account configuration and tool installation, inspect the dotfiles templates,
  package manifests and apply scripts. For secret access, read
  [Vault](https://github.com/wyrd-company/workspace-dotfiles/blob/main/docs/vault.md).

Locate an existing installer or generator before adding another one. Keep
workspace-specific values in the workspace options instead of hard-coding one
workspace's name, gateway URL or key path into shared configuration.

## Preserve state and apply the right layer

Applications may also write their own configuration. Use chezmoi modify templates
or the application's supported merge mechanism to change only the intended keys,
preserving unrelated settings, other integrations and account state. Preserve
unchanged content where possible so reapplying does not create needless drift.
See the existing
[Codex modify template](https://github.com/wyrd-company/workspace-dotfiles/blob/main/dot_codex/modify_private_config.toml)
for this pattern. A value persisted in `~/.codex/config.toml` can override a default
in `/etc/codex/config.toml`; inspect both layers before changing the default.

Secrets come through Wyrwood's socket using the existing `bao` access. Prefer a
client's native credential or header helper when it supports the integration;
keep credentials out of generated configuration and source control.

For running workspaces, `ansible-sync` uses the source and ref configured in
`/etc/ansible-setup/settings`: a remote source is fetched into its managed checkout;
an absolute local source is used directly. The workspace playbook then runs
`chezmoi update --init`, which pulls the configured dotfiles repository before
applying it. These commands do not automatically consume a separate editing
worktree. Identify the configured sources and the revisions actually applied.
`chezmoi apply <target>` applies a particular user-owned target from its selected
source directory without pulling.

Before merge, verify the branch's templates by rendering or diffing into an
isolated destination, with representative workspace options and existing
application state. Select the branch source explicitly; keep these checks separate
from applying to the running workspace. When applying cooperating layers, install
root helpers or other prerequisites before the dependent dotfiles apply.

Changes to the workspace definition may need a template update or container
rebuild. Read the
[workspace-template README](https://github.com/wyrd-company/workspace-template/blob/main/README.md)
and the generated workspace's `.toha.json` tracking record to identify its template;
consult the installed Toha help for supported operations before choosing an update
path. `/etc/devcontainer/` is read-only apart from the local extension points
documented in the workspace's `AGENTS.md`.

Verify the application's effective configuration, including its precedence and
the required integration's behavior. For files shared with the application,
check that unrelated state survives and repeated applies leave matching settings
unchanged. Report which source changed, whether it was applied to the running
workspace, and any restart or rebuild needed.
