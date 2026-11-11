# Definition of Done: the harder cases

Read this when a Definition of Done line rests on a suspected cause, asks for an assertion, or promises a property that only shows across an event.

## A suspected cause is a hypothesis

An executor rarely argues with a cause written into a task. They confirm it: the named defect is usually real, it sits on the observed path, and the checks go green afterwards. So the task must say how far the cause can be trusted.

- Where the task describes a cause, state its evidence status in the same sentence: **measured**, **inferred from reading the code**, or **assumed**.
- Test whether the cause is load-bearing: if it were false, could any Definition of Done line or constraint still be satisfied? If not, add the line "establish or falsify the recorded cause", and word the other lines so that disproving the cause completes the task instead of failing it.
- Check the task against itself. A task that quotes a measurement ruling a cause out, and then requires a fix for that cause, cannot be completed as written.
- A remedy that the stated cause makes impossible shows the cause was written from a symptom. Follow the cause through to each remedy you offer.

This does not apply to an investigation or spike. There the hypothesis is the subject, and falsifying it is the deliverable.

The same holds for a cause added after the task was written, in a log entry or a dispatch note. See [task-ownership](../../task-ownership/SKILL.md).

## An assertion must be able to fail

A line that asks for an assertion points at a surface: the place where the assertion runs. If an earlier layer (a validator, a loader, a schema, a type) already makes the forbidden state unrepresentable, no input reaches the assertion in that state, and it can never fail.

- Count the conditions the line asks for. Then count how many can each fail alone at that surface. If the second number is smaller, the line asks for documentation and calls it evidence.
- Repair it one of two ways: point the line at the layer that enforces the property, or ask for the assertion as documentation and say so, so that review does not count it as a proved guard.

An executor satisfies a task as written. An assertion that cannot fail will therefore come back reported as proved.

## A property across an event names the event

Some properties only show across an event: surviving a restart, resuming after an outage, leaving existing clients unaffected. For these, the line names the event and a consumer that holds state from before it, such as a client that keeps the URL it was given before the restart. A test that builds fresh state after the event does not prove the property. Say which environment the check runs against.
