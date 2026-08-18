# T3.2 — Is the depth question answerable? Yes, per shard, on quiet hours only.

**Date:** 2026-08-17. **Packet:** coworkpacket4, Phase 3, task T3.2. **Phase 4 depends on this.**

**Read with `A1-SHARD-SELECTION-2026-08-17.md`**, which carries the 15-hour measurement table and
adds the scope limit. This document answers *can it be done*; A1 answers *what it would be about*.

---

## The two questions

### 1. Did A4 bound the archive's receipt lag? **Yes, and the method generalises.**

A4 established that `timestamp_received` is a write-batch stamp and must never be used as an event
clock; that `orderbook_delta` rows carry the exchange clock at **0% null**; and that a snapshot can
be placed by joining it to the delta rows sharing its `timestamp_received` and taking their
min/max `timestamp` as a bracket. Re-tested on **fourteen shards A4 never touched**, the technique
works on every shard that contains delta rows.

### 2. Is H64's depth question answerable? **Yes — per shard, with coverage reported, on quiet hours.**

A4's headline was **95.9% of snapshot rows bracketable to ~1 s**, measured on **one** shard. Across
15 hours the true range is **0.00% to 99.69%**:

| bracketable | hours | example |
|---|---|---|
| 95-100% | 6 | 2026-06-09T12 at 99.69% |
| 50-95% | 4 | 2026-06-10T13 at 53.69% |
| 5-50% | 4 | 2026-06-09T00 at 16.09% |
| 0% | 1 | 2026-06-11T03 — zero delta rows, no clock at all |

**Carrying 95.9% forward as the archive's coverage would be wrong by a factor of twenty at the
bottom of that range.**

---

## Two corrections to A4, both recorded as amendments rather than edits

**1. Degradation is intermittent, not terminal.** A4 framed it as belonging to the final days. It
does not. `2026-06-07T18` is at **12.45%** bracketable and `2026-06-08T18` at **4.13%**, both
sitting between healthy neighbours. Two of the four worst hours in the sample are on 06-07 and
06-08 — the *earliest* days tested. **Shards cannot be selected by date.**

**2. There is a severity tier between DEGRADED and DEAD.** `2026-06-11T00` holds 4.24M rows of
which **92.08% are snapshots**, with **0.8 minutes** of exchange time in a 60-minute file. It has a
clock; half its snapshots still cannot be placed.

---

## Coverage of H64's window, and the archive today

H64's universe is `close_time` in **2026-06-07 → 2026-06-11**; the archive's Kalshi coverage ends
at **2026-06-11T03**. They overlap, so depth is reachable for the whole study window — subject to
per-shard health and to A1's scope limit.

Shard existence by **ranged GET**, reading the status at the resource layer: all probed hours from
`2026-06-07T00` to `2026-06-11T03` present; `2026-06-11T04` onward **404**. The archive **has not
resumed** — `kalshi_orderbook_2026-08-16T12.parquet` → **404**, control `1999-01-01T00` → 404.

---

## The answer Phase 4 needs

| precondition | status |
|---|---|
| Did A4 bound the receipt lag? | **Yes.** Batch-bracketing is sound and generalises. |
| Is depth answerable at all? | **Yes**, per shard, with coverage reported. |
| Over H64's window? | **Partly.** Six hours above 95%, one at 0%, four below 50%. |
| Is the archive still alive? | **No.** Dead since 2026-06-11T03. |
| Is shard selection safe? | **No — see A1.** Healthy shards are the quiet hours, 1.45-1.80x less traded. |

**A Phase 4 pre-registration must state in advance:** the per-shard health classification and its
thresholds; the bracketable-coverage floor below which a shard is excluded; **and A1's scope limit,
quoted, with the finding that excluding degraded shards excludes the busiest hours.**
