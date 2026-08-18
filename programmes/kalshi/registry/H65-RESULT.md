# H65 - The hurdle as a surface over order size. Mapped, negative everywhere, axis closed.

**Date:** 2026-08-18. **Pre-registration:** `registry/phase4-preregistration.md`, sealed 2026-08-17
in its own commit at **`4775d76`**, sha256
`44668cf75a08c4cfc5560f7bc4c96de2abbe1e3e1fa0c075de3065693a598fbc`, before any depth datum was read.

**Verdict: CONFIRMED on branch one, by Walton's ruling of 2026-08-18.** The ruling set the terms
below; the draft of this entry stated the verdict without separating shape from magnitude, and that
separation is the substance of what changed.

### Shape - CONFIRMED

The hurdle has a size axis. It is **negative at every one of the nine size points**, the 1-10 region
is **flat**, it **worsens monotonically above 10 contracts**, and it is **spread-dominated**: the
measured span across the axis is **7.23c against a fee arm bounded at 0.53c**, so the spread arm is
**13.6x** the entire fee arm. That is branch one, and the pre-registration's justification for
predicting it - *"a term bounded at 0.53c cannot dominate a term with no ceiling"* - is confirmed by
the measurement rather than merely by its direction.

### Magnitude at small size - NOT SEPARATED FROM ZERO

**The shape is confirmed. The small-size numbers are not.** Two independent checks agree on where
the surface becomes distinguishable from zero, and it is not at the small sizes that matter most to
a retail-scale order:

| size | mean | 95% CI | CI vs zero | LOO-series | LOO-series vs zero |
|---|---:|---|---|---|---|
| 1 | -3.11c | [-7.76, +1.37] | **includes 0** | [-4.73, +0.60] | **crosses 0** |
| 2 | -2.98c | [-7.63, +1.57] | **includes 0** | [-4.59, +0.76] | **crosses 0** |
| 5 | -2.99c | [-7.61, +1.74] | **includes 0** | [-4.67, +0.80] | **crosses 0** |
| 10 | -3.24c | [-7.86, +1.29] | **includes 0** | [-5.05, +0.61] | **crosses 0** |
| 25 | -3.71c | [-8.38, +0.87] | **includes 0** | [-5.59, +0.18] | **crosses 0** |
| 50 | -4.55c | [-9.29, +0.13] | **includes 0** | [-6.53, -0.51] | excludes 0 |
| 100 | -5.89c | [-10.73, -1.11] | excludes 0 | [-8.15, -1.81] | excludes 0 |
| 250 | -8.40c | [-13.17, -3.56] | excludes 0 | [-10.64, -4.18] | excludes 0 |
| 500 | -10.20c | [-14.96, -5.44] | excludes 0 | [-12.61, -6.39] | excludes 0 |

**The bootstrap interval excludes zero only from 100 contracts up. Leave-one-series-out excludes it
only from 50 up.** Below that the point estimates are negative and consistent with the rest of the
registry, but **this study does not establish their magnitude** - it establishes that the surface
does not improve with size, and that it becomes decisively negative once size is large enough to eat
the book.

So: **do not quote -3.11c at one contract as a measured hurdle.** Quote the shape, and quote the
magnitude from 100 contracts upward. The small-size hurdle remains what H56/H60 measured by other
means; H65 neither confirms nor refines it.

> **Every figure in this document is a property of quiet hours on Kalshi in June 2026. It is not a
> property of the exchange.**

---

## The surface

Unit of observation: **the EVENT**. Event-level bootstrap, **10,000 resamples, seed 20260818**
declared in the analysis script before it ran. Fee regime `documented`, `fee_multiplier` 1.0.

| order size | events | mean P&L (c/contract) | 95% CI | leave-one-market-out | leave-one-series-out |
|---|---:|---:|---|---|---|
| 1 | 201 | **-3.11** | [-7.76, +1.37] | [-3.51, -2.67] | [-4.73, **+0.60**] |
| 2 | 201 | **-2.98** | [-7.63, +1.57] | [-3.38, -2.54] | [-4.59, **+0.76**] |
| 5 | 201 | **-2.99** | [-7.61, +1.74] | [-3.40, -2.54] | [-4.67, **+0.80**] |
| 10 | 201 | **-3.24** | [-7.86, +1.29] | [-3.65, -2.79] | [-5.05, **+0.61**] |
| 25 | 201 | **-3.71** | [-8.38, +0.87] | [-4.12, -3.26] | [-5.59, **+0.18**] |
| 50 | 201 | **-4.55** | [-9.29, +0.13] | [-4.95, -4.09] | [-6.53, -0.51] |
| 100 | 200 | **-5.89** | [-10.73, -1.11] | [-6.30, -5.44] | [-8.15, -1.81] |
| 250 | 200 | **-8.40** | [-13.17, -3.56] | [-8.82, -7.95] | [-10.64, -4.18] |
| 500 | 198 | **-10.20** | [-14.96, -5.44] | [-10.63, -9.77] | [-12.61, -6.39] |

**Negative at every size point. No confidence interval excludes zero on the positive side.**

## Which branch, in B1's own words

> **"The surface worsens monotonically in size, or has a shallow minimum in the 1-10 contract range,
> and is negative everywhere."**

The least-cost point is **2 contracts at -2.98c**. B1 fixed in advance when that may be called:

> *"A minimum in the surface is **called** only if the size points either side of it differ from it
> by more than their own interval half-widths. Otherwise the surface is reported as flat."*

| neighbour | mean | difference from the least-cost point | its own interval half-width | called? |
|---|---:|---:|---:|---|
| 1 contract | -3.11c | 0.13c | 4.56c | **no** |
| 5 contracts | -2.99c | 0.01c | 4.67c | **no** |

**The minimum is not called.** The surface is reported as **flat from 1 to 10 and monotonically
worse above it** - branch one of the four sealed outcomes:

> *"Monotonically worse in size, negative throughout. Prediction confirmed. The size axis is closed;
> the hurdle is a horizon story only. Record and stop."*

## The arithmetic B1 predicted in advance

B1 justified the prediction by noting the fee arm is **bounded at 0.53c across the entire 500x axis**
while book impact is unbounded above, and that *"a term bounded at 0.53c cannot dominate a term with
no ceiling."*

**Measured span across the same axis: 7.23c** - from -2.98c at the least-cost point to -10.20c at
500 contracts. The spread arm is **13.6 times** the entire fee arm. The justification is confirmed
by the measurement, not merely its direction.

## Depth beside every price

| order size | median average fill | median notional |
|---|---:|---:|
| 1 | 49.00c | $0.49 |
| 100 | 54.18c | $54 |
| 250 | 58.16c | $145 |
| 500 | 60.87c | $304 |

Resting depth at the best ask: **median 49 contracts**, p25 16, p75 144, mean 1,480 (one family
carries a long tail). Median total ladder depth 3,978 contracts. Median spread **3.00c**.

Buying 500 contracts moves the average fill **11.87c** above the single-contract price. That is the
whole finding in one number.

---

## Per family, with that family's health composition beside it

B1 required this and forbade a pooled figure alone, because *"a pooled number is weighted by
collector health rather than by anything about the market."* It was right to.

| family | events priced | mean P&L @1 | @100 | median depth at best | notional at best | admitted hrs / hrs needed | hrs past archive end |
|---|---:|---:|---:|---:|---:|---|---:|
| `KXATPCHALLENGERMATCH` | 36 | **+3.42c** | **+3.13c** | 151 | $48 | 17 / 63 | 9 |
| `KXATPSETWINNER` | 24 | -1.08c | -7.39c | 94 | $38 | 13 / 40 | 9 |
| `KXBNB15M` | 71 | -0.13c | -1.80c | 20 | $9 | 34 / 118 | 17 |
| `KXCS2GAME` | 23 | +0.20c | -3.99c | 72 | $20 | 13 / 52 | 11 |
| `KXCS2MAP` | 47 | **-15.26c** | **-19.19c** | 29 | $13 | 17 / 61 | 13 |

**The dispersion is larger than the effect.** The pooled surface is negative everywhere, but one
family reads **+3.42c at a single contract** and another **-15.26c** - an 18.7c spread across
families against a 7.23c spread across the whole size axis. This is why leave-one-series-out
**crosses zero at every size up to 25 contracts**: dropping `KXCS2MAP` alone turns the pooled figure
positive at small size.

### `KXATPCHALLENGERMATCH`: OBSERVED, NOT REPORTED - pending branch three

It reads **+3.42c at one contract and +3.13c at 100**, on 36 events. Walton's ruling records it as
**observed, not reported.** It is not a result, it is not a lead, and it does not enter any figure,
summary or downstream study in that character.

B1 fixed in advance what would be required before any positive result may be stated:

> *"Do not report without (a) leave-one-series-out, (b) a depth-source replication, and (c) an
> explicit check that A1's quiet-hour restriction is not producing it."*

| requirement | status |
|---|---|
| (a) leave-one-series-out | **done** - and it is what exposes the dispersion above |
| (b) depth-source replication | **not done** - `archive.pmxt.dev` is the only Kalshi book source that exists, and it stopped at `2026-06-11T03`. There is no second source to replicate against |
| (c) quiet-hour check | **not done, and it is the decisive one** |

On (c): **this entire study runs on admitted shards, and A1 established that admitted shards are the
quiet hours** - trading 1.45-1.80x less actively than the hours excluded, pearson -0.631, LOO
[-0.698, -0.594]. A1 also stated the direction of the resulting bias in advance: *"quiet hours have
thinner resting size but also less competition for it"*, so a depth figure from healthy shards
**understates how hard it is to get filled when it matters**. A positive family figure is therefore
arriving through precisely the channel already shown to be selected, in the direction that flatters
it. That is the expected artefact, not a surprise.

**Because (b) cannot currently be satisfied at all, this observation is not merely unreported - it
is unreportable with the data that exists.** It is recorded here so it is not rediscovered as new.

## Family dispersion exceeds both measured axes of the hurdle - a finding about the POOLED hurdle, not about H65

**Walton's ruling gives this its own line, and it is not a caveat on this study. It is a statement
about every pooled hurdle figure this registry has ever quoted.**

At one contract, on a single horizon, in a single week, the five families run:

| family | mean P&L @1 contract |
|---|---:|
| `KXATPCHALLENGERMATCH` | **+3.42c** |
| `KXCS2GAME` | +0.20c |
| `KXBNB15M` | -0.13c |
| `KXATPSETWINNER` | -1.08c |
| `KXCS2MAP` | **-15.26c** |

**Span: 18.68c.** Set that against the two axes the registry has spent two packets measuring:

| source of variation | measured span |
|---|---:|
| **family**, at one size and one horizon | **18.68c** |
| size, 1 to 500 contracts (H65) | 7.23c |
| horizon, 24h to 10m (H60) | 1.87c |
| **size and horizon combined** | **9.10c** |

**Which family is in the pool moves the hurdle more than twice as much as both measured axes
together (2.05x).** Every pooled hurdle figure in this registry - H56's -4.39c, H60's horizon curve,
this surface - is therefore **weighted by its family mix at least as much as by the variable it
names**. H56's own false positive #7 was this same shape one level down: a -29.7pp calibration gap
where 62 of 89 markets were one series.

**The operational consequence:** a hurdle quoted without its family composition is not a hurdle, in
the same way that a price without size is not a price. Any future cost figure in this project should
carry its composition beside it, and any comparison between two hurdle figures should first check
whether it is comparing families rather than the axis it claims to compare.

This is not a scope limit on H65. **It is a general property of the pooled hurdle that H65 happened
to be the study large enough to expose.**

## Series composition of every size point

Stable to within one percentage point across the whole grid, so the shape of the surface is not a
composition artefact:

| size | ATPCHALLENGER | ATPSETWINNER | BNB15M | CS2GAME | CS2MAP |
|---|---|---|---|---|---|
| 1 - 250 | 19% | 12% | 27% | 14% | 28% |
| 500 | 19% | 11% | 28% | 14% | 27% |

## Bracket width of the snapshot used

n=262 markets: **median 0.44s, p90 3.31s, p99 8.71s, max 42.63s.** Comfortably inside the 60s
abandonment threshold B1 set, at which *"a T-10m entry cannot be located within its own horizon."*

## What was excluded, and by what

| stage | markets | remaining | share of population |
|---|---:|---:|---:|
| target population (5 families, `close_time` 2026-06-07 -> 06-11) | 1,704 | 1,704 | 100% |
| entry hour after the archive ends at `2026-06-11T03` | -267 | 1,437 | 84.3% |
| shard fails the 80% bracketable admission rule | -806 | 631 | 37.0% |
| **no snapshot in the shard before T-10m** | **-340** | 291 | 17.1% |
| empty ask ladder at T-10m | -27 | 264 | 15.5% |
| `result` is `scalar` (not yes/no) | -2 | 262 | **15.4%** |

**The largest single loss is not the archive ending and not the admission rule - it is that 54% of
markets on admitted shards carry no snapshot before their entry instant.** That was not anticipated
in the pre-registration and is the sharpest limit on this study. **201 events of 1,086 survive.**

A methodological note, stated because it flatters nothing: deltas falling inside the chosen
snapshot's bracket are treated as already reflected in that snapshot, and replay begins at the
bracket's upper edge. With a median bracket of 0.44s the exposure is small, but it is an assumption
rather than a measurement.

## Fee multiplier, both bounds

B1 required reporting under both 1.0 and today's observed value, because applying today's multiplier
to a 2021 market is an anachronism running in the false-positive direction. **All five families
return `fee_multiplier: 1`, `fee_type: quadratic` today**, so the two bounds coincide and the
surface is identical under either. The anachronism risk does not bite for this population. It would
for `KXMLBGAME`, which carries 0.5.

## Scope limits, stated as scope limits

- **Quiet hours only.** Admitted shards are healthy shards, and A1 measured healthy hours trading
  **1.45-1.80x less actively** than the hours excluded, pearson **-0.631**, LOO [-0.698, -0.594].
  A depth figure from healthy shards **understates how hard it is to get filled when it matters**.
- **Five families, June 2026, T-10m, Kalshi.** One horizon, one venue, five products, five days.
- **Buying YES at the ask only.** Selling, resting, and the NO side are unmeasured.
- **15.4% of the target population survives.** The surviving set is selected on collector health,
  which A1 showed is not independent of market activity.

## `revive_if`

- A depth source covering **busy** hours appears, at which point the surface can be re-measured off
  the selected channel and the scope limit lifted rather than restated.
- Any positive family figure is to be revisited **only** under B1's full branch three - LOO-series,
  a second depth source, and an explicit quiet-hour check. Not before.
- The snapshot-coverage limit is addressed - a replay that carries the book across shard boundaries
  would recover much of the 54% lost to `no snapshot before T`.

## What this closes

The hurdle is now measured on **both** of its axes: horizon (H60, -3.81c at 24h to -1.94c at ten
minutes) and size (here, flat to 10 contracts then -10.20c by 500). **It is negative on every point
of both.** The size axis is closed. Nothing in the registry revives at a different order size, and
sizing up makes it strictly worse above 10 contracts.

**Finding a minimum is not finding an edge, and none was found.**
