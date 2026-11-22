# Diagrams

Read this when a diagram has to stand on its own: in a brief, on a page, or in a deck, where the reader cannot ask what a box means.

## Choose the type by what the reader traces

| The reader needs to follow | Use |
|---|---|
| Messages between parts over time | A sequence diagram |
| Steps and branches of a process | A flowchart, with swimlanes when ownership matters |
| The states of one thing and what moves it between them | A state diagram |
| What depends on what | A dependency graph, arrows pointing at what is depended on |
| Layers and what may call what | A layer stack |
| Stored data and its relationships | An entity-relationship diagram |
| A change to a structure | The same diagram, before and after, side by side |
| Quantities | A chart. The `dataviz` skill covers charts when it is installed |

When two types seem to fit, choose the one that matches the main question. Do not combine two layouts in one figure.

## Ground it in the source

Every box, arrow and label must match something real, such as a module, a call, a table or a state. Search for each relationship before you draw it. Use the code's names, or the domain's names as the repository's glossary gives them. A diagram that shows how the system ought to be, rather than how it is, must say so in its title.

## Keep it legible

- Use one idea per diagram. When it needs more than about a dozen boxes, split it or remove the ones the question does not need.
- Give it a title that states the point, such as "Saves go through the cache before storage", not "Architecture".
- Label every arrow whose meaning is not obvious, and keep the arrows of one diagram to one meaning.
- Never use colour as the only signal. A highlighted path also gets a label or a line style, and text keeps enough contrast in light and dark themes.
- Use motion only to show a change or a path through the diagram, and respect `prefers-reduced-motion`.
- Use system fonts or bundled ones. A diagram must render offline and inside Postplan, which blocks external scripts.

## Formats

Mermaid is quick and diffable, and is the default inside Markdown. Use inline SVG when you need exact placement, annotations or a before-and-after pair. A PNG is for places that render neither. Export it from the SVG and upload it to the [assets bucket](assets.md).
