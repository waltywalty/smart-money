# programmes/kalshi - CLOSED

**57 entries. 45 killed, 4 corrected, 3 confirmed, 3 could-not-establish, 6 lost to a
2026-08-10 rollback and recorded as lost rather than reconstructed. None tradeable.**

Start with **`KALSHI-PROGRAMME.md`** - the synthesis, written to outlive the venue. It carries the
hurdle on both axes, the fifteen mechanisms, the instrument-failure catalogue, the seven
right-for-the-wrong-reason entries, and what the data constraint actually was.

## What it found

**The cost of crossing is a function, and it is negative everywhere on both axes.**

| axis | span | entry |
|---|---|---|
| horizon, 24h to 10 minutes | 1.87c (-3.81c to -1.94c) | H60 |
| size, 1 to 500 contracts | 7.23c (-2.98c to -10.20c) | H65 |

Three effects are real - mean reversion in prices (H62), in executed trades (H63), and the
horizon-dependence of the hurdle itself (H60). None is money: expected reversion is 0.146c against
a 1.3c spread at best, roughly **9x short of covering a single crossing**.

**The finding that outranks both axes:** family composition moves the pooled hurdle **18.68c** at a
single size and horizon - **2.05x both measured axes combined**. Every pooled cost figure here,
H56's headline -4.39c included, is weighted by its mix at least as much as by the variable it names.
**A hurdle quoted without its family composition is not a hurdle.**

## Layout

| path | what |
|---|---|
| `KALSHI-PROGRAMME.md` | the synthesis - read this first |
| `registry/hypotheses.json` | the main artifact. 57 entries with verdicts, figures and `revive_if` |
| `registry/INDEX.md` | generated from it by `lib/build_index.py`. Never edit by hand |
| `registry/*-preregistration.md` | rules sealed and hashed *before* outcomes |
| `CLOSEOUT-2026-08-*.md` | four close-outs, MEASURED / INFERRED / ASSUMED |
| `analysis/` | the working studies |
| `data/` | scope, manifests, gate evidence. The 110,836-row dataset itself is in R2 |
| `scripts/` | the Kalshi collectors |

## Two ceilings on anyone reopening this

1. **Depth is bounded to 2026-05-14 -> 2026-06-11T03, permanently.** `archive.pmxt.dev` is the only
   public Kalshi order-book archive that has ever existed and it stopped. The exchange does not
   retain the book, so no future collection recovers the past. Any depth question is also bounded to
   the 41% of hours passing admission, and to quiet hours within those.
2. **`registry/retention/` is not here.** It stayed at the repo root because the unattended census
   workflow writes to it and that workflow's path cannot be edited with the current credential. See
   `PARKED.md` P18.

## The rule that governed every entry

No verdict, figure or `revive_if` in this programme may be changed. It is closed. Amendments are
appended and dated; nothing is edited in place.
