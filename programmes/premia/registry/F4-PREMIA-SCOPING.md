# F4-01 - Structural risk premia (perp funding carry, variance risk premium), as a strand set

| | |
|---|---|
| **id** | `F4-01` |
| **programme** | premia (family 4) - **SCOPED, NOT OPEN** |
| **entered** | 2026-08-24 |
| **verdict** | **S1 could not establish / S2a KILL / S2b could not establish. Family does not survive scoping.** |
| **pre-registration** | `KILL-CONDITION.md`, sha256 `2a87dc4c7a34e6c3866fcd3f39ff8e0410506ad26330de85cd9100b7c27d2555`, commit `2d07ad7`, sealed before any venue or premium source was read |
| **evidence** | `PRIORS.md`, `MECHANICS.md`, `TAIL.md`, `SCOPING-VERDICT.md` |
| **capital deployed** | none. No account, no API key, no test position, no data pull. |

## The claim, as scoped

That perpetual funding carry or the variance risk premium carries a return, net of venue costs and
net of a documented sterling cash benchmark, large enough to justify building a book - at a size
Walton could run inside a survivability cap, and with a tail whose magnitude and frequency are
known.

## The verdict

**S2a - the equity index variance risk premium - is a KILL.** Its magnitude was measured, not
missing: traded option alphas are *"indistinguishable from zero"* over fifteen years, the
delta-hedged alpha *"has gone to zero"* since a break around 2010, and cumulative traded-put
returns are zero from March 2009 to December 2022 (Dew-Becker & Giglio, Chicago Fed WP 2025-17).
Against T1's 5.00 pp floor over Bank Rate, that fails item 1, and T1 section 7 makes items 1-4 kills.

**S1 and S2b are could-not-establish**, on independent routes:

1. **Units.** No published magnitude exists for a held perpetual funding-carry position. The two
   figures in the literature are a **fixed-date futures basis** (BIS WP 1087) and a **threshold
   convergence trade** (He et al.) - the papers say so themselves. S2b reports a **variance wedge**
   (0.14 annualised variance units), not a return.
2. **Fixed costs.** No venue read publishes a withdrawal figure. Hyperliquid says only *"there may
   be small gas fees."* `F` is incomplete, so `K_min` and `K_min / 0.15` cannot be computed.
3. **The hedge leg is uncosted** by every source read, and `L` - loss-given-failure including the
   unhedged-leg exposure - is not established, so `p*` cannot be computed.
4. **Tail frequency is not bounded.** But see the boundary note below: it is unretrieved, not
   unknowable.
5. **Vantage.** S2b's evidence closes December 2022 and Deribit has since changed ownership
   ("Deribit by Coinbase"), which T1 section 4.2 makes a per-venue vantage reset.

## The caution that travels with the verdict

**Every unestablished item is on the cost or risk side.** Fixed costs, the hedge leg,
loss-given-failure, tail frequency, Deribit's margin and fees, Binance's mechanisms. **Not one is
on the return side.**

**And the return side, where it was measurable, failed.** The closest post-vantage analogue for S1
is 1.11% excess for BTC in 2023 and 0.28% in 2022, against a floor of 5.00 pp - roughly a fifth of
the bar, before bid-ask, slippage, FX and fixed costs that the source's fee-only model omits.

**So the verdict is agnostic while the evidence is not.** Read this entry as: *the evidence needed
to decide does not exist in this packet, what is missing points down, and what was measured came in
at a fifth of the bar.*

## What is documented and adverse regardless of the verdict

- **Both venues whose ADL ordering is documented rank the queue by profitability.** OKX: *"Priority
  increases with higher unrealized profit."* Hyperliquid: ranked by *"unrealized pnl and leverage
  used."* A delta-neutral book's hedge leg is its profitable leg in the move that stresses the venue.
- **The carry predicts the carry receiver's own liquidation.** A 10% rise in standardised carry
  predicts a **22% increase in sell liquidations** - the closing of short futures positions
  (BIS WP 1087). At 10x leverage the futures leg *"would have been liquidated in over half of the
  months"* of a 2019-2024 sample.
- **$2.047 billion** of ADL notional at Hyperliquid in a **five-minute** window on 10 October 2025,
  in three waves, during a 10-20% decline in BTC/ETH/SOL.
- **Counter-finding, carried because T1 said "regardless of frequency":** in the one forensic study
  of that event, delevered shorts were *ex post* profitable, having been bought back at market
  lows. Source is an X thread whose authorship overlaps the paper reporting it; outcomes were
  heterogeneous and queue position mattered.

## revive_if

All of 1-4 must be satisfiable for S1, because they are independent. Any one alone changes the
picture but not the verdict. Item 5 alone revives S2b's magnitude question; nothing revives S2a
short of item 6.

1. **A published magnitude for the strand itself** - the return to a **held** short-perpetual /
   long-spot position collecting funding, annualised **per unit of continuously deployed capital**,
   from a sample **closing after 2023-01-01**, of at least 24 months, containing both signs of the
   funding rate, **with its dispersion stated.** Not a dated-futures basis; not a threshold
   convergence trade. *(lifts route 1)*
2. **A published fixed-cost figure** - the withdrawal, transfer and FX charge that does not scale
   with size, from a venue's own schedule. *(lifts route 2, and makes `K_min` computable)*
3. **A costed hedge leg** - the venue, custody arrangement, fee and cross-margin dependency of the
   second leg, plus a loss-given-failure figure that **includes the unhedged-leg exposure**.
   *(lifts route 3, and makes `p*` computable)*
4. **A frequency bound on ADL, socialised loss and venue failure** across the venue set, from a
   documented count over a stated exposure window. *(lifts route 4)*
5. **A post-2023 re-estimation of the Bitcoin variance risk premium** expressed as a **return on
   deployed capital** at a named venue, with that venue's margin requirement for a short-variance
   position stated. *(lifts S2b)*
6. **A published re-estimation showing the equity variance risk premium's delta-hedged alpha has
   returned**, on a sample closing after Dew-Becker & Giglio's December 2022, in a peer-reviewed or
   central-bank venue. *(the only thing that reopens S2a)*

## The cheapest open question, and it is a scope boundary rather than a gap

> **Route 4 is answerable from public, unauthenticated endpoints at two named venues, today.**
>
> - **Hyperliquid's public REST API** labels ADL fills - direction label, execution price,
>   liquidation mark price - *"allowing us to identify the realized ADL flow separately from
>   market-driven liquidations and voluntary trades"* (Campbell, Hey, Moallemi & Nutz, who
>   reconstructed the October 2025 event from it).
> - **Deribit's `public/get_last_settlements_by_currency`** returns `socialized`,
>   `session_tax_rate` and `session_bankruptcy` per settlement, with `search_start_timestamp` and
>   `continuation` paging.
>
> **Neither was called. Packet 8 forbids data pulls, and that is the only reason route 4 is open.**
> This is not a limit of public knowledge. It is a limit of this packet's scope, and it is cheap to
> lift.

## Not a revive condition

- **A larger carry figure from a pre-2023 sample.** T1 section 4.1, and He et al.'s own structural
  break.
- **The pooled 2020-2024 figure**, or any pooled figure spanning the break. Two dead years carried
  by two live ones is not a current estimate.
- **A figure on the venue's own exchange token.** BNB 2023 clears the floor at 6.27% and is
  excluded because a carry book whose underlying is the token of the venue holding its margin is
  doubly exposed to that venue, not diversified against it.
- **A gross carry, a funding-rate level, or a Sharpe ratio without a return and a dispersion.**
- **A vendor backtest, a practitioner thread, or a summary of any of the above.** `TAIL.md` treats
  an X thread as institutional evidence characterised by a paper read in full, never as a source in
  its own right - and the same standard applies here.
- **A venue's own marketing of its insurance fund.** T3 recorded the design and the court record
  alleges the fund is *"almost never drawn upon"* because it is fed by liquidation surplus. Size is
  not evidence of use.

## What was established and survives this entry

**The item-5 answer, for each strand, in one sentence:**

- **S1:** it persists because arbitrage capital is constrained by regulation and margin, and
  because the arbitrageur can be forced out before convergence.
- **S2a:** it did not persist - it was a restriction on who could sell options, and it decayed to
  zero as the restriction eased.
- **S2b:** not established.

> **Three families, one answer: the premium was the friction.** Family 2 - uneconomic to arbitrage.
> S1 - arbitrage capital constrained. S2a - supply restricted, and it ended when the restriction
> did. Packet 8 expected *"someone must warehouse a risk nobody wants"* and pre-committed that
> finding access friction instead would be family 2's result again. **It is, twice.**
>
> **Generalisation for the ROADMAP screen:** item 5 currently asks why a *published anomaly*
> survived publication. The stronger form, earned here, is to ask of **any** documented edge:
> **what is the friction, and is it still there?**
