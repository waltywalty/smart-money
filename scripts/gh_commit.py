#!/usr/bin/env python3
"""Commit files to GitHub from the Kernel VM via the Contents API.

Git is not installed in Kernel VMs, and Cowork's proxy 403s api.github.com.
Kernel reaches it fine, so this is the write path: raw HTTPS, no git needed.

Token comes from the environment. It is never printed, never written to disk,
and never committed. If GH_TOKEN is unset this exits rather than guessing.

    export GH_TOKEN=...            # set by the session, not by this file
    python gh_commit.py check
    python gh_commit.py put registry/FINDINGS.md ./FINDINGS.md "Add findings"
"""
import base64
import json
import os
import sys
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


def check():
    """Confirm the token works and has write access before relying on it."""
    status, repo = _request(API)
    if status != 200:
        sys.exit(f"repo endpoint returned {status}")
    perms = (repo or {}).get("permissions", {})
    print(f"200 {repo['full_name']}  push={perms.get('push')}")
    if not perms.get("push"):
        sys.exit("Token reached the repo but has no write access. "
                 "Check Contents = Read and write on the token.")
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
