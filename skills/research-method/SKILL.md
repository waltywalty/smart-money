---
name: research-method
description: A venue-neutral protocol for deciding whether a market effect is real and whether it is worth money. Use when designing, running or reviewing any empirical study of a market - prediction markets, equities, crypto, anything with a price and a cost of crossing. Covers pre-registration, unit of observation, obtainability as a separate gate, cost measured rather than assumed, controls that hold the measurement's access level, counterbalanced arms, and the distinction between a null and a could-not-establish.
---

# The method, extracted from the venue

This is `empirical-claims` and `prior-art` with the Kalshi specifics lifted out. The worked examples
stay, because they are what make it credible - but every rule below is about *studies*, not about
one exchange.

Read `skills/empirical-claims/SKILL.md` for the instrument-level rules (fetch layers, status codes,
pagination, controls). This file is the layer above: how a study is designed, gated and reported.

---

## 1. Pre-register, seal, hash

Before any outcome is seen, write down and commit **in its own commit**:

1. **The rule.** Exactly what will be measured, on what population, with what instrument.
2. **The settling sample size.** How many independent units make the answer real - decided in
   advance, because deciding afterwards is choosing the answer.
3. **The abandonment conditions.** What would make this not worth finishing.
4. **What each outcome means.** Every branch, including the ones you expect. A pre-registration that
   only describes the hoped-for branch is a hypothesis with extra steps.
5. **Disclosure of what has already been seen**, stated first. A pre-registration written after the
   data is not one.

Then hash it and commit it alone, so the git log proves the order.

> **Worked example.** A depth-surface study pre-registered a size grid, a fixed horizon, a shard
> admission threshold and four outcome branches, and stated in advance: *"the fee arm is worth at
> most 0.53c in total."* When execution later looked impossible, that sealed text was what made
> "could not establish" the honest answer rather than a redesign that happened to run.

**If the sealed design turns out to be impossible to execute, that is a could-not-establish.** It is
not a modified design that happens to run.

---

## 2. The unit of observation is the first question, not the last

Ask it before the sample size, because it determines the sample size.

- Rungs of one ladder resolve together. The unit is the **event**, not the row.
- Twelve strikes on one macro print are **one** observation wearing twelve hats. A calibration
  bucket built from them has n=1.
- Twenty hours inside one outage are **one** event. Leave-one-hour-out will show a tight interval
  and mean nothing; leave-one-**day**-out will show the variable vanishing.

**Test it by leaving one out at the level you claim independence.** If the interval collapses when
you drop a single group, the group was your unit.

> **Worked example.** An `r = +0.885` on n=4 became `-0.016` at n=11, and the leave-one-out range was
> `[-1, +1]` the whole time. The interval was never evidence; the unit was wrong.

---

## 3. Obtainability is a separate gate from statistical validity

A perfect replication is not evidence of tradability. Report the two separately and never let one
stand in for the other.

- **Statistical gate:** is the effect real? Interval, n, unit, leave-one-out.
- **Obtainability gate:** could you have transacted at that price, at that moment, at that size?

> **Worked example.** An effect returned **+4.96c in-sample and +4.99c on 644 genuinely held-out
> events** - matching to 0.03c, leave-one-series-out all positive. It was dead anyway: the ask moved
> +1.64c / +3.12c / +5.00c against the buyer at one, two and three minutes after entry, and the
> detect-to-fill budget was under 60 seconds against a five-minute cycle.

**Measure the price you could have TRANSACTED at, not the price you observed.** For any entry taken
from a bar, re-run the identical logic against the executable side at the entry instant. If they
disagree, the observed price was never available.

---

## 4. Cost is measured, not assumed, and it is a function

The cost of participating is almost never a constant. Before measuring any edge, measure the cost -
and express it as a function of **every axis it varies on**.

Axes worth checking in any market: **horizon** (how far ahead you commit), **size** (how much),
**instrument** (fee schedules vary by product - read the multiplier, never assume it), **venue**,
and **time of day**.

Then **decompose it**, because the components have different attackability. A crossing cost that
is half spread, a third fee and a sixth genuine mispricing has exactly one attackable sixth.

> **Worked example.** A hurdle assumed constant at -4.39c turned out to be **-3.81c at a 24-hour
> lead and -1.94c at ten minutes** - and, on the size axis, to vary by only **0.53c across a 500x
> range**, which bounded an entire study before it ran. The registry had been pricing at the most
> expensive point on the size axis, so the correction made the bar *easier* - the opposite of the
> expected direction.

**Every idea clears the hurdle at the horizon and size it would be entered at, never against zero.**

---

## 5. Controls must hold the measurement's access level

A control that cannot fail the way the measurement can fail is not a control.

- **Same access.** An unauthenticated probe of a private resource answers the *request*, not the
  *resource*. Real keys and impossible keys both returned **400**, indistinguishable, until
  credentials made them separate at **404 against 200**.
- **Same layer.** Read the status of the resource, not of a proxy, a CDN or a summarising fetch layer.
- **A control that must fail is only half of one.** An absence claim also needs a probe that **must
  succeed**, in the same pass - otherwise the pair cannot tell "this is gone" from "everything is
  404 right now".
- **Run it in the same pass**, every pass. Every silent instrument failure in this project was caught
  by a control disagreeing, and not one by inspection.

---

## 6. Counterbalance the arms, hold the source constant

When arms run in sequence, **elapsed history is a second factor and it was not randomised.** Anything
with memory - a rate limiter, a cache, a warmed index, a quota - loads it into whichever arm runs later.

1. Run each arm in **both positions** and report both orderings; or
2. **wash out** - idle until the shared state recovers, and *show* a baseline arm returning to its
   clean value before the next arm starts.
3. **Report the position.** A figure without what ran before it is not reproducible.
4. **Hold the source constant.** Two arms from two machines are not an A/B.

> **Worked example.** Three arms on endpoint A showed 0% rejection; one arm on endpoint B seconds
> later showed 28.4%. One variable differed and the conclusion wrote itself. Repeating the endpoint-A
> arm gave 32.5%, then 44.1% - the limiter was shared and had memory, and the apparent property of
> the endpoint was a property of the running order. Re-run from a different machine, the whole curve
> moved again. **Stopping at the confirming arm would have published a false fact backed by a real,
> reproducible-looking measurement.**

---

## 7. "Could not establish" is not a null

They are different claims and they blur easily.

- **Null:** the instrument worked, the sample was adequate, and the effect is not there.
- **Could not establish:** the instrument failed, or the sample does not exist, or the design could
  not be executed as sealed.

Recording an instrument failure as a finding is worse than either. Say which one it is, in those
words, and say what would change it.

**Check that held-out data exists before designing an out-of-sample test.** One study's entire
universe - 22 events - was already inside the sample that produced the lead. No amount of further
collection creates held-out data; only time does.

---

## 8. Right for the wrong reason - a standing check on premises

When a verdict rests on an unstated premise, **check the premise even when the answer looks right.**
If the premise is false the verdict may survive, but the next study builds on the *reason*, so the
reason has to be fixed even when nothing visible changes.

This check has caught seven entries in one programme. In several the conclusion survived and the
**direction inverted** - which matters, because direction is what the next design is built on.

Ask of every finding: *what would have to be true for this to be right, and did anyone measure it?*

---

## 9. Reporting

- **Lead with what would overturn it**, not with the number.
- Give the **interval, the n, and the unit that n counts**.
- **Depth beside every price.** A price without size is not a price.
- **Composition beside every pooled figure, not just every subgroup.** A pooled number is weighted
  by its mix at least as much as by the variable it names.

  > **Worked example, 2026-08-18.** A cost surface was measured across a 500x size range (span
  > 7.23c) and, in an earlier study, across a 24h-to-10m horizon range (span 1.87c). The five
  > product families in the pool spanned **18.68c at a single size and a single horizon** - **2.05x
  > both measured axes combined**. Which families were in the pool moved the answer more than either
  > variable being studied. The same shape had already appeared one level down, where a -29.7pp
  > calibration gap turned out to be 62 of 89 markets in one series.

  **A cost quoted without its composition is not a cost**, in the same way that a price without size
  is not a price. Before comparing two pooled figures, check whether you are comparing their mixes
  rather than the axis you named.

- **Separate the shape from the magnitude, and say which one you established.** A study can confirm
  that a curve is monotone, negative and dominated by one term while failing to separate its small-end
  values from zero. Report both verdicts. In the worked example above the interval excluded zero only
  from the 100-unit point up, and leave-one-group-out only from 50 up - so the shape was a finding and
  the small-end numbers were not.

- **Composition of every subgroup you highlight**, unprompted - a pooled figure weighted by
  collector health rather than by anything about the market is not a market figure.
- **Scope limits stated as scope limits**, in the sentence with the number: *this is a property of
  these conditions, not of the venue.*
- **Amend, never edit.** Sealed documents get dated amendments. A create that returns 200 instead of
  201 has overwritten something.
- **A session ends with a commit, not a summary.**
