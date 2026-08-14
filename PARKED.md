# PARKED

Items that terminate in a **decision**, a **verdict**, a **revival** or a **resource
commitment**. Under the packet 3 autonomy contract these are not mine to make during an
unsupervised run. Each entry is a completed piece of work: the evidence is gathered and the
options are stated. Only the ruling is missing.

Ranked by how much each blocks.

---

## P1 — The fee model in `docs/INFRA.md` is wrong, and it is load-bearing

**Blocks:** the cost model of every extreme-price hypothesis, and any re-measurement of the
hurdle at size. This is the highest-value item in the lot.

**Evidence.** `docs/INFRA.md` records *"Fees: taker `ceil(M·0.07·p·(1−p))` … rounded up on order
total."* Kalshi's documentation says the **trade fee** rounds up to a **centicent per fill**, and
that whole-cent behaviour comes from a separate balance-precision **rounding fee** which a
per-order **accumulator** then rebates. All three documented worked examples reproduce exactly
under the documented model — see `registry/fees/A1-FEE-ROUNDING-2026-08-15.md`.

**Options.**
(a) Correct `docs/INFRA.md` to the documented model and tag it `[measured 2026-08-15]`.
(b) Leave it and add a warning note.
(c) Withhold until the base formula is also resolved (see P3).

**Recommendation:** (a). The rounding model is documented and reproduced; the unresolved base
formula is a separate, clearly-scoped gap and does not justify leaving a known-wrong rule in place.

---

## P2 — The extreme-price family may be size-dependent kills

**Blocks:** whether H7, H9, H33, H34, H53, H55 and H64 were killed by the market or by an
assumed order size of one contract.

**Evidence.** Effective fee per contract, multiplier 1.0: at p=0.97, **1.0000¢ at one contract
against 0.2100¢ at a hundred** — 4.76×. At p=0.99, 14.29×. At p=0.50, 1.14×. The quantisation
binds **only** at the extremes, which is exactly where this family lives. Fragmentation does not
undo it: the per-order accumulator holds 100 contracts at 0.2100¢ whether filled in 1, 5 or 20
pieces.

**This is a `revive_if` come due**, and the packet forbids me from acting on it. C1 will produce
the per-entry audit; the ruling on any entry it names as size-dependent is Walton's.

**Options.** (a) Re-run the named entries at realistic size under a corrected cost model.
(b) Re-run only where depth evidence exists to support the size. (c) Leave all verdicts.

**Recommendation:** (b), and it depends on B2. **The size that amortises the fee is the same size
that must be resting at the ask.** A revival justified by a fee model but unsupported by depth
would repeat H61's error — a real effect that could not be obtained.

---

## P3 — The base fee formula is not established

**Blocks:** any absolute cost figure. Not the qualitative shape, which holds for any small base fee.

**Evidence.** Kalshi's rounding page states a trade fee of **\$0.0085 for 1 contract at \$0.055**.
`0.07·p·(1−p)` gives **\$0.003638**. No reachable page states the model. Series expose
`fee_type` — `quadratic`, `quadratic_with_maker_fees` — **a field this project has never read** —
and `fee_multiplier`, but the mapping from `fee_type` to a formula was not found.

**Options.** (a) Ask Kalshi support. (b) Infer from live fills — requires trading, which is
forbidden. (c) Bound it: collect settled trades and back out the implied rate. (d) Leave `rate` a
parameter and state the assumption everywhere.

**Recommendation:** (d) now, (c) as a measurement in a later packet. (b) is not available.

---

## P4 — H57's `revive_if` wording is a judgement about intent

**Blocks:** whether H57 is revivable at all. Flagged by the packet itself as the live example.

**Evidence.** `H57.revive_if` reads: *"At least 100 NEW KXRAIN events have settled that were not
in the 2026-08-12 universe."*

**Reading A — not satisfied.** "New" means newly settled, after 2026-08-12. Historical events are
old; they were merely unreachable. Under this reading H57 waits for calendar time.

**Reading B — satisfied, or nearly.** The clause names events "not in the 2026-08-12 universe",
and that universe was bounded by what the live endpoint reached. Events recoverable from
`/historical` were genuinely not in it. Under this reading the condition is about sample novelty,
not event age.

The wording supports both. **Walton rules.** Note that KXRAIN is also a young series — 24 events
total, earliest `KXRAIN-26AUG01` — so under either reading the available count needs measuring
against `/historical` before the ruling means anything. A2 will produce that number.

---

## P5 — H64's fee explanation is wrong in its reasoning

**Blocks:** nothing operational. Recorded so it is not inherited as fact.

**Evidence.** `H64-RESULT.md` says all 254 rungs "were charged exactly 1 cent" because Kalshi
"rounds fees up to whole cents on the order total". Nothing was charged — H64 was a paper study
and the 1¢ was computed by my own code from the inherited INFRA.md formula. The number is right
for one contract and a non-direct member, by balance rounding rather than by the trade-fee ceiling.
The conclusion that the fee advantage "does not exist in practice" is **wrong at size**.

**H64's verdict and every figure are untouched**, and its headline result does not depend on this:
the fee correction shifts the mean well inside the interval's half-width and changes no robustness
check.

**Options.** (a) Amendment to `H64-RESULT.md` correcting the reasoning, verdict untouched.
(b) Leave it; A1 already records the correction.

**Recommendation:** (a), as an appended amendment under the amend-never-edit rule.
