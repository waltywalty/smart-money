# Check 1 — Is shard ABSENCE a selection variable, the way shard DEGRADATION is?

**Date:** 2026-08-17. Carried over from packet 4's truncated message, outstanding since.
**Verdict: NO — and the reason is that absence and degradation are not the same kind of variable.**

A1 established that *degraded* shards are the busy hours (pearson −0.631, LOO [−0.698, −0.594],
degraded hours trading 1.45–1.80× harder). B2 then reported that **15.7% of the target population
has no shard at all.** The open question was whether that 15.7% is selected the same way. If it
were, missing data would be a second selection channel on top of the first.

It is not. Absence here is a **censoring boundary in calendar time**, not an intermittent property
of an hour, and it carries no activity signal once the diurnal cycle is controlled.

---

## Instrument

Same two-source separation A1 used, deliberately: health/presence from the archive, activity from
Kalshi, so the two cannot share a failure mode.

- **Presence:** `GET https://r2kalshi.pmxt.dev/kalshi_orderbook_<YYYY-MM-DD>T<HH>.parquet` with
  `Range: bytes=0-0`. **Ranged GET, never HEAD** — `docs/INFRA.md` records that HEAD returns 200
  for files that do not exist. Impossible control `kalshi_orderbook_1999-01-01T00.parquet` in the
  same pass: **HTTP 404.** So a 404 here means absent, and a 206 means present.
- **Activity:** `GET /historical/trades?min_ts=&max_ts=&limit=1000`, newest-first, capped at 1000;
  rate = `1000 / (newest − oldest)`. Impossible control, a 1999 window: **HTTP 200 with 0 trades.**
- **Span:** every hour from `2026-06-05T00` to `2026-06-11T23` UTC — 168 hours, covering H64's
  window (`close_time` 2026-06-07 → 06-11) with margin.
- 168 of 168 hours returned HTTP 200. **166 of 168 hit the 1000-trade cap**, so almost every rate
  is a real rate rather than a truncated count.

---

## 1. The absence is terminal, not intermittent — and that decides most of the question

| | hours |
|---|---:|
| present (HTTP 206) | **148** |
| absent (HTTP 404) | **20** |
| **interior gaps** (absent hours between the first and last present hour) | **0** |
| leading gaps | 0 |

The absent hours are exactly `2026-06-11T04` … `2026-06-11T23` — **one contiguous block, every
hour after the archive's last publication at 2026-06-11T03.**

This is the structural difference from degradation. A1 found `06-08T12` degraded while sitting
*between two healthy days* — degradation is intermittent, it recurs, and each degraded hour is a
separate event that can be correlated with that hour's activity. Absence, in this window, happens
**once**. The collector stopped and never restarted.

---

## 2. Raw comparison on A1's three measures

| measure | present (n=148) | absent (n=20) | ratio |
|---|---:|---:|---:|
| **trades/sec** | 45.60 | 42.74 | **0.94×** |
| distinct tickers | 259.59 | 268.65 | 1.03× |
| distinct series | 78.34 | 78.90 | 1.01× |

Degradation ran **1.45–1.80× harder**. Absence runs **0.94×** — if anything marginally *quieter*,
and in the opposite direction. Tickers and series do not move at all.

---

## 3. The confound, stated before the statistic

Because the absent block is contiguous clock time, it is **not a random sample of hours**. It
covers hours-of-day 04–23 and omits 00–03 entirely, and Kalshi activity has a strong diurnal
cycle: mean trades/sec by hour-of-day ranges from **23.7 to 82.1**, a 3.5× swing. A raw
present-vs-absent comparison is therefore partly a comparison of *times of day*.

So each absent hour is compared against the same hour-of-day on the present days.

---

## 4. Diurnal-matched comparison

| sample | mean difference | matched baseline | relative |
|---|---:|---:|---:|
| all 20 absent hours | **+1.50 trades/sec** | 41.24 | **+3.6%** |
| 18 hours, excluding the two-hour outage in §6 | **+4.55 trades/sec** | 42.94 | **+10.6%** |

Either way this is small, and it is *positive* — the absent block, if anything, is slightly busier
than its matched baseline, which is the same sign as A1's effect but roughly a fifth to a
fifteenth of its size, and it does not survive §5.

---

## 5. The correlation, and why it is not the answer

| absence vs | pearson | leave-one-HOUR-out |
|---|---:|---|
| trades/sec | **−0.041** | [−0.076, −0.009] |
| distinct tickers | +0.034 | [−0.002, +0.086] |
| distinct series | +0.011 | [−0.014, +0.094] |

Excluding the outage hours: **+0.026**. Against A1's **−0.631, LOO [−0.698, −0.594]**, this is
nothing.

But the leave-one-hour-out interval is misleading, and this project's own rule says so: **the unit
of observation is the event, not the row.** There is exactly **one** absence event. Leave-one-day-out
makes that visible:

| day dropped | pearson |
|---|---:|
| 2026-06-05 | −0.047 |
| 2026-06-06 | −0.044 |
| 2026-06-07 | −0.052 |
| 2026-06-08 | −0.067 |
| 2026-06-09 | −0.022 |
| 2026-06-10 | −0.037 |
| **2026-06-11** | **undefined — absence has no variance left** |

Dropping the single day that contains the boundary destroys the variable entirely. **n = 1, not
n = 20.** No correlation can be estimated from one event however many hours it spans, and the tight
leave-one-hour-out band above is an artefact of treating 20 correlated hours as 20 observations.

---

## 6. Found while doing this: a two-hour hole in Kalshi's own trade history

| hour (UTC) | trades returned | note |
|---|---:|---|
| 2026-06-11T06 | 1,000 (cap) | full hour, last trade 06:59:59.97 |
| **2026-06-11T07** | **13** | all 13 inside the first **0.26 seconds** of the hour, then nothing |
| **2026-06-11T08** | **0** | empty |
| 2026-06-11T09 | 1,000 (cap) | full hour |

Controls: `2026-06-10T07` and `2026-06-09T08` both return the full 1,000. Re-probed directly on a
second pass and reproduced exactly. The window boundaries are clean, so this is not a windowing
artefact — **it is a genuine ~2-hour gap in Kalshi's settled trade history on 2026-06-11.**

It matters beyond this check: a collector measuring activity would read those hours as *quiet*,
not as *missing*. That is the same shape as every other error this project has logged — an absence
produced by a layer other than the market, wearing the costume of a real measurement. Parked.

Note also that the outage sits **inside** the absent-shard block, which is suggestive but cannot be
followed up: the archive had already stopped four hours earlier, so there is no shard to compare
against and no way to tell whether the two events share a cause.

---

## What this changes

- **B2's 15.7% is a censoring boundary, not a selection channel.** It should be described as *"the
  part of the target population that falls after the archive stopped"* rather than as missing data
  that might be missing for a reason. Nothing in A1 or B2 needs re-deriving — **no verdict, figure
  or `revive_if` is changed by this check.**
- **The selection worry stands exactly where A1 put it and no further.** Depth is measurable only on
  quiet hours because *degraded* shards are the busy ones. Absence adds no second bias.
- **What is still not answered:** whether absence *elsewhere in the archive* is intermittent. This
  check covers 168 hours around H64's window and finds zero interior gaps. The full advertised
  coverage runs 2026-05-14 → 2026-06-11T03; the earlier three weeks were not probed. If any
  interior gap exists there, it would be a different variable from the one measured here and would
  need its own check.
