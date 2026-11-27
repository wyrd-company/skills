import io
import json
import os
import runpy
import struct
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread
from unittest.mock import patch
from urllib.error import HTTPError

SCRIPT = Path(__file__).resolve().parents[1] / "designing/scripts/excalidash-board.py"
ORIGIN = "https://excalidash.example.com"
CONFIG = f"""\
url: "{ORIGIN}"
vault-mount: "secret"
vault-path: "tools/excalidash"
"""
PNG_HEADER = b"\x89PNG\r\n\x1a\n" + struct.pack(">I4sII", 13, b"IHDR", 960, 640)


class BoardTests(unittest.TestCase):
    def invoke(self, args, send, vault_error=None, *, key="key-from-vault", export=None):
        output = io.StringIO()
        with (
            patch.dict(
                os.environ,
                {
                    "EXCALIDASH_URL": "https://ignored.example.com",
                    "EXCALIDASH_API_KEY": "ignored-environment-value",
                },
            ),
            patch.object(Path, "read_text", side_effect=[CONFIG, export]) as config_read,
            patch.object(sys, "argv", [str(SCRIPT), "--config", "/test/config.yml", *args]),
            patch.object(Path, "read_bytes", return_value=PNG_HEADER),
            patch(
                "subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, key, ""),
                side_effect=vault_error,
            ) as bao,
            patch("urllib.request.build_opener") as opener,
            redirect_stdout(output),
        ):
            opener.return_value.open.side_effect = send
            runpy.run_path(str(SCRIPT), run_name="__main__")
        self.assertEqual(config_read.call_count, 1 + (export is not None))
        bao.assert_called_once_with(
            ["bao", "kv", "get", "-field=api_key", "-mount=secret", "tools/excalidash"],
            capture_output=True,
            text=True,
            check=True,
            timeout=15,
        )
        self.assertNotIn("key-from-vault", output.getvalue())
        return output.getvalue()

    def test_reads_editor_url_with_vault_key(self):
        def send(req, timeout):
            self.assertEqual(req.get_method(), "GET")
            self.assertEqual(req.full_url, ORIGIN + "/api/drawings/board?omitPreview=1")
            self.assertEqual(req.get_header("Authorization"), "Bearer key-from-vault")
            return io.BytesIO(b'{"version": 4, "elements": []}')

        output = self.invoke(["read", ORIGIN + "/editor/board"], send)
        self.assertEqual(json.loads(output)["version"], 4)

    def test_publish_editable_scene_prints_link_and_verifies(self):
        elements = [{"id": "box", "type": "rectangle"}]
        export = json.dumps({"elements": elements})
        methods = []

        def send(req, timeout):
            method = req.get_method()
            methods.append(method)
            if method == "POST":
                self.assertEqual(json.loads(req.data)["elements"], elements)
                return io.BytesIO(b'{"id": "board", "version": 1}')
            self.assertEqual(req.full_url, ORIGIN + "/api/drawings/board?omitPreview=1")
            return io.BytesIO(
                json.dumps({"version": 1, "elements": elements, "files": {}}).encode()
            )

        output = self.invoke(["publish", "Diagram", "scene.excalidraw"], send, export=export)
        self.assertEqual(methods, ["POST", "GET"])
        self.assertEqual(
            output.splitlines(), [ORIGIN + "/editor/board", "Verified drawing version 1."]
        )

    def test_publish_rejects_export_with_unembedded_image(self):
        export = json.dumps(
            {
                "elements": [{"id": "image", "type": "image", "fileId": "attachment"}],
                "files": {"attachment": {"dataURL": "/api/files/board/attachment"}},
            }
        )
        with (
            patch.object(sys, "argv", [str(SCRIPT), "publish", "Diagram", "scene.excalidraw"]),
            patch.object(Path, "read_text", side_effect=[CONFIG, export]),
            patch("subprocess.run") as bao,
            redirect_stderr(io.StringIO()) as errors,
            self.assertRaises(SystemExit),
        ):
            try:
                runpy.run_path(str(SCRIPT), run_name="__main__")
            finally:
                bao.assert_not_called()
                self.assertIn("with its image data embedded", errors.getvalue())

    def test_vault_rejects_multiline_key_without_printing_it(self):
        errors = io.StringIO()

        def send(req, timeout):
            self.fail("No HTTP request should use a malformed key.")

        with redirect_stderr(errors), self.assertRaises(SystemExit):
            self.invoke(["list"], send, key="first-secret-line\nsecond-secret-line")
        self.assertIn("single API key", errors.getvalue())
        self.assertNotIn("secret-line", errors.getvalue())

    def test_rejected_publish_sends_populated_create_only(self):
        methods = []

        def send(req, timeout):
            methods.append(req.get_method())
            payload = json.loads(req.data)
            (element,) = payload["elements"]
            self.assertIn(element["fileId"], payload["files"])
            raise HTTPError(req.full_url, 413, "Too large", {}, None)

        with self.assertRaisesRegex(SystemExit, "HTTP 413"):
            self.invoke(["publish", "Mood board", "reference.png"], send)
        self.assertEqual(methods, ["POST"])

    def test_add_preserves_scene_and_lays_out_multiple_images(self):
        original = {
            "version": 4,
            "elements": [{"id": "existing", "x": 20, "width": 100}],
            "appState": {"viewBackgroundColor": "#fff"},
            "files": {"existing": {"dataURL": "/api/files/board/existing"}},
        }
        scene = original
        methods = []

        def send(req, timeout):
            nonlocal scene
            method = req.get_method()
            methods.append(method)
            if method == "PUT":
                payload = json.loads(req.data)
                self.assertEqual(payload["version"], 4)
                self.assertEqual(payload["appState"], original["appState"])
                self.assertEqual(payload["files"]["existing"], original["files"]["existing"])
                existing, first, second = payload["elements"]
                self.assertEqual(existing, original["elements"][0])
                self.assertEqual(first["x"], 160)
                self.assertEqual(second["x"], first["x"] + first["width"] + 40)
                for element in (first, second):
                    self.assertIn(element["fileId"], payload["files"])
                scene = {**payload, "version": 5}
            return io.BytesIO(json.dumps(scene).encode())

        output = self.invoke(["add", "board", "one.png", "two.png"], send)
        self.assertEqual(methods, ["GET", "PUT", "GET"])
        self.assertIn("Verified drawing version 5", output)

    def test_add_conflict_stops_after_one_write(self):
        methods = []

        def send(req, timeout):
            methods.append(req.get_method())
            if req.get_method() == "PUT":
                raise HTTPError(req.full_url, 409, "Conflict", {}, None)
            return io.BytesIO(b'{"version": 1, "elements": [], "appState": {}, "files": {}}')

        with self.assertRaisesRegex(SystemExit, "Read the latest scene"):
            self.invoke(["add", "board", "reference.png"], send)
        self.assertEqual(methods, ["GET", "PUT"])

    def test_vault_denial_stops_before_http(self):
        def send(req, timeout):
            self.fail("No HTTP request should follow a vault error.")

        errors = io.StringIO()
        with redirect_stderr(errors), self.assertRaises(SystemExit):
            self.invoke(
                ["read", "board"],
                send,
                subprocess.CalledProcessError(1, ["bao"], stderr="403 sensitive detail"),
            )
        self.assertIn("Vault denied access", errors.getvalue())
        self.assertNotIn("sensitive detail", errors.getvalue())

    def test_invalid_configuration_stops_before_vault(self):
        for payload in ("[", "api_key: do-not-print", CONFIG.replace("https:", "http:")):
            with (
                self.subTest(payload=payload),
                patch.object(sys, "argv", [str(SCRIPT), "list"]),
                patch.dict(os.environ, {"XDG_CONFIG_HOME": "/test/config"}),
                patch.object(Path, "read_text", autospec=True, return_value=payload) as config_read,
                patch("subprocess.run") as bao,
                redirect_stderr(io.StringIO()) as errors,
                self.assertRaises(SystemExit),
            ):
                try:
                    runpy.run_path(str(SCRIPT), run_name="__main__")
                finally:
                    config_read.assert_called_once_with(
                        Path("/test/config/excalidash/config.yml"), encoding="utf-8"
                    )
                    bao.assert_not_called()
                    self.assertIn("/test/config/excalidash/config.yml", errors.getvalue())
                    self.assertNotIn("do-not-print", errors.getvalue())

    def test_foreign_editor_url_stops_before_vault(self):
        with (
            patch.object(
                sys, "argv", [str(SCRIPT), "read", "https://elsewhere.example/editor/board"]
            ),
            patch.object(Path, "read_text", return_value=CONFIG),
            patch("subprocess.run") as bao,
            redirect_stderr(io.StringIO()) as errors,
            self.assertRaises(SystemExit),
        ):
            try:
                runpy.run_path(str(SCRIPT), run_name="__main__")
            finally:
                bao.assert_not_called()
                self.assertIn("configured instance", errors.getvalue())

    def test_add_requires_elements_in_read_back(self):
        scene = {"version": 1, "elements": [], "appState": {}, "files": {}}

        def send(req, timeout):
            if req.get_method() == "PUT":
                scene["version"] = 2
            return io.BytesIO(json.dumps(scene).encode())

        with self.assertRaisesRegex(SystemExit, "expected elements and files"):
            self.invoke(["add", "board", "reference.png"], send)

    def test_request_refuses_redirect_before_forwarding_key(self):
        calls = []

        class RedirectServer(BaseHTTPRequestHandler):
            def do_GET(self):
                calls.append((self.path, self.headers.get("Authorization")))
                if self.path == "/api/drawings":
                    self.send_response(302)
                    self.send_header("Location", "/destination")
                else:
                    self.send_response(200)
                self.end_headers()

            def log_message(self, *args):
                pass

        request = runpy.run_path(str(SCRIPT))["request"]
        with HTTPServer(("127.0.0.1", 0), RedirectServer) as server:
            thread = Thread(target=server.serve_forever)
            thread.start()
            try:
                with self.assertRaises(HTTPError) as error:
                    request(
                        f"http://127.0.0.1:{server.server_port}", "test-key", "GET", "/drawings"
                    )
                error.exception.close()
                self.assertEqual(error.exception.code, 302)
            finally:
                server.shutdown()
                thread.join()
        self.assertEqual(calls, [("/api/drawings", "Bearer test-key")])
