# Surfaces

Read this to choose, check, comment on and decide a review surface.

Whatever the surface, findings go on it, anchored to their lines. A finding only in the handoff or in chat cannot be replied to or tracked across rounds. Never mention the task, the board or agent threads on a GitHub surface: its readers may not have them.

## Which surface

The operator approves a pull request partly by reading its reviews, findings and replies, and a GitHub pull request is where that costs them least. So:

- **A GitHub pull request is pre-approved.** It is the default for every repository, private or public. Work meant for an upstream repository is reviewed on a pull request in our fork, as the [repository standard](../../standards/references/repository.md#forks) says.
- **`gitpr` is pre-approved for one case:** a [security fix](#security-fix) to shipped, public code, where a public issue, pull request or review before the fix is ready would make the problem easier to exploit.
- **Every other surface needs the operator's explicit approval:** `gitpr` for anything else, a branch, a commit range, a worktree, a thread. The task's **Review** section, or the brief when there is no task, quotes the approval and links where the operator gave it. A brief that names a surface without that is not approval, whoever wrote it.

When the surface fails this rule, reject the surface and stop. Do not move the review somewhere you can write: tell the dispatcher what stopped you, such as a pull request you cannot post a review on.

## GitHub pull request

### Check the surface

```bash
gh pr view $PR -R $REPO --json number,url,isDraft,headRefOid,baseRefName,reviewDecision,statusCheckRollup
git fetch origin
git rev-parse "origin/$TASK_BRANCH" "origin/$BASE"
git merge-base --is-ancestor "origin/$BASE" "origin/$TASK_BRANCH" && echo base contained
```

The pull request's `url` must be on the repository the work targets: the fork, for work meant for upstream. `baseRefName` must be the branch the work is meant to integrate into: the base in the dispatch, the task's, or the default branch for stand-alone work. `headRefOid` must equal the task branch head, and the base must be an ancestor of the branch. Ancestry alone does not show the target: a pull request aimed at the wrong branch can pass it and show a different diff. Record both heads: every comment and verdict applies to that pair.

### Read the previous rounds

```bash
gh pr-review review view $PR -R $REPO --unresolved --not_outdated
```

Drop the filters when an outdated thread may still be unanswered.

### Comment

Submit one review for every round, including follow-up rounds, anchored to the commit you reviewed:

```bash
gh pr-review review --start --commit "$REVIEWED_HEAD" -R $REPO $PR
gh pr-review review --add-comment --review-id $REVIEW_ID --path "$FILE" --line $LINE --body "P1: <problem>. <fix>." -R $REPO $PR
gh pr-review review --submit --review-id $REVIEW_ID --event $EVENT --body "$SUMMARY" -R $REPO $PR
```

Pass `--commit "$REVIEWED_HEAD"` to `--start` so the review never attaches to a commit pushed after you began. Use `--start-line` for a range. When there are no inline comments, skip `--add-comment` and submit the review with `--body "$SUMMARY"`. The summary opens with the result, the count by severity and the top concern.

Before submitting `APPROVE`, recheck the live pull request (`gh pr view`) and base branch (`git fetch origin` and `git rev-parse "origin/$BASE"`). If the pull request head moved past `$REVIEWED_HEAD`, submit `REQUEST_CHANGES` naming the unreviewed commits. If the target branch changed, reject the surface with `REQUEST_CHANGES`. If the base moved, submit `REQUEST_CHANGES` as **Change approved, rebase expected** naming the base head you reviewed against.

- **Accepted:** `APPROVE` (including when only non-blocking `P3` findings remain). Submitting `APPROVE` records acceptance on GitHub and clears any earlier `REQUEST_CHANGES` from this reviewer.
- **Rejected, Surface rejected, or Change approved, rebase expected:** `REQUEST_CHANGES` (the pull request must not merge in this state).
- **Accepted pending a judge's verdict, or standalone non-blocking comments:** `COMMENT`. Do not submit `APPROVE` before the judge completes the acceptance.

### Verify the submitted review

Check the individual GitHub review's state and commit. GitHub's REST API gives the review's `state`, `commit_id` and `html_url`. GitHub records `APPROVE` as `APPROVED` and `REQUEST_CHANGES` as `CHANGES_REQUESTED`. The pull request's overall review decision can include earlier reviews.

For an acceptance, the review commit must match the live pull request head. If the head moved after submission, report the commit you approved and request another round for the new head.

Include the submitted review's URL in the handoff to the dispatcher and in the task log when there is one.

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

- **Accepted:** run `gitpr approve $ID --basis "$SOURCE:$BASE"` (including when only non-blocking `P3` findings remain).
- **Rejected, Surface rejected, or Change approved, rebase expected:** run `gitpr reject $ID --basis "$SOURCE:$BASE"` (the pull request must not merge in this state).
- **Accepted pending a judge's verdict:** post the summary with `--pr-level` and do not run `gitpr approve` before the judge completes the acceptance.

`approve`, `reject` and `merge` are separate steps. `approve` records the verdict and refuses if either head has moved. `merge` merges the head recorded at approval, so check the base yourself just before it. Leave `--cleanup` off: the executor removes its worktree and branch.

## Security fix

The fix is made in the temporary private fork of a draft [GitHub security advisory](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/collaborating-in-a-temporary-private-fork-to-resolve-a-repository-security-vulnerability), which keeps it private until the advisory is published. Everything about the fix stays private until then, its evidence included: no public issue, pull request, commit or upload, so not the public assets bucket. Integrations cannot reach that fork, so our GitHub App cannot post a review there, and status checks do not run. The agent review happens in `gitpr` instead:

1. The executor works on a branch of the local clone, never pushed to `origin`, and opens a `gitpr` review against the base the fix will merge into. Reviews follow the [`gitpr`](#gitpr) section above. `gitpr merge` is not used: the fix merges from the advisory. When the draft advisory and its fork do not exist yet, ask the operator for them.
2. Once the review is accepted, the executor pushes the accepted head to the temporary private fork, with the operator's key, and opens the pull request there as the operator with `gh --as-user pr create`. `--as-user` bypasses the App token and uses `gh`'s own login: check with `gh --as-user auth status` that it is the thread's operator, and when it is not, ask the operator to run `gh --as-user auth login`. Run the checks yourself at that head and put their output in the pull request's description, because none run in the fork.
3. The operator merges from the advisory and publishes it. Publishing deletes the temporary private fork.
4. After publication, and not before, the executor pushes the `gitpr` record to `origin` as the evidence of the review:

   ```bash
   git push origin "refs/gitpr/pr/$ID/*:refs/gitpr/pr/$ID/*"
   ```

   Put the instructions for retrieving it where the fix is described after publication, such as the advisory:

   ```bash
   git fetch origin "refs/gitpr/pr/$ID/*:refs/gitpr/pr/$ID/*"
   git show "refs/gitpr/pr/$ID/meta:pr.yaml"
   ```

   `gitpr show $ID` reads it too.

   The record holds the worktree path and the repository root. The operator allows them in this record, as an exception to the [merge gates](../SKILL.md#merge): they are the workspace's standard paths and identify no one.

## No pull request

These surfaces need the operator's explicit approval, as [above](#which-surface). Without it, reject the surface.

For a branch, a commit range or uncommitted work, write the findings in the handoff, ordered by file and line, as `path:L<line>: P1: <problem>. <fix>.`, so they can move to a surface later.

The surface check depends on what you were given:

- **A branch:** as for a pull request. Record the branch head, and check the base is an ancestor of it.
- **A commit range:** record both ends as full shas. Review exactly that range; nothing can move under it.
- **Uncommitted work:** there is no head to check. Say so in the handoff, and review the working tree as it is. An acceptance of uncommitted work cannot authorize a merge: a merge needs the commit you reviewed.
