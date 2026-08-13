# CLAUDE.md — read this first

Continuity file for the Smart Money Detector. Claude Code loads it automatically.
Other sessions should be pointed at it:

> Read `https://raw.githubusercontent.com/waltywalty/smart-money/main/CLAUDE.md`
> before doing anything on this project.

Everything below is measured, not assumed. Where this file and
`registry/hypotheses.json` disagree, **the registry wins**.

---

## 1. The hard constraint

**Never place a real trade. Deployment GO is Walton's alone**, in writing, per strategy.
No exception, no matter how good a result looks or how explicitly a tool offers to
execute. The `Trayd` connector in some sessions exposes `place_order`, `short_sell`
and Robinhood linking — do not touch them.

Cloudflare deploys are done by Walton manually. Claude delivers `worker.js`; Claude
does not deploy.

Standing grant from Walton, for everything else: *"for the hourly scans and other things
for this project, I give you automatically full autonomy and permission to do what you
want so you don't need to request it back to me for permission."* Research, collection
and analysis need no permission. Trading and deploying always do.

## 2. What this project is

Quantitative research across prediction markets (Kalshi, Polymarket). It began as a
"follow the smart money" detector. It is now a record of **every idea that did not work
and the measurement that killed it** — 53 hypotheses, 45 killed, 4 corrected, 1 confirmed,
1 open, 2 could-not-establish.

**The hurdle is horizon-dependent.** −3.81¢ per contract at a 24-hour lead
[−4.91, −2.81], falling to −1.94¢ at a 10-minute lead [−2.02, −1.88], measured on liquid
sports with real per-series fee multipliers (H60, n=336–412 events per horizon). The
earlier −4.39¢ [−5.20, −3.67] figure is the 24-hour, weather-and-macro-ladder case and
must not be quoted as universal. It is never positive at any horizon tested.

Every idea clears the hurdle *at the horizon it would be entered at*, never zero. The
spread collapses from 5.01¢ at 24h to ~1.3¢ from 4h onward, and the half-spread saving
passes through to the taker in full rather than being absorbed by adverse selection.

Decomposition at the 24-hour lead: ~1.5¢ half-spread + ~1.55¢ fee + ~1.34¢ of the ask
sitting above fair value. Only that last third is attackable in principle. Cheapest series
to cross in bottom out at −2.50¢; nothing across 21 series is positive.

**Fee multipliers vary by series — read them, never assume.** `KXMLBGAME` carries
`fee_multiplier: 0.5` where the code assumed 1.0 everywhere.

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

### Sandboxes are not storage

The Cowork sandbox **rolled back three times on 2026-08-10 and 2026-08-12**, each time
destroying analysis directories and reverting the registry. Kernel VMs expire on their
own timeout. **Nothing that matters may live only in a sandbox.** Deliver results to
Walton and get them into this repo as you go, not at the end.

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

## 4. Method — non-negotiable

`skills/empirical-claims/SKILL.md` is the full protocol. The short version:

**Unit of observation is the EVENT, not the market.** Rungs of one ladder resolve
together. This single rule has killed more false positives than everything else combined.

**Measure the price you could have transacted at, not the price you observed.**
Re-run any bar-based entry one bar later. H61 replicated out-of-sample to within 0.03¢
and was still worth nothing — three minutes of delay consumed the entire edge.

**A perfect replication is not evidence of tradability.** Statistical validity and
obtainability are separate gates and must be reported separately.

**Eight false positives were caught before shipping.** Each is now a check:

1. `+$284` market-making profit — lookahead.
2. `r = +0.885` on n=4 → `−0.016` at n=11; leave-one-out range was `[−1, +1]` throughout.
   **Report leave-one-out on every correlation.**
3. A calibration bucket that was one payrolls print in twelve hats. **Count independent units.**
4. `+1.217¢` post-fill drift — own artifact; touch-fills marked at the mid restate the
   autocorrelation.
5. `+0.68¢` on 15 markets that all settled NO — reachable *because* far OTM. **Selection
   is the first suspicion.**
6. `+7.23¢` on favourites → `+0.82¢` once ladders with missing tail candles were excluded.
   **A missing quote means nobody was trading, which happens when the outcome is obvious.**
7. A `−29.7pp` calibration gap at high asks — 62 of its 89 markets were one series.
   **Always report series composition behind any bucket.**
8. `+4.99¢` on 644 held-out events, replicating in-sample to 0.03¢ — the ask
   moved +1.64¢/+3.12¢/+5.00¢ against the buyer at 1/2/3 minutes after entry.

**Four kills were right for the wrong reason** (H15, H16, H46, and H49's own premise).
When a verdict rests on an unstated premise, check the premise even if the answer survives.

**Pre-register before looking.** Write the rule, the sample size that settles it, and what
each outcome means — then hash the file and only then fetch outcomes. Surviving
pre-registrations are in `registry/`.

Say **"could not establish"** when the instrument failed. That is a different claim from a
null, and recording an instrument failure as a finding is worse than either.

## 5. State of play

- **45 killed, 4 corrected, 1 confirmed, 1 open, 2 could-not-establish.** Numbering gaps at
  H22–H27, H32, H45 were lost to a rollback and are recorded as lost, not reconstructed.
- **The one confirmed result: H60.** The cost of crossing is horizon-dependent, roughly
  halving between a 24-hour and a 10-minute lead. The first positive-direction finding in
  the project — and it is a property of the exchange, not an edge.
- **H50 is UNVERIFIED, not retracted.** Its lag-1 autocorrelation −0.2472 [−0.3471, −0.1416]
  was measured entirely through the fetch layer now known to fabricate, and failed to
  replicate on an independent instrument (H59, demonstrably well-powered to detect an effect
  of that size). **Do not cite it anywhere until it is re-measured on the clean Kalshi path.**
  That re-measurement is the highest-value open work in the project.
- **H61 is the sharpest lesson**: a real, out-of-sample-replicated ~5¢ effect that is
  unobtainable, needing sub-60-second detect-to-fill against a 5-minute cron. Walton decided
  on 2026-08-13 not to invest in latency infrastructure; the line stays closed.
- **H58 is the only open lead** — H40's calibration curve re-run on the clean path.
  H55 and H57 are could-not-establish: their samples do not exist, which is a calendar
  problem rather than a compute one. Neither may be carried as a live lead.
- Fifteen mechanisms explain all the kills — see `state_of_play_*.the_mechanisms` in the
  registry. Read them before proposing anything; most new ideas are one of them renamed.

## 6. Two external doors, still unopened

- A **MADIS data application** (free form) — the one demonstrated timing edge needs it.
- An **SEC / Dune bulk pull**.

## 7. Housekeeping

Scheduled tasks exist including `Smart Money autonomous` (`3 */3 * * *`) and a weekly deep
dive. An hourly whale/insider scan and several stale one-shot reminders are also live and
could be cleaned up. A trigger for an H32 tornado-count re-check fires 2026-09-02T14:00Z.
