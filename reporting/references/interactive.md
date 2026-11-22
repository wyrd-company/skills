# Interactive pages

Read this when you are building an HTML page, such as an explainer or a comparison, that the reader will use, not only read.

## When it earns its place

Make a page interactive only when the interaction is the explanation:

- **stepping** through a process or a state machine one step at a time;
- **switching** between variants that differ in a few places, such as mocks, before and after, or options A to E;
- **tuning** a parameter and watching the result change;
- **filtering** a table or a graph too large to read whole.

Otherwise, write a static page. It loads anywhere, prints, and survives in an archive. A report must still read correctly with its scripts off: put the conclusion and the evidence in the HTML, and let scripts add to them.

## Plan before you build

For a page with more than one figure, write the outline first. List each section in one line, and for each figure say what it shows and what the reader does with it. Show the outline to the person who asked before building, because changing the outline is cheap and changing the page is not. Every figure must pay off something the text has just set up. Three to five figures is usually enough.

## Build

- **Make it one self-contained file,** with CSS and JavaScript inline and no framework or build step. Postplan blocks external scripts, and a single file can be delivered through any [channel](../SKILL.md#delivery). When the page has to load a library or live data, serve it from [this workspace](workspace-site.md) instead.
- **Keep state in closures or in `location.hash`,** so a link can open a particular step or variant. Postplan's sandbox has no storage or network access.
- **Label every control,** make it reachable by keyboard, and make it respond visibly.
- **Lay it out for desktop and mobile widths.** Figures scroll sideways on narrow screens instead of shrinking until they are unreadable.
- **Follow the [interface standard](../../standards/references/interface.md)** for layout, type, colour and motion. When the page mocks part of a product, use that product's look as its `DESIGN.md` records it.
- **Label variants `A`, `B`, `C`...** so the reader can answer with a letter. Keep one file across rounds, so the URL stays the same.

## Check

Open the page in a browser before delivery. Every figure must render without console errors, every control must work, and the layout must hold at a phone width. Then check the claims and figures as [the skill says](../SKILL.md#check-before-delivery).
