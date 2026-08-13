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

### Polymarket

`gamma-api.polymarket.com/markets|/events`, `clob.polymarket.com/book|/midpoint|/prices-history`,
`data-api.polymarket.com/trades`. `clobTokenIds[0]` is the YES token. Winner source is
`clob.polymarket.com/markets/{cid}` → `tokens[].winner`, **only** — a summariser once
defaulted every `winnerIndex` to 1 and nearly logged two fake reversals.

`worker.js` calls **Polymarket only** (clob ×8, gamma ×4, data-api ×4, plus ntfy.sh).
Zero Kalshi endpoints — Kalshi schema changes do not affect production.

### The worker

Live is **v11.5**. The file in this repo is **v11.4**. **v12.3 existed and was lost** to
a container rollback on 2026-08-10; it is not recoverable from any sandbox — only
Cloudflare's version history might still have it. Do not deploy the repo copy without
checking that first.

Subrequest ceiling 50 per invocation, worst measured cycle 22 — exceeding it silently
kills scheduled runs and once looked exactly like a broken cron trigger. KV writes ~288/day
against a ~1k/day free tier.
