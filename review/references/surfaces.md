# Surfaces

Read this to check, comment on and decide a review surface. The task's **Review** section names the surface when it is not the repository's usual one. Public repositories review on GitHub, so the findings stay visible on the public change. Private ones may use `gitpr`, which keeps the review in the local repository.

Whatever the surface, findings go on it, anchored to their lines. A finding only in the handoff or in chat cannot be replied to or tracked across rounds. Never mention the task, the board or agent threads on a GitHub surface: its readers may not have them.

## GitHub pull request

### Check the surface

```bash
gh pr view $PR -R $REPO --json number,url,isDraft,headRefOid,baseRefName,reviewDecision,statusCheckRollup
git fetch origin
git rev-parse "origin/$TASK_BRANCH" "origin/$BASE"
git merge-base --is-ancestor "origin/$BASE" "origin/$TASK_BRANCH" && echo base contained
```

`headRefOid` must equal the task branch head, and the base must be an ancestor of the branch. Record both heads: every comment and verdict applies to that pair.

### Read the previous rounds

```bash
gh pr-review review view $PR -R $REPO --unresolved --not_outdated
```

Drop the filters when an outdated thread may still be unanswered.

### Comment

Post the round as one review:

```bash
gh pr-review review --start -R $REPO $PR
gh pr-review review --add-comment --review-id $REVIEW_ID --path "$FILE" --line $LINE --body "P1: <problem>. <fix>." -R $REPO $PR
gh pr-review review --submit --review-id $REVIEW_ID --event REQUEST_CHANGES --body "$SUMMARY" -R $REPO $PR
```

Use `--start-line` for a range. The summary opens with the result, the count by severity and the top concern.

- **Rejected:** `REQUEST_CHANGES`.
- **Accepted, or findings that do not block:** `COMMENT`. An agent never submits `APPROVE`. Approval on GitHub is the operator's, so an accepted review ends: `Ready for operator review at <head>.`

### Reply to the previous round

```bash
gh pr-review comments reply $PR -R $REPO --thread-id $THREAD_ID --body "Fixed at <head>: <what you checked>."
gh pr-review threads resolve $PR -R $REPO --thread-id $THREAD_ID
```

Open each reply with its verdict and the head you checked: fixed, still open, rejection accepted, deferral accepted, or answered. Resolve a thread only after you have verified it. If resolving fails for lack of permission, the reply is the record: stop trying, and say once in the review summary that the threads await the pull request's owner.

### Merge

Only with merge authority, and only when the [gates](../SKILL.md#merge) hold. Merge by pushing the reviewed head to the base, fast-forward only, so GitHub closes the pull request as merged:

```bash
git push origin "$REVIEWED_HEAD:refs/heads/$BASE"
```

A push needs the thread's git operator. A refused push is a stop, not something to work around: never force-push.

## `gitpr`

`gitpr` records reviews in the repository. Its commands check the heads for you.

```bash
gitpr review $ID      # the live basis: source_head_sha, base_head_sha, base_contained, verdict_hint
gitpr show $ID
gitpr comments $ID
```

Take the pair from the `basis:` block at the top, or from `verdict_hint`. Threads further down print the older pairs they were anchored to. `base_contained: false` means the base moved: reject the surface.

```bash
gitpr comment $ID --file "$FILE" --line-start $LINE --line-end $LINE --side new --text "P1: <problem>. <fix>." --basis "$SOURCE:$BASE"
gitpr comment $ID --thread $THREAD --text "Fixed at <head>: <what you checked>." --basis "$SOURCE:$BASE"
gitpr resolve $ID $THREAD
gitpr reject $ID --basis "$SOURCE:$BASE"
gitpr approve $ID --basis "$SOURCE:$BASE"
gitpr merge $ID
```

Use `--text-file` for text with backticks or several lines, and `--pr-level` for a finding with no line.

`approve`, `reject` and `merge` are separate steps. `approve` records the verdict and refuses if either head has moved. `merge` merges the head recorded at approval, so check the base yourself just before it. Leave `--cleanup` off: the executor removes its worktree and branch.

## No pull request

For a branch, a commit range or uncommitted work, write the findings in the handoff, ordered by file and line, as `path:L<line>: P1: <problem>. <fix>.`, so they can move to a surface later.
