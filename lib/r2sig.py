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


def sha256_file(path, chunk=1 << 20):
    """Stream a file's sha256. A 977 MiB VM cannot load a 256 MB object to sign it -
    measured 2026-08-17, the in-memory path is OOM-killed between 64 MB and 256 MB."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


RETRY_CODES = (408, 429, 500, 502, 503, 504)


def request_file(method, key, path=None, out=None, timeout=1800, tries=5):
    """Streaming variant: the body never enters memory, and 4xx/5xx are retried.

    Phase 1 uses this. `request()` holds the whole body in RAM and must not be used
    above ~64 MB on a 1 GiB VM.
    """
    ep, bucket, ak, sk, region = _cfg()
    host = urllib.parse.urlparse(ep).netloc
    cpath = urllib.parse.quote("/" + bucket + "/" + key.lstrip("/"), safe="/~")
    ph = sha256_file(path) if path else hashlib.sha256(b"").hexdigest()
    now = dt.datetime.now(dt.timezone.utc)
    amzdate = now.strftime("%Y%m%dT%H%M%SZ"); datestamp = now.strftime("%Y%m%d")
    hh = {"host": host, "x-amz-content-sha256": ph, "x-amz-date": amzdate}
    signed = ";".join(sorted(hh))
    ch = "".join("%s:%s\n" % (k, hh[k]) for k in sorted(hh))
    canon = "%s\n%s\n\n%s\n%s\n%s" % (method, cpath, ch, signed, ph)
    scope = "%s/%s/%s/aws4_request" % (datestamp, region, SERVICE)
    sts = "%s\n%s\n%s\n%s" % (ALGO, amzdate, scope, hashlib.sha256(canon.encode()).hexdigest())
    k = _sign(("AWS4" + sk).encode(), datestamp)
    k = _sign(k, region); k = _sign(k, SERVICE); k = _sign(k, "aws4_request")
    sig = hmac.new(k, sts.encode(), hashlib.sha256).hexdigest()
    hdrs = {"x-amz-content-sha256": ph, "x-amz-date": amzdate,
            "Authorization": "%s Credential=%s/%s, SignedHeaders=%s, Signature=%s"
                             % (ALGO, ak, scope, signed, sig),
            "User-Agent": "smart-money-research/1.0"}
    import subprocess, tempfile, time as _t
    dest = out or tempfile.NamedTemporaryFile(delete=False).name
    last = -1
    for attempt in range(tries):
        cmd = ["curl", "-sS", "-o", dest, "-w", "%{http_code}",
               "--max-time", str(timeout), "-H", "Expect:"]
        for kk, vv in hdrs.items():
            cmd += ["-H", "%s: %s" % (kk, vv)]
        if path:
            cmd += ["--upload-file", path]      # implies PUT, streams from disk
        else:
            cmd += ["-X", method]
        cmd.append(ep + cpath)
        r = subprocess.run(cmd, capture_output=True, text=True)
        try:
            last = int(r.stdout.strip() or -1)
        except ValueError:
            last = -1
        if last >= 200 and last not in RETRY_CODES:
            return last, ph
        _t.sleep(min(30, 1.5 * (2 ** attempt)))
    return last, ph


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
