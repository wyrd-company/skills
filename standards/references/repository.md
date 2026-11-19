# Repository

Read this when creating a repository, adding or reviewing one of the files every repository has, or bringing a repository or a fork up to the standard. It applies to every git repository we own, public and private. The repository's own `AGENTS.md` and docs win over it for that repository.

Most files below have a template in [`assets/repository/`](../assets/repository/). Copy it to the path in the table, and fill in every `{slot}`. In a Markdown template, the `<!-- -->` comments tell whoever fills it in what each section holds, and when to leave one out. A finished Markdown file has no `{slot}` and no `<!-- -->` comment left from its template. A configuration template keeps its comments, drops the lines and tasks that do not apply to the repository, and has no `{slot}` left.

## Files

| File | When | Template |
|---|---|---|
| `README.md` | Every repository | [`README.md`](../assets/repository/README.md), or [`README-monorepo.md`](../assets/repository/README-monorepo.md) for a repository with several components |
| `AGENTS.md` | Every repository, at the root; in a folder when it pays, as [below](#agentsmd-in-a-folder) | [`AGENTS.md`](../assets/repository/AGENTS.md), [`AGENTS-folder.md`](../assets/repository/AGENTS-folder.md) |
| `CONTRIBUTING.md` | Every repository | [`CONTRIBUTING.md`](../assets/repository/CONTRIBUTING.md) |
| `LICENSE` | Every public repository. A private one may have one. | The license's own text, as [below](#license) |
| `.gitignore` | Every repository | None, as [below](#gitignore) |
| `.gitattributes` | Every repository | [`gitattributes`](../assets/repository/gitattributes) |
| `.editorconfig` | Every repository | [`editorconfig`](../assets/repository/editorconfig) |
| `Taskfile.yml` | Every repository | [`Taskfile.yml`](../assets/repository/Taskfile.yml), as [below](#automation) |
| `.config/lefthook.yml` | Every repository | [`lefthook.yml`](../assets/repository/lefthook.yml), as [below](#automation) |
| `renovate.json` | Every repository, at the root | [`renovate.json`](../assets/repository/renovate.json) |
| `.devcontainer/devcontainer.json` | Every repository | None yet |

Each file has one job, and the files point at each other instead of repeating it:

| File | Its reader | It holds |
|---|---|---|
| `README.md` | A person deciding whether to use it, and then using it | What it is, how to get it, and how to start |
| `CONTRIBUTING.md` | A person changing it | How to propose a change, set up, and check the change |
| `AGENTS.md` | Every agent working in it, on every turn | What an agent gets wrong without being told |

## README.md

The README is the front door for people. It is often the only file they read, and package registries show it without GitHub's tabs around it.

- **The opening line says what it is,** in the same words as the repository's GitHub description.
- **Installation covers every way to get it,** each with its command.
- **The quickstart runs.** Copy its example into a clean environment and it works as written.
- **An interface gets a demo.** A command line, a terminal UI or an app shows an animated recording near the top. Commit the script that records it, such as a VHS `.tape`, so the demo is regenerated rather than going stale.
- **Prerequisites appear only when they are not obvious:** a runtime that is not bundled, an external service, a key. A tool with none has no prerequisites section.
- **Credits name what it builds on:** the upstream of a fork, projects that inspired it, and its major dependencies.
- **No license or contributing section.** GitHub shows `LICENSE` and `CONTRIBUTING.md` as tabs, and registries read the license from package metadata.

A README in a folder says how to use what is in that folder. Give a folder one only when its content is not obvious from its names.

## AGENTS.md

`AGENTS.md` is the front door for agents. How it is worded, and what belongs in it rather than in a skill or memory, is in the [instructions standard](instructions.md#agentsmd). Everything in it is paid for on every turn of every agent working there, so it holds what an agent cannot find by reading the repository. A line an agent could learn by reading the code, the `--help` or the configuration gets deleted.

- **Why this exists and Outcomes come from the person who owns the repository.** Draft them from what you know, and the owner approves them, or ask the owner when you have little context. These sections record the owner's decisions, so an agent never invents them.
- **The glossary is the shared vocabulary.** Every repository names the core terms of its domain, and the code, docs, interface and conversation all use them. Each term is defined once, as a `term` in `docs/terms/<slug>.yml`, as [designing](../../designing/references/documents.md#which-document) describes. The glossary lists each term with a one-line meaning and links to its definition. A term that spans several components of a product is defined in the product repository, and the glossary links there.
- **Thar be Dragons holds only what a check cannot catch.** First try to prevent the failure with a linter, a hook or a test. Write it here only when it can't be automated, and keep it short.
- **The tree in Orient shows what is not standard.** Leave out the standard files and directories in this document. In a repository's root `AGENTS.md` the tree may go several levels deep, chosen selectively. A component's root `AGENTS.md` inside a monorepo goes one level deep.

### AGENTS.md in a folder

An `AGENTS.md` in a folder is loaded every time an agent works there, while reading the folder costs an agent only when it needs to. Add one when the folder is complex enough that learning it by reading files is expensive, or when it holds a trap an agent must always know about. It has only Orient and Thar be Dragons.

## CONTRIBUTING.md

Every repository has its own, because how a change is set up and checked differs between repositories. It covers how to report an issue, how to propose a change, how to set up the development environment, and how to run the checks. The commands it gives are the repository's tasks, such as `task test`. It does not copy what they run.

## LICENSE

A public repository without a `LICENSE` is all rights reserved, and nobody may legally use, fork or contribute to it.

| The repository | License |
|---|---|
| Carries one of our brands, or embodies an idea of its own | Apache-2.0 |
| Is simple plumbing with no branding, such as a package tap or a wrapper | MIT |
| Is a specification or schema meant to be implemented as written | CC0-1.0 |
| Holds data or information rather than code | CC-BY-4.0 |
| Extends another ecosystem | That ecosystem's usual license |
| Is a fork | The upstream's license |

- **Apache-2.0 is the default.** It grants patent rights explicitly, licenses contributions on the same terms as the project, so outside pull requests need no contributor agreement, and grants no trademark rights.
- **One license, never `MIT OR Apache-2.0`.** Under a dual license the user picks MIT, and the patent grant and trademark terms are lost.
- **A published package declares its license in its metadata,** such as the `license` field of `package.json` or `Cargo.toml`. Registries read the metadata, not the file.
- **Plumbing says what its license covers.** The README of a tap or a wrapper says that the license covers the packaging, not what it installs.
- **Third-party licenses go in `LICENSES/`,** one file for each component whose code or assets the repository includes, named for the component and its license, such as `Microsoft-devcontainers-features-MIT.txt`.

## Automation

Task runs everything. Every command a person or agent runs in the repository is a task in `Taskfile.yml`, from [Task](https://taskfile.dev). CI, hooks, `CONTRIBUTING.md` and `AGENTS.md` call the tasks, so how anything runs is defined in one place.

The same task name means the same thing in every repository, so anyone can work in one without reading its `Taskfile.yml` first:

| Task | Does | When |
|---|---|---|
| `default` | Lists the tasks | Every repository |
| `test` | Runs the full test suite | Every repository |
| `lint` | Checks the code, formatting included, and changes nothing | Every repository |
| `format` | Rewrites files to the repository's formatting | Every repository |
| `check` | Runs everything CI runs: the one command to run before pushing | Every repository |
| `build` | Produces what the repository delivers | When it delivers an artifact: a package, a binary, an image, a site |
| `dev` | Runs it locally, rebuilding on change | When it runs: a site, an app, a service |

A repository with nothing else to check still lints its Markdown and YAML. Other tasks are the repository's own; name them for what they do.

**A monorepo's root `Taskfile.yml` includes each component's.** The root has every task in the table, running the components' tasks. Each component's `Taskfile.yml` sits in its folder. Every include sets `dir:` to the component's folder, because without it the component's tasks run from the root, and tests that depend on their working directory fail or pass for the wrong reason. The include's name is the component's name, so `task <component>:test` runs one component's tests.

**Lefthook runs the git hooks,** from `.config/lefthook.yml`, through [Lefthook](https://lefthook.dev). A hook calls a task, not a raw command.

| Hook | Runs |
|---|---|
| `pre-commit` | `format`, adding what it changes to the commit, and `lint` |
| `commit-msg` | `lint:commit-msg`, which checks the message follows [Conventional Commits](https://www.conventionalcommits.org) |

No `pre-push` hook. A slow hook teaches people to pass `--no-verify`, which skips every hook. CI runs `check` on every pull request, and is the gate.

## .gitignore

Start from the ignore file for the repository's stack in [github/gitignore](https://github.com/github/gitignore), and add the repository's own build output and local files. Every file a person or tool creates locally and nobody else needs, such as environment files, caches and editor state, is ignored. Lockfiles are committed.

## Layout

| Path | Holds |
|---|---|
| `docs/` | The project's documentation. Design documents go in the folders [designing](../../designing/references/documents.md#where-it-goes) gives. Published documentation for users and developers lives in `docs/user/`, grouped in navigation by audience and page kind as the [user documentation standard](user-documentation.md#audiences-and-navigation) gives. |
| `docs/terms/` | The glossary's terms |
| `tests/` | Tests, unless the stack expects them somewhere else, such as Go's files beside the code |
| `scripts/` | Python scripts the repository runs for itself |
| `LICENSES/` | Third-party licenses |
| `DESIGN.md` | A product's visual language, as [designing](../../designing/references/interface.md#the-visual-language) describes |
| `CHANGELOG.md` | The release history, written by the release tooling. Nobody edits it by hand. |

## Forks

A fork is kept to send changes upstream, kept to track upstream with additions of its own, or made to diverge from upstream on purpose.

- **A fork that sends changes upstream follows upstream's standards,** not these. Follow its `CONTRIBUTING.md` and documentation. Where they are silent, follow the practice its code, issues, pull requests and documentation show. The description of each pull request you send upstream lists the unwritten conventions it follows and where each was observed.
- **A fork that tracks upstream carries its additions only in the overlay upstream provides for them,** and takes upstream's changes by rebase. The workspace repositories are forked this way: see [Workspace](workspace.md#a-workspace-on-forks).
- **A fork that diverges meets this standard.** Change what contradicts it when the change is cheap and safe. Otherwise open an issue for each gap.
