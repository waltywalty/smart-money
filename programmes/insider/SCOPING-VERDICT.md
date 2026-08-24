# T5 - The verdict against T1

Programme: insider. Packet 7, task T5. Written 2026-08-24.

Judged against `KILL-CONDITION.md`, sealed **before any literature was read** -
sha256 `925b9bff478cea4211d7c4cdccf626e70f2ca58c99745a6730a90cef3dcfcde1`, commit `eac6eda`.

---

# VERDICT: COULD NOT ESTABLISH

**Every strand. No strand was killed. No strand survives.**

This is an **instrument failure in the literature review**, not a finding about whether the
anomaly exists. The packet named this outcome in advance as the one to expect, and it is what
happened.

**The gate is unchanged.** `ROADMAP.md` family 2 still reads *relocation complete, and family 1
has produced a verdict*, and neither has happened.

---

## 1. The pre-committed condition, quoted verbatim

From `KILL-CONDITION.md` section 5:

> **A strand survives scoping only if ALL of the following hold:**
>
> 1. Per-event residual **>= 25 bps** net of the central hurdle, at a stated horizon.
> 2. Residual **positive at the pessimistic hurdle**.
> 3. Annualised net residual **>= passive + 300 bps** on locked capital.
> 4. **>= 50 investable events per year**, from a published figure or one derivable from
>    published figures.
> 5. **Post-publication out-of-sample re-estimation exists**, and the re-estimated effect still
>    satisfies 1 through 3.
> 6. Every figure above traceable to a **named, dated source that was read rather than
>    summarised**.
>
> Missing any of 1-4 is a **kill**. Missing 5 or 6 is **could not establish**.

And from section 4:

> **Could not establish** is an instrument failure in the review. [...] **Any one of the
> following forces it, per strand:**
>
> 1. **The literature reports effect sizes without the horizon, the risk adjustment, or the
>    sample size** needed to compute section 1. An effect quoted without its horizon cannot be
>    netted against a hurdle.
> 2. **No post-publication re-estimation exists**, and the original sample closed more than ten
>    years ago (section 3a).
> 3. **The hurdle's uncertainty range spans the effect size**, so the sign of the residual is
>    indeterminate. This is neither a kill nor a survival and must not be reported as either.
> 4. **The strand's event rate is not reported anywhere** and cannot be derived from published
>    figures without pulling filing data - which this packet is forbidden to do.

### Why this is could-not-establish and not a kill

The distinction is pre-committed and it decides the verdict.

**Section 5's "missing any of 1-4 is a kill" applies where 1-4 were evaluated and found
wanting.** Here they were **not evaluable**. Section 4 fires first, and it is written as *any one
of the following forces it*. Four of its five clauses fire, on separate evidence:

| section 4 clause | fires? | on what |
|---|---|---|
| 4.1 - effect sizes without the horizon, risk adjustment or sample size needed for section 1 | **YES** | No strand reports a **per-event** effect. Every figure is a portfolio alpha or a subgroup mean. Zhao's "abnormal returns" are, on the paper's own statement, **not risk-adjusted**. |
| 4.2 - no post-publication re-estimation, sample closed >10 years ago | **YES** | None found for any strand. L&L closes 1995, CMP 2007 - both past the 2016-08-24 vantage line. |
| 4.3 - the hurdle's range spans the effect, sign indeterminate | **YES** | Worse than spanning: **spread and borrow were not established at all**, so there is no hurdle range to compare against. |
| 4.4 - event rate not reported and not derivable without filing data | **YES** | No strand reports an investable rate after its own classifier. T3 could not extract the classifiable share of the universe. |

**A kill would require having computed a residual and found it inside the hurdle. Nothing was
computed.** Reporting a kill would claim more knowledge than exists, in the direction that
happens to be convenient.

---

## 2. Per strand

| strand | verdict | binding clause |
|---|---|---|
| Aggregate insider buys vs sells | **could not establish** | 4.1, 4.2, 4.3, 4.4 |
| Routine vs opportunistic | **could not establish** | 4.1, 4.2, 4.3, 4.4 |
| Small-cap / microcap concentration | **could not establish** | 4.1 (Zhao not risk-adjusted), 4.3, 4.4 |
| Role weighting | **could not establish** | 4.1, 4.2, 4.3, 4.4 |
| Cluster buys | **could not establish** | no peer-reviewed source reached (section 4a) |
| First-time buyers | **could not establish** | same |
| Filing-lag informativeness | **could not establish** | same |

**The family survives only if at least one strand survives on its own numbers**
(`KILL-CONDITION.md` section 0). None does. **Averaging is prohibited** and none was done.

---

## 3. Four independent routes to the same verdict

Each would produce could-not-establish on its own. Their independence matters: fixing one does
not fix the others.

**Route 1 - the units do not exist.** Section 1 of the kill condition is stated *per event*. No
strand reports a per-event term. CMP report a monthly-rebalanced **long-short portfolio alpha**;
Lakonishok & Lee a 12-month **portfolio spread**; Zhao a **subgroup mean CAR**. None is
convertible to a per-event residual without data.

**Route 2 - the population is undefined, in the source.** T3 established that Form 4 code `P`
reads "Open market **or private** purchase" - the codes do not separate them, and no paper reached
states how it handled the distinction. And CMP's routine rule turns on "a trade" in the three-year
lookback, which is **never defined**: an insider taking an annual March grant is *routine* on an
any-transaction reading and *unclassifiable* on a `P`/`S` reading. **Two defensible readings of
the published rule produce different samples**, so the published effect size is not attached to a
reproducible population.

**Route 3 - neither implementation has a computable expected return.** The headline alphas are
explicitly long-short - "long opportunistic buys and short opportunistic sells". A **long-short**
version needs borrow in exactly the small names where borrow is scarcest, most expensive, and
often unavailable; that cost was not established. A **long-only** version avoids it and forfeits
an unknown share of the reported spread, because `PRIORS.md` does not decompose the legs. **Both
routes end without a number.**

**Route 4 - the vantage rule, pre-committed in section 3a.** No post-publication out-of-sample
re-estimation was found for any strand. Chen & Zimmermann's 331-signal catalogue contains **zero**
insider signals and **no Form 4 data category at all** - a controlled negative. Whether McLean &
Pontiff cover it is itself could-not-establish, their predictor list being in an Internet Appendix
that was not reached. **Section 3a caps these strands at could-not-establish regardless of how
large Lakonishok & Lee's 4.8% looks**, and that is the rule doing what it was written for.

---

## 4. What was established, and it is not nothing

The verdict is could-not-establish. **These are measurements, and they survive it.**

### 4a. Three independent instruments agree the effect concentrates where trading is hardest

| source | sample | finding |
|---|---|---|
| Cohen, Malloy & Pomorski | 1989-2007 | **EW 180 bp/mo vs VW 82 bp/mo** - over half the alpha is in the smaller names |
| McLean & Pontiff | ends 2013 | post-publication returns "higher for portfolios concentrated in stocks with **high idiosyncratic risk and low liquidity**" |
| SEC Rule 605 final release | Q1 2023 TAQ, 400 stocks | ~90% of realized-spread decline captured by 15s for the **largest** cap group, ~**50%** for smaller groups |

**Different instruments, different samples, different decades.** The convergence is the
substantive result of this packet, and it does not depend on any arithmetic that could not be
completed.

### 4b. The mechanism that convergence implies

The anomaly has been publicly documented since at least 2001 and prominently since 2012.
**What survived that publicity survived because it was uneconomic to arbitrage.** That is not an
edge waiting to be picked up - it is a **selection effect on which anomalies persist.** The
residual concentrates in illiquid, low-priced, hard-to-borrow names precisely because those are
the ones the arbitrage did not reach.

Stated as a mechanism, not a measurement. It is consistent with all three rows above and is not
separately tested here.

### 4c. Two hurdle components, established from documentation

**Commission is charged per share**, so its cost in basis points rises as the share price falls:
**35 bps round trip at $2/share**, 70 at $1. `KILL-CONDITION.md` section 1a sets a floor of
**25 bps net** - the commission alone clears it in the price range where CMP's equal-weight leg
lives, before spread, borrow or tax.

**The FX minimum binds on every position below ~$100,000.** 0.20 bp with a **USD 2.00** floor,
charged both ways: a $2,500 position pays **16 bps round trip, eighty times the advertised rate**.
That is less a cost than a **minimum viable position size** - and it points the wrong way for an
effect whose mean is realised across many events and whose hit rate Zhao puts at **36.7%**.
Escaping the fixed fee means fewer, larger positions; the effect needs breadth.

The same shape as the Kalshi fee ceiling: **a fixed charge that vanishes at size, in a strategy
that needs breadth rather than size.**

### 4d. The 10b5-1 field did not exist when the evidence was gathered

Structured 10b5-1 data begins **2023-04-01**. Every strand's evidence predates it. The exclusion
the literature treats as a refinement was, on its own samples, footnote inference or nothing - and
going forward there are **about 3.4 years** of structured data. The vantage rule from the other
direction: not *the evidence is old* but **the instrument the evidence describes did not exist
when the evidence was gathered.**

---

## 5. What would change this verdict

Stated so the verdict is reversible on evidence rather than on enthusiasm. **None of these is
authorised by this packet.**

1. **A post-publication out-of-sample re-estimation of any strand**, published, on a sample
   closing after 2016-08-24, reporting effect size **with horizon and risk adjustment**. The
   single item that lifts section 3a.
2. **McLean & Pontiff's Internet Appendix**, reached and read. If the strand is among their 97,
   their post-publication decline estimate applies directly and route 4 changes.
3. **A published per-event effect size** - abnormal return per Form 4 purchase, not a portfolio
   alpha - at a stated horizon with a stated benchmark.
4. **A published investable event rate** after a stated classifier, or the classifiable share of
   the insider universe under CMP's three-year rule.
5. **A citable effective-spread level in basis points** for sub-$2bn US names from published
   market-quality data, which would give the hurdle a range and let clause 4.3 close.
6. **An unambiguous statement, in a paper, of how `P` was split** between open-market and private
   purchases, and of what "a trade" means in the routine lookback.

**Items 3, 4 and 6 are requests of the literature, not of this project.** They are what would have
to exist for the comparison to be computable at all, and their absence is the finding.

---

## 6. What this verdict does not say

- **It does not say the anomaly is dead.** Nothing here refutes it. Lakonishok & Lee's 4.8% and
  CMP's 82 bp/month were measured and are not disputed - they are measurements of 1975-1995 and
  1989-2007.
- **It does not say the anomaly is alive.** No strand cleared the pre-committed bar.
- **It does not open the programme, and a survival would not have either.** The gate stands.
- **It is not a fourth outcome.** `KILL-CONDITION.md` section 6: "Ambiguity is **could not
  establish**, said plainly." It is said plainly.

---

## 7. What it cost

One session. No collector, no parser, no EDGAR pipeline, **no filing data fetched at any point**.

The packet's own note: *"the cheapest kill is the one that costs a day."* This is not a kill, but
it is the same economy - **the family is not built, and what stops it is that the numbers needed
to justify building it have not been published**, which no amount of building would have revealed.
