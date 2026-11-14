# Lefthook CLI reference

Assumes `lefthook` is already installed and on `PATH` (via npm/gem/Homebrew/
etc. — installation itself isn't covered here).

## Commands

### `lefthook install [hook-1] [hook-2] ...]`
Creates an empty `lefthook.yml` if none exists, then writes/updates
`.git/hooks/*` shims for every hook block in the config. Pass specific hook
names to install only those. You don't need to rerun this after editing
jobs inside an already-installed hook — the config is read fresh on every
`lefthook run`. Rerun it when you add a *new* hook name to the config, or
after changing the `rc`/`lefthook` executable options. `-f` forces
reinstall of existing shims.

The npm `lefthook` package runs this automatically in a postinstall script;
other install methods need it run manually after cloning.

### `lefthook run <hook-name>`
Executes a hook's jobs directly, without a real Git action triggering it —
the fast way to iterate on a `lefthook.yml` change. Installed Git hook
shims just call this under the hood.

Useful flags:
- `--job <name>` / `--tag <tag>` — run only matching jobs (repeatable,
  combinable): `lefthook run pre-commit --job lint --tag security`
- `--all-files` — force every file template to behave like `{all_files}`
- `--file <path>` (repeatable) — force file templates to this explicit set
  instead of the computed one (`--all-files` wins if both are given)
- `--no-tty` — same as the `no_tty` config option
- `--no-auto-install` — same as the `no_auto_install` config option

### `lefthook add <hook-name> [-d|--dirs]`
Registers a hook name with Git (writes the `.git/hooks/<name>` shim). With
`-d`/`--dirs`, also creates `.lefthook/<hook-name>/` so you have somewhere
to drop a script file before referencing it in `lefthook.yml`.

### `lefthook validate`
Validates the config against lefthook's JSON schema. Run this after hand
editing `lefthook.yml`, especially after nontrivial structural changes
(groups, remotes) — the YAML can be syntactically valid but semantically
wrong (e.g. `piped: true` and `parallel: true` together) and this catches
it before a broken hook silently no-ops.

### `lefthook dump`
Prints the fully-merged effective config — `lefthook.yml` plus `extends`,
`remotes`, and `lefthook-local.yml` all resolved and merged in the actual
precedence order. Use this to debug "why is this job not running the way I
expect" when remotes/extends/local overrides are in play; it's the ground
truth, not the source files.

### `lefthook check-install`
Non-interactive check of whether hooks are installed and in sync. Exit code
`0` = installed & synced, `1` = not installed or needs a sync — useful in
CI or an onboarding script to nudge a developer to run `lefthook install`.

### `lefthook uninstall`
Removes lefthook's shims from `.git/hooks`.

### `lefthook self-update`
Updates the binary to the latest GitHub release. Only works if lefthook was
installed from source or a downloaded release binary — if it came from
npm/gem/Homebrew/etc., update it through that package manager instead.

### `lefthook version [--full]`
Prints the version; `--full` adds the commit hash.

## Environment variables

### `LEFTHOOK`
`LEFTHOOK=0` or `LEFTHOOK=false` disables lefthook for that one command —
the standard "just let me commit" escape hatch:
```bash
LEFTHOOK=0 git commit -m "skip hooks this once"   # after git add <paths>
```
In CI with the npm package, `CI=true` normally suppresses the postinstall
hook-install step; set `LEFTHOOK=1`/`true` to force hook installation
despite `CI=true`.

### `CI`
Set `CI=true` when installing via the npm package in CI to prevent
`postinstall` from installing Git hooks in an environment that doesn't need
them (see `LEFTHOOK` above for the override).

### `LEFTHOOK_EXCLUDE`
Comma-separated tags or command names to skip for this run, same effect as
the `exclude_tags` config option:
```bash
LEFTHOOK_EXCLUDE=ruby,security,lint git commit -m "skip some checks"
```

### `LEFTHOOK_CONFIG`
Point at a different main config file: `LEFTHOOK_CONFIG=~/global_lefthook.yml`.
Local config, `extends`, and `remotes` are still loaded and merged in
normally on top of it.

### `LEFTHOOK_OUTPUT`
Comma-separated list from the same vocabulary as the `output` config option
(`meta,summary,success,failure,execution,execution_out,execution_info,skips,empty_summary`),
or `false` to silence everything but errors:
```bash
LEFTHOOK_OUTPUT=summary lefthook run pre-commit
```

### `LEFTHOOK_VERBOSE`
`1`/`true` enables verbose logging — the first thing to set when a hook
isn't behaving as expected and you need to see what lefthook thinks it's
doing.

### `LEFTHOOK_BIN`
Force a specific `lefthook` executable path instead of PATH/package-manager
autodetection — useful when multiple install methods coexist (e.g. Homebrew
binary plus a Gemfile entry shadowed by rbenv) or when debugging lefthook
itself.

### `NO_COLOR` / `CLICOLOR_FORCE`
`NO_COLOR=true` disables colored output for lefthook and everything it
shells out to; `CLICOLOR_FORCE=true` forces it on.
