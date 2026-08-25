# T2 - What the effect is, with item 5 run first

Programme: flow (mechanical flow). Packet 9, task T2.
Written **after** `KILL-CONDITION.md` was sealed - sha256
`c62c13ab11236f1bef8733f24c9709b6ec8ff893463fb126eb0ad4163f05056a`, commit `8f3c0a9`.

**No synthesis and no recommendation.** Per strand: the cash flow, the item-5 answer, published
magnitudes with every column populated or explicitly unknown, the re-estimation record, and - for
every magnitude - **T1 section 6.1: is this a measurement of the position Walton would hold?**

**No deal data, no live spread, no screen.** Every figure is from a published document.

---

## 0. Instrument findings, recorded before any result

### 0.1 arXiv exact-phrase, controlled both ways in this packet

| query | entries |
|---|---|
| `all:"merger arbitrage"` | **2** |
| `all:"deal break" AND all:"merger"` | 0 |
| `all:"index effect" AND all:"S&P 500"` | 0 |
| `all:"zzqxwv impossible control phrase"` | **0** |

A real phrase returns 2; the impossible phrase returns 0. **The two zeros are licensed as arXiv
nulls and as nothing more** - finance literature is largely not on arXiv, so this is not a statement
about the field.

**Crossref was used to find papers and never to report an absence**, per the finding recorded in
`programmes/premia/PRIORS.md` section 0.1: a nonsense query returned `total-results` = 3,766,699.

### 0.2 Wiley is unreachable at this vantage - the S1 canonical paper could not be read in full

Mitchell & Pulvino (2001) is recorded by OpenAlex as **bronze open access** with exactly one
location: `onlinelibrary.wiley.com/doi/pdfdirect/10.1111/0022-1082.00401`.

| route | result |
|---|---|
| raw HTTP | `403`, 5,695 bytes of `text/html` |
| browser network stack | `403`, `Cf-Mitigated: challenge`, Cloudflare managed challenge page |
| OpenAlex `locations` | **one** location, the same blocked URL |

> **Per T1 section 5.3 this is could not establish on the full text, never "no evidence found".**
> The abstract was read and is quoted below. **The body was not**, and section S1.5 records exactly
> what that costs.

---

## S1 - Merger arbitrage

### S1.1 The mechanism, as a cash flow

| | |
|---|---|
| **who is forced** | holders of the target who will not or cannot bear deal risk to completion - index funds forced out on deletion, mandate-constrained holders, and holders who want cash now |
| **what they pay** | the residual discount of the target's price to the offer, from announcement to close |
| **who receives it** | whoever stands between announcement and completion holding the risk |
| **the payoff shape** | **capped gain, large loss.** The spread is the maximum; a break returns the target toward - and sometimes below - its pre-announcement price |
| **the position** | long target; in a stock deal, **short the acquirer** in the exchange ratio, which requires borrow |

### S1.2 Item 5, run first: what is the friction, and is it still there?

**The friction is documented and it is structural, not an access restriction.** Mitchell & Pulvino
(2001), *Journal of Finance*, abstract verbatim:

> "This paper analyzes **4,750 mergers from 1963 to 1998**... risk arbitrage returns are **positively
> correlated with market returns in severely depreciating markets but uncorrelated with market
> returns in flat and appreciating markets. This suggests that returns to risk arbitrage are similar
> to those obtained from selling uncovered index put options.** Using a contingent claims analysis
> that controls for the nonlinear relationship with market returns, and after controlling for
> transaction costs, we find that risk arbitrage generates **excess returns of four percent per
> year**."

**This is a different kind of answer from the three that preceded it.** Families 2, 4a and 4b each
found a *friction* - an access restriction, a capital constraint, a rule about who may sell. **Here
the payoff itself is a short option.** The compensation is for bearing a loss that arrives in severe
market declines, which is a risk somebody must hold rather than a barrier somebody erected.

Baker & Savasoglu (2002), *Journal of Financial Economics*, `10.1016/s0304-405x(02)00072-7`, is
titled **"Limited arbitrage in mergers and acquisitions"** and is the standard citation for the
capital-constraint half of the story. **Its abstract is not in Crossref and its full text was not
reached** - could not establish on its content, and it is cited here for its title and venue only.

> **"Is it still there?" is NOT established by anything read in this packet.** The friction's
> *existence* rests on a sample **closing in 1998**. Its *present* condition is a separate claim and
> section S1.5 records that no reachable source establishes it.

**And the disclosed bias applies here.** T1 section 0a recorded that I expected merger arb's
friction to be real and present. **The first half is confirmed by a source I could only read in
abstract; the second half is not confirmed at all.** Per the standing instruction, confirmation of a
disclosed prior takes the higher bar, and the higher bar is not met.

### S1.3 Published magnitudes

| # | figure | horizon | sample | universe | gross/net | dispersion | **the position Walton would hold?** | source |
|---|---|---|---|---|---|---|---|---|
| A | **+4% per year excess return** | annual | **1963-1998** | 4,750 US mergers | **net of transaction costs** per the abstract; the cost model was **not read** | **not read** | **COULD NOT ESTABLISH.** A risk-adjusted portfolio excess return from a contingent-claims analysis. Whether the portfolio rule, weighting, position count, borrow treatment and cost assumptions match a UK retail book **is in the body, which is unreachable** | Mitchell & Pulvino (2001), *J. Finance*, `10.1111/0022-1082.00401` |
| B | "the shrinking merger arbitrage spread" - **magnitude not read** | unknown | unknown | unknown | unknown | unknown | **not assessable** | Jetley & Ji (2010), *FAJ*, `10.2469/faj.v66.n2.3`. **Closed access, no OA location. Could not establish.** |
| C | Brier score 0.151 on **>400 large deals across 42 countries**, three-outcome forecast, **24% below calibrated market-implied probabilities** | per deal | out-of-sample, **published 2026-07** | large global deals | **not a return figure at all** | n/a | **NO.** A **forecast-accuracy benchmark**, not a position return. T1 section 6.1 rules it out on its face | Jajal, Mucha, Sweat, Pulman, Flanagan & Anderson, arXiv `2607.09921v1` |

> **Row A is the only return figure for S1 in this packet, and it fails T1 section 6.1 on
> reachability rather than on substance.** The distinction matters: the number may well be the right
> kind of number. **This packet cannot tell**, and T1 section 7 item 5 makes that could not
> establish rather than a pass.

**Row C is worth one line beyond its cell.** A 2026 paper reports beating *calibrated market-implied
deal probabilities* by 24% on Brier score using a finetuned language model over hundreds of pages of
deal documents. That is evidence about **who else is working on this problem now**, and it is the
only post-vantage evidence of any kind this packet found on S1.

### S1.4 The vantage line for S1

T1 section 5.1 fixes S1's line at **the effective date of the most recent published revision of the
US merger-review framework**, to be established in T3 from the agencies' own publications. **That
date is not asserted here.** What is already certain without it: **row A's sample closes in 1998**,
which precedes any candidate line by decades.

### S1.5 Post-vantage re-estimation - **none found**

- **Row A** is 1963-1998. **Row B** is 2010 and **unreadable**. **Row C** is 2026 and **not a return**.

> **No reachable source re-estimates the return to a held merger-arbitrage position on a sample
> closing after any plausible vantage line.** Per T1 section 5.1 that caps S1 at **could not
> establish** whatever row A's historical figure, and per T1 section 7 item 4 it is an instrument
> failure rather than a finding about the strategy.

**The asymmetry still applies (T1 section 5.2).** Row A's *adverse* content - that the payoff is a
short uncovered index put, correlated with severe market declines - **does not expire**. It is
evidence about the shape of this strategy under stress and is carried to T4 as such.

---

## S2 - Index-reconstitution flow

### S2.1 The mechanism, as a cash flow

| | |
|---|---|
| **who is forced** | index funds, which must hold the index and therefore must buy an addition and sell a deletion |
| **by what** | their own mandate, on a date and at a price the methodology determines |
| **what they pay** | price impact - buying into a demand shock they announced in advance |
| **who receives it** | whoever supplies the stock before the effective date and unwinds after |
| **the payoff shape** | **not a short option.** Bounded event exposure over days, with market risk over the holding window. **T1 section 1.0 therefore applies sections 1.1, 1.3, 4, 5 and 6 to S2 and not the break-specific tests** |

### S2.2 Item 5, run first: what is the friction, and is it still there?

**The friction was real, it is documented from 1986, and it is gone.**

Greenwood & Sammon, *The Disappearing Index Effect*, **Journal of Finance 2024**, `10.1111/jofi.13410`:

> "The abnormal return associated with a stock being added to the S&P 500 has **fallen from an
> average of 7.4% in the 1990s to less than 1% over the past decade. This has occurred despite a
> significant increase in the share of stock market assets linked to the index.** A similar pattern
> has occurred for index deletions, with large negative abnormal returns during the 1990s but an
> average return of only 0.1% between 2010 and 2020... **We document a similar decline in the index
> effect among other families of indices.**"

The origin is Shleifer (1986), *J. Finance*, `10.1111/j.1540-6261.1986.tb04518.x`: *"Since September,
1976, stocks newly included into the Standard and Poor's 500 Index have earned a significant
positive abnormal return at the announcement of the inclusion."*

**And here is the cause**, from the NBER working-paper version read in full (w30748, 83,052
characters), conclusion verbatim:

> "our assessment is that the declining index effect is driven by **primarily two factors: an
> increase in migrations over time from the S&P MidCap Index, and an overall increase in the
> market's ability to provide liquidity to index changes. We cannot rule out that a third factor,
> increased predictability of index changes, played some role.**"
>
> "when demand shocks become **regular and repeated**, competitive markets **adapt over time to
> minimize price impact**."

### S2.3 My prior was right on the answer and wrong on the mechanism

T1 section 0a disclosed that I expected index decay, and packet 9's own framing anticipated that
*"methodologies have changed specifically to reduce predictability."*

> **The string `methodolog` appears ZERO times in the paper's full text** - against in-file positive
> controls of `migration` 31, `liquidity` 15, `predictab` 10, `explanation` 20.
>
> **Methodology change is not among the five explanations the paper considers.** The two drivers are
> **index migration from the S&P MidCap index** - a compositional fact - and **an increase in the
> market's capacity to absorb the demand shock.** Increased predictability is a third factor they
> **cannot rule out**, not a driver.

**Right answer, wrong reason.** This project's own rule - *a conclusion can be right for the wrong
reason* - fires here on my own prior. The decay is confirmed; **the mechanism I expected is not the
mechanism the evidence supports**, and a later reader relying on "methodologies changed" would be
relying on something this packet found no support for.

**The item-5 answer for S2 is therefore sharper than my prior:** the friction was **the market's
capacity to absorb a predictable demand shock**, and it expired because **capacity grew**, not
because anybody changed a rule.

### S2.4 Published magnitudes

| # | figure | horizon | sample | universe | gross/net | **the position Walton would hold?** | source |
|---|---|---|---|---|---|---|---|
| D | additions **7.4% (1990s) -> under 1% (past decade)**; deletions large negative in the 1990s -> **+0.1% (2010-2020)**; **similar decline in other index families** | announcement-window abnormal return | **1980-2020** | S&P 500 additions and deletions | **gross.** An abnormal return, not a net position return | **NO.** T1 section 6.1 names "an event-study abnormal return" as **not** the position Walton would hold. A tradeable figure is this minus spread, commission and FX both ways on a single name | Greenwood & Sammon (2024), *J. Finance*, `10.1111/jofi.13410` |
| E | additions earn "a significant positive abnormal return at the announcement of the inclusion" | announcement window | **from September 1976** | S&P 500 additions | gross | **NO**, same reason; and the sample is five decades before any vantage line | Shleifer (1986), `10.1111/j.1540-6261.1986.tb04518.x` |
| F | Russell 1000 and 2000 inclusion and reconstitution effects **have declined** over the past ten years | not read | not read | Russell indices | not read | **not assessable** | Chinco & Sammon (2022), **as cited inside w30748.** Not retrieved; **could not establish** |

### S2.5 A version difference, recorded because the deletions figure changes sign

| | 1980s additions | 1990s additions | recent additions | deletions 2010-2020 |
|---|---|---|---|---|
| **NBER w30748 (Dec 2022)** | 3.4% | **7.6%** | 0.8% | **-0.6%** |
| **J. Finance (2024)** | not in abstract | **7.4%** | "less than 1%" | **+0.1%** |

> **The journal version governs.** The deletions figure **changes sign** between the working paper
> and the published paper - a material difference, not a rounding one. Quoting the working paper's
> `-0.6%` would make deletions look like a live short opportunity; the published `+0.1%` makes them
> nothing at all.

### S2.6 Post-vantage re-estimation

**Row D is the re-estimation**, published in a top journal in 2024 on a sample running to 2020, and
it is **adverse**. T1 section 5.2's asymmetry means it is admissible regardless of where T3 fixes
S2's vantage line.

**What is not established:** whether the effect has declined further, stabilised, or reversed since
2020. No source read covers it.

---

## 3. Both strands against T1 section 6.1, in one place

| magnitude | the position Walton would hold? |
|---|---|
| A - M&P +4%/yr | **could not establish** - the body is unreachable |
| B - Jetley & Ji | **could not establish** - closed access |
| C - LLM Brier score | **no** - a forecast-accuracy benchmark |
| D - Greenwood & Sammon | **no** - an event-study abnormal return |
| E - Shleifer | **no** - an event-study abnormal return |
| F - Chinco & Sammon | **not assessable** - not retrieved |

> **Not one magnitude in this packet passes T1 section 6.1.** Two fail on reachability, three fail on
> units, one was never retrieved.
>
> **This is the third consecutive family in which the units question failed before any threshold was
> reached.** Family 2: portfolio alphas where a per-event effect was needed. Family 4: a dated basis
> and a threshold convergence trade where a held carry position was needed. Family 3: event-study
> abnormal returns and a risk-adjusted portfolio alpha where a held position return is needed.

---

## 4. Sources

| source | identifier | how obtained | status |
|---|---|---|---|
| Mitchell & Pulvino, *Characteristics of Risk and Return in Risk Arbitrage* | `10.1111/0022-1082.00401`, *J. Finance* 2001 | Crossref record; **full text 403 at Wiley over raw HTTP and browser stack** | **abstract only - could not establish on the body** |
| Greenwood & Sammon, *The Disappearing Index Effect* | `10.1111/jofi.13410`, *J. Finance* 2024; NBER w30748 | NBER open PDF, 1,736,830 bytes, http 200; impossible WP number returned 404 | **read in full** (working paper); journal abstract read |
| Shleifer, *Do Demand Curves for Stocks Slope Down?* | `10.1111/j.1540-6261.1986.tb04518.x` | Crossref abstract | **abstract only** |
| Baker & Savasoglu, *Limited arbitrage in mergers and acquisitions* | `10.1016/s0304-405x(02)00072-7`, *JFE* 2002 | Crossref record, **no abstract, closed access** | **could not establish** |
| Jetley & Ji, *The Shrinking Merger Arbitrage Spread* | `10.2469/faj.v66.n2.3`, *FAJ* 2010 | Crossref record; OpenAlex `oa_status = closed` | **could not establish** |
| Mitchell & Pulvino, *Arbitrage Crashes and the Speed of Capital* | `10.2139/ssrn.1628261` (2010) | Crossref abstract | **abstract read; carried to T4** |
| Jajal et al., *Global Merger-Arbitrage Forecasting with Language Models* | arXiv `2607.09921v1` (2026-07-10) | arXiv metadata | **abstract read** |
| Chinco & Sammon (2022) | cited inside w30748 | not retrieved | **could not establish** |

**Cross-check discipline:** Mitchell & Pulvino's record was confirmed on **OpenAlex** (J. Finance,
2001, 727 citations, one OA location) after being found on **Crossref** - two endpoints, not two
calls to one. Greenwood & Sammon's journal abstract was cross-checked against the NBER working
paper's own abstract, **which is how the version difference in section S2.5 was found.**
