# Roadmap - five families

Sorted by how much of the risk is *existence* versus *extraction*. Family 1 is
active; the rest are sequenced, not abandoned. Each has a stated gate, so moving
on is a decision rather than a drift.

## 1. Latency on public sources - ACTIVE
A market resolves to a named public page. Price updates when traders notice; we
act when the source publishes. Not a forecasting claim - the edge is tens of
cents against a hurdle of a few, rather than a few basis points against it.
Existence risk near zero for the mechanism; all risk is speed and event count.
Runs alert-only, no capital. **Gate: none.**

## 2. Documented public-record anomalies - NEXT
Opportunistic insider buys with the routine/opportunistic split, filing-text
drift, 13D events, small-cap post-earnings drift. External priors that survived
peer review - a stronger foundation than anything generated internally. Hurdle is
basis points, which is the point. Needs an EDGAR pipeline. Decay risk is real;
these are published.
**Gate: relocation complete, and family 1 has produced a verdict.**

## 3. Mechanical flow - HOLD
Index reconstitution, merger arb, spin-offs, lockup expiry. Someone trades
because a mandate compels it. Existence risk near zero; timing and marginal
names are contested.
**Gate: held until another family is producing. Merger arb's skew - collect 3%,
lose 25% on a break - makes a bad month a real loss rather than a null, and that
is the wrong first exposure.**

## 4. Structural risk premia - LATER
Perp funding carry, variance risk premium. Someone pays continuously to hold
what they don't want. Lowest existence risk here and the highest capacity. Risk
moves to counterparty and tail: a carry book dies on exchange failure, not on
edge decay.
**Gate: venue access confirmed post-move, and capital deployable through the
relocation without being needed elsewhere.**

## 5. Segmentation - LATER, jurisdiction-gated
Two venues, different user bases, no shared liquidity provider. Existence risk
low; the binding constraint is jurisdictional and changes with the move.
**Gate: post-move jurisdiction verified in writing - which venues are reachable
from the UK, tested rather than assumed.**

## The screen, before any new idea in any family
1. Run it against the fifteen mechanisms in `programmes/kalshi/`. Most new ideas
   are one of them renamed.
2. Answer: **who is on the other side, and why are they willing to lose?**
3. State the hurdle and the expected edge in the same units before building.
   45 kills died on arithmetic, not on imagination.
4. Check it does not reduce to *identifying informed traders from behaviour*.
   That is answered.
5. **Of any documented edge, ask: what is the friction, and is it still there?**
   Five strands now. **Four times the premium *was* the friction; once it was not.**
   - **Family 2** - it survived publication because it was uneconomic to arbitrage:
     concentration in illiquid, hard-to-trade names, so the cost side inherits the
     concentration. Three independent instruments agreed in packet 7 -
     `programmes/insider/registry/F2-INSIDER-SCOPING.md`.
   - **Perp funding carry** - it persists because arbitrage capital is constrained by
     regulation and margin, and the arbitrageur can be forced out before convergence.
   - **The equity variance risk premium** - it was a restriction on who could sell
     options, and the alpha ended when the restriction ended.
     Both in `programmes/premia/registry/F4-PREMIA-SCOPING.md`.
   - **Index-reconstitution flow** - it was the market's capacity to absorb a predictable
     demand shock, and it expired because **capacity grew**, not because any rule changed.
     `programmes/flow/registry/F3-FLOW-SCOPING.md`.
   - **Merger arbitrage** - the exception. It is **not a friction at all**: the payoff behaves
     like selling an uncovered index put, so somebody must bear a loss that arrives in severe
     market declines. **Whether it is still there could not be established.** Same entry.

   The variance case is the cleanest, because the friction and the premium ended
   together. **A friction that has since eased is not a smaller edge; it is a finished
   one.** Ask this of any edge, not only a published anomaly - the earlier form of this
   item asked only about published anomalies and would have missed three of the five.

   **Five strands in, the question sorts cleanly on its first half and stalls on its
   second.** What the friction *is* has been establishable from published work every time.
   Whether it is *still there* has been establishable three times in five. **So ask the
   second half first: it is the half that fails.**
