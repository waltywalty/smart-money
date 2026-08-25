# F3-01 - Mechanical flow (merger arbitrage, index reconstitution), as a strand set

| | |
|---|---|
| **id** | `F3-01` |
| **programme** | flow (family 3) - **SCOPED, NOT OPEN** |
| **entered** | 2026-08-25 |
| **verdict** | **S1 could not establish / S2 could not establish. Family does not survive scoping.** |
| **pre-registration** | `KILL-CONDITION.md`, sha256 `c62c13ab11236f1bef8733f24c9709b6ec8ff893463fb126eb0ad4163f05056a`, commit `8f3c0a9`, sealed before any source was read |
| **evidence** | `PRIORS.md`, `MECHANICS.md`, `BREAKS.md`, `SCOPING-VERDICT.md` |
| **capital deployed** | none. No broker account, no deal database, no screen, no data pull. |

## The claim, as scoped

That merger arbitrage or index-reconstitution flow carries a return, net of costs and of a
documented benchmark, large enough to justify building - at a breadth Walton could actually run, and
with a break distribution whose rate, severity **and clustering** are known.

## The verdict

**Neither strand survives, and neither is killed on its arithmetic - because in neither case was the
arithmetic evaluable.**

**S1 - merger arbitrage. Six independent routes:**

1. **Units and reachability.** The only return figure - Mitchell & Pulvino's +4%/yr, 4,750 mergers
   1963-1998 - is a risk-adjusted portfolio excess return whose construction sits in a body that
   returned `403` with `Cf-Mitigated: challenge`.
2. **Vantage.** The line is **2025-02-10**, the effective date of the HSR final rule (Federal
   Register `2024-25024`). **The newest S1 figure closes 2020.**
3. **The break rate's denominator.** Published rates are conditioned on *all HSR filings* or on
   *transactions receiving a Second Request*. **Neither is the universe a merger-arb book trades**
   - and retrieving the blocked source would not change that.
4. **Severity.** Loss-given-break is unpublished in any form - not a mean, not a quantile.
5. **Clustering unquantified.** Established as real by **three independent mechanisms** - the
   short-put payoff shape, 2008 financing withdrawal, and a common-cause MAE trigger in 2020 - and
   **measured by none.**
6. **`F_pos`, so `V_min` and `K_min`.** Third consecutive family in which the fixed-cost line was
   the binding unknown.

**S2 - index-reconstitution flow.** The magnitude is an **event-study abnormal return**, which T1
section 6.1 names as not the position Walton would hold, and no conversion input is established.
**But the direction is not in doubt:** additions fell from **7.4% in the 1990s to under 1% over the
past decade**, deletions to **+0.1% (2010-2020)**, with a similar decline in other index families
(Greenwood & Sammon, *J. Finance* 2024).

> **The deletion leg is dead on a measured figure.** A short-the-deletion position earns minus the
> abnormal return: **-0.1% gross, before any cost.**

## The caution that travels with the verdict

**Every unestablished item is on the cost, loss or observability side. Not one is on the return
side.** Break rate, severity, cluster fraction, fixed costs, borrow, deal-document terms, duration -
all of them. The passive benchmark, also unestablished, **raises** the bar.

**And the one measured return figure in the packet went the wrong way**: a decay to approximately
zero.

**So the verdict is agnostic while the evidence is not.** Read this entry as: *the evidence needed to
decide is behind a blocked vantage or in the wrong units, what is missing points down, and the only
thing measured is a decay.*

## What is documented and structural regardless of the verdict

- **The payoff is a short uncovered index put** - *"positively correlated with market returns in
  severely depreciating markets but uncorrelated... in flat and appreciating markets"* (Mitchell &
  Pulvino 2001). **Independence of breaks is refuted by the shape of the return before any break is
  counted.**
- **Clustering has three documented mechanisms and none of them is antitrust** - the one channel the
  regulatory record actually covers.
- **A Second Request extends the waiting period "after the parties have substantially complied"**,
  with no stated deadline for compliance. **Deal duration is open-ended by construction** (HSR final
  rule, effective 2025-02-10).
- **Early termination of the initial waiting period ended in March 2020** and had until then been
  routine - a dated, agency-documented, duration-lengthening change.
- **Required breadth never falls below roughly 50 simultaneous positions** anywhere in the positive
  zone, and is **57 at T1's own break-rate ceiling** - a structural consequence of a capped gain
  against a loss eight times its size, computed from formulas sealed before any evidence.
- **The index rule is deterministic, announced about five weeks ahead, updated three times daily
  including anticipated actions, and the provider distributes predictive index data.** There is no
  informational friction left.

## revive_if

S1 needs **1 and 2 and at least one of 3-5**; they are independent and no single source resolves
them. S2 needs 6 alone.

1. **A return to a held merger-arbitrage position** - per unit of deployed capital, at a stated
   breadth, net of commission, borrow and FX, from a sample **closing after 2025-02-10**.
2. **A break rate over the universe a merger-arb book trades** - announced deals with a listed
   target and a quoted spread - **with the denominator stated.** Not `P(abandoned | second request)`;
   not a count of HSR filings.
3. **Loss-given-break as a distribution** - a mean **and** at least one upper quantile.
4. **A cluster fraction**: for any documented episode, the share of concurrent deals that broke
   inside twelve months. **One number, and nobody publishes it.**
5. **A fixed per-position cost figure** (`F_pos`) from a broker schedule, making `V_min` and `K_min`
   computable.
6. **A post-2020 re-estimation of the index effect expressed as a net return on deployed capital**
   at a stated holding window - not an abnormal return.

## The cheapest open questions, and they are scope boundaries rather than gaps

> **Four documents that would move this verdict are public and were blocked at this vantage, not
> absent from the world:**
>
> - **Mitchell & Pulvino (2001), the body** - bronze OA at Wiley, `403`. Plausibly contains the break
>   rate, the severity and the portfolio construction, i.e. items 1, 3 **and** the section 6.1 test.
> - **Billman & Salop (2022)**, the complete second-request outcome database 2001-2020 - landing page
>   `200`, PDF endpoint `403`. *(Note it would still not supply item 2 - wrong conditional.)*
> - **Officer (2003)** and **Jetley & Ji (2010)** - closed access.
> - **Every merger agreement on EDGAR** - `403`.
>
> **A vantage that can reach publisher and agency-web hosts would answer several of these in a day.**
> This is a limit of the packet, not of public knowledge.

**Separately, and genuinely not knowable:** a break-rate figure under the post-2025-02-10 regime. The
regime is about eighteen months old; **a low-frequency event under an eighteen-month regime cannot
have a published rate yet.** That one is time, not access.

**And a scope boundary distinct from both:** a break distribution over the correct universe plausibly
sits in a **commercial deal database**, which packet 9 forbids calling.

## Not a revive condition

- **A break rate conditioned on a Second Request.** It is an adversely-selected subset by
  construction and overstates `p` for a merger-arb book by an unknown factor.
- **A count of HSR filings.** The rule itself says HSR-reportable transactions are *"a small fraction
  of the total number of mergers and acquisitions"*, and most have no listed target.
- **An event-study abnormal return**, for either strand. T1 section 6.1 names it.
- **A hedge-fund index return for merger arbitrage.** It is a fund's performance net of fees and
  subject to survivorship and backfill - not the position Walton would hold.
- **A pre-2025-02-10 merger-arb figure, however large**, and **a pre-2020 index-effect figure,
  however large.**
- **A forecasting-accuracy benchmark.** A Brier score is not a return.
- **A vendor backtest, a practitioner note, or a summary of any of the above.**
