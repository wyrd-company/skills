# Application configuration

Read this when designing, implementing or reviewing runtime configuration for a published or released application: a command-line tool, a client, or a self-hosted daemon or service. Configuration specifications and their native definitions are placed by [designing](../../designing/references/documents.md#specification-definitions), and generated reference documentation follows the [user documentation standard](user-documentation.md#reference). Not for workspace environment configuration ([workspace](workspace.md)), deployed internal services and their user settings, or CI/CD settings.

## Files and locations

- **Every setting lives in a configuration file.** Configuration files are YAML (`.yml`) with `kebab-case` field names. Settings are never environment-only or flag-only; the only exceptions are:
  - meta-options that cannot come from the file being loaded, such as `--config`, `--help` and `--version`;
  - per-invocation inputs that must not persist across runs, such as prompt answers (`--yes` in the [interface standard](interface.md#terminal)) and one-shot stdin inputs (`--<secret>-stdin`).
- **Default locations:**
  - **System services:** `/etc/<app>/config.yml`.
  - **User applications and CLIs:** `$XDG_CONFIG_HOME/<app>/config.yml`, falling back to `~/.config/<app>/config.yml` when `XDG_CONFIG_HOME` is unset or empty. When a user application also supports system-wide defaults in `/etc/<app>/config.yml`, the user file overrides the system file.
  - **Project-local tools:** when an application operates on a repository or working directory, look for `.<app>.yml` from the current working directory upward through parent directories up to the repository root (or filesystem root when outside a repository), loading only the nearest file found, which overrides user configuration. Treat project-local configuration as untrusted by default using an explicit allowlist declared in the schema. A field qualifies for the project-local allowlist only if a hostile repository setting it can affect solely how the tool operates within that project: it runs and loads no code, sends nothing to and fetches nothing from a host the user did not choose, writes nothing outside the project, and weakens no security or validation check (so executable commands, editors, hooks, secret sources, update/telemetry/credential endpoints, paths outside the project, and TLS/CA/proxy overrides all fail the test). Per-layer validation rejects any setting outside that allowlist from a project-local file. When a tool permits restricted settings from a project-local file, lift the refusal only after an explicit user trust decision persisted outside the repository (under user config or state), bound to both the file's canonical path and a digest of the approved restricted settings; any change to that digest invalidates trust and requires fresh approval. Grant trust only through a dedicated action that names the file and shows the restricted settings being approved (such as `<app> trust <path>` or an interactive prompt answered at a terminal). General prompt-answering flags such as `--yes` never grant trust, and a non-interactive run without a matching recorded approval refuses the restricted settings.
- **Explicit path override and missing files:** Support `--config <path>` (and `-c` where it does not conflict) and `<APP>_CONFIG`. An explicit path replaces default discovery and fails immediately if the file is missing or unreadable. Under default discovery, skip each absent optional file, retain values from all other layers (built-in defaults, present files, environment variables and CLI flags), and fail only when required settings remain unset after layering.
- **Resolve relative paths safely:** Resolve every relative path set in a configuration file (such as a CA bundle, client certificate, socket, secret `file`, or `command[0]` containing a path separator like `./bin/helper`) against the directory of the configuration file that declared it, never the current working directory. Resolve relative paths supplied by environment variables or CLI flags against the current working directory. Resolve a bare executable name (no path separator) strictly via `PATH`, never against the current working directory.
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
- **Merging across layers:** Mappings merge key by key across layers, except per-secret source mappings (which replace as a whole unit; see [Secrets](#secrets)). Lists replace the lower layer's list whole, and an explicit empty list (`[]`) clears the inherited list.
- **Expose settings across surfaces:** Offer environment variables for runtime settings, especially for services and containerised workloads. Applications with a CLI also expose settings as CLI flags, except literal secret values (see [Secrets](#secrets)).
- **Derive names mechanically from the YAML path:**
  - **YAML:** `kebab-case`, nested by concept (`server.listen-addr`).
  - **Environment variables:** `<APP>_UPPER_SNAKE_CASE`, prefixed with the application name to avoid collisions, joining path segments and hyphens with `_` (`APP_SERVER_LISTEN_ADDR`). Well-known cross-tool variables such as `NO_COLOR` ([interface](interface.md#terminal)), `BAO_ADDR` and `VAULT_ADDR` sit in the environment-variable layer as documented aliases of the corresponding setting and are listed in the generated reference. Within the environment layer, the derived `<APP>_` variable wins over any alias, and when multiple aliases map to the same setting, document their deterministic order (for OpenBao/Vault, `BAO_ADDR` wins over `VAULT_ADDR`).
  - **CLI flags:** `--kebab-case`, joining path segments with `-` (`--server-listen-addr`), with a shorter documented alias where unambiguous.
  - **No collisions or reserved-name overrides:** Every exposed field produces a unique environment variable and CLI flag name (avoiding sibling/nested ambiguities such as `server.listen-addr` alongside `server-listen-addr`) and never collides with reserved meta-options (`--config`, `-c`, `<APP>_CONFIG`, `--help`, `-h`, `--version`). Check uniqueness and reserved-name exclusions automatically in `task check` (for example in the schema or reference-generation tests).
- **Scalars everywhere; list and structured encoding:** Expose every scalar setting (string, number, boolean, duration, enum) across the config file, environment variables and CLI flags (excluding literal secret flags). When a list of scalars (such as allowed hosts or command arguments) is exposed as an environment variable or CLI flag, encode it as a JSON array (never whitespace- or comma-split), where `[]` clears an inherited list. Keep nested structures and lists of objects in the config file unless a concrete operational need justifies a dedicated flag or structured override.
- **Distinguish unset from explicit zero values:** Track whether each layer actually provided a value. An omitted CLI flag or unset environment variable never overwrites a lower-precedence value, while an explicit `false`, `0` or empty string (`--no-<flag>`, `APP_FLAG=false`) overrides a lower layer.

## Secrets

- **Never require secrets on disk or in environment variables.** Every secret setting offers retrieval methods so credentials stay out of config files and environment variables.
- **Use a shared YAML shape for secret sources:** Represent each secret field as a mapping selecting one source key (`value`, `file`, `vault` or `command`):

  ```yaml
  auth:
    token:
      # Select exactly one source per secret:
      file: /run/credentials/app/token
      # vault:
      #   address: https://vault.example.com
      #   mount: secret
      #   path: apps/example
      #   key: token
      # command: ["my-helper", "get-token"]
      # timeout: 10s
      # value: "<dev-token>"
  ```

  - **OpenBao / Vault (`vault`):** Built into the application, using a client library where full authentication or lease renewal is needed, or direct HTTP/Unix-socket API calls for simple reads to avoid heavy dependencies. Follow standard OpenBao/Vault conventions (address or Unix socket, mount, path, key, and standard auth methods); never hard-code internal workspace paths or assumptions into published software. When several secrets share one Vault server and auth setup, allow top-level `vault:` defaults that merge across layers and fill missing connection or auth fields on each effective per-secret `vault:` block after the merge. Whenever any layer or per-secret `vault:` block sets the Vault server (`address` or socket), it discards authentication settings from lower layers and from top-level `vault:` defaults configured for a different server; it must supply its own authentication (or use that server's explicit unauthenticated/socket mode) or effective validation fails.
  - **Credential helper command (`command`, optional `timeout` valid only with `command`):** A user-configured command invoked by the application to fetch the secret. Configure `command` as an argument array (`["cmd", "arg1"]`) rather than a shell string to avoid shell injection, enforce a timeout, treat a non-zero exit as a failure, and document the stdout contract: a single trimmed string for one secret, or a documented JSON object schema on a parent credentials block (for example `auth.credentials.command`) when one helper returns several secrets at once. A parent credentials block declares in the schema which secret fields it supplies.
  - **File path (`file`):** Read the secret from a file path (trimming a trailing newline), supporting container secret mounts and systemd `LoadCredential`.
  - **Direct value (`value`):** Accepted where convenient for local development or testing, never the only way to supply a secret.
- **No literal secrets in CLI flags:** Command-line arguments leak into process listings and shell history. Expose secret settings on the CLI through secret-source flags (`--<secret>-file`, `--<secret>-stdin`, `--<secret>-command`, or OpenBao/Vault flags), not a literal `--<secret> <value>` flag. `--<secret>-command` and `<APP>_<SECRET>_COMMAND` use the JSON array encoding above.
- **Reject ambiguous sources in one layer and replace whole across layers:** When two sources are configured for the same secret within one precedence layer (for example, both `file` and `command`, or both a parent credentials helper and an individual secret it declares, in the same layer), fail at startup before merging. Across layers, a per-secret source mapping is replaced as a whole unit: any higher layer setting a secret source must provide a complete source (for `vault`, at least the secret's `path` and `key`), so partial fragments such as setting only `<APP>_AUTH_TOKEN_TIMEOUT` or `<APP>_AUTH_TOKEN_VAULT_KEY` fail per-layer validation instead of silently patching a lower layer's source. A higher-layer individual secret source overrides only that secret from a lower-layer parent credentials helper, while a higher-layer parent helper replaces all secrets it declares.
- **Redact everywhere:** Replace secret values with a fixed marker such as `<redacted>` in logs, error messages, traces and config inspection output.
- **Handle rotation by lifecycle:** CLIs resolve secrets as needed for the command. Long-lived services re-fetch secrets on expiry or authentication failure (or renew OpenBao/Vault leases) so credential rotation does not require a restart.

## Shape, validation and diagnostics

- **One source of truth:** Describe the configuration contract in `docs/specifications/configuration.yml` and define it in JSON Schema beside it (for example `configuration.schema.v1.json`, or per-mode schemas such as `configuration.client.schema.v1.json` and `configuration.server.schema.v1.json`), placed by [specification definitions](../../designing/references/documents.md#specification-definitions). Generate reference documentation from the schema ([reference](user-documentation.md#reference)) and validate committed examples in `docs/user/` against it ([published links](user-documentation.md#published-links)).
- **Keep the shape concise and user-centred:**
  - Group fields by user concept rather than internal code packages, and keep nesting shallow (two to three levels deep).
  - Choose safe defaults so a minimal working configuration is only a few lines.
  - Encode units in field names or typed formats (`timeout: 30s` or `timeout-seconds`, never an untyped `timeout: 30`).
- **Fail fast and strictly on startup:**
  - **Validate each selected layer before merging:** Check every loaded file, supplied environment variable and CLI flag layer for unknown keys in files and CLI flags (so typos such as `auth_token` fail immediately), type and format errors, project-local allowlist and trust restrictions, and conflicting or incomplete secret sources within that layer, so a higher layer never hides a broken lower layer. For the environment layer, read only variables matching a derived name or a documented cross-tool alias and ignore all other environment variables so unrelated variables sharing a prefix never fail startup.
  - **Validate the effective configuration after merging:** Check required fields and cross-field constraints on the merged result, reporting every error together with its field path, the source layer that supplied it (file path, environment variable or flag), and what was expected.
  - Warn on deprecated keys with the replacement name rather than silently ignoring them.
- **Provide inspection commands for non-trivial configuration:** Offer `<app> config validate` (validates syntax and schema, exiting non-zero on error) and `<app> config show` (prints the effective merged configuration with each secret's configured source and, where practical, the source layer for each value). Neither command executes credential helpers, reads secret files, or contacts OpenBao/Vault; `config show` replaces any direct secret `value` and any inline Vault authentication credentials with `<redacted>`.
