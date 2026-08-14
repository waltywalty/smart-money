# H64 — near-certainties at a ten-minute lead. Result.

**2026-08-14. Pre-registration sealed `ba60eff4…` before any settlement was fetched.
Amendments 1–3, all written before any outcome was examined; current hash `bbf4cd3e…`.**

---

## Verdict: COULD NOT ESTABLISH

```
PRIMARY   T−10m, event-level, net of real fees
          +0.5135¢   95% bootstrap CI [−1.4469, +2.1816]   n = 245 events / 254 rungs
```

The 150-event bar was **cleared** — 245 events. This is not a sample-size failure. It is a null
with wide intervals, and two pre-registered robustness checks kill it outright.

### Leave-one-series-out crosses zero

```
without KXATPCHALLENGERMATCH   −0.2227   n=194
without KXCS2GAME              +0.2804   n=224
without KXCS2MAP               +0.9493   n=211
without KXBBCHARTPOSITIONALBUM +1.0963   n=242
                         RANGE  −0.2227 .. +1.0963
```

One series carrying **20.1%** of the rungs flips the sign. The pre-registration said in advance:
*"if one series carries the finding, there is no finding. This is false positive #7's shape."*

### The pre-committed split-half does not replicate

```
first half  06-08..06-09   +0.2660  [−2.3283, +2.4346]   n=159 events
second half 06-10..06-11   +0.9709  [−2.2465, +3.3023]   n= 86 events
```

Both span zero; neither constrains the other.

### And the unit of observation flips the sign

```
rung-level  mean  −0.9457   n=254 rungs
event-level mean  +0.5135   n=245 events    <- the pre-registered unit
```

Ladder rungs resolve together, so the event is the independent unit and **+0.5135 is the figure
that counts**. But reporting per-contract would have printed a *negative* number. Whoever chose
the unit after seeing the data could have had either sign — which is exactly why it was fixed
before.

---

## Two things this *does* establish

### 1. H55's structural finding is resolved — the band is populated at a short lead

```
H55  T−24h      1 of 1,523 rungs in band   = 0.07%
H64  T−10m    254 of 4,081 usable markets  = 6.22%      ~89× better populated
```

H55's `revive_if` pointed at the right place, and its own explanation — *"contracts are not priced
at 93–98¢ a day out; by the time one is that certain it is close to settlement"* — is confirmed
rather than merely plausible. The band exists at ten minutes. It does not pay.

### 2. The fee premise — H55's whole motivation — is defeated by rounding

H55 rested on `0.07·p·(1−p)` being minimised at the extremes. It is, in the continuous formula.
It is not what you are charged. **All 254 rungs paid exactly 1 cent.**

```
mean theoretical fee   0.2917¢     (0.07 · p · (1−p) · 100 at mean ask 0.9561)
mean charged fee       1.0000¢
ratio                  3.43×
```

Kalshi rounds the fee **up to whole cents on the order total**, so the analytic minimum is never
realised — the ceiling binds instead, and binds hardest exactly where the formula is smallest.
**The cheapness this idea was reaching for does not exist in practice.** That is a mechanism, not
a null, and it closes the line more firmly than the P&L does.

---

## Everything the pre-registration required

**Calibration.** 243 of 254 rungs settled YES = **95.67%**, against a mean entry ask of **0.9561**.
The market is well calibrated in this band. There is no mispricing to harvest — only a fee and a
spread.

**Series composition.** 44 series. `KXATPCHALLENGERMATCH` 20.1%, `KXCS2MAP` 14.2%, `KXCS2GAME`
8.3%, `KXATPSETWINNER` 5.9%, `KXBNB15M` 5.5%. Tennis and esports dominate; **nothing here
transfers to the macro markets** where H50, H62 and H63 live.

**Fee multipliers**, read per series and never assumed: 252 rungs at 1.0, 2 at 0.5.

**Return on capital.** −0.9890% over a ten-minute hold, rung-weighted. Deliberately not annualised
— a ten-minute holding period annualises to a number meaningless at any size, and this repo has
been misled by exactly that before (H7/H9).

**Obtainability, separately from statistical validity.**

```
T−10m   254 rungs   245 events   +0.5135  [−1.4469, +2.1816]
T− 5m   353 rungs   352 events   +0.9520  [−0.6918, +2.3026]
T− 1m   148 rungs   146 events   +2.0952  [+0.6199, +2.9692]
```

**The T−1m interval excludes zero and should not be believed.** It is below the 150-event bar, no
leave-one-series-out or split-half was run against it, and sixty seconds from close on tennis and
esports markets is where obtainability is least plausible. It appears because obtainability was
required to be reported, not because it is a finding.

**Staleness.** Mean 54.9s, median 32.0s; 325 observations excluded for exceeding the
pre-registered 600s cap.

---

## Limitations, stated rather than buried

**Depth was not observed, and the pre-registration required it.** Candlesticks carry volume, not
resting size, so *"what fraction of qualifying rungs had size at the ask"* could not be answered.
`archive.pmxt.dev` holds the book and would answer it. Until that runs, **every figure above
describes a quote, not a fill.**

**The usable sample is selected.** 4,081 of 13,832 markets were usable at T−10m; the rest were
excluded for no ask (5,018), no candle before the entry instant (3,088), no candles at all
(1,309), or staleness (325). A market with candles is a market that traded, so the exclusion runs
toward liquidity.

**T−1h and T−24h are unmeasured here** — candles were fetched only from `close − 1800s`. That is a
fetch-window limitation, not an observation. The band-population comparison uses H55's own T−24h
measurement.

---

## Instrument

Kalshi 1-minute candlesticks via `/historical/markets/{ticker}/candlesticks`, cross-checked
against the live path on six markets — identical candle counts on all six, two different endpoints
rather than a second call to the same one. Universe: 13,832 markets / 4,787 events / 245 series
with `close_time` in 2026-06-07 → 2026-06-11, `KXMVE*` excluded a priori.

## Status

- **H64: COULD NOT ESTABLISH.** +0.5135¢ [−1.4469, +2.1816] over 245 events — spans zero, one
  series of 44 flips the sign, and it does not replicate across halves of the window.
- **H55 stays could-not-establish, and its `revive_if` is discharged.** The shorter lead was
  tested, the band was populated, and there was nothing there. Its motivating premise is closed by
  the fee-rounding finding rather than by a P&L.
- **Nothing here is tradeable and nothing here contradicts the hurdle.** The one interval that
  excludes zero has the smallest sample, the weakest robustness, and the worst obtainability.

---

# Audit note — 2026-08-14 (packet 3, task C4)

**Appended, not edited. No figure, no verdict field and no `revive_if` above is changed.**

## 1. The verdict is two verdicts, and this project's own rule is that they be reported apart

The status section says COULD NOT ESTABLISH and, in the same breath, that this *"is not a
sample-size failure — it is a null with wide intervals."* Both are defensible. They answer
different questions, and `skills/empirical-claims/SKILL.md` requires statistical validity and
obtainability to be reported as separate gates.

**Gate 1 — quote level: does buying at the ask in [0.93, 0.98] at T−10m pay?**
**ANSWERED. Null.** `+0.5135¢`, 95% CI `[−1.4469, +2.1816]` over 245 events — spans zero;
leave-one-series-out runs `−0.2227 … +1.0963` and one series of 44 carrying 20.1% of rungs flips
the sign; the pre-committed split-half gives `+0.2660` against `+0.9709` with neither constraining
the other; and the rung-level mean is `−0.9457` against the event-level `+0.5135`. The 150-event
bar was cleared at 245. **This gate had enough data and returned nothing.**

**Gate 2 — fill level: what would it have returned?**
**COULD NOT ESTABLISH.** Depth was a *pre-registered requirement* and the instrument could not
supply it: candlesticks carry volume, not resting size, so "what fraction of qualifying rungs had
size at the ask" was never observed. Every figure above therefore describes **a quote, not a
fill**. This is an instrument failure, which SKILL.md holds is a different claim from a null.

Collapsing the two into one line makes the entry read as an underpowered study. It was not
underpowered. **It was fully powered on a question it could answer, and blind on a question it
pre-registered and could not.**

Since this result was written, A4 has characterised the instrument that would close Gate 2:
`archive.pmxt.dev` carries the resting book, its `timestamp` field is the exchange clock at
millisecond resolution, and snapshot rows can be placed to about a second
(`registry/historical/ARCHIVE-LAG-2026-08-14.md`). Its Kalshi coverage ends 2026-06-11 and this
study's window is 2026-06-07 → 2026-06-11 — they overlap. **Gate 2 is answerable.** Whether to
answer it is a decision, and decisions are parked in this run.

## 2. The fee reasoning above is wrong, and is size-conditional

The section headed *"The fee premise … is defeated by rounding"* states that **"All 254 rungs paid
exactly 1 cent"** because **"Kalshi rounds the fee up to whole cents on the order total."** Both
clauses are wrong, and they are wrong in two different ways:

- **Nothing was paid.** H64 was a paper study. The 1¢ was computed by this project's own code from
  the fee formula then in `docs/INFRA.md`. A property of the cost function was reported as a
  property of the exchange.
- **That is not how Kalshi rounds.** A1 (`registry/fees/A1-FEE-ROUNDING-2026-08-15.md`) reproduced
  all three of Kalshi's documented worked examples: the trade fee rounds **up to $0.0001 per
  fill**, and the whole-cent behaviour comes from a *separate* balance-precision rounding fee —
  $0.01 for a non-direct member — which a per-order accumulator partly rebates.

**The 1¢ figure is nevertheless right at one contract**, which is the size H64 never stated: A1's
schedule gives exactly 1.0000¢ per contract in this band for a non-direct member. At 100 contracts
it falls to about **0.33¢**. Substituting that moves the primary mean from `+0.5135¢` to roughly
`+1.18¢` — **inside the existing interval's half-width**, changing no robustness check and no
verdict. The mechanism claim, though, does not survive: **the analytic minimum at the extremes is
not destroyed by rounding, it is destroyed only at small size.** The sentence *"the cheapness this
idea was reaching for does not exist in practice"* should read *"does not exist at one contract."*

This is recorded as **P5** in `PARKED.md` and is not corrected in the body above, per the
amend-never-edit rule and this run's bar on changing figures.

## 3. Reconciling 6.22% against 254 rungs from a 13,832-market window

The two numbers look inconsistent and are not. **"Usable" denominates 4,081, not 13,832.**

```
universe                                     13,832 markets  (4,787 events, 245 series)
  − no ask at the entry instant               5,018
  − no candle before the entry instant        3,088
  − no candles at all                         1,309
  − staleness beyond the 600s cap               325
  = usable                                     4,081

in band [0.93, 0.98]                            254 rungs  =  6.22% of 4,081
                                                            =  1.84% of 13,832
```

Both percentages are true of different populations, and the reported one is the larger. Two things
follow that the body does not say:

1. **The `~89× better populated` comparison against H55 is usable-to-usable, not universe-to-universe.**
   H55's `1 of 1,523 rungs = 0.07%` is its own post-exclusion denominator, built by a different
   pipeline at a 24-hour lead. The ratio compares two differently-filtered populations. The
   direction of the finding is not in doubt — the band is populated at ten minutes and essentially
   empty at twenty-four hours — but **89× is not a measured multiple**, it is a ratio of two
   filtered rates.
2. **The filter runs toward liquidity, and the body says so.** 70.5% of the universe was excluded,
   over half of it for having no ask or no candle — and a market with candles is a market that
   traded. SKILL.md records this exact shape as a selection variable: *a missing quote means nobody
   was trading, which happens when the outcome is already obvious.* At a ten-minute lead on a
   93–98¢ contract, that is not a hypothetical.

**254 rungs across 245 events** is also worth stating plainly: almost every contributing event
supplied exactly one rung, which is what a mutually-exclusive ladder should do when only one rung
at a time can sit in a five-cent band. The event-level and rung-level samples are nearly the same
objects, which is why the two means differing in *sign* (`+0.5135` against `−0.9457`) is a
weighting artifact of a handful of multi-rung events rather than two independent readings.

## 4. One universe figure inherited by this entry is now known to be an undercount

The instrument section describes the universe as *"13,832 markets / 4,787 events / 245 series with
`close_time` in 2026-06-07 → 2026-06-11"*, derived from the **live** path. A2 has since measured
the same window on both paths and found `/historical` a strict superset — 20 events present only
on historical, zero only on live, because live `/markets` has a sliding `close_time` floor
(`registry/historical/REACH-2026-08-14.md` §A2.2).

**The 4,787 figure is an undercount of unknown size**, parked as **P7**. It is a denominator, not a
result: it does not enter the P&L, the intervals or any robustness check, and no figure above moves
because of it. It does mean the study's coverage claims are conservative.
