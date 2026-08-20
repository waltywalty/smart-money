# B2 prep - the source layer before anything is polled

Programme: latency. Packet 6, Phase B, step B2, preparatory measurements only.
First run 2026-08-18. **Re-run in full 2026-08-20 from a different VM and a different
egress IP after the first VM expired** - so every figure below is a two-day, two-vantage
replication rather than a single reading. Where the two runs differ, both are given.

Nothing was polled repeatedly. Nothing was traded. Nothing was deployed.

---

## 1. robots.txt across every in-scope host

201 hosts sit behind the in-scope resolution sources of both venues; **20,994 in-scope
markets** behind them.

| robots.txt status | 2026-08-18 | 2026-08-20 |
|---|---:|---:|
| 200 | 161 | 160 |
| 404 - no policy, permitted | 20 | 20 |
| 403 - the policy itself is unreadable | 15 | 15 |
| other (429/500/502/504/202/transport) | 5 | 6 |

A **403 on robots.txt is not the same as absence**. Twenty hosts say nothing and are
therefore unrestricted; fifteen refuse to tell you the rule at all. Those fifteen carry
their own compliance question and it is not answered by treating them as silent.

### The number that matters for the whole family

| declared `Crawl-delay` for UA `*` | hosts | markets | share |
|---|---:|---:|---:|
| none | 180-181 | 20,328 | **96.8%** |
| >=1s | 9-10 | 276 | 1.3% |
| >=10s | 7-8 | 72 | 0.3% |
| >=30s | 1 | 32 | 0.2% |
| >=60s | 2 | 286 | 1.4% |

**96.8% of in-scope markets sit behind hosts that declare no crawl delay at all.**

This matters more than its size suggests. B3's pre-committed kill criterion is a
**10-second median from detection to first price move**. If the source hosts had
broadly asked for 10-60 second gaps, that criterion would have been unmeetable by
polling before a single event was collected - the family would have closed on a
robots.txt file rather than on a finding. They do not. **The constraint was a live
risk to the whole programme and it is now measured rather than assumed.**

It does bite on eleven hosts, which a polling design has to route around or drop:

| host | delay | markets |
|---|---:|---:|
| `labiennale.org` | 60s | 193 |
| `portwatch.imf.org` | 60s | 93 |
| `ufc.com` | 15s | 36 |
| `fda.gov` | 30s | 32 |
| `un.org` | 10s | 16 |
| `spc.noaa.gov` | 10s | 11 |
| `operations.portofvirginia.com` | 10s | 4 |
| `radar.cloudflare.com` | 10s | 2 |
| `leginfo.legislature.ca.gov`, `stacks.cdc.gov`, `justice.gov` | 10s | 1 each |

### Disallowed paths

**14 hosts disallow at least one in-scope path, covering 204 markets** - 1.0% of the
population. Two are worth naming:

- **`x.com` disallows all 27 of its in-scope paths**, 124 markets. Every market whose
  stated resolution source is a named X account is out of reach by compliant polling.
- **`data.giss.nasa.gov` disallows both of its**, 8 markets. That is the NASA GISTEMP
  `graph_data` file B1 held up as the exemplar of a genuine machine-readable source.
  The one source in the corpus that looks most like a proper feed is the one that asks
  you not to fetch it. Recorded because it is the opposite of a convenient result.

## 2. The content control - P21 tested, and mostly lifted

B1 found that on a third of hosts an impossible path returns 2xx, so the standard
status-code control establishes nothing there. The proposed replacement: fetch the body
for the impossible path and for the target, hash both, **require them to differ**. An
app shell served twice fails; a real page passes.

Run on all 60 void hosts, and - because a control that only fires on the broken cases
is not a control - on a seeded sample of 40 hosts where the status control already
works.

| | content differs | content identical |
|---|---:|---:|
| status control **does not** separate | **50** (was 47) | 10 (was 13) |
| status control **does** separate - positive side | 40 (was 39) | 0 (was 1) |

**Recovers 50 of 60 void hosts (83%), covering 4,363 in-scope markets and $1,994,952
of open interest. Agrees with the status control on 40 of 40 where that control already
worked.** Adopt it.

### Still void: 10 hosts, 712 markets, 3.4%, $536,625 open interest

Byte-identical bodies for a path that cannot exist and one that can.

| host | markets | open interest | what it does |
|---|---:|---:|---|
| `carbonarc.ai` | 321 | $209,249 | identical 4,665-byte shell for everything |
| `binance.com` | 222 | $0 | **HTTP 202, zero-byte body**, for both paths |
| `carbonarc.co` | 125 | $53,478 | same shell as `.ai` |
| `fe.secondmarket.com` | 19 | $0 | identical 1,222-byte shell |
| `spacex.com` | 16 | $272,426 | identical 3,134-byte shell |
| `lighter.xyz`, `bcb.gov.br`, `ch.ch`, `guide.michelin.com`, `state.gov` | 6 | $1,472 | shells, or 202 with no body |

`binance.com` is the one to watch: it is the largest single Polymarket in-scope source
(`/en/trade/BTC_USDT` and `/en/trade/ETH_USDT`, 186 markets between them) and **neither
control establishes anything about it from this vantage point.**

These need either a headless render - which changes the measurement's access level and
so needs its own control - or an out-of-band source. Until then, anything measured on
them is uncontrolled and must be reported as such, not folded into a total. **Do not
let the 3.4% quietly become zero.**

### The control's own stability is not perfect

Between the two runs, `itftennis.com`, `sec.state.ma.us` and `ottawa.ca` moved from
void to separating, and `state.gov` moved the other way. Four hosts of 60 changed verdict
in 48 hours. **The content control is a good control and it is not a deterministic one**,
which means B2 must re-establish it per measurement session rather than caching a
host allowlist.

## 3. What is still owed

B2 proper has not started. What exists is the population, the compliance envelope and a
working control. The three things the packet asks for - change detection, false-positive
rate, and measured latency from publication to first price move - all need repeated
fetches over time, which is the first thing in this programme that is not a single read.

---

# Amendment, 2026-08-20 - the false-positive floor, and the split that reframes B2

Four rounds at T+0, +5m, +15m, +60m over 425 in-scope targets (the 14 robots-disallowed
hosts excluded outright) and 187 impossible-path controls, on an ordinary weekday
morning with nothing happening. Rounds 0-2 are reported here; round 3 lands at 06:22Z
and is appended below.

Two hashes per fetch: **raw** over the whole body, and **normalised** after stripping
`<script>`/`<style>` blocks, HTML comments and collapsing whitespace - so markup churn
can be told from content churn.

## 1. The headline, and the answer I had to throw away

Across 367 URLs that returned 2xx in all three rounds: **56.9% did not change at all,
28.9% changed at every single interval, 14.2% were intermittent.**

My first comparison put all targets against all impossible-path controls and produced a
**+9.6 pp lift** for targets - which reads as "a change on a real page means something".
**It does not.** An impossible path only has a body to hash on hosts that serve a
catch-all, which are exactly the app-shell hosts and the ones most likely to churn. The
comparison was between a broad target set and a narrow, unrepresentative control set.

Paired on the same host, holding access conditions constant:

| interval | target changed | control changed | lift | verdicts agreed |
|---|---:|---:|---:|---:|
| T+5m | 22.4% | 27.1% | **-4.7 pp** | 79/85 (93%) |
| T+15m | 32.9% | 29.4% | +3.5 pp | 82/85 (96%) |

**On the hosts where a control exists at all, a hash change carries essentially no
information - the page that cannot exist churns as much as the page that does.** This
is the same failure shape the project has hit before: the comparison was against the
wrong population rather than against a different endpoint. The unpaired number is
recorded because it was computed, not because it is usable.

## 2. The in-scope population is two different problems

Which pages churn is more informative than how many.

**Churns at every interval** - live-quote pages: `google.com/finance` NDX and SPX
(3,514 markets), `cfbenchmarks.com` BRTI/ETHUSD/XRPUSD (2,067), `app.pyth.com` (1,152),
`charts.youtube.com`, `tradingview.com`, `trends.google.com`.

**Stable** - publication pages: `oscars.org`, `federalreserve.gov` FOMC calendar,
`bls.gov` CPI, `bea.gov` GDP, `home.treasury.gov` yields, `billboard.com` Hot 100,
KBO schedule, 36 `wunderground.com` history pages.

**These need different mechanisms, and the packet's B2 question is only well-posed for
one of them.** "Measured latency from publication to first meaningful price move"
assumes a discrete publication. A live quote has none: it moves continuously and the
market resolves on a value read at a stated time. Change detection is right for the
first kind and a category error for the second.

## 3. Stability alone is not enough - a page that is always empty is maximally stable

`binance.com` returns HTTP 202 with **zero bytes** and `carbonarc.ai` an identical
4,665-byte shell for any path. Both scored perfectly stable. Neither can ever signal
anything. So the usable subset is stability **intersected with** P21's control result,
not stability alone.

| the stable set, by whether any control separates on that host | urls | markets | open interest |
|---|---:|---:|---:|
| status control separates (untested by the hash control) | 120 | 2,622 | $65,109,017 |
| status control separates (tested) | 26 | 4,981 | $6,030,572 |
| content control separates | 25 | 2,372 | $818,554 |
| **VOID - no control works** | **38** | **691** | **$536,625** |

**Usable for change detection: 171 URLs, 9,975 markets, $71,958,143 of open interest -
77.4% of all the open interest measured.** Dropping `nass.org/can-I-vote` as well, which
P19 records as a false positive: **170 URLs, 6,021 markets, $71,064,722.**

The money concentrates in the stable, controllable half. That is a better result than
the market count alone suggests, and it is the number B3 should be scoped to.

## 4. For the churning half: is the quote in the HTML, or only in JavaScript?

Hashing is the wrong instrument there, so the narrower question decides whether those
markets are reachable at all. Test: fetch twice 30s apart, extract every number with 3+
significant digits, and check whether the numeric set **moves**. Control at the same
access level: run the identical extraction on an impossible path on the same host, so
any number that moves there too is boilerplate.

On the 22 largest churning URLs:

| | urls | markets | open interest |
|---|---:|---:|---:|
| **live value is server-rendered** (numbers moved, control did not) | 5 | 5,280 | $16,519,038 |
| no numeric movement in the served HTML at all | 16 | 2,273 | $1,400,140 |
| movement indistinguishable from boilerplate | 1 | 32 | - |

The five that work are `google.com/finance` NDX and SPX and three `cfbenchmarks.com`
indices - real ticks, e.g. ETH `2,249.80 -> 2,250.25` and BTC `69,489.68 -> 69,489.73`
in 30 seconds. **Every `app.pyth.com` and `pythdata.app` page failed**: 129 KB, ~200
numbers, and not one of them moved in 30 seconds while the page hash churned every
interval. Those are JavaScript shells - the churn is markup and the value is not in the
HTML. `forbes.com/real-time-billionaires` moved 11 numbers while its control moved 277,
so its movement is boilerplate and the control correctly refused it.

Reaching the JS-only pages needs a headless render, which **changes the measurement's
access level and therefore needs its own control** before anything measured through it
counts.

## 5. The polling budget, from measured fetch times

Single-fetch wall time over 671 reachable in-scope sources: p50 **0.43s**, p90 1.23s,
p99 4.12s, and exactly one URL of 671 over 10 seconds. **The fetch is not the
bottleneck; the poll interval is.**

For the 170-URL usable set - 85 of them timed in the reach pass, the other 85
mean-imputed at 0.71s, so the sweep total of **120.8s is an estimate, not a
measurement**:

| concurrency | sweep (est) | median detection delay |
|---|---:|---:|
| 4 | 30.2s | 15.5s |
| 6 | 20.1s | 10.5s |
| **8** | **15.1s** | **8.0s** |
| 12 | 10.1s | 5.4s |
| 16 | 7.5s | 4.2s |

**The 10-second median detection target is met from concurrency 8 upward.** That settles
the half of B3's kill criterion that is under our control. The other half - how fast the
price moves once the source publishes - cannot be answered without real events, and is
what B3 exists to collect.

---

# Amendment, 2026-08-20 (later) - the fourth round, the stratum split, and what a short window costs

## 6. The T+60m round settles the paired comparison

All three intervals, paired on the same host:

| interval | target changed | control changed | lift | verdicts agreed |
|---|---:|---:|---:|---:|
| T+5m | 22.4% | 27.1% | -4.7 pp | 79/85 (93%) |
| T+15m | 32.9% | 29.4% | +3.5 pp | 82/85 (96%) |
| T+60m | 30.6% | 31.8% | -1.2 pp | 82/85 (96%) |

The lift hovers around zero at every horizon and the two arms agree on 93-96% of pairs.
**Naive hash-based change detection carries no signal on the hosts where a control
exists.** Three horizons, one conclusion.

## 7. What a 15-minute observation window costs

The usable set was originally defined on three rounds spanning 15 minutes. Recomputed
over all four rounds spanning an hour:

| window | urls | markets | open interest |
|---|---:|---:|---:|
| 15 minutes | 171 | 9,975 | $71,958,143 |
| 60 minutes | 126 | 9,228 | $71,684,318 |
| **lost by extending** | **45 (26.3%)** | 747 | **$273,825 (0.4%)** |

**A short window overstates the stable population by a quarter of its URLs and by almost
none of its value.** The pages that fail the longer test are cheap ones. That is a
fortunate result and it was not guaranteed - the same arithmetic could have removed the
White House page and taken 60% of the money with it.

Excluding `nass.org/can-I-vote` per P19: **125 urls, 5,274 markets, $70,790,897.**
Derived twice by different routes - by re-running the stability filter over four rounds,
and independently by cross-tabulating a measured volatility flag against the strata -
and the two agree exactly.

## 8. The stratum split, per the 2026-08-20 ruling

Scheduled publication versus unscheduled: opposite cost structures, opposite competition.
Pooling them would average an HFT race against an empty field.

| stratum | urls | markets | open interest | share of OI |
|---|---:|---:|---:|---:|
| SCHEDULED | 82 | 3,046 | $18,520,213 | 26.1% |
| UNSCHEDULED | 45 | 2,508 | $50,917,664 | 71.6% |
| UNKNOWN - not forced into a bucket | 43 | 467 | $1,626,845 | 2.3% |

### The concentration behind that table

| | top-1 url | top-3 | top-5 | top-10 |
|---|---:|---:|---:|---:|
| share of all in-scope open interest | **60.5%** | 77.7% | 87.5% | 93.6% |

**$43,018,413 of the $50.9M unscheduled stratum - 84.5% of it - is one page**:
`whitehouse.gov/administration/executive-office-of-the-president/`, 37 markets. Remove
that single url and the strata inverse: SCHEDULED $11.8M over 81 urls, UNSCHEDULED $7.9M
over 44.

"The uncontested stratum carries the money" is true and rests entirely on one White House
personnel page. The **competitive** argument for the unscheduled stratum stands on its own
logic and does not need the dollar total; but no bar may be computed on a pooled $50.9M
that is really one contract family. **Open for ruling before B3 is sealed.**

## 9. A third kind of source was hiding inside SCHEDULED

Reported by stratum, the T+15m -> T+60m decay first looked like the prediction failing:
SCHEDULED decayed at **42.7%**, UNSCHEDULED at 13.3%. Calendared pages should be the
stillest things in the corpus.

**32 of the 35 scheduled decayers were `wunderground.com` history pages** - rolling
observation feeds that accumulate a new reading every few minutes, not calendared
releases. Separating them:

| class | urls | decayed | markets | open interest |
|---|---:|---:|---:|---:|
| **SCHEDULED** (calendared release) | 41 | **0 - 0.0%** | 2,114 | $17,700,136 |
| UNSCHEDULED | 45 | 13.3% | 2,508 | $50,917,664 |
| UNKNOWN | 43 | 9.3% | 467 | $1,626,845 |
| **ROLLING** (new) | 41 | **85.4%** | 932 | $820,077 |

**Not one of the 41 calendared-release pages changed in an hour.** The prediction was
right and the pooled number was hiding it behind a single host with 36 urls.

The durable form is **not** a fourth semantic stratum - a host list fitted to which pages
happened to decay is not a classifier. Stratum stays semantic; **volatility is measured
per url** (did normalised content change at any point across four rounds) and B3's bar is
the intersection:

| stratum | quiet | volatile |
|---|---|---|
| SCHEDULED | 47 urls, 2,571 mk, $18,344,614 | 35 urls, 475 mk, $175,599 |
| UNSCHEDULED | 39 urls, 2,439 mk, $50,825,419 | 6 urls, 69 mk, $92,245 |
| UNKNOWN | 39 urls, 264 mk, $1,620,864 | 4 urls, 203 mk, $5,981 |

Excluding every volatile url costs **$273,825 - 0.4%**.

This also resolves a loose end: `billboard.com/charts/hot-100` decayed inside an hour
despite the Hot 100 updating weekly. A false positive of exactly the kind B2 exists to
count, now classified rather than floating.

## 10. What a 403 is conditioned on, and an API nobody named

`earthquake.usgs.gov/earthquakes/browse/` returned **403 from the first request** in the
sustained study while its impossible-path control returned 404 - the pair separates, so a
block, not a rate limit and not exhaustion. **Refused-from-request-1 and refused-after-N
are different findings and only the second is a rejection curve.**

Diagnostic - no browser user-agent was impersonated, and the result does not license
impersonating one:

| user-agent | the named source | impossible path | `fdsnws/event/1/version` |
|---|---|---|---|
| research UA | **403** | 404 | **200** |
| curl default | **403** | 404 | **200** |
| empty | **403** | 404 | **200** |

And `earthquake.usgs.gov/earthquakes/map/` returns **200** with the research UA. So the
block is **path-specific**, not user-agent-conditioned and not host-wide.

**The same agency serves an open JSON API on the same host** - the first machine-readable
feed found anywhere in this corpus, against B1's finding that in-scope sources are
essentially all HTML. The general move for B2: when the named source is blocked or
JavaScript-only, check whether the publisher offers an API.

**With a boundary that must not be blurred.** Substituting a different url for the venue's
named settlement source is *a different resource*. For detection and alerting that is
fine. For deciding how a market resolves it is not, and convenience is not a reason to
conflate them.

---

# Amendment, 2026-08-20 (later still) - the sustained-polling result, and a null worth stating as one

## 11. Three horizons, one conclusion. This is a null, not a caveat.

| interval | target changed | control changed | lift | verdicts agreed |
|---|---:|---:|---:|---:|
| T+5m | 22.4% | 27.1% | -4.7 pp | 79/85 (93%) |
| T+15m | 32.9% | 29.4% | +3.5 pp | 82/85 (96%) |
| T+60m | 30.6% | 31.8% | -1.2 pp | 82/85 (96%) |

The lift straddles zero at every horizon, twice negative and once positive, and the two
arms return the same verdict on 93-96% of pairs. **Naive hash-based change detection on
an in-scope resolution page carries no information about that page, on any host where a
control exists.** Stated as a finding, not as a limitation of the method: the method was
sound, the population was measured three times over a twelve-fold range of horizons, and
the answer is no.

What survives is narrower and was established separately: **change detection works on the
125 urls that are measurably quiet**, where the base rate of spurious change is zero by
construction rather than by assumption. The null is about the naive form. It is what makes
the filtered form worth anything.

## 12. Sustained polling - the rejection curve, and what the instrument did instead

**Design:** 7 hosts at one url per sweep, plus `wunderground.com` at 6 urls per sweep (the
many-urls-per-host case), a 9-second sweep, one hour, with arm A alternating between the
target and an impossible path on the same host so total load is unchanged and any refusal
can be attributed to the host rather than the page.

**What actually ran, stated before the result:**

| | design | achieved |
|---|---|---|
| sweep cadence | 9.0s | **median 9.7s** |
| duration | 60 min continuous | **29.8 min active** - the VM was suspended for a single 1,808s gap between sweeps 125 and 126 |
| arm A per-host rate | 1 per 9s | **1 per 13.3s** |
| wunderground per-host rate | 1 per 1.5s | **1 per 2.1s** |
| total requests | - | 1,809 |

The cadence held; the wall clock did not. **This was 30 minutes of polling inside a
60-minute window, and it must not be described as an hour.**

**The result: no rejection curve at either load.**

| host | requests | 1 per | status codes |
|---|---:|---:|---|
| `wunderground.com` | 871 | 2.1s | 200 x799, 404 x66 (controls), **0 x6** |
| `bls.gov`, `bea.gov`, `federalreserve.gov`, `home.treasury.gov`, `eia.gov` | 134 each | 13.3s | 200 x67, 404 x67 (controls) |
| `oklahoma.gov` | 134 | 13.3s | 200 x67, 301 x67 (controls) |
| `earthquake.usgs.gov` | 134 | 13.3s | **403 x67**, 404 x67 (controls) |

**Zero 429s. Zero `Retry-After` headers. Zero `RateLimit` headers.** Fetch-time drift from
the first quarter of the run to the last: between -10.6% and +8.1%, i.e. noise. A host that
slows without refusing is still throttling, and none of them did.

The six `code 0` transport failures on wunderground all landed in **one sweep**, all six
urls at once, then clean - a blip, not a curve.

**`earthquake.usgs.gov` refused from request one** and its control returned 404 throughout,
so the pair separates: a path-specific block, not a rate limit. **Refused-from-request-1 and
refused-after-N are different findings and only the second is a rejection curve.**

### The design constraint that fell out of the instrument missing its target

The sweep was budgeted at 9s and the first attempt drifted to 27s per sweep. The cause:
**`home.treasury.gov` takes 8.8 seconds per fetch**, and in a synchronous sweep the slowest
host gates every other host's next request.

> **B3 must not poll on a synchronous sweep.** One slow source otherwise sets the detection
> latency for the entire population. Per-url independent scheduling, or the 10-second bar is
> decided by whichever source happens to be slowest that day - which is a property of the
> scheduler, not of the market.

### What this does and does not license

**Does:** 1 request per 13.3s to six government hosts, and 1 per 2.1s to a commercial host,
for 30 minutes, drew no refusal and no slowdown.

**Does not:** B3's design calls for 1 per 9s, which was not tested; 30 minutes is not
indefinite; and a single 30-minute window on one weekday morning from one egress IP is one
sample of a curve this project has already shown to be a property of
*(endpoint, source, recent history)*. **No declared crawl-delay is silence, not permission,
and a clean 30 minutes is not consent either.** Re-measure before any cadence increase, and
treat a first 429 as a finding rather than an error.

### Correction to 12 - the rejection table above was split by wall-clock and one cell was empty

The first pass split the run into four equal **time** quarters, and the third quarter came
back `0/0` for every host - because the 1,808s suspension fell inside it, so a whole
quarter contained no requests. **That table was measuring the scheduler, not the hosts.**
Split by **sweep index** instead, which counts requests - what a rejection curve is
actually a function of:

**Arm A** - one url per host per sweep, 938 requests over 134 sweeps:

| host | sw 1-20 | 21-40 | 41-60 | 61-80 | 81-100 | 101-120 | 121-134 |
|---|---|---|---|---|---|---|---|
| `earthquake.usgs.gov` | 403 x10/20 | 403 x10/20 | 403 x10/20 | 403 x10/20 | 403 x10/20 | 403 x10/20 | 403 x7/14 |
| `home.treasury.gov` | ok 20 | ok 20 | ok 20 | ok 20 | ok 20 | ok 20 | ok 14 |
| `oklahoma.gov` | ok 20 | ok 20 | ok 20 | ok 20 | ok 20 | ok 20 | ok 14 |
| `bea.gov` | ok 20 | ok 20 | ok 20 | ok 20 | ok 20 | ok 20 | ok 14 |
| `bls.gov` | ok 20 | ok 20 | ok 20 | ok 20 | ok 20 | ok 20 | ok 14 |
| `eia.gov` | ok 20 | ok 20 | ok 20 | ok 20 | ok 20 | ok 20 | ok 14 |
| `federalreserve.gov` | ok 20 | ok 20 | ok 20 | ok 20 | ok 20 | ok 20 | ok 14 |

**Arm B** - `wunderground.com` at 6 urls per sweep, 6x the per-host rate, 871 requests:

| host | sw 1-20 | 21-40 | 41-60 | 61-80 | 81-100 | 101-120 | 121-134 |
|---|---|---|---|---|---|---|---|
| `wunderground.com` | ok 130 | ok 130 | ok 130 | ok 130 | ok 130 | **REF 6/130** | ok 91 |

**Six government hosts never refused a single request.** `usgs` refused at sweep 1 and in
every block after, flat - a block, and a flat line is not a curve.

`wunderground` is the only host that refused **after** a period of success: six transport
failures at request ~663, all inside one sweep, **then 91 further requests with none**.
That is not a rejection curve either. **A curve persists or worsens; this recovered
completely and never recurred.** It is recorded as a single-sweep transport failure, which
is a different thing and should not be allowed to become "we saw rate limiting" in a later
summary.

So the arm that carries 6x the per-host load - the many-urls-per-host case, which is the
real risk for a host like `wunderground` with 36 in-scope urls - absorbed **1 request every
2.1 seconds for 30 minutes** without a single 429 and with fetch times flat to -2.4%.
