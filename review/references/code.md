# Code

Read this when the work changes source, tests, scripts, configuration or CI. It covers what to read, where defects hide, and how to judge the evidence the executor handed over.

## Read in this order

1. **The contract,** so you know what the change is for before you see how it does it.
2. **The diff,** whole, at the reviewed head. Note every symbol it adds, changes or removes, and what now behaves differently, including what the diff does not spell out: a default that changed, an error path that moved.
3. **The handoff's evidence,** against the Definition of Done: which line each check proves, and whether the run came from the handoff commit.
4. **Beyond the diff,** at `normal` and `high`, as below.

## What to look for

Ask of every change, at every level:

- **Correctness:** wrong logic, missed edge cases (empty, zero, the maximum, a missing field), broken contracts, state left half-written, races between two actors.
- **Failure:** errors swallowed, caught too broadly or turned into success; resources not released on every exit path; work with no bound on size or time.
- **Security:** input from outside trusted without checks (injection, path traversal, request forgery, unsafe deserialization), authorization checked in the wrong place or not at all, secrets or personal data in logs, errors or commits.
- **Fit:** the change follows the patterns the repository already uses, puts responsibility where its neighbours expect it, and does not add a dependency the rest of the code avoids.
- **Removal:** dead code, flags nothing reads, branches nothing reaches, compatibility shims nobody needs. Less code is a finding worth making.

Check performance only where the code is hot or the data is large: a query inside a loop, an unbounded read, an allocation on every request.

## Beyond the diff

The diff shows what changed, not what it breaks. Listing callers is not the job, because anyone can grep for those. The job is the breakage a search does not show:

- **Find the fact the change is safe because of.** Most changes that look risky are safe because of one fact, such as "this only drops entries already expired". Find it. If it holds, most of the risks fall with it; if it does not, that is the finding.
- **Follow what a symbol search misses:** a field in JSON another service reads, a database column, a file format, a flag read from the environment, a script in CI, another language reading the same bytes, code several calls away.
- **Read the library, not your memory of it.** Check the pinned version's source or documentation when the change depends on how it behaves.
- **Search for the rule the change bends.** When it adds an exception to something stated as always or never, search for every other place that states it: docs, comments, tables, other skills. A statement the exception now contradicts is a finding.

How sure you are about the safety fact, from weakest to strongest:

1. Someone said so.
2. You pointed at the line.
3. You walked the failure step by step and it cannot happen.
4. You ran it: a script or test calls the real code and fails loudly if you are wrong.
5. You reproduced it in the running system.

At `high`, get the safety fact to step 4, or say in the handoff that it is unproven. At `normal`, say which step you reached.

## Judging the evidence

The handoff's evidence is a claim too. Check it the way you check the code:

- **A test proves what it asserts, nothing more.** A test that greps a template proves the string is there, not that the generated code runs or that the branch is reached.
- **A guard is proved when breaking it fails a named test.** Read the mutation report, when there is one, and check that each mutation names the assertion that caught it. "Six of six failed the suite" does not say which assertion failed, or whether a setup timeout turned the run red. At `normal` and above, reproduce one.
- **A claim in prose needs an assertion.** For each sentence the change adds saying the system will or cannot do something, find the test that holds it. If removing the guard leaves the suite green, the guarantee lives only in the prose.
- **A property across an event needs the event.** Survival across a restart, recovery after a crash and expiry over time are proved only by a test that performs the event, with something that held state from before it.
- **A skipped check is not a pass,** and a green run at an older head proves nothing about this one.

Re-run the cheapest check that proves the main Definition of Done line yourself, at `normal` and above. Use the repository's own commands.
