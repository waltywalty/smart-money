# T1 - The kill condition for family 2, written before the literature

Programme: insider (documented public-record anomalies). Packet 7, task T1.
Written **2026-08-24, before a single paper on insider trading was read or searched for**
in this session. Committed alone. **Not to be edited** - amendments only, dated, with the
original preserved verbatim.

The only inputs to the numbers below are this project's own documents (`CLAUDE.md`,
`ROADMAP.md`, `docs/METHOD.md`) and Walton's stated circumstances: a UK-resident retail
account trading US equities, with relocation pending. **No insider-trading result, effect
size, sample period or paper informed any threshold here.** If it had, the thresholds would
be fitted to the answer and this document would be worthless.

**The gate is not lifted by anything below.** `ROADMAP.md` family 2 reads: *relocation
complete, and family 1 has produced a verdict.* Neither has happened. A pass here means
"worth building to test", never "the effect is there", and never "build it".

---

## 0. Scope of the test

**The condition binds per strand, not on the family.** Strands differ in event rate and
effect size and must be evaluated separately - opportunistic-versus-routine, cluster buys,
first-time buyers, role weighting, small-cap concentration, filing-lag informativeness.

**The family survives only if at least one strand survives on its own numbers.** The family
dies if the best-performing strand fails. Averaging strands is prohibited: a strong strand
with four events a year and a weak one with four hundred do not combine into a business.

---

## 1. The residual effect size that makes this not worth building

All figures are **net of the full T4 hurdle** - commission, spread, borrow, FX both ways,
and capital lockup - at the horizon the strand's own literature claims, and at the size
Walton would actually enter.

**Two tests, both must pass.**

### 1a. Per-event floor: **25 basis points**

> **KILL if the per-event residual, net of the central hurdle estimate, is below 25 bps at
> the strand's claimed horizon.**

**Why 25 and not zero.** The floor is set by the precision of the cost estimate, not by
appetite. T4 will produce a *range* for spread on sub-$2bn US names, because published
market-quality data reports distributions rather than a number. **An effect smaller than
the width of its own cost estimate cannot be distinguished from zero by any backtest this
project could build**, and a strategy whose edge is inside its own measurement error is not
an edge. 25 bps is the smallest figure that stays meaningful if the hurdle's central
estimate proves wrong by a typical small-cap half-spread.

### 1b. Pessimistic-hurdle sign test

> **KILL if the residual is negative at the pessimistic end of the T4 hurdle range**, even
> where it clears 25 bps at the central estimate.

A residual whose *sign* depends on which end of the cost range is used has not been
established as positive. This is the arithmetic that killed the Kalshi programme, applied
before the build rather than after.

### 1c. Annualised, on locked capital: **300 bps over passive**

Per-event returns are not comparable across horizons. Convert:

```
annualised net residual = per-event net residual x (365 / horizon_days)
```

assuming serial redeployment of the same capital and no overlap.

> **KILL if the annualised net residual on continuously-deployed capital fails to exceed a
> passive US equity index return by 300 bps.**

**Why 300.** Below that, the honest comparison is a low-cost index fund, which requires no
EDGAR pipeline, no classifier, no maintenance, and carries no concentration or
short-squeeze risk. 300 bps is the compensation demanded for taking single-name
concentration, a build measured in weeks, and ongoing operational exposure - not a
prediction of what is achievable.

---

## 2. The event rate that makes it uninvestable regardless of effect size

> **KILL if the strand produces fewer than 50 investable events per year.**

"Investable" means: passes the strand's own classifier, in a name Walton could actually
trade from a UK retail account, at a size where the hurdle in T4 applies rather than a
worse one.

**Why 50.** It is this project's existing bar - B3 pre-registered 50 events before a median
may be read - and it is the point below which a year of live running cannot distinguish the
strategy from noise. A strategy a solo operator cannot evaluate inside a year is one they
will either abandon on a drawdown or keep on faith. **An edge of 200 bps on four events a
year is not a programme**, and neither is one on forty.

---

## 3. Post-publication decay that settles it

> **KILL if post-publication re-estimation shows the effect has more than halved AND the
> re-estimated residual sits inside the T4 hurdle range.**

Both clauses. A halving that still leaves a residual clearing section 1 is a smaller edge,
not a dead one. A residual inside the hurdle is dead whether or not it halved.

### 3a. The vantage rule, pre-committed

**A paper is an instrument; its sample period is its vantage.** A result estimated on
1986-2007 is a measurement of that era, and this anomaly has been publicly documented for
long enough that its own publicity is a treatment applied to it.

> **A strand whose only evidence comes from samples closing more than ten years before
> today - 2016-08-24 or earlier - and for which no post-publication out-of-sample
> re-estimation exists, CANNOT support a "survives scoping" verdict.** Its ceiling is
> **could not establish**, however large the original effect.

This is not a kill. It is a refusal to treat old evidence as current evidence, and it is
stated now so that finding a large 2012 number later cannot become a reason to relax it.

---

## 4. What makes the answer "could not establish" rather than a kill

**Could not establish** is an instrument failure in the review. It is a statement about
what the literature reports, not about whether the anomaly exists. Any one of the following
forces it, per strand:

1. **The literature reports effect sizes without the horizon, the risk adjustment, or the
   sample size** needed to compute section 1. An effect quoted without its horizon cannot
   be netted against a hurdle.
2. **No post-publication re-estimation exists**, and the original sample closed more than
   ten years ago (section 3a).
3. **The hurdle's uncertainty range spans the effect size**, so the sign of the residual is
   indeterminate. This is neither a kill nor a survival and must not be reported as either.
4. **The strand's event rate is not reported anywhere** and cannot be derived from published
   figures without pulling filing data - which this packet is forbidden to do.
5. **The literature is split** on whether the effect exists, with no later work resolving
   it, and the disagreement is not attributable to sample or method.

### 4a. Search failure is not absence

> **If a required paper cannot be reached - paywalled, unavailable, or only summarised -
> the strand is "could not establish" on that item. It is never recorded as "no evidence
> found".** A summary of a paper is not the paper, and this project does not treat the
> inability to read a source as a measurement of what the source says.

---

## 5. What a survival requires, stated for symmetry

A pre-registration that only defines failure invites a pass by default.

**A strand survives scoping only if ALL of the following hold:**

1. Per-event residual **>= 25 bps** net of the central hurdle, at a stated horizon.
2. Residual **positive at the pessimistic hurdle**.
3. Annualised net residual **>= passive + 300 bps** on locked capital.
4. **>= 50 investable events per year**, from a published figure or one derivable from
   published figures.
5. **Post-publication out-of-sample re-estimation exists**, and the re-estimated effect
   still satisfies 1 through 3.
6. Every figure above traceable to a **named, dated source that was read rather than
   summarised**.

Missing any of 1-4 is a **kill**. Missing 5 or 6 is **could not establish**.

---

## 6. What this document does not do

- It does not open the programme. The gate is unchanged.
- It does not authorise a build, a collector, a pre-registration, or capital.
- It does not predict the outcome. The thresholds were set without reference to any insider
  trading result and may well kill a strand this project would have liked to keep.
- It does not permit a fourth outcome. Ambiguity is **could not establish**, said plainly.

---

## 7. Amendment discipline

This document is sealed on commit. Sections 1 through 5 may not be edited. If a threshold
is wrong, that is recorded as a dated amendment below stating what changed, why, and
**what was already known when the change was made** - because a threshold relaxed after
seeing the data is not a threshold.
