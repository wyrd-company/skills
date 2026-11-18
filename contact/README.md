# contact

The skill an agent uses to reach a person outside its thread: to ask a question, send a notification, or wait for a reply. People are reached in Discord through the `deck` CLI. The skill says where to post, whom to mention, and how to treat the reply that wakes the thread; `deck skill` and `deck --help` hold the CLI's own usage. `executing` points to it when work is blocked on a person.

The workspace installs `deck` and writes its configuration through `workspace-dotfiles`; see its [deck](https://github.com/wyrd-company/workspace-dotfiles/blob/main/docs/deck.md) document.

| File | What it is for |
|---|---|
| [SKILL.md](SKILL.md) | Sending through `deck`, and replies |

## Sources

The skill is written in our own words. It draws on no other skill.

Formats and tools the skill uses, rather than drew on:

| Source | License | Use |
|---|---|---|
| [Deck](https://wyrd.foo/tools/deck), version 0.1.2 | Ours | The `deck` CLI the skill names, and its `deck skill` guide. |
| `wyrd-company/workspace-dotfiles`: `docs/deck.md` | Ours | How the workspace installs and configures `deck`. |
