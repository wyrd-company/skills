# User documentation

Read this when writing or reviewing documentation for users of a product or developers who build on it: an application, a command line, an API or a library. The README is the front door to it, and is in the [repository standard](repository.md#readmemd). Text inside the interface, such as `--help`, empty states and error messages, is in the [interface standard](interface.md). Design documents, written for whoever builds the product itself, are in [documentation](documentation.md).

A reader opens the documentation with one need: to learn, to get a task done, to look up a fact, or to understand. Each page meets one of them, and the documentation as a whole meets all four.

## Audiences and navigation

- **Users use the product.** Installing it, configuring it, running commands and completing work through its interface belong to Users.
- **Developers write code against the product.** Calling an API, using a library, consuming events and writing a plugin belong to Developers. These readers build on the public contract; contributing to the product's implementation is covered by its contributor and design documentation.
- **The line is whether the reader writes code against it.** Give a page that serves both audiences to its main reader, and link to it from the other audience. Keep one copy.
- **Published source lives in `docs/user/`,** including downloadable examples and the images and recordings its pages use. The repository's README links to the published documentation's entry point.
- **Navigation groups by audience, then kind:** Users and Developers, each with Tutorials, How-to guides, Explanation and Reference for the pages it offers. Each page has one home, and navigation makes it reachable. These are navigation sections; file names and subfolders follow the publishing contract.
- **The layer above this standard supplies the publishing contract:** where the documentation is published, its metadata and navigation format, and how it is built. Apply that contract together with this standard. Without one, follow the repository's existing published documentation; when it has none, ask before choosing where to publish.

## Four kinds of page

| Kind | Its reader | It holds |
|---|---|---|
| Tutorial | A newcomer learning by doing | A lesson that leads the reader to build something that works |
| How-to guide | A reader with a task to finish | The steps that reach one goal |
| Explanation | A reader stepping back to understand | Why it works the way it does, and how its parts fit together |
| Reference | A reader looking up a fact while working | A complete description of the public machinery: commands, options, fields, endpoints and errors |

- **A page is one kind.** When a tutorial needs a reason, it says it in a sentence and links to the explanation. When a how-to guide needs the full list of options, it links to the reference.
- **Both audiences use the four kinds.** A developer's tutorial teaches through a working integration; a user's tutorial teaches through the product's interface.

## Tutorials

- **The reader succeeds.** Every step works as written in a clean environment, and shows a result the reader can see. Walk it in one before review, as you do the README's quickstart.
- **It opens with what the reader will build,** and closes with what they built and where to go next.
- **One path.** No options, alternatives or branches the lesson does not need.
- **Doing, not explaining.** Each step says what to do and what to notice in the result. A reason gets one sentence and a link to the explanation.
- **The voice of a teacher beside the learner:** "we" and "now", with the expected output after each step.

## How-to guides

- **The title is the goal,** as the reader would search for it: "Rotate an API key", "Deploy behind a proxy".
- **It starts where the reader is.** It assumes they know the product, and lists only the prerequisites that are not obvious.
- **The steps are actions in order,** each with its command, input or control. It branches only where readers' situations really differ, and says which branch applies to whom.
- **It ends when the goal is reached,** with how to check that it was.

## Reference

- **Generated from the source of truth.** API, configuration and event reference comes from the raw specification definitions, such as OpenAPI, JSON Schema and proto, placed by [designing](../../designing/references/documents.md#specification-definitions). Command-line reference comes from the command line's specification definition in the ontology's CLI command specification format, as [interface design](../../designing/references/interface.md#by-platform) requires, placed like the other definitions. Both `--help` and the reference agree with it. Where no specification definition exists yet, generate from the parser's command definitions. Library reference comes from public signatures and source doc comments. Hand-written prose goes around what is generated, never in place of it; fix missing descriptions and examples in the generator's inputs.
- **The check catches drift.** A committed generation task produces the reference reproducibly. The repository's `check` regenerates it and fails on any difference from the committed output, including missing and obsolete pages. It also fails when generation fails. Review checks that changing a definition or doc comment without regenerating makes this check fail.
- **Its structure follows the product's:** a page for each command, endpoint, resource or module, in the same order and with the same names.
- **Complete and plain.** Every public entry is documented. Give its name, type or signature, default, accepted values, errors and example wherever those apply. It describes; it does not instruct or recommend.
- **Configuration reference covers sources and surfaces.** Generated configuration reference states the application's configuration sources and precedence order (file paths, environment variables, CLI flags, and admin policy when supported) from the configuration specification and schema, and marks each setting's schema-declared surfaces and constraints (environment variable, cross-tool aliases, CLI flag, project-local allowlist status, and whether admin policy may lock it; see [application configuration](configuration.md)).
- **The version that added an entry** is marked on the entry when the product has users on more than one version.

## Explanation

- **It answers why.** The concepts, the model the user works with, the reasons for the design, and the trade-offs that reach the user.
- **It is written for its audience,** in the product's terms. Explain the model and trade-offs the reader needs within the published documentation.
- **It is bounded by its topic.** A page explains one subject, titled as that subject: "How sync resolves conflicts".

## Writing

- **The glossary's words.** Use each term from `docs/terms/` with its one meaning, and the same name the interface shows.
- **Address the reader** in the present tense and the active voice: "Run `task check`", not "the user should run `task check`". A tutorial says "we", as above.
- **Describe the current version.** Leave version comparisons such as "new", "now supports" and "previously" to `CHANGELOG.md`. A tutorial's "we" and "now" guide the learner through its steps.
- **Commands and code in fenced blocks,** with a language tag. A block the reader copies holds only what they type, with no prompt; its output follows in a block of its own.
- **Placeholders are visible:** `<api-key>`, with a sentence saying what goes there.
- **Examples hold.** Every command, request and snippet runs or validates as written, against the version the documentation describes.
- **Headings in order,** one top-level heading per page, and links between pages relative, so they work wherever the documentation is read. `check` finds broken links.

## Published links

- **Users can learn entirely from the published pages.** Links lead to published user documentation or public product surfaces. Published pages never link into design documents: specifications, technical designs, decision records or other builder documents, including through full source-host URLs. Move the needed explanation into a published explanation page and link to the generated reference for the contract.
- **Publish the definitions developers build against.** Generate copies of raw definitions, such as schemas, OpenAPI and proto, under `docs/user/` alongside the generated reference. Preserve any native tree and relative imports those definitions need. These copies are generated outputs covered by the same drift check, never a second hand-edited source. Readers download or link to the published copies without following a link into a design folder.
- **Examples are available with the pages.** Put copyable examples and downloadable sample files in `docs/user/`, and validate them against their definitions. A link to an example hidden in a design folder is not a substitute.
- **Check the published result.** The documentation check resolves page links, fragments, images and downloads as published, and rejects links into design documents. A link that works in the source repository can still leave the published documentation incomplete.

## Show the interface

- **A page about an interface shows it.** Embed screenshots of the relevant graphical or terminal interface and its result. A page describing a workflow also embeds an animated recording of that workflow.
- **Captures are reproducible.** Commit the scripts and inputs that regenerate screenshots and recordings, with the command and the assets it produces documented in the repository. Use the interface and version the page describes, with synthetic data and no credentials or private content.
- **The text carries the instructions too.** Give images alternative text and recordings a written description. Write out each action and expected result so the reader can follow without viewing the media.

## Keeping it true

- **A change ships with its documentation.** A pull request that changes what a user sees or does updates the pages it affects, and review checks it.
- **The documentation lives with what it describes:** a component's in its repository, and pages spanning several components in the product repository, as [designing](../../designing/references/documents.md#where-it-goes) places design documents.
- **Published output is verified with its pages.** Run reference generation, link and example checks, and the capture scripts affected by the change before review.
