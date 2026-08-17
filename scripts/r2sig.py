"""Minimal SigV4 S3 client for Cloudflare R2, over urllib.

Why not boto3: measured 2026-08-17 inside a Kernel VM, LIST succeeds, `curl -X PUT`
returns a real R2 error in 0.15s, and boto3's `put_object` hangs indefinitely with
no error - through the same proxy, with the same credentials, with checksum
calculation set to when_required and the system CA bundle supplied. urllib and curl
both work, so the transport is fine and the SDK is not. Forty lines of SigV4 is a
smaller dependency than a hang nobody can explain.
"""
import datetime as dt, hashlib, hmac, os, sys, urllib.request, urllib.error, urllib.parse

ALGO = "AWS4-HMAC-SHA256"
SERVICE = "s3"


def _cfg():
    e = os.environ
    for v in ("R2_ENDPOINT", "R2_BUCKET", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"):
        if not e.get(v):
            sys.exit(f"{v} is not set. Refusing to continue.")
    return (e["R2_ENDPOINT"].rstrip("/"), e["R2_BUCKET"], e["AWS_ACCESS_KEY_ID"],
            e["AWS_SECRET_ACCESS_KEY"], e.get("AWS_DEFAULT_REGION", "auto"))


def _sign(key, msg):
    return hmac.new(key, msg.encode(), hashlib.sha256).digest()


def request(method, key="", body=b"", query=None, timeout=120):
    """Returns (status, headers, body). Never raises on an HTTP error status."""
    ep, bucket, ak, sk, region = _cfg()
    host = urllib.parse.urlparse(ep).netloc
    path = "/" + bucket + ("/" + key.lstrip("/") if key else "")
    cpath = urllib.parse.quote(path, safe="/~")
    cquery = urllib.parse.urlencode(sorted((query or {}).items()), quote_via=urllib.parse.quote)
    now = dt.datetime.now(dt.timezone.utc)
    amzdate = now.strftime("%Y%m%dT%H%M%SZ"); datestamp = now.strftime("%Y%m%d")
    payload_hash = hashlib.sha256(body).hexdigest()

    headers = {"host": host, "x-amz-content-sha256": payload_hash, "x-amz-date": amzdate}
    signed = ";".join(sorted(headers))
    canon_headers = "".join(f"{k}:{headers[k]}\n" for k in sorted(headers))
    canon = f"{method}\n{cpath}\n{cquery}\n{canon_headers}\n{signed}\n{payload_hash}"
    scope = f"{datestamp}/{region}/{SERVICE}/aws4_request"
    sts = f"{ALGO}\n{amzdate}\n{scope}\n{hashlib.sha256(canon.encode()).hexdigest()}"
    k = _sign(("AWS4" + sk).encode(), datestamp)
    k = _sign(k, region); k = _sign(k, SERVICE); k = _sign(k, "aws4_request")
    sig = hmac.new(k, sts.encode(), hashlib.sha256).hexdigest()
    auth = f"{ALGO} Credential={ak}/{scope}, SignedHeaders={signed}, Signature={sig}"

    url = ep + cpath + ("?" + cquery if cquery else "")
    hdrs = {k: v for k, v in headers.items() if k != "host"}
    hdrs["Authorization"] = auth
    hdrs["User-Agent"] = "smart-money-research/1.0"
    return _send(method, url, hdrs, body, timeout)


def _send(method, url, hdrs, body, timeout):
    """curl, not urllib.

    Measured 2026-08-17: some Kernel VMs export HTTPS_PROXY=https://ns.internal:3129
    - a proxy that speaks TLS on the proxy leg. curl handles that; Python's urllib
    does NOT - it opens a plain socket, sends CONNECT, and the proxy closes on it
    (`RemoteDisconnected`). Other VMs export an http:// proxy and urllib is fine.
    Whether Python networking works therefore varies VM to VM. curl works in both,
    so curl is the transport.
    """
    import subprocess, tempfile
    with tempfile.NamedTemporaryFile(delete=False) as bf:
        bf.write(body or b"")
        bpath = bf.name
    out = tempfile.NamedTemporaryFile(delete=False).name
    cmd = ["curl", "-sS", "-X", method, "-o", out, "-w", "%{http_code}",
           "--max-time", str(timeout),
           # curl sends `Expect: 100-continue` on a body over ~1 KB. Neither this
           # proxy nor R2 answers it: curl reports the interim 100 as the status and
           # blocks until --max-time. Measured 2026-08-17 - a 16 MB PUT returned
           # http=100 after 120s, and this is almost certainly what made boto3's
           # put_object hang too. An interim 1xx is never a success.
           "-H", "Expect:"]
    for k, v in hdrs.items():
        cmd += ["-H", f"{k}: {v}"]
    if body:
        cmd += ["--data-binary", "@" + bpath]
    cmd.append(url)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        code = int(r.stdout.strip() or -1)
        with open(out, "rb") as f:
            rb = f.read()
        return code, {}, rb
    finally:
        for f in (bpath, out):
            try:
                os.remove(f)
            except OSError:
                pass
