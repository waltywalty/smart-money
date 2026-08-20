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
