# T1 - The kill condition for family 3, written before the literature

Programme: flow (mechanical flow). Packet 9, task T1.
Written **2026-08-25, before a single source on merger arbitrage, deal breaks or index
reconstitution was read or searched for** in this session. Committed alone. **Not to be edited** -
amendments only, dated, with the original preserved verbatim.

**The gate is not lifted by anything below.** `ROADMAP.md` family 3 reads: *held until another
family is producing.* Nothing is producing - family 1 has detected no events, families 2 and 4 are
scoped and unopened. A pass here means "worth building to test", never "the effect is collectable",
and never "build it".

---

## 0. Why none of the earlier families' numbers appear here

| family | its floor | what set it |
|---|---|---|
| 2 (insider) | 25 bps per event, passive + 300 bps annualised, 50 events/year | the **precision of a US small-cap spread estimate**, and the count below which a year cannot separate the strategy from noise |
| 4 (premia) | 5.00 pp over a cash benchmark | a **deep-speculative-grade unsecured credit analogue**, as compensation for uninsured venue custody |

**Neither transfers, and the reason is structural rather than stylistic.** Family 2's bar was set by
the width of a cost estimate. Family 4's was set by an unquantifiable counterparty tail. **This
family's binding quantity is neither: it is a loss distribution with a known shape** - a capped gain,
an uncapped-in-practice loss many multiples of it, and losses that arrive together.

**So every threshold below is derived from that payoff algebra**, and several are derived *as
formulas* rather than as constants, because the algebra determines them once T2 and T4 supply the
two inputs. A constant fitted before the inputs are known would be a guess wearing a decimal point.

What is carried across is **structure only**: two tests that must both pass, a symmetry section
stating what survival requires, an explicit could-not-establish list, an asymmetric vantage rule,
and the refusal of a fourth outcome.

### 0a. Disclosure - what prior knowledge I hold, and how it did and did not enter

As in family 4, I cannot claim family 2's blindness and will not pretend to. **I hold general
background on both strands**: that merger arbitrage collects a spread and loses multiples of it on a
break; that deal breaks are associated with antitrust posture and with financing conditions; that
the index-inclusion effect was documented decades ago and is generally believed to have decayed. No
source was consulted this session.

**Where that background could bias this document:** toward setting the index strand's bar in a way
that presupposes decay, and toward setting merger arb's in a way that presupposes a real friction.

**The mitigation, applied throughout:** every threshold below is derived from **payoff algebra or
from Walton's stated circumstances**, and **none from a remembered effect size, break rate or
spread.** Where the packet itself states an illustrative shape - *collect 3%, lose 25%* - it is used
**only to instantiate a formula for legibility**, is labelled as the packet's stated shape at every
use, and **is not a measured magnitude.** T2 supplies `s`; T4 supplies `p` and `L`.

---

## 1. The strands, the notation, and the return threshold

### 1.0 Strand independence

**The condition binds per strand, not on the family.** Two strands:

- **S1 - merger arbitrage.**
- **S2 - index-reconstitution flow.**

**The family survives only if at least one strand survives on its own numbers.** Averaging is
prohibited. The two have different frictions, different loss shapes and probably different answers,
and a verdict on one transfers nothing to the other.

**S2 is not assumed to share S1's payoff shape.** Sections 1.2 to 3 below are written around a
capped-gain / large-loss binary because that is S1's structure. **If T2 establishes that S2's payoff
is not of that shape, S2 is judged on sections 1.1, 1.3, 4, 5 and 6 only**, and section 7 records
which tests were applicable. A condition applied to a payoff it was not written for is not a test.

### 1.1 Notation, fixed now so T5 has no discretion

| | |
|---|---|
| `B` | the benchmark. **T5 documents two** from primary sources - a sterling cash or near-cash rate available to a UK individual, **and** a passive equity index total return over a stated period - and **applies the threshold to the higher of the two.** Not zero. |
| `s` | gross gain per completed position, as a fraction of that position. From T2. |
| `L` | loss per broken position, as a fraction of that position. From T4, **as a distribution** - see 3.2. |
| `p` | probability a position breaks, per deployment period. From T4. |
| `c` | all costs per position round trip - commission on every leg, borrow on any short leg, FX both ways, and any fixed minimum. From T3. |
| `n` | number of simultaneous positions. |
| `mu` | expected net return per unit of deployed capital = `(1-p)s - pL - c`. |
| `E` | `mu - B`, the excess over benchmark. |

### 1.2 The two quantities this family's algebra determines

**Break-even break rate.** With a capped gain and a large loss, the strategy's sign is set by one
number:

```
p* = (s - c) / (s + L)
```

Above `p*` the strategy loses money however attractive the spread looks.

**Cluster tolerance.** If a fraction `f` of concurrent positions break inside a rolling 12 months
while the rest complete, the book's 12-month return is `(1-f)s - fL - c`. Setting that equal to
`-D_max` gives the largest survivable cluster:

```
f_max = (D_max + s - c) / (L + s)
```

**Both are pre-committed as formulas.** `D_max` is fixed in section 2.2; `s`, `L`, `p` and `c` are
supplied by T2, T3 and T4. Neither formula was chosen after seeing an input.

### 1.3 The return floor: **E >= 3.5 percentage points**

> **KILL if the net excess over the higher documented benchmark cannot reach 3.5 pp at any
> deployable size.**

**Derivation, from this family's own loss limit rather than from an external analogue.** Section 2.2
sets the maximum correlated-cluster drawdown at **10.0 pp of deployed capital**. A strategy must be
able to earn back its own design-limit drawdown **strictly inside three years**, because a recovery
longer than that exceeds the horizon over which this capital is uncommitted, and because a book that
spends three or more years recovering has a negative realised return over any period Walton would
actually hold it.

```
10.0 pp / 3.5 pp per year = 2.86 years to recover a design-limit cluster.
(10.0 / 3 = 3.33 pp would recover in exactly three years; the floor is set above that,
 not at it, because a limit met exactly is a limit already breached by any error.)
```

**Tag: ASSUMED** - the three-year recovery horizon is a judgement about Walton's circumstances. The
**arithmetic from it is not**: given 10.0 pp and three years, 3.5 pp follows.

**Why the benchmark is the higher of cash and passive.** Merger arbitrage is sold as a low-beta
absolute-return exposure, which argues for cash; the capital nevertheless sits in equities and bears
equity-like tail risk, which argues for the index. **Requiring the higher of the two removes the
choice**, and a threshold whose value depends on which benchmark the analyst picks is not a
threshold.

### 1.4 The break-rate ceiling: **p <= p\*/2**

> **KILL if the documented break rate exceeds half the break-even rate.**

**Derivation, from the payoff algebra and nothing else.** Substituting `p = p*/2` into the expected
return:

```
mu = (1-p)s - pL - c
   = s - p(s+L) - c            [expanding]
   = s - (s-c)/2 - c           [at p = p*/2, since p*(s+L) = s-c]
   = (s - c) / 2
```

> **A break rate at half of break-even leaves exactly half the net-of-cost gross spread as expected
> return.** That is the margin of safety this threshold buys, and it is an identity rather than a
> preference.

**Why a margin at all, and why this one.** `p` will be estimated from a historical sample under a
particular enforcement regime, and section 4 says that regime may not be the current one. A 2x
margin means the regime can be **twice as hostile as the sample** without flipping the sign. A
smaller margin makes the verdict a bet on the regime not changing; a larger one would be an
assertion rather than a derivation, because nothing in the algebra picks it.

---

## 2. Two loss thresholds, because one is half a condition

Breaks are **not independent**. A regulatory posture change, a financing market closing, or a
pandemic takes several at once. **A per-deal limit with no cluster limit is a limit on the event
that does not kill you.**

### 2.1 Per-deal maximum: **`d_max` = 2.0% of deployed capital**

> **KILL if the strategy cannot be run with every single position sized so that its break costs no
> more than 2.0% of deployed capital.**

**Derivation.** This family's return is a few percentage points a year **by construction** - a small
spread collected at a high completion rate. A single break costing more than 2.0% of the book
therefore costs **more than a typical year's entire expected return**, which converts one adverse
event into a lost year. At 2.0% a break is a bad quarter; at 4% it is two years; and a book that can
lose two years to one event, several times in a cluster, is not a spread strategy - it is a
short-option position with the premium quoted as a return.

**This implies a position-count floor directly**, which is the point of stating it in these units:

```
position weight w <= d_max / L      ->      n >= L / d_max
```

At the packet's stated shape (`L` = 25%, **illustration only**): `n >= 12.5`, so **13 positions**
before any other consideration.

**Tag: ASSUMED.** The 2.0% level is a judgement; the implication for `n` is arithmetic.

### 2.2 Correlated-cluster maximum: **`D_max` = 10.0% of deployed capital, rolling 12 months**

> **KILL if the documented clustering of breaks implies a rolling-12-month drawdown exceeding 10.0%
> of deployed capital.**

**Derivation.** At the few-percentage-point annual return this family's structure implies, a 10 pp
drawdown is **three to five years of expected return**. Beyond that the realised return over any
horizon Walton would hold it is negative, and the recovery period exceeds the relocation horizon
that makes this capital constrained in the first place. Section 1.3's return floor is derived *from*
this number, so the two are one judgement, not two.

**The test T4 must answer, in scale-free form.** Using `f_max` from section 1.2:

> **KILL if any documented break cluster shows a fraction of concurrent positions breaking inside a
> rolling 12 months greater than `f_max = (D_max + s - c)/(L + s)`.**

At the packet's stated shape (`s` = 3%, `L` = 25%, `c` ignored, **illustration only**):
`f_max = 0.13/0.28 = 46%`. **T4 must establish whether a cluster in which nearly half of concurrent
deals broke inside a year has ever occurred**, and that question is answerable from a historical
record in a way that an abstract drawdown percentage is not.

### 2.3 The two are not redundant, stated so a later reader does not collapse them

Section 2.1 constrains **position size**. Section 2.2 constrains **correlation**. A book can satisfy
2.1 perfectly - every position small - and still be destroyed by 2.2, because 2.1's arithmetic
assumes the breaks arrive one at a time. **Passing 2.1 is not evidence about 2.2**, and T5 may not
treat it as such.

---

## 3. Breadth - the family-4 lesson transposed

### 3.1 Minimum simultaneous position count, named before any spread figure is read

A positive mean with a skewed distribution is **realised only across breadth**. Below some count the
realised outcome is the *median*, and for this payoff the median sits on the **wrong side** of the
mean: with few positions the modal experience is **zero breaks**, which overstates the mean, until
the year it does not.

> **`n_min` = the largest of three, each derived separately:**
>
> ```
> (a) breadth for the mean to be the expectation faced:   n >= 3 / p
> (b) breadth for the realised return to be informative:  n >= (s+L)^2 * p(1-p) / mu^2
> (c) breadth implied by the per-deal loss limit:         n >= L / d_max        [section 2.1]
> ```

**Derivation of (a).** The number of breaks in a period is approximately Poisson with mean `np`.
Below `np = 3` that distribution is strongly right-skewed and its mode is at or near zero, so the
typical year returns roughly `s` and **flatters the strategy**. At `np >= 3` the count is close
enough to symmetric that a typical year brackets the mean rather than sitting above it. **Three is
the smallest integer mean at which the Poisson mode and mean differ by less than one event.**

**Derivation of (b).** With equal weights, the book's return is `R = s - (k/n)(s+L) - c` where
`k ~ Binomial(n, p)`, so `SD(R) = (s+L)*sqrt(p(1-p)/n)`. Requiring `SD(R) <= mu` - one standard
deviation no larger than the whole expected return - rearranges to (b). **This is the term that
explodes as `p` approaches `p*`**: as the mean collapses, the breadth needed to observe it rises
without bound. That behaviour is the reason (b) is stated as a formula and not a number.

> **KILL if `n_min` exceeds the number of simultaneous positions available**, which T3 and T4
> together must bound from the published rate of qualifying situations.

### 3.2 `L` is a distribution, not a number, and which point of it faces which test

Loss given break depends on **how far the target ran on announcement**, so it is a distribution and
a right-skewed one in loss terms.

> **T4 must supply `L` as a mean and at least one upper quantile.**
>
> - The **per-deal test (2.1)** uses the **mean**.
> - The **cluster test (2.2)** uses the **upper quantile**, because a cluster is precisely where the
>   tail of the loss distribution and the tail of the break process coincide.
> - **If only a point estimate is published, the strand is capped at could not establish** on the
>   cluster test - not passed on it.

**Why the two tests take different points.** Using the mean in the cluster test would assume that a
regime bad enough to break half the book breaks it at average severity. **The assumption that makes
clusters survivable is exactly the assumption a cluster violates.**

---

## 4. The capital floor

> **`K_min` = `n_min` x `V_min`**, where `V_min` is the smallest position at which fixed per-position
> costs are second-order.

**Derivation.** Let `F_pos` be the fixed cost of one position in currency - commissions on every
leg, and any minimum that does not scale, including an FX minimum of the kind family 2 found. Let
`mu_deal = (1-p)s - pL` be the expected gross gain per unit of position. Requiring fixed costs to
consume no more than a share `phi` of that:

```
F_pos <= phi * mu_deal * V      ->      V_min = F_pos / (phi * mu_deal)
K_min = n_min * V_min
```

**`phi` = 0.10, and here is why that number and not another.** `mu_deal` is a product of two
*estimated* quantities - `s` from a spread and `p` from a break rate - and section 1.4 already
permits `p` to be a factor of two away from its sample. **A fixed-cost drag of one tenth is the
level at which it is second-order to that estimation error rather than comparable to it.** Above a
tenth, the fixed cost and the parameter uncertainty are the same size, and the sign of the residual
depends on which of the two you trust. This is not family 4's one-third principle; it is tighter,
and it is tighter because this family has two estimated parameters where family 4 had one.

> **T5 must report `K_min` as a number, and must report `K_min` divided by the fraction of Walton's
> capital this family may occupy**, stated as: *"this structure requires investable capital of at
> least X for Walton to run it at the required breadth."*
>
> **This packet does not ask what Walton's capital is and must not assume it.** T5 reports the
> threshold; the comparison is his.

> **KILL if `F_pos` is established and `K_min` exceeds any plausible retail scale.** **COULD NOT
> ESTABLISH if `F_pos` cannot be established from T3**, because then `V_min` and `K_min` are not
> computable. Family 2 found a fixed FX minimum after the fact; family 4 could not compute its
> capital floor at all because no venue published a withdrawal figure. **This is the third time the
> fixed-cost line has been the binding unknown, and it is named in advance for that reason.**

---

## 5. The vantage rule - two lines, one per strand, both asymmetric

### 5.1 The lines are functional and fixed from primary documents in T3

No date is asserted here, because asserting one would mean using background knowledge of current
regulatory or index-provider facts that section 0a says must not enter.

| strand | the vantage line |
|---|---|
| **S1 merger arbitrage** | the effective date of the **most recent published revision of the US merger-review framework** - the Merger Guidelines, the HSR rules, or the equivalent primary instrument - established in T3 from the agencies' own publications. Break rates are a function of enforcement posture, and posture is expressed in those documents |
| **S2 index reconstitution** | the effective date of the **most recent methodology change that the index provider itself states was made to reduce predictability, front-running or trading impact** - established in T3 from the provider's own methodology document and change log |

> **A magnitude whose sample closes before its strand's line cannot support a "survives scoping"
> verdict.** Its ceiling is **could not establish**, however large the historical figure. This is
> the rule that decided family 2, restated for this family's regime variables.

### 5.2 The asymmetry, carried from family 4 because it is if anything more binding here

> **The vantage rule applies to favourable evidence only.**
>
> A completion rate, a spread level, an index-effect magnitude, a clean run of years - these are
> claims about the regime **as it now is**, and pre-line versions of them do not transfer.
>
> **Adverse evidence does not expire.** A documented break cluster is evidence that **clusters
> occur in this strategy**, and it remains evidence whether or not the enforcement regime that
> produced it still holds.

**Why it is more binding here than in family 4.** The set of enforcement regimes ever observed is a
handful, and clusters are by construction rare. **A symmetric line would discard most of the
observations that define the very risk this condition exists to bound**, and would do so by an
argument that sounds methodological. In this family, a symmetric vantage rule is not merely
survivorship bias - it is survivorship bias applied to the tail specifically.

### 5.3 Search failure is not absence, and neither is a paywall

> **A paywalled study, an unreachable page, or a source available only in summary is
> could-not-establish on that item. It is never recorded as "no evidence found".**

> **Run positive controls on any search whose null is reported.** A zero-hit search proves nothing
> unless terms that must appear in that source also return non-zero.

**And the packet-8 correction, pre-committed rather than discovered:**

> **T4 must distinguish unretrieved from unknowable.** If a break distribution exists in a
> commercial deal database that this packet forbids calling, that is a **scope boundary of this
> packet, not a limit of public knowledge**, and it must be written so a later reader cannot
> misread it. The two are recorded in **separate lists**, never one.

---

## 6. The break-distribution pre-commitment

> **A return figure computed without a quantified break distribution is not a result.**

**"Quantified break distribution" means all three, defined now so T5 cannot fudge it:**

1. **Rate bounded** - a documented break rate over a **stated universe and period**, with the
   universe defined precisely enough that the denominator is knowable.
2. **Severity as a distribution** - mean **and at least one upper quantile**, per section 3.2.
3. **Clustering characterised** - documented evidence on whether breaks arrive independently or in
   regime-driven clusters, **or documented evidence that they do not.**

> **Survival requires all three.** A rate alone is not a quantified break distribution.
>
> If **(2)** is unavailable, the cluster test is **could not establish** and the strand cannot
> survive.
>
> If **(3)** is unavailable, the verdict is likewise capped at could not establish. **An independent
> break process and a clustered one are different strategies with the same mean**, and this project
> does not treat them as one.

### 6.1 Is this a measurement of the position I would hold?

**This question has now failed two families first, before any threshold was reached.** Family 2: no
strand reported a per-event effect - all were portfolio alphas. Family 4: the ~7% was a fixed-date
basis and the Sharpe was a threshold convergence trade, neither of which is a held funding-carry
position.

> **Every magnitude entering T5 must be a measurement of the position Walton would hold.** A fund's
> reported performance, an index of arbitrage strategies, a portfolio alpha, an event-study
> abnormal return, or a spread quoted without the holding period are **not** that.
>
> **A magnitude that fails this test is could-not-establish on the strand, not a proxy for it.**

### 6.2 The disclosure rule

> **No return figure may appear in T2, T4, T5 or the close-out without, attached to it:** its sample
> period and universe; whether it is gross or net and of what; whether it is the position Walton
> would hold; and its **break-distribution status** - which of the three components above are
> established.

### 6.3 What loss channel does this condition not name?

Family 4's sealed condition enumerated loss channels and **missed two** - forced liquidation and
venue outage - both found inside its own packet, both recorded as defects. **That is a pattern, not
an accident: an enumeration written before the evidence will be incomplete.**

> **T4 must ask explicitly: what loss channel does T1 not name?** and record the answer, whether or
> not one is found. A blank answer is a finding; an unasked question is a defect waiting to be found
> by someone else.

---

## 7. What makes the answer "could not establish" rather than a kill

An instrument failure in the scoping, not a finding about the strategy. Any one forces it, per
strand:

1. The break **rate** is not published over a defined universe (section 6, item 1).
2. **Severity is published only as a point estimate**, so the cluster test cannot run (3.2).
3. **Clustering is neither established nor excluded** (section 6, item 3).
4. **No magnitude post-dates the strand's vantage line**, and no post-line re-estimation exists (5.1).
5. The published magnitude is **not a measurement of the position Walton would hold** (6.1).
6. **`F_pos` cannot be established** from T3, so `V_min` and `K_min` are not computable (section 4).
7. The **rate of qualifying situations is not published**, so `n_min` cannot be compared to what is
   available (3.1).
8. A search returns a **null its positive controls do not license** (5.3).
9. The strand's costs `c` cannot be reconstructed, so `p*` and `mu` are not computable (1.2).

---

## 8. What a survival requires, stated for symmetry

A pre-registration that only defines failure invites a pass by default.

**A strand survives scoping only if ALL of the following hold:**

1. `E >= 3.5 pp` over the **higher** of a documented cash and a documented passive benchmark (1.3).
2. `p <= p*/2`, with `p` and `p*` both computed from documented figures (1.4).
3. Every position sizeable so its break costs `<= 2.0%` of deployed capital (2.1).
4. No documented cluster exceeding `f_max` (2.2), evaluated at the **upper quantile** of `L` (3.2).
5. `n_min` computed and **available simultaneous positions >= `n_min`** (3.1).
6. `K_min` computed and **reported as a number** (section 4).
7. Magnitude from a sample **closing after the strand's vantage line** (5.1).
8. **All three components** of the break distribution established (section 6).
9. Every magnitude a **measurement of the position Walton would hold** (6.1).
10. Every figure traceable to a **named, dated source read rather than summarised**.

**Missing any of 1-5 is a KILL. Missing 6-10 is COULD NOT ESTABLISH.**

---

## 9. What T5 must state, beyond the verdict

### 9.1 Direction of the missing evidence

> **If the unestablished items sit on the loss side, the verdict is agnostic while the evidence is
> not**, and T5 must write that where a later reader cannot miss it.

In this family the asymmetry is structural: **spreads are quoted publicly and continuously; break
distributions are not.** The knowable half is the half that flatters the strategy.

### 9.2 Whether T4 actually decided the packet

Packet 8 wrote the equivalent tail pre-commitment and **it never fired**, because the carry failed
first; it was recorded as **untested, not vindicated**.

> **T5 must state plainly whether T4 decided this packet or whether something failed before it**,
> and must not arrange the ordering to match the expectation. A rule that has not been tested is not
> evidence that the rule works.

### 9.3 Survives is not now

> **T5 must state, separately from the verdict, whether a "survives" here would still mean "not
> now."**

Family 3's gate exists because **this is the first family where being wrong costs money**, and that
reason is independent of whether the premium is real. A loss distribution that is real, correctly
priced, and genuinely compensated is not thereby one Walton should bear at his size, through a
relocation. **T5 makes the first statement and must not blur it into the second.**

---

## 10. What this document does not do

- It does not open the programme. **The gate is unchanged.**
- It does not authorise a broker account, a deal-database subscription, a screen of live situations,
  a backtest, or capital.
- It does not predict the outcome. The thresholds were set from payoff algebra and from Walton's
  stated circumstances, and may kill a strand this project would have liked to keep.
- It does not permit a fourth outcome. **A spread with an unquantified break distribution is could
  not establish**, not a qualified survival.

---

## 11. Parameter summary and evidence tags

| parameter | value | derived from | tag |
|---|---|---|---|
| return floor `E` | **3.5 pp** over the higher benchmark | `D_max` recovered strictly inside three years | **ASSUMED** (horizon); arithmetic from it is not |
| per-deal max `d_max` | **2.0%** of deployed capital | more than a typical year's whole expected return | **ASSUMED** |
| cluster max `D_max` | **10.0%**, rolling 12 months | three to five years of expected return; exceeds the relocation horizon | **ASSUMED** |
| break-rate ceiling | **`p*/2`** | identity: leaves exactly `(s-c)/2` as expected return | **DERIVED** |
| break-even rate | **`p* = (s-c)/(s+L)`** | payoff algebra | **DERIVED** |
| cluster tolerance | **`f_max = (D_max+s-c)/(L+s)`** | payoff algebra | **DERIVED** |
| breadth (a) | **`n >= 3/p`** | Poisson mode within one event of the mean | **DERIVED** |
| breadth (b) | **`n >= (s+L)^2 p(1-p)/mu^2`** | `SD(R) <= mu` | **DERIVED** |
| breadth (c) | **`n >= L/d_max`** | equal-weight position sizing | **DERIVED** |
| fixed-cost share `phi` | **0.10** | second-order to a factor-of-two tolerance on `p` | **ASSUMED** |
| vantage lines | **functional, fixed in T3** | primary regulatory and index-provider documents | **to be MEASURED** |
| `B` | documented at T5, **higher of two** | primary sources, cited | **to be MEASURED** |
| `s`, `L`, `p`, `c` | from T2, T3, T4 | published studies and primary documents | **to be INFERRED** |

**Six of the twelve are derived rather than assumed**, which is the difference between this
condition and the previous two. **The four ASSUMED constants are judgements and are labelled as
such** - a threshold set in advance is a judgement by definition, and the discipline is that it is
stated before the evidence and not moved after.

---

## 12. Amendment discipline

This document is sealed on commit. **Sections 1 through 9 may not be edited.** If a threshold is
wrong, that is recorded as a dated amendment below stating what changed, why, and **what was already
known when the change was made** - because a threshold relaxed after seeing the evidence is not a
threshold.

**Family 4's condition acquired three dated defects inside its own packet.** The expected number
here is not zero. **Section 6.3 makes finding them a task rather than an accident**, and any found
are to be **recorded as defects, never patched into the sealed text.**

*(no amendments)*
