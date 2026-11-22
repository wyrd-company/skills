# Text figures

Read this when you are answering in the thread and prose alone would leave the point unclear. Text figures sit in a code block inside the message. They need no tool, and the reader does not have to leave the conversation.

## Choose by what the question is about

| The question is about | Show |
|---|---|
| Logic or an algorithm | Pseudocode |
| What calls what at runtime | A call tree |
| A UI's structure | A component tree, with the state and package boundaries that matter |
| Which file or module owns what | A shallow file tree, with a short comment per entry |
| Interaction between parts over time, or data moving through them | A Mermaid `sequenceDiagram` or `flowchart` |
| What a change does to an existing shape | A `diff` of that shape |

Keep each figure to what the question needs. Three levels of a call tree that answer the question are better than ten that cover the module.

## Pseudocode and trees

```text
on(save)
  if content is unchanged
    return cached result
  write new content
  return fresh result
```

```text
submitForm                      src/forms/submit.ts:14
  createSession                 src/sessions/create.ts:30
    persistPrompt
    launchAgent
  navigateToSession
```

Put a path and line beside a node when the reader may want to open it.

## Diffs of a shape

Use a `diff` block when the point is what changes and the shape around it already exists. Diff the shape the question is about, not only source code:

```diff
 src/
 ├── commands/
+│   └── show.ts          # expands the command
 ├── sessions/
-└── transport.ts
+└── transport/
+    ├── client.ts
+    └── stream.ts
```

```diff
 submitForm
   createSession
     persistPrompt
+    expandMention
     launchAgent
```

The same works for a component tree or for pseudocode. Show the whole block instead when most of it is new, when the omitted lines would hide ownership or order, or when the reader needs a target to copy.

## Mermaid

Use Mermaid when relationships form a graph or a sequence that a tree cannot show. Keep it to the participants in the question. Quote labels that contain punctuation. Check that the harness renders Mermaid. If it does not, a call tree or a short table usually says the same thing.
