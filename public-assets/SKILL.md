---
name: public-assets
description: >
  Use when you need a public URL for an image, recording or file: evidence for a pull request or issue, media for a report or Postplan page, or an attachment for Discord. Covers the `assets-wyrd-foo` bucket, object paths, uploading with the AWS CLI and checking the public URL. Not for deciding what evidence to collect (`executing`) or how to present it (`reporting`).
---

# Public assets

Media goes in the public R2 bucket `assets-wyrd-foo`, through the AWS CLI profile of the same name, and is served at `https://assets.wyrd.foo/<object-path>`. Anyone with the URL can fetch it, so upload only what you would publish: no secrets, tokens, private URLs or local file paths in the file or its name.

## Object paths

Name the object for what it belongs to:

| It belongs to | Object path |
|---|---|
| A pull request | `<repo>/pr-<number>/<file>` |
| An issue | `<repo>/issue-<number>/<file>` |
| A report with neither | `<repo>/reports/<report-name>/<file>` |

## Upload and check

```sh
aws --profile assets-wyrd-foo s3 cp ./login.png s3://assets-wyrd-foo/example-repo/pr-123/login.png
```

A successful upload does not prove the reader can fetch the file. Fetch the public URL without credentials:

```sh
curl -s -o /dev/null -w '%{http_code}\n' https://assets.wyrd.foo/example-repo/pr-123/login.png
```

Link the URL only after this prints `200`. When it prints anything else, the file is not available to the reader. Put the content inline instead, such as the script and its output in the comment, and report that the link failed.
