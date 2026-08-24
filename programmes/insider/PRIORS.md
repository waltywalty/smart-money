# T2 - What the priors actually claim

Programme: insider. Packet 7, task T2. Compiled 2026-08-24, **after** `KILL-CONDITION.md`
was sealed (sha256 `925b9bff478cea4211d7c4cdccf626e70f2ca58c99745a6730a90cef3dcfcde1`,
commit `eac6eda`).

**No synthesis and no recommendation appear in this document.** That is T5's job and it is
not done here.

## How this was read

Every figure below was extracted from the **source document fetched as raw bytes** and read
directly - PDFs pulled over raw HTTP and text-extracted, HTML stripped to text. **No figure
in this document comes from an abstract summary, a citation of a citation, a vendor page or
a blog.** Where only an abstract was reachable, the row says so.

Per `KILL-CONDITION.md` section 4a: **search failure is not absence.** A strand that could
not be sourced is marked *could not establish*, never *no evidence found*.

### The vantage line

`KILL-CONDITION.md` section 3a: a strand whose only evidence closes on or before
**2016-08-24**, with no post-publication out-of-sample re-estimation, cannot support a
survival verdict. Applied below as **VANTAGE: STALE**.

---

## Summary table - one row per strand

| strand | claimed effect | horizon | sample | n | risk adjustment | venue | vantage | post-pub re-estimation | replication coverage |
|---|---|---|---|---|---|---|---|---|---|
| Aggregate insider buys vs sells | **4.8%** spread (7.8% before controls) | 12 months | **1975-1995** | >1,000,000 trades | 6x5 size / book-to-market reference portfolios | RFS 2001 | **STALE** (closed 31y ago) | **none found** | **not covered** (C&Z); unknown (M&P) |
| Routine vs opportunistic | **VW 82 bp/mo** (9.8%/yr, t=2.15); **EW 180 bp/mo** (21.6%/yr, t=6.07); routine EW 43 bp/mo (t=1.73), VW negative | 1 month, monthly rebalanced | data 1986-2007; analysis **1989-2007** | not extracted | 5-factor = Carhart-4 + liquidity; also CAPM, FF3, DGTW | JF 2012 (NBER WP 2010) | **STALE** (closed 18.7y ago) | **none found** | **not covered** (C&Z); unknown (M&P) |
| Small-cap / microcap concentration | L&L: effect concentrated in small firms. Zhao: mean **CAR[1,30] 6.3%** on the >10%-run-up subgroup | L&L 12 months; Zhao **30 trading days** | L&L 1975-1995; Zhao **2018-2024** | Zhao 17,237 purchases / 1,343 issuers / 5,421 insiders | L&L size+B/M. **Zhao: NOT risk-adjusted - the paper says so itself** | RFS 2001; **arXiv preprint 2026, not peer-reviewed** | L&L STALE; **Zhao current** | Zhao is not a re-estimation of a prior strand | not covered |
| Role weighting (officers / directors / 10% holders) | L&L: large shareholders' predictive power **"not robust over time"** across 1976-85 vs 1986-95 | 12 months | 1975-1995 | as above | size + B/M | RFS 2001 | **STALE** | **none found** | not covered |
| Cluster buys | **COULD NOT ESTABLISH** | - | - | - | - | - | - | - | - |
| First-time buyers | **COULD NOT ESTABLISH** | - | - | - | - | - | - | - | - |
| Filing-lag informativeness | **COULD NOT ESTABLISH** | - | - | - | - | - | - | - | - |

---

## Strand detail

### 1. Aggregate insider buys versus sells - Lakonishok & Lee (2001)

*Read from* `lsvasset.com/pdf/research-papers/Insider-Trades-Informative.pdf`, HTTP 200,
349,843 bytes, text-extracted.

Verbatim from the source:

> "Before controlling for size and book-to-market effects, firms with extensive insider
> purchases during the prior six months outperform companies with extensive insider sales
> by **7.8% over the next 12 months**."
>
> "After controlling for size and book-to-market effects, the spread in returns decreases to
> **4.8%**."
>
> "We use the most extensive database available, which includes **more than one million
> trades** covering the period **from 1975 to 1995**."

**Two things the paper says about its own predecessors and itself, both decision-relevant:**

> "[Seyhun (1998)] that did not adjust for size and B/M **overestimated abnormal returns**."
>
> "in unreported regression results for two subperiods, 1976-1985 and 1986-1995, it is shown
> that the predictive power of **large shareholders' trades is not robust over time**."

**The effect lost 38% of its size to a risk adjustment before any decay.** 7.8% -> 4.8% is
the cost of controlling for size and book-to-market on the same data. That is not
post-publication decay; it is what the raw number was measuring.

### 2. Routine versus opportunistic - Cohen, Malloy & Pomorski

*Read from* `nber.org/system/files/working_papers/w16454/w16454.pdf`, HTTP 200, 219,222
bytes, text-extracted. NBER WP 16454, October 2010; published *Journal of Finance* 67(3),
2012.

Verbatim:

> "A portfolio strategy that focuses solely on opportunistic insider trades yields
> value-weight abnormal returns of **82 basis points per month**, while the abnormal returns
> associated with routine traders are essentially zero."
>
> "the equal-weight portfolio that goes long opportunistic buys and short opportunistic sells
> earns a five-factor alpha of **180 basis points per month (t=6.07), or over 21.6% per
> year**, while the portfolio that goes long routine buys and short routine sells earns a
> only marginally significant **43 basis points per month (t=1.73)**."
>
> "the spread in five-factor alphas between opportunistic buys and opportunistic sells is a
> positive and significant **82 basis points** [per month, t=2.15, 9.8% per year,
> value-weight]"

**Risk adjustment**, verbatim: "alphas for the CAPM, Fama-French three-factor model, the
Carhart (1997) four-factor model, and the **five-factor model including a liquidity
factor**, as well as DGTW characteristic-adjusted returns."

**Sample**: insider data "1986 to December, 2007"; the analysis runs **1989-2007** because
the routine classification needs three prior years.

**Units warning, recorded because it governs T4.** This is a **monthly-rebalanced long-short
portfolio alpha**, not a per-event buy-and-hold abnormal return. It incurs turnover on both
legs every month. Converting it to the per-event figure `KILL-CONDITION.md` section 1
requires is not a rescaling and the paper does not report the per-event number.

**The gap between the two headline figures is the whole story for a retail operator.**
Equal-weight 180 bp/mo against value-weight 82 bp/mo means **more than half the measured
effect lives in the smaller names** - which is where T4's spread and borrow costs are worst.

### 3. Small-cap and microcap - Zhao (2026), arXiv preprint

*Read from* `arxiv.org/abs/2602.06198` and `arxiv.org/html/2602.06198v1`, both HTTP 200.
Submitted 5 Feb 2026. **q-fin.ST preprint, 9 pages, not peer-reviewed.**

> "The analysis covers **17,237 open-market purchases across 1,343 issuers from 2018 through
> 2024**, restricted to market capitalizations between $30M and $500M."
>
> "transactions disclosed after price appreciation exceeding 10% yield the highest mean
> cumulative abnormal return (**6.3%**) and the highest probability of outperformance
> (**36.7%**)."

**Horizon**, from the paper's own definition: `CAR[1,30]` - "from trading day t+1 through
t+30". A 30-trading-day (~6 week) horizon.

**The risk adjustment does not exist, on the paper's own account.** From its discussion:

> "These channels can be distinguished by future work examining whether the effect remains
> when **the target is defined in risk-adjusted units** or when returns are normalized by
> recent volatility."

So the "abnormal returns" in the title and abstract are **not factor-adjusted**. Reading the
source rather than the abstract is what surfaced this; the abstract's phrasing would
otherwise have been recorded as a risk-adjusted result.

**A detail that matters more at retail size than at fund size.** The best subgroup has a mean
CAR of 6.3% and a **probability of outperformance of 36.7%** - below half. A positive mean
with a sub-50% hit rate is a right-skewed distribution in which most trades lose. At a size
where only a handful of positions can be held, the mean is not what gets realised.

**Investability filter**, verbatim: "a minimum average daily dollar volume (ADDV) of
**$200,000** over the trailing 30 days." T4 must price spread at that ADDV, not at
small-cap averages.

**Event rate**: 17,237 purchases over 2018-2024 = **~2,460/year** in the $30M-$500M band
before any classifier filter. Above `KILL-CONDITION.md` section 2's floor of 50/year on the
raw universe; the rate **after** the classifier's precision-0.38 threshold and the
>10%-run-up subgroup restriction is **not reported** and is not derivable without filing
data, which this packet is forbidden to pull.

### 4-6. Cluster buys, first-time buyers, filing-lag informativeness

**COULD NOT ESTABLISH.** Searched this session; **no peer-reviewed source was reached for
any of the three.** The search returned commercial and vendor material almost exclusively -
insider-signal trackers, brokerage blogs, and API vendors.

Per `KILL-CONDITION.md` section 4a this is recorded as an instrument failure in the review,
**not** as an absence of literature. Cluster-buy studies may well exist; this session did
not reach one.

**Worth recording as an observation rather than a finding:** the strand most heavily marketed
to retail - cluster buying - is the one for which a targeted search returned vendor content
and no paper.

---

## Post-publication decay and replication coverage

T2 calls this the single most decision-relevant item. **For every strand above, the answer
is that no post-publication out-of-sample re-estimation was found.** What was established is
*why* - and the two answers are different in kind.

### Chen & Zimmermann, Open Source Cross-Sectional Asset Pricing - CONTROLLED NEGATIVE

*Read from* `raw.githubusercontent.com/OpenSourceAP/CrossSection/master/SignalDoc.csv`,
HTTP 200, 181,712 bytes. Impossible-path control on the same host: **404**. The file carries
a `GScholarCites202509` column, so it is current to September 2025.

**331 documented signals. Zero match `insider`, `Form 4`, `Section 16`, `13D` or
`opportunistic`.**

That zero is **controlled**, not assumed. Terms that must appear if the catalogue extracted
correctly: `momentum` 20, `analyst` 23, `accrual` 16, `short interest` 3, `asset growth` 2,
`share issuance` 2. And the structural confirmation - the catalogue's data categories are:

| Cat.Data | signals |
|---|---:|
| Accounting | 196 |
| Price | 56 |
| Analyst | 21 |
| Trading | 20 |
| Other | 13 |
| Options | 9 |
| **13F** | **8** |
| Event | 8 |

**There is no Form 4 or Section 16 category at all.** Institutional holdings (13F) are
covered; insider filings are not. The largest open replication effort in the field has not
re-estimated any strand of this anomaly.

### McLean & Pontiff (2016) - COVERAGE UNKNOWN, and the search that nearly lied

*Read from* `tevgeniou.github.io/EquityRiskFactors/bibliography/AcademicReviewFactor.pdf`,
HTTP 200, 1,023,569 bytes.

> "We study the out-of-sample and post-publication return-predictability of **97 variables**
> that academic studies show to predict cross-sectional stock returns. Portfolio returns are
> **26% lower out-of-sample and 58% lower post-publication**. [...] Post-publication declines
> are **greater for predictors with higher in-sample returns**, and returns are higher for
> **portfolios concentrated in stocks with high idiosyncratic risk and low liquidity**."

**Their sample ends in 2013.**

`insider` appears **zero times** in this PDF - and **that proves nothing**, which is the
point. Control terms that must appear if the predictor list were in the document:
`share issuance` 0, `asset growth` 0, `net operating assets` 0. They are absent too, and the
paper states why:

> "associated studies are detailed in the paper's **Internet Appendix**."

**The predictor list is not in the document I read.** Had the control terms not been run, the
zero would have been recorded as "McLean & Pontiff do not cover insider trading" - a
fabricated negative from a search that could not have succeeded. **Whether this anomaly is
among the 97 is COULD NOT ESTABLISH**, pending the Internet Appendix, which was not reached.

**What the 58% figure is and is not.** It is a base rate for published anomalies in general,
measured on a sample ending 2013. **It is not a measurement of this anomaly.** Applying it to
these strands would be assuming the answer.

**Two of their conditional findings point the same way**, and both are read from the source
rather than inferred: post-publication declines are **larger** for predictors with higher
in-sample returns, and returns are higher in **low-liquidity** stocks. The strands here are
high-in-sample-return and concentrated in illiquid names.

---

## What is contested

Recorded as disagreement, not adjudicated.

1. **Whether the aggregate effect survives risk adjustment at a size worth trading.** L&L
   report the spread falling from 7.8% to 4.8% on adding size and B/M controls, and state
   that earlier work without those controls overestimated it.
2. **Whether large-shareholder trades predict at all.** L&L's own subperiod check says their
   predictive power is "not robust over time". Any role-weighting scheme that leans on 10%
   holders is leaning on the part the source says is unstable.
3. **Equal-weight versus value-weight.** CMP report 180 bp/mo EW against 82 bp/mo VW for the
   same strategy. These are not a range around one number - they are two different
   strategies with different cost structures, and the literature reports both without
   resolving which a small account should read.

---

## What is missing, stated as prominently as what was found

1. **No post-publication out-of-sample re-estimation was found for any strand.**
2. **Three of seven strands have no reachable peer-reviewed source at all** - cluster buys,
   first-time buyers, filing-lag informativeness.
3. **Four of seven strands rest on samples that closed before 2016-08-24** - two of them
   before 1996.
4. **Whether McLean & Pontiff cover this anomaly is unknown**, because their predictor list
   lives in an Internet Appendix that was not reached.
5. **No per-event effect size was found for any strand.** Every figure is a portfolio return
   or a subgroup mean. `KILL-CONDITION.md` section 1 is stated per event.
6. **No strand reports an investable event rate** after its own classifier is applied.
7. **The one current-sample source (Zhao 2026) is a non-peer-reviewed preprint that states
   it is not risk-adjusted.**
