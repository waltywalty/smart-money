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


def _curl(method, url, headers, body=None, timeout=120):
    """curl, not urllib.

    Measured 2026-08-17: some Kernel VMs export HTTPS_PROXY=https://ns.internal:3129,
    a proxy that speaks TLS on the proxy leg. curl handles that; Python's urllib does
    NOT - it opens a plain socket, sends CONNECT, and the proxy closes on it
    (RemoteDisconnected). Other VMs export an http:// proxy and urllib is fine, which
    is why this only shows up on some VMs. curl works in both cases.
    """
    import subprocess, tempfile
    bpath = None
    if body is not None:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(body)
            bpath = f.name
    out = tempfile.NamedTemporaryFile(delete=False).name
    cmd = ["curl", "-sS", "-X", method, "-o", out, "-w", "%{http_code}",
           "--max-time", str(timeout)]
    for k, v in headers.items():
        cmd += ["-H", "%s: %s" % (k, v)]
    if bpath:
        cmd += ["--data-binary", "@" + bpath]
    cmd.append(url)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        code = int(r.stdout.strip() or -1)
        with open(out, "rb") as f:
            raw = f.read()
        try:
            return code, (json.loads(raw) if raw else None)
        except Exception:
            return code, None
    finally:
        for f in (bpath, out):
            if f:
                try:
                    os.remove(f)
                except OSError:
                    pass


def _request(url, method="GET", payload=None):
    h = {"Authorization": "Bearer " + _token(),
         "Accept": "application/vnd.github+json",
         "User-Agent": UA,
         "X-GitHub-Api-Version": "2022-11-28"}
    body = None
    if payload is not None:
        body = json.dumps(payload).encode()
        h["Content-Type"] = "application/json"
    return _curl(method, url, h, body)


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
    h = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    last = None
    for attempt in range(tries):
        code, body = _curl("GET", url, h, None, 30)
        if code == 200:
            return code, body
        last = (code, None)
        if code == 404:                # propagation delay, not absence - bounded
            time.sleep(delay * (attempt + 1))
            continue
        return last
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


def put(path, local_path, message, branch="main", allow_update=False):
    """Create one file. One call = one commit. CREATE-ONLY by default.

    Why create-only is the default: on 2026-08-17 a `put` that meant to create a
    new close-out silently UPDATED the existing CLOSEOUT-2026-08-17.md and
    destroyed packet 3's close-out. Nothing refused, because nothing was asked to.
    The only signal was the status code - a create answers 201, an overwrite
    answers 200 - and a status code nobody checks is not a safeguard. That is the
    second same-name collision to destroy a file in this repository.

    Overwriting is now something the caller has to say out loud: --update.
    """
    with open(local_path, "rb") as f:
        raw = f.read()

    sha = get_sha(path, branch)
    if sha and not allow_update:
        print("REFUSING to write " + path, file=sys.stderr)
        print("  It already exists (blob " + sha[:7] + ").", file=sys.stderr)
        print("  This call would OVERWRITE it, not create it.", file=sys.stderr)
        print("  To replace it:   gh_commit.py put --update <repo_path> <local> <msg>", file=sys.stderr)
        print("  To add to it:    fetch it, append, then put --update.", file=sys.stderr)
        print("  For a new doc:   choose a path that does not exist.", file=sys.stderr)
        raise SystemExit(2)

    payload = {
        "message": message,
        "content": base64.b64encode(raw).decode(),
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha          # required for updates, rejected for new

    status, result = _request(f"{API}/contents/{path}", "PUT", payload)

    # 201 means created, 200 means something was already there. If we believed we
    # were creating and the API says 200, get_sha and the write disagree - treat
    # that as a failure rather than printing "created" over an overwrite.
    if not allow_update and status != 201:
        print("WRITE ABORTED CHECK: expected HTTP 201 (created) for " + path
              + ", got " + str(status) + ".", file=sys.stderr)
        print("  A 200 here means the path existed after all and has been overwritten.", file=sys.stderr)
        raise SystemExit(3)

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
        args = sys.argv[2:]
        allow_update = "--update" in args
        args = [a for a in args if a != "--update"]
        if len(args) < 3:
            sys.exit("usage: gh_commit.py put [--update] <repo_path> <local_path> <message> [branch]")
        put(args[0], args[1], args[2], args[3] if len(args) > 3 else "main", allow_update)
    else:
        sys.exit(f"unknown command: {cmd}")


if __name__ == "__main__":
    main()
