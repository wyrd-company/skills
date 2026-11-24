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
        # b's cut-short takeover makes b the manager: c waits on b, not a.
        self.assertEqual(self.b.takeover("c", "a"), (3, {"holder": "b"}))
        code, out = self.b.takeover("c", "b")
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

    def test_previous_task_changes_only_in_role(self):
        quoted = "## Requests\n\n```text\n- Previous task: #485\n```\n"
        b = Board(self, TEMPLATE.read_text().replace("## Requests\n", quoted, 1))
        b.takeover("a")
        b.set_roll_interval(b.first, 0)
        _, out = b.takeover("b", "a")
        body = b.body(out["task"])
        self.assertIn(f"- Previous task: #{b.first}", body)
        self.assertIn("- Previous task: #485", body)

    def test_an_inline_code_line_opens_no_fence(self):
        text = "## Requests\n\n```inline``` is code\n\n```\nexample\n```\n"
        b = Board(self, TEMPLATE.read_text().replace("## Requests\n", text, 1))
        b.takeover("a")
        b.set_roll_interval(b.first, 0)
        code, out = b.takeover("b", "a")
        self.assertEqual((code, out["roll_skipped"]), (0, None))
        self.assertIn("## Notices", b.body(out["task"]))

    def test_replay_repairs_a_wrong_pointer(self):
        self.b.takeover("a")
        (self.b.dir / "manager.json").write_text(json.dumps({"thread_id": "a", "task_id": 999}))
        code, out = self.b.takeover("a")
        self.assertEqual((code, self.b.pointer()["task_id"]), (0, self.b.first))

    def test_a_takeover_entry_written_before_a_crash_is_not_repeated(self):
        self.b.takeover("a")
        self.b.kb("edit", str(self.b.first), "--release")
        self.b.kb("edit", str(self.b.first), "--claim", "b")
        self.b.kb(
            "edit",
            str(self.b.first),
            "--append-body",
            "Takeover by b from a.",
            "--timestamp",
            "--claim",
            "b",
        )
        self.b.progress(
            status="running", thread="b", previous=["a"], rolled_from=None, logged="pending"
        )
        code, _ = self.b.takeover("b", "a")
        self.assertEqual(code, 0)
        self.assertEqual(self.b.body(self.b.first).count("Takeover by b from a."), 1)

    def test_a_log_line_mentioning_a_takeover_does_not_hide_the_entry(self):
        self.b.takeover("a")
        self.b.run(
            "manager.sh", "a", "log", "Takeover by b from a failed before changing ownership"
        )
        self.b.takeover("b", "a")
        self.assertIn("Takeover by b from a.\n", self.b.body(self.b.first) + "\n")

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

    def read_state(self):
        _, state = self.b.run("manager.sh", "a", "state")
        old = self.b.dir / "old.md"
        old.write_text(state)
        return state, old

    def set_state(self, text, old):
        new = self.b.dir / "new.md"
        new.write_text(text)
        return self.b.run("manager.sh", "a", "set-state", str(new), str(old))[0]

    def test_set_state_keeps_the_log(self):
        self.b.run("manager.sh", "a", "log", "kept entry")
        state, old = self.read_state()
        code = self.set_state(state.replace("## Requests\n", "## Requests\n\n- a request\n"), old)
        self.assertEqual(code, 0)
        body = self.b.body(self.b.first)
        self.assertIn("- a request", body)
        self.assertIn("kept entry", body)

    def test_set_state_refuses_a_missing_section(self):
        state, old = self.read_state()
        self.assertEqual(self.set_state(state.replace("## Notices", "## Other"), old), 1)

    def test_set_state_refuses_a_stale_read(self):
        state, old = self.read_state()
        self.assertEqual(
            self.set_state(state.replace("## Holds\n", "## Holds\n\n- hold\n"), old), 0
        )
        # A second edit made from the first read would drop the hold.
        stale = state.replace("## Requests\n", "## Requests\n\n- request\n")
        self.assertEqual(self.set_state(stale, old), 6)
        self.assertIn("- hold", self.b.body(self.b.first))

    def test_set_state_refuses_an_unclosed_fence(self):
        self.b.run("manager.sh", "a", "log", "kept entry")
        state, old = self.read_state()
        self.assertEqual(self.set_state(state + "\n```\nunclosed\n", old), 1)
        self.assertIn("kept entry", self.b.body(self.b.first))

    def test_state_before_the_first_takeover(self):
        b = Board(self)
        code, out = b.run("manager.sh", "a", "state")
        self.assertEqual(code, 0)
        self.assertIn("## Notices", out)

    def test_set_state_refuses_a_damaged_log_boundary(self):
        self.b.run("manager.sh", "a", "log", "history sentinel")
        body = self.b.body(self.b.first).replace("## Log\n", "## Logbook\n")
        self.b.set_body(self.b.first, body)
        code, out = self.b.run("manager.sh", "a", "state")
        self.assertEqual((code, out), (1, ""))
        old = self.b.dir / "old.md"
        old.write_text(body)
        self.assertEqual(self.set_state(TEMPLATE.read_text().split("## Log")[0], old), 1)
        self.assertIn("history sentinel", self.b.body(self.b.first))

    def test_own_unfinished_takeover_blocks_writes(self):
        self.b.progress(status="running", thread="a", previous=[], rolled_from=None)
        self.assertEqual(self.b.run("manager.sh", "a", "log", "x")[0], 5)

    def test_holder_during_an_unfinished_first_takeover(self):
        (self.b.dir / "manager.json").unlink()
        self.b.progress(status="running", thread="b", previous=[], rolled_from=None)
        code, out = self.b.run("manager.sh", "z", "holder")
        self.assertEqual((code, json.loads(out)), (0, {"holder": "b"}))

    def test_holder_during_a_cut_short_takeover(self):
        self.b.progress(status="running", thread="b", previous=["a"], rolled_from=None)
        code, out = self.b.run("manager.sh", "a", "holder")
        self.assertEqual((code, json.loads(out)), (0, {"holder": "b"}))


@needs_tools
class AdmitTests(unittest.TestCase):
    def setUp(self):
        body = TEMPLATE.read_text().replace(
            "| Agent threads running at once, across the workspace | 12 |",
            "| Agent threads running at once, across the workspace | 3 |",
        )
        self.b = Board(self, body)
        self.b.takeover("a")
        self.bin = self.b.dir / "bin"
        self.bin.mkdir()
        threads = {"data": [{"id": "a", "status": "running"}, {"id": "i", "status": "idle"}]}
        (self.b.dir / "threads.json").write_text(json.dumps(threads))
        t3c = self.bin / "t3c"
        t3c.write_text(f"#!/bin/sh\ncat {self.b.dir / 'threads.json'}\n")
        t3c.chmod(0o755)

    def admit(self, *args, thread="a"):
        env = {
            **os.environ,
            "PATH": f"{self.bin}:{os.environ['PATH']}",
            "MANAGER_BOARD": str(self.b.dir),
            "T3CODE_THREAD_ID": thread,
        }
        cmd = ["bash", str(SCRIPTS / "admit.sh"), *args]
        return subprocess.run(cmd, env=env, text=True, capture_output=True).returncode

    def test_places_count_until_released(self):
        # One thread running, limit 3: two places, then the limit.
        self.assertEqual(self.admit("take", "x"), 0)
        self.assertEqual(self.admit("take", "y"), 0)
        self.assertEqual(self.admit("take", "z"), 3)
        self.assertEqual(self.admit("release", "x"), 0)
        self.assertEqual(self.admit("take", "z"), 0)

    def test_the_same_label_cannot_take_two_places(self):
        self.assertEqual(self.admit("take", "review:1"), 0)
        self.assertEqual(self.admit("take", "review:1"), 5)

    def age_places(self, seconds):
        path = self.b.dir / ".admissions.json"
        places = json.loads(path.read_text())
        path.write_text(json.dumps([{**p, "at": p["at"] - seconds} for p in places]))

    def test_a_live_dispatchers_place_does_not_lapse(self):
        self.admit("take", "x")
        self.admit("take", "y")
        self.age_places(901)
        self.assertEqual(self.admit("take", "z", thread="b"), 3)

    def test_a_stopped_dispatchers_place_lapses(self):
        self.admit("take", "x", thread="gone")
        self.admit("take", "y", thread="gone")
        self.age_places(601)
        self.assertEqual(self.admit("take", "z"), 0)

    def test_an_unreadable_limit_starts_nothing(self):
        (self.b.dir / "manager.json").write_text(json.dumps({"thread_id": "a", "task_id": 999}))
        self.assertEqual(self.admit("take", "x"), 1)

    def test_concurrent_takers_share_the_last_place(self):
        self.admit("take", "x")
        env = {
            **os.environ,
            "PATH": f"{self.bin}:{os.environ['PATH']}",
            "MANAGER_BOARD": str(self.b.dir),
        }
        procs = [
            subprocess.Popen(["bash", str(SCRIPTS / "admit.sh"), "take", f"p{i}"], env=env)
            for i in range(4)
        ]
        codes = sorted(p.wait(timeout=60) for p in procs)
        self.assertEqual(codes, [0, 3, 3, 3])


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

    def test_a_fenced_example_row_is_ignored(self):
        example = "```\n| Daily budget (USD at list price, all providers) | 5 |\n```\n"
        body = TEMPLATE.read_text().replace("{amount}", "100")
        body = body.replace("## Budget\n", "## Budget\n\n" + example, 1)
        self.b.set_body(self.b.first, body)
        self.assertEqual(self.budget([{"costUsd": 50}]), (0, "budget: above"))

    def test_an_unreadable_manager_task_is_unavailable(self):
        other = self.b.create(TEMPLATE.read_text().replace("{amount}", "1000"), tags="")
        (self.b.dir / "manager.json").write_text(json.dumps({"task_id": other}))
        self.assertEqual(self.budget([{"costUsd": 101}]), (1, "budget: unavailable"))

    def test_a_roll_cut_short_before_the_pointer_is_unavailable(self):
        # The pointer still names the old task, which the roll has archived.
        self.b.kb("edit", str(self.b.first), "--release")
        self.b.kb("archive", str(self.b.first))
        self.b.progress(status="running", thread="b", previous=["a"], rolled_from=self.b.first)
        self.assertEqual(self.budget([{"costUsd": 101}]), (1, "budget: unavailable"))

    def test_no_manager_is_unset(self):
        (self.b.dir / "manager.json").unlink()
        self.b.kb("edit", str(self.b.first), "--release")
        self.b.kb("archive", str(self.b.first))
        self.assertEqual(self.budget([{"costUsd": 1}]), (0, "budget: unset"))

    def test_before_the_first_takeover_the_setup_task_counts(self):
        b = Board(self, TEMPLATE.read_text().replace("{amount}", "100"))
        self.b = b
        self.bin = b.dir / "bin"
        self.bin.mkdir()
        self.assertEqual(self.budget([{"costUsd": 101}]), (0, "budget: at"))

    def test_a_pointer_to_an_unclaimed_duplicate_is_unavailable(self):
        other = self.b.create(TEMPLATE.read_text().replace("{amount}", "1000"))
        (self.b.dir / "manager.json").write_text(json.dumps({"thread_id": "a", "task_id": other}))
        self.assertEqual(self.budget([{"costUsd": 101}]), (1, "budget: unavailable"))

    def test_a_missing_log_boundary_is_unavailable(self):
        body = TEMPLATE.read_text().replace("{amount}", "100").replace("## Log", "## Logbook")
        self.b.set_body(self.b.first, body)
        self.assertEqual(self.budget([{"costUsd": 1}]), (1, "budget: unavailable"))


@needs_tools
class SurveyTests(unittest.TestCase):
    def test_a_ready_task_in_flight_is_marked(self):
        b = Board(self)
        b.takeover("a")
        tasks = b.dir / "project"
        subprocess.run(
            ["kanban-md", "init", "--dir", str(tasks)], input="n\n", text=True, capture_output=True
        )
        for title in ("one", "two", "three"):
            subprocess.run(
                ["kanban-md", "create", title, "--status", "todo", "--dir", str(tasks)],
                capture_output=True,
                check=True,
            )
        _, state = b.run("manager.sh", "a", "state")
        old = b.dir / "old.md"
        old.write_text(state)
        new = b.dir / "new.md"
        new.write_text(
            state.replace("## Requests\n", f"- {tasks} #2, since now\n\n## Requests\n", 1)
        )
        self.assertEqual(b.run("manager.sh", "a", "set-state", str(new), str(old))[0], 0)
        bin_dir = b.dir / "bin"
        bin_dir.mkdir()
        (bin_dir / "t3c").write_text("#!/bin/sh\necho '{\"data\": []}'\n")
        (bin_dir / "t3c").chmod(0o755)
        repos = b.dir / "repos"
        repos.mkdir()
        env = {
            **os.environ,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "MANAGER_BOARD": str(b.dir),
            "TASK_ROOTS": str(tasks),
            "REPO_ROOT": str(repos),
        }
        out = subprocess.run(
            ["bash", str(SCRIPTS / "survey.sh")], env=env, text=True, capture_output=True
        ).stdout
        ready = [line for line in out.splitlines() if line.startswith(f"{tasks} #")]
        self.assertEqual(
            [line.endswith("(in flight)") for line in ready], [False, True, False], ready
        )


if __name__ == "__main__":
    unittest.main()
