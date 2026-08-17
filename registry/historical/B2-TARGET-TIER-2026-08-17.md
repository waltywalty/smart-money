# Addendum B2 — Does the quiet-hour scope limit exclude the population of interest?

**Date:** 2026-08-17. **Packet:** coworkpacket4, Addendum B, task B2.
**Must be quoted in any Phase 4 pre-registration that uses archive depth.**

**Verdict: outcome 1 of the three written down in advance, with a qualification that matters.**
Target rungs do **not** concentrate in degraded shards — but the surviving half is not a random
subset either, because A1 already showed healthy hours are the quiet ones. **About 45% of the
target population is measurable at good coverage, and it is systematically the quieter 45%.**

---

## Instrument, and its limits stated first

H64's actual 254 rungs cannot be reconstructed: `rows.json` was never committed, and the
qualifying filter was `ask in [0.93, 0.98]` at T−10m, which needs per-market candlesticks.

**Proxy used:** all markets in H64's window (`close_time` 2026-06-07 → 06-11) from its **five
largest series by rung share** — KXATPCHALLENGERMATCH (20.1% of the 254), KXCS2MAP (14.2%),
KXCS2GAME (8.3%), KXATPSETWINNER (5.9%), KXBNB15M (5.5%). Together **53.8% of the target rungs**.
Each series paged to cursor exhaustion; control `series_ticker=KXDEFINITELYNOTREAL` → 200, 0 rows.

**1,704 markets, 119 distinct entry hours** (entry = `close_time − 10 min`).

Health for all 119 hours would be ~10 GB of parquet. Instead **14 hours were drawn
probability-proportional to rung count** from the 101 hours inside archive coverage, and each was
downloaded and measured directly. **This is a sample, not a census.**

---

## The measurement

| entry hour | rungs | bracketable % | tier |
|---|---|---|---|
| 2026-06-07T10 | 36 | 98.53 | HEALTHY |
| 2026-06-07T14 | 38 | 95.55 | HEALTHY |
| 2026-06-08T10 | 26 | 61.31 | INTERMEDIATE |
| 2026-06-08T16 | 34 | 5.83 | **DEGRADED** |
| 2026-06-08T19 | 26 | 20.35 | **DEGRADED** |
| 2026-06-09T04 | 4 | 38.07 | **DEGRADED** |
| 2026-06-09T12 | 22 | 99.69 | HEALTHY |
| 2026-06-09T14 | 24 | 99.35 | HEALTHY |
| 2026-06-09T15 | 28 | 99.07 | HEALTHY |
| 2026-06-09T21 | 4 | 65.80 | INTERMEDIATE |
| 2026-06-10T12 | 14 | 95.89 | HEALTHY |
| 2026-06-10T14 | 14 | 32.25 | **DEGRADED** |
| 2026-06-10T15 | 16 | 12.58 | **DEGRADED** |
| 2026-06-10T18 | 18 | 0.14 | **DEGRADED** |

Tiers: HEALTHY ≥ 80% bracketable, INTERMEDIATE 50–80%, DEGRADED < 50%.

| tier | hours | rungs | share of in-coverage | **share of full target population** |
|---|---|---|---|---|
| HEALTHY | 6 | 162 | 53.3% | **44.9%** |
| INTERMEDIATE | 2 | 30 | 9.9% | 8.3% |
| DEGRADED | 6 | 112 | 36.8% | **31.1%** |
| **no shard exists** | — | 267 | — | **15.7%** |

**15.7% of the target population has no shard at all** — its entry hour falls after the archive
stops at 2026-06-11T03. That is not a coverage question; those rungs are unreachable at any
quality.

## By series family, as Addendum B asked

| series | healthy | intermediate | degraded | total | degraded share |
|---|---|---|---|---|---|
| KXATPSETWINNER | 24 | 4 | 2 | 30 | **7%** |
| KXATPCHALLENGERMATCH | 64 | 10 | 36 | 110 | 33% |
| KXCS2GAME | 20 | 4 | 14 | 38 | 37% |
| KXBNB15M | 24 | 8 | 24 | 56 | 43% |
| KXCS2MAP | 30 | 4 | 36 | 70 | **51%** |

Families differ by a factor of seven. **Esports (KXCS2MAP) is half-degraded; tennis set-winners
are almost entirely healthy.** Any depth figure aggregated across families inherits whatever mix
the surviving shards happen to impose.

---

## What this means, composed with A1

**On its own, B2 is permissive.** The target population is not concentrated in the degraded tier;
roughly half of it sits in shards good enough to measure. Depth is not lost for the population of
interest.

**Composed with A1, it is narrower than that.** A1 measured that healthy hours are the quiet ones
— pearson −0.631, LOO [−0.698, −0.594], degraded hours trading 1.45–1.80x harder. So the 45% that
survives is **not a random 45%**. It is the half of the target population that traded in quieter
hours. **B2 shows the population is reachable; A1 shows the reachable part is systematically the
quiet part.** Both must be quoted, and quoting only B2 would be the more flattering half.

## Limits

- **14 hours, 304 of 1,704 proxy markets.** A sample, not a census. Tier shares carry sampling
  error of roughly ±10pp at this n.
- **The proxy is five series covering 53.8% of H64's rungs**, not the rungs themselves. The
  remaining 46.2% sits in 39 smaller series that were not enumerated.
- **No ask filter was applied.** The proxy is *all* markets in those series in the window, not just
  those quoting 93–98c at T−10m. If qualifying rungs cluster differently in time than their series
  as a whole — plausible, since near-certainty arrives late in a match — the tier mix would shift.
  **That is the most likely way this result is wrong**, and it points toward *more* degradation,
  since matches resolve into peak activity.

## For the Phase 4 pre-registration

Quote all three numbers: **44.9% healthy, 31.1% degraded, 15.7% no shard.** State that the
surviving fraction is the quiet fraction, per A1. State the by-family spread, since a
cross-family aggregate is not a property of any family. And state the ask-filter caveat as the
named way this could be wrong.
