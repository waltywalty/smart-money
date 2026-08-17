# GATE 0 — durability

**Date:** 2026-08-17. **Packet:** coworkpacket4, Phase 0.

| # | question | answer |
|---|---|---|
| 1 | Does the token survive VM destruction and retrieval? | **NO ROUTE EXISTS — measured, not failed.** Kernel's credential store `create`s fine and reports `has_values: true`, but `get` returns metadata and key *names* only; a VM created **after** the credential has it in neither its environment nor its filesystem; and no Kernel-internal endpoint is routable from inside the VM (`169.254.169.254`, `localhost:444` → `http=000`). Tested with a **dummy** value before the real PAT was requested; probe credential and probe VM both deleted. The same fresh VM reaches `api.github.com` at **200**, so the write path is fine — only credential *delivery* has no durable route. **Walton ruled: per-session paste, and make loss cheap instead.** |
| 2 | Does `gh_commit.py check` fail correctly on a read-only token? | **Rewritten and tested; the read-only case is stubbed, not live.** `check()` no longer reads `permissions.push` — zero references remain outside the docstring that explains why. It now writes `tmp/write-test-<stamp>.txt`, reads it back **unauthenticated** via `api.github.com`, compares bytes, deletes, and exits non-zero on any failure. **Live against the real token: PASS** (`201 wrote / 200 CONTENT MATCHES / 200 deleted / exit=0`). Failure modes are covered by **11 stubbed regression tests** — write rejected, read-back 404, content mismatch, cleanup failure, litter after failure, path collision. **A genuinely read-only token has not been issued, so that path is tested by stub only.** |
| 3 | Does R2 round-trip a file from a fresh VM? | **NOT TESTED — blocked.** Bucket name and both keys supplied; the **endpoint arrived as the literal string `<paste>`**. R2's S3 endpoint is `https://<ACCOUNT_ID>.r2.cloudflarestorage.com` and the account ID is not derivable from an access key. The 1 MB round-trip (write, read back, sha256 compare, delete) runs the moment it arrives. |
| 4 | Are the stranded patches on `main`? | **NO for the census; the P9 amendment is superseded.** Verified by unauthenticated read-back: `registry/retention/` holds only `README.md`, `FINDINGS-2026-08-14.md` and `census-2026-08-14.json`. The 08-15 and 08-16 census outputs never landed — the scheduled task fired (`last_fired_at 2026-08-16T03:03Z`) and fell back to delivering a patch, exactly as instructed when `$GH_TOKEN` is absent. **P9's substance is committed** — the boundary re-measurement is in `ARCHIVE-LAG-2026-08-14.md` Amendment 1 and the resolution was reported 2026-08-17. |

## Verdict

**Gate 0 does not pass.** Line 3 is untested and line 1 has no route by construction.

Per Addendum A's correction — *any "not" means Phase 1 does not start; do **Phase 2 or Phase 3**
instead* — **Phase 1 has not started.** Phase 2 (T2.1) and Phase 3 (T3.1, T3.2, T3.3) were done
instead, along with Addendum A1, A2 and A3.

## What this establishes about durability, for the close-out

**The token problem is solved as well as it can be, and it is not solved durably.** Per-session
paste works and produced every commit in this session. What changed is the cost of losing it:
`check` now fails in **under two seconds** on a bad token instead of after an hour of collection,
and every artifact is committed as it is produced rather than at the end. **The Cowork sandbox
rolled back mid-session and took an entire prepared patch with it — and nothing was lost**, because
the rebuilt files went to `main` one at a time.

**The data problem is not solved.** Until R2 exists, Phase 1 would collect into an ephemeral VM,
which the packet correctly names as repeating the failure exactly.

**The one durable route left is GitHub Actions**, where the secret lives in GitHub's own store and
never enters a VM or a chat. The narrowed census is the pilot: if two requests a day run cleanly
from a runner — including against Kalshi's rate limiting on shared runner IPs — that is the
migration path for everything credential-dependent.

---

# Update — 2026-08-17, after credentials arrived

**Appended, not rewritten.** The assessment above was made with no PAT and no R2 endpoint. Both
arrived; three of the four lines have moved.

| # | question | answer now |
|---|---|---|
| 1 | Does the token survive VM destruction and retrieval? | **NO ROUTE — unchanged, and now a settled design decision.** Kernel's credential store cannot return a value to a script; measured with a dummy, probe deleted. Walton ruled per-session paste, and made loss cheap instead. Recorded in `PARKED.md` and here so it is not re-attempted. |
| 2 | Does `gh_commit.py check` fail correctly on a read-only token? | **PASS, live, twice, on two different VMs.** `201 wrote / 200 read back unauthenticated: CONTENT MATCHES / 200 deleted / exit=0`. `permissions.push` appears nowhere outside the docstring explaining why. 11 stubbed tests cover write-rejected, read-back-404, content-mismatch, cleanup-failure, litter-after-failure and path-collision. A genuinely read-only token has still not been issued, so **that specific path remains stub-tested only.** |
| 3 | Does R2 round-trip a file from a fresh VM? | **PASS, both halves.** 1 MB: `PUT 200 / GET 200 / sha256 MATCH / listable / DELETE 204 / control key 404`. And the half that matters: an object written by a VM that was then **destroyed** read back **byte-identical** (`sha256 931eb01d…`) from a fresh VM in a different metro. **The dataset now outlives the VM.** |
| 4 | Are the stranded patches on `main`? | **Census: still no.** Its two runs fell back to delivering patches, as instructed when `$GH_TOKEN` is absent. **P9's substance is committed** via `ARCHIVE-LAG-2026-08-14.md` Amendment 1. |

## Verdict: Gate 0 passes on the two lines that gate Phase 1

Line 3 was the blocker and it is closed. **Phase 1 may collect into R2.** Line 1 is a permanent
property of the platform rather than a failure, and line 4 is a delivery-mode artifact, not a data
loss.

## Two platform facts found while closing line 3, both worth more than the gate

**boto3 cannot write to R2 from a Kernel VM.** LIST succeeds; `curl -X PUT` returns a real R2 error
in 0.15s; `put_object` hangs silently until timeout — with the system CA bundle supplied and
checksum calculation forced to `when_required`. Replaced with ~40 lines of SigV4 over curl
(`scripts/r2sig.py`). **A hang nobody can explain is a larger dependency than a signature.**

**Python networking works on some Kernel VMs and not others.** Some export
`HTTPS_PROXY=https://ns.internal:3129` — a proxy that speaks **TLS on the proxy leg**. curl handles
it; Python's `urllib` opens a plain socket, sends `CONNECT`, and the proxy closes on it
(`RemoteDisconnected`). Other VMs export an `http://` proxy and urllib is fine. **`gh_commit.py
check` failed on a fresh VM for exactly this reason, on a token that was perfectly good.** Both
clients now use curl as transport. This retroactively explains a class of intermittent failure
this project has hit and never diagnosed.

## What this establishes about durability, for the close-out

**Data durability: solved.** R2 round-trips, survives VM destruction, and the client is committed.

**Credential durability: not solved, and now known to be unsolvable on this platform.** Per-session
paste is the design. What changed is the blast radius: `check` fails in under two seconds on a bad
token instead of after an hour of collection, and every artifact is committed as it is produced.
**The Cowork sandbox rolled back mid-session and destroyed a fully prepared patch — and nothing was
lost**, because the rebuilt files went to `main` one at a time.

**The one remaining durable route is GitHub Actions**, where the secret lives in GitHub's store and
never enters a VM. The narrowed census is the pilot.
