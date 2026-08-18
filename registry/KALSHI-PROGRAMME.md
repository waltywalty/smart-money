# The Kalshi programme - what was learned that outlives the venue

**Written 2026-08-18, packet 5 Phase B1.** Fifty-six entries: 45 killed, 4 corrected, 3 confirmed,
1 open, 3 could-not-establish, 6 lost to a rollback and recorded as lost rather than reconstructed.

This is not a summary of the register. It is the part that transfers.

The venue answered. Three effects are real, none is tradeable, and the cost of participating is now
measured on both of its axes and bounded on one. What was built to reach that answer is worth more
than the answer.

---

## 1. The hurdle - the single most useful number this project produced

Every idea must clear the cost of crossing **at the horizon it would be entered at**, never zero.
That cost is not a constant. It is a function of at least two variables, and the project measured
both.

### Horizon (H60, CONFIRMED, n=336-412 events per horizon)

| lead | hurdle | spread |
|---|---|---|
| 24 hours | **-3.81c** | 5.01c |
| 10 minutes | **-1.94c** | ~1.3c |

It roughly halves. The pre-registered check was whether the half-spread saving passes through to
the taker or is absorbed by adverse selection: half-spread saving **1.82c**, P&L improvement
**1.87c**. It passes through in full. That match is why the finding stands.

**It is the project's only positive-direction result, and it is still a cost.**

### Size (T2.1, bounded)

| order size | hurdle |
|---|---|
| 1 contract | **-4.39c** |
| 10 | -3.90c |
| 100 | -3.86c |
| continuous limit | -3.85c |

**A hundredfold size increase buys 0.53c, about 12%** - and the whole 500x axis is bounded by that
same 0.53c, against book impact that is unbounded above. The registry had been pricing at the most
expensive point on this axis, so sizing up makes the bar *easier*, not harder. That inverted the
expected direction and is why T2.1 sits on the right-for-the-wrong-reason list.

### Decomposition, at the 24-hour lead

| component | size | attackable? |
|---|---|---|
| half-spread | ~1.50c | no - it is the price of immediacy |
| fee | ~1.55c | no - it is the schedule, and it varies by series |
| **ask above fair value, beyond the half-spread** | **~1.34c** | **in principle, yes** |

**Only that last third is attackable at all**, and nothing measured across 21 series turned it
positive; the cheapest series to cross in bottom out at **-2.50c**. The -4.39c figure is the
24-hour weather-and-macro-ladder case and must never be quoted as universal.

**Fee multipliers vary by series.** `KXMLBGAME` carries `fee_multiplier: 0.5` where the code
assumed 1.0 everywhere. Read the multiplier; never assume it.

---

## 2. The three confirmed effects, and why none is money

**Mean reversion in prices (H62).** Lag-1 autocorrelation **-0.1896, 95% CI [-0.2147, -0.1650]**
over 90 markets and 87,315 candles, negative in 88 of 90, stable under leave-one-market-out and
leave-one-series-out.

**Mean reversion in executed trades (H63).** Between consecutive same-side executed trades,
**-0.2560 [-0.2858, -0.2247]** over 36 markets and 45,964 trades, **negative in 36 of 36**. The
naive all-trades control returned **-0.3048**, proving the method detects bid-ask bounce when bounce
is there - so what H62 saw is real price movement reverting, not quote flicker.

**The hurdle itself (H60)**, above.

**Why none of it is money:** expected reversion is **0.146c against a spread of 1.3c at the very
best** - roughly **9x short of covering a single crossing**, and **90.5x short** where the effect is
actually measurable. H63 settled *why* prices revert and moved the tradeability arithmetic by
exactly zero.

> **The mechanism question and the money question are independent.** Understanding why a sub-spread
> effect exists does not make it larger. This is the single most transferable sentence in the
> register.

---

## 3. The fifteen mechanisms - screen a new idea against these in five minutes

Forty-five kills reduce to fifteen reasons. Most new ideas are one of these renamed. Read them
**before** designing anything.

| # | mechanism |
|---|---|
| 1 | **Taker on public info:** edge = spread + fee, and the public feed is 78-258s behind a book that moves at 180s. |
| 2 | **Maker capturing spread:** the spread *is* the compensation for adverse selection. |
| 3 | **Maker collecting a subsidy:** the reward is tied quadratically to exposure. |
| 4 | **Internal-consistency arb:** the two books are one book; ladders are monotone; sets sum to $1. |
| 5 | **Cross-venue:** the gap is smaller than the round trip - and per H46 it was never even a hedge. |
| 6 | **Model vs market:** the free model's error bar is *wider* than the market's implied distribution. Four independent instances. |
| 7 | **Long-dated tails:** collateral drag beats mispricing. A 6000x mispricing returns 0.91%/yr. |
| 8 | **Short-dated tails:** where the tick exceeds fair value, the book is empty. |
| 9 | **Every bias measurable from free data is a bias only relative to free data.** |
| 10 | **Prices are calibrated** on both venues, at every bucket with enough events to test. |
| 11 | **Spread and flow are inversely coupled** - no market offers both. |
| 12 | **Cross-venue boxes:** settlement criteria diverge on 15 of 16 cross-listed pairs and the market prices the box at ~$1 regardless. The criteria risk is real, unpriced and still unharvestable, because the box costs above a dollar before the divergence matters. |
| 13 | **Rulebook breadth is priced:** on strict-superset pairs the broader contract is dearer by ~0.39c, the correct sign. What looked unpriced in the box was the two round trips. |
| 14 | **Non-partition ladders:** where no exclusivity clause exists multiple legs can pay, and the market already prices it - mids sum to 110c where a partition caps at 100c. |
| 15 | **Path, not level:** hourly changes mean-revert, and the expected reversion is a fraction of the spread. The only significant effect found, and still sub-spread. |

The unifying shape, stated once: **where the price is attractive, the market is not there.** Four
independent routes to it - far-OTM tails carry no bid (H34), cheap rungs never win (H53), the
mass is not misallocated (H54), and the obtainable version of a real effect moves against you
before you can take it (H61).

---

## 4. The instrument-failure catalogue - the most portable thing in this repository

None of these announced itself. None looked like a failure at the moment it happened. **Every one
was caught by two methods disagreeing, and not one by inspection.**

### 4.1 A status code is produced by a layer, and it may not be the resource's

Five instances, all silent, all in the direction of a plausible wrong answer:

| what was read | what actually produced it |
|---|---|
| a quote of `0.29/0.30` where the book said `0.05/0.06` | a **summarising fetch layer**, inventing a confident specific value |
| `http=200` for six keys that do not exist | the **CONNECT tunnel** - `HTTP/1.1 200 Connection Established`, printed first for every request through the VM proxy |
| "file absent" across an entire sweep | a **TLS failure on the proxy leg**; `urllib` cannot use an `https://` proxy, and the exception a `try/except` maps to absence |
| `http=100` after 120s on a 16 MB PUT | an **unanswered `Expect: 100-continue`**, an interim 1xx returned as if final |
| a control returning **400 identically to a real key** | an **unauthenticated probe of a private bucket** - it answers the request, not the resource |

Defences, all cheap: read the status of the *resource* (`-w '%{http_code}'`, never the first header
line); treat any 1xx as not-success; send `-H 'Expect:'`; an exception is not evidence of absence
until the request is shown to have reached the resource; and **run a control that must fail in the
same pass, at the same access level as the measurement.**

### 4.2 The fetch layer fabricates

A summarising fetch layer invented an entire order book at `0.409/0.415` where the true midpoint
was `0.2685`; reported `COUNT=101` for a page holding exactly 100 rows; returned 92 rows and then
34 for the same `limit=100`; truncated a large payload to a **different window per URL**, so three
passes gave three row counts; and reported an empty book as `0.0000/1.0000`, injecting a phantom
50% midpoint. **The same wrong answer reproduced across two independent fetches** - so re-fetching
alone does not catch systematic failure. Only a different endpoint does.

### 4.3 Filter honouring is per-endpoint and inverts

| endpoint | `ticker=` | `series_ticker=` | `min_ts`/`max_ts` |
|---|---|---|---|
| `/markets` | **IGNORED** | honoured | honoured |
| `/historical/markets` | **IGNORED** | honoured | **IGNORED** |
| `/historical/trades` | **honoured** | **IGNORED** | honoured |

An ignored filter returns a full, plausible, wrong result set. `?ticker=` once produced six
different quarter-hour crypto markets all reporting the same close time, and **only the impossible
control key exposed it**. Verify every parameter on every endpoint you use it on, and record the
verification per endpoint rather than per parameter.

### 4.4 Rate limiting has memory, and it is not a property of the API

Three arms on `/historical/markets` at 69 req/s read **0% rejection**; one arm on `/markets` at the
same rate seconds later read **28.4%**. One variable differed and the conclusion wrote itself.
Repeating the first arm gave **32.5%**, then **44.1%** - the limiter is shared and carries state,
and the apparent property of the endpoint was a property of the running order.

Then, from a different VM in a different metro: **3,200 requests at 64 threads, zero 429s**, where
the first machine began rejecting after roughly 600. The curve belongs to
*(endpoint, source, recent history)*. **Counterbalance both orderings or wash out and show the
baseline recovered; hold the source constant.** The clean band, measured immediately after a burst
being rejected at 44%, is **at or below ~6 req/s**; the knee is unbracketed between 5.9 and ~28.

### 4.5 A non-200 mid-pagination is not the end of the data

`/events?series_ticker=KXMLBGAME` read **1,400** events through a loop that broke on `st != 200`; a
429 arrived on page 7 and was recorded as cursor exhaustion. Paged again with the 429 retried, the
same query returns **4,083**. Every pagination must record *why* it stopped - `cursor_exhausted`,
`empty_page`, `http_<code>` or `page_cap` - and only the first two may be read as a complete answer.

### 4.6 A two-hour hole in the exchange's own trade history

`2026-06-11T07` returns **13 trades, all inside the first 0.26 seconds** of the hour. `T08` returns
**zero**. `T06` and `T09`, and the same hours on neighbouring days, all hit the 1,000-row cap.
Reproduced on a second direct probe. **A collector reads those hours as quiet, not as missing.**
Any study touching 11 June needs this.

### 4.7 A single page gives a false floor

`KXMLBGAME` reads 2026-07-05 on one page of 1,000 rows and 2026-06-08 fully paged. Follow the
cursor to exhaustion before reading a floor off anything.

---

## 5. Right for the wrong reason - seven entries, and what each teaches

A verdict can be correct while the premise under it is false. When that happens the answer may
survive, but **the next study builds on the reason, not on the answer**, so the reason has to be
fixed even when nothing visible changes.

| # | entry | the premise that was wrong | what survived |
|---|---|---|---|
| 1 | **H15** negRisk sum | the sets were not failing to sum for the reason assumed | the kill |
| 2 | **H16** cross-venue macro arb | the gap was never a hedge, so "gap < round trip" understated it | the kill |
| 3 | **H46** settlement divergence | criteria diverge on 15 of 16 pairs, which the kill had not priced | the kill |
| 4 | **H49** non-exclusive sum | its own premise about exclusivity clauses | the kill |
| 5 | **Rule 10, HEAD vs ranged GET** | `HEAD` does *not* return 200 for absent keys; the 200 was the CONNECT tunnel | the rule - ranged GET is still better, for a better reason (206 vs 404 is sharper) |
| 6 | **C1 / the fee-ceiling premise** | every cost model was said to be the size-free continuous form; H56 uses the one-contract ceiling | the conclusion, at every size - but the direction inverted, sizing up makes the bar easier |
| 7 | **INFRA's "13% at 3 threads / 0.55s"** | that configuration is 3.6 req/s and rejects 0 of 240 | "run slowly" - right to run slowly, wrong reason for it |

**A bookkeeping gap this synthesis found:** `registry/FEE-CEILING-AUDIT.md` records the list as
having seven members, and `README.md` names four. **The seven were never enumerated in one place.**
The table above is that enumeration, and entries 5-7 are reconstructed from their own documents
rather than from a maintained list. One further candidate was **declined**: packet 3's
"bare python-urllib User-Agent is blocked at the edge" was tested against the proxy-TLS hypothesis
and held - curl with a `Python-urllib/3.10` UA gets 403, with an explicit UA or none gets 206. The
mechanism survived, so it is not an eighth entry.

---

## 6. What the data constraint actually was

The project spent real effort on a framing that was false, and the correction is worth carrying.

**The false framing:** Kalshi deletes settled history after ~67 days, so studies must race a
deadline and self-collection is urgent.

**What is true:** Kalshi does not delete. It **splits** data into a live set and a historical set
at a queryable boundary. `/historical/markets` reaches back to **2021-07-01**; B1 collected
**7,269,014 settled markets** across 351,653 events and 6,703 series. The 67 days was never a
retention limit - it was where the live/historical boundary happened to sit.

**What the boundary does:** both edges slide. Measured 2026-08-17, the live floor advanced
2026-06-08 to 2026-06-10 while `/historical/cutoff` advanced 2026-06-14 to 2026-06-17. The gap
**widens** rather than closing, so no reachability hole opens. There was never a deadline.

Two consequences the register carries: **H55 and H57 are could-not-establish for a reason that was
itself wrong** - the registry says "a calendar problem rather than a compute one", and the truth is
that waiting slides the sample rather than growing it. And the archive that would have filled the
gap - `archive.pmxt.dev`, hourly Kalshi orderbook Parquet - **stopped at 2026-06-11T03 and has not
resumed**, re-verified 2026-08-18 with a positive control alongside the impossible one.

---

## 7. Where the method goes next

**This describes what is portable. It proposes nothing and ranks nothing. The decision is Walton's.**

What transfers unchanged, to any market:

- The **pre-registration discipline** - rule, settling sample size, abandonment conditions and the
  meaning of each outcome, sealed and hashed before outcomes are seen. It has caught seven wrong
  premises here.
- The **hurdle-first habit**: measure the cost of participating, as a function of every axis it
  varies on, before measuring any edge. On Kalshi that turned out to be the whole answer.
- The **instrument-failure catalogue** in section 4. Nothing in it is Kalshi-specific except the
  endpoint names.
- The **unit-of-observation question**, asked first rather than last.
- **Obtainability as a gate separate from statistical validity** - H61 is the worked example: a real
  +4.99c effect on 644 held-out events, replicating in-sample to 0.03c, and unobtainable.

What would need building for the equities work already sketched in the roadmap - opportunistic
insider filings with the routine/opportunistic split, filing-text drift, the public-record feeds:

- **A different data layer.** Kalshi's public API needs no credentials and no vendor. SEC EDGAR is
  free but the filing corpus is large, the parsing is real work, and the useful joins (prices,
  benchmarks) come from somewhere else.
- **A different hurdle magnitude.** The Kalshi hurdle is measured in **hundreds of basis points**;
  an equity commission-plus-spread hurdle is measured in **single-digit basis points**. That is a
  hundredfold change in what counts as an edge, which changes the required sample size and the
  precision of every measurement - not the method.
- **A different obtainability question.** H61 died on sub-60-second detect-to-fill against a
  5-minute cron. Filing-based signals have a different latency structure; whether it is friendlier
  is exactly the sort of thing that has to be measured rather than assumed.

What does **not** transfer: the fifteen mechanisms are prediction-market specific in their
particulars, though several - calibration, spread-flow coupling, model-vs-market error bars - have
obvious analogues that would need re-measuring rather than re-assuming.

---

## 8. The one-paragraph answer

Fifty-six entries, three confirmed effects, none tradeable, and the cost of participating measured
on both axes and bounded on one. **The venue answered, and the answer is no.** What was built to
get there does not depend on that answer: a pre-registration discipline with seven caught premises,
an instrument-failure catalogue no textbook contains, a five-year reachable dataset with a verified
cold-start recovery path, and a durable write path that survives the machine that used it. All of
it points at any market. **That is the finding of the programme, and it is not about Kalshi.**
