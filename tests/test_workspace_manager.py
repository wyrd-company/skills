"""Scenario tests for the workspace manager's scripts.

They run takeover.sh, manager.sh and budget.sh against scratch kanban-md boards,
with the real kanban-md and a stand-in t3c. The CI workflow installs kanban-md;
elsewhere they are skipped when kanban-md, jq or flock is missing.
"""

import fcntl
import json
import os
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "workspace-management" / "scripts"
TEMPLATE = ROOT / "workspace-management" / "assets" / "manager-task.md"
TOOLS = ("kanban-md", "jq", "flock")
HAVE_TOOLS = all(shutil.which(t) for t in TOOLS)
REQUIRE_TOOLS = os.environ.get("REQUIRE_MANAGER_TOOLS") == "1"


def needs_tools(cls):
    """Skip without the tools, unless CI says they must be there."""
    if REQUIRE_TOOLS:
        return cls
    return unittest.skipUnless(HAVE_TOOLS, "needs kanban-md, jq and flock")(cls)


class Board:
    """A scratch kanban-md board with one manager task from the template."""

    def __init__(self, case, body=None):
        self.dir = Path(tempfile.mkdtemp())
        case.addCleanup(shutil.rmtree, self.dir)
        subprocess.run(
            ["kanban-md", "init", "--dir", str(self.dir)],
            input="n\n",
            text=True,
            capture_output=True,
            check=True,
        )
        self.first = self.create(body if body is not None else TEMPLATE.read_text())

    def kb(self, *args):
        out = subprocess.run(
            ["kanban-md", "--json", *args, "--dir", str(self.dir)],
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        return json.loads(out)

    def create(self, body, tags="workspace-manager"):
        args = ["create", "Workspace manager", "--status", "todo", "--body", body]
        return self.kb(*args, *(["--tags", tags] if tags else []))["id"]

    def run(self, script, thread, *args, background=False):
        env = {
            **os.environ,
            "MANAGER_BOARD": str(self.dir),
            "T3CODE_THREAD_ID": thread,
            "WORKSPACE": "test",
        }
        cmd = ["bash", str(SCRIPTS / script), *args]
        if background:
            return subprocess.Popen(cmd, env=env, text=True, stdout=subprocess.PIPE)
        run = subprocess.run(cmd, env=env, text=True, capture_output=True)
        return run.returncode, run.stdout

    def takeover(self, thread, expected="-"):
        code, out = self.run("takeover.sh", thread, expected)
        return code, json.loads(out) if out.strip() else None

    def open_tasks(self):
        return self.kb("list", "--tag", "workspace-manager")

    def pointer(self):
        return json.loads((self.dir / "manager.json").read_text())

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

    def progress(self, **fields):
        (self.dir / ".takeover.json").write_text(json.dumps(fields))


@needs_tools
class TakeoverTests(unittest.TestCase):
    def setUp(self):
        self.b = Board(self)

    def test_first_shift_and_handover(self):
        code, out = self.b.takeover("a")
        self.assertEqual((code, out["previous_threads"]), (0, []))
        code, out = self.b.takeover("b", "a")
        self.assertEqual((code, out["previous_threads"]), (0, ["a"]))
        self.assertEqual(self.b.pointer()["thread_id"], "b")
        self.assertEqual(self.b.open_tasks()[0]["claimed_by"], "b")

    def test_overlapping_shift_is_refused(self):
        self.b.takeover("a")
        self.b.takeover("b", "a")
        code, out = self.b.takeover("c", "a")
        self.assertEqual((code, out), (3, {"holder": "b"}))
        self.assertEqual(self.b.pointer()["thread_id"], "b")

    def test_takeover_waits_for_the_lock(self):
        """C starts while B holds the lock, and must see B's claim when it gets it."""
        self.b.takeover("a")
        with open(self.b.dir / ".manager.lock", "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            c = self.b.run("takeover.sh", "c", "a", background=True)
            time.sleep(1)
            self.assertIsNone(c.poll(), "takeover ran without the lock")
            # What B's takeover does while it holds the lock.
            task = str(self.b.open_tasks()[0]["id"])
            self.b.kb("edit", task, "--release")
            self.b.kb("edit", task, "--claim", "b")
            fcntl.flock(lock, fcntl.LOCK_UN)
        self.assertEqual(c.wait(timeout=30), 3)

    def test_overlapping_roll_leaves_one_manager(self):
        self.b.takeover("a")
        self.b.set_roll_interval(self.b.first, 0)
        self.b.takeover("b", "a")
        code, _ = self.b.takeover("c", "a")
        self.assertEqual(code, 3)
        claimed = [t for t in self.b.open_tasks() if t.get("claimed_by")]
        self.assertEqual([t["claimed_by"] for t in claimed], ["b"])

    def test_roll_carries_the_standing_state_only(self):
        self.b.takeover("a")
        old = self.b.first
        self.b.set_roll_interval(old, 0)
        code, out = self.b.takeover("b", "a")
        self.assertEqual((code, out["rolled_from"]), (0, old))
        [current] = self.b.open_tasks()
        body = self.b.body(current["id"])
        self.assertIn(f"- Previous task: #{old}", body)
        self.assertIn("## In flight", body)
        self.assertNotIn("Takeover by a", body)
        self.assertIn("Takeover by b from a. Rolled forward from", body)
        self.assertEqual(self.b.kb("list", "--archived")[0]["id"], old)

    def test_log_headings_inside_fences_are_not_the_log(self):
        fences = "````markdown\n~~~\n## Log\n~~~\n````\n\n```\n## Log \n```\n"
        b = Board(self, TEMPLATE.read_text().replace("## Requests", "## Requests\n\n" + fences, 1))
        b.takeover("a")
        b.set_roll_interval(b.first, 0)
        code, out = b.takeover("b", "a")
        self.assertEqual((code, out["roll_skipped"], out["rolled_from"]), (0, None, b.first))
        body = b.body(out["task"])
        for section in ("## Holds", "## Notices", "## In flight"):
            self.assertIn(section, body)

    def test_roll_skipped_when_a_section_is_missing(self):
        b = Board(self, TEMPLATE.read_text().replace("## Notices", "## Other", 1))
        b.takeover("a")
        b.set_roll_interval(b.first, 0)
        code, out = b.takeover("b", "a")
        self.assertEqual((code, out["rolled_from"]), (0, None))
        self.assertIn("Notices", out["roll_skipped"])
        self.assertEqual(b.pointer()["thread_id"], "b")

    def test_retry_after_release_keeps_the_previous_shift(self):
        self.b.takeover("a")
        # b recorded its progress and released a's claim, then stopped.
        self.b.progress(status="running", thread="b", previous=["a"], rolled_from=None)
        self.b.kb("edit", str(self.b.first), "--release")
        code, out = self.b.takeover("b", "-")
        self.assertEqual((code, out["previous_threads"]), (0, ["a"]))

    def test_retry_after_finishing_repeats_the_summary(self):
        self.b.takeover("a")
        _, first = self.b.takeover("b", "a")
        since = self.b.pointer()["since"]
        time.sleep(1.1)
        code, again = self.b.takeover("b", "a")
        self.assertEqual((code, again), (0, first))
        self.assertEqual(self.b.pointer()["since"], since)

    def test_later_shift_settles_a_cut_short_takeover(self):
        self.b.takeover("a")
        self.b.progress(status="running", thread="b", previous=["a"], rolled_from=None)
        code, out = self.b.takeover("c", "a")
        self.assertEqual((code, out["previous_threads"]), (0, ["a", "b"]))

    def test_closed_but_unarchived_manager_task_is_archived(self):
        self.b.takeover("a")
        new = self.b.create(TEMPLATE.read_text())
        self.b.kb(
            "edit", str(self.b.first), "--release", "--status", "done", "--completed", "2026-01-01"
        )
        code, out = self.b.takeover("b", "-")
        self.assertEqual((code, out["task"]), (0, new))
        self.assertEqual([t["id"] for t in self.b.kb("list", "--archived")], [self.b.first])

    def test_takeover_text_in_the_standing_state_does_not_hide_the_log_entry(self):
        b = Board(
            self,
            TEMPLATE.read_text().replace(
                "## Holds\n", "## Holds\n\nTakeover by b from a failed.\n"
            ),
        )
        b.takeover("a")
        b.takeover("b", "a")
        log = b.body(b.first).split("\n## Log\n", 1)[1]
        self.assertIn("Takeover by b from a.", log)


@needs_tools
class ManagerTests(unittest.TestCase):
    def setUp(self):
        self.b = Board(self)
        self.b.takeover("a")

    def test_only_the_holder_writes(self):
        code, out = self.b.run("manager.sh", "z", "log", "hello")
        self.assertEqual((code, json.loads(out)), (3, {"holder": "a"}))
        code, _ = self.b.run("manager.sh", "a", "log", "hello")
        self.assertEqual(code, 0)
        self.assertIn("hello", self.b.body(self.b.first))

    def test_superseded_shift_waits_and_is_refused(self):
        """A write that arrives during a takeover waits for it, then is refused."""
        with open(self.b.dir / ".manager.lock", "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            a = self.b.run("manager.sh", "a", "log", "late request", background=True)
            time.sleep(1)
            self.assertIsNone(a.poll(), "write ran without the lock")
            self.b.kb("edit", str(self.b.first), "--release")
            self.b.kb("edit", str(self.b.first), "--claim", "b")
            (self.b.dir / "manager.json").write_text(
                json.dumps({"thread_id": "b", "task_id": self.b.first})
            )
            fcntl.flock(lock, fcntl.LOCK_UN)
        self.assertEqual(a.wait(timeout=30), 3)
        self.assertEqual(json.loads(a.stdout.read()), {"holder": "b"})
        self.assertNotIn("late request", self.b.body(self.b.first))

    def test_set_state_keeps_the_log(self):
        self.b.run("manager.sh", "a", "log", "kept entry")
        _, state = self.b.run("manager.sh", "a", "state")
        new = self.b.dir / "state.md"
        new.write_text(state.replace("## Requests\n", "## Requests\n\n- a request\n"))
        code, _ = self.b.run("manager.sh", "a", "set-state", str(new))
        self.assertEqual(code, 0)
        body = self.b.body(self.b.first)
        self.assertIn("- a request", body)
        self.assertIn("kept entry", body)

    def test_set_state_refuses_a_missing_section(self):
        _, state = self.b.run("manager.sh", "a", "state")
        new = self.b.dir / "state.md"
        new.write_text(state.replace("## Notices", "## Other"))
        code, _ = self.b.run("manager.sh", "a", "set-state", str(new))
        self.assertEqual(code, 1)

    def test_holder_during_a_cut_short_takeover(self):
        self.b.progress(status="running", thread="b", previous=["a"], rolled_from=None)
        code, out = self.b.run("manager.sh", "a", "holder")
        self.assertEqual((code, json.loads(out)), (0, {"holder": "b"}))


@needs_tools
class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.b = Board(self, TEMPLATE.read_text().replace("{amount}", "100"))
        self.b.takeover("a")
        self.bin = self.b.dir / "bin"
        self.bin.mkdir()

    def budget(self, buckets, sources=()):
        today = time.strftime("%Y-%m-%d", time.gmtime())
        usage = {
            "data": {
                "buckets": [{"day": today, "provider": "claude", **b} for b in buckets],
                "sources": list(sources),
            }
        }
        (self.b.dir / "usage.json").write_text(json.dumps(usage))
        t3c = self.bin / "t3c"
        t3c.write_text(f"#!/bin/sh\ncat {self.b.dir / 'usage.json'}\n")
        t3c.chmod(0o755)
        env = {
            **os.environ,
            "PATH": f"{self.bin}:{os.environ['PATH']}",
            "MANAGER_BOARD": str(self.b.dir),
        }
        run = subprocess.run(
            ["bash", str(SCRIPTS / "budget.sh")], env=env, text=True, capture_output=True
        )
        return run.returncode, run.stdout.splitlines()[0]

    def test_below_the_pace(self):
        self.assertEqual(self.budget([{"costUsd": 0}]), (0, "budget: below"))

    def test_unpriced_usage_makes_the_spend_unknown(self):
        bucket = {"costUsd": 0, "unpricedTokens": 900000, "unpricedRecords": 3}
        self.assertEqual(self.budget([bucket]), (0, "budget: unknown"))

    def test_a_failed_source_makes_the_spend_unknown(self):
        source = {"fingerprint": {"provider": "codex"}, "status": "error", "message": "boom"}
        self.assertEqual(self.budget([], [source]), (0, "budget: unknown"))

    def test_spend_past_the_budget_is_at(self):
        self.assertEqual(self.budget([{"costUsd": 150}]), (0, "budget: at"))

    def test_only_the_budget_section_counts(self):
        example = "| Daily budget (USD at list price, all providers) | 5 |\n"
        body = TEMPLATE.read_text().replace("{amount}", "lots")
        body = body.replace("## Channel\n", "## Channel\n\n" + example)
        body += "\n" + example.replace("5", "1000")
        self.b.set_body(self.b.first, body)
        self.assertEqual(self.budget([{"costUsd": 1}]), (0, "budget: unset"))

    def test_a_pointer_to_another_task_is_no_budget(self):
        other = self.b.create(TEMPLATE.read_text().replace("{amount}", "1000"), tags="")
        (self.b.dir / "manager.json").write_text(json.dumps({"task_id": other}))
        self.assertEqual(self.budget([{"costUsd": 1}]), (0, "budget: unset"))


if __name__ == "__main__":
    unittest.main()
