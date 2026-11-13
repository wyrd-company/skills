# Technical

Read this when the design shapes code: modules, interfaces, data structures and state.

## Ground it first

Know every part of the system the new code touches before you shape it: trace how it works today, not only which files it lives in. When the design moves ownership or layering, find out why the current shape is the way it is, so that reason becomes a constraint instead of a guess. Only work with no surrounding system skips this.

## Data first

Get the data's shape right before the logic. Define the core types, trace every way the data is read and written, and choose structures that fit the common paths. Changing a data structure is a line early and a rewrite late.

Model the domain in a structure instead of scattering it across conditionals:

- a state machine instead of booleans and phase checks that must agree;
- a typed model instead of loose parameters and repeated assumptions about a shape;
- a lookup table or a tagged union instead of branches spread across files;
- commands and events instead of ad hoc changes to state;
- a module that owns one body of knowledge instead of a pipeline of steps (load, validate, transform, save) that each repeat its rules.

The tells that this was skipped: a new feature that adds one more branch to an existing chain, and a second flag that has to stay in step with the first. Do not force a structure where the current code is clear, local and unlikely to grow: one that adds indirection without removing branches, duplicated rules or invalid states is not worth it.

When actors share state, ask what happens if another changes it at the same time. Unless the answer is "nothing", give it one owner.

## Write the caller first

Write how a caller will use the interface before the interface: the usage, then the types and signatures that serve it, then the module map. A sketch with unimplemented bodies is enough to judge a shape.

## Design it twice

The first shape you think of is rarely the best. When the shape is the decision, produce at least two designs that differ in structure, not in detail. Delegates given the same brief and different constraints are a good source:

- the smallest interface: one to three entry points, each doing a lot;
- the most flexible: many uses and extension points;
- the common case trivial: the default call needs nothing;
- the dependencies behind ports and adapters.

Each design gives its interface (types, invariants, ordering and errors), a usage example, what it hides, how it reaches its dependencies, and where it is strong and weak. Compare them on depth, on where a change would concentrate, and on where the boundaries fall. Then recommend one, or a combination, and say why. A contested or expensive choice can be an [arena](../../epic-planning/references/arena.md).

## Red flags

Revise or reject a design that shows these:

- **A shallow module:** a large interface that hides little. Callers coordinate several calls to complete one operation, or options expose internal stages. A deep module hides a lot behind a small interface; a deep chain of calls is not the same thing.
- **Leaked knowledge:** one internal decision, such as a representation, a policy or a wire format, known in several modules, so changing it means coordinated edits. Parse external data into domain types at the boundary, and keep storage, framework and protocol types private.
- **Steps instead of knowledge:** modules split by when they run rather than by what they own.
- **A pass-through:** a method that forwards its arguments to another with the same shape, adding a layer and hiding nothing.

## When the design proves wrong

Building against a design will show where it is wrong. A deviation is a signal to raise, not friction to absorb: a parameter the design did not foresee means the design was wrong, a requirement was missed, or the implementation is overreaching. One deviation is a question. The same deviation over and over, workarounds of one shape in unrelated places, or types that need escape hatches to compile mean the shape is wrong. Then redesign as if what you learned had been known from the start, smaller before it grows, and change the documents to match.
