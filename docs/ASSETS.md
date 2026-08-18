# docs/ASSETS.md - what this project built, so none of it is lost by being forgotten

**Written 2026-08-18, packet 5 Phase B3.** Every entry states what it is, where it lives, how to
verify it still works, what it would cost to rebuild, and what it would cost to point at a
different venue.

---

## 1. The R2 dataset - five years of settled Kalshi markets, scoped

| | |
|---|---|
| **What** | 110,836 settled market rows, 30 series, gzipped NDJSON, one object per series |
| **Where** | R2 bucket `smart-money-data`, prefix `phase1/2026-08-17/` |
| **Size** | 241.0 MB raw, **10.1 MB gzipped** (4.2% - the JSON is highly repetitive) |
| **Manifest** | `data/phase1/MANIFEST.json` - per-object sha256, byte count, row count, page count |
| **Scope rationale** | `data/SCOPE.md`, sealed *before* collection; `data/SCOPE-EVIDENCE.json` holds the raw derivation |
| **Gate evidence** | `data/phase1/GATES.json` |

**Why these 30 series and not others.** The scope was derived, not chosen: every `KX*` token in
`registry/hypotheses.json` (18 series) unioned with every `KX*` token in `analysis/` (20 tokens, 19
after excluding `KXMVE*` a priori). **12 of the 30 appear only in `analysis/`** - including
`KXHIGHNY`, the most-used weather series in the repo, which a registry-only scan would have dropped.
The prediction was stated before collecting and landed at **-0.7% on rows**.

**Four of the 30 have zero historical rows**, each explained: `KXRAIN` (earliest event 2026-07-16,
the whole series postdates the cutoff), `KXAGENCYELIM`, `KXEUREF`, `KXEUEXITCOUNTRY` (one event
each, resolving 2029-2030).

### Verification procedure - the one that has actually been run

1. Fetch `data/phase1/MANIFEST.json` unauthenticated from GitHub.
2. Pick objects at random from it (the runs to date used seed 1404).
3. `GET` each from R2 **authenticated** - and probe an impossible key in the same pass. Unauthenticated
   probes return **400 for real and impossible keys alike** and certify nothing; authenticated,
   the control returns **404** against **200**.
4. Compare byte count and sha256 against the manifest, then decompress and check the row count.

Run cold from a third metro on 2026-08-18: **3 of 3 byte-identical**, row counts exact, control 404.

### Extending it

`series_ticker=` is honoured on `/historical/markets` and verified against an impossible control.
Add a series by appending it to the scope list and re-running the collector; the endpoint ignores
`min_ts`/`max_ts`, so time filtering is client-side. Note that `status` on the historical path is
**`finalized`, never `settled`** - a collector carrying the live-list rule across filters away 100%
of rows and reports an empty dataset as an honest zero. And `result` is **not binary**: `KXMLBGAME`
returns `scalar` on ~1% of rows.

**Rebuild cost:** ~130 requests and about 12 minutes at a safe rate. Cheap - because the scope is
narrow. The unscoped equivalent was 7.27 GB and 19,483 requests, a **30x** reduction.
**Repoint cost:** the collector is endpoint-shaped, not venue-shaped; a new venue needs a new
pagination contract and a new filter-honouring table, which is a day of measurement, not of code.

---

## 2. The code

| asset | path | what it is | rebuild | repoint |
|---|---|---|---|---|
| **Collector** | packet 4 T1.2 | paginates `/historical/markets` per series, writes NDJSON, gzips, uploads, verifies through LIST, deletes locally, checkpoints per series. Survives a 352 MB disk. | ~2h | endpoint contract only |
| **Fee model** | `analysis/fees/fee_model.py` | Kalshi fee ceiling **per fill, to a centicent**: `_ceil_to(trade_fee_raw, 0.0001)`. All three documented worked examples reproduce exactly. | ~3h incl. doc reading | venue-specific, rewrite |
| **SigV4 shim** | `scripts/r2sig.py` | hand-rolled S3 signing over curl, ~40 lines of SigV4. Streaming `request_file()` so the body never enters memory. | ~4h | none - S3 is S3 |
| **R2 CLI** | `scripts/r2.py` | `roundtrip` / `put` / `get` / `ls` / `rm`; the roundtrip gate exits non-zero unless bytes match, the object lists, delete removes it, and an impossible control key is **not** readable | ~1h | none |
| **Write path** | `scripts/gh_commit.py` | commits via the Contents API over curl. `check` proves write access **by writing**, reading back unauthenticated, comparing and deleting. `put` is **create-only** unless `--update`, and a create returning 200 is a failure. | ~3h | none |
| **Index generator** | `scripts/build_index.py` | regenerates `registry/INDEX.md` from `hypotheses.json` | ~1h | none |
| **Tests** | `tests/` | 47+ Python regression tests plus 16 worker tests. `python3 -m unittest discover -s tests -t .` | - | - |

### The SigV4 shim's three ceilings, all found before they cost a run

1. **`Expect: 100-continue` is never answered.** A 16 MB PUT returned `http=100` after 120 s. With
   `-H 'Expect:'` the same PUT completes in **2.6 s**. Send it on every PUT, and never count a 1xx
   as success.
2. **Memory.** A 256 MB in-memory PUT was OOM-killed on a 977 MB VM. `request_file()` streams:
   128 MB at 9.3 MB/s with flat RAM.
3. **Disk.** VM disk has been measured at 9.8 GB and at **783 MB total / 352 MB free**. A collector
   that accumulates before uploading dies on the small ones. One series file, upload, delete, move on.

**Why not boto3:** measured inside a Kernel VM, LIST succeeds, `curl -X PUT` returns a real R2 error
in 0.15 s, and boto3's `put_object` **hangs indefinitely** through the same proxy with the same
credentials. Forty lines of SigV4 is a smaller dependency than a hang nobody can explain.

---

## 3. The registry as a research artifact

`registry/hypotheses.json` is the main artifact, not a by-product. It holds 56 entries with verdict,
figures, `revive_if` conditions, limitations stated as limitations, the fifteen mechanisms, the
method rules each failure produced, and 19 infrastructure facts. `registry/h*-preregistration.md`
hold the rules sealed before outcomes; `registry/INDEX.md` is generated from the JSON and says so.

**Its value is the negative space.** Forty-five kills with the reason recorded is a screening tool:
a new idea can be checked against the fifteen mechanisms in five minutes, and most new ideas turn
out to be one of them renamed. That is worth more than any single entry.

**Rebuild cost: not rebuildable.** It is the record of two weeks of measurement; the figures could
be re-derived only by re-running the studies, and six entries (H22-H27, H32, H45) are already
recorded as **lost to a 2026-08-10 rollback and not reconstructed**.
**Repoint cost:** the schema transfers unchanged. The content does not.

---

## 4. The durable write path

This is an asset in its own right and it took three sessions to establish. Data written by a VM
survives that VM's destruction; a fresh machine in a different metro can retrieve tooling from the
public repo, take credentials from a paste, and verify the dataset byte-for-byte. Proven end to end
on 2026-08-18 across three metros (`jfk` collected, `iad` and `yul` verified).

**The known limit, stated because it is load-bearing:** the credential has **no route** into a
fresh machine except a paste. The data outlives every machine; the *ability to verify it* does not
travel. The mitigation chosen is not a credential store but making loss cheap - **commit every
artefact as it is produced**, and stage to R2 when no token is present.

---

## Amendment, 2026-08-18 - section 4's known limit is lifted for scheduled work

Section 4 above says *"the credential has no route into a fresh machine except a paste ... the data
outlives every machine; the ability to verify it does not travel."* That stands for **interactive**
sessions on a fresh VM. **For scheduled work it is no longer true**, and the asset list gains an
entry.

### 5. The unattended measurement path

| | |
|---|---|
| **What** | A GitHub Actions workflow that probes an external venue, carries both an impossible control and a known-present positive control in the same pass, appends one line to a log, and commits it |
| **Where** | `.github/workflows/census.yml`; output at `registry/retention/CI-CENSUS-LOG.md` |
| **Credential** | the platform-issued `GITHUB_TOKEN`. **No PAT, no paste, no human** |
| **Proven** | run #1, `2026-08-18T06:01:34Z`, success; commit `bc2c8bf` authored and committed by `github-actions[bot]` |
| **Rebuild cost** | ~1h. It is 70 lines of YAML |
| **Repoint cost** | **near zero.** Nothing in it is Kalshi-specific except three URLs and the names of the two control keys |

**Why it is an asset and not a chore.** It is the only part of this project that keeps working when
nobody is watching. Section 2b of `CLOSEOUT-2026-08-18.md` describes a class of question that closed
permanently because an external archive stopped and nobody noticed for two months. A scheduled probe
with controls is the cheapest defence against that happening again - not because it prevents the
stop, but because it **dates** it.

**The limit, carried forward:** seven requests per run. This establishes reachability and the write
path, not a rate-limit regime. A GitHub-hosted runner IP is shared and its bucket history is set by
strangers, so the ~6 req/s clean band measured from a Kernel VM must be **re-measured on Actions**,
counterbalanced, before any bulk pull moves there. **Census-scale: established. Bulk: unmeasured.**
