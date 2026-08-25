# Close-out - packet 9, family 3 scoping

Programme: flow. **SCOPED, NOT OPEN.** The gate in `ROADMAP.md` is unchanged and this packet did not
address it.

| task | artefact | commit | sha256 (first 16) |
|---|---|---|---|
| T1 | `KILL-CONDITION.md` **sealed alone before anything was read** | `8f3c0a9` | `c62c13ab11236f1b` |
| T2 | `PRIORS.md` | `91ecdae` | `55ef539f83aab686` |
| T3 | `MECHANICS.md` | `a9f1584` | `1a2923fdaf3225c4` |
| T4 | `BREAKS.md` | `44f83b8` | `bc950e6dde50f097` |
| T5 | `SCOPING-VERDICT.md` | `353a67d` | `92cf04fbca9d0fe0` |
| T5 | `registry/F3-FLOW-SCOPING.md` | `8cc8a6a` | `8cbf6645bf1d2174` |

Every commit a **create** returning **201**, every file verified by reading the blob back through
the Git Data API - a different path from the one that wrote it.

---

## 1. T5's verdict, against T1 verbatim

**T1 section 8, sealed 2026-08-25 before any source was read:**

> "A strand survives scoping only if ALL of the following hold: 1. `E >= 3.5 pp` over the **higher**
> of a documented cash and a documented passive benchmark. 2. `p <= p*/2`... 3. Every position
> sizeable so its break costs `<= 2.0%` of deployed capital. 4. No documented cluster exceeding
> `f_max`, evaluated at the **upper quantile** of `L`. 5. `n_min` computed and **available
> simultaneous positions >= `n_min`**. 6. `K_min` computed and **reported as a number**. 7. Magnitude
> from a sample **closing after the strand's vantage line**. 8. **All three components** of the break
> distribution established. 9. Every magnitude a **measurement of the position Walton would hold**.
> 10. Every figure traceable to a **named, dated source read rather than summarised**.
>
> **Missing any of 1-5 is a KILL. Missing 6-10 is COULD NOT ESTABLISH.**"

**Benchmark, documented as required:** Bank of England **Bank Rate 3.75%** (effective 18 Dec 2025;
impossible page on the same host returned `404`). The **passive** half was not established, and since
T1 requires the *higher* of the two, **the floor is applied as a lower bound of 7.25% net** - which
can produce a fail but not a pass. Nothing reached it.

| strand | verdict | why |
|---|---|---|
| **S1 merger arbitrage** | **COULD NOT ESTABLISH** | items 6-9 fail; items 1-5 were **not evaluable**, so nothing in the kill group was missed |
| **S2 index reconstitution** | **COULD NOT ESTABLISH** | item 9 fails on units; the **deletion leg is dead on a measured figure** (+0.1% abnormal return, so **-0.1% gross** to a short position, before costs) |

> **Family 3 does not survive scoping. Neither strand is killed on its arithmetic, because in
> neither case was the arithmetic evaluable - which is itself the finding.**

---

## 2. Did T4 decide the packet, or did something fail first?

**Something failed first.** Packet 9 said T4 *"decides the packet, and unlike packet 8 it should
actually get the chance to."* **It did not get the chance.**

| stage | returned | decisive? |
|---|---|---|
| **T2** | **not one magnitude passes section 6.1** | **first** - the return side was could-not-establish before any break evidence was sought |
| **T3** | vantage line **2025-02-10**; newest S1 figure closes 2020 | **second, independently** |
| **T4** | all three break components fail | third |

**But T4's status differs from packet 8's, and flattening them would be the dishonest version.**
Packet 8's tail pre-commitment fired on nothing and was recorded as **untested**. **T4 here produced
an independent finding that would have capped any strand had the return side survived** - the break
distribution fails all three components of a rule sealed before the evidence.

> **T4 was not load-bearing. It was load-*capable*.** A rule that would have bound is evidence the
> rule is well-formed; a rule that never engaged is not.

**Three packets, three times the pre-committed hard half never became load-bearing.** That is now a
pattern about **where these families fail**: on **whether the published number is the number you
would earn**, long before they fail on risk.

---

## 3. MEASURED

By this project, in this packet.

- **HTTP status behaviour of eleven host classes**, each with a paired control. **Four return the
  same status for a real document and an impossible one** - `ftc.gov` (`403`, 453 B both),
  `spglobal.com` (`403`, 2,011 B both), `sec.gov` (`403`, 4,819 B both), and `govinfo.gov` (**`200`
  for a document that does not exist**, separated only by `Content-Type`).
- **Null-instrument capability**: `federalregister.gov` (impossible term -> count **0**, real term ->
  76) and arXiv exact-phrase (impossible -> 0, `"merger arbitrage"` -> 2) **are** null instruments;
  Crossref is not, per the finding carried from packet 8.
- **Term counts in retrieved documents, with in-file positive controls**: `discretion` / `front-run`
  / `predictab` each **0** in the Russell methodology against `index` 449, `Russell` 546,
  `reconstitution` 68; `methodolog` **0** in Greenwood & Sammon against `migration` 31,
  `liquidity` 15, `predictab` 10.
- **The breadth schedule** computed from T1 section 3.1's sealed formulas: minimum **48** simultaneous
  positions at the illustrative shape, **57** at T1's own break-rate ceiling, **1,765** at a 10%
  break rate.
- **File integrity of six commits**, by sha256 through an independent read path.

## 4. INFERRED

**A published break rate is INFERRED from that study's instrument on that study's sample**, and a
provider's or agency's document is that party's account of itself.

- **Every magnitude in `PRIORS.md`** - M&P's +4%/yr (1963-1998), Greenwood & Sammon's 7.4% -> under
  1%, Shleifer's 1976-onward abnormal returns.
- **Every procedural fact in `MECHANICS.md`** - the 30-day and 15-day waiting periods, the Second
  Request extension running from substantial compliance, the March 2020 end of routine early
  termination, the Russell rank-day rule, the five-week announcement lead, banding at plus/minus
  2.5% and 0.5%, the published predictive index data.
- **Every clustering mechanism in `BREAKS.md`** - the short-put payoff shape, the 2008 financing
  withdrawal, the 2020 common-cause MAE trigger.
- **The HSR filing counts** - FY 2021 3,520 and FY 2022 3,152 transactions - which are the agencies'
  own counts of their own filings.

## 5. ASSUMED

**Every threshold in T1**, and that is correct rather than a weakness.

- Return floor **3.5 pp** (from the three-year recovery horizon, which is the judgement; the
  arithmetic from it is not).
- Per-deal max **2.0%**; cluster max **10.0%** rolling 12 months.
- Fixed-cost share **`phi` = 0.10**.
- The Poisson-mode criterion at **`np >= 3`** and the **`SD <= mu`** criterion in the breadth term.

**Six of T1's twelve parameters were DERIVED rather than assumed** - `p*`, `f_max`, the `p*/2`
ceiling, and all three breadth routes - which is what distinguished this condition from the previous
two. **None of the six could be evaluated**, because every input they need is unestablished.

---

## 6. The item-5 answer, one sentence per strand

- **S1 - merger arbitrage:** the friction is **not a friction at all but a genuine short-option
  risk** - the payoff behaves like selling an uncovered index put, so someone must bear a loss that
  arrives in severe market declines - **and whether it is still there could not be established**,
  because the evidence closes in 1998 and the vantage line is 2025-02-10.
- **S2 - index reconstitution:** the friction was **the market's capacity to absorb a predictable
  demand shock**, and it expired because **capacity grew**, not because any rule changed.

### 6.1 Four families of that question, and the pattern is worth more than any single verdict

| family / strand | the friction | still there? |
|---|---|---|
| 2 - insider | uneconomic to arbitrage; concentration in illiquid names | **yes**, and that is why the edge is uncollectable |
| 4a - perpetual carry | arbitrage capital constrained by regulation and margin | **yes** |
| 4b - equity variance premium | a restriction on who could sell options | **no** - the alpha ended when the restriction did |
| 3b - index flow | market capacity to absorb a predictable shock | **no** - capacity grew |
| **3a - merger arbitrage** | **not a friction: a real short-option risk somebody must hold** | **unestablished** |

> **Four of the five are "the premium was the friction." S1 is the first that is not** - and it is
> the one this packet could not verify.
>
> **The pattern that transfers is not "frictions expire."** It is that the question *"what is the
> friction, and is it still there?"* **sorts these families cleanly on the first half and stalls on
> the second.** What the friction *is* has been establishable in all five cases from published work.
> Whether it is *still there* has been establishable in three of five, and in this packet in neither.

### 6.2 A prior that was right on the answer and wrong on the mechanism

T1 section 0a disclosed that I expected index decay. **The decay is confirmed. The mechanism I
expected is not.** I expected methodology changes made to reduce predictability; the paper considers
**five** explanations and methodology change is not among them (`methodolog` appears **zero** times,
controlled), and the provider's own methodology never states an anti-front-running purpose for any
rule (`front-run` **zero**, controlled). **Banding's stated purpose is "to reduce unnecessary
turnover."**

**Right answer, wrong reason** - the project's own check, firing on my own prior.

---

## 7. Unretrieved versus unknowable, and a third category

### 7.1 UNRETRIEVED - public, and blocked at this vantage

**T5 must not convert any of these into an absence of evidence.**

1. **Mitchell & Pulvino (2001), the body** - bronze OA at Wiley, one location, `403` with
   `Cf-Mitigated: challenge` over raw HTTP **and** the browser stack. Plausibly contains the break
   rate, the severity **and** the section 6.1 test.
2. **Billman & Salop (2022)** - the only complete second-request outcome database, 2001-2020,
   analysed *"across Presidential Administrations"*. Landing page `200`, PDF endpoint `403`.
3. **Officer (2003)** and **Jetley & Ji (2010)** - closed access.
4. **Every merger agreement on EDGAR** - break fees, MAC clauses, outside dates, financing
   conditions. `403`, control identical.
5. **FTC/DOJ HSR Annual Reports, appendix A** - `403`, control identical.
6. **S&P US Indices methodology** - `403`, control identical.

### 7.2 UNKNOWABLE from public sources

1. **A break rate over the universe a retail merger-arb book trades.** The published denominators
   are all-HSR-filings or conditional-on-second-request; **neither is the right one, and retrieving
   the blocked source would not fix it.**
2. **Loss-given-break as a distribution** - it depends on each target's own pre-announcement run-up.
3. **The fraction of concurrent positions breaking in any historical cluster.** One number, and
   nobody publishes it.
4. **Any break rate under the post-2025-02-10 regime.** The regime is about eighteen months old;
   **a low-frequency event under an eighteen-month regime cannot have a published rate yet.** This is
   the only item here that is unknowable because of **time** rather than access.

### 7.3 SCOPE BOUNDARY - purchasable, and this packet forbids buying it

> A break distribution over the correct universe plausibly sits in a **commercial deal database**.
> Packet 9 forbids calling one. **That is a boundary of this packet, and it is not the same as 7.2.1**
> - 7.2.1 says the *published literature* lacks the figure; this says a *purchasable source* likely
> has it.

---

## 8. Two defects in the sealed condition - recorded, not patched

T1 section 6.3 required the question *"what loss channel does this condition not name?"* be asked
explicitly. **It was, and it found things.** Per the standing instruction and packet 8's precedent,
**the sealed text stands as written and wrong.**

1. **T1 section 5.1's S2 vantage line cannot be drawn.** It was defined by *"the most recent
   methodology change that the index provider itself states was made to reduce predictability,
   front-running or trading impact."* **Providers do not make that statement** (controlled, T3
   section S2.3). **No bite**: S2's only magnitude is adverse and adverse evidence does not expire,
   so a line that cannot be drawn cannot exclude evidence it was never going to exclude.
2. **T1's payoff has no third state.** Every formula - `p*`, `f_max`, all three breadth routes -
   assumes *complete at `s`* or *break at `L`*. **The renegotiated deal, completing at a reduced
   price, is common and is a third outcome**, and section 3.3 of `BREAKS.md` shows a common-cause MAE
   event makes that renegotiation available to many acquirers at once. **This is structural**: it
   makes every sealed formula a first-order approximation with an unsigned error. **No bite on this
   packet's outcome**, because the evidence failed on grounds no payoff model would rescue.

**Two further unnamed channels**, recorded in `BREAKS.md` section 6: **duration** (T1 bounds `mu`
"per deployment period" and never bounds the deployment period, while the HSR rule makes it
open-ended) and **borrow recall on the short leg** (the same unhedged-leg shape family 4 reached only
by accident).

---

## 9. What this packet did not do

No broker account, no deal database subscription, no screen of live situations. No current spreads,
prices or deal terms. No backtest, no expected-value model, no historical return computation. No
pre-registration of a study. **No determination of what Walton can access or afford.**

**The gate is not lifted by this packet.** And per T5 section 7: **a "survives" here would still have
meant "not now"**, because family 3's gate rests on the loss distribution and on Walton's
circumstances rather than on whether the premium exists - and T4's clustering finding sharpens
rather than softens that.
