# Commandline Interfaces

- Unless it is small and self-contained, a CLI with libraries is always a thin-shell around those libraries.
- CLI should always expose a `skill`/`skills` that exposes embedded agent skills.
- Help text must be helpful but not overly verbose.
- There is always a path for agents, even for complicated workflows.
- A TUI/interview for humans when the tool is complicated
- A `--version` that prints the published version _and_ commit SHA for that version when possible.

## Delivery

In general we should strive to make our CLI tools as easy to install as possible, which means [publishing](../publishing/standard.md) to as many targets as possible, only leaving out those that do not make any sense.

- Native package system e.g. [`dotnet`](../publishing/dotnet.md), `go`, [`crates.io`](../publishing/crates_dot_io.md)
- [Homebrew](../publishing/homebrew.md)
- [NPMjs](../publishing/npmjs.md)
- [WinGet](../publishing/winget.md)
- [APT](../publishing/apt.md)/[RPM](../publishing/rpm.md)/[AUR](../publishing/aur.md)
- [Docker](../publishing/docker-hub.md) and [GitHub Container Registry](../publishing/ghcr.md)
- [Release Notes](../publishing/github-release.md)
- [install.sh](../publishing/install_dot_sh.md)