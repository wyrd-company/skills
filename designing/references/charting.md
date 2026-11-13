# Charting

Read this when the goal is framed and the way to it is not clear. Charting resolves the decisions between the frame and a plan. It produces decisions, not deliverables: when the pull to start building is strong, the way is probably clear, and it is time to hand over to planning.

## The destination

Name it first: the documents that, once written and reviewed, leave nothing to decide that blocks a plan. It might be a specification to build against, a technical design, or a domain model. The destination fixes the scope of the charting.

## The decisions

List what has to be decided to reach it.

- **A decision you can state precisely** goes on the list, even when it waits on another.
- **One you can only see dimly** is not on the list yet. Note it as not yet specified, and return when the decisions before it are made.
- **Work beyond the destination** is out of scope. Rule it out once, with the reason, instead of deciding it.

Resolve each decision in the way that fits it:

| Kind | When | How |
|---|---|---|
| Research | A fact from outside the repository: an API, a library, a standard | A read-only delegate reports what it found, with sources. |
| Spike | A technical question only running something can answer | A time-boxed experiment, recorded as a spike document: the question, what was tried, the findings and the conclusion. |
| Prototype | How it should look or behave is the question | A cheap, throwaway artifact to react to: a sketch, a stub, a rough screen. It is linked from the decision and never merged. |
| Alternatives | The shape is the question: an interface, a boundary, a data model | Two or more structurally different designs, compared. [Technical](technical.md) says how. An expensive or contested one can be an [arena](../../epic-planning/references/arena.md). |
| Conversation | Only the operator, or the task's judge, can decide | Options with a recommendation, one question at a time, as in [framing](framing.md). |
| Groundwork | Something has to exist before it can be judged: access, an account, data in place | Do it, and record what later decisions depend on: where the credential lives, the new URL. |

Each answer lands in the document it shapes ([documents](documents.md)). New decisions it makes possible go on the list.

## Decision tasks

When the decisions will not fit one session, or several people or agents resolve them, track them on a board with [task-authoring](../../task-authoring/SKILL.md).

- **The map** is one task for the design. Its body names the destination, lists each decision made with a one-line gist and a link to the document it landed in, notes what is not yet specified, and lists what was ruled out of scope and why. It is an index: it points at the answers and never restates them.
- **Each decision** is a child task. Its goal is the question, its Definition of Done names the document the answer lands in, and its body says which kind of decision it is. A decision that waits on another depends on it, so the open decisions that wait on nothing are the ones to take next.
- **A decision that is someone else's** names them in the task's `hitl` with the `judge` role. An agent never answers the operator's side of a conversation itself.
- **One decision per session,** except research, which delegates can resolve in parallel.

When a decision closes, add its line to the map, add the decisions it made specific enough to state, and remove them from not yet specified. When it shows a task to be beyond the destination, close that task and add it to the map's out-of-scope list with the reason. When it undoes an earlier answer, change the document that holds that answer.

The task holds the question and the work. The answer lives in the repository.
