# Packet 6 - close-out

Programme: latency (new), Kalshi (restructured). Worked 2026-08-18 and 2026-08-20.
Nothing was traded. Nothing was deployed. No GO was sought or given.

## The position

**B3 is sealed and unstarted. The family is unruled. Not one event has been detected.**

Everything in this packet characterises the *instrument*: what the universe is, how it
stratifies, which sources sit still, what load they tolerate, what resolution the
measurement can reach. None of it is evidence about whether the edge exists. The question
B3 asks - when a source publishes, how long before the price moves - has not been asked of
a single publication.

That is the correct state at the end of a packet, and it should be read as a position
rather than as progress toward one. A packet that had produced a latency number by now
would have produced it from an instrument nobody had checked.

## The three the packet asked for

**1. Did the census still commit after the restructure?** Yes, and then it did it
unattended, which is the stronger claim. Run #2 dispatched (`69cca04`), then the scheduled
run fired on its own and committed `e94dc5c` - author and committer `github-actions[bot]`,
verified through the commits API rather than the log file it wrote, impossible-sha control
**422**. Actions cron drifted **36 minutes** late, which is normal and is now written into
`docs/INFRA.md` as a constraint: anything scheduled that way must be idempotent and must
never stamp rows with its nominal cron time.

**2. B1's universe count and notional.**

| | markets | share | open interest |
|---|---:|---:|---:|
| Kalshi open, non-MVE | 84,231 | 100% | $752,020,238 |
| in scope by the event endpoint, reachable, control separates | 16,843 | 20.0% | $99,061,869 |
| **and the series endpoint agrees** | **14,540** | **17.3%** | **$91,407,507** |
| Polymarket money-bearing, same rule | 887 | 20.8% of 4,265 | - |

24h volume: Kalshi **$44.3M**, Polymarket **$31.4M** - the same order of magnitude, reached
with 84,231 open markets against a few thousand.

**3. B2's latency table.** Only half of it exists, and the missing half is the point.

| measured | value |
|---|---|
| single-fetch wall time, n=671 | p50 **0.43s**, p90 1.23s, p99 4.12s; 1 url of 671 over 10s |
| sweep of the 125-url population | ~15s estimated at concurrency 8 |
| **implied median detection delay** | **8.0s at concurrency 8** - meets a 10s bar |
| **publication -> first price move** | **NOT MEASURED. Zero events.** |

The polling side of the kill criterion is settled. The market side has no data at all.
Quoting the first as though it were the second is the specific error the pre-registration's
disclosure rule exists to prevent.

## MEASURED

Each of these was read from a resource, with a control that separated, and cross-checked
where a second route existed.

- **The Kalshi open universe.** 84,231 non-MVE markets paged to `cursor_exhausted` over 824
  pages; 99.93% joined to an open event. $752,020,238 of open interest at
  `notional_value_dollars` = 1.0000, read from the API rather than assumed.
- **Settlement sources are structured.** `settlement_sources` `[{name,url}]` on both the
  event and series objects. 10,939 open events, 3,464 series.
- **The two source endpoints disagree on 19.2% of events** (12,457 markets), moving the
  in-scope count by **10.6%**. Nothing marks either authoritative; B1 reports the
  intersection.
- **The in-scope population collapses to 758 distinct urls**, 274 under the strict reading.
- **Reachability with a separating control**: 306 of 547 Kalshi urls, 117 of 211 Polymarket.
  **On a third of hosts the status control is void** - 88 of 257 and 34 of 91 answer an
  impossible path with 2xx.
- **The content control recovers 50 of those 60 hosts (83%)**, agrees with the status
  control 40/40 where that works, and **is not deterministic** - 4 hosts of 60 changed
  verdict in 48 hours.
- **The source layer is HTML.** 22,116 markets behind `text/html`, 55 behind PDF, 3 behind
  `text/plain`.
- **robots.txt across 201 hosts**: 96.8% of in-scope markets behind hosts declaring no
  crawl delay; 14 hosts disallow an in-scope path (204 markets).
- **The false-positive floor.** Four rounds over an hour, 425 targets, nothing happening:
  56.9% of pages did not change, 28.9% changed at every interval. Paired on the same host,
  the lift was **-4.7, +3.5, -1.2 pp** at 5m/15m/60m with 93-96% verdict agreement.
- **Calendared-release pages are perfectly still.** 0 of 41 changed in an hour, once
  rolling-update sources were separated out.
- **A 15-minute window overstates stability by 26.3% of urls and 0.4% of the money.**
- **Sustained load.** 29.8 min active, 1 req/13.3s on six government hosts and 1 req/2.1s on
  one commercial host: zero 429s, zero `Retry-After`, drift -10.6% to +8.1%.
- **`raw.githubusercontent.com` is intermittently stale** and ignores cache-busting and
  `Cache-Control: no-cache`. `git/blobs/{sha}` is correct.

## INFERRED

Supported by measurement, resting on a step that is reasoning rather than reading.

- **Naive change detection carries no signal.** Three horizons agreeing that the lift
  straddles zero is a null, and it is inferred to generalise beyond the 85 host-paired urls
  it was measured on.
- **The population is two problems, not one.** Publication sources have an instant; live
  quotes do not. The split is inferred from churn behaviour plus what the pages are.
- **10s median detection is reachable from concurrency 8.** Arithmetic on measured fetch
  times, with half the population's times mean-imputed.
- **The unscheduled stratum is uncontested.** The competitive argument is Walton's and it is
  not measured. What *was* measured is that its dollar dominance is one page.
- **The EOP page's tight book is size, not competition.** r = -0.94 within EOP and a matched
  cell of **n=4**. The evidence for contestedness evaporated when the confounder was
  controlled; that is not the same as contestedness being ruled out.

## ASSUMED

Not established. Load-bearing anyway.

- **That a normalised-hash change is a proxy for publication.** Never tested against a known
  publication with a known instant. B3 §7.1 tests it before anything else, as a stop.
- **That the venue's price timestamps and ours are on the same clock.** Any sub-second
  interval is meaningless if they are not, and nothing has checked.
- **That the structural class-1 rule identifies sources that carry the answer.**
  `nass.org/can-I-vote` proves it does not always - 3,954 markets, a voter-information
  portal, correctly classified and useless. Nothing has parsed a single page.
- **That B3's population will still resolve when events arrive.** Now dated rather than
  assumed - the B4 probe records it, starting at 125 of 125.
- **That an hour on one weekday morning from one egress IP generalises.** This project's own
  finding is that the rejection curve is a property of *(endpoint, source, recent history)*.
- **That 50 events will arrive.** Cabinet departures and election certifications are rare.
  The six-month time box exists because they may not.

## Wrong before right

Eight things this packet believed and then stopped believing. Listed because the pattern is
more useful than any of them individually: **every one was caught by two things disagreeing,
and none announced itself.**

1. **"116,900 open Polymarket markets."** The gamma `/markets/keyset` cursor is inert. 410,196
   rows decode to **100 distinct markets** - one page repeated 4,102 times, HTTP 200
   throughout. The standing rule ("only `cursor_exhausted` counts") cannot catch this, because
   an inert cursor never exhausts. New rule: **assert the stream advances.**
2. **"Polymarket `resolutionSource` is always empty."** It is populated on 28% of
   money-bearing markets. The zero was a second-order artefact of the inert cursor.
3. **The first source classifier**, which demoted on the *domain*. Wrong in both directions -
   `google.com/finance/quote/NDX` demoted, `nass.org/can-I-vote` promoted. The seeded audit
   sample killed it in one pass.
4. **"Change detection carries signal (+9.6 pp)."** Measured against a control set of 33
   app-shell hosts and a target set of 369 pages of every kind. **Paired on the same host the
   lift went to -4.7 pp.** The comparison was measuring hosts, not pages.
5. **"Scheduled pages decay at 42.7%."** 32 of the 35 decayers were `wunderground.com` history
   pages - rolling observation feeds, not calendared releases. Separated out, calendared decay
   is **0 of 41**.
6. **"The write was verified."** Through `raw.githubusercontent.com`, which served a stale
   pre-edit copy. Caught only because a **second sample of the same instrument disagreed** -
   a check that proves nothing when it agrees.
7. **"The White House page is contested."** Mine, argued confidently, refuted by the only
   unconfounded test available.
8. **"`weather.com/kalshi` is unreachable."** It answers 206 in 0.3s. `text=True` on a gzip
   body raised `UnicodeDecodeError` and the `except` recorded it as a network failure. It had
   silently excluded **seven PDF and binary sources** - systematically the machine-readable
   ones - from every B2 measurement.

Three of the eight (1, 6, 8) were instrument faults that produce *clean-looking* results.
Those are the expensive ones: a wrong number announces itself eventually, a plausible one
does not.

## Parking lot, ranked by what it would cost to be wrong

1. **P19 - class 1 is a claim about the venue's stated source, not about the answer being at
   that url.** Nothing has parsed a page. If the rule is systematically wrong, the whole
   population is wrong. **B2's first task, and it is cheap: 485 urls is a list.**
2. **P20 - which Kalshi source endpoint is authoritative.** 10.6% of the count. Resolvable
   only by a venue statement or a settled market where the two lists imply different
   outcomes - a real experiment nobody has run.
3. **P21 - 10 hosts (712 markets, $536,625) where no control separates**, including
   `binance.com`, the largest single Polymarket source. Needs a headless render, which changes
   the access level and needs its own control.
4. **P18 - the credential cannot write `.github/workflows/` or dispatch.** B4's probe is
   staged and inert because of it. Every scheduled thing this programme wants needs Walton's
   hand once.
5. **P22 - the Polymarket count is a floor** and the enumerating stream has gaps.
6. **P16 - the two-hour trade hole** at `2026-06-11T07`-`T08`. Unchanged.
7. **P17 - T1.4's first-pass statement.** Unchanged, and the pattern recurred twice more this
   packet.
8. **T2.2 / T2.3** - the `fee_multiplier` anachronism and `FEE-MODEL-IMPLICATIONS.md`. Not
   started, two packets running.

## Deferred from this packet

- The `docs/INFRA.md` and `docs/STATE.md` splits (Kalshi specifics -> `programmes/kalshi/`),
  and `lib/kalshi.py` / `lib/polymarket.py`. Listed in A1's target structure, never created.
- `registry/retention/` still sits at the repo root. P18 is why.
- The UNKNOWN stratum's 43 urls have no rule. 2.3% of the money, 25% of the urls.

## What happens next, in order

1. **Install the B4 workflow.** One manual move of `programmes/latency/b4/population-probe.yml`
   into `.github/workflows/`. Until then the decay log has one row and no cadence.
2. **Run B3 §7's abandonment conditions** - all four, before arming anything. Any failure is a
   stop, not a caveat.
3. **Then, and only then, arm the population and wait.** The next CPI or FOMC release is the
   natural first test, because the instant is known.
