# Phase 4 — the hurdle as a surface, not a line. Pre-registration.

**Sealed 2026-08-17, before any depth datum has been read.**

Following the precedent set by `registry/h64-preregistration.md`: this document must be complete,
hashed and committed **in its own commit before any data is pulled**. Until then it pre-registers
nothing. Phase 1's collector reads `result` fields, so this seal precedes Phase 1, not merely
Phase 4.

---

## Disclosure of what has already been seen

Stated first, because a pre-registration written after the data is not one.

**Seen, and it motivates this study:**

- T2.1: H56's estimator charges `math.ceil(0.07·p·(1−p)·100)` per contract with no `contracts`
  term. The hurdle reads **−4.39¢ at 1 contract, −3.90¢ at 10, −3.86¢ at 100, −3.85¢ continuous.**
  A hundredfold size increase buys **0.53¢**, about 12%.
- H60: the hurdle is a function of horizon — −3.81¢ at 24h against −1.94¢ at ten minutes.
- A1: shard health correlates with exchange activity, r = −0.631.
- B2: the target population is 44.9% healthy / 31.1% degraded / 15.7% no-shard.
- A4 / T3.2: bracketability runs 0.00% to 99.69% across shards; the method for placing snapshot
  rows is established.

**Not seen, and this study will be the first to look:**

- Any resting-size figure from `archive.pmxt.dev` for any market in the target window.
- Any spread-versus-size relationship on Kalshi at any horizon.
- Any hurdle figure at any order size other than the four above, which are fee-only.

**The motivating observation cannot also be evidence.** T2.1's fee curve is what suggested that the
hurdle has a size axis. It is therefore excluded from the verdict: the fee arm is treated as a
known input, not as a result of this study.

---

## The claim

**The hurdle is a surface over (order size, horizon), and every figure this registry has ever
quoted is a single point on it, sampled along one axis.**

The two components pull opposite ways:

- **Fee cost falls with size** as the whole-cent ceiling amortises. Steep below ~10 contracts, flat
  above. **Bounded at 0.53¢ across the entire axis** — measured, not assumed.
- **Spread cost rises with size** as the order eats down the book. Flat while resting depth covers
  you, then steep. **Unbounded above in markets this thin.**

If both hold there is a minimum somewhere between, and no measurement in this registry has looked
for it.

## The prediction, with its justification, written before any depth data is examined

**The surface worsens monotonically in size, or has a shallow minimum in the 1–10 contract range,
and is negative everywhere.**

Justification: the fee arm is worth **at most 0.53¢ in total** and is nearly exhausted by 10
contracts (0.49¢ of the 0.53¢ is bought going from 1 to 10). Beyond that the fee curve is flat to
three decimal places, so any further movement in the surface is spread. Book impact in markets
where H10 measured a **median size at bid of five contracts** is not bounded by anything small.
A term bounded at 0.53¢ cannot dominate a term with no ceiling.

**This is a prediction, not a hedge.** If the surface has a minimum at 100 contracts, or is
positive anywhere, the prediction is wrong and that must be recorded as such.

---

## Instrument, fixed now

**Depth source:** `archive.pmxt.dev` hourly Kalshi orderbook parquet, `orderbook_delta` and
`orderbook_snapshot` rows. **The exchange clock is `timestamp`.** `timestamp_received` is a
write-batch stamp and is never used as an event clock; snapshot rows are placed by joining to the
delta rows sharing their `timestamp_received` and taking the min/max `timestamp` of that batch as
a bracket, per `ARCHIVE-LAG-2026-08-14.md`.

**Shard admission, fixed now:** a shard is admitted only if it contains delta rows **and** its
bracketable fraction is **≥ 80%**. Bracket width must be carried into the analysis, not discarded.
Shards are classified individually and **never selected by date** — degradation is intermittent
(`2026-06-08T18` at 4.13% sits between two healthy days).

**Fee source:** `analysis/fees/fee_model.py`, `regime='documented'`, with `rate` a visible
parameter because A1's base-rate gap is not closed. `fee_multiplier` joined per series from
`/series/{ticker}`, and **reported under both bounds (1.0 and today's observed value)** per T2.2's
standing constraint, because the endpoint returns today's multiplier and applying it to a 2021
market is an anachronism that runs in the false-positive direction.

**Horizon is held fixed at T−10m.** One axis moves at a time. H59 varied venue, frequency and
instrument together, found nothing, and wrongly triggered a downgrade of H50.

**Size grid, fixed now:** 1, 2, 5, 10, 25, 50, 100, 250, 500 contracts. Nine points, chosen to
resolve the 1–10 range where the prediction places any minimum.

## Unit of observation

**The EVENT.** Rungs of one ladder resolve together. Event-level bootstrap, 10,000 resamples,
fixed seed declared in the analysis script before it runs. Rung-level figures are reported
alongside and are never the headline — in H64 the two differed in sign.

## Bar

- **Minimum 150 independent events per size point**, or that point reads *could not establish* and
  is left out of the surface rather than plotted thin.
- A minimum in the surface is **called** only if the size points either side of it differ from it
  by more than their own interval half-widths. Otherwise the surface is reported as flat.
- **Leave-one-series-out is mandatory** on every point that is called, and its range is reported.

---

## Reported alongside, always

1. **Depth per family, with that family's health composition beside it.** Never a pooled figure
   alone. The sevenfold spread in degraded share across families — KXATPSETWINNER 7%, KXCS2MAP 51%
   — means a pooled number is **weighted by collector health rather than by anything about the
   market**. Every family row carries: n events, depth statistic, and its healthy /
   intermediate / degraded / no-shard split.
2. **Bracket width distribution** for every snapshot-derived figure.
3. **The fraction of the target population excluded** by the 80% admission rule, and by the archive
   ending at 2026-06-11T03.
4. **Series composition of every size point**, per false positive #7.
5. **A price without size is not a price** — depth is reported in contracts, and the notional it
   represents, beside every spread figure.
6. **Both fee-multiplier bounds**, as above.

---

## What each outcome means, written before looking

| outcome | meaning | what happens |
|---|---|---|
| **Monotonically worse in size, negative throughout** | Prediction confirmed. The size axis is closed; the hurdle is a horizon story only. | Record and stop. |
| **A minimum in the 1–10 range, still negative** | Prediction confirmed in shape. | Report the location, **note explicitly that it is not an edge**, record the surface as mapped. |
| **A minimum at large size, or anywhere positive** | **Prediction wrong.** | **Do not report without** (a) leave-one-series-out, (b) a depth-source replication, and (c) an explicit check that A1's quiet-hour restriction is not producing it. A positive result here would arrive through the one channel A1 has shown to be selected. |
| **Fewer than 150 events at a size point** | Instrument failure at that point. | *Could not establish* for that point. Not a null. |

**Finding a minimum is not finding an edge.** A surface can have an optimum and be negative at
every point on it. That is the prior from **fifty-six registry entries, three confirmed, none
tradeable**. This sentence is here so that a minimum cannot later be reported as a discovery.

## What would make me abandon it before starting

- Fewer than 150 events survive the 80% shard-admission rule in **any** of the 1, 10 and 100
  columns. Without those three the surface has no shape worth plotting.
- The bracket-width p99 on admitted shards exceeds **60 s**, at which point a T−10m entry cannot be
  located within its own horizon.
- Depth cannot be reconstructed from `orderbook_delta` at all — i.e. the book cannot be replayed to
  a given `timestamp`. This has **not** been demonstrated yet and is the single largest untested
  assumption in this document.

## Scope, fixed now so it cannot be widened later

Kalshi only. T−10m only. `close_time` 2026-06-07 → 2026-06-11 only. The five series families
named in B2 plus any others reaching 150 events. **No result from this study may be stated as a
property of the exchange**, for the reason quoted verbatim below.

---

## A1, quoted verbatim, as required

From `registry/historical/A1-SHARD-SELECTION-2026-08-17.md`:

> **Verdict: outcome 2 of the three written down in advance** — *"Degraded shards are the busy ones
> — depth is measurable only on quiet hours. That is a legitimate finding but it is a scope limit,
> and no depth figure may then be stated as a property of the exchange."*

> **Selecting healthy shards selects quiet hours.** A depth study run on healthy shards measures a
> book that is roughly **1.5 to 1.8 times less actively traded** than the hours it excludes.

> Depth, spread and competition are precisely the quantities that differ most between quiet and busy
> markets, and they differ in the direction that flatters a strategy: quiet hours have thinner
> resting size but also less competition for it. **A depth figure from healthy shards would
> understate how hard it is to get filled when it matters.**

With the measured association: bracketable % against trades/sec, **pearson −0.631, spearman
−0.461, leave-one-out [−0.698, −0.594]**, n = 15 hours; degraded tier **1.45×** at the ≥80%
threshold and **1.80×** at ≥50%.

## B2, quoted verbatim, as required

From `registry/historical/B2-TARGET-TIER-2026-08-17.md`:

> **Verdict: outcome 1 of the three written down in advance, with a qualification that matters.**
> Target rungs do **not** concentrate in degraded shards — but the surviving half is not a random
> subset either, because A1 already showed healthy hours are the quiet ones. **About 45% of the
> target population is measurable at good coverage, and it is systematically the quieter 45%.**

> **On its own, B2 is permissive.** The target population is not concentrated in the degraded tier;
> roughly half of it sits in shards good enough to measure. Depth is not lost for the population of
> interest.
>
> **Composed with A1, it is narrower than that.** […] **B2 shows the population is reachable; A1
> shows the reachable part is systematically the quiet part.** Both must be quoted, and quoting only
> B2 would be the more flattering half.

With the measured split: **HEALTHY 44.9%, INTERMEDIATE 8.3%, DEGRADED 31.1%, no shard exists
15.7%** of the target population; and by family, degraded share **KXATPSETWINNER 7%,
KXATPCHALLENGERMATCH 33%, KXCS2GAME 37%, KXBNB15M 43%, KXCS2MAP 51%.**

And B2's own named way of being wrong, carried here rather than left behind:

> **No ask filter was applied.** […] If qualifying rungs cluster differently in time than their
> series as a whole — plausible, since near-certainty arrives late in a match — the tier mix would
> shift. **That is the most likely way this result is wrong**, and it points toward *more*
> degradation, since matches resolve into peak activity.

---

## The sentence that goes on every figure this study produces

> This is a property of quiet hours on Kalshi in June 2026, measured on the 44.9% of the target
> population whose entry hour fell in a shard with ≥80% bracketable coverage. It is not a property
> of the exchange.

---

**Sealed sha256 (of this file up to but excluding this line): `44668cf75a08c4cfc5560f7bc4c96de2abbe1e3e1fa0c075de3065693a598fbc`**

Recompute with: `sed -n "1,$(wc -l < phase4-preregistration.md)p" phase4-preregistration.md | head -c 11665 | sha256sum`
