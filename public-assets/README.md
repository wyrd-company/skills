# public-assets

The skill an agent uses to put an image, recording or file at a public URL: the `assets-wyrd-foo` R2 bucket, served at `https://assets.wyrd.foo`. `executing` points to it for review evidence, and `reporting` for media in reports and Postplan pages. Agents that need only the bucket can read it without loading either.

The workspace provides the `assets-wyrd-foo` AWS CLI profile through `workspace-dotfiles`.

| File | What it is for |
|---|---|
| [SKILL.md](SKILL.md) | Object paths, uploading, and checking the public URL |

## Sources

The skill is written in our own words. It draws on no other skill. Its rules moved here from `executing`.

Formats and tools the skill uses, rather than drew on:

| Source | License | Use |
|---|---|---|
| [AWS CLI](https://aws.amazon.com/cli/) | Apache-2.0 | Uploading to the R2 bucket through its S3 API. |
