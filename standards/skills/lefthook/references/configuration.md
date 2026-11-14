# Lefthook configuration reference

Everything below is a config key not already covered in `SKILL.md`, grouped
by where it applies: top-level (whole config), hook-level (a specific Git
hook block), and job/command/script-level (an individual unit of work).
Job-level options are documented once; they apply the same way whether set
on a `jobs:` entry, a `commands:` entry, or a `scripts:` entry, unless noted.

## Top-level options

### `min_version`
Fail fast if the installed `lefthook` binary is older than required.
```yml
min_version: 1.1.3
```

### `extends`
Merge in other YAML files (local paths or globs). Order of precedence when
multiple sources define the same thing: `lefthook.yml` → `extends` →
`remotes` → `lefthook-local.yml` (later overrides earlier).
```yml
extends:
  - /home/user/work/lefthook-extend.yml
  - lefthook-extends/file.yml
  - projects/*/specific-lefthook-config.yml
```

### `remotes`
Pull shared hook configs from other Git repos and merge them in
automatically. Each remote needs `git_url`; optionally `ref` (branch/tag —
if you ever set it, keep setting it, lefthook won't guess later),
`refetch`/`refetch_frequency` (`always` / `24h`-style duration / `never`,
default `never` — a failed fetch just warns and reuses the last good copy),
and `configs` (paths within the remote repo, default `[lefthook.yml]`).
```yml
remotes:
  - git_url: git@github.com:evilmartians/lefthook
    ref: v1.0.0
    refetch_frequency: 24h
    configs:
      - examples/ruby-linter.yml
```
`extends` inside a remote config is resolved relative to *that* remote's
repo root. If a remote config declares `scripts:`, its script files must
live at the remote repo's root `<source_dir>` — you don't get to relocate
them.

### `templates`
Named placeholders you can reference in any `run:` as `{name}`, left empty
by default and filled in from `lefthook-local.yml`. Lets you make a shared
config locally overridable (e.g. wrap everything in `dip`) without editing
every job.
```yml
# lefthook.yml
templates:
  wrapper: docker-compose run --rm -v $(pwd):/app service
pre-commit:
  jobs:
    - run: "{wrapper} yarn lint"
```

### `lefthook`
Override how the `lefthook` executable itself is invoked (path, or a
wrapper command using `sh` syntax) — e.g. force a specific bundler/npm
install, or point at a subfolder's binary. Does **not** merge from
`remotes`/`extends` for security reasons; does merge from
`lefthook-local.yml`.
```yml
lefthook: bundle exec lefthook
```

### `source_dir` / `source_dir_local`
Where script files live: `.lefthook/<hook-name>/...` by default
(`source_dir`), and `.lefthook-local/` for scripts referenced only from
`lefthook-local.yml` (`source_dir_local`).

### `assert_lefthook_installed`
`true` fails the hook (exit 1) if the `lefthook` executable can't actually
be found (PATH, node_modules, gem, etc.) — a safety net so a broken install
doesn't silently no-op every hook.

### `skip_lfs`
`true` skips Git LFS hooks even if LFS is present.

### `colors`
`false` disables colored output; or supply a map of hex/ANSI overrides
(`cyan`, `gray`, `green`, `red`, `yellow`). Also controllable via
`NO_COLOR=true` / `CLICOLOR_FORCE=true` env vars.

### `no_tty`
`true` hides the spinner/interactive UI (same as `lefthook run --no-tty`).

### `no_auto_install`
`true` disables lefthook's default behavior of auto-(re)installing hooks
when it notices the config changed. Same as `lefthook run --no-auto-install`.

### `install_non_git_hooks`
Install hooks into `.git/hooks` even for hook names that aren't real Git
hooks — useful for tools like git-flow that call custom hook names.

### `output`
Controls verbosity. List of: `meta, summary, empty_summary, success,
failure, execution, execution_out, execution_info, skips`. All enabled by
default; `output: false` silences everything but errors. Extend at
runtime with `LEFTHOOK_OUTPUT=meta,success,summary lefthook run pre-commit`.

### `rc`
Path to a `sh` script sourced before running hooks — the escape hatch for
GUI git clients (VSCode, etc.) that don't inherit your shell's `$PATH`
tweaks (nvm/rbenv/fnm). Typically set in `lefthook-local.yml` since PATH
setups are per-machine.
```yml
# lefthook-local.yml
rc: ~/.lefthookrc
```
After changing `rc`, run `lefthook install -f` to refresh the hook shims.

### `glob_matcher`
`gobwas` (default) or `doublestar`. Changes how `**` behaves in every
`glob`/`exclude` in the config: `gobwas`'s `**/*.js` requires at least one
directory level (`src/file.js` matches, bare `file.js` doesn't);
`doublestar` matches at any depth including the root, like Bash. Pick
`doublestar` if you're porting globs from another tool or expect `**` to
mean "zero or more directories."

## Hook-level options

Set directly under a hook name (`pre-commit:`, `pre-push:`, etc.), alongside
`jobs`/`commands`/`scripts`.

### `files` (hook-level)
A shell command whose stdout becomes the file list available as `{files}`
to every job in the hook (job-level `files:` overrides this per-job). Empty
result skips the hook's jobs.
```yml
pre-commit:
  files: git diff --name-only master
```

### `follow`
`true` streams the running command/script's stdout live instead of buffering
it for the summary. Avoid combining with `parallel: true` — interleaved
output from multiple jobs is unreadable.

### `fail_on_changes` / `fail_on_changes_diff`
Controls whether lefthook exits non-zero when a job modifies tracked files
(e.g. an auto-fixer). Values: `never` (default), `always`, `ci` (only when
`CI` env var is set — pairs well with `stage_fixed` for a smooth local
experience but a strict CI check), `non-ci` (opposite, for CI setups that
auto-commit fixes themselves, e.g. autofix.ci). `fail_on_changes_diff: true`
prints the diff when it triggers (default: only in CI).

### `exclude_tags`
Tags (or command names) to skip for this hook. Overridable at runtime with
`LEFTHOOK_EXCLUDE=tag1,tag2`. The standard way to disable a category of
checks from `lefthook-local.yml` without touching the shared config.

## Job / command / script-level options

These apply to an entry under `jobs:`, or to an entry in the `commands:` /
`scripts:` maps (the older, name-keyed syntax — semantically equivalent).

### `name`
Label shown in output; also the merge key across `extends`/local config
(unnamed jobs just append instead of merging).

### `run` / `script` (mutually exclusive per job)
`run:` is an inline shell command executed via `sh`, with the placeholder
templates described in `SKILL.md`. `script:` names a file under
`<source_dir>/<hook-name>/` and requires `runner:` (see SKILL.md's Scripts
section). Long file lists are automatically chunked into multiple sequential
invocations if they'd exceed the OS command-length limit.

### `args`
Appended to `run`/`script` invocations — mainly useful so
`lefthook-local.yml` can override just the arguments without redefining the
whole command. Supports the same placeholders as `run`. Explicitly setting
`args` (even to `"{0}"`) discards any raw Git-supplied hook arguments.

### `glob`
One glob or a list of globs filtering which files count for this job (see
`glob_matcher` above for `**` semantics). Only affects file-template
expansion / the "skip if nothing matches" filtering described in SKILL.md —
it does not filter anything if `run` has no file template and no
`files`/`exclude`/`file_types` are set either.

### `files` (job-level)
Same idea as the hook-level version but scoped to one job; overrides it.

### `file_types`
Restrict by file kind rather than name pattern. Structural types (`text`,
`binary`, `executable`, `not executable`, `symlink`, `not symlink`) combine
with AND logic; MIME types (`text/javascript`, `text/x-python`,
`application/json`, etc.) combine with OR logic. Useful for e.g. "lint text
files but hex-dump binaries" or "skip symlinks."

### `root`
Changes the working directory for the command (e.g. a `frontend/` subfolder
with its own `package.json`). Does **not** affect glob matching — globs are
always evaluated from the repo root regardless of `root`.

### `exclude`
Globs to exclude from the file template, honoring `glob_matcher`.

### `env`
Extra environment variables for this job only. Also the mechanism for
extending `$PATH` per-job from `lefthook-local.yml` when a GUI git client
doesn't inherit your shell's PATH tweaks.

### `tags`
Labels for `exclude_tags`/`LEFTHOOK_EXCLUDE`/`lefthook run --tag` filtering.

### `skip` / `only`
See SKILL.md. Full value set: `true`/`false`, `rebase`, `merge`,
`merge-commit`, `ref: <glob>`, `run: <shell command>` (skip/only if exit
code 0). `skip` wins if both match on the same job.

### `interactive`
`true` gives the command a real TTY (opens `/dev/tty` on Unix) so it can
prompt interactively — needed for tools like `cz --hook` that ask
questions. Interactive jobs run after non-interactive ones unless `piped:
true`. Ignored if `no_tty` is set.

### `use_stdin`
Forwards the OS's real stdin to this one command/script (only one job per
hook should set this — the rest get nothing). Needed for scripts that do
`while read ...` against Git-supplied data (e.g. parsing `pre-push` ref
updates), since lefthook's pseudo-TTY otherwise never signals EOF.

### `stage_fixed`
`pre-commit`-only. `true` runs `git add` after the job, on whatever
`files`/`{staged_files}` (filtered by `glob`/`exclude`) the job touched —
the standard pattern for auto-fixing linters (`eslint --fix`, `rubocop -A`)
so the fix ends up in the commit instead of leaving the working tree dirty.

### `fail_text`
Extra text appended to the failure summary — e.g. a hint like "Add node
executable to $PATH" for a predictably confusing failure mode.

### `priority`
Integer ordering hint for sequential/piped execution (lower runs first;
`0`/unset effectively means "last"). No effect under `parallel: true`.

### `group`
Nest a sub-list of jobs with their own `parallel`/`piped` flow inside a
single job slot — e.g. a piped migration sequence running alongside other
parallel top-level jobs. `env`, `root`, `glob`, and `exclude` set on the
group apply to every nested job; other options must be set per nested job.
Give the group a `name:` if you need it to merge with local-config/extends
overrides.
```yml
pre-commit:
  parallel: true
  jobs:
    - name: migrate
      root: backend/
      glob: "db/migrations/*"
      group:
        piped: true
        jobs:
          - run: bundle install
          - run: rails db:migrate
    - run: yarn lint --fix {staged_files}
```
