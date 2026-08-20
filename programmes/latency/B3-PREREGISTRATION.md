# B3 - PRE-REGISTRATION. Alert-only detection of resolution-source publication.

Programme: latency. Packet 6, Phase B, step B3.
Sealed 2026-08-20 before any event was collected. **Amend, never edit.**

## 0. Constraints, restated because they govern everything below

- **No capital. No orders. No auto-fire. Alert-only.** This system observes and records.
  It does not act, and no code path in it may place a trade.
- **Deployment GO is Walton's alone, in writing.** Nothing here constitutes one.
- All measurement through raw HTTP from the Kernel VM. Never WebFetch. Ranged GET, explicit
  User-Agent, status codes never booleans, an impossible key on every probe **paired with a
  positive control**.
- A control must hold the measurement's access level and must be **matched on the
  confounder**. Where a status control is void, use the content control (P21).
- Verify a write through `git/blobs/{sha}`. `raw.githubusercontent.com` is CDN-cached,
  intermittently, and is unsuitable.
- A session ends with a commit.

## 1. The question

**When a resolution source publishes, how long is it before the market price moves?**

If the answer is "faster than anyone can act", the family closes in this form.

## 2. The population, fixed now

From B1 and B2, and not to be widened without an amendment:

| | urls | markets | open interest |
|---|---:|---:|---:|
| **B3-eligible** | **125** | **5,274** | **$70,790,897** |

Admission required all of: a single named settlement source with a specific URL path; the
same source named by **both** the Kalshi event and series endpoints (P20 intersection); the
URL reachable 2xx with a **separating control** on that host; and **measurably quiet** -
normalised content unchanged across four rounds spanning an hour with nothing happening.

Excluded, and why: 45 volatile URLs ($273,825, 0.4%); 38 URLs on hosts where no control
separates ($536,625); `nass.org/can-I-vote` (P19, 3,954 markets, a classified false
positive); every live-quote and rolling-update source, which have no publication instant.

### Strata, with separate bars. Pooling is prohibited.

| stratum | urls | markets | open interest |
|---|---:|---:|---:|
| SCHEDULED - calendared release, known instant | 47 | 2,571 | $18,344,614 |
| UNSCHEDULED - no announced instant | 39 | 2,439 | $50,825,419 |
| UNKNOWN - no stated rule matched; **no bar, reported only** | 39 | 264 | $1,620,864 |

**`whitehouse.gov/administration/executive-office-of-the-president/` is reported
separately inside UNSCHEDULED**, not as its own stratum. It carries $43,018,413 on 37
markets - 60.8% of eligible open interest on 0.7% of eligible markets. It is not
pre-registered as a stratum because 37 markets will not produce 50 events in any
reasonable window, and pre-registering a test that cannot run leaves the money unruled
while looking rigorous.

## 3. The governing sentence

> **The event-weighted median governs the kill decision. The notional-weighted figure is
> mandatory context and decides nothing.**

Stated in advance because two numbers without it invite picking the flattering one
afterwards.

## 4. The disclosure rule

> **No B3 figure may be quoted, in any document, summary, message or close-out, without its
> per-URL contribution table attached.** The table lists every URL that contributed events,
> its event count, and its share of the stratum's open interest.

This is the load-bearing defence and it is not optional. A headline median computed over
this population describes the $27.8M that generates events and is silent on the $43.0M that
does not. Making the correction available in a table is what was already wrong with the
alternative; making the table **inseparable from the figure** is the fix.

## 5. Definitions, fixed now

**A detected event.** A change in the **normalised** content hash of an eligible URL
(script/style blocks and HTML comments stripped, whitespace collapsed), that satisfies all
of:

1. **Confirmed** - a re-fetch 5s later returns the same new hash. A single differing fetch
   is discarded as transport noise, not counted and not timed.
2. **Controlled** - an impossible path on the same host, fetched in the same session,
   either returns 404/410 or returns a body whose hash differs from the target's. **The
   control is re-established every session, never cached** - four hosts of 60 changed
   verdict in 48 hours, so a stored allowlist would carry a stale verdict silently.
3. **Attributed** - the change is not simultaneous with a change on the same host's
   impossible path, which would make it host-level churn rather than page-level.

**Detection time `t_d`.** The timestamp of the **first** fetch that returned the new hash,
not of the confirming fetch.

**First meaningful price move `t_p`.** The first market-side observation, on any market
bound to that URL, at which **either** a trade prints **or** the mid moves >= 1.0c from the
pre-event mid. The pre-event mid is the last mid observed strictly before `t_d`.

**The measured quantity.** `t_p - t_d`, in seconds, signed. **Negative values are kept and
reported** - a negative means the market moved before we detected, which is the finding the
kill criterion is about, and discarding them would guarantee the answer.

**Unit of observation: THE EVENT.** Not the market, not the URL. One publication is one
observation however many markets it moves. Bootstrap at the event level, seed `20260820`,
10,000 resamples, and report leave-one-URL-out.

## 6. The kill criterion, pre-committed

> **After 50 detected events in a stratum, if the event-weighted median `t_p - t_d` in that
> stratum is under 10 seconds, the family closes in that stratum in this form.**

Per stratum, never pooled. A stratum that has not reached 50 events is **not ruled on** and
is reported as `n` with no verdict.

**Time box.** If a stratum has not reached 50 events by **2027-02-20** (six months), the
interim is reported with its `n` and the stratum is recorded as **unreportable with the
data that exists** - not "pending". Pending invites a return that never comes.

**A verdict of "the family survives" requires more than clearing the bar.** Clearing 10
seconds says the price did not move instantly. It does not say the move is capturable -
H65 measured a pooled hurdle of -3c to -10c per contract that any capture must clear
first, and that gate is separate and not tested here.

## 7. Abandonment conditions - tested FIRST, before any event is collected

H65's lesson: test the assumptions that would void the study before running it, not after.
Each of these is a **stop**, not a caveat.

1. **Can a known publication be detected at all?** Arm against one scheduled release with a
   published instant (the next CPI or FOMC statement) and confirm a normalised-hash change
   is observed within 60s of the announced time. **If no change is observed, the instrument
   does not detect publication and B3 cannot answer its question.**
2. **Does the market side resolve faster than the effect?** A 10-second median cannot be
   measured with a 10-second market-side poll. Market-side polling for markets bound to an
   armed URL must run at **<= 2s**, and this must be demonstrated on a known-moving market
   before arming. **If sustained 2s market-side polling is refused by the venue, the
   measurement's resolution is its poll interval and that must be reported as the floor.**
3. **Does the content control separate for every armed host, this session?** Any host where
   it does not is disarmed for the session and its markets excluded from that session's
   events.
4. **Is the source-side cadence sustainable at the load required?** See section 8.

## 8. Design requirements, not preferences

**8.1 Per-URL independent scheduling. A synchronous sweep is prohibited.**
`home.treasury.gov` takes **8.8 seconds** per fetch. In a synchronous sweep the slowest
host gates every other host's next request - the first sustained run drifted from a 9.0s
design to 27s per sweep for exactly this reason. **A synchronous B3 would have its
10-second bar decided by whichever source happened to be slowest that day, which is a
property of the scheduler and not of the market.** Each URL is scheduled on its own timer.

**8.2 The polling load is licensed only to what was measured, and no further.**
The sustained study licenses: **29.8 minutes of active polling, one request per 13.3s per
host on a single-URL host, and one per 2.1s on a host carrying six URLs.** It is **not** an
hour, **not** the 1-per-9s that a full sweep would need, and **not** general permission.
No declared `Crawl-delay` is silence, not consent, and a clean 30 minutes is not consent
either. Any cadence increase requires a fresh measurement first, and a first 429 is a
finding to be recorded, not an error to be retried around.

**8.3 Declared crawl delays are honoured, and robots-disallowed paths are never fetched.**
14 hosts disallow an in-scope path (204 markets) and are already excluded. Eleven hosts
declare a delay of >=10s; markets behind them cannot meet a 10-second detection bar by
polling and are reported as **detection-limited by the source's own terms**, not as failures.

**8.4 What the sustained result does not say.** `earthquake.usgs.gov` refused at sweep 1
and in every block after - **flat, and a flat line is not a curve.** `wunderground.com`
produced six transport failures in a single sweep at request ~663 and then **91 further
requests with none** - a blip, and a curve persists or worsens. **Neither may be summarised
later as "we saw rate limiting".** Recorded here so it cannot harden.

## 9. Pre-registered revisit triggers

Stated now so that finding them later is a confirmation rather than a discovery.

1. **If EOP events behave unlike their stratum-mates, the contestedness question is the
   first thing revisited.** B2 tested whether the White House EOP page is competitively
   contested and refuted it: within EOP, spread against log10(open interest) gives
   **r = -0.94, n = 32**, and the four EOP markets under 20,000 contracts quote at **6.00c**
   against 7.20c for other unscheduled markets and 5.00c for scheduled ones. A small EOP
   market is quoted as loosely as a small market anywhere else, so the tight book is size,
   not competition.
   **The caveat is pre-registered with the finding and must travel with it:** the largest
   non-EOP market in the population holds 16,440 contracts against an EOP median of
   1,548,106 - **the distributions do not overlap, so there is no matched population and
   this is not a weak control but no control.** The evidence for contestedness evaporated
   once the confounder was controlled. **That is not the same as contestedness being ruled
   out.** The matched cell is **n = 4**.
2. **If the scheduled stratum clears the bar and the unscheduled one does not**, or the
   reverse, check the strata are not proxying for market size before believing the split.
3. **If detection latency correlates with source fetch time**, the measurement is reading
   the scheduler and section 8.1 was not honoured.
4. **If more than 20% of confirmed events have no market-side move at all**, the binding of
   URLs to markets is wrong and the population needs re-deriving, not the statistic.

## 10. What is deliberately not being tested

- **Whether the move is capturable.** H65's hurdle gate is separate and unmet here.
- **The live-quote half of the in-scope universe.** It has no publication instant, so
  "latency from publication" is ill-posed there, not merely hard.
- **Polymarket.** B1's Polymarket population rests on a money-bearing slice rather than an
  enumerable universe, because gamma's cursor is inert and the CLOB enumeration is a floor
  (P22). Adding it needs an amendment and a stated denominator.
- **Anything requiring a headless render.** 13 hosts (712 markets, $536,625) are
  unverifiable by any control available; a headless render changes the access level and
  needs its own control before it counts.

## 11. What would make this whole design wrong

- If normalised-hash change is not a proxy for publication - if sources publish without
  changing the page we watch, or change the page without publishing. Condition 7.1 tests
  the first. **The second is only detectable by false-positive rate, which is why the quiet
  filter is a precondition and not a refinement.**
- If the venue's price timestamps are the venue's own clock and drift against ours. Any
  interval under a second is meaningless without establishing that they do not.
- If arming the URLs changes the thing measured - unlikely at this load, but a source that
  serves a cached page to repeat callers would flatten detection to the cache TTL and look
  like a null.

## 12. Seal

This document is sealed on commit. Nothing in sections 2 through 8 may be edited. Changes
are dated amendments appended below, stating what changed and why, with the original
preserved verbatim.

**Population, restated for the seal:** 125 URLs, 5,274 markets, $70,790,897 of open
interest, split SCHEDULED 47 / UNSCHEDULED 39 / UNKNOWN 39, with
`whitehouse.gov/administration/executive-office-of-the-president/` reported separately
inside UNSCHEDULED.

**Bootstrap seed `20260820`. 10,000 resamples. Unit of observation: THE EVENT.**
