# Changes

Read this when the reader needs to understand a change: a pull request, a diff, a branch, or a change you are proposing.

## A change that exists

1. **Summarize its purpose in a few sentences:** what it does, and why. Say what a reviewer should look at most closely.
2. **Group the files by purpose,** not by directory. A group is the files that together do one thing, such as "move session storage behind an interface". Give each group a title that says what it does.
3. **Order the groups so each one can be read with only the groups before it.** Put types and interfaces before the code that uses them, and the core change before its call sites and tests.
4. **For each group, list its files and what changed in them.** Name every change to a public interface, a stored data shape or observable behaviour, because those are what a reviewer must check. Say when a group is mechanical, such as a rename or formatting, so the reader can skim it.
5. **Draw a figure only where the change alters an interaction, a state transition or a data flow.** Show the part the change touches, before and after. A [shape diff](text-figures.md#diffs-of-a-shape) is often enough.

You are done when every changed file appears in a group and every public-interface change is named.

## A change you propose

Give each candidate:

- the files and modules it touches;
- the problem: what is hard or fragile today, with an example;
- the change, in plain words;
- what it buys, such as fewer places to change, a smaller interface or tests that can reach the behaviour;
- a before-and-after figure of the shape that changes;
- how strongly you recommend it: `Strong`, `Worth exploring` or `Speculative`.

When a candidate contradicts a recorded decision, such as an ADR, include it only when the problem is real enough to reopen that decision, and say so on the candidate. End with the one you would do first, and why.

Use the repository's own words for its domain, as its glossary or documentation uses them.
