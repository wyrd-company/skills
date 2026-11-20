# Dependencies

Read this when the survey's **Dependency updates** section lists open Renovate pull requests. Renovate opens them; nothing merges them on its own. Each one is read against the release notes of what it updates before it is merged, because a version bump can carry a fix the workspace needs to know about, a security fix, or a breaking change that passing CI does not catch.

## Which repositories

The workspace's repositories are the ones made with Toha's repo template: each repo folder `/workspace/<project>/<repo>/` with a `main` worktree, or `fork` for a fork. The repository is the one that worktree's `origin` names. The survey lists them this way and counts each repository once, even when two project folders hold it. Renovate pull requests in other repositories of the organisation belong to the workspaces that hold those repositories.

## Dispatch the updates

Dispatch one delegate for each repository with open updates, and at most one at a time for a repository: each merge changes the lock files, and Renovate rebases the rest after it. The manager task's **In flight** section lists the repositories that have one: skip those. A delegate counts against the thread limit and the budget, as any dispatch does, and a repository with a security update goes first. Above the pace, list only a repository's security updates in the prompt.

Choose the model from [models.yml](~/models.yml): the cheapest entry that lists `low` complexity. Reading release notes and fixing a failing check is narrow work. Send it with `delegate_task`, listing the pull requests from the survey:

```text
Work through the open Renovate pull requests in <owner>/<repo>, security updates first, then oldest first: <numbers>.

For each one, read the release notes and the changelog of every dependency it updates, from the version the repository uses now to the new one. Note the bug fixes and security fixes that concern how this repository uses it, and every breaking change. For a breaking change, check the code that uses what it changes.

When its checks fail, fix them on the pull request's branch, with the smallest change that makes them pass. Merge it, with a merge method the repository allows, when its checks pass and nothing in the notes calls for more than that fix. Otherwise leave it open, and comment on it with what holds it. When a later pull request conflicts after an earlier merge, leave it for Renovate to rebase.

Return, for each pull request: merged or held, and why when held, and the notes worth knowing: the bug fixes and security fixes that concern us, and the breaking changes. Copy the git operator from thread <your thread id>.
```

Add a line to the **In flight** section, with the repository and the delegate's thread, and log the dispatch.

## When the report comes back

- **Remove the repository's line from In flight.**
- **Log what merged and what was held,** in one entry for the repository.
- **Tell the operators what is worth knowing,** in [the channel](../SKILL.md#the-channel): a security fix, a bug fix the workspace may have been hitting, or a breaking change. One post for the report, not one for each pull request. A report with nothing worth knowing posts nothing.
- **A held update goes to the operator** with what holds it, once, as [authority](../SKILL.md#authority) says. Leave it out of later dispatches until the operator answers, and record it in the **Holds** section. A later Renovate pull request for the same dependency replaces it.
