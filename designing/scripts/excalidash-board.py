import argparse
import base64
import json
import os
import re
import secrets
import struct
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from uuid import uuid4


class RefuseRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(origin, api_key, method, path, body=None):
    req = Request(
        origin + "/api" + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method=method,
    )
    with build_opener(RefuseRedirects()).open(req, timeout=15) as response:
        return json.load(response)


def png_scene(path):
    png = path.read_bytes()
    if len(png) < 24 or png[:8] != b"\x89PNG\r\n\x1a\n" or png[12:16] != b"IHDR":
        raise ValueError("Supply a PNG reference image.")
    width, height = struct.unpack(">II", png[16:24])
    if not width or not height:
        raise ValueError("Supply a PNG with nonzero dimensions.")

    scale = min(1, 480 / width, 320 / height)
    timestamp = int(time.time() * 1000)
    file_id = uuid4().hex
    image = {
        "id": uuid4().hex,
        "type": "image",
        "fileId": file_id,
        "status": "saved",
        "x": 60,
        "y": 60,
        "width": width * scale,
        "height": height * scale,
        "scale": [1, 1],
        "crop": None,
        "angle": 0,
        "opacity": 100,
        "strokeColor": "transparent",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "groupIds": [],
        "frameId": None,
        "index": "a0",
        "roundness": None,
        "seed": secrets.randbits(30),
        "version": 1,
        "versionNonce": secrets.randbits(30),
        "isDeleted": False,
        "boundElements": None,
        "updated": timestamp,
        "link": None,
        "locked": False,
    }
    attachment = {
        "id": file_id,
        "mimeType": "image/png",
        "dataURL": "data:image/png;base64," + base64.b64encode(png).decode("ascii"),
        "created": timestamp,
    }

    return {"elements": [image], "appState": {}, "files": {file_id: attachment}}


def read_scene(path):
    if path is None:
        return {"elements": [], "appState": {}, "files": {}}
    if path.suffix.lower() == ".png":
        return png_scene(path)

    scene = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(scene, dict) or not isinstance(scene.get("elements"), list):
        raise ValueError("Supply an Excalidraw export with an elements array.")
    elements = scene["elements"]
    app_state = scene.get("appState", {})
    files = scene.get("files", {})
    if not isinstance(app_state, dict) or not isinstance(files, dict):
        raise ValueError("The scene's appState and files must be objects.")
    for element in elements:
        if not isinstance(element, dict) or not isinstance(element.get("id"), str):
            raise ValueError("Every scene element needs a string id.")
        if element.get("type") == "image" and not element.get("isDeleted"):
            attachment = files.get(element.get("fileId"))
            data_url = attachment.get("dataURL") if isinstance(attachment, dict) else None
            if not isinstance(data_url, str) or not data_url.startswith("data:image/"):
                raise ValueError("Export the scene with its image data embedded.")
    return {"elements": elements, "appState": app_state, "files": files}


def vault_key(mount, path):
    try:
        result = subprocess.run(
            ["bao", "kv", "get", "-field=api_key", f"-mount={mount}", path],
            capture_output=True,
            text=True,
            check=True,
            timeout=15,
        )
    except FileNotFoundError:
        raise ValueError("The bao CLI is required to read the ExcaliDash API key.") from None
    except subprocess.CalledProcessError as error:
        detail = "Vault denied access (403)." if "403" in error.stderr else "Vault read failed."
        raise ValueError(
            f"{detail} Check the configured mount, path, and workspace access."
        ) from None
    except subprocess.TimeoutExpired:
        raise ValueError("The vault read timed out.") from None
    key = result.stdout.strip()
    if not key or "\n" in key or "\r" in key:
        raise ValueError("The vault entry must contain a single API key in the api_key field.")
    return key


def drawing_id(board, origin):
    if board.startswith(origin + "/editor/"):
        board = urlsplit(board).path.removeprefix("/editor/")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", board):
        raise ValueError("Pass a drawing ID or an editor URL on the configured instance.")
    return board


def main():
    parser = argparse.ArgumentParser(
        description="List, read, publish, or add images to ExcaliDash boards."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    publish = commands.add_parser("publish", help="Create a blank or populated board")
    publish.add_argument("title")
    publish.add_argument("source", nargs="?", type=Path, help="PNG or Excalidraw scene export")
    read = commands.add_parser("read", help="Print the drawing scene as JSON")
    read.add_argument("board", help="Drawing ID or editor URL")
    add = commands.add_parser("add", help="Add one or more PNGs to a board")
    add.add_argument("board", help="Drawing ID or editor URL")
    add.add_argument("images", nargs="+", type=Path)
    listing = commands.add_parser("list", help="Search drawings by name")
    listing.add_argument("search", nargs="?", default="")
    listing.add_argument("--limit", type=int, default=10)
    listing.add_argument("--offset", type=int, default=0)
    args = parser.parse_args()

    origin = os.environ.get("EXCALIDASH_URL", "").rstrip("/")
    mount = os.environ.get("EXCALIDASH_VAULT_MOUNT", "")
    path = os.environ.get("EXCALIDASH_VAULT_PATH", "")
    try:
        url = urlsplit(origin)
        port = url.port
    except ValueError:
        parser.error("Set EXCALIDASH_URL to the instance's HTTPS origin.")
    if (
        url.scheme != "https"
        or not url.hostname
        or port == 0
        or url.path
        or url.query
        or url.fragment
        or url.username is not None
        or any(character.isspace() or character == "\\" for character in origin)
    ):
        parser.error("Set EXCALIDASH_URL to the instance's HTTPS origin.")
    if not mount or not path or path.startswith("-"):
        parser.error("Set EXCALIDASH_VAULT_MOUNT and EXCALIDASH_VAULT_PATH.")

    try:
        if args.command == "publish":
            scene = read_scene(args.source)
        elif args.command in {"read", "add"}:
            board = drawing_id(args.board, origin)
            if args.command == "add":
                images = [png_scene(path) for path in args.images]
        api_key = vault_key(mount, path)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    try:
        if args.command == "list":
            query = urlencode({"search": args.search, "limit": args.limit, "offset": args.offset})
            result = request(origin, api_key, "GET", f"/drawings?{query}")
            json.dump(result, sys.stdout, indent=2)
            print()
        elif args.command == "read":
            result = request(origin, api_key, "GET", f"/drawings/{board}?omitPreview=1")
            json.dump(result, sys.stdout, indent=2)
            print()
        elif args.command == "add":
            add_images(origin, api_key, board, images)
        else:
            publish_board(origin, api_key, args.title, scene)
    except HTTPError as error:
        error.close()
        if error.code == 409:
            raise SystemExit("Board changed. Read the latest scene and reapply the edit.") from None
        raise SystemExit(f"ExcaliDash returned HTTP {error.code}.") from None
    except (URLError, TimeoutError):
        raise SystemExit(
            "The ExcaliDash request did not complete. Check the board before retrying a write."
        ) from None


def publish_board(origin, api_key, title, scene):
    created = request(origin, api_key, "POST", "/drawings", {"name": title, **scene})
    print(f"{origin}/editor/{created['id']}", flush=True)
    verify_scene(origin, api_key, created["id"], created["version"], scene)


def add_images(origin, api_key, board, images):
    path = f"/drawings/{board}"
    current = request(origin, api_key, "GET", path + "?omitPreview=1")
    x = (
        max(
            (
                element["x"] + element["width"]
                for element in current["elements"]
                if not element.get("isDeleted")
            ),
            default=20,
        )
        + 40
    )
    additions = {"elements": [], "files": {}}
    for image in images:
        element = image["elements"][0]
        element.update(x=x, index=None)
        additions["elements"].append(element)
        additions["files"].update(image["files"])
        x += element["width"] + 40

    saved = request(
        origin,
        api_key,
        "PUT",
        path,
        {
            "version": current["version"],
            "elements": [*current["elements"], *additions["elements"]],
            "appState": current["appState"],
            "files": {**current["files"], **additions["files"]},
        },
    )
    verify_scene(origin, api_key, board, saved["version"], additions)


def verify_scene(origin, api_key, board, version, scene):
    verified = request(origin, api_key, "GET", f"/drawings/{board}?omitPreview=1")
    expected_ids = {element["id"] for element in scene["elements"] if not element.get("isDeleted")}
    saved_ids = {element["id"] for element in verified["elements"] if not element.get("isDeleted")}
    if (
        verified["version"] < version
        or not expected_ids.issubset(saved_ids)
        or not scene["files"].keys() <= verified["files"].keys()
    ):
        raise SystemExit("The saved scene did not contain the expected elements and files.")
    print(f"Verified drawing version {verified['version']}.")


if __name__ == "__main__":
    main()
