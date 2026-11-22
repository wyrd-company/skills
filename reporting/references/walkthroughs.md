# Walkthroughs

Read this when the reader wants to understand how code or a system works: how a request is handled, why a value ends up wrong, what a module is for.

## Organize around one path

A walkthrough follows one question along one path through the code. It is not a tour of the directory. Name the question in the first sentence ("what happens when a user saves a draft"), then follow the path in the order it runs.

1. **Find the real entry point,** such as the route, command, handler or job, by searching for it. Do not guess from names.
2. **Follow the calls the question depends on.** Skip a branch that does not change the answer, and say that you skipped it.
3. **Stop where the question is answered.** That may be the write to storage, the response, or the line where the behaviour the reader asked about is decided.

Every step names its file and line, as a link. Quote a few lines of code when the exact code is the point. Otherwise describe what it does.

## Figures

Start with a call tree or a sequence diagram of the whole path, then explain each step. Add a figure partway through only where a step is hard to follow in prose, such as a state change, a data shape or a loop. The [text figures](text-figures.md) reference has the forms.

## Depth

Adjust the depth to the reader. For a newcomer, say what each step is for before you say how it works, and define the framework's terms. For a colleague, put the surprising decision first and spend fewer words on the parts everyone knows.

## Check

The code is the source of truth. Before delivery, reopen every cited line and confirm it still says what the walkthrough claims. Code moves, and a line number from earlier in the session can be stale.
