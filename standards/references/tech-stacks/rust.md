# Rust

## Minimum Rust

- If our dependencies need a new minimum to update to latest, we update ours, especially if that dependency is popular.
- We always use latest _unless_ we are publishing a crate library, then we target minimum needed given our dependencies.

## Dependencies

- `anyhow` for CLIs/Web Servers/Binaries
- `thiserrors` for libraries
- `Tokio` for async
- `Axum`/`Reqwest` for web
- `serde` for serialization. `serde-norway` for YAML
- `Chrono` for time
- `Clap`/`inquire`/`ratatui`/`indicatif`
- `gix` for integrated git operations

## Repos

Our repo layout is standard modern Rust:

- `src/lib|main.js`
- `src/**/` crates
- `**/<module>_tests.rs`: Use when tests become a significant portion of an already large module file.

### Mono repos

We may in mono-repos use `crates/` for Rust sources.