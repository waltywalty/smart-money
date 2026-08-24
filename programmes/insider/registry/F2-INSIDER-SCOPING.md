# F2-01 - Documented Form 4 insider-trading anomalies, as a strand set

| | |
|---|---|
| **id** | `F2-01` |
| **programme** | insider (family 2) - **SCOPED, NOT OPEN** |
| **entered** | 2026-08-24 |
| **verdict** | **COULD NOT ESTABLISH** |
| **pre-registration** | `KILL-CONDITION.md`, sha256 `925b9bff478cea4211d7c4cdccf626e70f2ca58c99745a6730a90cef3dcfcde1`, commit `eac6eda`, sealed before any literature was read |
| **evidence** | `PRIORS.md`, `CLASSIFIER-SPEC.md`, `HURDLE.md`, `SCOPING-VERDICT.md` |
| **capital deployed** | none. No collector, no filing data, no trade. |

## The claim, as scoped

That one or more documented Form 4 insider-trading strands - aggregate buys versus sells,
routine versus opportunistic, cluster buys, first-time buyers, role weighting, small-cap
concentration, filing-lag informativeness - carries a residual, net of a UK-retail hurdle on US
equities, large enough to justify building an EDGAR pipeline.

## The verdict

**Could not establish, on all seven strands.** Not a kill: no residual was computed, so none was
found inside the hurdle. Not a survival: no strand cleared the pre-committed bar.

**Four independent routes**, no shared cause, so no single new paper resolves them:

1. **Units.** No strand reports a per-event effect. All are portfolio alphas or subgroup means.
2. **Population.** Form 4 code `P` = "Open market **or private** purchase"; and "a trade" in the
   three-year routine lookback is undefined, so two defensible readings give different samples.
3. **Implementation.** Long-short needs borrow in the names where borrow is scarcest (cost not
   established); long-only forfeits an undecomposed share of the reported spread. Neither yields
   a number.
4. **Vantage.** No post-publication out-of-sample re-estimation found for any strand. Four rest
   on samples closing before 2016-08-24; two before 1996.

## The caution that travels with the verdict

**Could-not-establish may be concealing a kill.** Four of nine hurdle cells are missing, and
**all four are on the cost side** - spread, borrow, and two components of it. Cost moves the
residual one way only.

**So the verdict is agnostic while the missing evidence is not.** This entry must not be read
later as "promising, needs more work". It is: *the evidence needed to decide does not exist, and
what is missing points down.*

## revive_if

All four must be satisfiable, because they are independent. Any one alone changes the picture
but not the verdict.

1. **A published out-of-sample re-estimation** of any named strand, in a peer-reviewed venue, on
   a sample **closing after 2016-08-24**, reporting the effect **with its horizon and its risk
   adjustment stated**. *(lifts route 4, and route 1 if it reports per-event terms)*
2. **A per-event effect size** - abnormal return per Form 4 purchase, not a portfolio alpha - at
   a stated horizon against a stated benchmark. *(lifts route 1)*
3. **A published statement of how the population was defined**: how code `P` was split between
   open-market and private purchases, and what counts as "a trade" in the routine lookback.
   *(lifts route 2)*
4. **A citable effective-spread level in basis points** for sub-$2bn US names from published
   market-quality data, plus a borrow-cost and availability figure for microcap shorts. *(lifts
   route 3 and gives the hurdle a range)*

**Also sufficient to reopen item 4 of route 4 alone:** McLean & Pontiff's Internet Appendix,
reached and read. If the strand is among their 97, their post-publication decline estimate
applies to it directly. This is the cheapest open question in the packet.

**Not a revive condition:** a larger effect size from an older sample; a vendor backtest; a
practitioner blog; or a summary of any of the above. `KILL-CONDITION.md` section 4a - a summary
of a paper is not the paper.

## What was established and survives this entry

Three independent instruments - Cohen/Malloy/Pomorski 1989-2007, McLean & Pontiff to 2013, the
SEC's Rule 605 release on Q1 2023 TAQ - **agree the effect concentrates where trading is
hardest**. Different samples, different decades, different methods.

**Mechanism implied, not separately tested:** what survived fourteen years of publicity survived
because it was uneconomic to arbitrage. A selection effect on which anomalies persist, not an
edge waiting to be collected. **Generalised to the ROADMAP screen as item 5.**
