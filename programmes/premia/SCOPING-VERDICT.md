# T5 - The verdict against T1

Programme: premia (family 4, structural risk premia). Packet 8, task T5.

**Pre-registration:** `KILL-CONDITION.md`, sha256
`2a87dc4c7a34e6c3866fcd3f39ff8e0410506ad26330de85cd9100b7c27d2555`, commit `2d07ad7`, sealed
2026-08-24 before any source on funding, variance premia, venue mechanics or venue failure was read.
**Evidence:** `PRIORS.md` (`69a2723`), `MECHANICS.md` (`855e8f4`), `TAIL.md` (`317201d`).

**This document does not open the programme.** `ROADMAP.md` family 4's gate - *venue access
confirmed post-move, and capital deployable through the relocation without being needed elsewhere* -
is unchanged and is not addressed here.

---

## 1. The benchmark, documented as T1 required

T1 section 1.1 required `B` to be *"a sterling cash or near-cash rate available to a UK individual,
documented at T5 from a primary source, cited. Not zero."*

**Bank of England Bank Rate = 3.75%**, effective 18 December 2025, from the Bank's own
`boeapps/database/Bank-Rate.asp` (http 200; an impossible page on the same host returned 404).

A retail-accessible sterling cash rate sits at or slightly **below** Bank Rate after spread and
fees, so using the policy rate makes the hurdle **harder**, which is the safe direction.

> **T1's floor in absolute terms: a net total return of 8.75% p.a.** on continuously deployed
> capital - 5.00 pp of excess over 3.75%.

---

## 2. S1 - perpetual funding carry

### 2.1 Against T1 section 7, item by item

| # | T1 requirement | result |
|---|---|---|
| 1 | `E(K) >= 5.00 pp` over a documented benchmark | **not evaluable** - see 2.2 |
| 2 | `E(K) >= 3 x F/K` | **not evaluable** - `F` incomplete |
| 3 | `K_min` computed and `K_min / 0.15` reported | **not computable** |
| 4 | every venue passes section 3.1 exclusion | **not evaluated** - Binance unreachable |
| 5 | `L` established including the unhedged-leg component | **fails** |
| 6 | documented tail frequency at or below `p*/3` | **fails** |
| 7 | tail correlation established or excluded | **passes** - established, and adverse |
| 8 | post-2023, >= 24-month, both-signs sample with dispersion | **not evaluable for the strand** |
| 9 | every figure from a named, dated source read rather than summarised | **passes** |

### 2.2 Why item 1 is *not evaluable* rather than failed

**No published magnitude exists for the strand.** `PRIORS.md` section S1.4 established that the
two magnitudes in the literature are for **different instruments**:

- **Instrument B** (BIS WP 1087, ~7% p.a. average) is the **fixed-date futures basis**. The paper
  says so: *"we study fixed-date contracts with proper price convergence of spot and futures on the
  settlement date"*, and notes that *"perpetual ones are not guaranteed to converge to the spot
  price, since the contracts have no expiration date to strictly enforce arbitrage."*
- **Instrument A** (He et al.) is a **threshold convergence trade** - open past a cost-adjusted
  bound, close at zero - not a held funding-carry position.
- **Row C** (Christin et al.) could not be located. **Could not establish**, per T1 section 4.4.

Substituting A or B for S1 would be exactly the move family 2 refused when it declined to net a
portfolio alpha against a per-event hurdle. **This is family 2's route 1 - units - a second time.**

### 2.3 What the closest analogue does say, reported in full including the cells that clear

Instrument A, He et al. Table 7, high trading-cost tier, **excess returns**, fee-only cost model:

| cell | E | vs the 5.00 pp floor |
|---|---|---|
| BTC 2022 (full year) | **0.28%** | 6% of the bar; short by 4.72 pp |
| BTC 2023 (full year) | **1.11%** | **22% of the bar; short by 3.89 pp** |
| ETH 2023 | 1.81% | 36% of the bar |
| DOGE 2023 | 0.68% | 14% of the bar |
| ADA 2023 | 1.63% | 33% of the bar |
| **BNB 2023** | **6.27%** | **125% of the bar - clears it** |
| **BTC pooled 2020-2024** | **6.38%** | **128% of the bar - clears it** |

**Two cells clear the floor and neither can carry a verdict.**

- **The pooled BTC figure is mixed-vantage.** T1 section 4.1 sets the family floor at 2023-01-01.
  The pooled number is 2020 (8.29%) and 2021 (14.81%) carrying 2022 (0.28%) and 2023 (1.11%), and
  He et al. name the break themselves: *"Since the year 2022... There seems to be a structural
  break... significantly lower annualized returns."* **T1's vantage rule exists to stop exactly
  this substitution.**
- **BNB 2023 is the venue's own exchange token.** A carry book whose underlying is the token of
  the venue holding the margin is not diversified against venue failure - it is doubly exposed to
  it. And the figure is fee-only, at 18.93% active time, on a single altcoin.

**On the liquid assets, post-vantage, the analogue reaches roughly a fifth of T1's floor.**

### 2.4 `p*`, as T1 section 3.2 requires T5 to state it

> **`p*` cannot be computed for S1.** `p* = E / L`, and neither `E` (2.2) nor `L` (T1 section 3.3,
> the unhedged-leg component) is established. T5 states that rather than producing a number.

**An illustration on the analogue, flagged as such.** *Granting* S1 instrument A's BTC 2023 excess
of 1.11% - which it is not entitled to, and which already fails the floor:

| assumed `L` | `p*` | required bound `p*/3` |
|---|---|---|
| 1.00 (same-venue book, total loss) | 1 in **90** years | 1 in **270** years |
| 0.25 (T1 section 2.1's material-loss floor) | 1 in **22.5** years | 1 in **68** years |

This is an **inversion, not an expected-value calculation** - it consumes the carry side only, and
T1 section 3.2 permits it explicitly. T1 section 4.1's vantage window is **3.6 years long**. **No
evidence base bounded by a 3.6-year window can place a frequency below one in 68 years, let alone
one in 270.** The inversion does not decide S1; it shows that even the generous reading leaves a
bar the evidence could not clear.

### 2.5 Verdict

> ## S1: COULD NOT ESTABLISH

**Five independent routes**, so no single new source resolves them:

1. **Units.** No published magnitude for the strand. The two that exist are other instruments.
2. **Fixed costs.** No venue read publishes a withdrawal figure - Hyperliquid says only *"there may
   be small gas fees."* `F` is incomplete, so `K_min` and therefore `K_min / 0.15` cannot be
   computed. T1 section 1.4(ii).
3. **The hedge leg is not costed** by any source read. T1 section 1.0a.
4. **`L` is not established**, including the unhedged-leg component. T1 section 3.3.
5. **Tail frequency is not bounded.** T1 section 5 item 2. See section 5 below for why this one is
   different from the other four.

---

## 3. S2a - equity index variance risk premium

### 3.1 The magnitude was measured, and it is approximately zero

Dew-Becker & Giglio, Chicago Fed WP 2025-17, 4 September 2025, read in full:

> "**over the past 15 years, option alphas have become indistinguishable from zero**"
>
> "the alpha of delta-hedged options has gone to zero... the CAPM alpha of the variance risk premium
> has shrunk towards zero"
>
> "the overall cumulative return on traded puts is **zero between March, 2009 and the end of the
> sample in December, 2022**" - and over ten-year windows the traded-put return *"actually turned
> positive at the end of the sample"*, i.e. selling them lost money.

The delta-hedged option return **is** the tradeable form of the variance risk premium
(Bakshi & Kapadia 2003; the paper makes the identification explicitly).

**`E` is approximately 0 pp against a floor of 5.00 pp.** T1 section 7 item 1 fails, and
T1 section 7 states: *"Missing any of 1-4 is a KILL."*

### 3.2 The vantage question, answered by T1's own asymmetry

The sample closes **December 2022**, before T1's 2023-01-01 floor. Under a symmetric vantage rule
this finding would be excluded. **T1 section 4.3 makes it asymmetric:** *"Adverse evidence does not
expire... a symmetric vantage rule is survivorship bias with a methodological justification
attached."*

The finding is adverse. **It is admissible, and the rule written before the evidence is what makes
it admissible.**

### 3.3 Verdict

> ## S2a: KILL

**Not could-not-establish.** The instrument did not fail. A magnitude was measured, over a
century of synthetic options and fifteen years of traded ones, by a named central-bank working
paper read in full - and the magnitude is zero.

---

## 4. S2b - Bitcoin variance risk premium

| T1 requirement | result |
|---|---|
| a return that can be netted against a threshold | **fails.** BVRP = 0.14 is a difference of **annualised variances** (risk-neutral 0.72, physical 0.58). Converting it needs the instrument, the notional convention, **the venue's margin against a short-variance position**, and a cost model. None of the four is published |
| post-vantage evidence | **fails.** Sample closes December 2022. And `www.deribit.com` now titles itself **"Deribit by Coinbase"** - a change of ownership, which T1 section 4.2 makes a per-venue vantage reset. **The evidence describes a different venue** |
| venue mechanics for the strand | **fails.** Deribit's fee schedule, margin rules and socialised-loss trigger are behind a single SPA shell that returns byte-identical content for every path |

> ## S2b: COULD NOT ESTABLISH

**Direction of the missing evidence: down.** Two things *are* known and both point the wrong way -
the unit mismatch conceals the cost and margin side entirely, and Almeida et al. report the BVRP is
**lower in high-volatility regimes**, i.e. the compensation shrinks exactly as the risk being sold
grows.

---

## 5. Which direction the missing evidence points - T1 section 8

T1 section 8: *"If the unestablished items are all on the cost or risk side, the verdict is agnostic
while the evidence is not, and T5 must write that where a later reader cannot miss it."*

> **Every unestablished item in this packet is on the cost or risk side.** Fixed monetary costs.
> The hedge leg. Loss-given-failure. Tail frequency. Deribit's margin and fees. Binance's
> mechanisms. **Not one is on the return side.** Cost and risk move a residual one way only.
>
> **And the one measured thing on the return side failed.** Instrument A's post-vantage BTC year is
> 1.11% against a 5.00 pp floor.
>
> **So the verdict is agnostic while the evidence is not.** This entry must never be read later as
> "promising, needs more work." It is: *the evidence needed to decide does not exist in this
> packet, what is missing points down, and what was measured came in at a fifth of the bar.*

### 5.1 One item is different, and T5 must not blur it

`TAIL.md` section 6: **the tail's frequency is not unknowable. It is unretrieved.**

- Hyperliquid labels ADL fills in its **public REST API** - Campbell et al. reconstructed the
  October 2025 event from it.
- Deribit returns `socialized`, `session_tax_rate` and `session_bankruptcy` per settlement on a
  **public, unauthenticated endpoint**, with paging.

**Neither was called, because packet 8 forbids data pulls.** T5 therefore records the frequency as
**out of scope, not unknowable** - and it is the cheapest open question here, exactly as McLean &
Pontiff's Internet Appendix was in packet 7.

---

## 6. Carried into T5 verbatim, as T1 section 3.4 required

T1 section 3.4, sealed before any venue documentation was read:

> "If a venue's own documentation shows that auto-deleveraging can close a profitable,
> fully-margined position without the holder's consent, that is a structural finding carried into
> T5 regardless of frequency... A delta-neutral book whose hedge can be removed by the venue at the
> moment of maximum stress is not delta-neutral. It is delta-neutral until it matters."

**It fired at both venues whose ADL ordering is documented:**

- **Hyperliquid:** *"the users on the opposite side of the position are ranked by unrealized pnl
  and leverage used... Those traders' positions are closed at the previous mark price against the
  now underwater user."*
- **OKX:** *"5 = highest priority (first in queue if the insurance fund is depleted). **Priority
  increases with higher unrealized profit.**"*

**And the pre-commitment obliges the counter-finding too.** `TAIL.md` section 3.3: in the one
forensic study of the largest documented ADL event, *"delevered short positions were ex post
profitable since they were bought in at relative market lows. This challenges the notion of ADL as
a loss socialization mechanism"* - though outcomes were heterogeneous, queue position mattered, the
source is an X thread rather than a paper, and its authorship overlaps the paper reporting it.

> **The mechanism's documented direction is adverse. Its one measured realisation was not.** Both
> are carried, because T1 said "regardless of frequency" and a rule that only carries the
> convenient half is not a rule.

---

## 7. The family

T1 section 1.0: *"The family survives only if at least one strand survives on its own numbers.
Averaging is prohibited."*

| strand | verdict |
|---|---|
| S1 - perpetual funding carry | **could not establish** |
| S2a - equity index variance risk premium | **KILL** |
| S2b - Bitcoin variance risk premium | **could not establish** |

> ## Family 4 does not survive scoping.
>
> **No strand survives, and the only strand whose magnitude was actually measurable was killed.**

### 7.1 What T4 was expected to do, and what it did

Packet 8: *"T4 decides this packet."*

**It did not.** The carry side failed first. `PRIORS.md` established that the post-vantage magnitude
for S1's closest analogue reaches about a fifth of T1's floor on the liquid assets, and that S2a's
magnitude is zero. **The tail never became load-bearing**, because there was no carry left for an
unquantified tail to disqualify.

T1's new pre-commitment - *"a carry figure computed without a quantified tail is not a result"* -
was written to stop a **large** carry surviving on an unexamined tail. **That clause never had to
fire.** It is recorded as untested rather than as vindicated.

### 7.2 What this document does not say

Packet 8's closing note: *"the scoping can return survives and the answer still be not now."* This
document returns neither. **It makes no statement about whether Walton could, should, or may access
any venue** - T3 recorded what venues state and this packet determined nothing.

---

## 8. The item-5 answer, which is the part that transfers

| strand | why it survived publication - one sentence |
|---|---|
| **S1** | It persists because arbitrage capital is constrained by regulation and margin, and because the arbitrageur can be forced out of the position before convergence - *"the limited deployment of arbitrage capital because of regulatory and margin frictions"* (BIS WP 1087). |
| **S2a** | **It did not persist.** It was an intermediary friction - retail could not sell options, so price was set by the highest-demand buyer - and it decayed to zero as the friction eased; synthetic options *"never, over the last 100 years, had negative alpha"* (Dew-Becker & Giglio). |
| **S2b** | **Not established.** No source read explains why a Bitcoin variance premium would persist, and no post-vantage estimate of it exists. |

> **Three families, one answer.** Family 2: it survived because it was uneconomic to arbitrage.
> S1: it survives because arbitrage capital is constrained. S2a: it was a restriction on who could
> supply, and it ended when the restriction did.
>
> **The premium was the friction, in every case where the answer is known.** Packet 8 expected
> *"someone must warehouse a risk nobody wants"* and predicted that finding access friction instead
> would be family 2's result again. **It is, twice.**
>
> This is the finding that transfers to family 3, and it sharpens ROADMAP screen item 5 from a
> question about published anomalies into a question about **any** documented edge: *what is the
> friction, and is it still there?*
