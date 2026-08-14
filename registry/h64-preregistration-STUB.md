# H64 — near-certainties at a one-hour lead. Pre-registration STUB.

**STUB, not sealed.** Written 2026-08-13 from a coverage check only. No quote and no outcome has
been fetched. This document must be completed, hashed and committed *before* any data is pulled;
until then it pre-registers nothing.

ID assumes H63 lands first — its addendum is written but not yet merged. Renumber if that changes.

## Why this is not H55 again

H55 asked whether buying at ask 0.93–0.98 at a **24-hour** lead pays, because the Kalshi fee
`0.07·p·(1−p)` is minimised at the extremes. It returned *could not establish*, and the reason was
structural rather than statistical: of 1,523 non-KXRAIN rungs carrying a quote at T-24h, **exactly
one** sat in the 93–98¢ band. The fee arithmetic was correct and irrelevant. Contracts are not
priced at 93–98¢ a day out; by the time one is that certain it is close to settlement.

H55's own `revive_if` names the successor: *re-tested at a shorter lead where the band is populated,
a different hypothesis needing its own pre-registration, with H7/H9's capital-lockup arithmetic
applied.* This is that hypothesis, and it is separate — different horizon, different universe,
different cost structure.

## The claim

**H64: at a one-hour lead the 93–98¢ band is populated, and buying it at the ask returns less than
zero after fees — the same hurdle H56 measured at T-24h and H60 measured at T-10m, not an exception
to it.**

Stated in the direction that costs the most to be wrong about. H60 established the hurdle *falls*
with horizon (−3.81¢ at 24h → −1.94¢ at 10m). If it keeps falling and crosses zero somewhere in the
extreme-price band, that is a real finding. The prior, from every one of 45 kills, is that it does not.

## Instrument

- **Quotes:** `archive.pmxt.dev` hourly Kalshi orderbook Parquet, CC BY 4.0. Verified coverage
  2026-05-14 → 2026-06-11T03:00 UTC. Fetch with a ranged `GET` and an explicit User-Agent — `HEAD`
  on that host returns 200 for keys that do not exist, and a bare urllib UA is blocked. Include an
  impossible key as a control on every run.
- **Outcomes:** Kalshi `?status=settled` only. Never `/events?with_nested_markets=true`, never the
  single-market endpoint — both serve stale results for settled markets (H39).
- **Never** the archive's final pre-expiry quote as an outcome proxy. That is H39's grave.

## The window, and why this expires

Quotes exist 2026-05-14 → 06-11. Kalshi outcomes reach back only to 2026-06-07. The usable
intersection is **2026-06-07 → 2026-06-11, five days, 233 measured independent events** (lower
bound, from 80 of 1,624 series). Kalshi's retention floor advances about one day per day, so the
intersection empties on or about **2026-08-17**. The archive stopped updating on 2026-06-11 and
should not be assumed to resume.

If the window closes before this is run, H64 cannot be run at all from public data, and the
question becomes an argument for continuous self-collection rather than an experiment.

## Method

1. Fix the entry rule before looking: **at the last hourly snapshot at or before T-1h from
   `close_time`, buy YES at the ask where the ask is in [0.93, 0.98].** One observation per rung.
2. Aggregate to the **EVENT**, never the market. Ladder rungs resolve together; this rule has killed
   more false positives in this repo than everything else combined.
3. Net the real fee: `ceil(fee_multiplier · 0.07 · p · (1−p) · 100)` cents. Read
   `fee_multiplier` per series — it is 1 on 12,907 series, 0.5 on 19, 0 on 14. Never assume 1.0.
4. Apply **H7/H9's capital-lockup arithmetic**, as H55's `revive_if` requires: a contract bought at
   97¢ ties up 97¢ to earn 3¢, and the return must be stated per unit of capital per unit of time,
   not per contract.
5. Report **obtainability separately from statistical validity**: re-price the entry one and two
   snapshots later and report what could have been transacted at, not what was observed. H61
   replicated out-of-sample to 0.03¢ and was still worth nothing.
6. Event-level bootstrap, 10,000 resamples. Leave-one-market-out **and leave-one-series-out**, both
   reported as ranges.
7. Report the series composition of every bucket, unprompted.

## Bar

- **≥ 150 independent events** carrying at least one rung in the band at T-1h. Below that, report
  *could not establish* and stop — do not widen the band to reach the number.
- The result survives leave-one-series-out. Five consecutive calendar days will be concentrated;
  if one series carries the finding, there is no finding. This is false positive #7's exact shape.
- Depth beside every price. A price without size is not a price, and this project has paid twice.

## What each outcome means, written down in advance

- **Negative and consistent with H56/H60** — the expected result. The hurdle holds at the extremes;
  H55's line closes for good and the fee-minimisation idea is finished at every horizon.
- **Negative but materially smaller than −1.94¢** — the hurdle keeps falling into the extreme band.
  Interesting, still not a trade, and it becomes an argument about horizon rather than about price.
- **Positive** — extraordinary, and the first thing to suspect is the five-day window and the series
  mix, not the market. Do not report it without leave-one-series-out and a same-day replication on
  a different slice of the window.
- **Fewer than 150 events, or the band empty even at T-1h** — *could not establish*, and H55's
  structural finding extends to the shorter lead. That is a real answer and should be recorded as one.

## What would make me abandon it before starting

- The overlap window has closed (on or after ~2026-08-17).
- The archive's Parquet schema turns out not to carry per-market bid **and** ask with a usable
  timestamp — unverified as of this stub; the files were located and sized but not opened, because
  the Kernel VM has no parquet reader and no package installer.
- Settlement for the window cannot be joined to the archive's market identifiers.

## Scope, stated now so it cannot be widened later

Kalshi only. A five-day window in June 2026. A one-hour lead. Nothing here will license a claim
about the exchange in general, about other venues, or about any other horizon.
