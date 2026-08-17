#!/usr/bin/env python3
"""R2 object store client for the smart-money dataset. Uses scripts/r2sig.py.

Credentials come from the environment, per-session. Never printed, never written
to a repo file, never committed:

    R2_ENDPOINT  R2_BUCKET  AWS_ACCESS_KEY_ID  AWS_SECRET_ACCESS_KEY

    python r2.py roundtrip [megabytes]   # T0.3 gate: write, read back, sha256, delete
    python r2.py put <key> <local>
    python r2.py get <key> <local>
    python r2.py ls [prefix]
    python r2.py rm <key>

`roundtrip` exits non-zero unless the bytes that come back are byte-identical to
the bytes that went out, the object is listable, the delete removes it, and an
impossible control key is NOT readable. A write that cannot be read back is not
a write.
"""
import hashlib, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r2sig import request


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _keys(prefix="", cap=100000):
    out, tok = [], None
    while len(out) < cap:
        q = {"list-type": "2", "max-keys": "1000"}
        if prefix:
            q["prefix"] = prefix
        if tok:
            q["continuation-token"] = tok
        st, _, b = request("GET", query=q)
        if st != 200:
            sys.exit(f"LIST returned {st}: {b[:200]!r}")
        x = b.decode("utf-8", "replace")
        out += [(k, int(s)) for k, s in zip(re.findall(r"<Key>(.*?)</Key>", x),
                                            re.findall(r"<Size>(\d+)</Size>", x))]
        if "<IsTruncated>true</IsTruncated>" not in x:
            break
        m = re.search(r"<NextContinuationToken>(.*?)</NextContinuationToken>", x)
        if not m:
            break
        tok = m.group(1)
    return out


def roundtrip(mb=1.0):
    n = int(float(mb) * 1024 * 1024)
    body = os.urandom(n)                 # incompressible, so nothing can dedup it away
    want = _sha(body)
    key = f"_selftest/roundtrip-{int(time.time())}-{os.urandom(4).hex()}.bin"
    print(f"bucket={os.environ.get('R2_BUCKET')} key={key} bytes={n}", flush=True)

    t = time.time(); st, _, b = request("PUT", key, body)
    print(f"  PUT    http={st}  {time.time()-t:.2f}s", flush=True)
    if st not in (200, 201):
        sys.exit(f"FAIL: PUT returned {st}: {b[:200]!r}")

    t = time.time(); st, _, got = request("GET", key)
    print(f"  GET    http={st}  {time.time()-t:.2f}s  {len(got)} bytes", flush=True)
    have = _sha(got)
    match = st == 200 and have == want and len(got) == n
    print(f"  sha256 out {want[:40]}")
    print(f"  sha256 in  {have[:40]}   {'MATCH' if match else 'MISMATCH'}", flush=True)

    listed = any(k == key for k, _ in _keys(key))
    print(f"  LIST   finds it: {listed}", flush=True)

    st, _, _ = request("DELETE", key)
    gone = not any(k == key for k, _ in _keys(key))
    print(f"  DELETE http={st}  gone: {gone}", flush=True)

    cst, _, _ = request("GET", "_selftest/IMPOSSIBLE-CONTROL-19990101.bin")
    print(f"  CONTROL impossible key -> http={cst} (must not be 200)", flush=True)

    if not match:
        sys.exit("FAIL: bytes read back do not match bytes written")
    if not listed:
        sys.exit("FAIL: object written but not listable")
    if not gone:
        sys.exit("FAIL: delete did not remove the object")
    if cst == 200:
        sys.exit("FAIL: an impossible control key read successfully")
    print("PASS: put -> get -> sha256 match -> list -> delete, control 404s")
    return True


def put(key, local):
    with open(local, "rb") as f:
        body = f.read()
    st, _, b = request("PUT", key, body)
    if st not in (200, 201):
        sys.exit(f"FAIL: PUT {key} returned {st}: {b[:200]!r}")
    print(f"put {key} <- {local} ({len(body)} bytes, sha256 {_sha(body)[:16]})")


def get(key, local):
    st, _, b = request("GET", key)
    if st != 200:
        sys.exit(f"FAIL: GET {key} returned {st}")
    with open(local, "wb") as f:
        f.write(b)
    print(f"get {key} -> {local} ({len(b)} bytes, sha256 {_sha(b)[:16]})")


def ls(prefix=""):
    ks = _keys(prefix)
    for k, s in ks[:30]:
        print(f"  {s:>12}  {k}")
    print(f"{len(ks)} objects, {sum(s for _, s in ks)/1e6:.1f} MB")


def rm(key):
    st, _, _ = request("DELETE", key)
    print(f"rm {key} http={st}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd, a = sys.argv[1], sys.argv[2:]
    {"roundtrip": lambda: roundtrip(a[0] if a else 1),
     "put": lambda: put(a[0], a[1]), "get": lambda: get(a[0], a[1]),
     "ls": lambda: ls(a[0] if a else ""), "rm": lambda: rm(a[0])}.get(
        cmd, lambda: sys.exit(f"unknown command: {cmd}"))()
