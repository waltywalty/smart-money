# T4 - The break distribution, and the honest limit of scoping it

Programme: flow. Packet 9, task T4. Written after T1 was sealed (sha256 `c62c13ab...`, commit
`8f3c0a9`), T2 (`91ecdae`) and T3 (`a9f1584`).

**Four categories kept separate throughout, as packet 9 requires: documented, inferred from
incidents, unretrieved, and unknowable.** The third and fourth are the ones packet 8's correction
exists to keep apart.

**No expected-value calculation appears here.**

---

## 0. The instrument finding of this packet: the vantage is class-blocked

Every block below was established with a **paired control** - the same host, an impossible path.

| host class | example | real | control | verdict |
|---|---|---|---|---|
| government API | federalregister.gov | count 76 | count **0** | **reachable, null-capable** |
| government depository | govinfo.gov | `200` `application/pdf` | `200` **`text/html`** | **reachable**, content-type discriminator |
| research repository | nber.org, arxiv.org | `200` PDF | `404` | **reachable** |
| bibliographic API | crossref, openalex | `200` | `404` / count 0 | **reachable** |
| index provider | research.ftserussell.com | `200` PDF | `404` | **reachable** |
| **academic publisher** | onlinelibrary.wiley.com | **`403`** | - | **blocked**, `Cf-Mitigated: challenge` |
| **federal agency web** | ftc.gov | **`403`**, 453 B | **`403`, 453 B** | **blocked**, control identical |
| **index provider** | spglobal.com | **`403`**, 2,011 B | **`403`, 2,011 B** | **blocked**, control identical |
| **securities regulator** | sec.gov, efts.sec.gov | **`403`**, 4,819 B | **`403`, 4,819 B** | **blocked**, control identical |
| **preprint host** | papers.ssrn.com | **`403`** | - | **blocked** |
| **law repository** | scholarship.law.georgetown.edu | landing `200`, control `404`; **PDF endpoint `403`** | - | **partially blocked** |

> **The pattern is not random.** Government APIs and depositories are open; **publisher, agency-web
> and institutional-repository hosts are closed.** That shapes what this packet could establish, and
> it is the reason section 5.1 below is long.
>
> **Four of the eleven return the same status for a real document and an impossible one.** In each
> case the control is the only thing that shows the status is the blocker's rather than the
> document's.

---

## 1. Break rate - **not established, and the reason is a denominator, not a paywall**

### 1.1 The four routes tried

| route | what it would give | outcome |
|---|---|---|
| **Mitchell & Pulvino (2001)**, 4,750 US mergers 1963-1998 | a break rate over a merger-arb universe | **body unreachable** (T2 section 0.2). Abstract carries no rate |
| **Officer (2003)**, *Termination fees in M&A*, JFE, 582 citations | a termination rate over its sample | **closed access; no abstract in Crossref.** Could not establish |
| **Billman & Salop (2022)**, *Merger Enforcement Statistics: 2001-2020* | *"rates of second request, challenges, consent decrees, **abandonments** and trial outcomes"*, **"across Presidential Administrations"** | landing page reachable, **PDF endpoint `403`.** Could not establish |
| **The HSR final rule's own statistics** (read in full, 45 pages, 372,237 characters) | agency counts | **reachable and read** - see 1.2 |

### 1.2 What the HSR rule does say, verbatim

> *"in FY 2021, the Agencies reviewed HSR Filings for **3,520 transactions**, over twice the number
> of the prior year's filings. In FY 2022, the Agencies reviewed **3,152 transactions**."* Figure 1
> covers **FY 2014-2023**.

and, decisively for the denominator question:

> *"**transactions reported under the HSR Act are a small fraction of the total number of mergers
> and acquisitions that occur each year in the United States.**"*

### 1.3 The denominator problem, which is T4's sharpest finding on the rate

**Every reachable statistic is conditioned on a different universe from the one a merger-arbitrage
book trades.**

| statistic | its denominator | is it Walton's universe? |
|---|---|---|
| HSR filings (3,520 / 3,152) | **all HSR-reportable transactions**, overwhelmingly private targets with no quoted spread | **no** |
| Billman & Salop abandonment rate | *"every transaction that **received a second request**"* | **no** - a heavily adversely-selected subset. A deal that draws a Second Request is, by selection, one the agencies thought worth a closer look |
| a merger-arb book | **announced deals with a listed target and a quoted spread** | this is the universe T1 needs |

> **T1 section 6 item 1 requires a break rate "over a stated universe... precise enough that the
> denominator is knowable." The denominators here are perfectly knowable and they are the wrong
> ones.**
>
> **This is a units failure in the break rate, exactly mirroring section 6.1's units failure in the
> return.** `P(abandoned | second request)` is not `p`. Substituting it would overstate the break
> rate by an unknown factor; substituting the HSR filing count would understate the base by
> including thousands of untradeable private transactions.
>
> **Retrieving Billman & Salop would not fix this.** The paper is unretrieved *and* its conditional
> is the wrong one. **That distinction matters and section 5 keeps it.**

> **T1 section 6 item 1: FAILS.**

---

## 2. Break severity - **not established at all**

T1 section 3.2 requires `L` as **a mean and at least one upper quantile**, because the per-deal test
takes the mean and the cluster test takes the tail.

> **No source read in this packet reports loss-given-break in any form** - not a mean, not a
> quantile, not a range. The only quantitative statement about severity anywhere in the packet is
> **packet 9's own illustrative framing** (*collect 3%, lose 25%*), which T1 section 0a bound
> explicitly as "an illustration, not a measured magnitude."
>
> **T1 section 6 item 2: FAILS.** And per T1 section 3.2, *"if only a point estimate is published,
> the strand is capped at could not establish on the cluster test - not passed on it."* Here not
> even a point estimate is published.

**Why this item is structurally hard and not merely missed.** Severity depends on **how far the
target ran on announcement**, so it is a property of each deal's own pre-announcement price, not a
parameter of the strategy. A published mean would have to be conditioned on a run-up distribution
that itself varies by regime.

---

## 3. Clustering - **documented by three independent mechanisms, quantified by none**

This is the item packet 9 named as most likely to be underreported. **It is worse than
underreported: the mechanism is documented three separate ways and the magnitude is documented
nowhere.**

### 3.1 Mechanism one - the payoff itself is a short index put

Mitchell & Pulvino (2001), abstract verbatim:

> *"risk arbitrage returns are **positively correlated with market returns in severely depreciating
> markets** but uncorrelated with market returns in flat and appreciating markets. This suggests that
> returns to risk arbitrage are **similar to those obtained from selling uncovered index put
> options**."*

**This is a clustering statement at the level of the payoff, not an empirical count.** If the
return behaves like a short index put, then losses arrive **when the market falls**, which is by
construction a common factor across every position in the book simultaneously. **Independence of
breaks is refuted by the shape of the return before any break is counted.**

### 3.2 Mechanism two - financing withdrawal, independent of any deal's merits

Mitchell & Pulvino (2010), *Arbitrage Crashes and the Speed of Capital*, abstract verbatim:

> *"The imminent failure of large Wall Street prime brokerage firms during the 2008 financial crisis
> caused a **sudden and dramatic decrease in the amount of financial leverage afforded hedge
> funds**... **Seemingly long-term debt capital became short-term capital** creating a large mismatch
> in the duration of arbitrage opportunities... A primary consequence of this withdrawal of
> financing was the **inability of hedge funds involved in relative-value trades to maintain prices
> of substantially similar assets at substantially similar prices**."*

**Nothing in this mechanism concerns whether the deals were good.** The cluster arrives through the
right-hand side of the balance sheet.

### 3.3 Mechanism three - a common-cause contractual event

Miller (2020), *Material Adverse Effect Clauses and the COVID-19 Pandemic*, abstract verbatim:

> *"...under a typical MAE clause, given the current tremendous contraction in economic activity,
> **most companies will have suffered a material adverse effect** as such term is used in the base
> definition of most MAE clauses."*

**"Most companies" is a common-cause statement about a contractual trigger**, applied to every live
deal at once. Whether the exceptions shifted the risk back to acquirers is the paper's subject and
it concludes *"in some instances, a company will have suffered an MAE even if the MAE clause
contains exceptions for pandemics, changes in law, or both."*

### 3.4 What is missing, and it is the only thing T1 asked for

> **Not one source read gives the fraction of concurrent deals that broke in any cluster.**
>
> T1 section 2.2 states the test in scale-free form precisely so that a historical record could
> answer it: *"KILL if any documented break cluster shows a fraction of concurrent positions breaking
> inside a rolling 12 months greater than `f_max`."* **`f_max` cannot be computed** (it needs `s` and
> `L`, and `L` failed in section 2) **and the observed fraction cannot be measured** (no source
> reports it).
>
> **T1 section 6 item 3: FAILS on quantification while passing on existence.** Clustering is
> **established as real by three independent mechanisms** and **unquantified in every one.**

**This is the reverse of what T1 anticipated.** T1 section 6 item 3 permitted *"documented evidence
that they do not [cluster]"* as an alternative route to satisfaction. **No such evidence was found
either**, and the three mechanisms above point the other way.

---

## 4. Enforcement-regime dependence

T3 fixed S1's vantage line at **10 February 2025**, the effective date of the HSR final rule
(Federal Register `2024-25024`).

**Regime dependence is not speculative - it is the organising variable of the one complete database
that exists.** Billman & Salop describe results *"both in aggregate and **across Presidential
Administrations**"*. That a serious enforcement-statistics paper structures its results that way is
itself evidence that break-relevant outcomes vary by regime.

| figure | sample closes | relative to the 2025-02-10 line |
|---|---|---|
| Mitchell & Pulvino (2001) | **1998** | 27 years before |
| Officer (2003) | not established | - |
| Jetley & Ji (2010) | not established | - |
| Billman & Salop | **2020** | 5 years before |
| HSR rule Figure 1 | **FY 2023** | ~1.5 years before, and it counts **filings**, not outcomes |

> **No break-rate figure reachable in this packet post-dates the vantage line.** Per T1 section 5.1
> that caps S1 at **could not establish** whatever any historical figure says.
>
> **The asymmetry (T1 section 5.2) still admits the adverse content**: the short-put payoff shape,
> the 2008 financing mechanism, and the 2020 common-cause MAE trigger are evidence about **what this
> strategy does under stress** and do not expire with a regime.

---

## 5. What cannot be quantified - unretrieved and unknowable, in separate lists

### 5.1 UNRETRIEVED - it exists, it is public, this vantage could not reach it

Per T1 section 5.3 and packet 8's correction. **T5 must not convert any of these into an absence of
evidence.**

1. **Mitchell & Pulvino (2001), the body.** Bronze OA at Wiley; one location; `403` over raw HTTP
   and browser stack with `Cf-Mitigated: challenge`. **Contains the sample's break rate, severity
   and portfolio construction** - i.e. plausibly items 1, 2 **and** the section 6.1 test.
2. **Billman & Salop (2022), the complete second-request outcome database, 2001-2020.** Landing page
   `200`; PDF endpoint `403`. **Note it would still not supply `p`** - section 1.3.
3. **Officer (2003).** Closed access, 582 citations.
4. **Jetley & Ji (2010).** Closed access, no OA location.
5. **Every merger agreement on EDGAR** - break fees, MAC clauses, outside dates, financing
   conditions. `403`, control identical.
6. **The FTC/DOJ HSR Annual Reports, appendix A**, cited by the rule as *"reporting Adjusted
   Transactions in which a Second Request could have been issued"*. `ftc.gov` `403`, control
   identical.
7. **S&P US Indices methodology.** `403`, control identical.

### 5.2 UNKNOWABLE from public sources

1. **A break rate over the universe a retail merger-arb book would actually trade.** Section 1.3:
   the published denominators are all-HSR-filings or conditional-on-second-request. **Constructing
   the right denominator requires a deal database - which packet 9 forbids** (see 5.3).
2. **Loss-given-break as a distribution.** Section 2: it depends on each target's own
   pre-announcement run-up, so a published summary statistic would need a conditioning variable no
   source reports.
3. **The fraction of concurrent positions breaking in any historical cluster.** Section 3.4.
4. **Any break-rate figure under the post-2025-02-10 regime.** The regime is roughly eighteen months
   old at the time of writing; **a low-frequency event under an eighteen-month regime cannot have a
   published rate yet.** This one is not a blocked host - **it is a genuine small-sample limit**, and
   it is the only item in this document that is unknowable because of time rather than access.

### 5.3 The scope boundary, stated so it is not mistaken for either list

> **A merger-arb break distribution over the correct universe sits in commercial deal databases.**
> Packet 9 forbids calling one: *"No broker account, no deal database subscription, no screen of
> live situations."*
>
> **That is a boundary of this packet, not a limit of public knowledge, and not the same thing as
> item 5.2.1 above.** 5.2.1 says the *published literature* does not contain the figure; this says a
> *purchasable* source plausibly does. **T5 must keep the two apart.**

---

## 6. T1 section 6.3: what loss channel does this condition not name?

T1 required this question be asked explicitly and answered whether or not anything was found.
**Three were found. The first is structural.**

### 6.1 The renegotiated deal - **T1's payoff has no third state**

T1 models every position as **complete at `s`** or **break at `L`**. A third outcome exists and is
common: **the deal completes at a reduced price.** The acquirer renegotiates - often under threat of
a MAC claim, which section 3.3 shows becomes available to many acquirers at once in a common-cause
event.

> **Every formula in T1 assumes two states.** `p* = (s-c)/(s+L)`, `f_max = (D_max+s-c)/(L+s)`, and
> all three breadth terms are derived from a binary. **A three-state payoff makes each of them a
> first-order approximation with an unsigned error**, and T1 gives T5 no rule for handling it.
>
> **This is a defect in the sealed condition.** Recorded, not patched. Per the standing instruction
> and packet 8's precedent: the sealed text stands as written and wrong.

**It does not change this packet's outcome**, because sections 1 to 3 fail on evidence that no
payoff model would rescue. **It would have mattered had the evidence been there**, which is exactly
why T1 section 6.3 required the question be asked rather than left to a later reader.

### 6.2 Duration, which T1 bounds nowhere

T3 established from the rule that a Second Request extends the waiting period *"after the parties
have **substantially complied**"*, with **no stated deadline for substantial compliance**. So an
individual position's holding period is **open-ended above**.

> T1 section 1.1 defines `mu` as a return **"per deployment period"** and **never bounds the
> deployment period.** A deal that takes three years does not lose money - it divides the return by
> three and occupies one of the `n_min` slots T1 section 3.1 requires be filled simultaneously.
> **T1 has a loss threshold and a breadth threshold and no duration threshold connecting them.**

### 6.3 Borrow recall on the short leg

In a stock deal the position is short the acquirer (T2 section S1.1). **A borrow recall forces the
hedge closed and leaves a naked long target** - the same shape as family 4's unhedged-leg exposure,
which family 4's condition reached only by accident and this one does not name at all. **No borrow
cost or availability figure was obtained** (T3 section S1.4).

---

## 7. Verdict of T4 against T1 section 6

| T1 section 6 component | status |
|---|---|
| 1. **rate bounded over a stated universe** | **FAILS** - wrong denominators, section 1.3 |
| 2. **severity as mean plus upper quantile** | **FAILS** - nothing published in any form, section 2 |
| 3. **clustering characterised** | **FAILS on quantification**, established as real by three independent mechanisms, section 3 |

> **The break distribution is not quantified on T1's own three-part definition.**
>
> T1 section 6: *"Survival requires all three... If (2) is unavailable, the cluster test is could not
> establish and the strand cannot survive. If (3) is unavailable, the verdict is likewise capped at
> could not establish."*
>
> **T4 returns COULD NOT ESTABLISH for S1. It does not return survives scoping.**

**And the direction is not neutral.** Of the three components, the one where evidence *was* found -
clustering - was found **entirely on the adverse side**: three mechanisms establishing that breaks
arrive together, and none establishing that they do not.

**S2 is not evaluated here.** T1 section 1.0 exempted a non-binary payoff from the break-specific
tests, and T3 section 4 recorded that S2's fate rests on T1 sections 1.3 and 6.1, which T2 answered.
