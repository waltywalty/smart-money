# C1 — The fee-ceiling registry sweep

**Date:** 2026-08-14. **Packet:** coworkpacket3autonomous, Phase C, task C1.
**Scope:** every registry entry whose verdict rests on a band where `p(1−p) < 0.05` — roughly
`p > 0.947` or `p < 0.053`.
**Nothing is changed here.** No verdict, no figure, no `revive_if`. This is a reading of the
registry against A1's fee finding, and where an entry looks size-dependent it goes to `PARKED.md`.

---

## The finding, before the table

**Not one registry entry states the order size its cost model assumed.** The column the packet
asked me to fill is empty for every row — not because the entries were careless, but because every
cost model in this project is a **per-contract continuous function**, `0.07·p·(1−p)`, which has no
size parameter at all. A per-contract fee cannot be size-dependent by construction.

A1 established that the real schedule is not that function. The trade fee rounds **up to a
centicent per fill**, and a separate balance-precision rounding fee — **$0.01 for a non-direct
member** — sits underneath it. At the extremes the true continuous fee is tiny and that $0.01 floor
dominates completely:

| price | continuous `0.07·p·(1−p)` per contract | effective at **1** contract | effective at **100** | ratio |
|---|---:|---:|---:|---:|
| 0.50 | 1.7500¢ | ≈ 1.75¢ | 1.7500¢ | 1.14× |
| 0.97 | 0.2037¢ | **1.0000¢** | 0.2100¢ | **4.76×** |
| 0.99 | 0.0693¢ | **1.0000¢** | 0.0700¢ | **14.29×** |
| 0.999 | 0.0070¢ | **1.0000¢** | 0.0070¢ | **143×** |

So the honest way to state the audit's premise: **the registry's cost models assumed no size, which
is equivalent to assuming the continuous fee — i.e. to assuming infinite size.** The error, where it
exists, runs the *opposite* way from the packet's worry. The registry did not kill things with an
over-large small-size fee; it priced them with an **under-large** fee that is only reachable at
size. An entry that survived on paper might not survive at one contract.

That reverses which entries are at risk, and the table reflects it.

---

## The table

| entry | verdict | price band | assumed size | fee ceiling binding? | verdict size-dependent? |
|---|---|---|---|---|---|
| **H9** | KILLED | ≥ 98¢, actual resting ask 99.9¢ | **none stated** (continuous) | **Yes, decisively** — at 1 contract the $0.01 floor is **10× the entire 0.1¢ gross edge** | **No, but for a new reason** — see below |
| **H53** | KILLED DECISIVELY | ask ≤ 5¢, `p(1−p) ≤ 0.0475` | **none stated** (continuous, ≈0.07¢ at 1¢) | **Yes** — true fee at 1 contract is 1.00¢, not 0.07¢ | **No.** The correction makes the kill *stronger* |
| **H52** | KILLED | mean fill 2.17¢, `p(1−p) = 0.021` | **none stated** | Yes in magnitude | **No.** Kill rests on −15¢ adverse selection, ~700× the fee |
| **H55** | COULD NOT ESTABLISH | ask 0.93–0.98 (upper half in band) | **none stated** | Partly | **Not testable** — the band was unpopulated at the tested lead |
| **H64** | COULD NOT ESTABLISH | 93–98¢ | **1 contract, implicitly** — its code charged a flat 1¢/rung | **Yes** — and it charged the ceiling without knowing it | **Yes in magnitude, no in verdict.** See below |
| **H15** | KILLED | negRisk sum 0.9970 | **none stated** | **Yes** — a 0.30¢ gross gap against a 1.00¢ per-leg floor at 1 contract | **Possibly.** Flagged |
| **H46** | KILLED as a trade | box legs at 0.99–0.9955 | **none stated** | Yes per leg | **No.** Kill is settlement-criteria divergence, not cost |
| **H10** | KILLED | quotes across 1–95¢ | **none stated** | No | **No.** Kill is *median size at bid = 5 contracts* — a depth kill, and depth is what fee amortisation needs |
| **H61** | KILLED | mid ∈ [80,100)¢ | **none stated** | Only in the top of the band | **No.** Kill is latency: +1.64/+3.12/+5.00¢ against the buyer at 1/2/3 minutes |
| **H37** | KILLED out of sample | mean ask 0.98 on winners | **none stated** | Not load-bearing | **No.** Kill is a −2.44¢ return with CI [−9.3, +4.4] |
| **H39** | KILLED as executed | `last_price` converged to 0.01/0.99 | n/a | n/a | **No.** Instrument failure, not an economic verdict |
| **H35** | KILLED | winning band ≥ 0.95 at issue time | n/a | No | **No.** Kill is a timing finding |
| **H42** | KILLED | maker/taker on 1.42¢ mean spread | **none stated** | No — spread ≫ fee | **No** |
| **H54** | KILLED | favourite at ≈ 0.50 implied | — | **Out of scope** — `p(1−p) = 0.25` | — |
| **H56** | KILLED (THE HURDLE) | broad; not an extreme band | **none stated** | Out of scope by band, **in scope by consequence** | **Unknown — and it is the important one.** See below |

---

## The three entries that need saying more about

### H9 — the ceiling is binding, and it kills the trade a second time

H9's recorded kill is economic: *"the only resting ask on the safe outcome is 99.9¢, so the taker
edge is 0.1¢. No reversal rate rescues a tenth of a cent."* That reasoning never mentions fees, and
it did not need to.

A1 now shows the fee alone would have killed it at small size: at 99.9¢ the balance-rounding floor
is **1.00¢ per contract at one contract**, ten times the entire gross edge. At 100 contracts the
fee falls to 0.0070¢ and the 0.1¢ edge survives it — which is the one place in this registry where
the packet's "killed at one contract, not killed at one hundred" pattern actually appears.

**It is still not a revival.** H9's kill is about economic significance and capital lockup: the
68,373 contracts resting at 99.9¢ are $68,300 of collateral earning $68 gross. That is a
capital-days question, not a fee question, and A1 does not touch it. Recorded, verdict untouched.

### H64 — it charged the ceiling by accident, and the accident was in the right direction

H64 charged a flat **1¢ per rung** and its write-up explained this as Kalshi rounding fees up to
whole cents on the order total. That explanation is wrong (**P5**). But the *number* is what a
non-direct member actually pays **at one contract** in the 93–98¢ band — A1's schedule gives
exactly 1.0000¢ there. H64 charged the correct fee for the wrong reason, at a size it never stated.

At size the fee falls to about **0.33¢ per contract** at p = 0.95. Substituting it moves H64's mean
from **+0.5135¢** to roughly **+1.18¢** — which is still well inside its own interval
**[−1.4469, +2.1816]** and changes no robustness check: leave-one-series-out still ranges
−0.2227 to +1.0963, split-half still disagrees (+0.2660 vs +0.9709), and the rung-level estimate is
still negative (−0.9457) against a positive event-level one.

**The verdict is unaffected and is not touched.** The magnitude is size-dependent and that is now
on the record.

### H56 — the hurdle is the entry this audit is really about, and it is out of band

H56 is **not** an extreme-band entry, so it falls outside C1's stated scope. It is listed anyway
because it is the entry whose size assumption matters most: −4.03¢ / −4.39¢ is the bar every other
idea in this registry is measured against, and it was computed with a **size-free** cost model.

If the hurdle was priced at the continuous fee, it is the *size-infinite* hurdle, and every idea
killed against it was killed against a bar that a one-contract trader could never reach. If it was
priced implicitly at one contract, the bar is too high at size. **Which of these is true has not
been determined here**, because it requires reading H56's estimator rather than its registry entry.

This is precisely the Phase D candidate the packet names — *"the hurdle re-measured at size"* — and
C1's contribution is to say that the question is real and unanswered, not to answer it. Parked as
**P11**.

---

## Entries flagged to `PARKED.md`

| | why |
|---|---|
| **P11** | H56's hurdle was computed with a size-free cost model. Which size it implies is undetermined, and every kill in the registry calibrates against it. |
| **P12** | H15's negRisk gap (0.30¢ on a 0.9970 sum) sits below the 1.00¢ per-leg small-size floor and above the ~0.07¢ large-size fee. Whether the kill survives at size was not determined. |

**No entry was found that was killed at one contract and would not have been killed at one
hundred.** H9 comes closest and fails for an unrelated reason. The packet anticipated finding
`revive_if`s come due; the honest answer is that the registry's cost models were size-free, so the
failure mode it was looking for could not have been introduced in the first place — and the
opposite failure mode, pricing at a fee only reachable at size, is the one now on the table.
