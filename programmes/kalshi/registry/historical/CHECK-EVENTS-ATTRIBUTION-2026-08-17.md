# Check — packet 2's `/events` attribution is falsified by the project's own A3 table

**Date:** 2026-08-17. Prompted by Gate 4's deltas of 0, 0 and +4 of 3,321 at low request rate.
**Verdict: the stated attribution is FALSIFIED. The replacement mechanism is strongly supported
but not proven, and the 2,020 figure cannot be re-derived.**

---

## The claim under test

`CLOSEOUT-2026-08-14.md`, T2:

> Counts recorded: **13,832 markets, 13,832 unique tickers, 4,787 events, 245 series** … The second
> derivation via `/events` disagreed — **2,020 against 4,787** — and the disagreement is recorded
> rather than reconciled: it is `/events` pagination on high-frequency series.

So `/events` returned **42%** of the live path's event count, and the shortfall was attributed to
`/events` pagination behaving badly on high-frequency series.

---

## 1. The attribution predicts the wrong direction, and the same session measured it

`docs/INFRA.md`, section A3, measured **2026-08-14 — the same day**. Ten series, **both endpoints
paged to cursor exhaustion**, distinct `event_ticker` counted in code, and — stated in the file —
*"all twenty pagings terminated on an empty cursor, none on a page cap and none on a non-200."*

| series | `/events` | `/markets` | ratio |
|---|---:|---:|---:|
| KXBTC15M | 22,999 | 6,449 | 3.6× |
| KXETH15M | 22,986 | 6,449 | 3.6× |
| KXSOL15M | 20,622 | 6,449 | 3.2× |
| KXXRP15M | 17,403 | 6,449 | 2.7× |
| KXBNB15M | 14,020 | 6,450 | 2.2× |
| KXHYPE15M | 14,019 | 6,449 | 2.2× |
| KXDOGE15M | 14,019 | 6,451 | 2.2× |
| KXNCAABBGAME | 7,272 | 17 | 428× |
| KXITFMATCH | 14,649 | 7,750 | 1.9× |
| KXITFWMATCH | 13,362 | 6,730 | 2.0× |

**`/events` returns MORE than the market path on every one of ten series — and the largest multiples
are precisely the high-frequency series**, the seven 15-minute crypto books at 2.2×–3.6×.

The T2 attribution requires `/events` to *under*-return on high-frequency series. A3 measured it
*over*-returning on exactly those series, cleanly, with stop reasons recorded. **The stated
mechanism is contradicted by the project's own instrument, from the same day.**

---

## 2. The mechanism that does produce a shortfall was found the same day, on the same endpoint

`docs/INFRA.md`:

> `/events?series_ticker=KXMLBGAME` was read as **1,400** events on 2026-08-14 by a loop that broke
> on `st != 200`; a 429 arrived on page 7 and was silently recorded as exhaustion. Paged again with
> the 429 retried, the same query returns **4,083**.

That is a **2.9× undercount**, on `/events`, from a 429 read as end-of-data. T2's gap is
**4,787 / 2,020 = 2.37×** — same endpoint, same day, same direction, comparable magnitude.

Ordering, as far as the record goes: the close-out calls it *"the **second** derivation via
`/events`"* — it ran after the 13,832-market collection. Given a shared limiter with memory, a
second arm inherits whatever the first drew down.

---

## 3. What could NOT be established, said plainly

- **No request log, no script and no series list survives for the T2 `/events` derivation.** The
  word "second" is prose, not a timestamped record. The ordering is *stated*, not *proven*.
- **The bulk arm may not have depleted anything.** B1 later ran **19,483 requests with zero 429s**
  at ~4.06 req/s — inside the clean band measured today. If T2's collection ran at a similar rate,
  it would not have drawn the bucket down at all, and the 429 would have to have come from
  somewhere else.
- **The 2,020 cannot be re-derived.** It spans 245 series in a window whose series list was never
  committed; `/historical/markets` ignores `min_ts`/`max_ts`, so reconstructing the universe means
  re-pulling the full 7.27 GB.

### The counterbalanced reproduction attempt, and why it is inconclusive

Two paging modes — `legacy` (break on non-200, the 2026-08-14 bug) and `retry` — run in **both
orders**, on a fresh bucket and after bursts, per the new counterbalance rule:

| round | bucket state | order | legacy | retry |
|---|---|---|---|---|
| 1 | fresh | legacy→retry | 4,124 `cursor_exhausted` | 4,124 `cursor_exhausted` |
| 2 | fresh | retry→legacy | 4,124 `cursor_exhausted` | 4,124 `cursor_exhausted` |
| 3 | after 320-req burst | legacy→retry | 4,124 `cursor_exhausted` | 4,124 `cursor_exhausted` |
| 4 | after 1,280 req | retry→legacy | 4,124 `cursor_exhausted` | 4,124 `cursor_exhausted` |
| 5 | after 3,200 req @ 64 threads | legacy→retry | 4,124 `cursor_exhausted` | 4,124 `cursor_exhausted` |

**Zero 429s in any of it.** The bug cannot fire without a 429, and no 429 could be induced from
this VM — 3,200 requests at 64 threads, where this morning's VM began rejecting after ~600.
**The mechanism was therefore not reproduced today.** Reporting it as reproduced would be the same
error this check exists to correct.

---

## Verdict

| claim | status |
|---|---|
| "the disagreement is `/events` pagination on high-frequency series" | **FALSIFIED** — A3 measured `/events` over-returning on those series by 1.9×–428× |
| "a 429 read as exhaustion truncated the `/events` pass" | **strongly supported, not proven** — same endpoint, same day, 2.9× vs the observed 2.37× |
| "the arms were sequential and `/events` ran second with a depleted bucket" | **sequential: stated in the close-out. Depleted: not established** |
| the 2,020 figure itself | **unreliable — treat as a failed measurement, not as evidence about `/events`** |

**No registry verdict, figure or `revive_if` is changed by this check.** `4,787` is unaffected; it
came from the live path and is separately parked as **P7** for a different reason (it is a live-path
undercount at the window edge). What changes is only the *explanation* attached to `2,020`, and the
correct entry is: **a paging loop that could not tell a rate limit from the end of the data.**
