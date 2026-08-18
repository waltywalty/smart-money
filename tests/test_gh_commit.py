"""T0.2 regression tests for scripts/gh_commit.py check().

The defect these lock out: check() used to report `permissions.push` and call it
write access. That field reflects the authenticated actor's repo access, not a
fine-grained token's Contents grant, and it reported push=True for a token that
could not write on 2026-08-12.

check() must now prove write access BY WRITING, verify through an unauthenticated
read (SKILL.md rule 12), clean up, and exit non-zero on any failure. These stub the
transport, so the suite needs no network and no token.
"""
import base64, importlib.util, io, os, unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "gh_commit", os.path.join(ROOT, "lib", "gh_commit.py"))
gh = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gh)


def _repo(private=False):
    return (200, {"full_name": "waltywalty/smart-money", "private": private,
                  "permissions": {"push": True}})


class Harness:
    """Stands in for the network. Records what check() actually did."""

    def __init__(self, write_status=201, delete_status=200,
                 readback=('match', 200), private=False):
        self.write_status, self.delete_status = write_status, delete_status
        self.readback, self.private = readback, private
        self.calls, self.written = [], None

    def request(self, url, method="GET", payload=None):
        self.calls.append((method, url))
        if method == "GET" and url.endswith("/smart-money"):
            return _repo(self.private)
        if method == "PUT":
            self.written = base64.b64decode(payload["content"])
            return self.write_status, {"content": {"sha": "deadbeef"}}
        if method == "DELETE":
            return self.delete_status, {}
        raise AssertionError("unexpected %s %s" % (method, url))

    def unauth(self, url, **kw):
        self.calls.append(("GET-unauth", url))
        kind, status = self.readback
        if kind == 'match':
            return status, {"content": base64.b64encode(self.written).decode()}
        if kind == 'differ':
            return status, {"content": base64.b64encode(b"something else").decode()}
        return status, None


class TestNoPermissionsPush(unittest.TestCase):
    def test_source_does_not_read_permissions_push_as_proof(self):
        with open(os.path.join(ROOT, "lib", "gh_commit.py"),
                  encoding="utf-8") as fh:            # rule 9: close what you open
            src = fh.read()
        code = src.split('"""', 2)[-1]               # strip the module docstring
        self.assertNotIn('perms.get("push")', code)
        self.assertNotIn("permissions", code)


class TestCheckRoundTrip(unittest.TestCase):
    def _run(self, h):
        with mock.patch.object(gh, "_request", h.request), \
             mock.patch.object(gh, "_request_unauth", h.unauth), \
             mock.patch("sys.stdout", new=io.StringIO()):
            return gh.check()

    def test_passes_only_on_a_completed_round_trip(self):
        h = Harness()
        self.assertTrue(self._run(h))
        m = [x for x, _ in h.calls]
        self.assertIn("PUT", m); self.assertIn("GET-unauth", m); self.assertIn("DELETE", m)

    def test_read_back_happens_through_the_unauthenticated_path(self):
        h = Harness()
        self._run(h)
        self.assertTrue(any(m == "GET-unauth" for m, _ in h.calls),
                        "check() must verify through the unauthenticated reader")

    def test_fails_when_the_write_is_rejected(self):
        with self.assertRaises(SystemExit):
            self._run(Harness(write_status=403))

    def test_fails_when_the_read_back_404s(self):
        with self.assertRaises(SystemExit):
            self._run(Harness(readback=('missing', 404)))

    def test_fails_when_the_read_back_content_differs(self):
        with self.assertRaises(SystemExit):
            self._run(Harness(readback=('differ', 200)))

    def test_fails_when_cleanup_fails(self):
        with self.assertRaises(SystemExit):
            self._run(Harness(delete_status=403))

    def test_cleans_up_even_when_verification_fails(self):
        h = Harness(readback=('differ', 200))
        with self.assertRaises(SystemExit):
            self._run(h)
        self.assertIn("DELETE", [x for x, _ in h.calls],
                      "a failed check must not leave litter in the repo")

    def test_warns_when_the_repo_is_private(self):
        h = Harness(private=True); buf = io.StringIO()
        with mock.patch.object(gh, "_request", h.request), \
             mock.patch.object(gh, "_request_unauth", h.unauth), \
             mock.patch("sys.stdout", new=buf):
            gh.check()
        self.assertIn("NOT an", buf.getvalue())


class TestWriteTestPath(unittest.TestCase):
    def _put(self, h):
        with mock.patch.object(gh, "_request", h.request), \
             mock.patch.object(gh, "_request_unauth", h.unauth), \
             mock.patch("sys.stdout", new=io.StringIO()):
            gh.check()
        return [u for m, u in h.calls if m == "PUT"][0]

    def test_write_target_is_a_throwaway_under_tmp(self):
        put = self._put(Harness())
        self.assertIn("/contents/tmp/write-test-", put)
        self.assertTrue(put.endswith(".txt"))

    def test_two_checks_do_not_collide(self):
        self.assertNotEqual(self._put(Harness()), self._put(Harness()))
