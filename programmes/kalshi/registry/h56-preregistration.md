# H56 pre-registration - re-measure THE HURDLE on the clean data path

Written BEFORE any outcome was inspected. Sealed by sha256 below.

sha256: 433b4a1ec4d52f8e5531351dce4e18a5824a0411abb970e5fd7d34cfcffc90a3
sealed: 2026-08-12T07:49Z, before any settled outcome was joined to any price

## Why
The project's central number - buying at the ask loses 4.03c per event,
95% CI [-7.4, -0.7], n=41 events - was measured through a fetch layer
now known to fabricate quotes, drop rows silently, and invent midpoints
for empty books. Every verdict that cites the hurdle inherits that doubt.
Raw HTTP is now available. Re-measure it.

## Rule (fixed in advance)
- Universe: SETTLED markets from named real series only. Excluded a priori:
  KXMVESPORTSMULTIGAMEEXTENDED, KXMVECROSSCATEGORY and any KXMVE* -
  machine-generated combinatorial markets with no independent flow.
- Entry: buy YES at the ask, from the 60-min candle whose end_period_ts is
  the last one at or before T-24h from close_time. Require the candle to be
  within 3600s of the lead. yes_ask.close_dollars is the entry price.
- Require yes_ask strictly between 0.00 and 1.00. A 0 or 100 ask is not a
  tradeable quote.
- Exit: settlement. result=='yes' -> 100c, else 0c.
- Fee: Kalshi taker, ceil(0.07 * p * (1-p) * 100) cents, p = ask in dollars.
- P&L per market, cents = (100 if yes else 0) - ask_cents - fee_cents

## Unit of observation
THE EVENT, not the market. Rungs of one ladder resolve together and are not
independent. Each event contributes ONE observation = the mean P&L of its
qualifying rungs. This is the rule that turned a 12-market 'finding' into
2 real observations once before.

## Sample size fixed in advance
Minimum 150 independent events. Below that, report 'could not establish'
rather than a verdict. Target 300+.

## Primary statistic
Mean P&L per event, with a 95% percentile interval from 10,000 event-level
bootstrap resamples.

## What each outcome means - decided NOW
- Interval entirely below 0  -> hurdle confirmed. Record the new point
  estimate; it supersedes -4.03c and every idea must clear it.
- Interval spans 0           -> the -4.03c hurdle was NOT established.
  A dozen verdicts that were retroactively priced out by it must be
  re-opened. This is the outcome that costs the most and I am naming it
  in advance so it cannot be argued away later.
- Interval entirely above 0  -> buying at the ask pays. Extraordinary;
  would require an independent replication on a disjoint series set
  before anything is built on it.

## Pre-declared robustness checks (all reported, not just the flattering ones)
1. Equal-weight by market instead of by event.
2. Restricted to events where EVERY rung had a candle at the lead
   (the H54 candle-availability selection).
3. Leave-one-series-out: recompute dropping each series in turn.
4. Concentration: largest single event's share of total P&L.

## Abandon conditions
- Fewer than 150 events qualify -> 'could not establish', no verdict.
- Any cross-endpoint disagreement above 1c on a spot check of 20 markets
  -> stop, the data path is not clean after all.

---

## Sample actually drawn (recorded before outcomes were joined)
- 7,542 settled markets across 21 real series, 1,763 independent events
- Sampled to 377 events / 3,688 markets, capped at 30 events per series,
  spaced evenly across each series' available time range so the sample is
  not concentrated in one market regime.
- 377 events is 9x the n=41 the original hurdle rested on.
