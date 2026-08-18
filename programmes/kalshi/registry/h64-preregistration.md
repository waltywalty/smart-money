# H64 — near-certainties at a ten-minute lead. Pre-registration.

**Sealed 2026-08-14, before any settlement outcome was fetched.**

Supersedes `h64-preregistration-STUB.md`, which was written when the archive was believed to be
hourly snapshots. It is not — it is a tick-level feed, and that changed the design. The stub said
the finest testable lead was T−1h and that a ten-minute test was unreachable. Both were wrong.

## Disclosure of what has already been seen

Honesty about the seal is worth more than the seal. Before writing this I fetched Kalshi market
**listings** (`?status=settled`) to count how many events settle inside the usable window, and I
opened one archive file to read its schema. Those responses carry a `result` field. **No outcome
was extracted, printed, aggregated or reasoned about** — only `ticker`, `event_ticker` and
`close_time` were used, to produce the count of 233 events. I have not seen a single settlement.
The band-population figures, the hit rate and the P&L are all unknown to me as I write this.

## Why this is not H55 again

H55 asked whether buying at ask 0.93–0.98 at a **24-hour** lead pays, because Kalshi's fee
`0.07·p·(1−p)` is minimised at the extremes. It returned *could not establish*, and for a
structural reason rather than a statistical one: of 1,523 non-KXRAIN rungs quoted at T−24h,
**exactly one** sat in the band. The fee arithmetic was right and irrelevant. Contracts are not
priced at 93–98¢ a day out; by the time one is that certain it is near settlement.

H55's own `revive_if` names the successor: *re-tested at a shorter lead where the band is
populated, a different hypothesis needing its own pre-registration, with H7/H9's capital-lockup
arithmetic applied.* This is that hypothesis. Different horizon, different universe, different
cost structure.

## The claim

**H64: at a ten-minute lead the 93–98¢ band is populated, and buying it at the ask returns less
than zero after fees — the same hurdle H56 measured at T−24h and H60 measured at T−10m, not an
exception to it.**

Stated in the direction that costs most to be wrong about. H60 established the hurdle *falls* with
horizon: −3.81¢ at 24h, −1.94¢ at 10m. If it keeps falling and crosses zero in the extreme-price
band, that is a real finding. The prior from 45 kills is that it does not.

## Instrument

- **Quotes.** `archive.pmxt.dev`, Kalshi orderbook, CC BY 4.0. Verified coverage 2026-05-14 →
  2026-06-11T03:00Z, hourly-sharded Parquet. Contents are **tick-level**: one measured hour held
  14,072,547 rows across 390,681 markets — 13,548,617 `orderbook_delta` and 523,930
  `orderbook_snapshot`, timestamped to the microsecond. Book state at an arbitrary instant is
  reconstructed by taking the last `orderbook_snapshot` at or before that instant and replaying
  every `orderbook_delta` forward to it.
- Fetch with a ranged `GET` and an explicit User-Agent. `HEAD` on that host returns 200 for keys
  that do not exist, and a bare urllib UA is blocked. **Every collection run includes an
  impossible key as a control** and aborts if the control returns anything but 404.
- **Outcomes.** Kalshi `?status=settled` only. Never `/events?with_nested_markets=true`, never the
  single-market endpoint — both serve stale results for settled markets (H39).
- **Never** the archive's last pre-expiry quote as an outcome proxy. That is H39's grave.

## The window, and why this expires

Quotes run to 2026-06-11. Kalshi's settled-outcome retention reaches back only to ~2026-06-07 and
advances about a day per day. The usable intersection is **2026-06-07 → 2026-06-11**, and it
empties on or about **2026-08-17**. The archive stopped updating on 2026-06-11 and must not be
assumed to resume. If the window closes before this runs, H64 is unrunnable from public data and
becomes an argument for continuous self-collection instead of an experiment.

## Universe

Every Kalshi market whose `close_time` falls in 2026-06-07 → 2026-06-11 and which is still
reachable via `?status=settled`, **excluding `KXMVE*`** a priori. Series are enumerated from
`/events?status=settled`, which is not flooded, then each series pulled from `/markets`.

Markets with no `orderbook_snapshot` in the archive at or before their entry instant are
**excluded before any statistic is computed**, and the excluded count is reported. A market the
instrument cannot see is not a null.

## Entry rule, fixed now

1. For each market, the entry instant is **`close_time` − 10 minutes**.
2. Reconstruct the book at that instant. Take the **best yes ask** and the size resting at it.
3. Qualify if best yes ask ∈ **[0.93, 0.98]** inclusive.
4. Buy one contract at that ask. Hold to settlement.
5. Net cents = `100·1{settles YES} − 100·ask − fee`, with
   `fee = ceil(M · 0.07 · p · (1−p) · 100)` in cents, `p` = ask, and **`M` read from the series'
   `fee_multiplier`** — never assumed 1.0. It is 1 on 12,907 series, 0.5 on 19, 0 on 14.

## Unit of observation

**THE EVENT.** Ladder rungs resolve together, so an event contributes exactly one observation: the
mean net cents across its qualifying rungs. This rule has killed more false positives in this repo
than everything else combined, and the 93–98¢ band is precisely where one event wears many hats.

## Bar

- **≥ 150 independent events** with at least one qualifying rung. Below that: report **could not
  establish** and stop. Do not widen the band, do not extend the window, do not lower the bar.
- The result must survive **leave-one-series-out**. Five consecutive calendar days will be
  concentrated; if one series carries it, there is no finding. This is false positive #7's shape.
- **Depth reported beside every price.** A price without size is not a price, and this project has
  paid for that twice.

## Reported alongside, always

- **Series composition of every bucket**, unprompted.
- **Leave-one-market-out and leave-one-series-out**, as ranges, not points.
- **Obtainability, separately from statistical validity.** Re-price the same entry at T−5m and
  T−1m and report what could have been transacted at. H61 replicated out-of-sample to 0.03¢ and
  was worth nothing.
- **Fill feasibility**: what fraction of qualifying rungs had any resting size at the ask, and the
  distribution of that size. An untakeable quote is not an entry.
- **H7/H9 capital-lockup arithmetic**, as `revive_if` requires: a contract bought at 97¢ locks 97¢
  to earn 3¢. Report return per unit of capital, not cents per contract alone. Do **not** annualise
  a ten-minute hold — that number is meaningless at any size and this repo has been misled by it
  before.
- **Band population as a function of lead** (T−24h, T−1h, T−10m, T−1m), descriptive only. This is
  the direct successor to H55's structural finding and is not a second hypothesis test.

## What each outcome means, written before looking

- **Negative and consistent with H56/H60** — expected. The hurdle holds at the extremes, H55's
  line closes for good, and fee minimisation is finished at every horizon tested.
- **Negative but materially smaller than −1.94¢** — the hurdle keeps falling into the extreme band.
  Interesting, still not a trade, and it becomes a claim about horizon rather than about price.
- **Positive** — extraordinary. Suspect the five-day window and the series mix before the market.
  Do not report it without leave-one-series-out **and** a split-half replication across the window's
  first and second halves, both pre-committed here.
- **Fewer than 150 qualifying events, or the band still empty at T−10m** — *could not establish*,
  and H55's structural finding extends to short leads. That is a real answer and gets recorded as
  one, not as a null.

## What would make me abandon it before starting

- The overlap window has closed.
- Replayed books fail a sanity check: crossed or inverted books, or a reconstructed best ask that
  disagrees with the snapshot it was built from at the snapshot instant.
- Settlement cannot be joined to the archive's `market_ticker`.

## Scope, fixed now so it cannot be widened later

Kalshi only. Five days in June 2026. A ten-minute lead. Nothing here licenses a claim about the
exchange in general, about other venues, or about any other horizon.

---

# AMENDMENT 1 — 2026-08-14, before any settlement was examined

**The instrument changed. The hypothesis, the entry rule, the bar and the outcome meanings did
not.** This is recorded rather than quietly applied, and it is timestamped before any outcome has
been looked at — the disclosure in the original seal still holds in full.

## What happened

The sealed design used `archive.pmxt.dev` for quotes because Kalshi was believed unable to supply
short-lead quotes for settled markets. **That belief is false.** Kalshi serves **1-minute
candlesticks** for settled markets, carrying `yes_ask.close_dollars` and `yes_bid.close_dollars`
against an inclusive `end_period_ts` — checked directly on a settled market from the window:
`period_interval=1` returned candles, `period_interval=60` returned candles, both with the ask.

The archive was never necessary. Three consequences, all of which make the study better:

1. **No book reconstruction.** The ask at T−10m is read directly instead of replayed from a
   snapshot plus deltas. Two out-of-memory failures and a stalled VM came from that replay; none of
   that work was needed.
2. **The deadline is gone.** The 2026-08-17 expiry was the archive's frozen end date sliding past
   Kalshi's retention floor. With candlesticks the binding constraint is Kalshi's own rolling
   settled-history window, which refreshes daily. This test no longer expires.
3. **The five-day window is no longer forced.** The original design's sharpest weakness — five
   consecutive calendar days is one regime, and series concentration would be severe — was imposed
   by the archive, not by the question.

## What changes

- **Primary quote instrument:** Kalshi 1-minute candlesticks, `yes_ask.close_dollars`, taking the
  candle whose `end_period_ts` is the latest at or before the entry instant.
- **Staleness is now a reported quantity and a filter.** A candle exists only where there was
  activity. The age of the candle used is recorded for every observation, and any observation whose
  candle is **more than 10 minutes stale** is excluded before any statistic is computed, with the
  excluded count reported. A stale ask is exactly the artifact H50 spent sixty hypotheses worrying
  about, and forward-filling one into an entry price would manufacture the result.
- **Cross-instrument check retained.** `archive.pmxt.dev` is kept as an independent check on a
  subsample of qualifying markets — the project's standing rule is that a finding is verified
  against a different endpoint, never a second call to the same one. Disagreement between the two
  instruments on the same market at the same instant is reported, not reconciled away.
- **Sample extension, pre-specified now.** The universe stays the sealed window first:
  2026-06-07 → 2026-06-11, 13,832 markets, 4,787 events. **If fewer than 150 events carry a
  qualifying rung, the window is extended forward one day at a time** through Kalshi's retention
  range until 150 is reached or the range is exhausted. Each extension is reported with its own
  event count so the reader can see whether the result moved as the sample grew.

## What does not change

The claim, the entry rule (T−10m, best yes ask in [0.93, 0.98], held to settlement), the fee
formula and its per-series multiplier, the event-level unit of observation, the 150-event bar,
the required leave-one-series-out survival, the obtainability and depth reporting, the H7/H9
capital-lockup arithmetic, and what each outcome is allowed to mean.

**Still unseen at the time of this amendment:** band population, hit rate, and every settlement.

---

# AMENDMENT 2 — 2026-08-14, before any settlement was examined

**Amendment 1 was wrong about the deadline. Retracted here, in full.**

Amendment 1 claimed that moving the quote instrument from `archive.pmxt.dev` to Kalshi's
1-minute candlesticks removed the 2026-08-17 expiry, because "the binding constraint is Kalshi's
own rolling settled-history window, which refreshes daily."

**It does not refresh in the direction I assumed, and candlesticks are not a separate retention
domain.** Measured today with a control:

```
KXHIGHNY-26JUN10-T82   candlesticks  200, 25 candles     (inside the window)
KXHIGHNY-26JUN08-T82   candlesticks  404 not_found
KXHIGHNY-26JUN03-T82   candlesticks  404 not_found
KXHIGHNY-25DEC15-T82   candlesticks  404 not_found
CONTROL, impossible ticker           404 not_found
```

Once a market passes the retention floor its candlesticks 404, and `/markets?event_ticker=` returns
zero rows, so the ticker cannot even be discovered to ask for candles. **The quote history expires
with the market listing.** Changing endpoint changed nothing about the deadline; I assumed a
different endpoint meant a different retention domain and did not test it until now.

One honest caveat on that table: the `-T82` strike may not have existed on the older events, so a
404 there is consistent with "wrong strike" as well as "expired". The load-bearing evidence is not
the strike probe — it is that `/markets?event_ticker=KXHIGHNY-26JUN03` returns **zero markets**, so
no valid ticker for that event can be obtained by any route.

**Consequence:** the deadline is real and is roughly where it was originally estimated. The archive
ends 2026-06-11; the exchange-wide floor is 2026-06-08 today and advancing about a day per day, so
the H64 window empties on or about **2026-08-17**. Markets closing 2026-06-08 are expiring now.

**What this changes in the procedure, and nothing else:** collection is re-ordered **oldest close
date first**, so the most endangered observations are captured before the least. The universe was
captured at 01:43 UTC today and already shows the erosion — 13 markets closing 06-07 against 2,644
closing 06-08, because 06-07 had almost entirely fallen off by the time it was pulled.

The claim, the entry rule, the fee formula, the unit of observation, the 150-event bar, the
leave-one-series-out requirement, the staleness filter and the outcome meanings are unchanged.

**Still unseen at the time of this amendment:** band population, hit rate, and every settlement.

---

# AMENDMENT 3 — 2026-08-14, before any settlement was examined

**There is no deadline. There never was one. Kalshi deletes nothing.**

Amendments 1 and 2 argued about *when* the H64 window expires. Both were arguing about a
premise that is false. Kalshi splits its data into a **live** set and a **historical** set at a
documented, queryable boundary, and serves the historical set from a parallel endpoint family.
Nothing is discarded; it moves.

```
GET /trade-api/v2/historical/cutoff
  {"market_settled_ts":"2026-06-14T00:00:00Z", ...}

GET /historical/markets?event_ticker=KXHIGHNY-26JUN03   200, 6 markets, results {yes:1, no:5}
GET /historical/markets?event_ticker=KXHIGHNY-25DEC15   200, 6 markets, results {yes:1, no:5}
GET /historical/markets?event_ticker=HIGHNY-21AUG06     200, 1 market,  result  yes    (2021)
GET /historical/markets/KXHIGHNY-26JUN03-T83/candlesticks   200, 9 candles
GET /series/KXHIGHNY/markets/KXHIGHNY-26JUN03-T83/candlesticks   404   <- the live path
```

Every one of those events returns **zero markets** from `/markets`. The same events return full
market rows, settlement results and minute candlesticks from `/historical/markets`. **Five years
of history, with outcomes, one endpoint away.**

Kalshi documents this plainly. `GET /historical/cutoff` — *"Returns the cutoff timestamps that
define the boundary between **live** and **historical** data."* And on the live candlesticks
endpoint: *"Candlesticks for markets that settled before the historical cutoff are only available
via `GET /historical/markets/{ticker}/candlesticks`."*

## What this changes

- **The 2026-08-17 deadline is void.** H64 can be run at any time, on any window, for as far back
  as Kalshi has existed.
- **The five-day window is no longer forced by anything.** The sealed universe stays the primary
  sample so the seal means something, but the pre-committed extension in Amendment 1 is now
  unbounded rather than capped by retention — and the "five consecutive days is one regime"
  weakness can be removed outright rather than caveated.
- **`archive.pmxt.dev` was never needed.** Kalshi has its own complete history, with settlement
  attached, which the archive does not.
- **Collection switches to `/historical/markets/{ticker}/candlesticks`** for any market whose
  settlement precedes the cutoff, and the live path for the rest. The cutoff is queryable, so
  which path applies is a lookup rather than a guess.

## How this was missed, which is the part worth keeping

The prior-art rule added to `CLAUDE.md` on 2026-08-13 says to check the current API surface
before building. I did not read Kalshi's documentation. I inferred a retention policy from
response shapes, built two collectors against that inference, exhausted a VM's memory twice,
declared a four-day deadline, and re-ordered a collection to race it. **One documentation page
would have prevented all of it**, and the packet that prompted this asked for exactly that check
in T5, which I ran last instead of first.

The measurement that produced the "67-day floor" was not wrong — the live set really does end
there, uniformly, and really does advance a day per day. The error was concluding *deletion* from
*absence in one endpoint*, without asking whether another endpoint held it.

**Still unseen at the time of this amendment:** band population, hit rate, and every settlement.
