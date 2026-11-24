# Application configuration

Read this when designing, implementing or reviewing runtime configuration for a published or released application: a command-line tool, a client, or a self-hosted daemon or service. Configuration specifications and their native definitions are placed by [designing](../../designing/references/documents.md#specification-definitions), and generated reference documentation follows the [user documentation standard](user-documentation.md#reference). Not for workspace environment configuration ([workspace](workspace.md)), deployed internal services and their user settings, or CI/CD settings.

## Files and locations

- **Every setting lives in a configuration file.** Configuration files are YAML (`.yml`) with `kebab-case` field names. Settings are never environment-only or flag-only; the only exceptions are meta-options that cannot come from the file being loaded, such as `--config`, `--help` and `--version`.
- **Default locations:**
  - **System services:** `/etc/<app>/config.yml`.
  - **User applications and CLIs:** `$XDG_CONFIG_HOME/<app>/config.yml`, falling back to `~/.config/<app>/config.yml` when `XDG_CONFIG_HOME` is unset or empty. When a user application also supports system-wide defaults in `/etc/<app>/config.yml`, the user file overrides the system file.
  - **Project-local tools:** when an application operates on a repository or working directory, support a documented local file (such as `<app>.yml` or `.<app>.yml`) that overrides user configuration.
- **Explicit path override:** Support `--config <path>` (and `-c` where it does not conflict) and `<APP>_CONFIG`. An explicit path replaces default discovery and fails immediately if the file is missing or unreadable. Under default discovery, a missing file falls back to built-in defaults and fails only when required settings are unset.
- **Multiple modes in one binary:**
  - When modes are exclusive and serve distinct roles or lifecycles (such as a daemon and a CLI client), use separate files named for each mode: `/etc/<app>/server.yml` and `~/.config/<app>/client.yml`.
  - When modes run together or share one lifecycle, keep one `config.yml` with top-level sections per mode.
  - When settings apply identically across modes, keep them shared with no split.

## Sources, naming and precedence

- **Precedence from lowest to highest:**
  1. Built-in defaults
  2. System configuration file (`/etc/<app>/...`)
  3. User configuration file (`$XDG_CONFIG_HOME/<app>/...` or `~/.config/<app>/...`)
  4. Project-local configuration file (for project-scoped tools)
  5. Environment variables
  6. CLI flags

  When `--config` or `<APP>_CONFIG` is set, that file replaces layers 2 through 4.
- **Expose settings across surfaces:** Offer environment variables for runtime settings, especially for services and containerised workloads. Applications with a CLI also expose settings as CLI flags, except literal secret values (see [Secrets](#secrets)).
- **Derive names mechanically from the YAML path:**
  - **YAML:** `kebab-case`, nested by concept (`server.listen-addr`).
  - **Environment variables:** `<APP>_UPPER_SNAKE_CASE`, prefixed with the application name to avoid collisions, joining path segments and hyphens with `_` (`APP_SERVER_LISTEN_ADDR`).
  - **CLI flags:** `--kebab-case`, joining path segments with `-` (`--server-listen-addr`), with a shorter documented alias where unambiguous.
- **Scalars everywhere; complex structures in the file:** Expose every scalar setting (string, number, boolean, duration, enum) across the config file, environment variables and CLI flags (excluding literal secret flags). Keep nested structures and lists of objects in the config file unless a concrete operational need justifies a dedicated flag or structured override.
- **Distinguish unset from explicit zero values:** Track whether each layer actually provided a value. An omitted CLI flag or unset environment variable never overwrites a lower-precedence value, while an explicit `false`, `0` or empty string (`--no-<flag>`, `APP_FLAG=false`) overrides a lower layer.

## Secrets

- **Never require secrets on disk or in environment variables.** Every secret setting offers retrieval methods so credentials stay out of config files and environment variables.
- **Support a consistent set of secret sources:**
  - **OpenBao / Vault:** Built into the application, using a client library where full authentication or lease renewal is needed, or direct HTTP/Unix-socket API calls for simple reads to avoid heavy dependencies. Follow standard OpenBao/Vault conventions (address or Unix socket, mount, path, key, and standard auth methods); never hard-code internal workspace paths or assumptions into published software.
  - **Credential helper command:** A user-configured command invoked by the application to fetch the secret. Configure it as an argument array (`["cmd", "arg1"]`) rather than a shell string to avoid shell injection, enforce a timeout, treat a non-zero exit as a failure, and document the stdout contract: a single trimmed string for one secret, or a documented JSON object schema when one helper returns several secrets.
  - **File path:** Read the secret from a file path (trimming a trailing newline), supporting container secret mounts and systemd `LoadCredential`.
  - **Direct value:** Accepted where convenient for local development or testing, never the only way to supply a secret.
- **No literal secrets in CLI flags:** Command-line arguments leak into process listings and shell history. Expose secret settings on the CLI through secret-source flags (`--<secret>-file`, `--<secret>-stdin`, `--<secret>-command`, or OpenBao/Vault flags), not a literal `--<secret> <value>` flag.
- **Reject ambiguous sources in one layer:** When two sources are configured for the same secret at the same precedence level (for example, both a direct value and a credential helper in the same file), fail at startup rather than guessing. Across layers, a higher-precedence layer replaces the lower layer's secret source completely.
- **Redact everywhere:** Replace secret values with a fixed marker such as `<redacted>` in logs, error messages, traces and config inspection output.
- **Handle rotation by lifecycle:** CLIs resolve secrets as needed for the command. Long-lived services re-fetch secrets on expiry or authentication failure (or renew OpenBao/Vault leases) so credential rotation does not require a restart.

## Shape, validation and diagnostics

- **One source of truth:** Define the configuration contract in `docs/specifications/configuration.yml` with its JSON Schema beside it (for example `configuration.schema.v1.json`, or per-mode schemas such as `configuration.client.schema.v1.json` and `configuration.server.schema.v1.json`) as [designing](../../designing/references/documents.md#specification-definitions) specifies. Generate reference documentation from the schema and validate committed examples in `docs/user/` against it in `task check`, as the [user documentation standard](user-documentation.md#reference) requires.
- **Keep the shape concise and user-centred:**
  - Group fields by user concept rather than internal code packages, and keep nesting shallow (two to three levels deep).
  - Choose safe defaults so a minimal working configuration is only a few lines.
  - Encode units in field names or typed formats (`timeout: 30s` or `timeout-seconds`, never an untyped `timeout: 30`).
- **Fail fast and strictly on startup:**
  - Reject unknown keys so typos (such as `auth_token` instead of `auth-token`) fail immediately rather than falling back to defaults.
  - Validate the merged configuration against the schema on startup, reporting every error together with its field path, the source that supplied it (file path, environment variable or flag), and what was expected.
  - Warn on deprecated keys with the replacement name rather than silently ignoring them.
- **Provide inspection commands for non-trivial configuration:** Offer `<app> config validate` (validates syntax and schema, exiting non-zero on error) and `<app> config show` (prints the effective merged configuration with secrets redacted and, where practical, the source layer for each value).
