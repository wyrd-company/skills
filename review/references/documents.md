# Documents

Read this when the work is prose: documentation, a design, a specification, or instructions written for agents. Prose fails differently from code. It compiles whatever it says, so nothing stops it being wrong, unclear or out of step with the system it describes, and its reader acts on it anyway.

## Read in this order

1. **The contract,** and the standard the document is judged against: its soft claims, a template, a style guide, the pattern of its neighbours.
2. **The document whole,** before any line-level reading. Then write a paraphrase in a few sentences: what it proposes or instructs, and how it says the existing system works. If you cannot write one for a section, that section is a finding. Compare the paraphrase with the task's intent: a wrong paraphrase is a finding too.
3. **What it describes:** the code, the other documents, the skills it refers to.

## What to look for

- **Truth:** each claim about the system matches the system. Read the code or run the command; do not trust the document's own word. A claim about tested behaviour matches its test.
- **Completeness for its reader:** each term is defined or linked, and nothing assumes a prerequisite the reader does not have. Read from where its reader starts, not from where you start.
- **One source:** it refers to the specification instead of restating it. Two copies of a rule will disagree.
- **Calibration:** each claim is as strong as its evidence. Each caveat names the decision it affects, or it goes.
- **Economy:** cut what the reader does not need. A sentence that changes nothing is a cost every reader pays.
- **Structure:** it follows the template or standard it is held to, and its headings let a reader find the part they need.

## Designs and specifications

A design is reviewed before anything is built on it, when a miss costs least to fix.

- **Its questions are answered.** Check it against its template or the issue: every question it must settle is settled.
- **Its assumptions are justified.** A claim about behaviour, performance or a constraint that the design rests on has evidence, or is marked as an assumption to test.
- **Its failure modes are named:** what happens on error, under load, at the limits, and with an attacker.
- **It can be built.** An implementer can start without making a design decision of their own: a storage choice, an interface, an error strategy. Each one left open is a finding.
- **Its trade-offs are real.** Where it accepts a compromise as unavoidable, ask whether it is. A finding here proposes the alternative and says what the alternative costs.

## Instructions for agents

Skills, prompts, `AGENTS.md` and templates are followed literally, by readers who cannot ask the author what was meant. A wrong rule repeats in every piece of work that follows it.

- **Walk it as its reader.** Take a realistic task and follow the instructions step by step. Find where an agent would stop because nothing says what to do next, guess, or loop.
- **Every rule is reachable.** The description says when the instructions apply, and the agent would actually load them then. A reference says when to read it.
- **No contradiction with other instructions.** Search the other skills and `AGENTS.md` files for the same subject. Two instructions that disagree are a finding, even when this one is right.
- **It says what to do, not only what to avoid.** A prohibition with no alternative leaves the agent guessing.
- **It assumes no single user.** Operators, handles and paths come from the thread or the record, not from the text.
- **Each rule earns its place.** Ask what goes wrong without it. A rule that covers a case that never happens costs every reader.
