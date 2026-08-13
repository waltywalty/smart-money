# Smart Money Detector

Quantitative research on prediction markets (Kalshi, Polymarket). It began as a "follow the smart
money" signal detector and became something more useful: **a record of every idea that did not work,
and the measurement that killed it.**

The headline result is a cost, not an edge.

> ### The hurdle is horizon-dependent
>
> **−3.81¢ per contract at a 24-hour lead** [−4.91, −2.81], falling to **−1.94¢ at a 10-minute
> lead** [−2.02, −1.88], measured on liquid sports with real per-series fee multipliers (H60,
> n=336–412 events per horizon). The earlier −4.39¢ [−5.20, −3.67] figure is the 24-hour,
> weather-and-macro-ladder case and **must not be quoted as universal.** It is never positive at
> any horizon tested.
>
> That is what crossing the spread costs. Every idea in this repo clears it or it isn't an idea.

**No live capital has ever been deployed. No real order has ever been placed.**

---

## The registry is the point

`registry/hypotheses.json` holds **53 entries — 45 killed, 4 corrected, 1 confirmed, 1 open, 2
could-not-establish.** It exists because a killed idea has a habit of coming back wearing a new name,
and because a project that only records its wins learns nothing.

Every entry carries a `revive_if` field: the specific evidence that would reopen it. A verdict
without one is an opinion.

Numbering has gaps at H22–H27, H32 and H45. Those were lost in a container rollback and are recorded
as missing rather than reconstructed from memory.

### The kills collapse into a short list of reasons

- **Taker on public info** — edge = spread + fee, and the public feed runs 78–258s behind a book that
  moves at 180s.
- **Maker capturing spread** — the spread *is* the compensation for adverse selection, measured at
  2.7× the spread against.
- **Maker collecting a subsidy** — the reward is tied quadratically to exposure.
- **Internal-consistency arb** — the two books are one book (17 of 26 markets have YES and NO as
  exact mirrors), ladders are monotone, partitions sum to $1.
- **Cross-venue** — the gap is smaller than the round trip, and per H46 it was never even a hedge:
  settlement criteria diverge on 15 of 16 cross-listed pairs.
- **Model vs market** — four separate free professional benchmarks (Cleveland Fed nowcast, Fed-funds
  derivation, NBS MOS, GDPNow) each had error bars *wider* than the market's implied distribution.
- **Long-dated tails** — collateral drag beats mispricing; a 6000× mispricing returns 0.91%/yr.
- **Short-dated tails** — where the tick exceeds fair value, the book is empty.
- **Spread and flow are inversely coupled** — 40 of 51 markets quote a spread wider than their own
  move, and the median 24h volume of those 40 is **zero**.
- **Calibration** — prices are calibrated on both venues at every bucket with enough events to test.

### The one confirmed result

**H60.** The cost of crossing is not a constant but a **function of horizon**, falling from −3.81¢ at
a 24-hour lead to −1.94¢ at ten minutes as the spread collapses from 5.01¢ to ~1.3¢. The half-spread
saving (1.82¢) and the P&L improvement (1.87¢) match, so the gain passes through to the taker in full
rather than being absorbed by adverse selection — that pass-through was the pre-registered check and
is why the finding stands.

It is the project's first positive-direction result, and it is still a cost, not an edge.

### The effect that was real, replicated, and worthless anyway

**H61.** Buying favourites at a 10-minute lead returned **+4.96¢ in-sample and +4.99¢ on 644 genuinely
held-out events** — matching to 0.03¢, leave-one-series-out all positive, the largest single event a
*loser*, 98% coverage. It passed every statistical check in this repo.

Then the entry ask was measured one, two and three minutes later: **+1.64¢, +3.12¢, +5.00¢ against the
buyer.** Three minutes of delay consumes the whole edge, and the real entry is already a minute late by
construction. Capturing it needs sub-60-second detect-to-fill against a 5-minute cron — three orders of
magnitude too slow. Killed on execution, not on statistics.

**A perfect replication is not evidence of tradability.** Statistical validity and obtainability are
separate gates. That distinction is now the sharpest lesson in the registry.

### H50 has been downgraded to UNVERIFIED

Formerly billed here as "the one real effect" — lag-1 autocorrelation **−0.2472 [−0.3471, −0.1416]**.
It was measured entirely through the fetch layer now known to fabricate, and it **failed to replicate**
on an independent instrument (H59: −0.0038, CI spanning zero, on a point-in-time recorder well-powered
to detect an effect six interval-widths smaller). Not retracted — downgraded, and **not to be cited
until re-measured on the clean path.** That is the highest-value open measurement in the project.

## Method

`skills/empirical-claims/SKILL.md` is the procedure, extracted because it kept earning its keep.

**The data layer fabricates.** A fetch that passes through a summarising model invents values.
Observed here: a quote returned as `0.29/0.30` where the order book said `0.05/0.06`; `limit=100`
silently returning 34 rows; an empty book reported as `0.0000/1.0000`, injecting a phantom 50¢
midpoint; and the *same wrong answer* reproduced across two independent fetches. Cross-check against
a **different endpoint**, never a second call to the same one.

**Eight false positives were caught before shipping.** Each is now a rule:

1. `+$284` market-making profit — lookahead.
2. `r = +0.885` on n=4 — became `−0.016` at n=11; the leave-one-out range was `[−1, +1]` throughout.
3. A 0.75–0.85 calibration bucket — one payrolls print wearing twelve hats. *Count the independent unit.*
4. `+1.217¢` post-fill drift — an artifact; touch-fills marked at the mid restate the autocorrelation.
5. `+0.68¢` on 15 markets that all settled NO — reachable *because* they were far OTM. *Selection.*
6. `+7.23¢` on favourites — collapsed to `+0.82¢` once ladders with missing tail candles were excluded.
7. A `−29.7pp` calibration gap at high asks (H56) — 62 of its 89 markets were one series, `KXRAIN`.
8. `+4.99¢` on 644 held-out events (H61), replicating in-sample to 0.03¢ — and the ask moved
   `+1.64¢`/`+3.12¢`/`+5.00¢` against the buyer at 1/2/3 minutes after entry. *Measure the price you
   could have transacted at, not the price you observed.*

Four kills were also **right for the wrong reason** (H15, H16, H46, and H49's own premise), and the
registry says so rather than quietly keeping the correct answer.

## Layout

| Path | What it is |
|---|---|
| `worker.js` | Cloudflare Worker — recorder + paper-trading engine. **See the warning below.** |
| `index.html` | Dashboard, single file, no build step |
| `registry/hypotheses.json` | **The main artifact** |
| `registry/h*-preregistration.md` | Pre-registrations written *before* looking at outcomes |
| `skills/empirical-claims/SKILL.md` | The anti-fabrication + verification protocol |
| `tests/wtest*.js` | 16 regression tests |
| `analysis/h50/` | Lag-1 autocorrelation study |
| `analysis/h53/` | Far-OTM rung study |
| `analysis/mm/` | Market-making / adverse-selection study |
| `analysis/h56/` | The hurdle re-measurement — result, 346 events, collector, analysis |

## ⚠️ worker.js is v11.4 — production runs v11.5

`worker.js` in this repo is **v11.4**. The deployed worker is **v11.5**, and a **v12.3** existed but
was lost in a container rollback on 2026-08-10 and is not recoverable from any sandbox.

**Do not deploy this file without checking Cloudflare's version history first.** It is committed as
history, not as the current build.

Operational notes:

- Subrequest ceiling is **50 per invocation**; worst measured cycle is 22. Exceeding it silently
  kills scheduled runs, and that failure once looked exactly like a broken cron trigger.
- KV writes ~288/day against a ~1k/day free tier.
- The worker calls **Polymarket only** — `clob`, `gamma-api`, `data-api`, plus `ntfy.sh`. No Kalshi.

```
node tests/wtest14.js    # the broadest regression test
```

## API notes worth keeping

**Kalshi migrated its schema.** Fields are now `yes_bid_dollars` / `yes_ask_dollars` / `volume_fp` /
`volume_24h_fp` / `open_interest_fp` / `liquidity_dollars`; the order book is `orderbook_fp` with
`yes_dollars` / `no_dollars` as `[price, size]` string pairs. Old names return undefined.
`liquidity_dollars` reads `0.0000` even on a market with 236k volume and appears dead.
**Candlesticks are unchanged** — `yes_ask.close_dollars` still works, and `end_period_ts` is still
the *inclusive end* of the bucket.

**Outcomes must come from `?status=settled`.** Both `/events?with_nested_markets=true` and the
single-market endpoint serve stale `active`/blank results for long-settled markets.

**Kalshi rate-limits and returns a real 429.** Sustainable pacing is 3 threads at 0.55s per request
(~13% rejection, all retried); 4 threads at 0.4s bounces 42%.

---

*Numbers here are copied from `registry/hypotheses.json`. Where they disagree, the registry is correct.*
