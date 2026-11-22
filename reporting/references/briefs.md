# Briefs

Read this when you are writing a report or brief for someone outside the work, such as a manager, an architect, or an operator who was away. The reader has not followed the thread, the code or the design documents, and may read only the first screen.

## Structure

1. **Title and status.** Name the work in the title. Give one sentence saying where it stands, and a status in words, such as `done`, `blocked` or `needs a decision`.
2. **What the reader needs to do.** List the decision you need, the question to answer or the review to start. Say what happens if they do nothing. Write "nothing" when nothing is needed.
3. **Outcome.** Say what is now true that was not true before, in terms of what a user or the business sees, not the files that changed.
4. **Evidence.** List what shows the outcome is real: a test run, a screenshot, a release, a live check. Link each one.
5. **What changed from the plan.** List where the work departed from its design or task, and why.
6. **Risks and open questions,** each with who owns it.
7. **Next.** Say what happens next and who does it.

Leave out a section that has nothing in it, unless its absence tells the reader something. For example, "no departures from the plan" is worth one line.

## Evidence roles

A brief mixes what was planned, what was built and what was shown to work. Give each claim one of these labels, so the reader can see how far to trust it:

- **Intended:** stated by the design or the task.
- **Built:** visible in the code, configuration or a merged change.
- **Shown:** supported by a test, a release or a live run.
- **Inferred:** your reasoned conclusion, not directly observed.
- **Unresolved:** the evidence is missing or conflicting.

When sources conflict, say so in the brief. Do not pick the version that makes the work look finished.

## Writing for the reader

- Use plain words. Describe a component by what it does before you give its name.
- Link every outside thing you mention: the repository, the pull request, the issue, a page you cite.
- Keep detail behind the summary. On a page, use a short summary followed by sections. In a [deck](decks.md), put an overview slide at the top of each stack and the detail below it.
