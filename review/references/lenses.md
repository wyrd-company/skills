# Lenses

Read this at `high`. A lens is a fresh reviewer that reads the work for one question. It knows nothing of the work's history or of your own reading, so it sees what familiarity hides from you, and its narrow question makes it look further than a general read does.

Lenses are the most expensive part of a review, so they are reserved for `high`, and you choose the few that fit the work.

## Run them

1. **Finish your own read first,** so you know where the work is weak and which questions matter.
2. **Choose two to four lenses** from the catalogue below, for the work's kind and what triage found. Fewer, well-chosen lenses beat all of them.
3. **Delegate each one** in parallel, read-only. A mid-tier model is usually enough for one narrow question; choose from [models.yml](~/models.yml). Give it only the surface, the contract, and its question, not your findings: a lens that is told what you found confirms it.

   ```text
   You are reviewing <surface> at <head>, read-only, for one question: <the lens's question>.
   The contract it must meet: <task, issue, standard>.
   Report each problem with its location, why it matters, and a severity: P0, P1, P2, P3, or Q for a question. Report nothing outside your question. If you find no problem, say so.
   ```

4. **Treat what comes back as leads.** Verify each one yourself before it becomes a finding, merge duplicates, and drop what you cannot confirm or what is outside the contract.
5. **Record each lens in the handoff,** with what it found. A lens that failed or returned nothing is `not run`, not "no findings". Retry it once.

## Catalogue

| Lens | Kind of work | The question |
|---|---|---|
| Correctness | Code | Where does this produce a wrong result, lose data, or leave state half-written? |
| Adversary | Code, designs | How would someone exploit this, through its input, its permissions or its timing? |
| Blast radius | Code | What outside the diff does this break, and what single fact is it safe because of? |
| Evidence | Code | Does each test and check prove the claim it is cited for? |
| Fit | Code, documents | Does this follow the patterns, names and structure of the code or documents around it? |
| Fidelity | Documents | Does every claim about the system match the code, and is everything the reader needs documented? |
| Comprehension | Documents, designs | Paraphrase it. Where does a reader without the author's context get lost or misread? |
| Agent walk-through | Instructions | Following this literally on a realistic task, where does an agent stop, guess or loop? |
| Design critic | Designs | Which assumptions are unjustified, and which failure modes are unaddressed? |
| Readiness | Designs, plans | What would an implementer still have to decide for themselves? |
| False compromise | Designs | Where does it accept a trade-off as unavoidable that is not? What would the alternative cost? |
| Zoom out | Any | Does this solve the problem the issue states, at the right altitude, or a nearby problem? |
| Economy | Documents, instructions | What can be removed without the reader losing anything they need? |
| Visual | Interfaces | Shot by shot, how far is the render from its reference, on each dimension of the rubric, and what are the largest gaps? |

The Visual lens sees the rendered result and nothing else: the shots the [interface standard](../../standards/references/interface.md#proving-it) describes, each beside its reference, and the rubric with its bar. It gets no code, no task history and no one's opinion of the work, including who built it. Run at least two, one from a provider other than the builder's, and take the median score per dimension. When two scores differ widely, run a third.

When a review needs a question this catalogue does not have, write it, and record the lens and what it found as an observation in memory tagged `review` and `lenses`.
