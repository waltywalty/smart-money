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
