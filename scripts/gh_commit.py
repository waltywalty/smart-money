#!/usr/bin/env python3
"""Commit files to GitHub from the Kernel VM via the Contents API.

Git is not installed in Kernel VMs, and Cowork's proxy 403s api.github.com.
Kernel reaches it fine, so this is the write path: raw HTTPS, no git needed.

Token comes from the environment. It is never printed, never written to disk,
and never committed. If GH_TOKEN is unset this exits rather than guessing.

    export GH_TOKEN=...            # set by the session, not by this file
    python gh_commit.py check      # write -> read back unauthenticated -> delete
    python gh_commit.py put registry/FINDINGS.md ./FINDINGS.md "Add findings"
"""
import base64
import json
import os
import sys
import time
import uuid
import urllib.error
import urllib.request

REPO = "waltywalty/smart-money"
API = f"https://api.github.com/repos/{REPO}"
UA = "smart-money-kernel/1.0"


def _token():
    t = os.environ.get("GH_TOKEN")
    if not t:
        sys.exit("GH_TOKEN is not set. Refusing to continue.")
    return t


def _request(url, method="GET", payload=None):
    """Return (status, parsed_body). Raises on non-2xx except 404."""
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers={
        "Authorization": f"Bearer {_token()}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
        "User-Agent": UA,
    })
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return 404, None
        # Report the status. Never let an exception be read as "absent".
        sys.stderr.write(f"HTTP {e.code} on {method} {url}\n{e.read()[:400]}\n")
        raise


def _request_unauth(url, tries=6, delay=1.5):
    """Read a public resource with NO Authorization header.

    This is the different path in `verify a write by reading it back through a
    different path` (SKILL.md rule 12): a token that cannot write, or a write
    that silently did not land, cannot fake a result here. api.github.com is
    used rather than raw.githubusercontent.com because the latter is CDN-fronted
    and a stale edge would show the pre-write state - which is exactly the
    reading rule 12 warns is evidence FOR staleness, not against it.

    Retries are bounded and a timeout is a failure, never a pass.
    """
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", UA)
    req.add_header("Accept", "application/vnd.github+json")
    last = None
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            try:
                e.read()
            except Exception:
                pass
            e.close()
            last = (e.code, None)
            if e.code == 404:          # propagation delay, not absence - bounded
                time.sleep(delay * (attempt + 1))
                continue
            return last
        except Exception as ex:
            last = (-1, {"exc": type(ex).__name__})
            time.sleep(delay * (attempt + 1))
    return last


def delete(path, sha, message, branch="main"):
    """Remove one file. Used by check() to clean up after itself."""
    payload = {"message": message, "sha": sha, "branch": branch}
    status, _ = _request(f"{API}/contents/{path}", "DELETE", payload)
    return status


def check(verbose=True):
    """Prove write access by WRITING. Returns True, or exits non-zero.

    write -> read back unauthenticated -> compare -> delete.
    Nothing short of a completed round trip is accepted as proof.
    """
    status, repo = _request(API)
    if status != 200:
        sys.exit(f"FAIL: repo endpoint returned {status}")
    private = bool((repo or {}).get("private"))
    if verbose:
        print(f"200 {repo['full_name']}  private={private}")
    if private:
        print("WARNING: repo is private - the read-back below is NOT an "
              "independent path. Treat this check as weaker than it looks.")

    stamp = f"{int(time.time())}-{uuid.uuid4().hex[:8]}"
    path = f"tmp/write-test-{stamp}.txt"
    body = f"gh_commit write test {stamp}\n".encode()

    payload = {"message": f"write test {stamp}", "branch": "main",
               "content": base64.b64encode(body).decode()}
    status, result = _request(f"{API}/contents/{path}", "PUT", payload)
    if status not in (200, 201):
        sys.exit(f"FAIL: write returned {status} - token cannot write")
    sha = result["content"]["sha"]
    if verbose:
        print(f"{status} wrote {path}")

    url = f"https://api.github.com/repos/{REPO}/contents/{path}?ref=main"
    rstatus, rbody = _request_unauth(url)
    ok = False
    if rstatus == 200 and isinstance(rbody, dict):
        got = base64.b64decode(rbody.get("content", "") or "")
        ok = got == body
        if verbose:
            print(f"{rstatus} read back unauthenticated: "
                  f"{'CONTENT MATCHES' if ok else 'CONTENT DIFFERS'}")
    else:
        if verbose:
            print(f"{rstatus} read back unauthenticated: FAILED")

    dstatus = delete(path, sha, f"remove write test {stamp}")
    if verbose:
        print(f"{dstatus} deleted {path}")

    if not ok:
        sys.exit("FAIL: write was not confirmed by an independent read. "
                 "Do not rely on this token.")
    if dstatus not in (200, 201):
        sys.exit(f"FAIL: could not delete {path} (status {dstatus}) - "
                 "write access is partial")
    print("PASS: write -> independent read-back -> delete all succeeded")
    return True


def get_sha(path, branch="main"):
    """Current blob SHA, or None if the file does not exist yet."""
    status, body = _request(f"{API}/contents/{path}?ref={branch}")
    if status == 404:
        return None
    if isinstance(body, list):
        sys.exit(f"{path} is a directory, not a file")
    return body["sha"]


def put(path, local_path, message, branch="main"):
    """Create or update one file. One call = one commit."""
    with open(local_path, "rb") as f:
        raw = f.read()

    payload = {
        "message": message,
        "content": base64.b64encode(raw).decode(),
        "branch": branch,
    }
    sha = get_sha(path, branch)
    if sha:
        payload["sha"] = sha          # required for updates, rejected for new

    status, result = _request(f"{API}/contents/{path}", "PUT", payload)
    commit = result["commit"]["sha"][:7]
    print(f"{status} {'updated' if sha else 'created'} {path} "
          f"({len(raw)} bytes) -> {commit}")
    return result


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "check":
        check()
    elif cmd == "put":
        if len(sys.argv) < 5:
            sys.exit("usage: gh_commit.py put <repo_path> <local_path> <message> [branch]")
        put(*sys.argv[2:6])
    else:
        sys.exit(f"unknown command: {cmd}")


if __name__ == "__main__":
    main()
