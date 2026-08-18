# INFRA.md — operational facts, changes slowly
Endpoint schemas, rate limits, sandbox behaviour, deployment topology.
Everything here was learned the hard way; do not delete a line because it looks
obvious.

## 3. Infrastructure — the part that keeps getting relearned

### Raw HTTP works, and it is the whole game

The **Kernel MCP browser VM** (`mcp__Kernel__manage_browsers` → `create`, then
`mcp__Kernel__exec_command`) has unproxied internet. `curl` and `urllib` reach
`api.elections.kalshi.com` and all Polymarket hosts directly, returning **raw bytes**,
real HTTP status codes, real exit codes. Python 3.10 is present; **git is not**.

This matters more than any single result. For most of this project's life every fetch
went through a summarising layer that **invented values**: a quote returned as
`0.29/0.30` where the book said `0.05/0.06`; `limit=100` silently returning 34 rows;
an empty book reported as `0.0000/1.0000`, injecting a phantom 50¢ midpoint; the *same
wrong answer* reproduced across two independent fetches. Every false positive in this
project traces to it. **Do all measurement through Kernel. Never through WebFetch.**

Verified clean on 2026-08-12: `limit=100` → exactly 100 rows / 400,039 bytes; six pages
→ 1,200 rows, 1,200 unique tickers, zero gaps; list quotes vs order book agreed exactly
on 15 of 18 liquid markets (other three: empty-book convention, and one 1¢ tick on a BTC
market between sequential calls); Polymarket's gamma `outcomePrices`, `/midpoint` and raw
`/book` agreed to 0.0000.

### Tool routing — which surface does which job

| Job | Use | Never use |
|---|---|---|
| Any price, book, or outcome measurement | Kernel VM, raw `curl`/`urllib` | **WebFetch**, or any summarising fetch layer |
| Library / API docs (pandas, pykalshi, pmxt…) | Context7 → `resolve-library-id`, then `query-docs` | Recall from memory — schemas have migrated |
| Finding prior art before building | Kernel VM + GitHub code search API | — |
| Long collection runs (>10 min) | Kernel VM, checkpointed, 3 threads @ 0.55s | A local or Cowork session |
| Writing and committing code | Local Claude Code | The Cowork sandbox (cannot push) |
| Analysis write-ups, xlsx, PDF, chart packs | Cowork | — |
| Trading, deploying | **Nothing. Walton, manually, in writing.** | Everything |

Connectors are disabled per-project rather than instructed against: a compacted
context can lose an instruction, but it cannot call a server that is off.

### Sandboxes are not storage

The Cowork sandbox **rolled back three times on 2026-08-10 and 2026-08-12**, each time
destroying analysis directories and reverting the registry. Kernel VMs expire on their
own timeout. **Nothing that matters may live only in a sandbox.** Deliver results to
Walton and get them into this repo as you go, not at the end.

**A session ends with a commit, not a summary.** If work exists only in a
conversation or a sandbox when the session ends, it does not exist. v12.3 and
H22–H27 were lost this way. Write to the repo as you go.


### Getting work into this repo

- The **Cowork sandbox cannot push.** Its git proxy refuses any repo outside the
  session's authorized set — it strips your credential and won't inject its own. Reads
  and `git clone` work (public repo); writes return 403. A GitHub PAT does not help.
  `api.github.com` is also proxied and 403s from Cowork; **from Kernel it works fine.**
- **Claude Code can push, but only to its own branch** — sandbox push protection, not a
  permissions problem, not fixable with a token. It must open a PR.
- `.github/workflows/automerge.yml` auto-merges PRs from `claude/*` branches by the repo
  owner, so that PR lands by itself.
- **Never use GitHub's web "Upload files" button for folders** — it flattens every path.
  On 2026-08-12 that put 84 files in the repo root and silently destroyed
  `analysis/h50/analyse.py` (same basename as `analysis/h56/analyse.py`; one overwrote
  the other with no error). "Create new file" with a slashed path is safe.

### Kalshi API

Base `https://api.elections.kalshi.com/trade-api/v2`, no auth for public market data.

- **Schema migrated.** Fields are `yes_bid_dollars` / `yes_ask_dollars` / `volume_fp` /
  `volume_24h_fp` / `open_interest_fp` / `liquidity_dollars`. Order book is
  `orderbook_fp` with `yes_dollars` / `no_dollars` as `[price, size]` string pairs.
  Old names return undefined. `liquidity_dollars` reads `0.0000` even on a market with
  236k volume — treat as dead.
- **Candlesticks unchanged**: `yes_ask.close_dollars`, `yes_bid.close_dollars`, and
  `end_period_ts` is the **inclusive end** of the bucket.
- **Outcomes must come from `?status=settled`.** Both `/events?with_nested_markets=true`
  and the single-market endpoint serve stale `active`/blank results for long-settled
  markets.
- **Rate limit is real and returns 429.** Sustainable: **3 threads, 0.55s sleep**
  (~13% rejection, all retried). 4 threads at 0.4s bounces 42%. Always resume from a
  checkpoint; always retry with backoff.
- `?status=settled` unfiltered is flooded with `KXMVE*` machine-generated combinatorial
  markets — 2,000 of the first 2,000 rows. **Exclude `KXMVE*` a priori.**
- Fees: taker `ceil(M·0.07·p·(1−p))`, maker `ceil(M·0.0175·p·(1−p))`, rounded up on
  order total. A few series carry `fee_multiplier: 0` but have zero settled markets.
- Band semantics: `less` with cap C wins when actual < C; `between` wins when
  floor ≤ actual ≤ cap; `greater` wins when actual > floor. **Read strike fields, never
  titles.**

- **`ticker=` is not a filter.** `GET /markets?ticker=X` and `GET /historical/markets?ticker=X`
  both **silently ignore** the parameter and return the unfiltered head of the collection — which
  begins with the `KXMVE*` machine-generated flood, closing at `2026-06-14T23:45:00Z`. Verified
  2026-08-14 with an impossible control key: `?ticker=KX-IMPOSSIBLE-CONTROL-19990101` returns
  **HTTP 200 with 5 markets** on both paths, while `?series_ticker=` and `?event_ticker=` controls
  correctly return 0 rows. This produced six different quarter-hour crypto markets all reporting
  the *same* close time, and only the control exposed it. **Filter by `event_ticker`; read a single
  market from `/markets/{ticker}` (path segment, not query), whose control returns 404.**

### Kalshi retention — there is none. There is a live/historical split.

Measured and documented 2026-08-14. Every backward-looking Kalshi study in this project
is shaped by this, so it lives here rather than in a dated note.

**Kalshi deletes nothing.** Data sits in a **live** set or a **historical** set, split at a
boundary you can query:

```
GET /trade-api/v2/historical/cutoff
  {"market_settled_ts":"2026-06-14T00:00:00Z", "trades_created_ts":"...", ...}
```

Markets settling before that timestamp are served by a **parallel endpoint family**, not by the
normal one:

| live | historical |
|---|---|
| `/markets?…` | `/historical/markets?…` |
| `/series/{s}/markets/{t}/candlesticks` | `/historical/markets/{t}/candlesticks` |
| `/trades`, `/portfolio/fills`, `/portfolio/orders` | `/historical/trades`, `/historical/fills`, `/historical/orders`, `/historical/positions` |

`/historical/markets?event_ticker=HIGHNY-21AUG06` returns a market from **2021** with its
settlement result. The same event returns **zero rows** from `/markets` under every status
filter. Kalshi's docs state it: *"Candlesticks for markets that settled before the historical
cutoff are only available via `GET /historical/markets/{ticker}/candlesticks`."*

**The live set slides.** Its floor by `close_time` was uniform at 2026-06-08 on 2026-08-14 across
sixteen series carrying between 25 and 6,348 events, and advanced exactly one day from the day
before. Uniform across three orders of magnitude of volume rules out count-based expiry. Two
traps sit next to it:

- **`/events` outruns `/markets`.** `/events?series_ticker=…&status=settled` lists events back
  years; `/markets?event_ticker=` for those events returns nothing. Event metadata is not
  evidence the market data is reachable *on that endpoint*.
- **A single page gives a false floor.** `KXMLBGAME` reads 2026-07-05 on one page of 1,000 rows
  and 2026-06-08 fully paged; `KXBTC15M` reads 2026-08-03 against 2026-06-08. **Follow the cursor
  to exhaustion before reading a floor off anything.**

**How far `/events` outruns `/markets` — measured 2026-08-14 (A3).** Ten series, both
endpoints paged to **cursor exhaustion** on every row, distinct `event_ticker` counted in
code. `stop_reason` recorded per series; all twenty pagings terminated on an empty cursor,
none on a page cap and none on a non-200.

| series | `/events` | `/markets` | gap | ratio |
|---|---:|---:|---:|---:|
| KXBTC15M     | 22,999 | 6,449 | **16,550** | 3.6× |
| KXETH15M     | 22,986 | 6,449 | **16,537** | 3.6× |
| KXSOL15M     | 20,622 | 6,449 | **14,173** | 3.2× |
| KXXRP15M     | 17,403 | 6,449 | 10,954 | 2.7× |
| KXBNB15M     | 14,020 | 6,450 |  7,570 | 2.2× |
| KXHYPE15M    | 14,019 | 6,449 |  7,570 | 2.2× |
| KXDOGE15M    | 14,019 | 6,451 |  7,568 | 2.2× |
| KXNCAABBGAME |  7,272 |    17 |  7,255 | **428×** |
| KXITFMATCH   | 14,649 | 7,750 |  6,899 | 1.9× |
| KXITFWMATCH  | 13,362 | 6,730 |  6,632 | 2.0× |

The three largest absolute gaps are **KXBTC15M, KXETH15M and KXSOL15M**. The largest
*ratio* is **KXNCAABBGAME at 428×** — college basketball is out of season, so its live
market presence has collapsed to 17 events while 7,272 event shells remain listed. Ratio
and gap rank differently and neither alone describes the endpoint.

**The `/markets` counts independently confirm the sliding floor.** Seven unrelated
15-minute crypto series all exhaust at 6,449–6,451 distinct events. A 15-minute series
produces 96 events/day; 2026-06-08 → 2026-08-14 is 67 days, and 67 × 96 = 6,432. The floor
measured off weather and baseball series predicts the crypto counts to within 0.3%. Three
unrelated product families, one boundary.

**A non-200 mid-pagination is not the end of the data.** `/events?series_ticker=KXMLBGAME`
was read as 1,400 events on 2026-08-14 by a loop that broke on `st != 200`; a 429 arrived
on page 7 and was silently recorded as exhaustion. Paged again with the 429 retried, the
same query returns **4,083**. Every pagination must record *why* it stopped —
`cursor_exhausted`, `empty_page`, `http_<code>`, or `page_cap` — and only the first two may
be read as a complete answer. This is the same failure shape as reading a 403 as a 404.

**What this means for study design.** Historical depth is not a constraint — design the sample
the question wants, then route each market to the right endpoint by comparing its settlement time
to `/historical/cutoff`. Do not build a collector to beat a deadline; there isn't one. The
2026-08-13 coverage note concluded the opposite from absence in one endpoint without checking
whether another held it, and that error produced a false four-day deadline, two out-of-memory
collector failures and a nine-month self-collection proposal. **Read the API docs before
inferring a policy from response shapes.**

### Polymarket

`gamma-api.polymarket.com/markets|/events`, `clob.polymarket.com/book|/midpoint|/prices-history`,
`data-api.polymarket.com/trades`. `clobTokenIds[0]` is the YES token. Winner source is
`clob.polymarket.com/markets/{cid}` → `tokens[].winner`, **only** — a summariser once
defaulted every `winnerIndex` to 1 and nearly logged two fake reversals.

`worker.js` calls **Polymarket only** (clob ×8, gamma ×4, data-api ×4, plus ntfy.sh).
Zero Kalshi endpoints — Kalshi schema changes do not affect production.

### The worker

Live is **v11.4**, and so is the file in this repo — verified 2026-08-13 by fetching the
worker's own `GET /`, which returns `version` from the source constant. **There is no
evidence v11.5 was ever deployed**; that claim sat here unchecked for days and one HTTP
request settled it. **Ask the worker, not the dashboard.** See `DEPLOY.md`.

**v12.3 existed and was lost** to a container rollback on 2026-08-10 — and was then **recovered
on 2026-08-13 from Cloudflare's own version history**, which nobody had checked for three days.
Archived verbatim at `archive/worker-v12.3.js`. It does not run today: its Kalshi leg reads
pre-migration field names and would silently record zeros. See `archive/WORKER-V12.3-RECOVERY.md`.
**"Unrecoverable" was true of the sandboxes and false of the world.**

Subrequest ceiling 50 per invocation, worst measured cycle 22 — exceeding it silently
kills scheduled runs and once looked exactly like a broken cron trigger. KV writes ~288/day
against a ~1k/day free tier.

### R2 object store, and three ceilings found before Phase 1 ran

Bucket `smart-money-data`, endpoint `https://<account>.r2.cloudflarestorage.com`, region `auto`.
Credentials are per-session environment variables — `R2_ENDPOINT`, `R2_BUCKET`,
`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` — never committed. Client: `scripts/r2.py` over
`scripts/r2sig.py`. Gate: `python3 scripts/r2.py roundtrip 1`.

**[measured 2026-08-17] The data outlives the VM.** An object written from one VM read back
byte-identical (sha256 `931eb01d…`) from a fresh VM in a different metro after the first was
destroyed. That is the packet-3 failure closed.

**Ceiling 1 — `Expect: 100-continue` is never answered.** curl sends it on any body over ~1 KB.
Neither the Kernel egress proxy nor R2 responds to the interim, so curl reports **`http=100`** as
the status and blocks until `--max-time`: a 16 MB PUT took **120 s and returned 100**. With
`-H 'Expect:'` the same PUT takes **2.6 s**. **This is almost certainly what made boto3's
`put_object` hang** — LIST worked, `curl -X PUT` worked, `put_object` hung, all through the same
proxy with the same credentials. Any HTTP client used here must disable Expect, and **an interim
1xx must never be treated as success.**

**Ceiling 2 — memory.** The in-memory path (`request()`) is **OOM-killed between 64 MB and
256 MB** on a 977 MiB VM. 64 MB passes at 12.8 MB/s; 256 MB is killed. Use `request_file()`,
which streams from disk and never loads the body: **128 MB streams at 9.3 MB/s with a sha256
match and RAM flat.**

**Ceiling 3 — VM disk varies, and can be small.** One VM had 9.8 GB; another had **783 MB total,
352 MB free**. A collector that accumulates before uploading will die on the small ones.
**Phase 1 must write one series file, upload it, delete it locally, then move on.**

**[measured 2026-08-17] Python networking is not portable across Kernel VMs.** Some export
`HTTPS_PROXY=https://ns.internal:3129` — a proxy that speaks **TLS on the proxy leg**. curl handles
it; Python's `urllib` opens a plain socket, sends `CONNECT`, and the proxy closes on it
(`RemoteDisconnected`). Other VMs export an `http://` proxy and urllib is fine. **`gh_commit.py
check` failed on a fresh VM for this reason, on a perfectly good token.** Both `gh_commit.py` and
`r2sig.py` therefore shell out to curl. This retroactively explains a class of intermittent
failure this project has hit and never diagnosed.

**[measured 2026-08-17] Kernel's credential store cannot return a secret to a script.** `create`
reports `has_values: true`; `get` returns metadata and key *names* only; a VM created after the
credential has it in neither its environment nor its filesystem; no Kernel-internal endpoint is
routable from inside the VM. Tested with a dummy value, probe deleted. **Do not re-attempt this.**
Credentials are pasted per session; the mitigation is to make their loss cheap, not to make them
durable.

---

## Amendment, 2026-08-17 - rate limiting re-measured (T1.2)

Appended, not edited. The paragraph above beginning *"Rate limit is real and returns 429"*
stands as the record of what was observed; these are the parameters that reproduce.

Fifteen arms, one variable at a time, same VM, same afternoon (`data/phase1/GATES.json`):

| request rate | rejection |
|---|---|
| 1.2 - 5.9 req/s, either endpoint | **0% in 550 requests** |
| ~11 req/s | 0.8% |
| ~28 req/s | 16.2% |
| 62 - 73 req/s | **0% to 53%, depending on what ran before it** |

Three corrections:

1. **`3 threads / 0.55s` is 3.6 req/s and does not reject.** 0 of 240, both endpoints. The
   ~13% figure recorded beside those parameters belongs to a much higher rate; ~28 req/s
   measures 16.2%. The observation was real; the parameters written next to it are not the
   ones that produce it.
2. **`4 threads / 0.4s` did not bounce 42%.** It measured 0 of 120.
3. **The limiter is shared across endpoints and has memory.** `/historical/markets` at 69
   req/s measured 0% on its first burst, then 32.5% and 44.1% on identical repeats minutes
   later. There is no `/historical` exemption - the first burst simply arrived with the
   bucket full. **A single ordering of arms is not a control.**

Practical rule, unchanged in direction and corrected in reason: **stay at or below ~6 req/s.**
Not because three threads is a magic number, but because that is the band measured clean even
immediately after a burst that was being rejected at 44%.

## Amendment, 2026-08-17 - `/historical/markets` reports `finalized`, never `settled`

The rule *"outcomes must come from `?status=settled`"* above is about the **live** `/markets`
list. On `/historical/markets` the same markets report `status: finalized` on **100%** of rows
and `settled` on **0%**, with `result` populated on 100%. Measured on 2,000 rows across
`KXHIGHNY` and `KXMLBGAME`, cross-checked on `GET /markets/{ticker}` and
`GET /historical/markets/{ticker}`.

A collector that carries `status == "settled"` over to the historical path filters away every
row and reports an empty dataset as an honest zero.

Related: **`result` is not binary.** `KXMLBGAME` page 1 returns `no` 495, `yes` 495, `scalar` 10.

## Amendment, 2026-08-17 - restricted collection is 30x smaller than the full pull

Scope derived in `data/SCOPE.md` from `registry/hypotheses.json` and `analysis/`: **30 series,
110,836 rows, 241 MB raw, 10.1 MB gzipped** against the prior full-exchange 7.27 GB. 130 pages,
all HTTP 200, no retries. Four of the 30 have **zero** settled history, `KXRAIN` among them.

## Amendment, 2026-08-17 (second) - the 13% figure is FALSIFIED, and the knee is unbracketed

This corrects the amendment immediately above, written 90 minutes earlier. That one reported the
measured rates as though they were properties of the API. They are not.

**1. The "~13% rejection at 3 threads / 0.55s" figure is falsified, not merely unreproduced.**
That configuration is **3.6 req/s** and returned **0 rejections in 240 requests**, on both
endpoints, including immediately after a burst that was being rejected at 44%. Nothing about
"3 threads / 0.55s" produces 13%. The number is not a description of that setting and should not
be cited as one. Whatever produced 13% was running faster than the label says - most likely far
faster, since ~28 req/s measures 16.2%.

Anything that cited "13% at 3 threads" as a reason to run slowly was **right to run slowly for
the wrong reason**. The direction survives; the mechanism does not.

**2. The knee is UNBRACKETED between 5.9 and ~28 req/s.**

| req/s | rejection | status |
|---|---|---|
| 1.2 - 5.9 | 0% in 550 requests | measured |
| **5.9 - 28** | **unknown** | **never measured - the knee is somewhere in here** |
| ~11 | 0.8% | one arm only, single ordering |
| ~28 | 16.2% | measured |
| 62 - 73 | 0% to 53% | measured, order-dependent |

The ~11 req/s point sits inside the unbracketed band but was run once, in one position, so it
brackets nothing on its own. **Do not quote a threshold. Quote the clean band: at or below ~6
req/s, nothing has ever been rejected.**

**3. The rejection curve is a property of (endpoint, SOURCE, recent history) - not of the API.**
Re-running the arms from a different Kernel VM in a different metro: **3,200 requests at up to 64
threads, zero 429s**, where the first VM began rejecting after roughly 600 requests in a burst.
Same endpoints, same page size, same afternoon. So:

- A rate figure measured on one VM does not transfer to another.
- Two arms run from two machines are **not an A/B**.
- Depletion could not be induced at all from the second VM, so any experiment needing a drained
  bucket must first demonstrate the bucket is drained rather than assume a burst drained it.

**4. Method requirement, now standing.** Every endpoint A/B in this project must be
**counterbalanced** - each arm run in both positions, both orderings reported - or **washed out**,
with a baseline arm shown returning to its clean value before the next arm starts. See
`skills/empirical-claims/SKILL.md`, *"A single ordering of arms is not a control"*.

## Amendment, 2026-08-18 - a two-hour hole in Kalshi's own settled trade history

**Any study touching 11 June 2026 needs this.** `/historical/trades` over a one-hour window,
newest-first, capped at 1,000:

| hour (UTC) | trades returned | note |
|---|---|---|
| `2026-06-11T06` | 1,000 (cap) | full hour, last trade at 06:59:59.97 |
| **`2026-06-11T07`** | **13** | all thirteen inside the first **0.26 seconds** of the hour, then nothing |
| **`2026-06-11T08`** | **0** | empty |
| `2026-06-11T09` | 1,000 (cap) | full hour |

Controls: `2026-06-10T07` and `2026-06-09T08` both return the full 1,000. Re-probed directly on a
second pass and reproduced exactly; the window boundaries are clean, so it is not a windowing
artefact.

**A collector reads those two hours as *quiet*, not as *missing*.** Activity measured per hour will
show a near-zero rate that is an outage, not a market state. Found during Check 1, where excluding
the two hours moved a diurnal-matched comparison from +3.6% to +10.6%.

## Amendment, 2026-08-18 - the `/events` attribution, and what is NOT claimed

Stated so it does not harden with retelling:

- Packet 2's *"the disagreement is `/events` pagination on high-frequency series"* is **FALSIFIED**.
  A3, measured the same day, paged both endpoints to cursor exhaustion on ten series and found
  `/events` **over**-returning by 1.9x to 428x, with the largest multiples precisely on the
  high-frequency series. The attribution predicts the wrong direction.
- The replacement - a **429 read as end-of-data** truncating the `/events` pass - is **strongly
  supported and NOT reproduced.** Same endpoint, same day, 2.9x undercount on `KXMLBGAME` against
  the observed 2.37x. Ten counterbalanced paging arms on 2026-08-17 all returned 4,124 with
  `cursor_exhausted` and **zero 429s**; the bug cannot fire without a 429 and none could be induced.
- The **2,020 figure is unreliable** and should be treated as a failed measurement, not as evidence
  about `/events` pagination. `4,787` is unaffected - it came from the live path and is separately
  parked as P7 for a different reason.

**Falsified / replacement supported / not reproduced.** Do not upgrade the middle term.

## Amendment, 2026-08-18 - the CI write path: a pasted PAT cannot create workflows

Packet 5 Phase C asked whether a GitHub Actions runner reaches Kalshi cleanly and can commit
**without a pasted secret**. That question is **still unanswered**, and the reason is itself the
finding:

```
PUT .github/workflows/census.yml  ->  HTTP 403
```

The fine-grained PAT supplied per session carries **Contents: write** but not **Workflows: write**,
which GitHub treats as a separate permission. Every other write in this session succeeded with the
same token; only `.github/workflows/` was refused. So:

- **No census workflow exists and none has ever run.** The repository's only workflows are
  `automerge.yml` and GitHub's own `pages build and deployment`.
- The runner's reachability to Kalshi, the status codes it would see, and whether the built-in
  `GITHUB_TOKEN` can commit **are all untested** - `could not establish`, not a null.
- **Unblocking it needs one of:** a PAT with the Workflows permission added, or the workflow file
  committed once by hand through the web UI, after which the built-in token runs it on schedule
  with no paste at all.

The workflow itself is written and ready (`workflow_dispatch` plus a daily cron, probing
`/historical/cutoff` and the live floor with both an impossible control and a known-present
positive control, appending one line to `registry/retention/CI-CENSUS-LOG.md` and committing with
`GITHUB_TOKEN`). It is held out of the repository only by the 403.

## Amendment, 2026-08-18 - the Kalshi depth ceiling. A hard limit, findable here on purpose.

**There is no public source of Kalshi order-book depth outside `2026-05-14` -> `2026-06-11T03`, and
there never will be.**

`archive.pmxt.dev` / `r2kalshi.pmxt.dev` is the **only** public archive of the Kalshi book that has
ever existed. It stopped at `2026-06-11T03` and has not resumed. Re-verified 2026-08-18 with a
positive control beside the impossible one, because a control that must fail is only half a control:

| probe | status |
|---|---|
| impossible key `1999-01-01T00` | **404** |
| known-present `2026-06-10T12` | **206** |
| last published `2026-06-11T03` | **206** |
| first hour after coverage `2026-06-11T04` | **404** |
| `2026-08-16T12`, `2026-08-17T12` | **404** |

The exchange does not retain the book, so **no amount of future collection recovers the past**. Any
Kalshi depth question is bounded to that window, and within it to the **41% of hours** that pass an
80% bracketable admission rule, and within those to **quiet hours** - A1 measured admitted shards
trading 1.45-1.80x less actively than the hours excluded.

**The practical consequence:** a study needing a *second* depth source for replication cannot get
one. That is why H65's positive family observation is recorded as **unreportable with the data that
exists** rather than pending - *pending* invites someone to come back to it, and nobody can.

**What would lift it:** a new public archive, a commercial book feed, or continuous self-collection
from today forward - which buys the future and never the past.

## Amendment, 2026-08-18 - THE DURABLE WRITE PATH. A CI runner reaches Kalshi and commits unattended.

**This is the portable result of packet 5.** Everything else in this file is a Kalshi fact. This one
is about the project's ability to operate without a human, and it transfers to any venue.

**Established end to end, run #1, no pasted secret anywhere in the loop.**

Verified from the resources rather than from a report - the commit API, the runs API and the file
the runner wrote, each with a control:

| check | result |
|---|---|
| control: impossible commit sha | **422** (not 200) |
| workflow run #1, `Kalshi boundary census` | **completed / success**, `2026-08-18T06:01:34Z` |
| commit `bc2c8bf` author **and** committer | **`github-actions[bot]`** `<41898282+github-actions[bot]@users.noreply.github.com>` |
| what it wrote | `registry/retention/CI-CENSUS-LOG.md` (added, +9 lines) |
| credential used | the built-in `GITHUB_TOKEN`. **No PAT, no paste, no human** |

**Kalshi is reachable from a shared GitHub-hosted runner IP, and returns real status codes:**

| probe | status |
|---|---|
| `/historical/cutoff` | **200**, `market_settled_ts` `2026-06-18T00:00:00Z` |
| live floor, `/markets?series_ticker=KXHIGHNY` paged | **200**, min `close_time` `2026-06-11T04:59:00Z` |
| impossible-series control | **200 with 0 rows** - the filter is honoured, not ignored |
| known-present positive control | **200** |

Both controls ran in the same pass, because a control that must fail is only half of one.

**Three things this establishes, in increasing order of what they are worth:**

1. `api.elections.kalshi.com` is not blocked from GitHub's shared runner ranges. Public market data
   needs no credential, so nothing had to be smuggled onto the runner.
2. The runner reads **status codes of the resource**, not of a proxy - the impossible control
   separates from the positive control, which is the only way to know that.
3. **A scheduled job can measure an external venue and commit the result to the repository with no
   human present.** That is the thing the project has lacked in every session so far, where every
   write needed a credential pasted into a fresh VM by hand.

### The limit, stated so it is not over-claimed

**This establishes reachability and the write path at census volume - seven requests - and nothing
about bulk collection.** The rate-limit amendment above records that the rejection curve is a
property of *(endpoint, **source**, recent history)*: the same configuration read 0%, 32.5% and
44.1% on repeat, and a second machine took 3,200 requests at 64 threads with zero rejections where
the first began rejecting after ~600.

A **GitHub-hosted runner IP is shared with every other user of the platform**, so its recent history
is not yours and is not observable. A collector moved onto CI would be running from a source whose
bucket state is set by strangers. **Do not assume the ~6 req/s clean band measured from a Kernel VM
transfers to a shared runner.** It has to be re-measured there, counterbalanced, before any bulk
pull runs on Actions.

**Census-scale scheduled measurement: established. Bulk collection from CI: unmeasured.**

### Incidental, from run #1's own data

The boundary is still benign. `market_settled_ts` advanced to `2026-06-18` and the live floor to
`2026-06-11T04:59`, a gap of **~7 days** - unchanged from 2026-08-17 and up from 6 on 2026-08-14.
Both edges slide, the gap is stable or widening, and no reachability hole opens. **P9 remains closed.**

## Amendment, 2026-08-18 - A CURSOR IS PRODUCED BY A LAYER AND MAY NOT ADVANCE THE RESOURCE

**The rule this file already carries is not enough.** "Only `cursor_exhausted` or `empty_page` may
be read as a complete answer" assumes a cursor that eventually does one or the other. Polymarket's
`gamma-api.polymarket.com/markets/keyset` does neither: it returns a fresh 216-character
`next_cursor` on every call and **ignores it**. 410,196 rows were pulled from it. They decode to
**100 distinct `conditionId`** - one page, repeated 4,102 times, at HTTP 200 throughout.

Ten probes on the same page-one cursor, each HTTP 200, none advancing: parameter names `cursor`,
`next_cursor`, `after`, `page_cursor`, `start_cursor`, each raw and percent-encoded. Identical first
five conditionIds every time.

> **The rule, stated to generalise: assert that the stream ADVANCES. Count distinct keys per page and
> stop when a page adds none. A legitimate stop reason is necessary and is not sufficient.** This is
> the fifth time this project has been misled by an artefact of a layer rather than the resource, and
> the first where the artefact was a *pagination token* rather than a status code.

An earlier B1 pass reported "116,900 Polymarket open markets". That number was 100 markets counted
1,169 times. It was never committed as a finding; it is recorded here because the failure mode is
reusable and the near-miss is the point.

### Polymarket gamma: what is honoured and what is silently ignored

Each verified by an impossible value beside a permissive one, never by a single call.

| parameter | honoured | how it was established |
|---|---|---|
| `closed=` | yes | `closed=true` returns `closed:true` rows |
| `volume_num_min` | yes | `1e18` -> **0 rows**; `0` -> rows |
| `liquidity_num_min` | yes | `1e18` -> **0 rows**; `50000` -> rows |
| `end_date_min` | yes | year 3000 -> **0 rows** |
| `order=` / `ascending=` | yes | desc -> $2.92M top liquidity, asc -> $0, impossible field -> **422** |
| `active=` | **NO - silently ignored** | `active=false` returns `active:true` rows |
| `archived=` | **NO - silently ignored** | `archived=true` returns `archived:false` rows |
| `limit=` above 100 | **NO - silently truncated** | `limit=500` and `limit=1000` both return exactly 100 |
| `offset` above ~2,000 | **422** | body: `offset too large, use /markets/keyset for deeper pagination` - which points at the endpoint that does not work |

### The working route

**`clob.polymarket.com/markets`** - a different host and a different layer. 1,000 rows a page, a
cursor that genuinely advances (`aWQ6...` = base64 `id:<n>`), and the fields `active`, `closed`,
`accepting_orders`, `enable_order_book`, `description`, `end_date_iso`, `tags`, `tokens`. It carries
**no volume or liquidity**, so enumeration and notional have to come from different places on this
venue.

Two cautions measured on it: a **malformed cursor returns HTTP 200 with data** rather than an error,
so a corrupted token silently restarts the stream; and the stream has **gaps** - three consecutive
full pages of nothing new at 279,803 distinct, then new markets resumed. A stall guard set at 2 pages
fired falsely. Set it at tens of pages, and treat any enumerated total as a floor.

## Amendment, 2026-08-18 - TWO FIELDS THAT EXIST IN THE SCHEMA AND ARE NEVER POPULATED

- **Kalshi `liquidity_dollars` reads `"0.0000"` on all 84,290 open markets.** Cross-checked on a
  second endpoint (`/markets/{ticker}`) on the busiest market on the exchange - 23.3M contracts of
  open interest, `yes_ask_size_fp: 42535.60`, and still `liquidity_dollars: "0.0000"`. There is a
  book; the field does not report it. **Do not use it as a notional measure.** Use open interest
  times `notional_value_dollars`, which was read from the API and is exactly `1.0000`.
- **Polymarket `resolutionSource` appeared empty on every row** the keyset stream returned. It is in
  fact populated on 28% of money-bearing markets. The zero was a second-order artefact of the inert
  cursor above - the 100 repeated markets all happen to have it blank. **An artefact in a pager
  propagates into every field statistic computed downstream of it.**

## Amendment, 2026-08-18 - `orderbook_fp`, not `orderbook`. This does NOT disturb the depth ceiling.

`GET /markets/{ticker}/orderbook?depth=N` returns HTTP 200 with the payload under the key
**`orderbook_fp`**. Reading `orderbook` yields `{}` - which reads exactly like an authentication
gate, and was briefly recorded as one before the raw body was printed. The live public book is fully
populated: five levels a side with sizes on the market checked, unauthenticated.

**This is a live-book fact and the depth-ceiling amendment above is a historical-book claim.** That
amendment says the exchange does not retain the book and no public archive exists outside
`2026-05-14` -> `2026-06-11T03`; nothing here contradicts it, and H65's "unreportable with the data
that exists" stands unchanged. Recorded together because the two are close enough to be confused.

## Amendment, 2026-08-18 - A CONTROL THAT CANNOT SEPARATE, ON A THIRD OF ALL HOSTS

Probing 758 external resolution-source URLs across 348 hosts with an impossible path on the same host
as the control:

| | Kalshi | Polymarket |
|---|---|---|
| hosts probed | 257 | 91 |
| impossible path returns **404/410** - the pair separates | 169 (66%) | 57 (63%) |
| impossible path returns **200/202/206** - the host answers any path alike | 88 | 34 |

**On a third of hosts a 2xx is a fact about the router, not about the resource.** Single-page apps
and catch-all routers make the standard control void, exactly as a 400 that means "forbidden" and a
400 that means "absent" were indistinguishable in packet 5's T1.4. Any measurement on those hosts
needs a different control - content hashing against a known-absent path is the obvious candidate and
is untested.

## Amendment, 2026-08-18 - KALSHI'S TWO SETTLEMENT-SOURCE ENDPOINTS DISAGREE

`settlement_sources` - a structured `[{name,url}]` array - is carried on the **event** object and
again on the **series** object. They are not the same list.

| | events | markets |
|---|---:|---:|
| identical | 8,247 (80.8%) | 71,774 |
| **different** | **1,966 (19.2%)** | **12,457 (14.8%)** |

The disagreement changes the implied source class on thousands of markets and moves B1's in-scope
count by **10.6%** (22,966 from the event endpoint, 20,526 from the series endpoint, 19,500 agreeing).
Nothing in either response says which is authoritative. **Take the intersection and say so.**
