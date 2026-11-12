# Start

Read this when you have been handed an epic and its task is not claimed yet. It sets up what every later pass and every event depends on: the claim, the epic branches and pull requests, and the schedule.

The workspace manager hands you the epic in the thread that will run its passes.

1. **Claim the epic task with this thread,** as in [task-ownership](../../task-ownership/SKILL.md), and move it to `in-progress`. Every pass runs in this thread, so the claim holds across them.
2. **Open the epic branch and its pull request.** In each repository the epic touches, create the epic branch from the current default branch, push it, and open a draft pull request into the default branch. GitHub needs a commit to open one: start the branch with an empty commit. The description states the outcome, links the issues, and has an empty **What landed** section. People watch this pull request as the work lands. Set up a repository the epic reaches later the same way, before its first dispatch. When the **Target branch** section names the default branch instead, there is no epic branch or epic pull request: children merge into the default branch, and the default branch is what you record below.
3. **Create the schedule** that runs the passes: bound to this thread, a fresh session for each run, a cheap model from [models.yml](~/models.yml), and an interval of a few hours as the backstop. Its prompt:

   ```text
   Run a pass of epic task <id> on board <dir>, with the epic-orchestration skill.
   ```

4. **Register the epic for events.** Record the schedule's id, the epic branch and the repositories on the epic task. The devcontainer's [event path](devcontainer.md) finds the epic by these, and only while it is `in-progress` or `review`.
5. **Release the children** from `backlog` to `todo` as the epic's pattern calls for them.

```bash
kanban-md move "$EPIC" in-progress --dir "$BOARD" --claim "$THREAD"
git commit --allow-empty -m "chore: start epic <name>"
kanban-md edit "$EPIC" --dir "$BOARD" --claim "$THREAD" \
  --set-property schedule='"<schedule id>"' \
  --set-property branch='"<epic branch>"' \
  --set-property repos='"<owner>/<repo>,<owner>/<repo>"'
kanban-md move "$IDS" todo --dir "$BOARD"
```
