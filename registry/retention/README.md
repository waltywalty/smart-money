# Retention census — the prediction, written before the observations

Task packet 2, T4 Part B. Ten daily censuses of a fixed 25-series panel, same query every time.
**Do not draw a conclusion before `census-2026-08-23.json` exists.**

This directory exists because the 2026-08-13 coverage note asserted a rolling window from
evidence that could not establish it — growth at the front edge, and one day's floor reading.
The fix is not more argument. It is naming what should disappear, in advance, and then looking.

## The prediction

**If retention is a rolling window**, the earliest reachable `close_time` advances by about one
day per day, and these specific event tickers stop returning markets:

| event ticker | earliest close inside it | predicted absent by |
|---|---|---|
| `KXHIGHNY-26JUN07` | 2026-06-08 | **2026-08-15** |
| `KXHIGHCHI-26JUN07` | 2026-06-08 | **2026-08-15** |
| `KXHIGHNY-26JUN08` | 2026-06-09 | 2026-08-16 |
| `KXHIGHCHI-26JUN08` | 2026-06-09 | 2026-08-16 |
| `KXHIGHNY-26JUN09` | 2026-06-10 | 2026-08-17 |
| `KXHIGHNY-26JUN10` | 2026-06-11 | 2026-08-18 |

"Absent" means `GET /markets?event_ticker={T}&limit=100` returns **zero markets**, which is what
already happens for `KXHIGHNY-26JUN03` today under every status filter.

**If retention is static** — a one-time purge around 2026-06-08 that is not advancing — the floor
stays at 2026-06-08 for all ten days and **none of these six tickers disappears.**

Both branches are falsifiable by the same query. The 08-15 pair is the one that settles it fastest;
if those two are still returning markets on 2026-08-16, the rolling-window reading is wrong and the
H55/H64 deadline does not exist.

## What is already measured, and what these ten days add

Already measured (see `FINDINGS-2026-08-14.md`): the floor is uniform at **2026-06-08** across
sixteen series carrying between 25 and 6,348 events, which excludes count-based retention; and it
moved from 2026-06-07 to 2026-06-08 between 08-13 and 08-14 on two independently checked series.

Two timepoints establish a direction. They do not establish a rate, they do not exclude a one-off
adjustment that happened to land between the two readings, and they cannot show whether 67 is
stable or drifting. That is what the ten files are for.

## Method — read this before adding a census

**Follow the cursor to exhaustion.** A single page of 1,000 rows gives a false floor on
high-volume series, and it is the exact artifact T6 warned about:

```
KXMLBGAME   one page: floor 2026-07-05 (500 events)   fully paged: floor 2026-06-08 (852 events)
KXBTC15M    one page: floor 2026-08-03 (1000 events)  fully paged: floor 2026-06-08 (6348 events)
```

- Query: `GET /trade-api/v2/markets?series_ticker={S}&status=settled&limit=1000`, cursor followed
  to exhaustion. Exclude `KXMVE*`.
- Raw HTTP from the Kernel VM. Explicit `User-Agent` — a bare `python-urllib` UA is blocked at
  some edges. Record **status codes, not booleans**: a 403 read as "absent" is how the last sweep
  went confidently wrong.
- Record `{series_ticker, earliest_reachable_close_time, event_count, event_ticker_list}` plus,
  for each named ticker above, the market count returned by `?event_ticker=`.
- Same panel, same query, every time. A panel that drifts measures nothing.

## Two things not to confuse

**Event metadata is not market data.** `/events?series_ticker=…&status=settled` reaches back years
— `HIGHNY-21AUG06`, `FED-21DEC`, `CPIYOY-22DEC` are all still listed — while `/markets` reaches 67
days. An event can be listed and have zero retrievable markets. Do not read event depth as evidence
the data survives.

**A young series is not a retained series.** `KXRAIN` floors at 2026-07-16 because it has 24 events
in total with the cursor exhausted, earliest `KXRAIN-26AUG01`. `KXWTI15M` and `KXGOLD15M` are the
same story at 2026-07-31. Their floors will *not* advance, and that is not evidence against a
rolling window. The seasonal series (`KXNBAGAME`, `KXNHLGAME`, `KXTONYAWARDS`) have the mirror
problem: their newest event is old, so their floor is pinned by inactivity. **Only the sixteen
series flooring at 2026-06-08 carry the test.**
