# The public assets bucket

Read this when a report, a pull request, an issue or a Discord message needs an image, a recording or a file that its host cannot store, or that a Postplan page has to load over `https`.

Media goes in the public R2 bucket `assets-wyrd-foo`, through the AWS CLI profile of the same name. Anything uploaded there can be fetched by anyone who has the URL, so upload only what you would publish.

Name the object for what it belongs to:

| It belongs to | Object path |
|---|---|
| A pull request | `<repo>/pr-<number>/<file>` |
| An issue | `<repo>/issue-<number>/<file>` |
| A report with neither | `<repo>/reports/<report-name>/<file>` |

```sh
aws --profile assets-wyrd-foo s3 cp ./login.png s3://assets-wyrd-foo/example-repo/pr-123/login.png
```

Link it as `https://assets.wyrd.foo/<object-path>`: here, `https://assets.wyrd.foo/example-repo/pr-123/login.png`.

A successful upload does not prove the reader can fetch the file. Fetch the public URL without credentials and confirm a `200` before you link it:

```sh
curl -s -o /dev/null -w '%{http_code}\n' https://assets.wyrd.foo/example-repo/pr-123/login.png
```

When it does not return `200`, the file is not available to the reader. Put the content inline instead, for example the script and its output in the comment, and report that the link failed.
