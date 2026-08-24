# T4 - The tail, and the honest limit of scoping it

Programme: premia. Packet 8, task T4. Written after T1 was sealed (sha256 `2a87dc4c...`, commit
`2d07ad7`), T2 (`69a2723`) and T3 (`855e8f4`).

**Three lists, kept separate throughout: what is documented, what is inferred from incidents, and
what is not knowable from public sources.** A fourth category turned out to be necessary and is
the most important finding in this document - see section 6.

**No expected-value calculation appears here.** T1 section 3.2 forbids multiplying an unestablished
frequency by a loss, and nothing below does.

---

## 1. What the search instruments were, and what they proved

| instrument | null-capable? | control |
|---|---|---|
| **CourtListener** RECAP exact-phrase search | **yes** | `"zzqxwv nonexistent control phrase"` -> **count 0**; `"FTX Trading"` -> **count 515**. Paired both ways |
| **arXiv** exact-phrase search | **yes** | established in `PRIORS.md` section 0.2, re-confirmed here: impossible phrase -> 0 entries, `"auto-deleveraging"` -> 1 |
| **within-document** term counts | **yes**, with in-file positive controls | reported inline at each use |
| Crossref result counts | **no** | see `PRIORS.md` section 0.1 |

### 1.1 A court-filing hit can be a news article stapled to a pleading

`"auto-deleveraging"` returns **16** CourtListener documents. The top three are
**Dolgov**, **Sorokin** and **Razvan v. HDR Global Trading Limited** (N.D. Cal.) - HDR being
BitMEX's operator - and the search snippet for each is *"EXHIBIT 3 ... The Mechanics of Market
Manipulation - CoinDesk"*.

The second amended consolidated complaint in the related **BMA LLC v. HDR** (N.D. Cal.,
3:20-cv-03345-WHO) was downloaded and extracted (13.1 MB, 90 pages, 203,293 characters):

| term | count in the pleading body |
|---|---|
| auto-deleverag | **0** |
| deleverag | **0** |
| socializ | **0** |
| clawback | **0** |
| insurance fund | 20 |
| *positive control:* BitMEX | 573 |
| *positive control:* plaintiff | 64 |

> **The ADL hits were inside an attached press exhibit, not in any pleading.** A full-text search
> over court filings returns whatever a litigant stapled to a complaint. **An aggregator summary
> filed as an exhibit is still an aggregator summary**, and packet 8 excludes it.

---

## 2. Venue failures - what the primary record contains

**Established as fact, from the court record:**

- **FTX.** `"FTX Trading"` returns **515** documents on CourtListener, spanning *In re FTX Trading
  Ltd.* (Bankr. D. Del. and D. Del.), *In re FTX Cryptocurrency Exchange Collapse Litigation*
  (MDL and S.D. Fla.), and *United States v. Bankman-Fried* (S.D.N.Y. 22-cr-00673-LAK), whose
  trial transcripts are on the docket. The collapse is not in doubt and is not re-established here.
- **BitMEX / HDR Global Trading Limited.** *United States v. HDR Global Trading Limited*
  (S.D.N.Y. 1:24-cr-00424-JGK), with a **sentencing letter filed by HDR on the docket** - i.e. the
  matter reached sentencing. Separately, the CFTC's civil action (S.D.N.Y. 1:20-cv-08132) appears
  as an exhibit in the private suits.

**Alleged, not established - a plaintiff's pleading is a primary document whose contents are
allegations.** From the BMA second amended consolidated complaint, verbatim:

> para 182: "Automatically liquidating contracts that were out of the money, BitMEX would cover the
> trader's losses but would also **take all of the trader's collateral**. **By setting the
> liquidation point higher than necessary** to protect against the risk of a loss greater than the
> trader's collateral, BitMEX **consistently profited from these liquidations.** BitMEX would place
> these profits in its insurance fund... **the Insurance Fund is almost never drawn upon and
> instead has grown consistently** such that it now contains assets worth hundreds of millions of
> dollars."

> para 185: "During a period in the day with high market volatility and crashing bitcoin prices
> (from nearly $8,000 to $4,000 per bitcoin)... **BitMEX's trading platform went offline for
> twenty-five minutes. As a result of the outage, BitMEX did not dip into its Insurance Fund, but
> rather liquidated $800 million of its customers' highly leveraged positions**..."

The complaint further alleges intent behind the outage. **That allegation is not repeated as fact
here**, and the case's disposition was not established in this packet.

**What survives the allegation/fact line as a structural claim** is the design point, which is
consistent with T3's documentation: **a liquidation engine set conservatively takes all collateral,
and the insurance fund is fed by liquidation surplus rather than drawn down by it.** T3 found the
same shape at Hyperliquid - *"During backstop liquidation, the maintenance margin is not returned
to the user... the liquidator vault requires a buffer to make sure backstop liquidations are
profitable on average."* Two venues, two decades apart in venue-generation terms, same design.

---

## 3. Socialised loss and ADL specifically - **one quantified event, no frequency**

### 3.1 The literature says the area is understudied, and says so in those words

The only academic work located on the mechanism itself is **Campbell, Hey, Moallemi & Nutz,
*Risk-Based Auto-Deleveraging*, arXiv `2603.15963v2`** (published 2026-03-16, updated 2026-07-16) -
read in full, 213,717 characters. Abstract, verbatim:

> "Auto-deleveraging (ADL) mechanisms are a **critical yet understudied** component of risk
> management on cryptocurrency futures exchanges. When available margin and other loss-absorbing
> resources are insufficient to cover losses following large price moves, **exchanges reduce
> positions and socialize losses among solvent participants via rule-based ADL protocols.**"

And in the body: *"To the best of our knowledge, **multi-asset ADL has not been discussed in the
prior literature**."*

### 3.2 The one quantified event

From the same paper's empirical section, verbatim and in figures:

> "On **October 10, 2025**, the perpetual futures exchange **Hyperliquid** experienced a
> concentrated auto-deleveraging episode in which a large number of accounts were partially or
> fully closed **within a five-minute window**."

| quantity | value |
|---|---|
| total realised ADL notional, 75-coin core universe | **$2.047 billion** |
| window | **21:16-21:21 UTC**, three waves at 21:16:05, 21:16:56, 21:17:06 |
| wave 1 | $176.9M - HYPE, PUMP, FARTCOIN |
| wave 2 | $93.3M |
| wave 3 | $386.6M - **ETH, SOL, BTC, XRP** |
| market context | *"the exchange was not facing an isolated liquidation in a single asset, but a **broad and rapid repricing across the active universe**. Even the deepest markets, such as BTC, ETH, and SOL, decline by roughly **10-20%**, while several thinner names lose **more than half** their value"* |

**The magnitude side of T1 section 5 item 1 is therefore satisfied for one venue on one date.**
$2.047 billion of positions closed without their holders' consent in five minutes.

### 3.3 The counter-evidence, reported because it cuts the other way

The same paper reports a forensic analysis that **contradicts the natural reading**:

> "a recent discussion by Jia et al. [2026] provides an on-chain forensic analysis of Hyperliquid's
> October 10, 2025 liquidation event... **They observe that delevered short positions were ex post
> profitable since they were bought in at relative market lows. This challenges the notion of ADL
> as a loss socialization mechanism.** However, **individual ADL outcomes are heterogeneous because
> there were several waves of ADL and queue position mattered.**"

**Three qualifications, all of which matter and none of which cancels it:**

1. **It is an X thread, not a paper.** The reference reads: *"R. Jia, X. Ma, C. C. Moallemi, and
   S. Wang. Thread on Hyperliquid's liquidation pipeline, backstop vault, and ADL outcomes.
   `https://x.com/RuizheJia/status/2020906838653604056`, Feb. 2026. **X thread.**"* The thread was
   **not fetched** and is **could not establish** as a source in its own right. What is recorded
   here is the arXiv paper's characterisation of it, which was read in full.
2. **It is not an independent instrument. Moallemi is an author of both** the arXiv paper and the
   thread. This is one research group reporting on itself, and T1 section 5's requirement is
   *documented evidence*, not *independent* evidence - so it counts, but it is not corroboration.
3. **"Ex post profitable" is path-dependent.** Being deleveraged out of a short means buying back;
   buying back at a market low is a good fill **only because the market subsequently recovered**.
   Had it continued down, the same fill would have been a large forgone gain. One realisation of
   one path is not a distribution.

> **So the direction of ADL's effect on a delta-neutral book is contested, and this document
> reports it as contested.** T3 established that both documented ADL queues rank by profitability.
> The one forensic study of the largest event says the deleveraged shorts nevertheless did well.
> **T1 section 3.4 pre-committed that the structural finding is carried into T5 regardless of
> frequency, and that pre-commitment now cuts in a direction I did not anticipate when I wrote it:
> it obliges me to carry the counter-finding too.**

### 3.4 A third positive-controlled null

The FSB's *The Financial Stability Risks of Decentralised Finance* (16 February 2023), read in full
(142,712 characters):

| term | count |
|---|---|
| auto-deleverag | **0** |
| socializ | **0** |
| insurance fund | **0** |
| clawback | **0** |
| *positive control:* crypto | 217 |
| *positive control:* leverage | 30 |

**An international standard-setter's financial-stability report on this sector does not name the
mechanism by which a solvent venue reallocates losses between its users.** That is consistent with
"critical yet understudied" and it is a third independent instrument agreeing.

---

## 4. Correlation of the tail with the carry - **established, and the direction is adverse**

T1 section 5 item 3 asks whether qualifying events cluster in the conditions where carry is
largest. **Three independent sources, different data and different methods, say yes.**

| # | source | finding |
|---|---|---|
| 1 | Schmeling, Schrimpf & Todorov, BIS WP 1087 - regression, Table 7 | *"a higher carry predicts liquidations of short futures positions... a rise in standardized carry by 10% predicts a **22% increase in total sell liquidations**"*, and *"a high carry predicts overall greater risk (since implied volatility goes up when carry rises)"*. **Sell liquidations are the closing of short futures positions - the carry receiver's leg.** |
| 2 | He, Manela, Ross & von Wachter, arXiv 2212.06888v6 - FTX episode | *"Bitcoin futures prices were substantially higher than spot prices **at FTX**, but the opposite was true on other exchanges... consistent with **FTX investors liquidating their short futures positions quickly**, either voluntarily... or **involuntarily as the exchange liquidated their underfunded positions**."* **The basis blew out against the carry receiver at the failing venue specifically.** |
| 3 | Campbell, Hey, Moallemi & Nutz, arXiv 2603.15963v2 - the Oct 2025 event | ADL fired during *"a broad and rapid repricing across the active universe"* with BTC/ETH/SOL down 10-20%. **Not an idiosyncratic single-asset failure - a market-wide move.** |

And the same BIS paper measures how often the position is lost at all: *"assuming a leverage of 10
(which is significantly lower than the maximum leverage offered by most exchanges), **the futures
leg of the strategy would have been liquidated in over half of the months in our sample.**"*

> **T1 section 5 item 3 is satisfied, and the answer is that the tail is correlated with the
> carry.** The compensation is largest under the conditions that remove you from the position.
> Packet 8 anticipated this as the case that would matter: *"the premium is not compensation for a
> random risk - it is compensation for a risk that arrives exactly when you are most exposed to
> it."*

---

## 5. What cannot be quantified - **frequency**

T1 section 3.2 requires T4 to bound the documented frequency at or below `p*/3`. **It cannot be
bounded from anything read in this packet.** Four independent routes, each controlled:

1. **The two papers that establish the carry magnitude never mention the mechanisms.** Zero hits
   for insurance fund, socialised loss, clawback, ADL, default and custody across both, with
   in-file positive controls of 210/56 (arbitrage), 123/8 (funding), 202/119 (spot). (`PRIORS.md`
   section S1.8.)
2. **The one paper on the mechanism contains no event record.** In arXiv 2603.15963v2:
   `historical` **0**, `incident` **0**, `frequency` **0**, `how often` **0**, `FTX` **0**,
   `March 2020` **0** - against in-file positive controls `leverage` **259** and `ADL` **224**. It
   is a mechanism-design paper with one reconstructed event, not a frequency study.
3. **The court record surfaces collapses, not routine ADL** - and the ADL hits it does return are
   press exhibits (section 1.1).
4. **The FSB report does not name the mechanisms** (section 3.4).

**One event is not a frequency.** The paper calls October 10, 2025 *"one of the largest publicly
observable ADL episodes of 2025"*, which implies there were others and names none.

> **Frequency of ADL, socialised loss and venue failure is not established by this packet, and
> T1 section 5 item 2 therefore fails.** Per T1 section 3.2 that is **could not establish**, never
> a kill: no frequency was established, so none was found above the bar.

---

## 6. The category T1 did not have: **knowable, and out of scope**

This is the most important paragraph in T4.

**The frequency is not unknowable. It is unretrieved, because this packet forbids the retrieval.**

- **Hyperliquid.** Campbell et al. reconstructed the October 2025 event from *"tick-level trade
  records... obtained from the **public Hyperliquid REST API**. These records contain the trade
  time, user address, coin, signed size, side, **direction label**, execution price, and
  liquidation mark price where applicable, **allowing us to identify the realized ADL flow
  separately from market-driven liquidations and voluntary trades.**"* **ADL events at Hyperliquid
  are publicly enumerable, and the venue labels them.**
- **Deribit.** T3 established that `public/get_last_settlements_by_currency` returns `socialized`,
  `session_tax_rate` and `session_bankruptcy` per settlement, with paging parameters. **The
  socialised-loss history is publicly enumerable.**

Both are **data pulls**, and packet 8 is explicit: *"Reading an exchange's published fee schedule,
funding-rate methodology, insurance-fund documentation or historical statistics page is in scope.
Pulling current funding rates, order books or price series is not."* **Neither endpoint was
called.**

> **T5 must not report this as "not knowable from public sources."** Two venues out of two whose
> mechanisms are documented also publish the event stream. The correct statement is: **the tail's
> frequency is knowable from public, unauthenticated endpoints at two named venues, cheaply, and
> this packet's own scope is the only reason it is not in this document.**
>
> That makes it a **revive condition**, not a limit of public knowledge - and, as with packet 7's
> McLean & Pontiff Internet Appendix, it is the cheapest open question in the packet.

---

## 7. Two loss channels T1 does not enumerate - recorded and parked, not amended

T1 is sealed. Standing rule: *record it and park it.* Neither of these is corrected below; both
are carried into T5 and the close-out.

1. **Forced liquidation of the hedge leg.** T1 section 2.1 defines a material loss event as removal
   of capital *"by an action of the venue or its backstop rather than by the market movement of the
   position itself."* A liquidation is triggered by market movement and executed by the venue's
   engine, so it sits on the boundary of that definition and is not named by it. **T1 section 3.3
   nevertheless catches the exposure** - the surviving leg becoming unhedged - so the sealed
   condition is not blind to it, but it reaches it by the wrong route. Given the BIS finding that
   the futures leg would have been liquidated **in over half of the months**, this is not a tail at
   all; it is the modal outcome at 10x, and the deficiency in T1's enumeration is material.
2. **Venue outage.** If the venue is unreachable you cannot add margin, unwind, or re-hedge.
   Alleged at BitMEX for twenty-five minutes on 13 March 2020 during an ~$8,000 to $4,000 move.
   **No venue documentation read in T3 mentions outage as a loss channel**, and T1 does not
   enumerate it. Section 3.3's unhedged-leg clause is again the only thing that reaches it.

---

## 8. The three lists, as packet 8 requires

### Documented

- ADL exists at Hyperliquid and OKX, is a final solvency safeguard, and both documented queues rank
  by profitability (T3).
- Deribit socialises losses at bankruptcy sessions, with an amount, a rate and a public history
  endpoint (T3).
- Hyperliquid backstop liquidation at 2/3 of maintenance margin transfers **all** cross margin (T3).
- **$2.047 billion** of ADL notional at Hyperliquid in five minutes on 10 October 2025, in three
  waves, during a 10-20% move in the deepest names.
- The carry predicts liquidations of the carry receiver's own leg (22% per 10% of standardised
  carry).
- At 10x leverage the futures leg would have been liquidated in **over half of the months** of a
  2019-2024 sample.

### Inferred from incidents

- Insurance funds at these venues are fed by liquidation surplus and are rarely drawn on (alleged
  for BitMEX; documented in equivalent form for Hyperliquid's liquidator vault).
- Venue failure and the carry receiver's leg interact directly: at FTX the basis moved against the
  short-futures side at the failing venue while moving the other way everywhere else.
- ADL's realised effect on deleveraged shorts in the one studied event was **ex post favourable**,
  per a non-independent X thread characterised in a paper read in full.

### Not knowable from public sources

- **Nothing in this list that matters.** See section 6: the frequency is knowable and unretrieved.
- Genuinely not established anywhere reachable: **Binance's** mechanisms and history (WAF
  challenge, T3 section 0); the **trigger** for a Deribit bankruptcy session; the **disposition** of
  the BitMEX civil class actions; whether any documented ADL event has ever fired against an
  identified delta-neutral book.

---

## 9. What T4 hands T5

- **Magnitude: bounded**, at one venue on one date, at $2.047bn / five minutes, plus total loss of
  cross margin at 2/3 maintenance margin.
- **Frequency: not bounded** - T1 section 5 item 2 **fails**.
- **Correlation: established, adverse** - T1 section 5 item 3 **passes**, in the wrong direction.
- **Therefore the tail is not quantified on T1's own three-part definition**, and T1 section 5
  pre-committed the consequence: *"If (2) is unavailable... the verdict is **could not establish**,
  whatever the carry."*

**One thing T5 must say plainly.** Packet 8 stated that T4 would decide this packet. **On the
evidence, it did not.** `PRIORS.md` established that the post-vantage carry does not reach T1's
floor on any liquid asset, so the carry side fails before the tail is reached. The tail work above
is not thereby wasted - T1 section 3.4 carries the ADL finding into T5 regardless - but the
ordering must be reported honestly rather than arranged to match the expectation.
