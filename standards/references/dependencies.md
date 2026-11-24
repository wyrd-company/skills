# Dependencies

Read this when adding, pinning, auditing, updating, reviewing or removing a dependency in a repository: language packages, package managers, runtimes, container base images and CI actions. Every repository also carries `renovate.json`, committed lockfiles and `LICENSES/` as the [repository standard](repository.md) specifies. Not for choosing an application's primary framework ([stack](stack.md)) or installing tools into a devcontainer ([workspace](workspace.md)).

## Choosing and adding

- **Make every dependency earn its keep.** Use the standard library or a small amount of owned code instead of a single-purpose micro-package. Every added package expands audit, upgrade and supply-chain surface.
- **Vet before adding.** Confirm the package is actively maintained, its license is compatible with the repository's [license](repository.md#license) (no unintended strong copyleft such as AGPL or SSPL in Apache-2.0 or MIT projects), and its transitive dependency tree is proportionate to what it provides.
- **One library per job, one major version per graph.** Reuse the dependency the repository already carries for a concern (HTTP, dates, CLI parsing, serialisation) rather than adding a second one. When a change adds a duplicate major version of a shared dependency to the lockfile, inspect the graph (`cargo tree -d`, `pnpm why`, `uv tree`) and consolidate to one version unless an upstream transitive dependency forces the split.
- **Scope dependencies accurately.** Put test, lint, formatting and build-only tools in development or build dependency groups, never in runtime dependencies.

## Pinning and reproducibility

- **Commit lockfiles for applications; keep ranges compatible for libraries.**
  - Applications, services and internal tools commit their lockfile ([repository](repository.md#gitignore)) so every developer and CI run resolves identical packages.
  - Published libraries declare compatible version ranges in their package manifest so downstream consumers can resolve one shared version without conflict.
- **Enforce frozen installs in CI.** Run installations with the ecosystem's lockfile check (`pnpm install --frozen-lockfile`, `uv sync --locked`, `cargo ... --locked`) so manifest-to-lockfile drift fails the build instead of re-resolving silently.
- **Pin the whole build chain.** Reproducibility stops at the first unpinned tool:
  - **Package managers and runtimes:** declare the exact package manager (`packageManager` in `package.json`) and the runtime or compiler floor (`.python-version`, `rust-toolchain.toml`, `engines`, `requires-python`).
  - **Container base images:** pin by digest (`image:tag@sha256:...`), keeping the tag for readability.
  - **CI actions:** pin third-party GitHub Actions to a full commit SHA with a trailing version comment (`uses: owner/action@<40-char-sha> # vX.Y.Z`).

## Supply-chain security

- **Enforce a release cooldown.** Require newly published package versions to soak for 3 to 7 days before Renovate proposes them or a package manager installs them (for example Renovate `minimumReleaseAge` or pnpm `minimumReleaseAge`), so fresh account-takeover and typosquatting releases are caught upstream before landing. Bypass the cooldown only for an urgent security fix, naming the advisory in the pull request.
- **Disable install lifecycle scripts by default.** In JavaScript and TypeScript repositories, block arbitrary `postinstall` execution (`ignore-scripts=true` or pnpm's `onlyBuiltDependencies` allowlist) and allow only packages that compile native code.
- **Audit vulnerabilities and licenses in `task check`.** Run the ecosystem's audit tool (`cargo audit` and `cargo deny`, `pnpm audit`, `pip-audit`, or `osv-scanner`) as part of the repository's [checks](repository.md#automation). When an advisory is unreachable in the repository, record a scoped, time-boxed ignore with the reason and review date rather than suppressing the check globally.
- **Record third-party licenses for included code or assets.** Any vendored or bundled third-party code or asset carries its license file in `LICENSES/` ([repository](repository.md#license)).

## Updating and reviewing

- **Update on a steady, small-batch cadence.** Use the repository's [Renovate configuration](repository.md#files) to group low-risk updates (linters, type definitions, patch releases) on a regular schedule so updates stay small and reviewable instead of accumulating into large catch-up changes.
- **Keep dependency updates isolated.** Land dependency updates in their own commits and pull requests, separate from feature work and refactors, so regressions bisect and revert cleanly.
- **Read release notes; never automerge.** Automated dependency updates are never automerged on green CI alone. Read the upstream release notes or changelog for bug fixes, security fixes, deprecations and behavioural changes before merging.
- **Verify behavioural changes on high-risk majors.** A green test suite proves only what the tests already assert. When a major upgrade touches a library that shapes output (a template engine, serialiser or parser), sits on a security boundary (authentication, cryptography, sandboxing), or formats error text that later passes through redaction or logging:
  - treat the upgrade as high risk during review rather than a mechanical bump;
  - read the upstream upgrade guide and changed defaults;
  - compare the old and new versions against representative inputs when existing tests do not pin formatting, error messages or edge cases.
- **Document consumer-visible effects.** When a dependency update raises a minimum runtime or compiler version, changes documented behaviour or alters an upgrade step, update the repository's documentation and release-note mechanism in the same change.

## Pruning and lifecycle

- **Remove unused dependencies.** Delete dependencies when the code that used them goes, and check periodically or in `task lint` for orphans (`knip` for JavaScript and TypeScript, `cargo-machete` for Rust, `deptry` for Python).
- **Track end-of-life runtimes and archived upstreams.** When a runtime, framework or direct dependency reaches end of life or is archived upstream, file an issue with its replacement or exit plan rather than waiting for a build break.

## Enforcement

Prefer an automated check over a review habit ([instructions](instructions.md#every-instruction)):

| Rule | Enforced by |
|---|---|
| Lockfile freshness and reproducibility | CI (`--frozen-lockfile` / `--locked`) |
| Release cooldown, update grouping, SHA-pinned actions and image digests | Organisation Renovate preset ([`renovate.json`](../assets/repository/renovate.json)) |
| Blocked install lifecycle scripts | Repository package-manager configuration (`.npmrc` or `pnpm-workspace.yaml`) |
| Vulnerabilities and disallowed licenses | `task check` / CI (`cargo deny`, `pnpm audit`, `pip-audit`, `osv-scanner`) |
| Unused dependencies | `task lint` or scheduled cleanup (`knip`, `cargo-machete`, `deptry`) |
| Release-note and behavioural review | Pull request review |
