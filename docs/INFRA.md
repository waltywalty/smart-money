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
