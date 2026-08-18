# Addendum A1 — Shard health IS a selection variable. Degraded shards are the busy hours.

**Date:** 2026-08-17. **Packet:** coworkpacket4, Addendum A, task A1.
**This settles the precondition. It must be quoted in any pre-registration that uses archive depth.**

**Verdict: outcome 2 of the three written down in advance** — *"Degraded shards are the busy ones
— depth is measurable only on quiet hours. That is a legitimate finding but it is a scope limit,
and no depth figure may then be stated as a property of the exchange."*

---

## The question

T3.2 established that bracketability runs 0% to 96.6% across shards and that shards must therefore
be chosen by **health**, not by date. Choosing data by a property is selection. So:

**Is archive collector health independent of exchange activity in that hour?**

**It is not.**

---

## Instrument

**Two different sources, deliberately.** Health comes from the archive parquet files. Activity
comes from **Kalshi**, via `GET /historical/trades?min_ts=&max_ts=` — never from the archive, so
the two measures cannot share a failure mode.

The trade endpoint returns newest-first within the window, capped at 1000. Activity rate is
therefore `1000 / (newest − oldest returned)` in trades per second. Every hour hit the 1000 cap,
so every rate is a real rate rather than a truncated count.

**Controls.** `min_ts`/`max_ts` set to a 1999 window returns **HTTP 200 with 0 trades** — the
filter is honoured, not ignored. Epoch conversions were computed in code, never by hand.

**A new API fact found while doing this, and it inverts what the market endpoints do:**

| endpoint | `ticker=` | `series_ticker=` | `min_ts`/`max_ts` |
|---|---|---|---|
| `/markets` | **IGNORED** | honoured | honoured |
| `/historical/markets` | **IGNORED** | honoured | **IGNORED** |
| `/historical/trades` | **honoured** (control 404s) | **IGNORED** (control returns the same head) | **honoured** (control empty) |

Filter honouring is per-endpoint and not guessable. **Control every parameter on every endpoint.**

---

## The measurement, 15 hours

| hour (UTC) | bracketable % | snapshot % | lag p50 s | exch span min | **trades/sec** | tickers | series |
|---|---|---|---|---|---|---|---|
| 2026-06-07T00 | 80.06 | 14.04 | 527.1 | 89.1 | 45.39 | 353 | 95 |
| 2026-06-07T12 | 96.61 | 3.20 | 1.1 | 60.0 | 31.57 | 237 | 76 |
| 2026-06-07T18 | 12.45 | 98.66 | 1486.2 | 29.8 | **53.68** | 391 | 88 |
| 2026-06-08T06 | 96.23 | 15.93 | 751.7 | 60.8 | 28.34 | 137 | 55 |
| 2026-06-08T12 | 79.71 | 27.83 | 2443.6 | 20.3 | 22.21 | 258 | 75 |
| 2026-06-08T18 | 4.13 | 99.92 | 639.6 | 48.7 | **41.45** | 285 | 94 |
| 2026-06-09T00 | 16.09 | 99.61 | 957.1 | 28.6 | **104.32** | 218 | 63 |
| 2026-06-09T12 | 99.69 | 3.72 | 0.4 | 60.0 | 43.41 | 214 | 73 |
| 2026-06-09T18 | 97.74 | 9.02 | 834.4 | 39.0 | 37.82 | 323 | 96 |
| 2026-06-10T00 | 6.39 | 99.86 | 681.4 | 44.3 | **64.00** | 332 | 77 |
| 2026-06-10T06 | 97.66 | 18.33 | 1.4 | 60.1 | 30.10 | 158 | 62 |
| 2026-06-10T12 | 95.89 | 32.53 | 1056.7 | 33.8 | 26.96 | 292 | 84 |
| 2026-06-10T13 | 53.69 | 37.08 | 2271.7 | 57.9 | 28.91 | 338 | 94 |
| 2026-06-11T00 | 48.55 | 92.08 | 594.7 | 0.8 | 30.52 | 203 | 70 |
| 2026-06-11T03 | 0.00 | 100.00 | n/a | n/a | **59.34** | 248 | 80 |

## The association

| health measure | activity measure | pearson | spearman | leave-one-out range |
|---|---|---|---|---|
| **bracketable %** | **trades/sec** | **-0.631** | -0.461 | **[-0.698, -0.594]** |
| bracketable % | distinct tickers | -0.342 | -0.329 | [-0.424, -0.230] |
| bracketable % | distinct series | -0.177 | -0.175 | [-0.305, -0.058] |
| **snapshot %** | **trades/sec** | **+0.593** | +0.407 | **[+0.554, +0.675]** |
| snapshot % | distinct tickers | +0.216 | +0.196 | [+0.078, +0.321] |
| lag p50 | trades/sec | -0.104 | - | [-0.242, +0.073] (n=14) |

**The leave-one-out range on the headline correlation does not span zero and never comes near it.**
That is the check this project applies to every correlation, and it is the reason this is reported
as a finding rather than as noise.

By tier, which is how a study would actually select:

| threshold | healthy | degraded | **degraded / healthy** |
|---|---|---|---|
| bracketable >= 80% | n=7, 34.80 trades/sec | n=8, 50.55 trades/sec | **1.45x** |
| bracketable >= 50% | n=9, 32.75 trades/sec | n=6, 58.88 trades/sec | **1.80x** |

**Distinct tickers and series barely move** (245 vs 284; 77 vs 80). It is not that degraded hours
cover more of the exchange — it is that the **same breadth of market trades harder**. The archive
fell over on *intensity*, not on *breadth*.

---

## The direction of the bias, stated plainly

**Selecting healthy shards selects quiet hours.** A depth study run on healthy shards measures a
book that is roughly **1.5 to 1.8 times less actively traded** than the hours it excludes.

Depth, spread and competition are precisely the quantities that differ most between quiet and busy
markets, and they differ in the direction that flatters a strategy: quiet hours have thinner
resting size but also less competition for it. **A depth figure from healthy shards would
understate how hard it is to get filled when it matters.**

This is the same shape as false positive #5 in `skills/empirical-claims/SKILL.md` — *the sample was
reachable because of a property correlated with the outcome* — and false positive #6, where
missing tail candles meant nobody was trading. **Here the mechanism is inverted and worse: the data
is missing precisely where trading was heaviest.**

## What this permits, and what it forbids

**Permits:** measuring depth on healthy shards and reporting it as **a property of quiet hours on
Kalshi in June 2026**, with this document cited and the 1.45x-1.80x activity gap quoted.

**Forbids:** any depth figure stated as a property of the exchange; any hurdle surface whose depth
axis comes from healthy shards without this scope limit attached; and any comparison between a
depth number from this archive and a fee number from the full universe, since they would describe
different populations.

## Limits of this result

- **n = 15 hours**, spanning 2026-06-07 to 2026-06-11 only. The correlation is stable under
  leave-one-out but the sample is five days of one archive.
- **The activity rate is measured from the last 1000 trades of each hour**, because the endpoint
  returns newest-first. It estimates the rate near the hour's end rather than the hour's mean. A
  within-hour activity profile would sharpen it; the tier separation is large enough that it is
  unlikely to reverse.
- **Association is not mechanism.** That busy hours degrade the collector is the obvious reading
  and matches the snapshot-storm signature, but nothing here rules out a third factor driving both.
- **This says nothing about whether depth itself is measurable** — T3.2 already answered that. It
  says what any depth measurement would be *about*.

## For Phase 4

Phase 4's precondition list included *"T3.2 says depth is answerable."* It does. **This addendum
adds a second condition that was not in the original list: any Phase 4 pre-registration must state
the scope limit above, in advance, and must not describe its hurdle surface as a property of the
exchange.** Per Addendum A, this result is quoted whichever way it landed, and it landed on the
restrictive side.
