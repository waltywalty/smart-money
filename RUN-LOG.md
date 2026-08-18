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

---

## Session 3 — 2026-08-17 (packet 4 + Addendum A)

**Constitution re-read** before any work, from the tree at `7374215` fetched as a tarball —
deliberately a different path from the contents API, which is rule 12 applied to the re-read.

**GATE 0 does not pass** → `docs/GATE0.md` (`101e8eb`). The R2 endpoint arrived as the literal
string `<paste>`, and Kernel's credential store has **no route** to hand a secret to a script —
measured with a dummy value before the real PAT was requested, probe credential and probe VM both
deleted. Per Addendum A's corrected fallback, **Phase 1 did not start; Phases 2 and 3 ran instead.**

**T0.2 done and live** → `scripts/gh_commit.py` (`de75d97`), `tests/test_gh_commit.py` (`972c482`).
`check()` no longer reads `permissions.push` — zero references remain outside the docstring
explaining why. Against the real token: `201 wrote / 200 read back unauthenticated: CONTENT MATCHES
/ 200 deleted / PASS / exit=0`. **11 stubbed regression tests**; full suite **47, all passing**.

**T2.1 done** → `registry/FEE-MODEL-T2.1.md` (`db44da9`). `analysis/h56/analyse.py` line 31 is
`math.ceil(0.07*p*(1-p)*100)` with **no `contracts` term** — **the one-contract charge**, the
dearest point on the size axis. **Packet 4 and my own C1 both had this backwards.** The hurdle is
−4.39c at 1 contract, **−3.86c at 100**, −3.85c continuous — at size the bar is *easier*, not
harder. Published statistic reproduced first as a control (−4.39c [−5.21, −3.66] against
[−5.20, −3.67]). **Verdict unchanged at every size.** The effect is small because H56's asks are
median 18.7c, nowhere near where the ceiling bites; it says nothing about the 93–98c band.

**T3.1 done** → **P14**. Three independent signatures, all clear. **No committed code has ever used
`ticker=` as a filter**; the only three committed HTTP callers use `series_ticker=` or the
path-segment form, so **H56 is clean**. Addendum A3's third signature checked **7,075 rows across
50 files against their intended tickers — zero mismatches**. Five studies are permanently
unauditable because their collectors were never committed; listed per hypothesis.

**T3.2 done** → `DEPTH-ANSWERABLE-2026-08-17.md` (`fa625d3`) and Amendment 1 to
`ARCHIVE-LAG-2026-08-14.md` (`6035bf5`). A4 bounded the lag correctly and the method generalises,
but its **95.9% bracketable was one shard** — across 15 hours the range is **0.00% to 99.69%**.
**Degradation is intermittent, not terminal**: two of the four worst hours are 06-07 and 06-08, the
earliest days tested.

**T3.3 done** → `README.md` (`81036c8`). Counted in code: **56** entries, **3** could-not-establish
— it said 55 and 2, having missed H64. Added the INDEX reconciliation (64 rows = 56 + 8 `LOST`) and
the Python suite. **The v11.5 warning needed no fixing — C3 corrected it on 2026-08-14.**

**Addendum A1 done** → `A1-SHARD-SELECTION-2026-08-17.md` (`9ed33b3`). **Shard health IS a
selection variable.** Bracketable % against Kalshi-sourced trades/sec: pearson **−0.631**,
leave-one-out **[−0.698, −0.594]** — never near zero. Degraded shards trade **1.45–1.80x** harder
while covering the same breadth of tickers and series. **Outcome 2 of the three written down in
advance: depth is measurable only on quiet hours, and no depth figure may be stated as a property
of the exchange.** Phase 4 gains a precondition that was not in its original list.

**Addendum A2 done** → `skills/empirical-claims/SKILL.md` (`cbed16d`). **`HEAD` never misbehaved.**
Read at the resource layer, `HEAD` on the impossible 1999 control returns **404** and on a real key
**200**; ranged GET gives 404 and 206. Packet 2's "HEAD returns 200 for keys that do not exist" was
reading `HTTP/1.1 200 Connection Established` — the CONNECT tunnel's status, identical for every
request regardless of method. **The rule stands, the mechanism was wrong.** Rule 11 gains the layer
clause; **rule 12 is in**.

### A new API fact, and it inverts the market endpoints

| endpoint | `ticker=` | `series_ticker=` | `min_ts`/`max_ts` |
|---|---|---|---|
| `/markets` | IGNORED | honoured | honoured |
| `/historical/markets` | IGNORED | honoured | **IGNORED** |
| `/historical/trades` | **honoured** | **IGNORED** | **honoured** |

Each verified with an impossible control. **Filter honouring is per-endpoint and not guessable.**

**No STOP conditions hit.** No registry verdict, figure or `revive_if` changed. `worker.js`
untouched. No trade, no deployment. **The Cowork sandbox rolled back mid-session and destroyed a
prepared patch; nothing was lost**, because every rebuilt artifact went to `main` as it was
produced — Walton's ruling working as intended.

**Next action:** the R2 endpoint, then Gate 0 line 3, then Phase 1.

---

## Session, 2026-08-18 — packet 5, Phase A0 + Phase B + Phase C

Three clocks agreed at the start (VM, Kalshi, GitHub): `2026-08-18T01:48Z`. Measurements from
2026-08-17 keep that date in their filenames; this session's own work is dated 08-18.

**A0 — control audit, run before A1 as instructed.** Every control class re-run live at the access
level of the measurement it certified, not reasoned from documents. **One void class: an
unauthenticated probe of the private R2 bucket, where control and real key both return 400.** It was
recognised as void in the session that ran it, and everything it touched is established at
authenticated access, so **no finding reverts to unverified and `PARKED.md` gets no entries from
A0**. That absence is the report, not a skip.

The packet's leading candidate — packet 2's 1999-dated key on `r2kalshi.pmxt.dev` — **fails on one
count, not two**: the host is public, so control and measurement held matching (anonymous) access
and the control does separate at 404 against 206. It failed on *layer*, and that was corrected on
2026-08-17.

**A0's own new finding:** an impossible control is only half a control. **An absence claim also
needs a probe that must succeed, in the same pass** — otherwise the control and the measurement
return the same status and the pair cannot tell *gone* from *everything is 404 right now*. Every
absence claim in the register passed this, but **by habit rather than by rule**. Now in rule 10.

`skills/empirical-claims/SKILL.md` rules 10–14 consolidated into one status-layer rule with five
instances. Rules 12 and 13 kept at their numbers because `gh_commit.py`, its tests and this log all
cite "rule 12"; 11 and 14 became pointers rather than renumbering live references.

**Phase B — the close of the programme.** `registry/KALSHI-PROGRAMME.md` (the hurdle on both axes
with its decomposition, the three confirmed effects and why none is money, the fifteen mechanisms as
a five-minute screen, the instrument-failure catalogue, the seven right-for-the-wrong-reason entries
enumerated in one place **for the first time**, and what the data constraint actually was).
`skills/research-method/SKILL.md` lifts the method off the venue, keeping the Kalshi instances as
worked examples. `docs/ASSETS.md` inventories everything built, with rebuild and repoint costs.

**Phase C.** P14's third signature had already run — 7,075 rows checked, **0 mismatches** — so it was
confirmed, not re-run. The two-hour trade hole and the `/events` attribution wording are now
amendments in `INFRA.md`, the latter pinned at **falsified / replacement supported / not reproduced**
so it cannot harden. P15 and P16 parked.

**The census question is answered by its own failure.** `PUT .github/workflows/census.yml` → **403**:
the per-session PAT carries `Contents: write` but not `Workflows: write`. Every other write in the
session succeeded with the same token. So whether an Actions runner reaches Kalshi cleanly and can
commit without a paste is **could not establish**, not a null — and the workflow is committed out of
the way at `.github/CENSUS-WORKFLOW-PENDING.md` rather than rebuilt from memory later.

**One correctness fix.** The create-guard printed *"a 200 here means the path existed after all"*
for every non-201 status, including the 403 above — a misleading message on a refused write. It now
distinguishes 200, 401/403 and everything else. 16 tests still pass.

**A1–A3 (H65) are NOT started**, per Walton's instruction to bring A0's result for a ruling first.
Phase B was run in the meantime rather than idling, as the packet directs.

**No STOP conditions hit.** No registry verdict, figure or `revive_if` changed. `worker.js`
untouched. No trade, no deployment.

**Next action:** Walton's ruling on A0, then A1 — execute B1's sealed design exactly.

## Session, 2026-08-18 (continued) - the A0 ruling, then H65

**A0 ruling applied.** Walton parked T1.4's first-pass statement only: its claim that three R2
objects were unreadable without credentials was certified by a probe where the impossible key and
the real keys both returned 400, so it established nothing. **Probably true, not shown.** Everything
resting on the authenticated 404 control stands. Parked as **P17**, and
`registry/historical/A0-CONTROL-AUDIT-2026-08-18.md` carries a dated amendment with its original
"nothing to rule on" conclusion **left on the page** - the point being that the reasoning changed,
not that it was never written. The audit had laundered a void control in its own closing paragraph,
on its own subject matter.

**Census stays parked as P15.** Not attempted again this session.

**H65 executed exactly as B1 sealed it** (`4775d76`). All three abandonment conditions were tested
first and none fired: the book **is** reconstructible from `orderbook_delta` (the pre-registration's
single largest untested assumption); bracket-width p99 across admitted shards runs **median 6.0s,
max 59.0s** against a 60s threshold; and every size point clears the 150-event bar (198-201).

101 archive hours probed, **41 admitted** at the sealed 80% bracketable rule. Books replayed to
T-10m, YES bought at the ask off resting NO bids, fees from `analysis/fees/fee_model.py` at
`regime='documented'`.

**Verdict: CONFIRMED, branch one.** Flat from 1 to 10 contracts, monotonically worse above, and
**negative at every point** - -3.11c at 1, -2.98c at the least-cost point of 2, -5.89c at 100,
**-10.20c at 500**. The least-cost point fails B1's own calling rule (neighbours differ by 0.13c and
0.01c against interval half-widths of 4.56c and 4.67c), so it is reported **flat, not a minimum**.
Span across the axis **7.23c against a fee arm bounded at 0.53c** - the spread arm is 13.6x the
entire fee arm, which is what the pre-registration predicted and why.

**Two things the study did not flatter itself about.** Leave-one-series-out **crosses zero at every
size up to 25 contracts** - dropping `KXCS2MAP` alone turns the pooled figure positive at small
size - and family dispersion (+3.42c to -15.26c at one contract) is larger than the whole size axis.
`KXATPCHALLENGERMATCH` reads positive and is **explicitly not reported as a result**: B1's branch
three requires LOO-series, a depth-source replication and a quiet-hour check, and only the first has
been done - and the third is decisive, because the entire study runs on admitted shards, which A1
established are the quiet hours.

**The sharpest limit was not anticipated by the pre-registration:** 54% of markets on admitted
shards carry **no snapshot before their entry instant**, which costs more than the archive ending
and more than the admission rule. **201 events of 1,086 survive - 15.4% of the target population.**

`registry/INDEX.md` rebuilt: 57 substantive entries, H65 CONFIRMED. No other verdict, figure or
`revive_if` changed. `worker.js` untouched. No trade, no deployment.

**Next action:** Walton's ruling on H65.

**H65 ruling applied, 2026-08-18.** Branch one confirmed, with three changes to how it is stated.

**Shape and magnitude separated.** Shape CONFIRMED - negative at every size point, flat 1-10,
monotonically worse above, spread-dominated at 13.6x the fee arm. **Small-size magnitude NOT
separated from zero**: the bootstrap CI excludes zero only from 100 contracts up and
leave-one-series-out only from 50 up. The entry now says plainly *do not quote -3.11c at one
contract as a measured hurdle*.

**Family dispersion promoted to a finding about the pooled hurdle generally.** At one contract, one
horizon, one week, the five families span **18.68c** - against 7.23c for the whole size axis and
1.87c for the whole horizon axis, so **2.05x both measured axes combined**. Every pooled hurdle
figure in the registry, H56's -4.39c included, is weighted by its family mix at least as much as by
the variable it names. Same shape as false positive #7 one level down. Folded into
`registry/KALSHI-PROGRAMME.md` and generalised in `skills/research-method/SKILL.md` as *a cost
quoted without its composition is not a cost*.

**`KXATPCHALLENGERMATCH` recorded as OBSERVED, NOT REPORTED**, pending branch three. Requirement (b),
a depth-source replication, **cannot currently be satisfied at all** - `archive.pmxt.dev` is the only
Kalshi book source that has existed and it stopped at `2026-06-11T03`. So it is not merely unreported,
it is unreportable with the data that exists, and it is written down so it is not rediscovered as new.

**Phase B updated** rather than rewritten: the synthesis carries a dated amendment superseding its
own section-1 framing of the size axis, and the method skill gains two rules - composition beside
every pooled figure, and separate the shape from the magnitude and say which you established.

Commits: `07a8296` H65 entry - `daa6e5f` registry - `5ef44cf` INDEX - `7a70789` synthesis -
`c57ab2c` method skill. Census remains parked as P15. No other verdict, figure or `revive_if`
changed. `worker.js` untouched. No trade, no deployment.

**Packet 5 closed out** at `CLOSEOUT-2026-08-18.md` (`e2ad0dd`). MEASURED / INFERRED / ASSUMED as
three lists, parking lot ranked, three findings that were wrong before they were right, H65 in B1's
own words, and a portability section that describes and stops. Family dispersion is a MEASURED item
in its own right rather than a line in a verdict. The depth ceiling is recorded as a hard limit in
`docs/INFRA.md` (`0205041`) so it is findable without reading footnotes: no public Kalshi book source
outside 2026-05-14 to 2026-06-11T03 has ever existed, so replication is impossible and
**unreportable** is the correct word, not pending.

**P15 RESOLVED, 2026-08-18.** Walton added Workflows permission; the census workflow landed and
**run #1 went green**. Verified from the resources with controls, not from the report: impossible
commit sha **422**, run #1 **success**, commit **`bc2c8bf`** authored and committed by
**`github-actions[bot]`**, writing `registry/retention/CI-CENSUS-LOG.md` using the built-in
`GITHUB_TOKEN` - **no PAT, no paste, no human**. Kalshi from a shared runner IP: cutoff 200, live
floor 200, impossible control 200/0 rows, positive control 200, both controls in one pass.

**Recorded as the durable write-path finding** in `docs/INFRA.md` (`50227db`), unparked in
`PARKED.md` (`afaf328`), added to `docs/ASSETS.md` as asset 5 (`5d05e6f`), and folded into the
close-out (`8973d2e`) - which re-ranks its own parking lot, since the item a person could fix has
been fixed and **the top item is now the one nobody can**.

**Not over-claimed:** seven requests establish reachability and the write path, not a rate-limit
regime. A shared runner IP has a bucket history set by strangers, so the ~6 req/s clean band from a
Kernel VM must be re-measured on Actions before any bulk pull moves there.

**Incidental, from run #1's own data:** `market_settled_ts` 2026-06-18, live floor 2026-06-11T04:59,
gap ~7 days - unchanged since 08-17, up from 6 on 08-14. P9 remains closed, and the check that
confirmed it ran without anyone asking.
