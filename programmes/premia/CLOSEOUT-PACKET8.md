# Close-out - packet 8, family 4 scoping

Programme: premia. **SCOPED, NOT OPEN.** The gate in `ROADMAP.md` is unchanged and this packet did
not address it.

| task | artefact | commit | sha256 (first 16) |
|---|---|---|---|
| T1 | `KILL-CONDITION.md` **sealed alone before anything was read** | `2d07ad7` | `2a87dc4c7a34e6c3` |
| T2 | `PRIORS.md` | `69a2723` | `a4b4bf7eae7e84d1` |
| T3 | `MECHANICS.md` | `855e8f4` | `d25733d0702df2a3` |
| T4 | `TAIL.md` | `317201d` | `6a181f9cadbc70fb` |
| T5 | `SCOPING-VERDICT.md` | `798e5ec` | `25a4e734dfde063a` |
| T5 | `registry/F4-PREMIA-SCOPING.md` | `4e61a22` | `df671bcbed24c88f` |

Every commit was a **create** returning **201** and every file was verified by reading the blob
back through the Git Data API - a different path from the one that wrote it.

---

## 1. T5's verdict, against T1 verbatim

**T1 section 7, sealed 2026-08-24 before any source was read:**

> "A strand survives scoping only if ALL of the following hold: 1. `E(K) >= 5.00 pp` over a
> **documented** benchmark... 2. `E(K) >= 3 x F/K`... 3. `K_min` computed, and `K_min / 0.15`
> **reported as a number**... 4. Every venue in the strand's set **passes section 3.1** exclusion.
> 5. `L` established **including the unhedged-leg component**. 6. Documented tail frequency **at or
> below `p*/3`**. 7. Tail **correlation with carry** established or excluded. 8. Carry from a
> **post-2023-01-01**, >= 24-month, both-signs sample **with dispersion**. 9. Every figure traceable
> to a **named, dated source that was read rather than summarised.**
>
> **Missing any of 1-4 is a KILL. Missing 5-9 is COULD NOT ESTABLISH.**"

**Benchmark, documented as required:** Bank of England Bank Rate **3.75%** (effective 18 Dec 2025).
**The floor is therefore a net total return of 8.75% p.a.**

| strand | verdict | why |
|---|---|---|
| **S1** perpetual funding carry | **COULD NOT ESTABLISH** | items 1-3 not evaluable (no magnitude for the strand; no published fixed cost); items 5, 6 fail |
| **S2a** equity index VRP | **KILL** | item 1 fails on a **measured** magnitude of approximately zero |
| **S2b** Bitcoin VRP | **COULD NOT ESTABLISH** | magnitude is a variance wedge, not a return; no post-vantage evidence; venue changed ownership |

> **Family 4 does not survive scoping. No strand survives, and the only strand whose magnitude was
> actually measurable was killed.**

---

## 2. MEASURED

By this project, in this packet. The list is short, and that is the honest shape of a
documentation-only scoping.

- **HTTP status behaviour of six venue and source hosts**, each with a paired control:
  Binance `202`/0 bytes for a real *and* an impossible article, with `X-Amzn-Waf-Action: challenge`;
  `www.deribit.com` returning **byte-identical** 12,155-byte responses (md5 `fc19b206...`) for a KB
  article, an impossible path and the terms of service; GitBook soft-404s returning `200` with a
  `# Page Not Found` body; arXiv, CourtListener, Crossref, OpenAlex, BIS and chicagofed each
  controlled with an impossible identifier.
- **Null-instrument capability of four search endpoints.** Crossref's `total-results` returned
  **3,766,699** for a nonsense query and is **not** a null instrument. arXiv exact-phrase and
  CourtListener exact-phrase **are**, controlled both ways (`"FTX Trading"` -> 515;
  `"zzqxwv nonexistent control phrase"` -> 0).
- **Term counts in documents this project retrieved and extracted**, each with in-file positive
  controls: the zero-mentions of insurance fund / socialised loss / clawback / ADL / default /
  custody across both S1 papers (controls 210/56, 123/8, 202/119); the zero-mentions of historical /
  incident / frequency / FTX / March 2020 in the ADL paper (controls 259, 224); the zero-mentions of
  the same mechanisms in the FSB report (controls 217, 30); the **zero** mentions of
  "auto-deleverag" in the BitMEX pleading body (controls 573, 64).
- **The arithmetic against T1's thresholds**, including the `p*` inversion.
- **File integrity of six commits**, by sha256 through an independent read path.

## 3. INFERRED

**A venue's published documentation is INFERRED from that venue's own account of itself, not
measured by this project.** So is every figure from a paper: a paper is an instrument and its
sample period is its vantage.

- **Every venue mechanic in `MECHANICS.md`** - Hyperliquid's hourly funding, its
  `clamp(interest - P, +/-0.0005)` formula, its 4%/hour cap, its 2/3-maintenance-margin backstop
  taking all cross margin, its ADL sorting index; OKX's ADL 0-5 priority "increases with higher
  unrealized profit"; Deribit's `socialized` / `session_tax_rate` / `session_bankruptcy` settlement
  fields.
- **Every magnitude in `PRIORS.md`** - the ~7% dated-futures basis (BIS WP 1087); instrument A's
  6.38% pooled and 1.11%/0.28% post-break years (He et al. Table 7); the equity option alpha
  "indistinguishable from zero" (Dew-Becker & Giglio); BVRP 0.14 (Almeida et al.).
- **Every tail figure in `TAIL.md`** - $2.047bn ADL notional on 10 October 2025 and its three
  waves; the 22%-per-10% carry-to-sell-liquidations regression; "liquidated in over half of the
  months" at 10x.
- **The counter-finding** that delevered shorts were ex post profitable, which is a paper's
  characterisation of an X thread and is inferred at two removes.
- **Allegations in the BitMEX pleading** - the $800M liquidation during a 25-minute outage, the
  insurance fund "almost never drawn upon." A pleading is a primary document whose contents are
  allegations, and the case's disposition was not established here.

## 4. ASSUMED

**Every threshold in T1**, and that is correct rather than a weakness - a threshold set in advance
is a judgement by definition.

- 5.00 pp absolute floor, from a deep-speculative-grade unsecured credit analogue.
- The one-third principle, used twice (fixed costs and tail).
- 196 attention-hours/year at GBP 60/hour.
- 25% of venue capital as a material loss event; 15% single-venue and 30% aggregate survivability
  caps; the non-independence reasoning behind 30 rather than 45.
- 3-year maximum holding period.
- The 2023-01-01 vantage floor - **and its asymmetry**, which is the one place family 2's rule was
  deliberately broken.
- 24 months, both signs, with dispersion, as the minimum carry sample.

**One thing that is ASSUMED and should not be:** T1 section 0a disclosed that I hold general prior
knowledge of this sector and could not claim family 2's blindness. That disclosure stands. The
mitigation held - every threshold derives from a stated cost or risk quantity, none from a
remembered return - and the outcome is some evidence for it: **the floor bound on both strands, and
two of the analogue's cells cleared it**, which is not what a threshold quietly fitted to be
clearable, or to be unclearable, would have produced.

---

## 5. The item-5 answer, one sentence per strand

**This is the part that transfers to family 3.**

- **S1 - perpetual funding carry:** it persists because arbitrage capital is constrained by
  regulation and margin, and because the arbitrageur can be forced out of the position before
  convergence.
- **S2a - equity index variance risk premium:** it did not persist - it was a restriction on who
  could sell options, and it decayed to zero as the restriction eased.
- **S2b - Bitcoin variance risk premium:** not established; no source read explains why it would
  persist, and no post-vantage estimate of it exists.

> **Three families, one answer: the premium was the friction.** Packet 8 expected *"someone must
> warehouse a risk nobody wants"* and pre-committed that finding access friction instead would be
> family 2's result again. **It is, twice.**

**Proposed, not made:** ROADMAP screen item 5 currently asks why a *published anomaly* survived
publication. The stronger form earned here applies to **any** documented edge: *what is the
friction, and is it still there?* **That change is not made in this packet.** Packet 7 established
that what goes into the screen is Walton's ruling.

---

## 6. What is not knowable from public sources

**The list is shorter than expected, and the reason matters.**

### 6.1 Genuinely not established anywhere reachable

- **Binance's** funding formula, cap, margin, insurance fund, ADL and fee schedule. The venue whose
  figures underpin instrument A. AWS WAF challenge at this vantage, over raw HTTP and over the
  browser network stack.
- **The trigger** for a Deribit bankruptcy session, and its fee and margin schedules - single SPA
  shell.
- **The disposition** of the BitMEX civil class actions.
- **Whether any documented ADL event has ever fired against an identified delta-neutral book.**
- **Christin, Routledge, Soska & Zetlin-Jones (2022)**, *The crypto carry trade* - cited by BIS WP
  1087, not located. Could not establish, never "no evidence found."
- **The Jia et al. X thread** itself, as opposed to the paper's characterisation of it.

### 6.2 The category T1 did not have: **knowable, and out of scope**

> **The tail's frequency is not unknowable. It is unretrieved.**
>
> - **Hyperliquid's public REST API** labels ADL fills. Campbell, Hey, Moallemi & Nutz
>   reconstructed the entire October 2025 event from it.
> - **Deribit's `public/get_last_settlements_by_currency`** returns `socialized`,
>   `session_tax_rate` and `session_bankruptcy` per settlement, with paging.
>
> **Neither was called, because packet 8 forbids data pulls.** Two venues out of two whose
> mechanisms are documented also publish the event stream. **T5's could-not-establish on tail
> frequency is a scope boundary of this packet, not a limit of public knowledge**, and it is the
> cheapest open question here - the same shape as packet 7's McLean & Pontiff Internet Appendix.

---

## 7. Recorded and parked - not amended, because T1 is sealed

Standing rule: *never change a registry verdict, figure or `revive_if` during this run; record it
and park it.* Three items. **None is corrected below.**

1. **T1 section 2.1 does not enumerate forced liquidation.** It defines a material loss event as
   removal *"by an action of the venue or its backstop rather than by the market movement of the
   position itself."* A liquidation is triggered by market movement and executed by the venue's
   engine, so it falls between the two. T1 section 3.3's unhedged-leg clause reaches the exposure,
   but by the wrong route. **Material**, because at 10x the futures leg would have been liquidated
   *"in over half of the months"* - which is not a tail but the modal outcome.
2. **T1 does not enumerate venue outage.** If the venue is unreachable you cannot add margin,
   unwind or re-hedge. No venue documentation read mentions outage as a loss channel either.
3. **T1 section 1.1 defines `E` per unit of deployed capital, and the literature does not report
   that.** He et al. annualise by the Lucca & Moench convention over active periods; the strategy is
   active 20.06% of the time. The convention was checked rather than assumed, and it turns out the
   figure is compatible - but T1 did not say which convention it required, and a different paper
   could have made the same number mean something else.

---

## 8. Instrument findings worth carrying to the method skill

Four, each of which would have produced a false result.

1. **A result count is not a null instrument unless controlled.** Crossref returned 3,766,699 hits
   for a nonsense query. arXiv and CourtListener exact-phrase search return zero and are usable.
2. **The arXiv Atom feed carries a feed-level `<updated>` equal to the query time.** Parsing the
   first `<updated>` in the response returned *today* for a 2024 paper. **Every paper would have
   looked post-vantage and the vantage rule would have passed everything it exists to stop.**
3. **A single-page application returns one shell for every path.** Three different Deribit paths
   returned byte-identical responses. A `200` from such a host carries no information about whether
   a document exists, and only a **byte-identity control** shows it.
4. **A court-filing full-text hit can be a news article stapled to a pleading.** All the
   "auto-deleveraging" hits in three BitMEX class actions were inside an attached CoinDesk exhibit;
   the pleading body contains the term **zero** times against positive controls of 573 and 64.

---

## 9. What this packet did not do

No exchange account. No API key. No test position of any size. No live funding rate, order book or
price series. No backtest, no historical carry computation, no expected-value model. No
pre-registration of a study. **No determination of whether Walton can legally or practically access
any venue** - `MECHANICS.md` records what venues state and determines nothing.

**The gate is not lifted by this packet.**
