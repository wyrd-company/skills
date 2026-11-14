# Interface

Read this when building or reviewing an interface a person uses: a web application or site, a native application, or a terminal tool. How an interface is designed, and where its decisions are recorded, is in [designing](../../designing/references/interface.md).

The product's `DESIGN.md` sets its look. These rules are the floor every look keeps. A platform's own guidelines win on that platform where they differ.

## Feedback and control

- **Every action shows a result within a second:** the change itself, or a sign that it is under way.
- **A wait shows what it is waiting for.** Under a second, an inline indicator. Up to a few seconds, a skeleton in the shape of what will load. Longer, progress that measures the real work. Loading shows in the region it affects, not over the whole screen.
- **Nothing is submitted twice.** A control doing asynchronous work shows it, accepts no second press, and keeps its size.
- **Every state has a way out:** a close or cancel on every overlay, a back on every step that keeps what later steps hold.
- **Undo beats confirmation.** An action that can be reversed is, with undo. One that cannot says what it will destroy and how much ("Delete 240 messages"), its button names the action, and cancel has the focus. The most destructive ask for the name of what they destroy.
- **Saving is not confirmed.** Long input saves itself or keeps a recoverable draft, and unsaved changes are marked.
- **Transient news is a toast:** success clears itself after a few seconds, an error stays until dismissed, and one shows at a time. A dialog is only for a decision that must interrupt.
- **Frequent work has fast paths:** keyboard shortcuts for frequent actions, and a command palette where actions are many.
- **Interactive elements keep their size and place** on hover and press. Elements that are not interactive do not respond to hover.

## Accessibility

Interfaces meet WCAG 2.2 at level AA.

- **Contrast:** body text and placeholders at least 4.5:1; large text (24px, or 18.7px bold) at least 3:1; controls, icons and focus indicators at least 3:1 against what is next to them. Measure it rendered, in every state and theme, and over images. A disabled control is exempt, and still has its shape.
- **Colour is never the only signal.** Status, errors, selection and links also carry text, an icon or a shape.
- **Everything works from the keyboard,** in the visual order, with no trap. Focus is always visible, as an outline or a replacement as strong.
- **Overlays manage focus:** focus moves in when one opens, stays inside a modal, and returns to its trigger when it closes.
- **Targets are at least 24 by 24 CSS pixels,** and 44 where there is room: 44 points on iOS, 48dp with 8dp between on Android. A small mark keeps a full-size hit area.
- **Semantics before ARIA:** native elements, landmarks, one `h1` and an ordered outline of headings, `lang` on the page. ARIA only where no element says it: `aria-expanded`, `aria-current`, a labelled `dialog`, `role="status"` and `role="alert"` for live updates.
- **Everything has a name:** an icon-only button, a meaningful image (decorative ones have `alt=""`), a chart (with a table or a text alternative).
- **Text scales:** to 200% without loss or sideways scrolling, and with the person's own zoom, font size, system text size, and a line height raised to 1.5.
- **Reduced motion has its own path:** spatial movement is replaced, and fades and state changes stay. A global switch that zeroes every duration is not that path.
- **Nothing flashes** more than three times a second.

## Names and navigation

- **One name per thing,** from the domain's terms, in the person's words: the same in navigation, titles, breadcrumbs, dialogs, errors, documentation and the command line.
- **Labels name their effect,** with a verb and its object ("Archive project"), in three words at most. A title carries the longer explanation.
- **Navigation is grouped by what the person is doing,** not by how the product is built. Each level groups one way.
- **Place and scope are visible.** The current location is marked by more than colour. Beyond two levels there are breadcrumbs or a named way back; beyond three, search. The person can always tell which record they are editing, and whose account they are acting as.
- **Environments look different.** Staging, internal tools and acting on another's behalf are unmistakable, and a tenant is named by a label.
- **Tabs hold two to seven views of one context.** More becomes a sidebar; a sequence becomes steps. A guided sequence shows progress, makes each step one decision, and summarises before the step that cannot be undone.

## Layout and hierarchy

- **The hierarchy survives a squint:** blurred, the primary element, the secondary and the groups still read in order.
- **Grouping is spacing first:** tight within a group, wide between groups, more above a heading than below. Borders and boxes come after space.
- **Spacing comes from a scale on a 4px base,** in the product's tokens.
- **One primary action per section or step.** The others recede, and a destructive one is set apart.
- **Each surface is separated one way:** a border, a shadow or a fill. Containers nest two deep at most, and cards do not sit inside cards.
- **Density fits the scene.** Work surfaces on a desktop are dense, mobile surfaces are not, and density is reduced by cutting words before shrinking them.
- **Repeated items align** whatever their content: equal sizes from the layout, one slot that absorbs variable length, anchors such as a price or a status in a fixed place, media in a fixed ratio.
- **Truncate identifiers, not explanations,** and keep the full value reachable.
- **Content has a maximum width,** with prose at 45 to 75 characters a line. Backgrounds may run full width.
- **One scroll per axis.** Avoid scroll areas inside a scrolling page, and never take over scrolling.
- **Tables:** the header stays in view, the whole row selects it, selection shows its count and its bulk actions, active filters show and can be removed, and a missing value is a dash, not "N/A". Status and primary actions on a row are always visible; only secondary ones wait for hover.

## Components and states

- **Every interactive component has all its states:** default, hover, focus, pressed, selected, disabled, loading and error. A component library defines them once, so siblings cannot drift.
- **Every view has all its states:** first use, no results, filtered to nothing, not permitted, failed, loading and full. Each empty state says why it is empty and offers the next step.
- **A family shares its parts:** buttons and inputs in a row are the same height, variants share one radius, focus and error look the same everywhere, two border widths at most.
- **Use standard controls.** Scrollbars, form controls, menus and dialogs behave as the platform's do. A new component is built only when the library has none.
- **Overlays fit their job:** a tooltip names, a popover holds a little, a menu lists actions, a drawer holds a side task, a modal blocks for a decision, a bottom sheet on mobile. A modal does not open another modal.
- **Elevation is a scale of tokens** and marks what floats. Shadows are soft and offset; one element declares its depth once, by border or by shadow.
- **Opacity marks a state,** such as disabled or dragging. A tint is its own token.
- **Icons come from one set,** at one weight, one icon for each concept.

## Colour

- **Colours are roles, not swatches:** canvas, surface, text, action, focus, border, data, and the four statuses.
- **Statuses are four, each with one meaning everywhere:** error, warning, success and information. Amber means warning and nothing else.
- **The accent marks action, selection and state.** On a Work surface, neutrals carry the screen.
- **Code uses tokens, never literal colours.** A theme changes the roles, and nothing else.
- **Dark is composed, not inverted:** surfaces step by lightness in one hue, the accent is softened, and contrast is checked again. When both themes ship, the system preference chooses.
- **Neutrals lean to the brand's hue.** Avoid pure black on pure white.

## Type

- **Sizes come from one base and one ratio.** On Work and Read surfaces the ratio is 1.125 to 1.2 and sizes are fixed; Persuade and Show surfaces may use a larger ratio and fluid display sizes.
- **Body text is at least 16px,** secondary text no less than 14px. Native applications use the platform's text styles: Dynamic Type on iOS, Material's type roles in `sp` on Android.
- **Figures in tables are tabular.** Monospace is for code, data and measurement.
- **Headings balance their lines,** and no line ends with a single stranded word.
- **Load only the faces and weights used,** with metric-compatible fallbacks.

## Motion

- **Motion has a purpose:** feedback, showing where something went, showing a change of state, or explaining. Without one, it is cut. What the person is reading or acting on does not move for effect.
- **Frequent actions do not animate.** Anything done many times an hour responds instantly.
- **Routine motion lasts 300ms or less:** about 100 to 160ms for a press, 150 to 250ms for a menu, up to 300ms for a panel. An exit is quicker than its entrance.
- **Ease out,** for entering and responding. Bounce and elastic easing only where the product's language calls for them.
- **Animate transform and opacity,** and name each property transitioned. Entrances start near full size, not from nothing; a popover grows from its trigger.
- **Interruptible:** a repeated trigger redirects the motion rather than restarting it.
- **Content is visible without script,** and motion out of view stops.

## Forms, errors and copy

- **Every field has a visible label** that stays. A placeholder shows an example, never the label.
- **Validate when the field is left,** or as the person types, after a pause, for formats that need it. Submitting moves to the first error.
- **An error sits by its field,** says in words what is wrong and how to fix it, keeps what was typed, and is tied to the field for assistive technology.
- **Mark the fewer:** required or optional, in the label.
- **Use the right input types** and `autocomplete`, and group related fields with `fieldset` and `legend`.
- **Every error says what happened, why when it is known, and what to do next.** No raw codes, no stack traces, no blame. A failure that may pass has a retry. Its weight fits it: a field error inline, a passing failure as a toast, an ongoing problem as a banner on what it affects, a blocking one on the page.
- **Copy says each thing once,** in whole sentences that translate: no assembled fragments, plurals through the localisation library, room for text to grow by a third, logical properties for right-to-left layouts, and dates, numbers and currency formatted for the locale.
- **The tone fits the stakes.** No jokes about payment, deletion or lost access.
- **Real content only.** No placeholder text, invented figures or claims the product does not keep.

## Platforms

- **Responsive layouts change structure, not scale:** stack, reorder, collapse and reveal. Mobile drops or moves what a desktop shows; a dense desktop layout is not shrunk to fit a phone.
- **Input decides behaviour, not width.** Hover effects and hover help apply only where the pointer can hover.
- **The web is fast:** largest contentful paint within 2.5s, layout shift at most 0.1, interaction to next paint within 200ms, images sized in advance. A single-page application updates the title and moves focus on each route.
- **iOS:** content inside the safe areas, a tab bar for sections and a navigation stack for depth, swipe back always works, system controls and SF Symbols, Dynamic Type, and a crossfade under Reduce Motion.
- **Android:** Material 3. A navigation bar at compact width and a rail or drawer wider, Back and predictive Back always work, edge to edge with insets, colour roles with a first-class dark theme, snackbars for transient news, and motion off under Remove animations.
- **Desktop:** the operating system's menus, shortcuts, windows and dialogs.
- **A native application is not a web page in a frame:** no affordance that needs hover, and no navigation or buttons shaped like the web's.

## Terminal

A command line is a contract written as a `specification` ([designing](../../designing/references/interface.md#by-platform)). Its output is held to these rules.

- **Help is built in:** `--help` and `-h` on every command, with a usage line, the options, and an example. With no arguments, a command that needs them prints its usage.
- **Data to standard output, messages to standard error.** Progress, warnings and errors go to standard error, so the output can be piped.
- **Exit codes mean something:** 0 for success, non-zero for failure, and the meaning of each one documented.
- **Machine-readable output on request,** as `--json`, stable across versions like any contract.
- **Colour only on a terminal:** none when output is not a terminal, when `NO_COLOR` is set, or with `--no-color`. Colours are few, each with one meaning, readable on light and dark backgrounds, and never the only carrier of meaning.
- **Interactive only on a terminal.** Every prompt has a flag that answers it, so a script never waits. A destructive command asks, and `--yes` answers for it.
- **Errors say what to do:** what failed, the input that caused it, and the fix, without a stack trace unless asked for.
- **Long work shows progress** on standard error, and Ctrl-C stops it cleanly.
- **Terminal interfaces** work from the keyboard alone, show their keys on screen, redraw when the window is resized, and fit 80 columns.

## Made for this product

- **The look comes from the product,** as `DESIGN.md` records it, not from a framework's defaults or the habits of generated interfaces: identical grids of icon cards, a large number over a small label as a page's opening, gradient text, decorative glows, emoji standing in for icons. Each needs a reason in the brief.
- **A Work surface earns trust by being familiar:** standard navigation and controls, and identity in the details: type, palette, density, one signature element.
- **A site and its product share one brand:** logo, hue, status colours, type and focus ring. Where they differ, it is a decision recorded in `DESIGN.md`.
- **The parts the browser draws are themed too:** selection, caret, scrollbars and focus rings.

## Proving it

An interface is checked rendered, not read from its code.

- **Fix the shots first.** A shot is one screen in one state at one viewport size, with its reference when the design has one. Set each up so it renders the same frame every time: a fixture or story with fixed data, a route with seeded data, a viewport preset. Render each beside its reference, at the same size.
- **Score each dimension apart,** so the weakest cannot hide behind the others: layout and spacing, type and components, colour, and interaction and motion. A critic who sees only the shots and the rubric scores them, never the builder: the Visual [lens](../../review/references/lenses.md) in a review.
- **Look at it at every size it ships at,** with real content, in each state, in each theme. On the web, at least a phone and a desktop width. Native screens come from the simulator, emulator or device, never a browser, and the evidence says which.
- **Stress it:** long and short text, translations, 200% text, empty lists, a thousand rows, a slow network, a failed request.
- **Pass it by keyboard alone,** and with a screen reader on what changed.
- **Run the checks a machine can:** an accessibility scanner such as axe or Lighthouse, the `DESIGN.md` linter, and the performance budget. A clean scan is the floor, not the verdict on hierarchy, rhythm or type.
- **Watch motion slowed down,** interrupted, repeated, and with reduced motion on.
- **Say how each number was made.** Measured, when a command produced it on this build: a contrast ratio, a timing, a colour difference. Judged, when a person or a model scored it. A check that did not run is written as not run, never as passed.
- **Hand over the evidence:** the shots beside their references, recordings of motion, which tools ran and what they reported, and what was not checked.
