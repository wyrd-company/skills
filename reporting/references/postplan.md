# Postplan

Read this when you publish a static page or deck to Postplan, or when someone gives you a `postplan.dev` URL to read. Postplan hosts HTML at a shareable URL. The `postplan` CLI is on the PATH. `postplan --help` and `postplan <command> --help` list its commands and flags.

## Publish

1. **Check the account and its limits** before you build a large, multi-page or scripted page: `postplan check --json`. It reports the account, the upload size limit and what the account may use. Uploads need a signed-in account: when it reports a sign-in error, ask the operator to run `postplan auth login` before you build the page. When the page will not fit, split it into linked pages rather than dropping content, or serve it from [this workspace](workspace-site.md).
2. **Write the page** as one self-contained file. Postplan blocks external scripts (`<script src>`), forms, iframes, embeds, objects, `javascript:` URLs and meta refresh. Inline scripts run in a sandbox with no storage, cookies or network access. Stylesheets, images, video and fonts may load from any `https` URL, but not from a local path: first upload media as the [`public-assets` skill](../../public-assets/SKILL.md) says, and link the URL it returns.
3. **Validate the file:** `postplan check <path>`. Fix every error, and treat each warning as something that will break for the reader. Done when it prints `Ready.`
4. **Upload from the right checkout:** `postplan upload <path> --description "<one line>" --json`. Postplan records the repository of the Git checkout containing the file, so write the file inside the repository the page is about. Read the exit status directly, without piping through `head` or `tail`.
5. **Hand over the receipt:** the `url`, and `versionUrl` when the reader needs that exact version. The page is published only when the receipt says `"ok": true`.

A folder with an `index.html` uploads as a multi-page document, with pages linked by relative paths.

## Update

Uploading the same absolute path again on the same machine updates the same page. To update from another path or machine, pass `--draft <id>`. Give a page a stable custom URL with `--slug <name>` when the account allows custom URLs. Use `--new` only when the reader wants a separate page. To edit a page you do not have locally, use `postplan download <url> --json`.

## Read

When given a `postplan.dev` URL, fetch it with `curl` into a fresh file and read that. Every client gets the uploaded HTML unchanged, so a web tool that refuses the URL is a limit of that tool and says nothing about Postplan. Remove a `#fragment` but keep the path, since `/v/<n>` pins a version. If `curl` fails, report its HTTP status or network error.
