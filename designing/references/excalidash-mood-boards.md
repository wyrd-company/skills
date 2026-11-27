# Mood boards and design diagrams with the ExcaliDash REST API

Read this when a design benefits from a shared sketch or mood board.
Use ExcaliDash to collect reference screenshots, color swatches, and design
notes on an editable Excalidraw board. Share the editor link with a reviewer
who has access so they can rearrange references and annotate the canvas.

## Set up vault access

Ask the operator to provision the vault entry and grant workspace access.

In ExcaliDash settings, the operator creates an account API key with **Read drawings**.
Include **Write drawings** if the workspace will publish boards. Save the
key in the `api_key` field of a dedicated OpenBao KV entry. Use your vault's
secret entry form, or run this from a Bash shell with permission to create
the entry. Replace the example mount and path with the ones for your workspace.

```bash
(
  set +ax
  unset excalidash_key
  read -rsp 'ExcaliDash API key: ' excalidash_key || exit
  printf '\n' >&2
  printf '%s' "$excalidash_key" |
    bao kv put -mount=secret tools/excalidash api_key=-
)
```

Grant the workspace's Wyrwood identity read access to that entry. For a KV v2
mount, the policy path for the example is `secret/data/tools/excalidash`.
Keep the non-secret settings below in the workspace's local configuration,
for example in `.config/excalidash.env` at the workspace root. Source that
file in the same shell invocation as the board command, or export the values
in the current interactive shell.

```bash
export EXCALIDASH_URL='https://excalidash.example.com'
export EXCALIDASH_VAULT_MOUNT='secret'
export EXCALIDASH_VAULT_PATH='tools/excalidash'
```

The [board script](../scripts/excalidash-board.py) uses the workspace's
`bao` access and reads the key into memory for each invocation.

## Find and read a board

Run these commands from the designing skill directory.

```bash
python3 scripts/excalidash-board.py list 'Mood board' --limit 10 --offset 0
python3 scripts/excalidash-board.py read 'https://excalidash.example.com/editor/drawing-id'
```

The list command prints `drawings`, `totalCount`, `limit`, and `offset`.
Increase `offset` to page through matches. The read command accepts a
drawing ID or an editor link on the configured instance and prints the
scene JSON, including the drawing version, elements, app state, and files.
Stored image entries can point to URLs that require a signed-in session.

## Publish a board for the operator

From the designing skill directory, run [the board script](../scripts/excalidash-board.py)
with Python 3. Pass a PNG screenshot for a mood board or an Excalidraw scene
export for an editable diagram. Include the image data in any scene export
that references images.

```bash
python3 scripts/excalidash-board.py publish 'Mood board — Website redesign' reference.png
python3 scripts/excalidash-board.py publish 'Record ownership' ownership.excalidraw
```

Each run creates a new board and prints its editor URL as soon as it exists.
For a populated board, the script checks the saved scene with a fresh GET.
The ExcaliDash account that issued the API key owns the board. Have that
account share the board through the editor and grant edit access if the
operator will annotate it. Open the URL while signed in and check the canvas
before sending the link and the question to review.

## Collect a diagram from the operator

Ask for an existing editor link if the operator already has a diagram. If
they need a canvas, run the board script with only a title.

```bash
python3 scripts/excalidash-board.py publish 'Design sketch'
```

Have the owning account grant edit access in the editor, then share the
printed URL. Give the operator a specific question to sketch, such as which
steps happen before a handoff or which system owns a record.

When they finish, open the editor URL with an account that has access or
use the board script's `read` command to inspect the scene.
Ask the operator to explain any ambiguous labels or arrows. Link the diagram
from the frame or decision it informed, and record what the operator
confirmed there.

## Edit a board

Use `add` to place one or more PNGs to the right of the existing content.

```bash
python3 scripts/excalidash-board.py add drawing-id first.png second.png
```

The script reads the board with `GET /api/drawings/<id>?omitPreview=1`,
preserves the existing scene, and sends the updated scene with its drawing
version to `PUT /api/drawings/<id>`. It checks the saved scene with a fresh
GET. Use the editor to rearrange the canvas or change existing elements.

On `409 VERSION_CONFLICT`, read the board again and confirm the images
still belong there before rerunning `add`. After an uncertain write, inspect
the board before retrying so you avoid duplicate images. If creation times
out before returning an ID, search for the title first.

An image element's `fileId` matches an entry in the scene's `files` map.
ExcaliDash can replace an image data URL with a stored file URL in later
reads. Keep the original PNG if you need its bytes for another board or
export. The drawing key can receive `404` on the stored file URL.

[Drawing read implementation](https://github.com/ZimengXiong/ExcaliDash/blob/c1013c0de630b3efeea6a11851adc039c2d2afe3/backend/src/routes/dashboard/drawingReadRoutes.ts)
and [drawing write implementation](https://github.com/ZimengXiong/ExcaliDash/blob/c1013c0de630b3efeea6a11851adc039c2d2afe3/backend/src/routes/dashboard/drawingCreateUpdateRoutes.ts).
