# PARKED

Items that terminate in a **decision**, a **verdict**, a **revival** or a **resource
commitment**. Under the packet 3 autonomy contract these are not mine to make during an
unsupervised run. Each entry is a completed piece of work: the evidence is gathered and the
options are stated. Only the ruling is missing.

Ranked by how much each blocks.

---

## P1 — The fee model in `docs/INFRA.md` is wrong, and it is load-bearing

**Blocks:** the cost model of every extreme-price hypothesis, and any re-measurement of the
hurdle at size. This is the highest-value item in the lot.

**Evidence.** `docs/INFRA.md` records *"Fees: taker `ceil(M·0.07·p·(1−p))` … rounded up on order
total."* Kalshi's documentation says the **trade fee** rounds up to a **centicent per fill**, and
that whole-cent behaviour comes from a separate balance-precision **rounding fee** which a
per-order **accumulator** then rebates. All three documented worked examples reproduce exactly
under the documented model — see `registry/fees/A1-FEE-ROUNDING-2026-08-15.md`.

**Options.**
(a) Correct `docs/INFRA.md` to the documented model and tag it `[measured 2026-08-15]`.
(b) Leave it and add a warning note.
(c) Withhold until the base formula is also resolved (see P3).

**Recommendation:** (a). The rounding model is documented and reproduced; the unresolved base
formula is a separate, clearly-scoped gap and does not justify leaving a known-wrong rule in place.

---

## P2 — The extreme-price family may be size-dependent kills

**Blocks:** whether H7, H9, H33, H34, H53, H55 and H64 were killed by the market or by an
assumed order size of one contract.

**Evidence.** Effective fee per contract, multiplier 1.0: at p=0.97, **1.0000¢ at one contract
against 0.2100¢ at a hundred** — 4.76×. At p=0.99, 14.29×. At p=0.50, 1.14×. The quantisation
binds **only** at the extremes, which is exactly where this family lives. Fragmentation does not
undo it: the per-order accumulator holds 100 contracts at 0.2100¢ whether filled in 1, 5 or 20
pieces.

**This is a `revive_if` come due**, and the packet forbids me from acting on it. C1 will produce
the per-entry audit; the ruling on any entry it names as size-dependent is Walton's.

**Options.** (a) Re-run the named entries at realistic size under a corrected cost model.
(b) Re-run only where depth evidence exists to support the size. (c) Leave all verdicts.

**Recommendation:** (b), and it depends on B2. **The size that amortises the fee is the same size
that must be resting at the ask.** A revival justified by a fee model but unsupported by depth
would repeat H61's error — a real effect that could not be obtained.

---

## P3 — The base fee formula is not established

**Blocks:** any absolute cost figure. Not the qualitative shape, which holds for any small base fee.

**Evidence.** Kalshi's rounding page states a trade fee of **\$0.0085 for 1 contract at \$0.055**.
`0.07·p·(1−p)` gives **\$0.003638**. No reachable page states the model. Series expose
`fee_type` — `quadratic`, `quadratic_with_maker_fees` — **a field this project has never read** —
and `fee_multiplier`, but the mapping from `fee_type` to a formula was not found.

**Options.** (a) Ask Kalshi support. (b) Infer from live fills — requires trading, which is
forbidden. (c) Bound it: collect settled trades and back out the implied rate. (d) Leave `rate` a
parameter and state the assumption everywhere.

**Recommendation:** (d) now, (c) as a measurement in a later packet. (b) is not available.

---

## P4 — H57's `revive_if` wording is a judgement about intent

**Blocks:** whether H57 is revivable at all. Flagged by the packet itself as the live example.

**Evidence.** `H57.revive_if` reads: *"At least 100 NEW KXRAIN events have settled that were not
in the 2026-08-12 universe."*

**Reading A — not satisfied.** "New" means newly settled, after 2026-08-12. Historical events are
old; they were merely unreachable. Under this reading H57 waits for calendar time.

**Reading B — satisfied, or nearly.** The clause names events "not in the 2026-08-12 universe",
and that universe was bounded by what the live endpoint reached. Events recoverable from
`/historical` were genuinely not in it. Under this reading the condition is about sample novelty,
not event age.

The wording supports both. **Walton rules.** Note that KXRAIN is also a young series — 24 events
total, earliest `KXRAIN-26AUG01` — so under either reading the available count needs measuring
against `/historical` before the ruling means anything. A2 will produce that number.

---

## P5 — H64's fee explanation is wrong in its reasoning

**Blocks:** nothing operational. Recorded so it is not inherited as fact.

**Evidence.** `H64-RESULT.md` says all 254 rungs "were charged exactly 1 cent" because Kalshi
"rounds fees up to whole cents on the order total". Nothing was charged — H64 was a paper study
and the 1¢ was computed by my own code from the inherited INFRA.md formula. The number is right
for one contract and a non-direct member, by balance rounding rather than by the trade-fee ceiling.
The conclusion that the fee advantage "does not exist in practice" is **wrong at size**.

**H64's verdict and every figure are untouched**, and its headline result does not depend on this:
the fee correction shifts the mean well inside the interval's half-width and changes no robustness
check.

**Options.** (a) Amendment to `H64-RESULT.md` correcting the reasoning, verdict untouched.
(b) Leave it; A1 already records the correction.

**Recommendation:** (a), as an appended amendment under the amend-never-edit rule.

---

## P6 — the A1 deliverable's filename is dated one day ahead of its measurement

**Blocks:** nothing. Cosmetic, but it is a date on a registry artefact.

**Evidence.** `registry/fees/A1-FEE-ROUNDING-2026-08-15.md` was written and committed on
**2026-08-14**. Three independent clocks agree on the true date: the Cowork host, the Kernel VM,
and the `Date:` response header from `api.elections.kalshi.com` (`Fri, 14 Aug 2026`). The packet's
run window is 2026-08-15 → 2026-08-17, so the run began a day early and the filename took the
planned date rather than the measured one. `RUN-LOG.md`'s session-1 block inherits the same date.

**Options.** (a) Leave both, and let this entry carry the correction. (b) Rename the file and
rewrite the index — a committed registry path change mid-run, for a cosmetic reason.

**Recommendation:** (a). Later deliverables in this run are dated 2026-08-14, correctly.

---

## P7 — packet 2's 4,787-event universe count is an undercount

**Blocks:** any Phase B sample-size estimate that inherits it.

**Evidence.** The 4,787-event figure for 2026-06-07 → 06-11 was derived from the **live** path
alone. `registry/historical/REACH-2026-08-14.md` §A2.2 measures the same window on both paths:
`/historical` returns 56 events against live's 36 over 06-07→06-10, with **20 events only on
historical and zero only on live**; a run over a window one day wider gave 74 against 54, the same
delta of 20. The live `/markets` endpoint has a sliding `close_time` floor, so any window
straddling it is under-reported by construction. The size of the shortfall on the full 4,787
figure has **not** been measured — only that its sign is negative.

**Options.** (a) Re-derive the window from the union of both paths and record the corrected count
as a new dated measurement. (b) Annotate the original figure as an undercount and leave it.
(c) Both.

**Recommendation:** (c), but the re-derivation is a Phase B activity and changing a recorded
figure is forbidden in this run. Parked.

---

## P8 — `open_interest_fp` disagrees between the live and historical paths

**Blocks:** any study using open interest across the boundary. Silently, with no error.

**Evidence.** For 41 markets across four events inside the overlap band, the live and historical
rows are **identical on all 45 fields except one**: `open_interest_fp`. Historical returns `0.00`
for **41 of 41**; live returns 48789.67 / 22196.76 / 1939544.19 / 993.00 for the four events'
first rungs. Both endpoints return HTTP 200 and neither signals a default.

Two readings survive: open interest legitimately falls to zero once positions settle, making
historical correct and live a stale high-water mark; or the historical export drops the field.
Nothing measured separates them. A settled-market open-interest series read from `/historical`
would be all zeros, and a series joined across the 2026-06-08 boundary would show a cliff.

**Options.** (a) Probe `/historical/positions` or `/historical/trades` for the same markets and
reconstruct open interest independently — decides it. (b) Treat historical `open_interest_fp` as
unusable and say so in INFRA.md. (c) Ask Kalshi.

**Recommendation:** (a), then (b) whichever way it lands. (a) is cheap and is a genuine
cross-endpoint check rather than a second call to the same one.

---

## P9 — the live/historical overlap band is closing, on a dated schedule

**Blocks:** collection urgency. This is the one entry here with a clock on it.

**Evidence.** Two measured quantities move in opposite directions. The live `/markets`
`close_time` floor sat at **2026-06-08** on 2026-08-14 and `docs/INFRA.md` records it advancing
**exactly one day per day**, uniform across sixteen series spanning 25 to 6,348 events; A3
confirms it from a third product family (seven 15-minute crypto series exhaust at 6,449–6,451
distinct events, against 67 days × 96/day = 6,432, within 0.3%). `/historical/cutoff`
`market_settled_ts` reads **2026-06-14T00:00:00Z** and has not moved across this project's
records.

If both hold, the floor passes the cutoff on or about **2026-08-20**, and a reachability gap
opens between the two paths that widens by a day per day.

**This is a prediction, not a finding.** The likeliest resolution is that historical ingestion is
batched and the cutoff jumps forward, in which case nothing is lost. But the failure mode is
asymmetric: if the cutoff is frozen, waiting costs data permanently, and the window to notice is
about six days.

**Options.** (a) Do nothing; the daily census will answer it. (b) Collect the at-risk band
(2026-06-08 → 2026-06-14, both paths) now, before it can move. (c) Escalate to Walton for a
collection decision.

**Recommendation:** (a) plus a cheap insurance policy — the daily census now records
`/historical/cutoff` and one series' live floor, so the answer exists by 2026-08-20 whichever way
it goes. (b) is a resource commitment and is Walton's call.

---

## P10 — where the B1 dataset lives, and whether it should live in the repo

**Blocks:** every Phase B and Phase D study that would use it. Right now the data exists only in an
ephemeral Kernel VM.

**Evidence.** B1 collected **7,269,014 markets** across 6,703 series — about **1 GB** gzipped in the
projected 24-field form, roughly 3.4 GB raw. The packet's instruction is explicit: *"If the volume
is too large for the repo, collect anyway, write the manifest and summary statistics into the repo,
and park the storage question. Do not silently drop rows. Do not commit gigabytes without asking."*
That is what was done: `data/historical/MANIFEST.json` carries per-series row counts, unique-ticker
counts, unique-event counts, date coverage and **sha256 per file**; the data itself is not
committed.

**The exposure.** The VM is reclaimed after inactivity. When it goes, the 7.27M rows go with it.
What survives is the manifest, `scripts/b1_collect.py`, and the collector state — enough to
reproduce the pull in about 90 minutes of active VM time, not enough to reproduce it *identically*
if Kalshi's cutoff has advanced by then.

**Options.** (a) Commit it, gzipped, ~1 GB across 6,703 files — a large repository, and the packet
says not without asking. (b) Git LFS. (c) An external object store (R2/S3) with the manifest's
sha256 list as the integrity record. (d) Do not store it; re-run the collector when a study needs
it, accepting that the boundary will have moved. (e) Store only the series a study actually needs
— weather, macro and sports are 1.33M rows, about 18% of the total.

**Recommendation:** (e) now and (c) if it recurs. Two-thirds of the volume is intraday crypto and
FX strike ladders that no entry in this registry studies. **But this is a resource commitment and
it is Walton's call.**

---

## P11 — H56's hurdle was computed with a size-free cost model

**Blocks:** the calibration of every kill in the registry. This is the highest-leverage parked item.

**Evidence.** C1 (`registry/FEE-CEILING-AUDIT.md`) swept every entry whose verdict rests on an
extreme band and found that **not one states the order size its cost model assumed** — because every
cost model in this project is the per-contract continuous function `0.07·p·(1−p)`, which has no size
parameter. A1 showed the real schedule has a **$0.01 balance-precision floor per fill** for a
non-direct member, which at p=0.99 is **14.29×** the continuous fee at one contract and vanishes by
a hundred.

H56's −4.03¢ / −4.39¢ is the bar every other idea is measured against. If it was priced at the
continuous fee it is the **size-infinite** hurdle, and ideas killed against it were killed against a
bar a one-contract trader can never reach. If it was priced implicitly at one contract, the bar is
too high at size. **Which is true was not determined** — it needs H56's estimator read, not its
registry entry.

**Options.** (a) Read `analysis/h56/` and state the assumed size; cheap, and settles the question of
*which* hurdle exists today. (b) Re-measure the hurdle at an explicit size ladder (1 / 10 / 100 /
1000 contracts) on B1's data — this is the Phase D candidate the packet names. (c) Leave it.

**Recommendation:** (a) unconditionally, since it changes no figure and answers half the question.
(b) is a new study and needs a sealed pre-registration.

---

## P12 — H15's negRisk gap sits between the small-size and large-size fee

**Blocks:** nothing operational. A verdict whose size-dependence is undetermined.

**Evidence.** H15 was killed on a negRisk set summing to **0.9970** — a 0.30¢ gross gap. Under A1's
schedule the per-leg fee is **1.00¢ at one contract** (the gap is then hopeless) and about
**0.07¢ at a hundred** (the gap then exceeds the fee). The kill is safe at one contract and
**undetermined at size**, and nothing in the entry states which it assumed.

**Caveat that may dissolve it:** a negRisk set has several legs, so the fee is paid several times
while the gap is earned once, and Polymarket's fee schedule is not Kalshi's — A1's arithmetic does
not transfer without checking. This is flagged as a question, not as a finding.

**Options.** (a) Read H15's cost model and state its assumed size and venue. (b) Re-measure at size.
(c) Leave it — negRisk sets that sum below \$1 are rare and the depth to trade them at size may not
exist, which would settle it without any arithmetic.

**Recommendation:** (a), then (c) if the depth is not there. Low priority.

---

## P13 — PHASE D: the hurdle re-measured at size. Parked, which is the correct outcome.

**Blocks:** nothing. This is a study design held back deliberately.

The packet permits a new study only under **all four** of its conditions. Checked one at a time:

| condition | status |
|---|---|
| 1. Gate 1 answered every question affirmatively | **FAILS.** Four of five are answered. The fee question is answered only in its structural half — the ceiling is per fill — and its numerical half is explicitly *could not establish*: Kalshi's own worked example gives \$0.0085 for one contract at \$0.055 against \$0.003638 from `0.07·p·(1−p)`. |
| 2. The instrument is fully characterised, no open questions of any kind | **FAILS.** `open_interest_fp` disagrees between paths (**P8**); the live/historical boundary may open a gap on ~2026-08-20 (**P9**); authenticated reach is untested; 4.1% of archive snapshot rows are unbracketable. |
| 3. Pre-registration sealed and committed in its own commit before any outcome is touched | Not started. Achievable, but conditions 1 and 2 already fail. |
| 4. Does not require reviving a parked entry | **FAILS.** The study *is* **P11** — determining what size H56's hurdle assumed. |

**Three of four fail.** The design is therefore parked rather than run, exactly as the packet
anticipated: *"Realistically: expect to park this. That is the correct outcome."*

**What the design would be, recorded so it is not re-derived from scratch.** Re-measure the
cost of crossing at an explicit size ladder — 1 / 10 / 100 / 1,000 contracts — across the price
range, using `analysis/fees/fee_model.py` with `rate` a visible parameter and
`target_precision` set for both direct and non-direct membership, over B1's 7.27M-market
universe. Report the hurdle as a **function of size and price**, not a scalar. Every kill in the
registry currently calibrates against a scalar.

**Unblocking it needs, in order:** A1's base-rate gap closed (the docs' worked example
reconciled), P11 answered by reading `analysis/h56/`, and P8 resolved or the field excluded.
None requires new collection.

---

## P14 — the `ticker=` audit clears every committed collector, on three independent signatures

**Blocks:** nothing directly. It bounds how far the `ticker=` defect can have propagated.

**Signature 1 — source (T3.1).** All 127 committed files scanned for `?ticker=` / `&ticker=` in a
URL, `{'ticker': …}` in a params dict, and any bare `ticker=`; every hit read by eye. **No
committed code has ever used `ticker=` as an API filter.** Only three committed files make HTTP
calls at all: `scripts/b1_collect.py` (`series_ticker=`, honoured), `analysis/h56/grab.py`
(ticker as a **path segment** — `/series/{s}/markets/{ticker}/candlesticks` — which is honoured,
so **H56, the hurdle, is clean**), and `scripts/gh_commit.py` (GitHub, not Kalshi). Everything
else is documentation of the defect, a test that models it, a JS property comparison, or an
f-string column header.

**Signature 2 — junk rows.** No committed data file contains a `KXMVE` market row, and no study's
data shows the repeated-timestamp pattern a filtered-to-the-head pull would leave. The closest
look-alikes (`h53/markets_raw.txt`, 126 tickers over 15 timestamps) are mutually-exclusive ladders
sharing one event `close_time` by construction.

**Signature 3 — ticker mismatch (Addendum A3).** Signatures 1 and 2 both fail if a dead collector
fetched the unfiltered head and applied the standing `KXMVE*` exclusion afterwards. This one does
not. For every committed data file whose intended ticker is recoverable, every row was checked
against it:

| study | files | rows checked | **mismatches** | intended set from |
|---|---|---|---|---|
| H50 (`analysis/h50/data`) | 22 | 2,398 | **0** | filename |
| market-making (`analysis/mm`) | 20 | 4,497 | **0** | filename |
| H53 (`urls.txt`) | 108 | 108 | **0** | URL vs label |
| H53 (`urls2.txt`) | 72 | 72 | **0** | URL vs label |
| **total** | | **7,075** | **0** | |

Every H53 URL requests `/series/{s}/markets/{ticker}/candlesticks` — the path-segment form. None
used a query filter.

**Where the intended set cannot be recovered, per hypothesis:**

| study | why |
|---|---|
| H55, H57, H58 | collector `/tmp/h5x/collect.py` never committed; only summary statistics survive |
| H64 | `/tmp/h64/cand2.py` and `rows.json` never committed; its events are not enumerated in the repo |
| H56 | `rows.json` not committed — `events.csv` has event tickers but not per-rung market tickers |
| H52 | trade-level pull never committed |
| H1, H2, H3, H44 | Polymarket wallet and tape studies — no Kalshi tickers at all |

**Affected hypothesis IDs: none identified. A negative result from an incomplete instrument.**
That phrasing is kept deliberately: three signatures agree, and none of them can reach the
collectors that no longer exist.

**Options.** (a) Accept the bound and record that uncommitted collectors are permanently
unauditable. (b) A standing rule that a collector is committed **before** its results are, so the
hole cannot reopen. (c) Re-derive the highest-stakes results from a rebuilt dataset.

**Recommendation:** (b) unconditionally — free, and the actual lesson. Then (c) for H56 and H64.
**No verdict is changed by this entry.**

---

## P15 — the CI write path is blocked by a token permission, not by anything technical

**Blocks:** the durable, human-free write path. Everything this project writes today needs a human
to paste a credential into a fresh VM.

**Status: could not establish.** `PUT .github/workflows/census.yml` returns **403**. The per-session
fine-grained PAT carries `Contents: write` but not `Workflows: write` — GitHub treats them as
separate permissions, and every other write in the same session with the same token succeeded.

**What is therefore untested, and must not be reported as working:** whether a GitHub Actions runner
reaches `api.elections.kalshi.com` cleanly, what status codes it sees, and whether the built-in
`GITHUB_TOKEN` commits without any paste. **No census workflow has ever run.** The repository's only
workflows are `automerge.yml` and GitHub's own pages build.

**The workflow is written and committed out of the way** at `.github/CENSUS-WORKFLOW-PENDING.md` so
it is not rebuilt from memory: `workflow_dispatch` plus a daily cron, probing `/historical/cutoff`
and the live floor with **both** an impossible control and a known-present positive control, then
appending one line to `registry/retention/CI-CENSUS-LOG.md` and committing with `GITHUB_TOKEN`.

**Unblocked by either:** a PAT with the Workflows permission, or one manual commit of that file
through the web UI — after which it runs on schedule with no paste at all, forever.

**revive_if:** either unblock happens. Then the first run answers three questions at once —
reachability, status codes, and whether the project can write without a human.

---

## P16 — a two-hour hole in Kalshi's settled trade history, 2026-06-11T07–T08

**Blocks:** nothing currently, but it silently corrupts any per-hour activity measure over 11 June.

`/historical/trades` returns **13 trades for `T07`, all inside the first 0.26 seconds**, and **zero
for `T08`**, while `T06` and `T09` and the same hours on neighbouring days all hit the 1,000-row cap.
Reproduced on a second direct probe with clean window boundaries.

**Why it matters:** a collector reads those hours as **quiet**, not as **missing**. In Check 1,
excluding them moved a diurnal-matched comparison from **+3.6% to +10.6%** — the outage was doing a
quarter of the work of the headline number.

**Not diagnosed:** whether it is an exchange outage, a history-backfill gap, or an API artefact. It
sits four hours after the `archive.pmxt.dev` collector stopped at `2026-06-11T03`, which is
suggestive and cannot be followed up — there is no shard left to compare against.

**revive_if:** any study uses 11 June 2026 at hourly resolution.

---

## P17 — T1.4's first-pass statement was certified by a void control. UNVERIFIED.

**Walton's ruling, 2026-08-18.** Recorded as a ruling, not as a measurement.

**The claim:** T1.4's first pass, run from a fresh VM before the collecting VM was destroyed,
reported that the three sampled R2 objects were **unreadable without credentials**.

**Why it is unverified:** the control that certified it was an unauthenticated probe of a private
bucket. A **400 meaning "forbidden"** and a **400 meaning "absent"** are indistinguishable, and the
impossible control key returned exactly the same 400 as the three real objects. The probe could not
separate the two states, so it established nothing about either.

**Status: probably true, not shown.** The claim is almost certainly correct — a private bucket does
refuse anonymous reads, and the authenticated pass two hours later found the objects present and
intact. **That does not retro-certify it.** Walton's ruling states the principle:

> **A claim certified by a void control is unverified even when a later measurement makes it look
> obvious.**

The later measurement answered a *different* question. "The objects exist and hash correctly when
authenticated" is not "the objects are unreadable when unauthenticated"; the second is a claim about
the access boundary, and no probe that can distinguish forbidden from absent has been run against it.

**What is NOT affected.** Every R2 claim resting on the **authenticated 404 control stands** —
control 404 against real 200, re-verified 2026-08-18. That covers: the T1.4 second pass (3 of 3
byte-identical), Gate 0 line 3 (data read back from a destroyed VM's write, another metro), the
Phase 1 per-object LIST verification, the `r2.py` roundtrip gate, and the packet 5 handoff
re-download. **No verdict, figure or `revive_if` changes.**

**revive_if:** anyone runs an anonymous probe against the bucket that can separate the two states —
for example an unauthenticated request that is well-formed enough to earn a 403 rather than a 400,
alongside a public object in the same bucket as a positive control. Until then the access boundary
is assumed, not measured.

**Why it is parked rather than dropped:** the standing use of R2 assumes the data is not world
readable. That assumption is now explicitly untested rather than quietly inherited.

---

## P15 - RESOLVED 2026-08-18. The CI write path works end to end.

**Unparked, not amended away.** The entry above stands as the record of the block; this is what
lifted it.

Walton added **Workflows: read and write** to the PAT and the workflow landed. **Run #1 green.**
Verified from the resources, each with a control - impossible commit sha **422**, run #1
**success**, commit **`bc2c8bf`** authored *and* committed by **`github-actions[bot]`**, writing
`registry/retention/CI-CENSUS-LOG.md`. **The built-in `GITHUB_TOKEN` did it. No PAT, no paste, no
human.**

Kalshi from a shared GitHub runner IP: cutoff **200**, live floor **200**, impossible-series control
**200 with 0 rows**, positive control **200**. Both controls in the same pass.

**What was actually being tested was never the census.** It was whether this project can measure an
external venue and record the result without a human present. It can. Full finding in
`docs/INFRA.md`, *"THE DURABLE WRITE PATH"*.

**What remains unmeasured, and is not covered by this:** bulk collection from CI. Seven requests
establish reachability, not a rate-limit regime, and the shared runner IP has a bucket history set
by strangers. That has to be re-measured on Actions, counterbalanced, before any bulk pull moves
there. **Census-scale scheduled measurement: established. Bulk collection from CI: unmeasured.**

---

## P18 - the PAT cannot write `.github/workflows/` or dispatch a run. A0's verification is unreachable.

**Blocks: packet 6 A0 step 4, and therefore Phase B.** It also re-opens, in a narrower form, the
question P15 closed.

**Three 403s, isolated by probe rather than assumed:**

| attempt | result |
|---|---|
| Git Data API, tree **containing** `.github/workflows/census.yml` | **403** `Resource not accessible by personal access token` |
| Git Data API, identical tree of 240 entries **without** that path | **201** |
| Contents API, `PUT .github/workflows/census.yml` | **403** `refusing to allow a Personal Access Token to create or update workflow ... without workflow scope` |
| `POST /actions/workflows/census.yml/dispatches` | **403** `Resource not accessible by personal access token` |

The first two are the control pair: same endpoint, same token, same tree size, **one path
different**. That is what identifies the cause. The Git Data 403 message names the token generally
and is misleading - the token *is* accessible to that endpoint, just not for that path. Another
status naming the wrong cause.

**Consequence, and what was done about it.** A0 required the workflow's paths to move in the same
commit as the restructure, then a live run to prove the unattended probe still writes. Neither is
possible with this credential. A0's own fallback was executed: **`registry/retention/` was returned
to the repo root**, so the workflow's paths are byte-identical to what run #1 used and nothing it
touches has moved. Everything else stayed restructured.

**The probe is therefore untouched, not verified.** It should behave exactly as it did on run #1 -
but *should* is not *did*, and this project has already paid for that distinction once.

**revive_if - any one of these:**

1. The PAT gains **Workflows: read and write** *and* **Actions: read and write**. Then the path moves
   and the run is dispatched in one session.
2. Walton clicks **Run workflow** in the UI now. That alone verifies the current parked state - a
   `github-actions[bot]` commit with the control pair separating - and unblocks Phase B without any
   permission change.
3. The `17 4 * * *` cron fires (next: **2026-08-19T04:17Z**). Same verification, ~21 hours later,
   unattended - which is the more faithful test of the thing being claimed.

**Until one of those:** `registry/retention/` stays at the root and `programmes/kalshi/README.md`
says why, so nobody tidies it away without reading this.

### P18 update, 2026-08-18 - VERIFIED by dispatch. The probe survived the restructure.

**Route 2 taken.** Walton dispatched the workflow manually; verified here from the resources with a
control, not from the report:

| check | result |
|---|---|
| control: impossible commit sha | **422** (not 200) |
| run **#2** | **completed / success**, `2026-08-18T06:55:49Z` |
| commit **`69cca04`** author *and* committer | **`github-actions[bot]`** |
| what it wrote | `registry/retention/CI-CENSUS-LOG.md` (modified, **+1**) |
| the four probes | cutoff **200**, live floor **200**, impossible-series control **200 / 0 rows**, positive control **200** |

**The control pair separates**, which is what makes the four 200s mean anything: the impossible
series returns 200-with-0-rows against a known-present series returning 200. **A 113-file
restructure landed underneath this probe and it still writes.**

**Route 3 has not been consumed and should be allowed to fire.** The `17 4 * * *` cron next runs at
**2026-08-19T04:17Z**. Run #2 was *dispatched by a human*; the cron run is **unattended**, which is
the more faithful test of the property being claimed - that this project can measure and record with
nobody present. A dispatched green run proves the paths are right. Only the scheduled one proves the
thing P15 was actually about. **Check that it landed.**

**Still parked, and still the reason `registry/retention/` sits at the root:** the credential cannot
write `.github/workflows/` by any API, nor dispatch a run. Routes 1 remains open. Until then the
directory stays where it is and `programmes/kalshi/README.md` explains why.

**Incidental, from the two rows now in the log.** Between `06:01Z` and `06:55Z` the cutoff advanced
`2026-06-18` -> `2026-06-19` and the live floor `2026-06-11T04:59` -> `2026-06-12T04:59` - a full
day on both edges inside 54 minutes, with **the gap constant at 7 days**. The boundary appears to
step once daily rather than sliding continuously, and the two rows straddled the step. Benign, and
visible only because the census now has more than one row.
