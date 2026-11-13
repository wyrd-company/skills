# Workspace

Read this when understanding, configuring or troubleshooting a workspace's environment: where a piece of configuration belongs, how it is applied, and how to make a change last. Not for an application's own configuration inside a product repository.

A workspace is a devcontainer for one product or theme. Agents, and people connecting over SSH or VS Code, all run as the shared `vscode` account, and its home-directory configuration is part of the standard environment. The operator chosen for a thread decides who commits and pushes; it does not select another account or another configuration. The workspace's own `AGENTS.md` gives its paths and limits.

## Where configuration belongs

`workspace-ansible` and `workspace-dotfiles` configure the same workspace, split by who owns the configuration:

- **Owned by root:** `workspace-ansible`.
- **Owned by `vscode`:** `workspace-dotfiles`, managed with chezmoi.
- **Prefer `/etc`** for settings common to everyone, when the application reads them from there. When it needs a file in the home directory, manage that file in the dotfiles.

Choose the layer by what the application actually supports for the setting. A system-wide layer may reject fields, or disable extensions, that the user's file allows: check before you choose it. A setting in the home directory configures the shared account. It is not one person's preference.

## Find the source

Read the configuration that is in effect, then find the source that produces it before you change anything. A rendered file shows what runs; a lasting change goes in its source.

| Source | What it holds |
|---|---|
| `devcontainers` | Base images and features: the system tools and what the container can do. |
| `workspace-template` | The workspace definition, mounts, where persistent state lives, the options, and the workspace-wide `AGENTS.md`. |
| `workspace-ansible` | Root configuration and system helpers, rendered from the workspace options, and the run that applies the dotfiles. |
| `workspace-dotfiles` | The `vscode` account's configuration and the tools installed for it. |

Each repository's own instructions and docs are its manual:

- The workspace definition, paths and provisioning: [Workspaces](https://github.com/wyrd-company/workspace-template/blob/main/docs/workspaces.md), and [Devcontainers](https://github.com/wyrd-company/workspace-template/blob/main/docs/devcontainers.md) where it applies.
- Root rendering and the order of applying: `workspace-ansible`'s `container.yml` and its templates. The workspace options are at `/etc/workspace/config.yml`.
- The account's configuration and tools: the dotfiles' templates, package lists and apply scripts. Secrets: [Vault](https://github.com/wyrd-company/workspace-dotfiles/blob/main/docs/vault.md).

Look for an existing installer or generator before you add one. Values that differ between workspaces, such as a name, a gateway URL or a key path, come from the workspace options, never hard-coded into shared configuration.

## Keep what applications write

Applications write to their own configuration files too. Change only the keys you mean to, with a chezmoi modify template or the application's own merge mechanism, so other settings, other integrations and the account's state survive. Leave unchanged content as it is, so applying again changes nothing. The dotfiles' [Codex modify template](https://github.com/wyrd-company/workspace-dotfiles/blob/main/dot_codex/modify_private_config.toml) is the pattern.

Layers override each other. A value in `~/.codex/config.toml` overrides the default in `/etc/codex/config.toml`, for example. Read every layer before changing a default.

## Secrets

Secrets come through the Wyrwood socket, with the existing `bao` access. Prefer an application's own credential or header helper when it has one for the integration. Credentials never go in generated configuration or in source control.

## Check a branch apart from applying it

Applying configuration and checking a branch are different things.

- **Applying:** `ansible-sync` uses the source and ref set in `/etc/ansible-setup/settings`. A remote source is fetched into its managed checkout; a local absolute path is used as it is. The playbook then runs `chezmoi update --init`, which pulls the configured dotfiles repository before applying it. Neither picks up a worktree you are editing. Know which sources are configured, and which revisions were actually applied.
- **Applying one file:** `chezmoi apply <target>` applies one `vscode`-owned file from its source directory, without pulling.
- **Checking a branch, before merge:** render or diff its templates into a separate destination, with realistic workspace options and existing application state, and the branch selected as the source explicitly. Keep this apart from applying to the running workspace.

When the layers depend on each other, apply the root helpers and other prerequisites before the dotfiles that need them.

A change to the workspace definition may need a template update or a container rebuild. The [workspace-template README](https://github.com/wyrd-company/workspace-template/blob/main/README.md) and the workspace's `.toha.json` record say which template it came from. Read Toha's installed help for how to update it. `/etc/devcontainer/` is read-only, apart from the local extension points the workspace's `AGENTS.md` names.

## Done

The application's effective configuration has the setting, with its precedence understood, and the integration behaves as required. In files the application also writes, unrelated state survived, and applying again changed nothing. Report which source changed, whether the change was applied to the running workspace, and any restart or rebuild it needs.
