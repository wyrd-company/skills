# Framing

Read this to frame an outcome with the operator, before any solution is discussed. The frame is what every solution is judged against, so the operator confirms it, and a solution never stands in for it.

## The frame

1. **The problem,** stated apart from any solution. "Operators cannot tell which containers hold a credential", not "add a credentials page".
2. **The invariants:** what every acceptable solution keeps true.
3. **The requirements,** each with the observable criterion that shows it is met.
4. **One acceptance scenario,** end to end, from the user's point of view, across the real system boundaries.

A request often arrives as a proposed design. Do not infer the frame from it: ask what problem it solves, and frame that. The design may still turn out to be the answer.

## The interview

- **One question at a time,** each with your recommended answer and the reason for it.
- **Walk the tree.** Settle a question before the questions that depend on it.
- **Ask only what only the operator knows.** Answer the rest from the code, the documents and memory.
- **Keep the question short.** Put the context and reasoning around it, not in it: a long question gets skimmed.
- **Label what stays open.** An unresolved point goes in the frame as an assumption or an open question, so it cannot quietly become a requirement.

## Words

- **Check terms against the repository's `terms/`.** When the operator uses a word differently from its definition, say so at once: "`terms/cancellation` means the whole order is withdrawn; you seem to mean one line of it. Which is it?"
- **Sharpen vague words.** When a word is overloaded ("account" for both the customer and the login), propose one precise term for each meaning, and record it as a term document ([documents](documents.md)).

## Test it

- **Probe the edges with scenarios.** Invent concrete cases that force the boundary between two concepts to be precise.
- **Check claims against the code.** When the operator says how something works, look. A contradiction is a question: "The code cancels whole orders, but you said a partial cancellation is possible. Which is right?"

## Confirm

Read the whole frame back, and have the operator confirm it. Write it on the GitHub issue for the goal, creating the issue when there is none. Then chart the way.
