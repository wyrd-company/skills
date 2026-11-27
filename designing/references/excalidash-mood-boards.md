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
The [board script](../scripts/excalidash-board.py) uses the workspace's
`bao` access and reads the key into memory for each invocation.

## Create the user configuration file

Run the script with `uv run`. Its inline dependency declaration lets uv
supply PyYAML in an isolated environment.

Create the configuration directory and file in your user config directory.
Replace the example values with the ExcaliDash origin and OpenBao entry
your operator configured.

```bash
config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/excalidash"
mkdir -p "$config_dir"
```

Save this YAML as `config.yml` in that directory. It contains only the
three non-secret settings. The API key belongs in OpenBao.

```yaml
url: "https://excalidash.example.com"
vault-mount: "secret"
vault-path: "tools/excalidash"
```

The script reads `~/.config/excalidash/config.yml` by default, or uses
`$XDG_CONFIG_HOME/excalidash/config.yml` when `XDG_CONFIG_HOME` is set.
Pass `--config /path/to/config.yml` before the subcommand to use another
file. In a managed workspace, have the operator manage this non-secret
file in the workspace dotfiles with chezmoi so it survives a rebuild.
[Workspace configuration standard](../../standards/references/workspace.md#where-configuration-belongs)

## Find and read a board

Set `skill_dir` to the absolute path of the installed designing skill. The
examples use the default location for Codex and Pi. Run the commands from
any directory. Relative input paths resolve from your current directory.

```bash
skill_dir="$HOME/.agents/skills/designing"
uv run "$skill_dir/scripts/excalidash-board.py" list 'Mood board' --limit 10 --offset 0
uv run "$skill_dir/scripts/excalidash-board.py" read 'https://excalidash.example.com/editor/drawing-id'
```

The list command prints `drawings`, `totalCount`, `limit`, and `offset`.
It searches boards owned by the account that issued the key. Increase
`offset` to page through matches. The read command accepts a
drawing ID or an editor link on the configured instance and prints the
scene JSON, including the drawing version, elements, app state, and files.
Stored image entries can point to URLs that require a signed-in session.

## Publish a board for the operator

Run [the board script](../scripts/excalidash-board.py) with uv. Pass a PNG screenshot for a mood board or an Excalidraw scene
export for an editable diagram. Include the image data in any scene export
that references images.

```bash
uv run "$skill_dir/scripts/excalidash-board.py" publish 'Mood board — Website redesign' reference.png
uv run "$skill_dir/scripts/excalidash-board.py" publish 'Record ownership' ownership.excalidraw
```

Each run creates a new board and prints its editor URL as soon as it exists.
For a populated board, the script checks the saved scene with a fresh GET.
The ExcaliDash account that issued the API key owns the board. Have that
account share the board through the editor and grant edit access if the
operator will annotate it. Send the link and the question to review. Ask the operator to check the
canvas while signed in.

## Collect a diagram from the operator

Ask for an existing editor link if the operator already has a diagram. If
they need a canvas, run the board script with only a title.

```bash
uv run "$skill_dir/scripts/excalidash-board.py" publish 'Design sketch'
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

Publish the first screenshot with `publish`, then use `add` to place more
PNGs to the right of the existing content.

```bash
uv run "$skill_dir/scripts/excalidash-board.py" add drawing-id first.png second.png
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
ExcaliDash stores uploaded image bytes separately and returns a stored file
URL in the scene. Keep the original PNG if you need its bytes for another board or
export. The drawing key can receive `404` on the stored file URL.

[Drawing read implementation](https://github.com/ZimengXiong/ExcaliDash/blob/c1013c0de630b3efeea6a11851adc039c2d2afe3/backend/src/routes/dashboard/drawingReadRoutes.ts)
and [drawing write implementation](https://github.com/ZimengXiong/ExcaliDash/blob/c1013c0de630b3efeea6a11851adc039c2d2afe3/backend/src/routes/dashboard/drawingCreateUpdateRoutes.ts).
