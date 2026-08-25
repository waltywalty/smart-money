# T5 - The verdict against T1

Programme: flow (family 3, mechanical flow). Packet 9, task T5.

**Pre-registration:** `KILL-CONDITION.md`, sha256
`c62c13ab11236f1bef8733f24c9709b6ec8ff893463fb126eb0ad4163f05056a`, commit `8f3c0a9`, sealed
2026-08-25 before any source on merger arbitrage, deal breaks or index reconstitution was read.
**Evidence:** `PRIORS.md` (`91ecdae`), `MECHANICS.md` (`a9f1584`), `BREAKS.md` (`44f83b8`).

**This document does not open the programme.** `ROADMAP.md` family 3's gate - *held until another
family is producing* - is unchanged. Nothing is producing.

---

## 1. The benchmark, and how an unestablished half is handled

T1 section 1.1 required **two** documented benchmarks and the threshold applied to **the higher**.

| benchmark | status |
|---|---|
| **sterling cash** | **Bank of England Bank Rate = 3.75%**, effective 18 December 2025, from the Bank's own `boeapps/database/Bank-Rate.asp` (`200`; an impossible page on the same host returned `404`) |
| **passive equity index total return** | **NOT ESTABLISHED.** No primary source for it was reached in this packet |

> **The unestablished half can only raise the bar, never lower it**, because T1 requires the higher
> of the two. **So T1's floor is applied as a lower bound: `mu` must reach at least 3.75 + 3.5 =
> 7.25% net, and plausibly more.** A test applied at its lower bound is still a test; it can produce
> a fail but not a pass. **No strand below reaches even the lower bound**, so nothing turns on the
> missing half.

---

## 2. S1 - merger arbitrage, against T1 section 8 item by item

| # | requirement | result |
|---|---|---|
| 1 | `E >= 3.5 pp` over the higher benchmark | **not evaluable** - `s`, `p`, `L` and `c` all unestablished |
| 2 | `p <= p*/2` | **not evaluable** - no break rate over the right universe (`BREAKS.md` 1.3) |
| 3 | every position sized so a break costs `<= 2.0%` | **not evaluable** - `L` unpublished in any form |
| 4 | no documented cluster exceeding `f_max` | **not evaluable** - `f_max` needs `L`; and **no cluster fraction is published anywhere** |
| 5 | `n_min` computed and available positions `>= n_min` | **not evaluable** - needs `p`; see section 4 for what the formula shows regardless |
| 6 | `K_min` computed and reported as a number | **FAILS** - `F_pos` never established; broker and EDGAR sources `403` |
| 7 | sample closing after the vantage line | **FAILS** - line fixed at **2025-02-10**; the newest S1 figure closes **2020** |
| 8 | all three break-distribution components | **FAILS** - all three (`BREAKS.md` 7) |
| 9 | every magnitude the position Walton would hold | **FAILS** - not one magnitude passes (`PRIORS.md` 3) |
| 10 | every figure from a named, dated source read rather than summarised | **partial** - the two sources that matter most were read in abstract only |

**Items 1-5 are *not evaluable* rather than failed.** T1 section 8 makes 1-5 kills and 6-10
could-not-establishes. **Nothing in 1-5 was evaluated, so nothing in 1-5 was missed**, and the
verdict falls to the 6-10 group.

> ## S1: COULD NOT ESTABLISH

**Six independent routes**, so no single new source resolves them:

1. **Units and reachability of the return.** The one return figure - Mitchell & Pulvino's +4%/yr -
   is a risk-adjusted portfolio excess return whose construction is in a body this vantage cannot
   reach. Section 6.1 could not be applied to it.
2. **Vantage.** No S1 figure post-dates 2025-02-10, and the newest closes five years before it.
3. **The break rate's denominator.** Published rates are conditioned on *all HSR filings* or on
   *transactions receiving a Second Request*. **Neither is the universe a merger-arb book trades**,
   and retrieving the blocked source would not change that.
4. **Severity.** Loss-given-break is unpublished in any form - not a mean, not a quantile.
5. **Clustering is unquantified.** Established as real by three independent mechanisms; measured by
   none.
6. **`F_pos`, so `K_min` and `V_min`.** Third consecutive family in which the fixed-cost line was
   the binding unknown - T1 section 4 named that in advance for exactly this reason.

---

## 3. S2 - index-reconstitution flow

T1 section 1.0 exempted a non-binary payoff from the break-specific tests, and T3 confirmed S2's
payoff is not a short option. **S2 is judged on items 1, 6, 7, 9 and 10 only.**

| # | requirement | result |
|---|---|---|
| 1 | `E >= 3.5 pp` over the higher benchmark | **not evaluable** - the magnitude is in the wrong units and no conversion input is established |
| 6 | `K_min` reported as a number | **FAILS** - `F_pos` never established |
| 7 | sample closing after the vantage line | **the line cannot be fixed as T1 defined it** - see 3.2 |
| 9 | the position Walton would hold | **FAILS** - an event-study abnormal return, named in T1 section 6.1 as not that |
| 10 | read rather than summarised | **passes** - the working paper was read in full |

> ## S2: COULD NOT ESTABLISH

### 3.1 And the direction is not in doubt, which T1 section 9.1 requires be written where it cannot be missed

**The measured evidence is adverse and it is not close.** Greenwood & Sammon, *Journal of Finance*
2024, sample 1980-2020: additions **7.4% in the 1990s to under 1% over the past decade**; deletions
from large and negative to **+0.1% between 2010 and 2020**; *"a similar decline in the index effect
among other families of indices."*

> **The deletion leg is dead on a measured figure.** A short-the-deletion position earns the negative
> of the abnormal return; at **+0.1%** it earns **minus 0.1% gross, before any cost.** That is not a
> could-not-establish - it is a measured loss, and it is recorded as such inside a
> could-not-establish verdict that rests on the addition leg's units.

**And the mechanism is documented as expired, from the provider's own methodology (T3):** the demand
shock is derived by a published deterministic rule, announced roughly **five weeks** ahead, updated
three times daily including *anticipated* actions, with the provider itself distributing
**predictive index data**. There is no informational friction left to be paid for.

### 3.2 S2's vantage line cannot be fixed as T1 defined it - a defect, and it has no bite

T1 section 5.1 defined S2's line by *"the most recent methodology change that **the index provider
itself states was made to reduce predictability, front-running or trading impact**."* T3 established,
with positive controls, that the provider makes **no such statement** - `discretion`, `front-run` and
`predictab` each occur **zero** times against controls of `index` 449 and `Russell` 546.

> **Recorded as a defect in the sealed condition. Not patched, not widened.**
>
> **It changes nothing.** S2's only magnitude is adverse, and T1 section 5.2 says adverse evidence
> does not expire. **A line that cannot be drawn cannot exclude evidence it was never going to
> exclude**, and T5 states that so the defect is not mistaken for load-bearing.

---

## 4. The breadth term, and why "positive but unobservable" is not the verdict

T1 section 3.1's three breadth routes were sealed before any evidence. **They cannot be evaluated,
because `p`, `s` and `L` are unestablished.** What the formula shows regardless is a property of the
payoff, not of any sample.

At **the packet's own illustrative shape** (`s` = 3%, `L` = 25%, `c` = 0, `d_max` = 2%) - an
illustration of a sealed formula, **not a measured magnitude**:

| `p` | `mu` | (a) `3/p` | (b) `SD<=mu` | (c) `L/d_max` | **`n_min`** |
|---|---|---|---|---|---|
| 2% | 2.44% | 150 | 3 | 13 | **150** |
| 4% | 1.88% | 75 | 9 | 13 | **75** |
| 6% | 1.32% | 50 | 26 | 13 | **50** |
| **7%** | 1.04% | 43 | 48 | 13 | **48** *(the minimum)* |
| 8% | 0.76% | 38 | 100 | 13 | **100** |
| 9% | 0.48% | 34 | 279 | 13 | **279** |
| 10% | 0.20% | 30 | 1,765 | 13 | **1,765** |
| **`p*/2` = 5.36%** *(T1's own ceiling)* | 1.50% | 57 | 18 | 13 | **57** |

> **Required breadth is U-shaped and its floor is about 48 simultaneous positions.** At low break
> rates you need `3/p` deals to see a break at all; at high ones the mean collapses and the variance
> term explodes. **There is no region of the positive zone where a small book is enough.**
>
> **At T1's own break-rate ceiling the requirement is 57 simultaneous positions.**

**Walton asked for "positive but unobservable" to be reported as its own verdict if the breadth term
landed there. It cannot be, and the reason matters:** *positive* is not established. `s`, `L` and
`p` are all unknown, so the strategy's sign is unknown. **Reporting "positive but unobservable"
would assert the half of that phrase this packet has no evidence for.**

What can be said, and is: **whatever the sign, the breadth requirement never falls below roughly
fifty simultaneous positions**, and that is a structural consequence of a capped gain against a loss
eight times its size. It is the one quantitative statement this packet can make about S1 without an
unestablished input.

---

## 5. T1 section 9.2: did T4 decide this packet?

**No. Something failed first, and the ordering is reported as it happened rather than as it was
expected to happen.**

| stage | what it returned | when it became decisive |
|---|---|---|
| **T2** | **not one magnitude passes section 6.1** - two unreachable, three in event-study units, one unretrieved | **first.** The return side was already could-not-establish before any break evidence was sought |
| **T3** | vantage line fixed at **2025-02-10**; newest S1 figure closes 2020 | **second, and independently** - section 5.1 caps S1 whatever T4 finds |
| **T4** | all three break components fail | **third** |

> **Packet 9 stated that T4 "decides the packet, and unlike packet 8 it should actually get the
> chance to." It did not get the chance, for the same reason packet 8's tail pre-commitment did not:
> the return side failed first.**

**But the two are not the same, and flattening them would be the dishonest version.** In packet 8
the tail pre-commitment fired on nothing and was recorded as **untested**. **Here T4 produced an
independent finding that would have been decisive had the return side survived** - the break
distribution fails all three of T1 section 6's components, which caps any strand at could-not-
establish under a rule sealed before the evidence. **T4 was not load-bearing; it was
load-*capable*.** That is a different status from packet 8's and it is worth recording as such,
because a rule that would have bound is evidence the rule is well-formed, and a rule that never
engaged is not.

**Three packets, three times the pre-committed hard half never became load-bearing.** That is now a
pattern about **where these families fail**, not about the rules: they fail on **whether the
published number is the number you would earn**, long before they fail on risk.

---

## 6. Direction of the missing evidence - T1 section 9.1

> **Every unestablished item in this packet is on the cost, loss or observability side. Not one is
> on the return side.**

| unestablished | which side |
|---|---|
| break rate over the right universe | loss |
| loss-given-break, in any form | loss |
| cluster fraction | loss |
| `F_pos`, `V_min`, `K_min` | cost |
| borrow cost and availability | cost |
| break fees, MAC clauses, outside dates | loss |
| deal duration distribution | cost, via lockup and slot occupancy |
| the passive benchmark | **raises** the bar |

**And the one thing that was measured on the return side went the wrong way**: S2's index effect
declined from 7.4% to under 1%, with deletions at +0.1%.

> **So the verdict is agnostic while the evidence is not.** This entry must never be read later as
> "promising, needs more work." It is: *the evidence needed to decide is behind a blocked vantage or
> in the wrong units, what is missing points down, and the only measured return figure in the packet
> is a decay to approximately zero.*

---

## 7. T1 section 9.3: would a "survives" here have meant "not now"?

**Yes, and it must be said separately from the verdict because it does not depend on it.**

Family 3's gate is *held until another family is producing*, and packet 9's own framing gives the
reason: **this is the first family where being wrong costs money.** That reason is a fact about the
loss distribution and about Walton's circumstances, **not about whether the premium exists.**

**A survives here would still have met a gate that has not moved**: nothing is producing, family 1
has detected no events, families 2 and 4 are scoped and unopened. And T4's clustering finding
sharpens it - a strategy whose losses arrive **together**, through market declines, financing
withdrawal or a common contractual trigger, is the wrong first exposure for capital that must
survive a relocation.

**T5 makes only the first statement. This section is the second, and it is not a verdict.**

---

## 8. The family

T1 section 1.0: *"The family survives only if at least one strand survives on its own numbers.
Averaging is prohibited."*

| strand | verdict |
|---|---|
| **S1 - merger arbitrage** | **could not establish** |
| **S2 - index-reconstitution flow** | **could not establish**, with the **deletion leg dead on a measured figure** |

> ## Family 3 does not survive scoping.
>
> **No strand survives. Neither is killed on its arithmetic**, because in neither case was the
> arithmetic evaluable - which is itself the finding.

---

## 9. The item-5 answer, which is the part that transfers

| strand | what is the friction, and is it still there? |
|---|---|
| **S1 merger arbitrage** | **The friction is real and it is not an access barrier - the payoff itself is a short uncovered index put, so someone must bear a loss that arrives in severe market declines. Whether it is still there is not established**: the evidence closes in 1998 and the vantage line is 2025-02-10. |
| **S2 index reconstitution** | **The friction was the market's capacity to absorb a predictable demand shock, and it expired because capacity grew** - not because any rule changed. |

**Four families now.**

| family | the friction | still there? |
|---|---|---|
| 2 - insider | uneconomic to arbitrage: concentration in illiquid names | yes, and that is why the edge is uncollectable |
| 4a - perp carry | arbitrage capital constrained by regulation and margin | yes |
| 4b - equity VRP | a restriction on who could sell options | **no** - the alpha ended when the restriction did |
| **3a - merger arb** | **not a friction at all - a genuine short-option risk** | **unestablished** |
| **3b - index flow** | **market capacity to absorb a predictable shock** | **no** - capacity grew |

> **S1 is the first strand in four families where the answer is not "the premium was the friction."**
> It is *"someone must hold a risk that arrives all at once"* - the answer packet 8 expected to find
> in family 4 and did not.
>
> **And it is the one this packet could not verify.** The confirmation of a disclosed prior (T1
> section 0a) required the higher bar; the higher bar was a post-vantage measurement of a held
> position; that measurement does not exist at this vantage.
