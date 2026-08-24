# T2 - What the premium is, and why it persists

Programme: premia (structural risk premia). Packet 8, task T2.
Written **after** `KILL-CONDITION.md` was sealed - sha256
`2a87dc4c7a34e6c3866fcd3f39ff8e0410506ad26330de85cd9100b7c27d2555`, commit `2d07ad7`.

**No synthesis and no recommendation.** Per strand: the cash flow, the item-5 answer, the
magnitudes with every column populated or explicitly unknown, and the re-estimation record.
The comparison against T1 happens in T5, not here.

**Nothing in this document was obtained from an account, an API key, or a live market feed.**
Every figure is from a published document, read in full rather than summarised.

---

## 0. Instrument findings, recorded before any result

Three, because each would have corrupted a null or a date if it had gone unnoticed.

### 0.1 Crossref's result count is not a null instrument

`query.bibliographic` is fuzzy relevance ranking, not matching. The deliberately impossible
query `zzqxwv nonexistent term control alpha` returned **`total-results` = 3,766,699** and six
plausible-looking rows.

> **A Crossref result count may never be cited as evidence that a literature does not exist.**
> Crossref is used here to *find* papers and never to report an absence.

### 0.2 arXiv exact-phrase search IS a null instrument - controlled both ways

| query | entries |
|---|---|
| `all:"fundamentals of perpetual futures"` | 1 |
| `all:"primer on perpetuals"` | 1 |
| `all:"zzqxwv nonexistent perpetual phrase"` | **0** |

Real phrases return exactly one; the impossible phrase returns zero. The paired control holds,
so an arXiv null is reportable **as an arXiv null** - never as a statement about the literature.

### 0.3 The arXiv Atom feed carries a feed-level `<updated>` equal to the query time

Parsing the **first** `<updated>` in the response returned `2026-08-24T09:25:11Z` for He et al. -
minutes old. The entry-level field is `2024-08-21T21:37:38Z`.

> **Every paper would have looked post-vantage.** The vantage rule would have passed everything
> it exists to stop. Fixed by extracting `<updated>` from inside `<entry>`.
>
> Same shape as false positive #7 and the unpaired change-detection control: **the field that is
> easiest to read is not the field that means what you want.**

---

## S1 - Perpetual funding carry

### S1.1 The mechanism, as a cash flow

| | |
|---|---|
| **who pays** | the long side of the perpetual contract |
| **to whom** | the short side, directly - the venue is not the counterparty to the payment |
| **how often** | every 8 hours on Binance; interval is venue-specific (T3) |
| **on what condition** | sign and size track the perpetual-minus-spot gap; positive gap means longs pay shorts, negative means the reverse |
| **what the payer buys** | leveraged exposure to the underlying **without rollover and without direct ownership** |
| **what enforces it** | nothing terminal. **Unlike fixed-maturity futures, perpetuals are not guaranteed to converge to spot** - there is no expiry to force it (He et al., abstract and section 3) |

That last row is the mechanism's defining feature and it separates S1 from every dated-basis
result quoted below. A dated basis trade is self-liquidating at expiry; a perpetual carry book
must exit through the market, always.

### S1.2 Item 5, run first: why it survived publication

**The answer is limits to arbitrage, not risk warehousing - and it is stated by the authors.**

Schmeling, Schrimpf & Todorov, *Crypto carry* (BIS WP 1087, April 2023 rev. October 2025;
Management Science 2026, DOI `10.1287/mnsc.2024.05069`), abstract, verbatim:

> "We trace the large and volatile crypto carry to the interplay of two main forces: **(i) demand
> from smaller, trend-chasing investors seeking leveraged exposure** and **(ii) the limited
> deployment of arbitrage capital because of regulatory and margin frictions.** Our findings
> highlight how **structural limits to arbitrage** - especially severe in the case of crypto - can
> amplify price inefficiencies across financial markets."

The 2022 working-paper vintage adds the risk-bearing half explicitly:

> "the relative scarcity of 'arbitrage' capital taking the other side through a cash and carry
> position. **Engaging in the latter is risky due to spikes in margins and liquidations amid
> drawdowns.**"

**So it is both, and the risk half is not the risk the packet expected.** The arbitrageur is not
warehousing a risk nobody wants in the insurance sense. The arbitrageur is warehousing **the risk
of being forced out of the position**, which is a funding-liquidity risk rather than a fundamental
one.

> **This is family 2's answer with a different mechanism.** Family 2: *it survived because it was
> uneconomic to arbitrage.* S1: *it survives because arbitrage capital is constrained by
> regulation and margin, and because the arbitrageur can be liquidated before convergence.*

**One version-difference, recorded because quoting the wrong vintage would flatter the strand.**
The 2022 SSRN abstract says carry reaches "**up to 60% p.a.**"; the 2021 SSRN and 2026 Management
Science abstracts say "**sometimes exceeding 40% per annum**". The journal version governs. And
neither number is the average - see S1.4.

### S1.3 What the payer is protected from that Walton would not be

The payer buys leveraged upside with no rollover and no custody of the underlying. The receiver -
Walton, short the perpetual and long the spot - is exposed to four things the payer is not:

1. **Forced liquidation of the short leg, timed by the carry itself.** Crypto carry, section on
   liquidations: *"assuming a leverage of 10 (which is significantly lower than the maximum
   leverage offered by most exchanges), **the futures leg of the strategy would have been
   liquidated in over half of the months in our sample**"*; and *"a rise in standardized carry by
   10% predicts a **22% increase in total sell liquidations**"*, where sell liquidations are the
   closing of **short** futures positions - the carry trader's leg.
2. **No convergence anchor.** The perpetual has no expiry, so the gap need never close.
3. **Venue custody of both legs' margin**, with no deposit protection.
4. **Cross-venue correlation of the carry itself** - see S1.5.

### S1.4 Published magnitudes

**No published figure was found for a continuously-held perpetual funding-carry position.** Both
magnitudes below are for **related but different instruments**, and are recorded as such.

| # | instrument | effect | horizon | sample | venue | gross/net | dispersion | source |
|---|---|---|---|---|---|---|---|---|
| A | **Threshold convergence trade** on the perp-spot deviation (open past a cost-adjusted bound, close at 0) - **not** a held funding-carry position | **+6.38% annualised excess return**, SR 1.80, **max drawdown -4.43%**, **active 20.06% of hours**, mean position 134.9 h | continuous, 36,578 hourly obs | **Jan 2020 - Mar 2024** | Binance, BTC | **Net of exchange fees only** at their "high" tier: **6.75 bps spot / 1.44 bps futures**. **No bid-ask, no slippage, no FX, no withdrawal cost.** | std dev 3.55%; full by-year table below | He, Manela, Ross & von Wachter, *Fundamentals of Perpetual Futures*, arXiv `2212.06888v6` (v6 2024-08-21), Table 7 |
| B | **Fixed-date futures basis** (dated contract minus spot), not perpetual | **~7% p.a. average**, "frequently exceeding 20%", spikes past 40%, and **below -50%** during the FTX collapse | to contract maturity | **Apr 2019 - Jul 2024** (some tables from Feb 2018) | OKEx, CME and others; BTC and ETH | **Gross.** Costs are discussed only to argue they are too small to *explain* the carry, never netted to produce a capturable return | "significant variation over time"; no interval published for the mean | Schmeling, Schrimpf & Todorov, BIS WP 1087 / Management Science 2026 |
| C | Short-perpetual carry "generates high Sharpe ratios" | **UNKNOWN - no figure read** | unknown | unknown | unknown | unknown | unknown | Christin, Routledge, Soska & Zetlin-Jones (2022), *The crypto carry trade*, Working Paper - **cited by BIS WP 1087; not located as a retrievable document in this packet. COULD NOT ESTABLISH, not "no evidence"** |

**Instrument A's cost model is a fee schedule, not an effective cost.** 6.75 bps spot and 1.44 bps
futures are venue fee-tier numbers. With a mean holding period of 134.9 hours and the position
opening and closing on a threshold, the round trip is paid repeatedly, and bid-ask and slippage
are absent from the model. Under this project's own rule - *measure the price you could have
transacted at* - A is an upper bound on what was capturable.

**Instrument A's return is per unit of capital committed for the whole period, not per active
hour.** The authors annualise by the Lucca & Moench (2015) convention: *"We first calculate the
mean and standard deviation of our trading strategy **during the time it is active**. Next, we
scale by the number of periods the strategy is active in a year."* The capital is idle and
unremunerated for the other **79.94%** of the year while remaining at the venue and exposed to it.

### S1.5 Post-publication and post-regime re-estimation - **it exists, and it is adverse**

**He et al. identify the break themselves**, verbatim:

> "**Since the year 2022, the deviation between the futures and the spot has become smaller and
> less volatile. There seems to be a structural break.** We indeed find the trading strategy takes
> less active positions and **significantly lower annualized returns**."

Their Table 7 (unrestricted strategy, **high** trading-cost tier), read from the paper:

| year | BTC ret% | ETH ret% | BNB ret% | DOGE ret% | ADA ret% | BTC SR | BTC active% | obs |
|---|---|---|---|---|---|---|---|---|
| 2020 | 8.29 | 17.12 | 31.23 | 59.81 | 21.35 | 2.26 | 28.66 | 8,616 |
| 2021 | 14.81 | 18.08 | 33.13 | 53.43 | 24.19 | 2.39 | 34.43 | 8,760 |
| **2022** | **0.28** | **1.19** | 5.01 | 1.53 | 3.05 | 0.70 | 9.21 | 8,760 |
| **2023** | **1.11** | **1.81** | 6.27 | 0.68 | 1.63 | 1.32 | 7.68 | 8,760 |
| 2024 *(stub)* | 11.97 | 10.98 | 15.11 | 6.78 | 5.02 | 11.52 | 22.18 | **1,682** |
| **All** | **6.38** | 9.59 | 18.41 | 23.31 | 12.03 | 1.80 | 20.06 | 36,578 |

*Internal consistency check: the paper's text states "an SR of 1.80 for BTC" under high trading
costs, and the All/BTC cell reads 1.80. Return/volatility = 6.38/3.55 = 1.80. Both hold.*

**Three observations, no synthesis:**

- The pooled **6.38%** is a mixed-vantage figure. **Two of its four-and-a-quarter years supply
  almost all of it**, and both are pre-2022.
- The only two **full** post-break years are **2022 (0.28%)** and **2023 (1.11%)** for BTC.
- The **2024 figure covers 1,682 hours - roughly ten weeks** - and that window contains the spot
  BTC ETF launch, which BIS WP 1087 uses as its causal experiment on the arbitrage friction. It is
  a stub containing a one-off event, and T1 section 1.2 requires 24 months containing both signs.

### S1.6 Cross-venue correlation of the carry

Two independent sources, different data and method, agree:

- BIS WP 1087: *"carry is **highly correlated across nonregulated exchanges with correlation
  coefficients in excess of 90%**"*, with CME the least correlated - which they read as evidence
  of segmentation.
- He et al.: *"**Funding rates tend to be similar across exchanges due to cross-exchange arbitrage
  activity, but can diverge during extreme liquidity episodes.**"*

### S1.7 The FTX episode, from the S1 sources rather than an aggregator

He et al., on the November 2022 collapse:

> "Bitcoin futures prices were substantially higher than spot prices **at FTX**, but the opposite
> was true on other exchanges. This pattern is consistent with **FTX investors liquidating their
> short futures positions quickly**, either voluntarily to reduce their exposure to the failing
> exchange, or **involuntarily as the exchange liquidated their underfunded positions**."

And, from the same paper's figure note: *"The FTX collapse led to significant negative funding
rates on solvent exchanges. Vice versa on the insolvent FTX."*

**Recorded, not interpreted:** the leg that was liquidated at the failing venue was the **short
futures** leg, which is the carry receiver's leg. T4 decides what this means.

### S1.8 A positive-controlled null on both S1 sources

Term counts in the full extracted text of both papers:

| term | He et al. | BIS WP 1087 |
|---|---|---|
| insurance fund | **0** | **0** |
| socialised / socialized | **0** | **0** |
| clawback | **0** | **0** |
| auto-deleverag / deleverag | **0** | **0** |
| default | **0** | **0** |
| custody | **0** | **0** |
| counterparty | 1 | **0** |
| *positive control:* arbitrage | 210 | 56 |
| *positive control:* funding | 123 | 8 |
| *positive control:* spot | 202 | 119 |

> **The two papers that establish this premium's magnitude do not mention its loss backstop at
> all.** The controls license the null: the search works and the files are intact.
>
> This is a statement about the literature, not about the venues. What the venues publish is T3.

---

## S2 - Variance risk premium

The strand splits, because the evidence does. **S2a** is the canonical equity-index VRP; **S2b**
is the Bitcoin VRP. They are recorded separately and neither transfers to the other.

### S2.1 The mechanism, as a cash flow

| | |
|---|---|
| **who pays** | the buyer of options, or the fixed leg of a variance swap |
| **to whom** | the seller / the floating leg |
| **how often** | at expiry, or continuously through the delta hedge's rebalancing P&L |
| **on what condition** | the seller keeps the wedge whenever **realised** variance comes in below **implied** |
| **what the payer buys** | protection against a variance outcome worse than the one priced |
| **the tradeable form** | the **delta-hedged** option return. Dew-Becker & Giglio: *"the difference between the returns on the traded and synthetic put returns is exactly the return on a delta-hedged put, which is a version of the variance risk premium (Bakshi and Kapadia (2003))"* |

### S2.2 Item 5, run first: why it survived publication

**It did not.** The strand's own canonical literature reports that it has gone.

Dew-Becker & Giglio, *The Decline of the Variance Risk Premium: Evidence from Traded and Synthetic
Options*, Federal Reserve Bank of Chicago WP 2025-17, 4 September 2025, DOI `10.21033/wp-2025-17`.
Abstract, verbatim:

> "Equity index options historically displayed sharply negative returns and CAPM alphas. This
> could reflect investor risk preferences or intermediary frictions. **We document that over the
> past 15 years, option alphas have become indistinguishable from zero.** We also introduce
> synthetic options, that, under some conditions, reflect risk preferences of the average equity
> investor, independent of option-market frictions. **Synthetic options never, over the last 100
> years, had negative alpha, indicating that equity investors never required high compensation for
> market downturns.** An intermediary-based model explains the patterns in both synthetic and
> traded options, including the recent decline in the variance risk premium."

And on the cause, from the body:

> "a **decline in trading frictions** can explain the decline in option overpricing. Intuitively...
> when **retail investors are unable to sell options - the model's core friction** - the
> equilibrium price of options will be driven by the investors with the greatest demand. But as
> the frictions decline, overpricing will also, **because the investors willing to supply options
> become free to do so.**"

> **The item-5 answer for S2a is that the premium was an access friction and not a risk premium,
> and the friction has eased.** The synthetic-option result is the sharp form of it: over a
> century, the *average equity investor* never required compensation for downturns. The
> compensation was paid to whoever was permitted to supply the option, not to whoever bore the
> risk.
>
> **That is family 2's answer for the third time in this project**, and the second time in this
> packet. In family 2 the friction was the cost of trading illiquid small caps. In S1 it is
> regulatory and margin constraints on arbitrage capital. Here it is a restriction on who may sell.

### S2.3 What the payer is protected from that Walton would not be

On the synthetic-option evidence, the honest answer is **apparently nothing, for the equity case** -
over 100 years the average equity investor did not pay for downside protection above its actuarial
cost. The seller was collecting an intermediation rent, and rents end when entry opens.

For the crypto case (S2b) this question is **not answered by any source read in this packet**.

### S2.4 Published magnitudes

| # | strand | effect | horizon | sample | venue | gross/net | dispersion | source |
|---|---|---|---|---|---|---|---|---|
| D | **S2a - equity index VRP** | **Alpha indistinguishable from zero since ~2010.** Cumulative return on traded puts **zero between March 2009 and December 2022**; over ten-year windows the traded-put return **turned positive at the end of the sample** (i.e. selling them lost money). Delta-hedged put and straddle alphas "approximately zero since 2010" | monthly options | traded options to **Dec 2022**; synthetic options back to **1926** | US equity index options | alphas, so net of the modelled hedge but not of an execution cost model | "confidence bands that are economically narrow"; full-sample information-ratio lower bound **-0.2** for synthetic options | Dew-Becker & Giglio, Chicago Fed WP 2025-17 |
| E | **S2b - Bitcoin VRP** | **BVRP = 0.14 in annualised variance units** (risk-neutral variance 0.72 minus physical 0.58; i.e. implied vol ~85% against realised ~76%). Bitcoin premium (first moment) 66% p.a. | one month | **Jul 2017 - Dec 2022** | **Deribit** | **Neither.** It is a moment wedge, not a position return - see the note below | conditional estimates by regime reported; **no interval on the unconditional 0.14 was read** | Almeida, Grith, Miftachov & Wang, *Risk Premia in the Bitcoin Market*, arXiv `2410.15195v2` (v2 2025-08-01) |

> **Row E's 0.14 is not a return and must not be netted against a return threshold.** It is a
> difference of annualised variances. Converting it to a return on deployed capital requires the
> instrument (variance swap or delta-hedged straddle), the notional convention, **the margin the
> venue would require against a short-variance position**, and an execution cost model. **None of
> the four is in the paper.**
>
> This is family 2's route 1 in a new costume. There the strands reported portfolio alphas where a
> per-event effect was needed. Here the strand reports a moment wedge where a return on capital is
> needed. **Same failure, different units.**

**One vantage failure inside row E's own comparison.** Almeida et al. benchmark the Bitcoin VRP
against the S&P 500 VRP of *"approximately 2%, according to Bollerslev, Tauchen, and Zhou
(2009)"*. Row D documents that the equity VRP's tradeable alpha went to zero after roughly 2010.
**The comparison uses a pre-decline vintage of the number it compares against**, which makes the
crypto figure look better relative to equity than a current comparison would. Recorded; not
adjusted, because adjusting it would require a computation this packet is forbidden to make.

### S2.5 Regime dependence - the direction is adverse

Almeida et al., abstract: *"The **low-volatility regime** implies a relatively high share of BP
attributable to positive returns and a **high** Bitcoin Variance Risk Premium (BVRP). In
**high-volatility** states... the **BVRP is lower**."*

**Recorded, not interpreted:** the compensation for selling variance is largest when variance is
lowest, and smallest when variance is highest. T4 decides what that means for a seller.

### S2.6 Post-publication and post-regime re-estimation

- **S2a: yes, and it is the finding.** Row D *is* the re-estimation, and it is a peer-reviewable
  central-bank working paper dated September 2025 documenting decay to zero.
- **S2b: none found.** The Bitcoin VRP evidence read here ends **December 2022**. No post-2023
  re-estimation of the Bitcoin variance risk premium was located. Per T1 section 4.4 this is
  recorded as **could not establish on that item**, and the search that produced it is controlled
  below rather than reported as an absence.

### S2.7 The S2 search, with its controls

| query (arXiv exact phrase, the controlled index) | entries |
|---|---|
| `"variance risk premium"` AND `"cryptocurrency"` | **0** |
| `"variance risk premium"` AND `"bitcoin"` - *same query form, positive control* | 1 |
| `"zzqxwv impossible variance phrase"` - *impossible control* | 0 |

The same AND-form returns 1 for one term and 0 for the other, and the impossible phrase returns 0.
**The null is licensed for arXiv and for arXiv only.** Finance literature is largely not on arXiv,
so this is not a statement about the field. Crossref was swept for the same strand and surfaced
rows D and E plus older work, but per section 0.1 its counts carry no null.

---

## Both strands close on the same date, and it is the wrong side of the line

| strand | primary evidence | sample closes |
|---|---|---|
| S1, instrument A | He et al. | 2024-03-11 *(last full year 2023)* |
| S1, instrument B | BIS WP 1087 | 2024-07 |
| S2a, row D | Dew-Becker & Giglio | **2022-12** |
| S2b, row E | Almeida et al. | **2022-12** |

T1 section 4.1 sets the family vantage floor at **2023-01-01**, and T1 section 4.3 makes it
**asymmetric**: favourable evidence expires, adverse evidence does not.

**Every S2 magnitude read in this packet closes before that line. Every S2 finding that survives
the line is adverse** - the decline in row D, and the absence of any post-2023 Bitcoin
re-estimation. That is the asymmetry doing the work it was written for, on the first document that
faced it.

S1 straddles the line, and its post-line years are in the table at S1.5. No synthesis here.

---

## Sources, all read in full rather than summarised

| source | identifier | how obtained | status |
|---|---|---|---|
| Schmeling, Schrimpf & Todorov, *Crypto carry* | BIS WP 1087, Apr 2023 rev. Oct 2025; Management Science 2026, DOI `10.1287/mnsc.2024.05069` | BIS open PDF, 643,650 bytes, http 200; impossible working-paper number returned 404 | **read in full** |
| He, Manela, Ross & von Wachter, *Fundamentals of Perpetual Futures* | arXiv `2212.06888v6`, v6 dated 2024-08-21 | arXiv PDF, 5,236,156 bytes, http 200; impossible version `v99` returned 404 | **read in full** |
| Dew-Becker & Giglio, *The Decline of the Variance Risk Premium* | Chicago Fed WP 2025-17, DOI `10.21033/wp-2025-17` | DOI resolved to chicagofed.org PDF, 5,578,265 bytes, http 200; impossible WP number returned 404 | **read in full** |
| Almeida, Grith, Miftachov & Wang, *Risk Premia in the Bitcoin Market* | arXiv `2410.15195v2`, v2 dated 2025-08-01 | arXiv PDF, 1,306,580 bytes, http 200 | **read in full** |
| Christin, Routledge, Soska & Zetlin-Jones, *The crypto carry trade* | Working Paper, 2022; cited by BIS WP 1087 | **not located** | **could not establish** |

**Two endpoints were rate-limited at this vantage** and are recorded as a vantage fact rather than
an absence: OpenAlex returned `429 Rate limit exceeded` on anonymous search (single-record DOI
lookups succeeded, and were used for the cross-check of Management Science), and Semantic Scholar
returned `429` requesting an API key. **A 429 is produced by a layer and is not the resource's
status.**

**Cross-check discipline:** the *Crypto carry* record was confirmed on **OpenAlex** (title,
authors, Management Science, closed access) after being found on **Crossref** - two endpoints, not
two calls to one. The He et al. Table 7 figures were cross-checked against the paper's own prose
claim of SR 1.80 and against the identity return/volatility = Sharpe.
