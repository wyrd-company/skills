# Decide

Read this when you have been asked to decide for an epic. You are the escalation, not the pass: you make the rulings the epic needs, with the orchestrator's authority, and record them so later passes can act on them.

## Decide without asking

Decide when the decision:

- keeps the epic's goal and scope;
- can be reversed without material migration, compatibility, security, publishing or financial cost;
- concerns an implementation detail, an internal contract, an unpublished API or schema, or an incomplete design;
- fills an omission with the smallest coherent solution;
- reconciles sources whose differences do not matter to the goal.

When unsure, ask: "Who or what breaks if this changes later?" If the answer is nothing outside the epic, decide. An API is not a one-way door only because it is public: it is one when a released consumer, persisted data, an external integration or a compatibility promise depends on it.

Among several adequate solutions, choose the smallest one that keeps the intent, follows the existing language and conventions, adds the fewest concepts and surfaces, and stays easy to revise.

Before ruling to remove or narrow a capability, check what the code supports at the epic branch head. Notes alone do not establish it.

## Record the ruling

Record each ruling in the epic task's log, so a reviewer can check the authority without your conversation and the next pass can act on it. Use the log, not the body: a body can be rewritten and the ruling lost. Say what the pass should do next.

## Bring in the operator

Bring in the operator when the decision changes the outcome or scope, breaks a released contract, has costly or irreversible consequences for data or compatibility, carries material security, spending, legal or publishing risk, chooses between materially different product or architectural intents, or is still deadlocked after a ruling. How to ask is in [executing](../../executing/SKILL.md#when-to-decide-and-when-to-ask).

Log the question on the epic task as a hold. The operator's answer on GitHub wakes a pass, and the pass acts on it.
