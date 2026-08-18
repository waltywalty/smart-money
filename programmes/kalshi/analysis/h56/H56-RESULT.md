# H56 — The hurdle, re-measured on a clean data path

**2026-08-12. Pre-registration sealed 07:49Z, sha256 `433b4a1e…`, before any outcome was joined to any price.**

---

## The result

```
mean P&L per event   −4.39¢    95% CI [−5.20, −3.67]    n = 346 events
prior estimate       −4.03¢    95% CI [−7.40, −0.70]    n =  41 events
```

**VERDICT: HURDLE CONFIRMED.**

The point estimate barely moved. The interval is **4.4× tighter** — 1.53¢ wide against 6.70¢.

This is the outcome I wanted least to be interesting and most to be true. The project's central
number was measured through a fetch layer now known to fabricate quotes, drop rows silently, and
invent midpoints for empty books. It would have been reasonable to expect it to fall apart. It
didn't. **The old number was right, and it was right by luck of a kind — the layer was lying, but
not in a direction that moved this particular estimate.**

Every verdict in the registry that was retroactively priced out by the hurdle stays priced out.

## Sample

| | |
|---|---|
| Settled markets discovered | 7,542 across 21 real series |
| Independent events available | 1,763 |
| Sampled | 377 events / 3,688 markets — capped at 30 events per series, spaced evenly across each series' time range |
| Quotes fetched | 3,688, **0 fetch failures**, 408 rate-limit rejections all successfully retried |
| No candle at the T−24h lead | 1,679 markets (46%) |
| Qualifying markets | 1,973 |
| **Events in the primary statistic** | **346** |

Machine-generated combinatorial series (`KXMVE*`) were excluded *a priori* in the pre-registration —
they flood the settled list (2,000 of the first 2,000 rows) and carry no independent flow.

## Robustness — all four pre-declared checks, reported whether flattering or not

**R1 — equal-weight by market instead of event:** −6.69¢ [−8.28, −5.08], n=1,973.
Worse, and expected to be: rungs of one ladder aren't independent, and per-market weighting
over-counts deep ladders.

**R2 — the H54 selection check.** Restricted to the 320 events where *every* rung had a quote at
the lead: **−4.17¢ [−4.95, −3.48]**. Barely moves. The candle-availability selection that destroyed
H54 — where a missing tail quote meant the outcome was already obvious — **does not touch this
result.** This was the check most likely to kill it and it passed cleanly.

**R3 — leave-one-series-out:** range **−4.57¢ to −3.54¢** across all 19 series. Sign stable
everywhere. The most influential single series is `KXRAIN`; removing it moves the estimate to
−3.54¢, still comfortably negative.

**R4 — concentration:** the largest single event is **3.9%** of total P&L. For contrast, the H54
false positive had its top event at 13.9% and its top three at 41.3%. Nothing here is driven by a
handful of events.

## What the 4.39¢ is made of *(post-hoc diagnostic — not pre-registered)*

```
gross edge before fees      −2.84¢   [−3.66, −2.12]
fee paid                    −1.55¢   [−1.58, −1.52]
                            ───────
total                       −4.39¢

quoted spread at entry       2.99¢ mean, 1.30¢ median
residual after half-spread  −1.34¢
```

So the cost splits roughly into thirds: **~1.5¢ of crossing the spread, ~1.55¢ of fee, and ~1.34¢
of the ask sitting above fair value beyond the half-spread.** That last third is the part that
isn't a mechanical transaction cost, and it is the only part any strategy could in principle attack.

The cheapest series to cross in are the liquid sports and weather ladders at **−2.50¢**. That is the
floor. Nothing in 21 series is positive.

## A false positive caught inside this study

The calibration table by ask bucket looked spectacular at first pass:

| ask | market-level realised vs implied |
|---|---|
| 70–79¢ | 43.8% vs 73.5% — **−29.7pp** |
| 80–89¢ | 58.6% vs 85.2% — **−26.6pp** |
| 90–99¢ | 75.9% vs 95.6% — **−19.7pp** |

Read naively that is a screaming short signal on expensive contracts. It is not.

Counting the **independent events** behind each bucket instead of the markets:

- 70–79¢: 89 markets → **41 events**, of which **62 of the 89 markets are `KXRAIN`**
- 80–89¢: 29 markets → **19 events**, 13 `KXRAIN` and 8 `KXPAYROLLS`
- 90–99¢: 54 markets → **26 events**, 41 `KXRAIN`

Re-computed at the event level the gaps shrink hard — 70–79¢ goes from 43.8% to **60.1%** realised.
The dramatic version of this table is one series wearing a disguise. `KXRAIN` was already the worst
line in the per-series breakdown at −16.94¢; it is not an independent discovery that it also looks
mispriced at high asks.

The low buckets, which carry real event counts (240, 168, 149 events), tell the sober version:
−2.2pp, −4.2pp, −2.9pp. The ask is modestly above fair everywhere. That is the finding.

## Consequences

1. **The hurdle stands at −4.39¢ [−5.20, −3.67].** It supersedes −4.03¢. Every future idea clears
   this or it isn't an idea.
2. **No verdict needs re-opening.** The expensive branch named in the pre-registration did not fire.
3. **H55 (buying near-certainties at 0.93–0.98) is not supported.** The 90–99¢ bucket realises 77.1%
   at the event level against 95.6% implied. But 41 of its 54 markets are `KXRAIN`, so this is
   evidence *against* H55, not a clean kill. Recorded as unsupported pending a pre-registered test
   on a `KXRAIN`-free sample.
4. **New hypothesis H57, untested:** `KXRAIN` contracts quoted above ~70¢ may be systematically
   overpriced. 41 events, discovered by post-hoc slicing, in the single worst-performing series.
   This is a hypothesis and nothing more. It needs its own pre-registration and a fresh disjoint
   sample before it is worth an hour of anyone's time.

## Reproducing this

Everything ran against raw HTTP from a browser VM — no summarising layer anywhere in the path.

- `PREREG.md` — the sealed pre-registration
- `grab.py` — collector (paginates settled markets, fetches the T−24h candle per market)
- `analyse.py` — implements the pre-registration exactly, fixed seed `20260812`
- `events.csv` — the 346 event-level observations behind the headline number

Cross-endpoint integrity was verified before collection: list quotes vs order book agreed exactly on
15 of 18 liquid markets, the other three being empty-book convention and one 1¢ tick on a BTC
market between sequential calls.
