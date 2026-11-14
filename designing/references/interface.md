# Interface

Read this when the design shapes what a person sees and operates: a web application, a site, a native application, or a terminal tool. The rules the result is held to are in the [interface standard](../../standards/references/interface.md).

## The person and the scene

Start from the [persona](product.md#jobs-and-people) and the job, then the scene of use: where the person is, on what device and screen, how often and for how long, how expert they are, and what else holds their attention. Write the scene into the frame. An interface that suits another scene fails in this one.

Then name what success is on each surface. It sets how much the design expresses and how much it recedes:

- **Work:** the person completes a task, often many times a day. Application screens, dashboards, editors, administration, settings and terminal tools. Speed, scanning, consistency and the conventions the person already knows come before expression. Identity shows in precise details.
- **Persuade:** the person decides and acts. Landing, product and pricing pages. The design carries the message, so it commits to a distinct point of view.
- **Read:** the person understands something. Documentation, guides and changelogs. Structure serves comprehension first, then comfort over a long read.
- **Show:** the person looks at the work itself. Portfolios, galleries and demonstrations. The work leads, and the interface recedes.

Name it per surface, not per product. A tool's landing page persuades, and its documentation is read.

## Structure before look

Decide what the interface is made of before how it looks.

- **The domain is the map.** The things a person sees and acts on are the [domain model](documents.md#which-document)'s, named by its terms. A thing has one name on every screen, in every message, in the documentation and on the command line.
- **Navigation shows place and scope.** At every point the person can see where they are, what they can reach, and what an action will affect.
- **One layout for each kind of screen.** Choose how each kind of screen is laid out (a table or list, a board, master and detail, a canvas, a dashboard, a feed, a form or a guided sequence) and use the same one wherever that kind recurs.
- **Flows have a way back.** Walk the path through the job, step by step. Every step can be left or undone. An action that cannot be undone asks for confirmation, and says what it will destroy.
- **Every state is designed:** empty (first use, and no results), loading, partial, failed, stale or offline, done, and with too much content as well as too little. A state left out of the design is designed by accident in code.

## The visual language

A product has one visual language: its colour, type, spacing, shape, elevation, components and motion. It is recorded in `DESIGN.md`, in the [DESIGN.md format](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md). The tokens in its front matter are normative, and its sections say how to apply them.

- **It sits at the repository root,** or in the product repository when several components share it.
- **Tokens have one source.** When the code keeps its own token file, one of the two is generated from the other, and both change in the same work. `npx @google/design.md export` writes Design Tokens JSON and Tailwind themes.
- **Lint it** with `npx @google/design.md lint DESIGN.md`. A broken reference is an error. A contrast warning is a failed accessibility check, not a style note.

### Refine or replace

Read what exists first: `DESIGN.md`, the tokens, the components and the rendered screens. A missing `DESIGN.md` does not make a product new.

- **A refinement keeps the incumbent:** its identity, its behaviour, its copy, and everything outside the scope.
- **A redesign replaces the language,** and `DESIGN.md` with it. It keeps the product's content, functions and platform conventions. The old look is evidence of what failed, not a base to polish.

### A new language

A new visual language comes from the product: its people, its scene, and what success is on its surfaces. It does not come from a framework's defaults or from the habits of generated interfaces. Identity is a decision about the goal, so it is the operator's. Present two or three directions as rendered [prototypes](charting.md), with your recommendation. When the operator has given an aesthetic, an era, a font or a palette, it holds even where you would choose otherwise.

### By platform

- **Native applications** follow the platform's conventions: Apple's Human Interface Guidelines, Material Design, or Windows' Fluent. The visual language shows through tokens and details, not through controls reinvented.
- **Terminal tools** keep a small language: a few colours, each with one meaning, that read on light and dark terminals and that the output does not depend on. The command line itself is a contract: a `specification`, with its definition in the ontology's [CLI command specification](https://github.com/wyrd-company/refinery-ontology/blob/main/realization/design/cli-command-specification.json) format. A terminal tool needs a `DESIGN.md` only when it shares a language with a graphical surface.

## References set the bar

Collect real screens that do what this interface must do well: from the product's own best surfaces, from products its people already use, and from collections of real product screens. For each, write down what to take from it: the layout, the type, the spacing, the density, a piece of interaction. Each one is the floor the work must reach, not something to copy. Take from several, and never another product's identity.

The references and what to take from each are linked from the `feature` or the decision they shape. They become the reference shots the built interface is compared against ([standard](../../standards/references/interface.md#proving-it)).

## Prototype to decide

How an interface should look or behave is a [prototype](charting.md) question. Render the variants and look at them at the sizes they will ship at, side by side. Show the operator what the decision is between. A prototype is thrown away: it is linked from the decision, and never merged.

## Where it lands

| Decision | Document |
|---|---|
| Who uses it, and the job they are doing | `persona`, `job-to-be-done` |
| What a person can do: the flows, the rules, and a scenario for each state that matters | `feature` |
| What each thing is called | `term` |
| The visual language and its tokens | `DESIGN.md` |
| A command line: its commands, options and output | `specification` |
| How the interface is built: its components, its state, how data reaches it | `technical-design` |
| A real trade-off, such as one theme only | `decision-record` |

Mockups and prototypes are not design documents. The decision links to them. Once the interface is built, the built screens and `DESIGN.md` are how it looks.
