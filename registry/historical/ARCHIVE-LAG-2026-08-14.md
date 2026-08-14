# A4 — `archive.pmxt.dev` receipt lag: what `timestamp_received` measures, and when it can be trusted

**Date of measurement:** 2026-08-14 (UTC)
**Packet:** coworkpacket3autonomous, Phase A, task A4
**Instrument:** Kernel VM. Files fetched by `curl` with explicit User-Agent
`smart-money-research/1.0`; object-store existence probed by **ranged GET** (`Range: bytes=0-0`),
never `HEAD`; an impossible control key on every probe. Parquet read locally with DuckDB 1.5.5
under a 350 MB memory cap. Row counts computed in code, never self-reported.

**Sample:** five hourly shards spanning the archive's life — `2026-05-15T00`, `2026-06-01T12`,
`2026-06-10T12`, `2026-06-10T13`, `2026-06-11T03` — totalling **51,247,338 rows**.

---

## What would overturn this

1. **A sixth file that is healthy but batched differently.** The bracketing recipe below assumes
   `timestamp_received` is a write-batch stamp shared by neighbouring delta and snapshot rows.
   Five files agree. A file where snapshots are written in their own batches would break it — and
   one already does (`2026-06-11T03`, below).
2. **Evidence that `timestamp` is not the exchange clock.** The cross-check here is structural,
   not documentary: quarter-hour market tickers encode their own close time and `timestamp` lands
   on those boundaries to the second. A counterexample series would overturn it.
3. **The lag being a market property rather than a clock property.** Measured per market it is
   not — but only within two hours of one day.

---

## The headline

**Do not use `timestamp_received` as an event clock. Ever.** It is the archiver's *write-batch*
stamp, and it is degenerate in exactly the way that matters: in a healthy hour **98.4% of
consecutive rows for the same market carry the identical value**. It has no resolution within a
market at all.

**Use `timestamp`.** It is the exchange clock, it has millisecond resolution, and it is **100%
populated on `orderbook_delta` rows**.

**The problem is `orderbook_snapshot` rows, where `timestamp` is 100% null.** For those, the
receipt lag is the whole question — and the answer is that it is **bounded to about a second when
the archiver is healthy, and unbounded when it is not**. It must be measured per file. It is not a
constant of the archive; it is a **health indicator**.

---

## The two clocks

| column | `orderbook_delta` | `orderbook_snapshot` |
|---|---|---|
| `timestamp` (exchange) | **0.000% null** (7,527,002 / 7,527,002 in `2026-06-10T12`) | **100.000% null** (3,629,771 / 3,629,771) |
| `timestamp_received` (archiver) | populated | populated |

This is why `timestamp_received` was ever reached for: on snapshot rows it is the only clock
present. The prior note in this project recorded that fact correctly and stopped there.

---

## Lag, per file — it is bimodal, and the mode is the archiver's health

`lag = timestamp_received − timestamp`, over delta rows only (the only rows where both exist).

| file | rows | deltas | snapshots | exchange span covered | lag min | lag p50 | lag max |
|---|---:|---:|---:|---|---:|---:|---:|
| `2026-05-15T00` | 20,197,265 | 18,515,214 | 1,682,051 | 23:59:58 → 00:59:59 (**60.0 min**) | 0.1 s | **0.4 s** | 9.4 s |
| `2026-06-01T12` | 11,839,385 | 11,807,343 | 32,042 | 11:59:59 → 12:59:59 (**60.0 min**) | 0.1 s | **0.4 s** | 5.5 s |
| `2026-06-10T12` | 11,156,773 | 7,527,002 | 3,629,771 | 11:51:54 → 12:25:44 (**33.8 min**) | 474.1 s | **1,056.7 s** | 2,055.9 s |
| `2026-06-10T13` | 7,111,062 | 4,474,384 | 2,636,678 | 12:25:44 → 13:23:38 (57.9 min) | 306.9 s | **2,271.7 s** | 2,429.7 s |
| `2026-06-11T03` | 942,853 | **0** | 942,853 | — **no exchange clock in the file at all** | — | — | — |

Three regimes, not one:

1. **Healthy** (May 15, June 1). Median lag **0.4 s**, worst case under 10 s, and the file covers
   a full 60 minutes of exchange time. Here `timestamp_received` is a usable clock to about a
   second, and the distinction between the two clocks barely matters.
2. **Degraded** (June 10). Median lag **17.6 min** rising to **37.9 min** an hour later; the T12
   file covers only **33.8 minutes** of exchange time inside a 60-minute receipt window. The
   archiver is replaying a backlog at roughly **0.55× real time** and falling further behind by
   about 26 s of lag per minute of wall clock. Snapshot share jumps from 0.3% to 32.5% — a
   reconnect storm re-requesting full books.
3. **Dead** (June 11, the last file). **Zero delta rows.** 942,853 snapshot rows, every one with a
   null `timestamp`. **This file has no exchange clock and no way to recover one from inside it.**

### The consequence that will silently corrupt a study

**The filename is not the file's content window.** `kalshi_orderbook_2026-06-10T12.parquet` is
sharded by *receipt* hour and contains exchange events from **11:51:54 to 12:25:44** — eight
minutes before its nominal start and thirty-four minutes short of its nominal end. Selecting a
time window by filename, which is the obvious thing to do with an hourly-sharded archive, silently
returns the wrong 34 minutes. In the healthy files the filename *is* accurate to the second, which
is worse: the error appears only in the files where it matters.

---

## Within a market: the receipt clock has no resolution, the exchange clock has milliseconds

Five busiest markets in the healthy `2026-06-01T12` shard; gaps between consecutive delta rows for
the same market, in seconds.

| market | rows | exchange p50 | p90 | p99 | max | receipt p50 | receipt max |
|---|---:|---:|---:|---:|---:|---:|---:|
| KXINTLFRIENDLYGAME-26JUN01PAKBAN-PAK | 345,477 | 0.0012 | 0.0195 | 0.0777 | 20.60 | **0.0** | 20.50 |
| KXBTCD-26JUN0109-T72099.99 | 197,650 | 0.0012 | 0.0434 | 0.2587 | 3.10 | **0.0** | 3.00 |
| KXINTLFRIENDLYGAME-26JUN01PAKBAN-TIE | 182,580 | 0.0043 | 0.0316 | 0.2094 | 20.19 | **0.0** | 20.50 |
| KXBTCD-26JUN0109-T72199.99 | 156,679 | 0.0014 | 0.0514 | 0.3419 | 7.86 | **0.0** | 7.50 |
| KXBTCD-26JUN0109-T71999.99 | 140,465 | 0.0018 | 0.0586 | 0.3648 | 6.08 | **0.0** | 6.00 |

On the busiest market, **98.37% of consecutive rows share the identical `timestamp_received`**,
against 38.82% sharing the identical exchange `timestamp`. The receipt clock is quantised to the
write batch; the exchange clock resolves to about a millisecond.

**The lag is a property of the clock, not of the market.** Across 3,728 markets with ≥100 delta
rows in the degraded hour, the per-market *median* lag runs 487 s → 2,034 s — but the *within-market*
range averages 1,436 s, essentially the same spread. Markets are not lagging differently from each
other; they are all riding one global skew that drifts through the file. That is precisely why the
fix below works.

---

## Can it be bounded? Yes — for 95.9% of snapshot rows, to about a second

The archiver writes in batches. In `2026-06-10T12` there are **7,377 distinct
`timestamp_received` values** covering 11,156,773 rows — 1,512 rows per batch on average, capped
at exactly **5,000**, which is the flush threshold. **4,294 batches contain both delta and
snapshot rows.**

Within one batch the exchange timestamps span:

| statistic | span of `timestamp` inside one batch |
|---|---:|
| median | **0.128 s** |
| mean | 1.018 s |
| p99 | 5.94 s |
| max | 9.32 s |

So the recipe is:

> **To place a snapshot row on the exchange timeline, join it to the delta rows sharing its
> `timestamp_received`, and take their `min(timestamp)` and `max(timestamp)` as the bracket.**

| | rows | share |
|---|---:|---:|
| snapshot rows in `2026-06-10T12` | 3,629,771 | 100% |
| **bracketable** (their batch contains ≥1 delta row) | **3,480,688** | **95.893%** |
| not bracketable (snapshot-only batch) | 149,083 | 4.107% |

Bracket width for the bracketable rows: **1.166 s mean, 5.974 s at p99.**

**This holds even in the degraded hour.** The 35-minute lag is a *shift*, and a shift is
recoverable; what would not be recoverable is jitter, and there is almost none inside a batch.
The 4.1% in snapshot-only batches must either be interpolated between neighbouring batches or
dropped — and dropping them is a selection decision, because snapshot-only batches are
disproportionately the reconnect storms.

**`2026-06-11T03` cannot be bracketed at all** — zero delta rows means zero anchors. That file's
942,853 snapshot rows are unplaceable in exchange time by any method internal to the archive.

---

## Cross-check — against the exchange's own schedule, not a second call to the archive

The claim "`timestamp` is the exchange clock" needs a source outside the archive. Kalshi's
quarter-hour crypto series supply one for free: **the ticker encodes the close time.**
`KXBTC15M-26JUN10**0815**-15` closes at 08:15 America/New_York = 12:15:00 UTC.

From the degraded `2026-06-10T12` shard, where the two clocks are ~20 minutes apart and therefore
discriminating:

| market | archive `timestamp` range (UTC) | archive `timestamp_received` range (UTC) |
|---|---|---|
| KXBTC15M-26JUN10**0800**-00 | 11:51:54 → **12:00:00** | 12:00:00 → 12:13:16 |
| KXBTC15M-26JUN10**0815**-15 | **12:00:00** → **12:15:00** | 12:13:17 → 12:37:57 |
| KXBTC15M-26JUN10**0830**-30 | **12:15:00** → 12:25:44 | 12:37:56 → 12:59:59 |
| KXETH15M-26JUN10**0800**-00 | 11:51:54 → **12:00:01** | 12:00:00 → 12:13:17 |
| KXETH15M-26JUN10**0815**-15 | **12:00:00** → **12:15:00** | 12:13:16 → 12:37:57 |
| KXETH15M-26JUN10**0830**-30 | **12:15:00** → 12:25:44 | 12:37:57 → 12:59:59 |

`timestamp` lands on the exact quarter-hour boundary **six times, on two independent asset
families, to the second**. `timestamp_received` lands nowhere near one. The exchange clock is
`timestamp`. The two truncated ends (11:51:54 and 12:25:44) are the file's own boundaries, not the
markets'.

---

## An instrument failure caught by the control, and it would have fabricated this section

The first attempt at the cross-check above asked Kalshi for each market's `close_time` via
`GET /historical/markets?ticker={ticker}`. All six markets came back with the identical
`close_time = 2026-06-14T23:45:00Z`, which is nonsense for six markets fifteen minutes apart — and
it was only visible as nonsense because the impossible control key was run in the same pass:

```
/historical/markets?ticker=KX-IMPOSSIBLE-CONTROL-19990101  ->  HTTP 200, 5 markets returned
```

**The `ticker` parameter is not a filter on `/historical/markets` — or on live `/markets`.** It is
silently ignored, and the endpoint returns the unfiltered head of the collection, which begins
with `KXMVESPORTSMULTIGAMEEXTENDED-…` closing at `2026-06-14T23:45:00Z`. That is exactly the value
that came back six times.

Tested against the control on both paths:

| parameter | `/historical/markets` | live `/markets` |
|---|---|---|
| `series_ticker` | control returns 0 rows — **honoured** | control returns 0 rows — **honoured** |
| `event_ticker` | control returns 0 rows — **honoured** | control returns 0 rows — **honoured** |
| `ticker` | control returns **5 rows** — **IGNORED** | control returns **5 rows** — **IGNORED** |

Without the control, this document would have contained a confident, specific, entirely fabricated
cross-check. A2's measurements are unaffected — they used `series_ticker` and `event_ticker`, both
honoured. Written into `docs/INFRA.md`.

---

## Measured vs assumed

**Measured:**

- `timestamp` null rates by `event_type`: 0% on deltas, 100% on snapshots.
- Lag distributions on five shards spanning 2026-05-15 → 2026-06-11 (51,247,338 rows).
- Exchange-time span of each shard against its filename hour.
- Batch structure: 7,377 batches, 5,000-row flush cap, 4,294 mixed batches.
- Intra-batch exchange-time span: p50 0.128 s, p99 5.94 s, max 9.32 s.
- Bracketable share of snapshot rows: 95.893%.
- Within-market consecutive-row gaps on the five busiest markets of a healthy shard.
- Per-market lag dispersion over 3,728 markets in the degraded shard.
- Ticker-boundary alignment on six quarter-hour markets, two asset families.
- Object store: `2026-06-11T04` → 404, control `1999-01-01T00` → 404, real keys → 206.
- `ticker=` is ignored on both `/markets` and `/historical/markets`.

**Assumed, or not established:**

- That five shards characterise ~700 hours of archive. They were chosen to span the range, not at
  random, and two of the five are consecutive hours of one degraded day.
- That the 0.55× replay rate on 2026-06-10 is a backlog rather than something else. The shape fits;
  the cause is not established.
- That snapshot-only batches are reconnect storms. Plausible from the snapshot-share jump; not
  demonstrated.
- **Why** the archive stopped after `2026-06-11T03`. Unknown. The degradation on 2026-06-10 and the
  delta-free final file are consistent with a feed failure, but that is a story fitted to two data
  points.
- That any of this is stable if the archive resumes. It has been stale for two months.

---

## What this licenses, and what it does not

**Licenses:** using the archive as a quote source at **millisecond** resolution on `timestamp`,
for delta rows, in any healthy hour; and using snapshot rows placed by batch-bracketing to within
~1 s for 95.9% of them, provided the bracket width is carried into the analysis rather than
discarded.

**Does not license:** selecting a time window by filename; using `timestamp_received` as an event
clock; using any row from `2026-06-11T03`; or treating the 4.1% unbracketable snapshots as a
random sample of snapshots.

**Bearing on B2 (depth study).** The instrument is sound at the resolution B2 would need, but only
over the healthy period, and the usable quote window still ends at 2026-06-11 while it ends in
practice on 2026-06-10 once the degraded hours are excluded. That interacts with P9's closing
overlap band and belongs in GATE 1, not here.
