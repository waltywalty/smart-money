# GATE 1 — after Phase A

**Date:** 2026-08-14. **Packet:** coworkpacket3autonomous.

A gate that passes itself is worthless. Each answer below states what was measured, and the
final section states what the gate refuses to license.

---

## The five questions, one line each

**1. Is the fee ceiling per order, per fill, or per contract?**
**Per fill — measured.** The trade fee rounds **up to $0.0001 (a centicent) per fill**; the
whole-cent behaviour this project inherited comes from a *separate* balance-precision rounding fee
that a per-order accumulator rebates in whole cents, and all three of Kalshi's documented worked
examples reproduce exactly — but the **base fee rate could not be established** (the docs' own
example gives \$0.0085 for one contract at \$0.055 against \$0.003638 from `0.07·p·(1−p)`), so the
*location* of the ceiling is measured and its *magnitude* is not.
→ `registry/fees/A1-FEE-ROUNDING-2026-08-15.md`, `analysis/fees/fee_model.py`

**2. How far back does `/historical` reach, per series?**
**To each series' launch — measured, cursor-exhausted in every case**: KXFED 2021-07-26,
KXHIGHNY 2021-08-07, KXHIGHCHI 2021-08-20, KXCPIYOY 2022-12-13, KXPAYROLLS 2023-04-07,
KXMLBGAME 2025-04-16, and **KXRAIN zero rows** — the limit is data, not pagination and not the
API.
→ `registry/historical/REACH-2026-08-14.md` §A2.1

**3. Do `/historical` and live agree on a common window?**
**No — measured disagreement, and the mechanism is measured too**: over 2026-06-07→2026-06-10
`/historical` returns 56 events against live's 36, with **20 events only on historical and zero
only on live**, because live `/markets` has a `close_time` floor sliding at one day per day
(2026-06-08 on 2026-08-14); inside the overlap band the two paths agree on **45 of 45 fields**
except `open_interest_fp`, which `/historical` returns as `0.00` for **41 of 41** markets.
→ `registry/historical/REACH-2026-08-14.md` §A2.2, §A2.3; parked as **P8**

**4. Does `/events` reconcile with `/markets`?**
**No, and it never should — measured**: `/events` is a strict superset of `/markets`' event set in
all eighteen series tested (`markets − events = 0` everywhere), with gaps up to **16,550 events**
(KXBTC15M: 22,999 against 6,449) and ratios up to **428×** (KXNCAABBGAME: 7,272 against 17,
out of season) — they reconcile only as `markets ⊆ events`, and an event listing is not evidence
its market rows are reachable.
→ `docs/INFRA.md`, A3 measurement block

**5. Can the archive's receipt lag be bounded?**
**Yes, conditionally — measured**: `timestamp_received` is a write-batch stamp (98.4% of
consecutive rows in one market share it) and must never be used as an event clock, but delta rows
carry the exchange clock at 0% null, and joining a snapshot to the delta rows in its own batch
brackets **95.9% of snapshot rows to 1.2 s mean / 6.0 s p99** — in every shard that contains delta
rows, which the final shard `2026-06-11T03` does not.
→ `registry/historical/ARCHIVE-LAG-2026-08-14.md`

---

## What the gate licenses

| Phase B task | Gate condition | Status |
|---|---|---|
| **B1** bulk historical settled-market collection | "Within the reach A2 established" — A2 established reach | **Proceed** |
| **B2** depth study | "Only if A4 bounded the receipt lag" — A4 bounded it, with two carried conditions | **Proceed, conditioned** |
| **B3** fee-model backtest harness | A1 established the rounding regime | **Proceed, with `rate` a parameter** |

**Conditions that must travel with B1:**

1. Page `/historical/markets` by `series_ticker` or `event_ticker` **only**. `ticker=` is silently
   ignored on both paths and returns the unfiltered `KXMVE*` head — caught 2026-08-14 by a control
   key, after it had already fabricated six identical close times.
2. Filter every window **client-side**. `/historical/markets` accepts `min_close_ts`/`max_close_ts`
   with HTTP 200 and ignores them.
3. Record `stop_reason` on every pagination. A 429 read as cursor exhaustion under-reported one
   series by 65% on 2026-08-14 (1,400 against 4,083).
4. Join `fee_type` and `fee_multiplier` from `/series/{ticker}` — they are absent from market rows
   on **both** paths, and KXMLBGAME carries `fee_multiplier: 0.5`.
5. Collect the union of both paths. Neither is complete; the overlap band is the only region where
   a cross-check is possible, and per **P9** it may close on or about 2026-08-20.

**Conditions that must travel with B2:**

1. Use `timestamp`, never `timestamp_received`. Select shards by content, never by filename — the
   degraded shards' filenames are wrong by up to 34 minutes.
2. Carry the bracket width into the analysis for snapshot-derived rows, and treat the 4.1%
   unbracketable rows as a **selection** question, not a rounding one — they are concentrated in
   snapshot-only batches.

---

## What the gate refuses to license

- **Any fee figure stated in dollars.** The ceiling's location is measured; its rate is not. Every
  fee number this project produces must carry `rate` as a visible parameter until A1's gap closes.
- **Any use of `open_interest_fp` from `/historical`.** 41 of 41 read `0.00`, and which path is
  correct is not established (**P8**).
- **Any universe count taken from the live path alone**, including packet 2's 4,787 events
  (**P7**).
- **Any statement about authenticated reach.** Every Phase A measurement was unauthenticated;
  authenticated reach is recorded as **untested, not equal**.
- **Any row from archive shard `2026-06-11T03`.** Zero delta rows, therefore no exchange clock and
  no bracketing anchor.
- **Phase D.** Its four conditions are not evaluated here and, per the packet's own expectation,
  are unlikely to hold in this run.

---

## The honest summary

Four of the five questions are answered with measurements; the fifth (fees) is answered in its
structural half and explicitly **could not establish** in its numerical half. Phase B is licensed
because A2 established reach — not because Phase A went well. It went well in one specific sense
worth recording: **three of Phase A's findings were errors caught by controls and cross-checks
rather than by inspection** — a 429 read as exhaustion, a parity claim framed against an
expectation instead of the other endpoint, and an ignored `ticker=` filter that had already
produced a confident fabricated result. None announced itself.
