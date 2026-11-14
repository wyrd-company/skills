---
name: lefthook
description: Configure and use Lefthook, the fast Git hooks manager, in a repository. Use this whenever the user wants to add or edit pre-commit/pre-push/commit-msg hooks, write or debug a lefthook.yml (or lefthook.toml/json), run linters/tests/formatters on staged or pushed files via Git hooks, wrap tools like commitlint/rubocop/eslint into hooks, set up parallel or piped hook execution, filter files with glob/exclude/file_types, share hook configs across repos with remotes/extends, or troubleshoot lefthook install/run/validate/dump commands. Trigger on mentions of "lefthook", "lefthook.yml", "git hooks", "pre-commit hook" (the Lefthook tool, not the separate Python "pre-commit" framework), "husky alternative", or requests to auto-run checks before commit/push.
---

# Lefthook

Lefthook is a fast, single-binary Git hooks manager. You write a `lefthook.yml`
describing what to run for each Git hook (pre-commit, pre-push, commit-msg,
etc.), then `lefthook install` drops a tiny shim into `.git/hooks/*` that
calls `lefthook run <hook-name>`. All the actual logic — which linters run,
on which files, in what order — lives in the YAML, not in the hook scripts
themselves. This is the core reason to reach for it: hooks become versioned,
declarative config instead of ad-hoc shell scripts.

Full option-by-option reference lives in `references/configuration.md`
(long-tail config keys) and `references/cli.md` (every CLI command and env
var). Read those when you need a key not covered below — don't guess at
syntax, the schema is opinionated and typos fail silently or noisily
depending on the key.

## Core workflow

1. Create/edit `lefthook.yml` in the repo root.
2. Run `lefthook install` to (re)generate the Git hook shims. You only need
   to rerun this when hook *names* change (new hooks added) or when the
   `lefthook` binary/config path changes — editing jobs inside an existing
   hook takes effect immediately since the config is read on every run.
3. Trigger it: `git commit`, `git push`, etc. — or run it directly with
   `lefthook run <hook-name>` to test without making a real commit.
4. Validate before committing config changes: `lefthook validate`.

## Minimal example

```yml
# lefthook.yml

pre-commit:
  parallel: true
  jobs:
    - run: yarn eslint --fix {staged_files}
      glob: "*.{js,ts,jsx,tsx}"
      stage_fixed: true

    - run: bundle exec rubocop --force-exclusion -- {staged_files}
      glob: "*.rb"
```

Adapt to the project's real toolchain — don't invent linters that aren't
actually installed. Check `package.json`/`Gemfile`/etc. first for what's
already in use.

## Config file location

Lefthook looks for `lefthook.yml` (also accepts `.yaml`, `.toml`, `.json`,
`.jsonc`, with or without a leading dot, optionally under `.config/`) in the
repo root. If more than one matching file exists, which one wins is
undefined — stick to a single format per project.

`lefthook-local.yml` is an optional, git-ignored companion file that
overrides/extends the main config — useful for personal overrides (e.g.
wrapping a command in Docker, or disabling a check locally) without
affecting teammates. See "Local overrides" below.

## Anatomy of a hook

A top-level key is a Git hook name (`pre-commit`, `pre-push`, `commit-msg`,
`post-merge`, ...) or a custom name you invoke yourself via `lefthook run`.
Under it:

```yml
pre-commit:
  parallel: true        # or `piped: true` — see "Execution order" below
  jobs:
    - name: lint         # optional, shown in output; required if you want
                          # this job mergeable via extends/local config
      run: yarn lint {staged_files}
      glob: "*.js"        # only run/count files matching this
      exclude: "*.min.js"
      root: "frontend/"    # cwd for the command; doesn't affect glob matching
      env:
        NODE_ENV: test
      stage_fixed: true    # pre-commit only: `git add` the files back after
      tags: [frontend]
      skip: rebase          # or `only:` — see skip.md semantics below
```

`jobs` is the modern, preferred way to define work (added in 1.10.0) — each
entry is either a `run:` command, a `script:` (see Scripts below), or a
nested `group:` of jobs with its own `parallel`/`piped` flow. You'll also
see older configs using `commands:` (a map of name → options) and `scripts:`
(a map of script filename → options) as siblings of `jobs:` — they're
equivalent in capability to individual jobs, just a different — older —
syntax. Prefer `jobs:` for new configs since it supports grouping and mixes
commands and scripts freely in one ordered list.

### File template placeholders in `run`

- `{staged_files}` — files staged for commit
- `{push_files}` — committed files not yet pushed
- `{all_files}` — every file tracked by git
- `{files}` — output of a custom `files:` command you provide
- `{cmd}` — the command itself (useful for wrapping, e.g. `docker run ... {cmd}`)
- `{0}`, `{1}`, `{2}`, ... — raw Git hook arguments (e.g. `{1}` is the commit
  message file path in `commit-msg`)
- `{lefthook_job_name}` — the current job's name

`glob`/`exclude`/`file_types`/`root` filter which files a template expands
to. If a job has one of these filters but no explicit files template in
`run`, lefthook still applies the filter to the hook's default file set
(`{staged_files}` for pre-commit, `{push_files}` for pre-push) and **skips
the job entirely if nothing matches** — this is usually what you want and
avoids invoking a linter with zero files.

Quote the placeholder (`"{staged_files}"` or `'{staged_files}'`) if
filenames might contain spaces or you're targeting Windows.

### Scripts

For anything more than a one-liner, put a script under
`<source_dir>/<hook-name>/` (default `.lefthook/`) instead of inlining a
long `run:`. Scaffold the directory with `lefthook add -d <hook-name>`,
write the script, then reference it:

```yml
pre-commit:
  jobs:
    - script: "lint.sh"
      runner: bash
```

`runner` is invoked as `<runner> <path-to-script>` (e.g. `runner: node`,
`runner: "go run"`). Pass arguments with `args:` (same template
placeholders as `run`). Use `use_stdin: true` if the script itself reads
from stdin (e.g. a `while read ...` loop parsing `pre-push` ref updates) —
without it lefthook's pseudo-TTY never closes stdin and the script hangs.

## Execution order: parallel vs piped vs sequential

- Default (neither set): jobs run **sequentially**, all of them, regardless
  of earlier failures.
- `parallel: true`: all jobs run concurrently. Good for independent linters
  (eslint + rubocop have nothing to say to each other).
- `piped: true`: jobs run in order and **stop at the first failure**. Good
  for dependent steps like `db:create` → `db:migrate` → `db:seed`, or
  install-then-run pipelines. Cannot be combined with `parallel: true`.
- `priority: <n>` on a job orders it within a sequential/piped run (lower
  runs first; unset/`0` means "run last"). Only meaningful when not
  parallel.

Both settings exist at the hook level and inside a `group:` (so you can
nest, e.g. a piped migration group running alongside other parallel jobs —
see `references/configuration.md#group` for the pattern).

## Conditional execution: `skip` / `only`

Both accept: `true`/`false`, `rebase`, `merge`, `merge-commit`, `ref: <branch-glob>`,
or `run: <shell command>` (skip/only if it exits 0). `only` is the inverse
of `skip` — think "run only when"; if both match, `skip` wins.

```yml
pre-commit:
  commands:
    lint:
      skip: [merge, rebase]     # don't lint during a merge or rebase
    lint-quick:
      only: rebase              # ...but do run a faster check then
```

`skip: true` on a shared config's job is the standard way to disable it
from `lefthook-local.yml` without touching the shared file (see below).

## Filtering by tag

Tag jobs/commands with `tags:`, then exclude a whole tag at run time without
editing the config:

```yml
pre-push:
  exclude_tags: [frontend]   # or: LEFTHOOK_EXCLUDE=frontend git push
  commands:
    eslint: { tags: [frontend], run: yarn eslint . }
    rubocop: { tags: [backend], run: bundle exec rubocop }
```

Or scope a single run to specific jobs/tags: `lefthook run pre-commit --job lint --tag security`.

## Local overrides (`lefthook-local.yml`)

Add `lefthook-local.yml` to a personal/global gitignore and use it to
override the shared config per-developer — wrap a command in Docker, disable
a flaky check, tweak `PATH`/env, or add hooks the rest of the team doesn't
need. Jobs with the same `name:` merge by name; unnamed jobs just append.

```yml
# lefthook-local.yml
pre-commit:
  jobs:
    - name: lint
      run: docker compose run backend {cmd}   # wrap the shared command
```

## CLI essentials

```bash
lefthook install          # (re)generate .git/hooks/* shims from config
lefthook run pre-commit   # run a hook's jobs without a real git action
lefthook validate         # check config against the JSON schema
lefthook dump             # print the fully-merged config (remotes/extends/-local applied)
lefthook add pre-push -d  # scaffold .lefthook/pre-push/ for a script
lefthook uninstall        # remove lefthook's Git hook shims
```

`LEFTHOOK=0 git commit` skips lefthook entirely for one invocation — the
standard escape hatch when someone needs to force a commit through. Full
command list, flags, and environment variables are in `references/cli.md`.

## Where to go deeper

- **references/configuration.md** — every config key not covered above:
  `remotes`/`extends` (sharing configs across repos), `templates`
  (overridable placeholders), `output`/`colors`, `glob_matcher`,
  `file_types`, `fail_on_changes`, `source_dir`, and more, organized by
  scope (top-level / hook-level / job-level).
- **references/cli.md** — every subcommand (`add`, `check-install`,
  `self-update`, `version`, ...) and every `LEFTHOOK_*` environment variable.

When writing a new `lefthook.yml`, check the project's existing lint/test
commands (package.json scripts, Rakefile, Makefile) rather than guessing —
lefthook just orchestrates whatever commands already work in the repo.
