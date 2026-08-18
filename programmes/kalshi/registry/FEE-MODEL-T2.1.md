# T2.1 — What fee model does the hurdle use? The one-contract charge, not the continuous form.

**Date:** 2026-08-17. **Packet:** coworkpacket4, Phase 2, task T2.1, started under Addendum A's
corrected Gate 0 fallback (*any "not" means Phase 1 does not start; do Phase 2 **or** Phase 3*).
**Nothing is changed.** No verdict, no figure, no `revive_if`. H56's published number stands.

---

## The answer, in one line

`analysis/h56/analyse.py` line 31:

```python
fee = math.ceil(0.07 * (a / 100) * (1 - a / 100) * 100)     # Kalshi taker
pnl = (100 if r['res'] == 'yes' else 0) - a - fee
```

`a` is the ask in cents. **There is no `contracts` term anywhere in the file.** That `math.ceil`
to a whole cent, applied per contract, is exactly `effective_per_contract(1, p, regime='inherited')`
in `analysis/fees/fee_model.py`.

**H56's hurdle is the ONE-CONTRACT hurdle.** It is the *most expensive* point on the size axis,
not the cheapest.

---

## This contradicts what both packet 4 and C1 assumed

Packet 4, page 5:

> *"every cost model in the registry uses the size-free continuous form. That is the
> hundred-contract price. So the registry has been pricing at the cheapest reachable fee, and the
> true cost at retail size is higher, not lower."*

And `registry/FEE-CEILING-AUDIT.md` (C1), which I wrote:

> *"every cost model in this project is a **per-contract continuous function**, `0.07·p·(1−p)`,
> which has no size parameter at all."*

**Both are false for H56**, the one entry where it matters most. C1 did flag it as undetermined —
*"in scope by consequence … not determined here, because it requires reading H56's estimator
rather than its registry entry"* — and parked it as **P11**. Reading the estimator is what this
task did, and the answer is the opposite of the assumed one.

**C1's conclusion survives; its stated reason does not.** No entry killed at one contract revives
at a hundred — still true. But not *because the models are size-free*. H56's is size-**fixed**, at
the smallest and dearest size. That belongs on the **right for the wrong reason** list.

---

## What the hurdle reads at each order size

Recomputed from `analysis/h56/events.csv` (346 events, committed). The published statistic is
reproduced first, as a control on the reconstruction:

    REPRODUCED  -4.39c [-5.21, -3.66]     published  -4.39c [-5.20, -3.67]

Agreement to 0.01 cent on the mean and on both bounds; the residual is bootstrap draw order.
The reconstruction is sound.

| order size | mean P&L | 95% CI | mean fee | delta vs 1 | **hurdle** |
|---|---|---|---|---|---|
| **1 (as published)** | -4.64c | [-5.46, -3.91] | 1.800c | - | **-4.39c** |
| 10 | -4.15c | [-4.98, -3.42] | 1.314c | **+0.49c** | **-3.90c** |
| 100 | -4.11c | [-4.93, -3.37] | 1.266c | **+0.53c** | **-3.86c** |
| 1,000 | -4.10c | [-4.93, -3.37] | 1.262c | +0.54c | -3.85c |
| continuous, no ceiling | -4.10c | [-4.93, -3.37] | 1.262c | +0.54c | -3.85c |

**Method note, and it matters.** `rows.json` is not committed, so the per-*rung* asks are gone;
`events.csv` carries per-*event* means. The fee is convex in p, so applying it at the mean ask
overstates the level — visible as 1.800c against the 1.550c H56 actually charged per rung.
**The absolute levels carry that bias; the delta column does not**, because the same approximation
sits on both sides of the difference. The **hurdle** column is the published -4.39c with the
measured delta applied, which is the honest way to state it.

---

## Three things this establishes

**1. Packet 4's closing note has the direction backwards for H56.** It predicted *"the true retail
hurdle is higher than the -3.81c/-1.94c that every kill calibrates against."* For H56, **-4.39c
already is the retail figure.** The size-infinite hurdle is **-3.85c** — 0.54c *cheaper*. Trading
at size makes the bar easier to clear, not harder.

**2. The size effect is small, and the reason is the sample.** H56's asks run **mean 28.6c, median
18.7c, range 1-90c**. The whole-cent ceiling only bites where the continuous fee falls below 1c —
roughly p below 0.015 or above 0.985. At the median ask the continuous fee is already **1.06c**, so
the ceiling is barely active. **This is a hurdle measured in the middle of the book, where size
hardly matters.** It says nothing about the extremes, where C1 measured ratios of 4.76x and 14.29x.

**3. The verdict is unchanged at every size.** Every interval above excludes zero. **HURDLE
CONFIRMED at 1 contract and at 1,000.** Nothing calibrated against -4.39c moves: the nearest miss
in the registry is H64 at +0.5135c with an interval half-width of 1.8c, and 0.54c does not rescue
it.

---

## What this does NOT establish

- **Nothing about the spread half of the cost.** The -4.39c decomposes with a quoted spread of
  2.99c mean / 1.30c median at entry, and spread cost **rises** with size as an order eats the
  book. This task moved only the fee component. **The two pull opposite ways, which is exactly
  Phase 4's premise, and Phase 4 remains unrun.**
- **Nothing about the extremes.** A hurdle measured at a median ask of 18.7c does not extend to
  the 93-98c band where H55 and H64 live.
- **Nothing about `fee_multiplier`.** Every figure here assumes 1.0. **T2.2** is the task that asks
  whether that is safe on historical data, and it is not yet done.

---

## For `PARKED.md`

**P11 is answered, not resolved.** *"What size does H56's hurdle assume?"* now has an answer —
**one contract** — and the sensitivity is measured at **+0.54c from 1 to infinity**. What stays
parked is the decision that follows: whether the registry calibrates against the retail hurdle
(-4.39c), the at-size hurdle (-3.86c at 100), or both. **That is a choice about how this registry
states its bar, and it is Walton's.**

Recommendation, for the record: **report both, as a pair, always.** A single scalar hurdle is what
produced this confusion in the first place, and Phase 4's premise is that the hurdle is a surface
rather than a line.
