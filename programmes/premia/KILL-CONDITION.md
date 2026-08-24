# T1 - The kill condition for family 4, written before the venues

Programme: premia (structural risk premia). Packet 8, task T1.
Written **2026-08-24, before any source on perpetual funding, variance risk premium, venue
mechanics or venue failure was read or searched for** in this session. Committed alone.
**Not to be edited** - amendments only, dated, with the original preserved verbatim.

**The gate is not lifted by anything below.** `ROADMAP.md` family 4 reads: *venue access
confirmed post-move, and capital deployable through the relocation without being needed
elsewhere.* Neither has happened. A pass here means "worth building to test", never "the
premium is collectable", and never "build it".

---

## 0. Why none of family 2's numbers appear here

Family 2's floor was **25 bps per event**, and its derivation was the width of a published
effective-spread estimate on US small caps. Its annualised bar was **passive + 300 bps**, and its
derivation was the compensation for single-name concentration against an index fund. Its event
floor was **50 per year**, and its derivation was the number below which a year of live running
cannot separate the strategy from noise.

**None of those quantities exist in this family.** There is no per-event unit - the return is a
continuous flow, not an event. There is no spread estimate whose width sets a resolution limit.
There is no event count. Carrying any of those numbers across would be fitting this family's bar
to another family's cost structure, which is the same error as fitting a threshold to a result.

What *is* carried across is **structure**: two tests that must both pass, a symmetry section
stating what survival requires, an explicit could-not-establish list, and the refusal of a fourth
outcome. Structure transfers. Numbers do not.

### 0a. Disclosure - what prior knowledge I hold, and how it did and did not enter

Family 2's T1 could truthfully say no insider-trading result informed any threshold. **I cannot
say that here and will not pretend to.** I hold general background knowledge about this sector:
that perpetual funding rates take both signs and are regime-dependent; that venue failures have
occurred; that insurance funds and auto-deleveraging exist as mechanisms. No source was consulted
this session, but the background is present and the honest thing is to name it rather than claim a
blindness I do not have.

**Where that background could bias this document:** toward leniency, if I unconsciously calibrated
a threshold to a remembered carry level so that it would be clearable.

**The mitigation, applied throughout:** every threshold below is derived from a stated **cost or
risk** quantity. **None is derived from a remembered return.** I noted while setting section 1c
that I could have asked whether the floor "binds" against carry levels I half-remember, and
deliberately did not use that reasoning - a threshold chosen to be clearable is not a threshold.

---

## 1. The strands, and the return threshold

### 1.0 Strand independence

**The condition binds per strand, not on the family.** Two strands:

- **S1 - perpetual funding carry.**
- **S2 - variance risk premium.**

**The family survives only if at least one strand survives on its own numbers.** Averaging is
prohibited. **S2 inherits every venue test in this document and nothing else from S1** - an
options venue has its own fee, margin and backstop structure, and a verdict on S1 transfers
nothing to it.

### 1.0a The second leg is part of the strand

A delta-neutral carry book has **two legs**. Reporting a funding carry against the perp leg's
costs alone, while the hedge leg sits at another venue or in custody with its own fees, its own
margin dependency and its own failure mode, is a half-costed strand.

> **The cost and risk of the hedge leg - venue, custody arrangement, fees, and any cross-venue
> margin dependency - are part of the strand. A strand whose hedge leg is not costed is
> could-not-establish, not a carry figure with a caveat.**

### 1.1 The quantities, defined now so T5 has no discretion

All annualised, as a fraction of capital deployed to the strand.

| | |
|---|---|
| `B` | the benchmark - a **sterling cash or near-cash rate available to a UK individual**, documented at T5 from a primary source, cited. Not zero. |
| `G` | **conservative** gross carry (see 1.2). |
| `H` | holding period in years, stated and defended by T5. |
| `C` | full round-trip cost as a fraction of deployed capital: **all four fee events** (both legs, entry and exit), plus both FX conversions, plus any transfer or withdrawal charge. |
| `f` | ongoing proportional costs (funding-side fees, borrow, margin financing) from T3. |
| `F` | **fixed** annual cost of running the book, in currency, independent of size (see 1.4). |
| `K` | capital deployed to the strand, in currency. |
| `E(K)` | achieved excess over benchmark = `G - C/H - f - F/K - B`. |
| `E_inf` | excess before fixed costs = `G - C/H - f - B`. |

### 1.2 Which carry number faces the threshold

> **The threshold is applied to a conservative point of the carry distribution, never to the
> mean.** `G` is the lower bound of a published interval; where dispersion is published without an
> interval, `G` = mean minus one stated standard deviation.
>
> **If no dispersion is published for a strand, that strand is capped at could not establish**,
> whatever the mean.

**Why.** Perpetual funding is an autocorrelated, regime-dependent series that takes both signs. A
mean without dispersion cannot be netted against a threshold, for the same reason family 2 found
that an effect quoted without its horizon could not be netted against a hurdle. A single-regime
sample is a measurement of the regime.

> **A carry figure must come from a sample of at least 24 months that contains periods of both
> signs, or the strand is capped at could not establish.**

### 1.3 Test A - the absolute floor: **E(K) >= 5.00 percentage points over benchmark**

> **KILL if the excess over benchmark, net of every cost line, cannot reach 5.00 pp at any
> deployable size.**

**Derivation.** This is the minimum spread for holding **unsecured, uninsured exposure to a
non-bank counterparty** with no deposit protection, no mandated segregation, and a documented
industry loss history. The nearest priced analogue in traditional markets is deep-speculative-grade
unsecured credit, where spreads over risk-free run in the high single digits. Venue-custody
exposure has plausibly **worse** loss-given-default than CCC credit - historical recoveries in
venue failures have been poor and slow - and possibly **better** frequency. 5.00 pp sits below
the CCC anchor to reflect the frequency difference, and far above investment grade because this
exposure has none of the protections investment grade implies.

**Tag: ASSUMED.** It is a judgement anchored on a credit analogue, not a measurement. Stating that
plainly is the point of tagging it.

### 1.4 Test B - the fixed-cost multiple: **E(K) >= 3 x F/K**

**The principle, stated once and used twice in this document:**

> **No single cost or risk line may consume a third or more of the excess return.** A line that
> large makes the *sign* of the residual hostage to that line's own estimation error. This is
> family 2's pessimistic-hurdle sign test in the shape this family's cost structure takes.

> **KILL if fixed costs consume a third or more of the excess over benchmark at every deployable
> size.**

**`F` has two components:**

**(i) Attention.** A delta-neutral perpetual book requires margin monitoring, funding-cycle
attention and rebalancing - and requires *most* of it precisely in the volatile periods when carry
is highest. Pre-committed: **3 hours/week baseline over 44 weeks, plus 8 hours/week over 8 stress
weeks = 196 hours/year.** At **GBP 60/hour** opportunity cost: **GBP 11,760/year.**

**Tag: ASSUMED**, all three inputs. Because I invented the hourly rate, **T5 must report `K_min`
at GBP 30/hour and GBP 120/hour as well as GBP 60.** A parameter I made up must not silently drive
the answer.

**(ii) Fixed monetary costs** - transfers, withdrawals, FX round trips, and any charge that
behaves like family 2's FX floor by not scaling with size. **Unknown until T3.**

> **If T3 cannot establish the fixed monetary costs, the strand is capped at could not establish** -
> `F` is incomplete, so `K_min` cannot be computed.

### 1.5 The capital floor, computed rather than asserted

Both tests are one inequality in `K`. T5 solves it:

```
Test A:  E_inf - F/K >= 0.0500      ->  K >= F / (E_inf - 0.0500)
Test B:  E_inf - F/K >= 3F/K        ->  K >= 4F / E_inf

K_min = max(  F / (E_inf - 0.0500) ,  4F / E_inf  )

If E_inf <= 0.0500 there is no K that passes  ->  KILL on carry.
```

**T5 must state `K_min` as a number**, at each of `H` in {0.25, 0.5, 1, 2, 3} years, using the `H`
that maximises `E_inf` subject to `H <= 3`.

**Why `H <= 3`.** A holding period longer than three years is a bet on a venue surviving three
years, and section 3 refuses to underwrite that.

> **KILL if `C/H` alone exceeds `G - B - 0.0500` at every `H <= 3`** - the round-trip cost cannot
> be amortised to below the floor over any defensible holding period.

---

## 2. The loss threshold - because a carry threshold alone is half a condition

This family's failure mode is **not a slow bleed. It is a discrete event.**

### 2.1 What counts as a material loss event

> **The removal of >= 25% of the capital deployed at a single venue, or its unavailability for
> more than 30 days, by an action of the venue or its backstop rather than by the market movement
> of the position itself.**

**Why 25%.** At an excess of 5-10 pp, a 25% loss takes three to five years of carry to recover. At
or above that the strategy stops being a carry book and becomes a recovery exercise, and a
strategy that spends years recovering has a negative realised return over any holding period this
family can defend.

### 2.2 The survivability ceiling on deployed size

> **No more than 15% of Walton's investable capital at any single venue. No more than 30% across
> all family-4 venues combined.**

**Why 15%.** A total loss at one venue must be a bad year, not a changed plan. 15% is the level at
which the remainder absorbs a total loss without altering the relocation - which is the specific
thing this family's capital must survive.

**Why the aggregate is 30% and not 45%.** **Venue failures in this sector are not independent.** A
stress that fires one venue's backstop is the same stress that fires another's. The aggregate cap
must therefore sit well below the sum of the independent caps, and treating three venues as three
independent 15% exposures is the error this line exists to prevent.

**Tag: ASSUMED**, both figures.

### 2.3 The uninvestability test - family 2's FX floor, generalised in advance

Fixed costs make the required carry a **declining function of size**. Survivability makes the
permitted size an **increasing function of Walton's capital**. Those two curves may not meet.

> **T5 must report the investable capital at which `K_min` equals 15% of it - that is,
> `K_min / 0.15` - and state it as: "this structure requires investable capital of at least GBP X
> for Walton to run it inside the survivability cap."**
>
> **This packet does not ask what Walton's capital is and must not assume it.** T5 reports the
> threshold; the comparison is his.

> **KILL if `K_min / 0.15` exceeds any plausible retail scale** - stated by T5 as a number, with
> the judgement left explicitly to Walton rather than made on his behalf.

Family 2 discovered a fixed FX minimum that made small positions uneconomic **after** the fact.
This is the same shape, pre-committed, and it may well be what decides this packet.

---

## 3. Counterparty-failure history - named before reading how often it has happened

### 3.1 Venue exclusion - absolute, not a rate

A venue is **excluded from the venue set** if, within its vantage window (section 4), it has:

1. **suspended, gated or delayed customer withdrawals for more than 72 hours** outside a
   pre-announced maintenance window;
2. **applied socialised loss, clawback, or any reduction to a profitable or fully-margined
   position** other than through a published, pre-existing auto-deleveraging mechanism;
3. an **unresolved customer loss** - users not made whole, in full, in the asset owed; or
4. **failed to publish, or withdrawn, its insurance-fund balance history.**

> **If exclusion empties the venue set for a strand, that strand is a KILL** - not could not
> establish. Exclusions rest on established facts, not on instrument failure.

### 3.2 The rate test, by inversion - because frequency may not be estimable

Frequency of venue failure is a small-sample problem by construction, and T4 may not be able to
estimate it. So the rate test is posed **backwards**:

```
p*  =  E / L        the annual failure frequency at which the excess falls to zero
```

where `L` is loss-given-failure as a fraction of capital deployed to the strand.

> **T5 must state `p*`.** The verdict may be **survives** only if T4 **bounds the documented
> frequency at or below `p*/3`** - the one-third principle of section 1.4, applied to the tail.
>
> **If T4 cannot bound the frequency, the verdict is could not establish.** Not a kill: no
> frequency was established, so none was found above the bar.

> **`p*` is not an expected-value calculation and must not be presented as one.** It consumes the
> **carry side only**. It states *what you are being paid to accept*, not an estimate of what you
> are accepting. **No figure multiplying an assumed frequency by a loss to produce an expected
> cost may appear in T4 or T5.** That is the calculation this section exists to replace.

### 3.3 `L` is not bounded above by the deposit at the failing venue

The trap this line exists to catch: if the perp leg's venue fails, the loss is not merely the
margin held there. **The surviving hedge leg becomes an unhedged market position**, and the loss
includes whatever that position does over the time required to re-hedge or unwind it.

> **`L` must include the market exposure created by the surviving leg becoming unhedged.** If T3
> and T4 cannot establish that, `L` is could not establish, `p*` cannot be computed, and the strand
> is **could not establish**.

**Corollary T3 must answer:** whether the two legs sit at the **same** venue or at different ones.
Same venue means zero diversification and `L = 1.0` - a single failure takes both legs. Different
venues does **not** automatically mean a lower `L`, for the reason above.

### 3.4 Auto-deleveraging is a structural finding, not a frequency question

ADL is not a failure. It is **designed behaviour in normal-but-stressed operation**, which is why
it will be under-represented in any incident record.

> **If a venue's own documentation shows that auto-deleveraging can close a profitable,
> fully-margined position without the holder's consent, that is a structural finding carried into
> T5 regardless of frequency.**
>
> A delta-neutral book whose hedge can be removed by the venue at the moment of maximum stress is
> not delta-neutral. It is delta-neutral until it matters.
>
> **No frequency estimate is required to record this, and its absence from the incident record is
> not evidence against it.**

---

## 4. The vantage rule - and the asymmetry this family requires

### 4.1 The family floor: **2023-01-01**

**Justification.** The perpetual-swap venue population was materially reconstituted following the
venue failures of 2022; a venue's earlier record describes a different competitive structure, a
different disclosure practice, and in several cases different ownership. A 2023-01-01 floor also
leaves roughly three and a half years of record at today's date - **enough to observe events and
not enough to estimate their frequency.** That limitation is part of the T4 finding, not a reason
to move the line.

### 4.2 Per-venue override, whichever is later

Evidence about a venue from before its most recent **change of legal domicile, change of ownership
or corporate restructuring, change of insurance-fund or socialised-loss policy, or any
withdrawal-gating event** is evidence about a different venue.

### 4.3 The asymmetry - stated because a symmetric rule would launder survivorship bias

> **The vantage rule applies to favourable evidence only.**
>
> A venue's clean operating record, its published policy, its insurance-fund balance, a carry
> estimate drawn from it - these are claims about the venue **as it now is**, and pre-vantage
> versions of them do not transfer.
>
> **Adverse evidence does not expire.** A failure, a socialised loss, a clawback or a gating event
> is evidence about **what this class of counterparty does under stress**. It remains evidence
> whether or not the venue that produced it still exists, and whether or not it predates the
> vantage line.

**Why.** The surviving venue set is a **survivor set by construction**. A symmetric vantage line
would discard exactly the observations that define the tail and retain exactly the ones that
flatter it. In this family, **a symmetric vantage rule is survivorship bias with a methodological
justification attached.**

Family 2's vantage rule was symmetric because its evidence was effect sizes from independent
samples, where an old sample is simply an old measurement. That reasoning does not transfer, and
the difference is written here so the carry-over is not mistaken for a copy.

### 4.4 Search failure is not absence - and venue silence is a third thing

> **A paywalled paper, an unreachable page, or a source available only in summary is
> could-not-establish on that item. It is never recorded as "no evidence found".**

> **Run positive controls on any search whose null is reported.** A zero-hit search proves nothing
> unless terms that *must* appear in that source also return non-zero. This is packet 7's McLean &
> Pontiff catch, and it applies to incident searches exactly as it applied to a predictor list.

**Three states, never to be conflated:**

| state | meaning | where it goes |
|---|---|---|
| **the venue does not publish it** | a datum **about the venue** | T3, flagged as a silence |
| **the source exists and I could not reach it** | instrument failure | could not establish |
| **the source is reachable and says nothing on the point** | a null, **only if positive-controlled** | reportable |

---

## 5. The tail pre-commitment - the one this family needs and family 2 did not

> **A carry figure computed without a quantified tail is not a result.**

**"Quantified tail" means all three of the following, defined now so T5 cannot fudge it:**

1. **Magnitude bounded** - the maximum fraction of deployed capital the documented backstop
   mechanism can remove, from the venue's own documentation, **and** the unhedged-leg exposure of
   section 3.3.
2. **Frequency bounded** - a documented count of qualifying events over a stated exposure window,
   sufficient to place the frequency at or below `p*/3`.
3. **Correlation established** - documented evidence on whether qualifying events cluster in the
   conditions under which carry is largest, **or** documented evidence that they do not.

> **Survival requires all three. Magnitude alone is not a quantified tail.**
>
> If **(2)** is unavailable - which T4 may well find, because it is a small-sample problem by
> construction - the verdict is **could not establish**, whatever the carry.
>
> If **(3)** is unavailable, the verdict is likewise capped at could not establish. An uncorrelated
> tail and a carry-correlated tail are **different instruments with the same mean**, and this
> project does not treat them as one.

### 5.1 The disclosure rule

> **No carry figure may appear in T2, T4, T5 or the close-out without, attached to it:** its sample
> period and venue; whether it is gross or net and of what; its dispersion; and its **tail status** -
> which of the three components above are established.

A carry number quoted bare is a number without its instrument. This is packet 6's per-URL
contribution rule in this family's shape.

---

## 6. What makes the answer "could not establish" rather than a kill

An instrument failure in the scoping, not a finding about the premium. Any one forces it, per
strand:

1. A venue does not publish its **loss-backstop mechanism**, its trigger, or its history of use.
2. **No post-vantage-line re-estimation** of the strand's magnitude exists (section 4.1).
3. A published magnitude exists but is **gross only**, and its cost components cannot be
   reconstructed from T3.
4. A magnitude exists **without dispersion**, or from a sample shorter than 24 months, or from a
   sample of a single sign (section 1.2).
5. **T4 cannot bound the tail frequency** at or below `p*/3` (section 3.2).
6. **`L` cannot be established**, including the unhedged-leg component (section 3.3).
7. **Correlation of tail with carry is neither established nor excluded** (section 5, item 3).
8. **Fixed monetary costs cannot be established** from T3, so `K_min` cannot be computed
   (section 1.4ii).
9. **The hedge leg is not costed** (section 1.0a).
10. A search returns a null **its positive controls do not license** (section 4.4).

---

## 7. What a survival requires, stated for symmetry

A pre-registration that only defines failure invites a pass by default.

**A strand survives scoping only if ALL of the following hold:**

1. `E(K) >= 5.00 pp` over a **documented** benchmark, at a stated `K` and `H` (section 1.3).
2. `E(K) >= 3 x F/K` at that `K` (section 1.4).
3. `K_min` computed, and `K_min / 0.15` **reported as a number** (section 2.3).
4. Every venue in the strand's set **passes section 3.1** exclusion.
5. `L` established **including the unhedged-leg component** (section 3.3).
6. Documented tail frequency **at or below `p*/3`** (section 3.2).
7. Tail **correlation with carry** established or excluded (section 5, item 3).
8. Carry from a **post-2023-01-01**, >= 24-month, both-signs sample **with dispersion** (1.2, 4.1).
9. Every figure traceable to a **named, dated source that was read rather than summarised.**

**Missing any of 1-4 is a KILL. Missing 5-9 is COULD NOT ESTABLISH.**

**And regardless of the above:** section 3.4's ADL finding, if it fires, is **carried into T5
verbatim** whether or not the strand otherwise survives.

---

## 8. What T5 must state about direction

As family 2's entry did:

> **If the unestablished items are all on the cost or risk side, the verdict is agnostic while the
> evidence is not**, and T5 must write that where a later reader cannot miss it.

In this family the asymmetry is structural rather than incidental: **magnitude is published and
frequency is not**, so the knowable half of the tail is the half that flatters it.

---

## 9. What this document does not do

- It does not open the programme. **The gate is unchanged.**
- It does not authorise an account, an API key, a test position of any size, a backtest, or capital.
- It does not predict the outcome. The thresholds were set from cost and risk quantities, not from
  any carry figure, and may kill a strand this project would have liked to keep.
- It does not permit a fourth outcome. **A large carry with an unquantified tail is could not
  establish**, not a qualified survival.
- **It does not decide whether Walton should do this even if a strand survives.** Scoping can
  return *survives* and the answer still be *not now* - a premium that is real, documented and
  correctly priced can be unavailable to someone who cannot survive its worst month or needs the
  capital during a relocation. **T5 makes only the first statement.**

---

## 10. Parameter summary and evidence tags

| parameter | value | derived from | tag |
|---|---|---|---|
| absolute floor over benchmark | 5.00 pp | deep-speculative-grade unsecured credit analogue | **ASSUMED** |
| one-third principle | `3x` | sign-of-residual hostage to one line's estimation error | **ASSUMED** |
| attention hours | 196 h/yr | 3 h/wk x 44 + 8 h/wk x 8 | **ASSUMED** |
| hourly opportunity cost | GBP 60 | judgement; **T5 reports GBP 30 and GBP 120 too** | **ASSUMED** |
| material loss event | 25% of venue capital | 3-5 years of carry to recover at 5-10 pp | **ASSUMED** |
| single-venue cap | 15% of investable capital | total loss must not alter the relocation | **ASSUMED** |
| aggregate venue cap | 30%, not 45% | venue failures are **not independent** | **ASSUMED** |
| max holding period | 3 years | longer is a bet on venue survival section 3 will not underwrite | **ASSUMED** |
| vantage floor | 2023-01-01 | post-2022 reconstitution of the venue population | **ASSUMED** |
| min carry sample | 24 months, both signs, with dispersion | regime-dependence of the series | **ASSUMED** |
| benchmark `B` | documented at T5 | primary source, cited | **to be MEASURED** |
| `C`, `f`, `F` monetary | from T3 | venue documentation | **to be INFERRED** |
| `G`, dispersion | from T2 | published estimates | **to be INFERRED** |

**Every pre-committed threshold is tagged ASSUMED, and that is correct rather than a weakness.** A
threshold set in advance is a judgement by definition; the discipline is that it is stated before
the evidence and not moved after.

---

## 11. Amendment discipline

This document is sealed on commit. **Sections 1 through 8 may not be edited.** If a threshold is
wrong, that is recorded as a dated amendment below stating what changed, why, and **what was
already known when the change was made** - because a threshold relaxed after seeing the evidence
is not a threshold.

*(no amendments)*
