# Instructions for agents

Read this when writing or reviewing anything an agent follows: a skill, an `AGENTS.md`, or a brief to a delegate. Its reader follows it literally, on every run, and cannot ask what you meant. A wrong or vague rule repeats in every piece of work that follows it.

## Every instruction

- **Say what to do.** State the behaviour you want, so the agent never reads the one you don't. A prohibition belongs only where the rule cannot be put positively, and then sits beside the positive target.
- **Fit the form to the failure.** Before writing a rule, name what goes wrong without it:

  | Without the rule, the agent | Write |
  |---|---|
  | Knows the rule, and breaks it under pressure | A prohibition, with the reasons agents give for breaking it and why each is wrong |
  | Does the work, in the wrong shape | The shape: what the output is, its parts, in order |
  | Leaves out a required part | A slot for it in the template |
  | Should act only in some cases | A condition the agent can observe: "when the task names a judge, ..." |

- **Make each exception its own condition.** "Unless it matters" reopens the rule for negotiation, and "this does not apply to X" does not stop the rule reaching X. Write the exception as a rule of its own, on a condition the agent can observe.
- **Give the reason, not capitals.** A reason lets the agent apply the rule to a case you did not foresee. "MUST" and "NEVER" in capitals tell it only that you were worried.
- **Give a default, not a menu.** Name one way, and the case that calls for another: "use X; when Y, use Z".
- **End each step on a criterion the agent can check,** and make it exhaustive: "every changed model accounted for", not "produce a list of changes". A vague end invites the agent to stop early.
- **Keep each rule in one place.** Link to the skill or reference that holds it, by name. Two copies of a rule drift apart.
- **Leave to the environment what the environment says.** Scripts, configuration, the directory layout and `--help` are already true; a copy of them goes stale. Write what the agent cannot find by looking: the convention, the reason, the trap.
- **Cut what changes nothing.** A sentence that asks for what the agent does anyway costs every reader and does nothing. Delete the whole sentence. When people disagree whether a sentence matters, run the instructions with and without it.
- **Turn a repeated correction into a check.** A rule that has to be given twice is a candidate for a linter, a script, a hook or a test. Prose is for what needs judgement.
- **Assume no single user.** Operators, handles and paths come from the thread or the record, never from the text. Write "the operator", not a person's name or the tool they use.
- **One word for each idea,** used every time. Write as the only version, as the [documentation standard](documentation.md#state-what-is) says.

## Skills

A skill is a folder: `SKILL.md`, the `references/` it reads when a case calls for them, the `assets/` it copies or fills in, such as a template, and any `scripts/` it runs. A template is held to this standard too, as its reader is the agent that fills it in: `task-authoring`'s task template is one. Its `README.md` is for humans and the record of its sources; `SKILL.md` does not link to it. What the README holds is in the repository's `AGENTS.md`.

- **The description decides when the skill is read.** It is the only part an agent sees before choosing. Write it as: "Use when ... . Covers ... . Not for ... (`other-skill`)."
  - **Use when** names each distinct case that should load the skill, once, in the words a task or a person would use. Two words for the same case are one case.
  - **Covers** names topics, never the steps. An agent given the workflow in the description follows that summary and skips the skill.
  - **Not for** names the neighbouring skill that takes each nearby case.
- **`SKILL.md` holds what every case needs.** What only some cases need goes in a reference, and the line that links to it says when to read it. A reference is linked from `SKILL.md` or from the reference that sends the agent there, one level deep, never through a chain.
- **Keep a topic together.** Its definition, rules and exceptions sit under one heading, so reading one part brings the rest.
- **`SKILL.md` stays under 500 lines.** Past that, attention thins over the excess: move what only some cases need into references.
- **Script what agents keep rewriting.** When agents write the same code for a skill again and again, or a sequence breaks when done by hand, put a script in `scripts/` and have the skill run it through its interpreter: `bash scripts/x.sh`.
- **Walk it before you hand it over.** Take a realistic task and follow the skill as its reader would, from the description on. Fix every place where you would stop, guess or loop.

## AGENTS.md

`AGENTS.md` is read by every agent that works in its folder, on every turn. Each line costs that much, so it holds only what applies to all work there:

- what the repository or folder is, and its layout;
- settled rules about working in it, which every agent there must follow;
- where to start, and pointers to the documents and skills that matter, each saying when to read it.

A folder whose work differs has its own `AGENTS.md`, which the agent reads with its parents'. A repository's `AGENTS.md` wins over a skill or standard for that repository.

Each kind of instruction has its own home:

| What it is | Where it goes |
|---|---|
| A settled rule about working in one repository or folder | That folder's `AGENTS.md` |
| How to do a kind of task, in any repository | A skill |
| A rule the work is held to, shared by executor and reviewer | A standard in `standards` |
| Something learned and not yet settled, or knowledge across repositories | Memory, as an observation |
| A rule a program can check | A check: a linter, a hook, a test |

## Briefs to delegates

A brief is the only context a delegate has. It does not see your conversation, and you see only what it sends back.

**Write a task when the delegate owns the result:** it delivers something judged on its own, such as a pull request with its own review, or the work must outlast the session, be resumed, or be coordinated with other work. [`task-authoring`](../../task-authoring/SKILL.md) says how. When the result comes back to you and becomes part of your own work (research, a search, an independent read, a step of your task), the brief carries it alone. A brief that needs a Definition of Done, or context the next agent will also need, is a task: write the task, and brief against it.

**With a task, the brief holds only what is true for this run.** The task is the contract, true for any agent that picks it up: point at it, and do not paste or restate it. The brief names:

- the role for this run (implement, remediate, review, accept), and the task's id and board;
- the base: its branch and commit;
- the authority for this run, such as whether to merge on acceptance;
- the surfaces that work running in parallel is touching;
- for `hitl` work, the person the agent helps.

[Dispatch](../../epic-orchestration/references/dispatch.md) gives the prompt for an epic's tasks.

**Without a task, the brief is the contract,** kept to what this one run needs:

- **One piece of work per brief,** with its goal, what is already ruled out, and the scope, in and out. Leave out the history of how you got here.
- **Point at files; don't paste them.** Name the paths to read. Put exact values the delegate must use verbatim in a file it reads, so they exist in one copy.
- **Say what to send back,** in a fixed shape: the result, the evidence, and what was not checked. A long result goes in a file, and the reply names its path.
- **Name when to stop.** Say which conditions should end the work and come back as a question or a block, instead of a guess.
- **When it cannot ask, decide for it.** A delegate with no way to ask questions needs the scope, the paths it may touch and the acceptance criteria up front.

**Every brief:**

- **Withhold your conclusions when you want an independent read.** A reviewer told what you found confirms it. Give it the work and the question.
- **Fresh context unless you want it shared.** A fork inherits your context and your assumptions. Start the delegate fresh when its value is an outside view.
- **A delegate does not delegate** unless the brief says so. It does the work itself.
- **Choose its model for the work.** One left unset inherits yours. [Dispatch](../../epic-orchestration/references/dispatch.md) says how models are chosen.
- **No secrets.** A brief is a message other agents and logs can read.
