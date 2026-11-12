# Finalize

Read this when the epic pull requests have merged into the default branch, or when acceptance has passed for an epic whose children targeted the default branch. It closes the epic down: it checks that the work is finished, removes what the epic left behind, brings GitHub up to date, archives the board, and stops the schedule.

1. Confirm every child is `done`, or `archived` with the ruling that dropped it in its log, and that every agent has stopped.
2. Delegate the cleanup: fast-forward the local default branch, remove the epic's worktrees, delete the epic and task branches locally and on the remote, settle the threads, and remove scratch files and Docker artifacts.
3. Close the issues whose goal is met. On any other, comment with what remains.
4. Bring the GitHub project up to date.
5. Close the epic task with a final log entry naming the merge commits and pull requests, then commit and push its board.
6. Archive the board, as below.
7. Report to the workspace manager that the epic is finished.
8. Delete the schedule. Do this last: this pass is one of its runs.

## Archive the board

A finished epic's board goes to S3 storage, then leaves the tasks folder, so `epics/` holds only the epics that are running. The archive keeps the board exactly as it was: `kanban-md --dir` can read a copy of it again, and analysis such as ClickHouse reads it from there. Its schema belongs to whatever analyses the boards, not to the epic, so archiving stays a copy.

Copy the whole folder: the task files, `activity.jsonl` and `config.yml`, leaving out kanban-md's `.lock`. It goes to the `workspace-archives` bucket, keyed by the workspace, the project and the epic, with the profile of the same name.

```bash
export AWS_PROFILE=workspace-archives
DEST="s3://workspace-archives/$WORKSPACE/<project>/<epic>/"
aws s3 sync "$BOARD" "$DEST" --exclude .lock --delete
aws s3 sync "$BOARD" "$DEST" --exclude .lock --delete --dryrun   # prints nothing when the archive matches
git rm -r "$BOARD"
git commit -m "chore: archive epic <epic>"
git push
```

`--delete` removes anything under the epic's key that is not on the board, such as a task file a retry renamed, so the archive is the board exactly. Remove the folder only once the dry run prints nothing. If the copy fails, leave the board where it is and escalate: the board is the epic's only full record.
