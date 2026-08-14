# RUN-LOG — autonomous run, task packet 3

Append-only. One block per session. Newest at the bottom.

---

## Session 1 — 2026-08-15 06:05 UTC

**Constitution re-read:** yes — `CLAUDE.md` §4 and `skills/empirical-claims/SKILL.md`
Part 1 (all eleven rules, including 10 and 11 added on 2026-08-14).

**Resumed at:** run start. No prior RUN-LOG existed.

**Completed this session:** *(updated as work lands)*
- Direct commit path established and **proven by a real write**, not by the
  `permissions.push` field. `scripts/gh_commit.py check` reports
  `200 waltywalty/smart-money push=True`, and `scripts/gh_commit.py` was itself
  committed as `f4557da`. That field reflects the USER's repo access rather than the
  token's and misled this project on 2026-08-12, when a PAT reporting `push=True`
  returned 403 on the first blob POST. The only proof of write access is a write.
  **The patch-and-apply cycle is retired.**
- Token held as `GH_TOKEN` in the VM environment, mode 600, outside the repo, never
  printed and never committed. Deviation flagged to Walton: it is sourced from a
  mode-600 file in the VM rather than held only in memory, because `exec_command`
  starts a fresh login shell per call and passing it inline would place it in the
  conversation on every commit — more exposure, not less.

**Parked this session:** none yet.

**STOP conditions hit:** none.

**Next action:** A1 — establish Kalshi's fee rounding rule from documentation
(per order / per fill / per contract), find and reproduce a worked example, then build
`analysis/fees/fee-model.py`.

**Completed this session (A1):**
- **A1 done.** Fee rounding established from Kalshi documentation, not inference. Trade fee
  rounds up to a **centicent per fill**, not a whole cent; whole-cent behaviour comes from a
  separate balance-precision rounding fee that a **per-order accumulator** rebates. All three
  documented worked examples reproduce exactly.
- **Fragmentation does not destroy amortisation** — 100 contracts at p=0.97 cost 0.2100¢ each
  whether filled in 1, 5 or 20 pieces. **Size does matter, and only at the extremes**: 1 contract
  is 1.0000¢ at any price above 0.9, against 0.2100¢ at 100 contracts (p=0.97) and 0.0700¢
  (p=0.99). At p=0.50 the ratio is 1.14×.
- Delivered `analysis/fees/fee_model.py` (rounding regime a parameter, documented examples as
  unit tests) and `registry/fees/A1-FEE-ROUNDING-2026-08-15.md`.
- Base fee formula **could not be established** — the docs example gives \$0.0085 for 1 contract
  at \$0.055 against \$0.003638 from `0.07·p·(1−p)`. `rate` left a parameter everywhere.

**Parked this session:** P1–P5 → `PARKED.md`.

**STOP conditions hit:**
- **STOP 1** — A1 contradicts `docs/INFRA.md` ("rounded up on order total"). Both versions
  recorded, neither built on, INFRA.md unchanged.
- **STOP 2** — A1 overturns H64's stated fee conclusion. H64's verdict and figures untouched;
  its result does not depend on the fee.

**Next action:** A2 — depth-probe `/historical` per series for the earliest reachable settled
market, re-derive the 2026-06-07→06-11 window from `/historical` and compare against the live
path's 4,787 events, check field parity (`fee_multiplier` especially), and candlestick reach.
Deliver `registry/historical/REACH-2026-08-15.md`.

---

## Session 2 — 2026-08-14

**Constitution re-read — done before any work, per the packet's anti-drift rule.**
`CLAUDE.md` §4 (5,916 bytes) and `skills/empirical-claims/SKILL.md` (10,279 bytes) fetched raw
from the repository via the GitHub contents API in the Kernel VM, both HTTP 200, and read in
full. The Cowork sandbox had rolled back again and held no working copy; the VM is the only
surviving surface, and it is ephemeral — `/root/work` was empty at session start.

**Date correction.** Three independent clocks — the Cowork host, the Kernel VM, and the `Date:`
header from `api.elections.kalshi.com` — read **2026-08-14**, not 2026-08-15. Session 1's
deliverable filename is a day ahead of its own measurement. Not renamed; parked as **P6**.

**A2 done** → `registry/historical/REACH-2026-08-14.md` (`2ff36f4`), amended (`0bc5c37`).

- `/historical/markets` reaches 2021-07-26 (KXFED) and 2021-08-07 (KXHIGHNY). **The limit is
  data, not pagination and not the API** — the cursor exhausted in all six series probed.
- Legacy ticker prefixes (`HIGHNY-`, `FED-`, `PROLLS-`, `CPIYOY-`) resolve under the modern
  `KX*` series parameter. A collector keyed on ticker prefix drops most of the depth.
- **KXRAIN returns HTTP 200 and zero historical rows** — decision-relevant for H57 / P4.
- **The live/historical disagreement is real and its mechanism is measured.** Live `/markets`
  has a hard `close_time` floor at 2026-06-08; `/historical` is a strict superset below it
  (only-hist 20, only-live 0). The obvious explanation — a `status=settled` vocabulary
  artifact — was **refuted**: removing the status filter entirely returns identical counts,
  and every row reads `status="finalized"`.
- Cross-checked on two different endpoints, not a second call to the same one:
  `/events/{e}` returns 200 with `"markets": []` below the floor (control 404s), and
  `/historical/markets?event_ticker=` returns the six markets the live path lost.
- **`/historical/markets` ignores `min_close_ts`/`max_close_ts`**; `/markets` honours them.
  Window filters against the historical path must be client-side.
- **Field parity is exact**, 45/45 on the same ticker, zero fields on either side alone.
- **`open_interest_fp` is 0.00 on historical for 41 of 41 overlap-band markets.** One field,
  every market. Parked as **P8**; which path is correct is not established.
- **Candlesticks reach as deep as market rows**: 18 of 18 tickers return candles on the
  historical path back to 2021-07-26, and the four overlap-band tickers return **identical
  counts on both paths** (33/33, 33/33, 75/75, 44/44) — a completeness gate that passes.
- Authentication reach: **untested, recorded as untested, not assumed equal.**

**A3 done** → `docs/INFRA.md` (`ff026a5`). Ten series, both endpoints paged to cursor
exhaustion, distinct `event_ticker` counted in code. Largest gaps: **KXBTC15M 16,550**,
**KXETH15M 16,537**, **KXSOL15M 14,173**. Largest *ratio*: **KXNCAABBGAME at 428×** (7,272
events against 17 markets — out of season). Seven crypto 15-minute series exhaust at
6,449–6,451 markets, which is 67 days × 96/day to within 0.3% — the floor measured off weather
and baseball, confirmed by a third product family.

### Three errors made this session, all caught before they shipped

1. **A 429 read as end-of-data.** A paging loop broke on `st != 200`, so a rate-limit reply on
   page 7 was recorded as cursor exhaustion: `/events?series_ticker=KXMLBGAME` reported
   **1,400** events. Paged again with the 429 retried it returns **4,083**. Same failure shape
   as reading a 403 as a 404. Every pagination now records *why* it stopped, and only
   `cursor_exhausted` or `empty_page` may be read as a complete answer. Written into INFRA.md.
2. **A field-parity claim framed against an expectation instead of against the other path.**
   An earlier note in this run said `fee_multiplier`, `fee_type` and `settled_time` were
   *absent from historical*. They are absent from **both** paths' market rows — they are
   series-level properties, present and correct on `/series/{ticker}`. Corrected in A2.3
   before it propagated. `KXMLBGAME` carries `fee_multiplier: 0.5`, a live instance of the
   "one series charged half of what the code assumed" hazard.
3. **Prior art not consulted first.** `docs/INFRA.md` already recorded, the same day, that the
   live floor is a sliding window advancing one day per day across sixteen series, and that
   `/events` outruns `/markets`. CLAUDE.md §4 requires searching for prior art **before**
   building a collector. Nothing measured was wrong and the independent numbers agree to the
   day, but the "assumed" list overstated what was unknown. Recorded as Amendment 1 rather
   than silently corrected.

**Parked this session:** P6–P9 → `PARKED.md` (`75ce66c`). **P9 has a clock on it**: the live
floor advances one day per day, the historical cutoff has not moved, and if both hold they meet
on or about **2026-08-20**.

**No STOP conditions hit this session.** No registry verdict, figure or `revive_if` was
changed. `worker.js` untouched. No trade, no deployment.

**Next action:** A4 — characterise `archive.pmxt.dev`'s `timestamp_received` receipt lag:
the distribution of gaps within a market, stability across markets and hours, and whether it
can be bounded. Then GATE 1 → `registry/historical/GATE1.md`.

### Session 2 continued — Phases B, C, D, E

**GATE 1** → `registry/historical/GATE1.md` (`92b4d89`). Four of five questions answered with
measurements; the fee question answered structurally and explicitly could-not-establish
numerically. B1, B2 and B3 licensed with carried conditions.

**B1 done** → `registry/historical/B1-COLLECTION-2026-08-14.md` (`f0170de`),
`data/historical/MANIFEST.json` (`c4a3638`), `scripts/b1_collect.py` (`11c5e38`),
`scripts/b1_manifest.py` (`ce16c19`), `scripts/b1_gate3_refetch.py` (`a5427df`).
**7,269,014 markets / 351,653 events / 6,703 series, back to 2021-07-01**, in 19,483 requests
with **zero 429s**. Row count equals unique-ticker count exactly. Two-thirds of the exchange's
settled history by row count is intraday crypto and FX. Nine crypto series were stopped by
budget and are marked incomplete with their cursors retained. The data is ~1 GB and is **not**
committed — parked as **P10**.

**Phase C:** C1 → `registry/FEE-CEILING-AUDIT.md` (`84601ad`) — **no registry entry states an
assumed order size**, because every cost model in the project is a size-free continuous
function. That reverses the packet's expected failure mode. C2 (rule) → `CLAUDE.md` (`9bdfded`).
C3 → `README.md` (`45ceb3a`). C4 → audit note appended to `registry/H64-RESULT.md` (`ea65c44`),
splitting it into an answered quote-level null and a could-not-establish fill-level gate, and
reconciling 6.22% against 4,081 usable of 13,832. C5 → `registry/REVIVAL-CANDIDATES.md`
(`55b7cf2`). C6 → 36 passing tests in `tests/` (`6e69f21`, `7d7ee30`, `cfee248`, `fc76eab`).

**Phase D parked** as **P13**. Three of its four conditions fail.

**Phase E:** `registry/retention/README.md` amended (`4d85f1e`) — purpose narrowed, and the P9
cutoff check added to each remaining run. The scheduled task's prompt was updated to match.

**A fourth error caught this session:** the Gate 3 re-fetch check counted four HTTP 429
responses as **data mismatches**. A status code is not a disagreement. Fixed by separating
`http_*` outcomes from field comparisons and retrying them. That is the third time in this run a
status code was nearly read as data, after the 429-as-exhaustion and the ignored `ticker=`
filter.

**One deviation from the packet, recorded:** B1 ran on 4 workers rather than 3 after request
13,457. The packet's "3 threads at 0.55s" targets ~5.45 req/s by its own arithmetic; latency held
3 threads to 4.06. Zero 429s across all 19,483 requests, backoff never disabled.

**No STOP conditions hit.** No registry verdict, figure or `revive_if` changed. `worker.js`
untouched. No trade, no deployment.

**Not completed:** C2's full measured/asserted tagging pass across `CLAUDE.md`, `docs/INFRA.md`
and `docs/STATE.md` — the rule was added, the tagging was not done. Time limit, not instrument
failure. B2 and B3 not started.
