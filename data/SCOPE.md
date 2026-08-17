# data/SCOPE.md - collection scope for Phase 1 (T1.1)

Written 2026-08-17, **before** collection. Packet 4 T1.1: *"which series families any
hypothesis has ever used, derived from `registry/hypotheses.json` and `analysis/` rather
than from judgement ... State the expected row count and byte size before collecting, so
the result can be checked against the prediction."*

This file states the prediction. It is committed before the first collection request, so the
prediction cannot be revised to fit the outcome.

## Method - derivation, not judgement

1. `registry/hypotheses.json` fetched from `api.github.com` and scanned for `KX[A-Z0-9]{2,}`.
   **18 distinct series.**
2. Every blob under `analysis/` enumerated from the git tree API (62 files, 286,784 bytes,
   `truncated: false`), each fetched raw from `raw.githubusercontent.com` and scanned with the
   same regex. 62/62 fetched, zero failures. **20 distinct tokens, 19 after exclusions.**
3. Scope = the union. **30 series.**

The regex stops at the first `-`, so the market ticker `KXHIGHCHI-26AUG09-B85.5` yields the
series `KXHIGHCHI`. No family was added or removed by opinion.

### Why `analysis/` had to be scanned separately

**12 of the 30 families appear only in `analysis/`, never in `registry/hypotheses.json`** -
including `KXHIGHNY`, the most-used weather series in the repository, which a registry-only
scan would have dropped. Packet 4 was right to name both sources.

| source | n | series |
|---|---|---|
| registry only | 11 | `KXAGENCYELIM`, `KXATPCHALLENGERMATCH`, `KXATPSETWINNER`, `KXBNB15M`, `KXCS2GAME`, `KXCS2MAP`, `KXEUEXITCOUNTRY`, `KXEUREF`, `KXGDP`, `KXNOBELPEACE`, `KXUSAEXPANDTERRITORY` |
| `analysis/` only | 12 | `KXATPMATCH`, `KXHIGHAUS`, `KXHIGHDEN`, `KXHIGHLAX`, `KXHIGHMIA`, `KXHIGHNY`, `KXHIGHPHIL`, `KXNBAGAME`, `KXNFLGAME`, `KXNHLGAME`, `KXUCLGAME`, `KXWTAMATCH` |
| both | 7 | `KXCPIYOY`, `KXEGGS`, `KXFED`, `KXHIGHCHI`, `KXMLBGAME`, `KXPAYROLLS`, `KXRAIN` |

## Exclusions

- **`KXMVE*` excluded a priori.** Not a judgement call - `docs/INFRA.md` records it as a
  standing rule: *"`?status=settled` unfiltered is flooded with `KXMVE*` machine-generated
  combinatorial markets - 2,000 of the first 2,000 rows. Exclude `KXMVE*` a priori."* One
  `KXMVE` token appears in `analysis/h56/H56-RESULT.md`; it is a mention of that flood, not a
  study of it.
- **Nothing else is excluded.** Crypto (`KXBNB15M`) stays in scope because the registry
  references it, not because it is interesting. The registry says so; that is the rule.

## Existence and filter controls (2026-08-17)

All 30 return **HTTP 200** from `GET /series/{ticker}`. The impossible control key
`KX-IMPOSSIBLE-CONTROL-19990101` went out on all three paths in the same pass:

| control | result |
|---|---|
| `GET /series/KX-IMPOSSIBLE-CONTROL-19990101` | **404** |
| `GET /events?series_ticker=KX-IMPOSSIBLE-CONTROL-19990101` | 200, **0 events** |
| `GET /historical/markets?series_ticker=KX-IMPOSSIBLE-CONTROL-19990101` | 200, **0 markets** |

So `series_ticker=` is honoured on both list endpoints, and a zero-row answer for a real series
means zero rows - not a silently ignored filter. (Contrast `ticker=`, which `docs/INFRA.md`
records as silently ignored on both paths.)

## Four in-scope series have no historical rows at all

Each returns HTTP 200 with **0 markets** from `/historical/markets`. Cross-checked against a
different endpoint - `/events` and live `/markets` - which is where the explanation is:

| series | historical rows | live events | live markets | why |
|---|---|---|---|---|
| `KXRAIN` | 0 | 29 | 100 | *"Where will it rain daily"*, daily. **Earliest event 2026-07-16 - the entire series postdates the historical cutoff of 2026-06-17.** |
| `KXAGENCYELIM` | 0 | 1 | 4 | one event, `KXAGENCYELIM-29` - resolves 2029 |
| `KXEUREF` | 0 | 1 | 4 | one event, `KXEUREF-30` - resolves 2030 |
| `KXEUEXITCOUNTRY` | 0 | 1 | 6 | one event, `KXEUEXITCOUNTRY-30` - resolves 2030 |

`KXRAIN` is the **most-referenced series in `registry/hypotheses.json` (3 entries)** and it has
zero settled history. Anything needing settled `KXRAIN` outcomes needs forward collection, not a
historical pull. Recorded here; **no registry verdict, figure or `revive_if` is changed by this
run** - parked.

## Two instrument facts found while scoping, before collecting

**1. On `/historical/markets`, `status` is `finalized`, never `settled`.**
Measured across 2,000 rows of `KXHIGHNY` and `KXMLBGAME`: `status` is `finalized` on **100%** of
rows and `settled` on **0%**, while `result` is populated on **100%**. Cross-checked on a
different path - `GET /markets/{ticker}` and `GET /historical/markets/{ticker}` both return
`status=finalized, result=no` for `KXHIGHNY-26JUN16-T82`. The `docs/INFRA.md` rule *"outcomes
must come from `?status=settled`"* is about the **live** `/markets` list. A collector that
carried it over to `/historical/markets` would filter away 100% of rows and report an empty
dataset as an honest zero.

**2. `result` is not binary.** `KXMLBGAME` page 1: `no` 495, `yes` 495, **`scalar` 10**. An
estimator mapping `result` onto `{yes, no}` mis-handles the third value silently.

## The prediction

Two bases, marked per row:

- **exact** - page 1 at `limit=1000` returned no cursor, so the page is the whole series.
- **events x mpe** - `events_pre_cutoff x markets_per_event`, where `events_pre_cutoff` counts
  events dated on or before the cutoff `2026-06-17`, obtained by paginating
  `/events?series_ticker=`, and `markets_per_event` is measured on page 1 of
  `/historical/markets` with the first and last event on the page dropped, since the page
  boundary truncates them.

Bytes per row is each series' own measured `size_download / rows` on page 1.

### Predictor validated where truth is known

Two series have both a complete event count and an exact row count:

| series | predicted | actual | error |
|---|---|---|---|
| `KXUCLGAME` | 193 x 3.0 = 579 | 579 | **0.0%** |
| `KXNFLGAME` | 332 x 2.0 = 664 | 666 | **0.3%** |

Two series, both sports, both small. A calibration check, not a guarantee.

### Headline prediction

| quantity | value |
|---|---|
| **Rows** | **111,658** |
| **Bytes, uncompressed JSON** | **259,225,944 (259.2 MB)** |
| Series with >0 rows | 26 of 30 |
| Largest single series file | `KXATPCHALLENGERMATCH`, 11,234 rows, 28.7 MB |
| Prior full-exchange pull, for contrast | 7.27 GB |
| Reduction | **~28x** |

The largest single file is well inside the streaming SigV4 path already exercised at 128 MB, and
inside the 352 MB of free VM disk - but only one series at a time. Upload, delete, move on.

### Per series

| series | source | predicted rows | bytes/row | predicted MB | basis |
|---|---|---:|---:|---:|---|
| `KXATPCHALLENGERMATCH` | registry | 11,234 | 2551 | 28.66 | events x mpe |
| `KXHIGHNY` | analysis | 10,632 | 2399 | 25.51 | events x mpe |
| `KXHIGHCHI` | both | 10,560 | 2394 | 25.29 | events x mpe |
| `KXCS2MAP` | registry | 8,804 | 1961 | 17.27 | events x mpe |
| `KXATPMATCH` | analysis | 6,866 | 2509 | 17.23 | events x mpe |
| `KXHIGHMIA` | analysis | 6,792 | 2408 | 16.36 | events x mpe |
| `KXHIGHAUS` | analysis | 6,774 | 2397 | 16.24 | events x mpe |
| `KXMLBGAME` | both | 6,634 | 2301 | 15.27 | events x mpe |
| `KXWTAMATCH` | analysis | 6,622 | 2511 | 16.63 | events x mpe |
| `KXATPSETWINNER` | registry | 6,548 | 2775 | 18.18 | events x mpe |
| `KXBNB15M` | registry | 6,211 | 2158 | 13.40 | events x mpe |
| `KXCS2GAME` | registry | 5,166 | 1944 | 10.05 | events x mpe |
| `KXHIGHDEN` | analysis | 3,450 | 2364 | 8.16 | events x mpe |
| `KXHIGHPHIL` | analysis | 3,450 | 2396 | 8.27 | events x mpe |
| `KXHIGHLAX` | analysis | 3,174 | 2374 | 7.54 | events x mpe |
| `KXNHLGAME` | analysis | 3,076 | 1630 | 5.01 | events x mpe |
| `KXNBAGAME` | analysis | 2,896 | 1643 | 4.76 | events x mpe |
| `KXNFLGAME` | analysis | 666 | 2167 | 1.44 | exact |
| `KXCPIYOY` | both | 582 | 1824 | 1.06 | exact |
| `KXUCLGAME` | analysis | 579 | 2120 | 1.23 | exact |
| `KXFED` | both | 391 | 1776 | 0.69 | exact |
| `KXPAYROLLS` | both | 336 | 1751 | 0.59 | exact |
| `KXGDP` | registry | 174 | 1905 | 0.33 | exact |
| `KXNOBELPEACE` | registry | 24 | 1497 | 0.04 | exact |
| `KXEGGS` | both | 16 | 1541 | 0.02 | exact |
| `KXUSAEXPANDTERRITORY` | registry | 1 | 2120 | 0.00 | exact |
| `KXAGENCYELIM` | registry | 0 | - | 0.00 | exact |
| `KXEUEXITCOUNTRY` | registry | 0 | - | 0.00 | exact |
| `KXEUREF` | registry | 0 | - | 0.00 | exact |
| `KXRAIN` | both | 0 | - | 0.00 | exact |

## How this prediction can be wrong

Stated now, so a miss is diagnosable rather than explained away later.

1. **`markets_per_event` is measured on the newest page only.** Weather reads a flat 6.0
   strikes/event on June 2026 events; if 2021-2024 events carried a different strike count, the
   weather predictions move proportionally. Weather is 32% of the predicted total, so this is the
   largest single risk.
2. **`KXBNB15M` event count is a lower bound.** Pagination was capped at 60 pages (12,000
   events) and stopped while still returning a cursor. Pre-cutoff events counted: 6,211. An
   independent cadence estimate - 96 events/day x 66 days from 2026-04-12 to the cutoff - gives
   ~6,336, so the cap likely cost under 2%. **Logged rather than hidden.**
3. **Event date is a proxy for settlement.** Events are dated from `strike_date`, falling back
   to the date in the ticker. An event dated just before the cutoff may not have finalized before
   it. Expected direction: prediction slightly high.
4. **48 events across the macro series carry no parseable date** (monthly tickers such as
   `KXCPIYOY-26MAY`). Every one of those series is exact-basis, so no prediction depends on them.
5. **Bytes are uncompressed JSON as the API returns it.** Stored NDJSON differs by the array
   framing; gzip should land near 10-15%% of these figures.

## What counts as a hit

- Total rows within **+/-10%** of 111,658: prediction confirmed.
- Any single series off by **more than 2x**: the predictor is wrong for that family, and the
  reason gets reported rather than smoothed.
- Zero rows for any of the 26 non-empty series: instrument failure, not a finding.

## Status

Prediction sealed. T1.2 collects. Discipline for the run: raw HTTP through the Kernel VM,
explicit User-Agent, a status code recorded for every response rather than a boolean, and one
series file uploaded to R2 and deleted locally before the next begins.
