---
name: reporting
description: >
  Use when someone asks you to explain something, walk them through code or a change, or write a report, brief, summary, presentation or deck. Covers fitting the form to the reader and the question, choosing visuals, checking claims and figures, and delivery: in the thread, Postplan, a page served from this workspace, Discord and the public assets bucket. Not for a pull request's handoff (`executing`), a design document (`designing`), or documentation that ships with a repository (`standards`).
---

# Reporting

A report exists so that one reader can understand something or decide something. Work out who that reader is and what they need to understand or decide. The format comes after that.

## Before you write

- **Name the reader and the question.** The reader is the person who asked, unless they name someone else, such as a manager reading a brief. The question is what that person needs to understand or decide. When the request leaves the reader unclear and the right depth depends on it, ask.
- **Pitch it to what the reader knows.** When the reader is an operator, their profile says what they know and how they want to be told. A colleague in the code can follow file names and internal terms. A manager or a newcomer gets plain words, a definition the first time a term appears, and a link to anything they would need to open.
- **Assume the reader has none of your context, even when they asked.** You have read files, memories, logs and tool output that the reader has not seen. A reader who comes back after an hour has forgotten most of the thread, including what you told them. Open with where things stand: what the work is, what has happened since they last looked, and what you need from them. Before you refer to a file, a memory, a term, an earlier decision or an option you offered, say what it is. "The earlier fix" and "option B" mean nothing to a reader who has lost the thread.
- **Find the facts before you write about them.** Read the code, run the command or open the source. A claim about how code behaves comes from reading or running it, not from a function's name, a comment or memory.

## Shape

- **Lead with the answer.** Put the conclusion, the recommendation or the decision you need first, in one or two sentences. Then give what supports it, in the order the reader needs it.
- **Use the smallest form that makes the point clear.** Use one default and move up a step only when the step below leaves the point unclear:
  1. prose, a list or a table;
  2. a text figure in the message: pseudocode, a call tree, a file tree or a diff;
  3. a diagram, in Mermaid or SVG;
  4. an HTML page, when the reader needs to compare variants side by side, step through state, or try a parameter;
  5. a deck, when the reader asked for slides or will present the material.
- **Give every figure one job,** and put it next to the sentence it supports. Show only the calls, files, states and boundaries the question needs. A figure that only decorates the page gets cut.
- **Cite what you describe.** Link each file at the line you mean, each pull request and issue, and each outside source you used.
- **Keep observations apart from conclusions.** Say what you saw and what it rests on. A check you did not run is named as unverified.

## Check before delivery

Every factual claim and every figure must be supported by a source you opened in this session. That covers numbers, names, dates, quotes, the order of events, and statements that X does Y or causes Y. For each one, open the source and read the passage, or the code at the line you cite. If the source supports the claim, keep it. If it says something different, correct the claim. If nothing supports it, cut it. Interpretation is allowed when it is labelled as interpretation.

Check figures the same way: every arrow, call and state in a diagram exists in the code or the source. Open a rendered page and look at it before you hand it over. Text that shows only in one colour also needs a label. You are done when every checkable claim and figure traces to a source and the rendered output has been seen.

Then reread the prose once for length. Cut filler, restatements and inflated claims. Do not change what the text means.

## By case

Read the reference for the case in front of you:

- **A short explanation in the thread:** [Text figures](references/text-figures.md) covers the inline forms and the diff variants.
- **Explaining code or a system:** [Walkthroughs](references/walkthroughs.md) covers tracing one path through real code.
- **Explaining a change, such as a pull request, a diff or a proposal:** [Changes](references/changes.md) covers grouping by purpose, reading order, and before-and-after.
- **A report or brief for someone outside the work:** [Briefs](references/briefs.md) covers the structure of a brief and what a manager needs from it.
- **A diagram that has to stand on its own:** [Diagrams](references/diagrams.md) covers choosing the type and keeping it legible.
- **An interactive page:** [Interactive pages](references/interactive.md) covers when interactivity earns its place and how to build the page.
- **A presentation or deck:** [Decks](references/decks.md) covers the deck source and its build script.

## Delivery

Deliver in the thread unless the reader needs the report somewhere else. When it goes elsewhere, use the first channel below that fits, and give the reader the URL:

| The reader needs | Deliver through |
|---|---|
| To read it in the thread | Your reply. Use the harness's preview tool for HTML or images when it has one |
| A link to a static page or deck, outside the thread | [Postplan](references/postplan.md) |
| A page that runs code, reads live data from this workspace, or is too large for Postplan | [A page served from this workspace](references/workspace-site.md) |
| An image, recording or file to embed in GitHub, Postplan or Discord | The [`public-assets` skill](../public-assets/SKILL.md) |
| A notice that the report is ready, or an answer about it | Discord, through the [`contact` skill](../contact/SKILL.md). Link the report from the message |

Everything delivered outside the thread can be read by someone other than the person you are working with. It must contain no secrets, tokens, private URLs or local file paths.
