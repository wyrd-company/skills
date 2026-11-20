"""Scenario tests for the workspace manager's scripts.

They run takeover.sh and budget.sh against scratch kanban-md boards, with the
real kanban-md and a stand-in t3c. They are skipped where kanban-md, jq or
flock is not installed.
"""

import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "workspace-management" / "scripts"
TEMPLATE = ROOT / "workspace-management" / "assets" / "manager-task.md"
TOOLS = ("kanban-md", "jq", "flock")


@unittest.skipUnless(all(shutil.which(t) for t in TOOLS), "needs kanban-md, jq and flock")
class TakeoverTests(unittest.TestCase):
    def setUp(self):
        self.board = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.board)
        subprocess.run(
            ["kanban-md", "init", "--dir", str(self.board)],
            input="n\n",
            text=True,
            capture_output=True,
            check=True,
        )
        self.create(TEMPLATE.read_text())

    def kb(self, *args):
        out = subprocess.run(
            ["kanban-md", "--json", *args, "--dir", str(self.board)],
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        return json.loads(out)

    def create(self, body):
        return self.kb(
            "create",
            "Workspace manager",
            "--status",
            "todo",
            "--tags",
            "workspace-manager",
            "--body",
            body,
        )["id"]

    def takeover(self, thread, expected="-"):
        env = {
            **os.environ,
            "MANAGER_BOARD": str(self.board),
            "T3CODE_THREAD_ID": thread,
            "WORKSPACE": "test",
        }
        run = subprocess.run(
            ["bash", str(SCRIPTS / "takeover.sh"), expected],
            env=env,
            text=True,
            capture_output=True,
        )
        out = json.loads(run.stdout) if run.stdout.strip() else None
        return run.returncode, out

    def open_tasks(self):
        return self.kb("list", "--tag", "workspace-manager")

    def pointer(self):
        return json.loads((self.board / "manager.json").read_text())

    def body(self, task_id):
        return self.kb("show", str(task_id))["body"]

    def set_body(self, task_id, body):
        claim = self.kb("show", str(task_id)).get("claimed_by")
        self.kb("edit", str(task_id), "--body", body, *(["--claim", claim] if claim else []))

    def set_roll_interval(self, task_id, days):
        body = self.body(task_id).replace(
            "- Roll forward every: 1 day", f"- Roll forward every: {days} days"
        )
        self.set_body(task_id, body)

    def test_first_shift_and_handover(self):
        code, out = self.takeover("a")
        self.assertEqual((code, out["previous_threads"]), (0, []))
        code, out = self.takeover("b", "a")
        self.assertEqual((code, out["previous_threads"]), (0, ["a"]))
        self.assertEqual(self.pointer()["thread_id"], "b")
        self.assertEqual(self.open_tasks()[0]["claimed_by"], "b")

    def test_overlapping_shift_is_refused(self):
        self.takeover("a")
        self.takeover("b", "a")
        code, out = self.takeover("c", "a")
        self.assertEqual((code, out), (3, {"holder": "b"}))
        self.assertEqual(self.pointer()["thread_id"], "b")

    def test_overlapping_roll_leaves_one_manager(self):
        self.takeover("a")
        self.set_roll_interval(self.open_tasks()[0]["id"], 0)
        self.takeover("b", "a")
        code, _ = self.takeover("c", "a")
        self.assertEqual(code, 3)
        claimed = [t for t in self.open_tasks() if t.get("claimed_by")]
        self.assertEqual([t["claimed_by"] for t in claimed], ["b"])

    def test_roll_carries_the_standing_state_only(self):
        self.takeover("a")
        old = self.open_tasks()[0]["id"]
        self.set_roll_interval(old, 0)
        code, out = self.takeover("b", "a")
        self.assertEqual((code, out["rolled_from"]), (0, old))
        [current] = self.open_tasks()
        body = self.body(current["id"])
        self.assertIn(f"- Previous task: #{old}", body)
        self.assertIn("## Budget", body)
        self.assertNotIn("Takeover by a", body)
        self.assertIn("Takeover by b from a. Rolled forward from", body)
        self.assertEqual(self.kb("list", "--archived")[0]["id"], old)

    def test_log_heading_in_a_code_block_is_not_the_log(self):
        text = TEMPLATE.read_text().replace(
            "## Requests", "## Requests\n\n```markdown\n## Log\n```\n", 1
        )
        self.kb("delete", "1", "--yes")
        task = self.create(text)
        self.takeover("a")
        self.set_roll_interval(task, 0)
        code, out = self.takeover("b", "a")
        self.assertEqual((code, out["roll_skipped"]), (0, None))
        body = self.body(out["task"])
        for section in ("## Holds", "## Notices", "## Budget"):
            self.assertIn(section, body)

    def test_roll_skipped_when_a_section_is_missing(self):
        text = TEMPLATE.read_text().replace("## Notices", "## Other", 1)
        self.kb("delete", "1", "--yes")
        task = self.create(text)
        self.takeover("a")
        self.set_roll_interval(task, 0)
        code, out = self.takeover("b", "a")
        self.assertEqual((code, out["rolled_from"]), (0, None))
        self.assertIn("Notices", out["roll_skipped"])
        self.assertEqual(self.pointer()["thread_id"], "b")

    def test_retry_after_release_keeps_the_previous_shift(self):
        self.takeover("a")
        task = self.open_tasks()[0]["id"]
        # b recorded its progress and released a's claim, then stopped.
        (self.board / ".takeover.json").write_text(
            json.dumps({"thread": "b", "previous": ["a"], "rolled_from": None})
        )
        self.kb("edit", str(task), "--release")
        code, out = self.takeover("b", "a")
        self.assertEqual((code, out["previous_threads"]), (0, ["a"]))
        self.assertFalse((self.board / ".takeover.json").exists())

    def test_later_shift_settles_a_cut_short_takeover(self):
        self.takeover("a")
        (self.board / ".takeover.json").write_text(
            json.dumps({"thread": "b", "previous": ["a"], "rolled_from": None})
        )
        code, out = self.takeover("c", "a")
        self.assertEqual((code, out["previous_threads"]), (0, ["a", "b"]))

    def test_closed_but_unarchived_manager_task_is_archived(self):
        self.takeover("a")
        old = self.open_tasks()[0]["id"]
        new = self.create(TEMPLATE.read_text())
        self.kb("edit", str(old), "--release", "--status", "done", "--completed", "2026-01-01")
        code, out = self.takeover("b", "-")
        self.assertEqual((code, out["task"]), (0, new))
        self.assertEqual([t["id"] for t in self.kb("list", "--archived")], [old])

    def test_running_again_logs_once(self):
        self.takeover("a")
        self.takeover("a")
        body = self.body(self.open_tasks()[0]["id"])
        self.assertEqual(body.count("Takeover by a"), 1)


@unittest.skipUnless(all(shutil.which(t) for t in TOOLS), "needs kanban-md, jq and flock")
class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.board = self.tmp / "board"
        self.board.mkdir()
        subprocess.run(
            ["kanban-md", "init", "--dir", str(self.board)],
            input="n\n",
            text=True,
            capture_output=True,
            check=True,
        )
        body = TEMPLATE.read_text().replace("{amount}", "100")
        out = subprocess.run(
            [
                "kanban-md",
                "--json",
                "create",
                "Workspace manager",
                "--status",
                "todo",
                "--tags",
                "workspace-manager",
                "--body",
                body,
                "--dir",
                str(self.board),
            ],
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        (self.board / "manager.json").write_text(json.dumps({"task_id": json.loads(out)["id"]}))
        self.bin = self.tmp / "bin"
        self.bin.mkdir()

    def budget(self, buckets):
        today = subprocess.run(["date", "-u", "+%F"], text=True, capture_output=True).stdout.strip()
        usage = {"data": {"buckets": [{"day": today, "provider": "claude", **b} for b in buckets]}}
        (self.tmp / "usage.json").write_text(json.dumps(usage))
        t3c = self.bin / "t3c"
        t3c.write_text(
            textwrap.dedent(f"""\
            #!/bin/sh
            cat {self.tmp / "usage.json"}
            """)
        )
        t3c.chmod(0o755)
        env = {
            **os.environ,
            "PATH": f"{self.bin}:{os.environ['PATH']}",
            "MANAGER_BOARD": str(self.board),
        }
        run = subprocess.run(
            ["bash", str(SCRIPTS / "budget.sh")], env=env, text=True, capture_output=True
        )
        return run.returncode, run.stdout.splitlines()[0]

    def test_unpriced_usage_makes_the_spend_unknown(self):
        self.assertEqual(
            self.budget([{"costUsd": 0, "unpricedTokens": 900000, "unpricedRecords": 3}]),
            (0, "budget: unknown"),
        )

    def test_spend_past_the_budget_is_at(self):
        self.assertEqual(self.budget([{"costUsd": 150}]), (0, "budget: at"))

    def test_budget_row_below_the_log_is_ignored(self):
        task = json.loads((self.board / "manager.json").read_text())["task_id"]
        body = TEMPLATE.read_text().replace("{amount}", "lots")
        body += "\n| Daily budget (USD at list price, all providers) | 1000 |\n"
        subprocess.run(
            ["kanban-md", "edit", str(task), "--body", body, "--dir", str(self.board)],
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(self.budget([{"costUsd": 1}]), (0, "budget: unset"))


if __name__ == "__main__":
    unittest.main()
