# User-acceptance testing

Verification proves the work works. Review judges how it was built. Acceptance asks whether it meets the user's need, judged from the user's side. Only the last needs the user.

## When it is needed

- The issue or the operator asks for it.
- The bar includes a judgement only the user can make: "is this what I meant", "does this read well", "is this pleasant to use". In the Definition of Done this is a soft claim whose judge is the user.

It is not needed when the bar can be checked fully without the user (a bug with its reproduction, a refactor, maintenance), or when the user already accepted a prototype or an earlier slice that the result matches.

## Who the user is

The user is whoever the work is for, and it is not always a person. Work for agents (a skill, a tool, a prompt) has agents as its users. Its acceptance is a fresh agent, with no other context, using the result for its purpose.

## Accept it yourself first

Before any person is asked, run the acceptance yourself, as the user: follow the user's path, not the developer's, and judge the result against the bar. Fix what fails. A person is asked to accept only work that has passed your own acceptance run and its review.

## Accept early when you can

Acceptance need not wait until the end. A prototype, a mock-up or a first end-to-end slice can be accepted while the rest is still cheap to change. An early acceptance that the result still matches may make a final one unnecessary.

## Prepare the user

A user must not be expected to remember the goal or the work. Give them:

- the goal, and the bar this acceptance is against;
- the decisions made along the way that may change what they expect, why each was needed, and the alternatives considered;
- what they need to understand the result: its documentation, screenshots, a short explainer.

Then let them use it their own way. Do not hand them a script of steps to follow: a user clicking through "this, then this" is following your path, not judging the result.

Set up beforehand everything the acceptance does not cover: prerequisites, data, access, running services. The exception is when setting up is part of the experience being accepted, such as installing a new service. Then the setup is under test: give the user the instructions a real user would get, step by step, and let them follow those.

Put the brief and its evidence on the review surface, and notify the user that it is waiting for them.
