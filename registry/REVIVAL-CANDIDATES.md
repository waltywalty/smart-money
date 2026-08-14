# C5 — Revival candidates, ranked. A list, and nothing else.

**Date:** 2026-08-14. **Packet:** coworkpacket3autonomous, Phase C, task C5.
**Nothing is proposed and nothing is revived.** Every verdict and every `revive_if` in the registry
is untouched. This ranks what a larger sample would change, using the sample **A2 and B1 actually
measured** rather than the sample optimism would like there to be.

## What is actually available now

| | |
|---|---:|
| settled Kalshi markets, historical path | **7,269,014** |
| unique events | **351,653** |
| series with data | 6,703 |
| earliest `close_time` | **2021-07-01** |
| latest `close_time` covered | 2026-06-14 (the `/historical/cutoff`) |

With `result`, `settlement_ts`, `settlement_value_dollars`, strike fields and final quotes on every
row, plus `fee_type`/`fee_multiplier` joined per series. Candlesticks reach the same depth
(A2 §A2.4). **What it does not supply: Polymarket, wallets, trades, or resting depth.**

That exclusion decides most of this list.

---

## Rank

### 1. H56 — THE HURDLE, re-measured on a materially earlier period

- **Original reason it closed:** not a kill for lack of data — `revive_if` reads *"Never as stated.
  To move the number, re-measure on a disjoint venue or a materially later period."*
- **What the larger sample changes:** it supplies a **materially earlier and wider** period, which
  is the same test in the other direction — 2021-07 → 2026-06 against H56's original window,
  across 6,703 series rather than a handful.
- **Sample now available:** the full 7.27M-market universe; the macro and weather series H56 cares
  about hold 137,299 rows between them.
- **Cost to re-run:** low. The data is collected; this is an estimator run, not a fetch.
- **Why it ranks first:** −4.03¢ / −4.39¢ is the bar every other entry in this registry is
  calibrated against, and C1 has just established that it was computed with a **size-free** cost
  model (**P11**). A hurdle that is wrong is wrong everywhere at once.

### 2. H9 — its stated sample bar is now clearable, and it still will not matter

- **Original reason:** killed on economics — *"the only resting ask on the safe outcome is 99.9¢,
  so the taker edge is 0.1¢."*
- **But its own bar was a sample bar:** *"At 98.0¢: n≥150. At 99.25¢: n≥400. At 99.9¢: n≥3000."*
  It closed at **63 markets, 0 reversals**.
- **Sample now available:** n ≥ 3,000 near-certainties with settlement outcomes is comfortably
  inside 7.27M markets. **The bar that was out of reach is now cheap.**
- **What it changes:** the reversal *rate*, to the precision H9 asked for. **It does not change the
  verdict**, because the kill is that 0.1¢ gross does not survive capital lockup, and no reversal
  rate rescues a tenth of a cent. C1 adds that at one contract the fee floor alone is 10× the edge.
- **Cost:** low. **Value: the number, not the verdict.** Ranked here because it is the clearest
  case in the registry of a bar becoming reachable, and it is worth recording that reaching it
  still would not revive anything.

### 3. H54 — the selection check that killed it can now be run at scale

- **Original reason:** the +7.23¢ favourite edge collapsed to **+0.82¢** once restricted to the 51
  of 61 ladders where every rung had a candle at the lead. The effect lived in 10 ladders with a
  missing tail candle, and the favourite won 9 of those 10.
- **What the larger sample changes:** n. 61 complete ladders became the whole study; B1 holds
  **351,653 events**, and complete-ladder detection is a row-count check against the event's rung
  count, computable offline.
- **Sample now available:** every mutually-exclusive ladder that settled before 2026-06-14.
- **Cost:** low–medium. Requires candlestick fetches per rung for the entry price — the market rows
  alone give settlement but not the lead quote.
- **Caveat that keeps it at rank 3:** the finding that killed it was a *selection* mechanism, and
  selection does not weaken with n. A bigger sample measures the same artifact more precisely.

### 4. H53 — decisive already; the larger sample sharpens a bound rather than moving it

- **Original reason:** KILLED DECISIVELY at n=128, zero winners, exact one-sided 95% upper bound
  **2.313%** against a **2.68%** break-even.
- **What changes:** H54 later found **1 of 147** rungs at ask ≤ 5¢ settled YES (0.68%), correcting
  H53's "never won once" phrasing. B1 makes the far-OTM YES rate measurable at n in the tens of
  thousands rather than the hundreds.
- **Cost:** low. **It cannot reverse the verdict** — 0.68% is far under 2.68% — but it converts a
  rule-of-three bound into a measured rate, and C1 notes the fee correction pushes the kill
  *further* from break-even at small size.

### 5. H3 — the portfolio version, but on the wrong venue

- **`revive_if`:** *"Re-run as a PORTFOLIO on resolved-market history rather than trader-sampled
  tape."* Its bar: *"A band needs n≥100 before it means much; the whole curve needs the cheap end
  (0–20¢) populated."*
- **What is available:** exactly that shape of data — resolved-market history with entry quotes —
  at n≫100 per 5¢ band, cheap end included.
- **Why it is rank 5 and not rank 1:** **H3 is a Polymarket hypothesis.** B1 is Kalshi. Running it
  on Kalshi is not a revival of H3; it is a **new hypothesis** that happens to share H3's shape,
  and it needs its own pre-registration. Recorded so nobody later mistakes one for the other.

### 6. H64 — not a sample problem; its instrument is now characterised

- H64's quote-level gate is **answered and null** with 245 events against a 150-event bar. More
  events change nothing there (see the audit note appended to `H64-RESULT.md`).
- Its **fill-level** gate was could-not-establish because depth was unobservable. A4 has now
  characterised `archive.pmxt.dev`: the exchange clock is `timestamp` at millisecond resolution,
  snapshots place to about a second, and its coverage (→ 2026-06-11) overlaps H64's window
  (2026-06-07 → 06-11).
- **This is an instrument becoming available, not a sample growing.** Listed so the distinction
  stays visible.

---

## Explicitly NOT revival candidates, with the reason

| entry | why a larger sample does not help |
|---|---|
| **H59** | Its own entry says so: *"An effect of H50's magnitude sits SIX interval-widths outside anything observed. A genuine null, not an inconclusive one."* |
| **H50** | Killed on economics, not power — the reversion is entirely sub-spread, 0.17¢ against a 2.00¢ cost to cross, **11.7×**. Its interval already excluded zero. |
| **H1, H2, H44** | Polymarket **wallets and tape**. B1 supplies neither. H2's bar (*wallets with 50+ resolved positions*) and H44's n=11 panel are unreachable from Kalshi market rows at any n. |
| **H61** | `revive_if` requires *sub-60-second detect-to-fill latency* — an execution capability, not a sample. The next-bar half is measurable; the latency half is not. |
| **H52, H42, H46, H15, H49** | Killed on adverse selection, spread economics or settlement-criteria divergence. None is an n problem. |
| **H55** | Its `revive_if` was **discharged** by H64: the shorter lead was tested, the band was populated, and there was nothing there. |

---

## H57 — straight to `PARKED.md`, as the packet directs

`H57.revive_if`, verbatim:

> *"At least 100 NEW KXRAIN events have settled that were not in the 2026-08-12 universe. A
> calendar problem, not a compute problem."*

**Two readings, both defensible:**

**Reading A — "new" means new to the study.** Any KXRAIN event outside the 2026-08-12 universe
counts, whenever it settled. Historical events were simply unreachable at the time and are
reachable now, so the condition is about *coverage*, and reaching further back satisfies it.

**Reading B — "new" means newly settled.** The condition is about the passage of time — "a calendar
problem" — so only events settling *after* 2026-08-12 count. Old events found by looking harder are
not new; they are old and were missed.

**The measurement that bears on it, and it is decisive either way:**
`/historical/markets?series_ticker=KXRAIN` returns **HTTP 200 and zero rows**, cursor exhausted
(A2 §A2.1). Control: an impossible series returns 200 with 0 rows, so the empty result is real.

**So under Reading A the condition is still not met** — the historical path supplies **no**
additional KXRAIN events at all, because KXRAIN is a young series whose history begins where its
live record begins. Under Reading B it is not met either, and cannot be until roughly 100 more
events settle. **The ruling matters for the principle, not for H57's status**, which stays
could-not-establish under both.

**This is Walton's ruling to make.** It is a judgement about what the author meant, and the same
wording pattern appears in other `revive_if` fields. Parked as **P4** and restated here.
