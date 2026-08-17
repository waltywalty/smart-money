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
    req = urllib.request.Request(url, data=body if body else None, method=method)
    for h, v in headers.items():
        if h != "host":
            req.add_header(h, v)
    req.add_header("Authorization", auth)
    req.add_header("User-Agent", "smart-money-research/1.0")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        b = b""
        try:
            b = e.read()
        except Exception:
            pass
        e.close()
        return e.code, {}, b
