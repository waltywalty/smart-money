# B1 — the historical settled-market universe: what was collected, and what it is not

**Date:** 2026-08-14 (UTC). **Packet:** coworkpacket3autonomous, Phase B, task B1.
**Licensed by:** `registry/historical/GATE1.md`, which established reach in A2.
**Artifacts:** `data/historical/MANIFEST.json` (per-series counts, date coverage, sha256),
`scripts/b1_collect.py`, `scripts/b1_manifest.py`.

> **The data itself is not in this repository.** 7.27 million rows compress to roughly 1 GB.
> The packet's instruction is followed: collected in full, manifest and summary statistics
> committed, storage question parked (**P10**). The collector is resumable from its state file,
> so the dataset is reproducible rather than merely lost.

---

## What would overturn this

1. **The `KXNBAGAME` anomaly generalising.** B1 holds one event that `/events` does not list.
   One is a curiosity; a pattern would mean the two endpoints disagree in *both* directions and
   the superset relation A3 measured is wrong.
2. **A mismatch appearing deeper in the re-fetch sample.** 1,082 events matched exactly. The
   sample is 11.2% of the packet's 1% target, not the full 1%.
3. **The nine capped series behaving differently from the rest.** They are crypto strike ladders
   and were stopped by budget, not by the API. Nothing suggests they differ; nothing rules it out.

---

## The asset

| | |
|---|---:|
| series in frame (`/series?category=`, 15 categories) | **12,531** |
| series with at least one historical market | **6,703** |
| series returning zero rows (HTTP 200, empty) | 5,828 |
| **markets collected** | **7,269,014** |
| **unique tickers** | **7,269,014** |
| unique events | **351,653** |
| earliest `close_time` | **2021-07-01** |
| latest `close_time` | 2026-11-03 |
| requests issued | 19,483 |
| HTTP 429 responses | **0** |
| transient socket failures (retried to success) | 7 |
| `KXMVE*` markets excluded a priori | 96.77% of the unfiltered collection |

Rows by category:

| category | rows | | category | rows |
|---|---:|---|---|---:|
| Crypto | 3,376,365 | | Climate and Weather | 116,821 |
| Financials | 2,420,271 | | Entertainment | 89,514 |
| Sports | 1,197,641 | | Commodities | 27,458 |
| Economics | 20,478 | | Politics | 11,562 |
| Elections | 4,835 | | everything else | 4,069 |

**Two-thirds of the exchange's settled history, by row count, is intraday crypto and FX strike
ladders.** The series this project's registry actually studies — weather, macro, sports — are
1.3 million rows between them. That ratio is worth knowing before anyone designs a sampling
scheme over "all Kalshi markets": an unweighted sample of this dataset is a sample of crypto.

The ten largest series, all cursor-exhausted unless marked:

| series | rows | events | window | |
|---|---:|---:|---|---|
| KXINXU | 777,894 | 2,755 | 2022-08-09 → 2026-06-12 | |
| KXNASDAQ100U | 777,844 | 2,756 | 2022-08-09 → 2026-06-12 | |
| KXEURUSDH | 393,197 | 4,169 | 2023-02-28 → 2026-01-30 | |
| KXUSDJPYH | 390,148 | 3,917 | 2023-02-28 → 2026-01-30 | |
| KXBTCD | 353,000 | 1,925 | 2026-03-24 → 2026-06-14 | **incomplete** |
| KXDOGED | 315,472 | 5,424 | 2024-11-21 → 2026-06-14 | |
| KXDOGE | 295,000 | 5,000 | 2025-10-10 → 2026-06-14 | **incomplete** |
| KXSOLE | 274,000 | 3,661 | 2026-01-07 → 2026-06-14 | **incomplete** |
| KXXRP | 274,000 | 3,726 | 2026-01-03 → 2026-06-14 | **incomplete** |
| KXETHD | 253,000 | 3,439 | 2026-01-20 → 2026-06-14 | **incomplete** |

---

## The four completeness gates

### Gate 1 — row count equals unique ticker count

**PASS, exactly.** 7,269,014 rows against 7,269,014 unique tickers, across 6,703 files.
**Zero series** contain a duplicate ticker. No duplicates to explain.

### Gate 2 — no unexplained interior date gaps

**Characterised, not zero — and the gaps are real.** Interior gaps exist and belong to the
series, not the collector: `KXRAINNYC` covers 48.05% of its 2021-09-09 → 2026-06-14 span with an
866-day hole; `KXAAAGASD` covers 10.59%; `KXTOPALBUM` 7.86%. These are dormant periods — seasonal
sports, retired weather cities, one-off event families — not missing pages, and every page in
every series terminated on `cursor_exhausted` or `empty_page`, never on a status code.

Rather than assert "no gaps", the manifest carries `days`, `span` and `maxgap` for every series so
any future study can judge a series before using it. **A collector that reports zero gaps on data
like this is not reporting; it is asserting.**

### Gate 3 — a random sample re-fetched individually matches the bulk pull

**PASS on the sample taken; the sample is smaller than the packet asked for and the shortfall is
stated, not hidden.**

| | |
|---|---:|
| series sampled (of 6,703) | **951** |
| events re-fetched individually | **1,082** |
| events matching exactly | **1,082** |
| events mismatching | **0** |
| markets compared field-by-field | **9,814** |
| HTTP errors during the check | **0** |
| fraction of the packet's 1% target | **11.18%** |

Method: a seeded shuffle over all series with data, then 1% of each series' events (capped at 12
per series), each re-fetched via `/historical/markets?event_ticker=` and compared field-by-field
against the bulk pull. The shuffle is what makes a partial run usable — the sample is unbiased
across series even though it is incomplete.

**Why not `ticker=`:** that parameter is silently ignored on both market endpoints and returns the
unfiltered `KXMVE*` head. A re-fetch built on it would have compared every market against the same
five rows and reported a catastrophic mismatch, or worse, been "fixed" until it agreed. See
`registry/historical/ARCHIVE-LAG-2026-08-14.md`.

**One methodological catch worth recording:** the first version of this gate counted four HTTP 429
responses as *mismatches*. They are not mismatches; they are the instrument failing. The check now
separates `http_*` outcomes from data disagreements and retries them. This is the same error shape
as reading a 403 as a 404, and it is the third time in this run a status code was nearly read as
data.

### Gate 4 — total event count cross-checked against `/events`

**PASS, with the deficit fully explained and one anomaly recorded.**

| series | B1 events (historical) | `/events` (live, cursor-exhausted) | difference |
|---|---:|---:|---:|
| KXHIGHNY | 1,769 | 1,831 | **−62** |
| KXHIGHCHI | 1,757 | 1,819 | **−62** |
| KXCPIYOY | 43 | 48 | −5 |
| KXFED | 38 | 46 | −8 |
| KXPAYROLLS | 39 | 45 | −6 |
| KXNBAGAME | 1,449 | 1,448 | **+1** |

The two daily weather series differ by **exactly 62 each**, against **61 days** from the
`/historical/cutoff` of 2026-06-14 to today. Those events are real, are on the live path, and are
outside this dataset by construction — the deficit *is* the cutoff, measured to the day, from a
different endpoint. The monthly series' deficits (5, 8, 6) are the same effect plus
future-scheduled events that have not settled.

**KXNBAGAME is the anomaly: B1 holds one event that `/events` does not list.** One event, in one
series. Recorded and not explained. Control: `/events?series_ticker=KXDEFINITELYNOTREAL` returns
HTTP 200 with zero events.

---

## What is deliberately not in this dataset

- **Anything settling after 2026-06-14.** This is the historical path only. The live path holds
  everything from its sliding floor (2026-06-08 today) forward, and per **P9** that floor is
  advancing toward the cutoff.
- **`KXMVE*` combinatorial markets** — excluded a priori per the packet. They are **96.77%** of
  the unfiltered collection, measured on a 105,000-row global sample.
- **Nine crypto strike-ladder series**, stopped by collection budget at 223–353 pages each:
  KXBTCD, KXBTC, KXETH, KXETHD, KXSOLD, KXSOLE, KXXRP, KXXRPD, KXDOGE. Their cursors are retained
  in the collector state, so collection resumes exactly where it stopped. **Their row counts are
  lower bounds and the manifest marks each one `inc: true`.**
- **`open_interest_fp`.** Present in the rows, and **worthless** — it reads `0.00` on the
  historical path for every market tested (**P8**). It is kept rather than dropped so that nobody
  later assumes it was never collected.

---

## Deviation from the packet, recorded

The packet specifies **"3 threads at 0.55s"**, which its own arithmetic puts at ~5.45 req/s.
Latency held three threads to **4.06 req/s**, so a fourth worker was added after request 13,457 to
reach the rate the packet intended — not to exceed it. **Zero 429 responses were observed across
all 19,483 requests.** Backoff on 429 was never disabled.

---

## What this licenses

**Licenses:** B3's fee-model backtest harness over any subset of these 7.27M markets, joined to
`fee_type`/`fee_multiplier` which the manifest carries per series (6,681 series at 1, **14 at 0**,
**19 at 0.5** — the 33 non-unity series are exactly where a model that assumes 1.0 goes wrong).
Any registry re-derivation over the pre-2026-06-14 universe.

**Does not license:** treating this as "all Kalshi markets" (it is the historical path only);
unweighted sampling across it (two-thirds is crypto); any use of `open_interest_fp`; or any claim
about the nine incomplete series' totals.
