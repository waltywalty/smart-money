"""Regression tests for gh_commit.py put() create-only mode.

The defect these lock out: on 2026-08-17 a `put` meaning to CREATE
CLOSEOUT-2026-08-17.md silently UPDATED the existing file and destroyed packet 3's
close-out. The API had said so - 200 for an overwrite, 201 for a create - but
nothing checked, and nothing refused. Second same-name collision in this repo.

put() is now create-only unless allow_update is set. These stub the transport, so
the suite needs no network and no token.
"""
import base64, importlib.util, os, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "gh_commit_co", os.path.join(ROOT, "scripts", "gh_commit.py"))
gh = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gh)

EXISTING_SHA = "abc1234def5678"


class Transport:
    """Stands in for the network. Records every call so the test can assert that a
    refused write issued NO PUT at all - refusing after writing is not refusing."""

    def __init__(self, exists, put_status=201):
        self.exists, self.put_status = exists, put_status
        self.calls = []

    def request(self, url, method="GET", payload=None):
        self.calls.append((method, url, payload))
        if method == "GET":
            if self.exists:
                return 200, {"sha": EXISTING_SHA}
            return 404, {}
        if method == "PUT":
            return self.put_status, {"commit": {"sha": "0" * 40}}
        raise AssertionError("unexpected method " + method)

    @property
    def puts(self):
        return [c for c in self.calls if c[0] == "PUT"]


class CreateOnlyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".md")
        self.tmp.write(b"new content")
        self.tmp.close()
        self.addCleanup(os.unlink, self.tmp.name)
        self._orig = gh._request
        self.addCleanup(lambda: setattr(gh, "_request", self._orig))

    def _install(self, t):
        gh._request = t.request
        return t

    def test_refuses_when_path_exists(self):
        t = self._install(Transport(exists=True))
        with self.assertRaises(SystemExit) as cm:
            gh.put("CLOSEOUT-2026-08-17.md", self.tmp.name, "msg")
        self.assertNotEqual(cm.exception.code, 0, "refusal must exit non-zero")
        self.assertEqual(t.puts, [], "refusal must issue no PUT at all")

    def test_creates_when_path_absent(self):
        t = self._install(Transport(exists=False, put_status=201))
        gh.put("data/brand-new.md", self.tmp.name, "msg")
        self.assertEqual(len(t.puts), 1)
        self.assertNotIn("sha", t.puts[0][2], "a create must not send a sha")

    def test_overwrites_only_when_update_requested(self):
        t = self._install(Transport(exists=True, put_status=200))
        gh.put("CLOSEOUT-2026-08-17.md", self.tmp.name, "msg", allow_update=True)
        self.assertEqual(len(t.puts), 1)
        self.assertEqual(t.puts[0][2]["sha"], EXISTING_SHA,
                         "an update must send the existing blob sha")

    def test_create_rejects_a_200_response(self):
        """get_sha said absent but the API answered 200 - that is an overwrite that
        slipped through a race. It must fail, not print 'created'."""
        t = self._install(Transport(exists=False, put_status=200))
        with self.assertRaises(SystemExit) as cm:
            gh.put("data/racy.md", self.tmp.name, "msg")
        self.assertNotEqual(cm.exception.code, 0)

    def test_cli_requires_explicit_update_flag(self):
        import sys
        t = self._install(Transport(exists=True))
        argv = sys.argv
        try:
            sys.argv = ["gh_commit.py", "put", "CLOSEOUT-2026-08-17.md", self.tmp.name, "msg"]
            with self.assertRaises(SystemExit) as cm:
                gh.main()
            self.assertNotEqual(cm.exception.code, 0)
            self.assertEqual(t.puts, [])
            sys.argv = ["gh_commit.py", "put", "--update", "CLOSEOUT-2026-08-17.md", self.tmp.name, "msg"]
            gh.main()
            self.assertEqual(len(t.puts), 1)
        finally:
            sys.argv = argv


if __name__ == "__main__":
    unittest.main()
