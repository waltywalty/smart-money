# B1 - The universe: which markets resolve to a fetchable source

Programme: latency. Packet 6, Phase B, step B1.
Run 2026-08-18, Kernel VM, raw HTTP throughout. Nothing was traded. Nothing was deployed.

> The packet: *"Report count and notional. A hundred markets worth $200 each is not a
> business. This is the gating number for the whole family."*

**The gating number: between one market in six and one in five.**

| | markets | share | open interest |
|---|---:|---:|---:|
| Kalshi, source named by the event endpoint, reachable, control separates | 16,843 | 20.0% | $99,061,869 |
| Kalshi, **and** the series endpoint names the same source | **14,540** | **17.3%** | **$91,407,507** |
| Polymarket, money-bearing, reachable, control separates | 887 | 20.8% | - |

The strict Kalshi row is the one to quote. It survives three independent filters: two
Kalshi endpoints agree on what the source is, the page answers, and an impossible
path on the same host does not. It is 12.2% of the venue's $752.0M of open interest.

The two venues were measured with the same rule and the same control pair and landed
within a few points of each other, which was not arranged and is not corroboration -
see section 7.

These are floors, not estimates. Section 7 says what they are floors of.

---

## 0. What was measured, and against what

| | Kalshi | Polymarket |
|---|---|---|
| enumeration route | `/trade-api/v2/markets?status=open` | `gamma /markets?offset=` + `clob.polymarket.com/markets` |
| paged to | `cursor_exhausted`, 824 pages | offset ceiling ~2,000; CLOB cursor |
| open markets | **84,290** non-`KXMVE*` | see section 3 - the venue cannot be enumerated cleanly |
| joined to an event | 84,231 (99.93%); 59 events had closed between passes | n/a |
| open events / series | 10,213 events, 3,464 series | n/a |
| source metadata | `settlement_sources` `[{name,url}]`, structured, on the event AND the series | `resolutionSource` (28% populated) + free-text `description` |

Kalshi hands you the source as structured data. Polymarket mostly does not, and
where it does the field is empty three times in four. That asymmetry runs through
everything below.

## 1. The money, before any classification

Kalshi, complete over the open universe. Open interest is contracts times
`notional_value_dollars`, which was read from the API and is exactly `1.0000`.

| | markets | open interest | 24h volume |
|---|---:|---:|---:|
| all open non-MVE | 84,231 | $752,020,238 | $44,329,848 |
| with any 24h volume | 14,952 (17.8%) | - | - |

Four markets in five did not trade at all in the last day. The count and the
notional are different questions and they give different answers; the packet was
right to ask for both.

Polymarket, over the money-bearing set defined in section 3.

| | markets | liquidity | 24h volume | lifetime volume |
|---|---:|---:|---:|---:|
| liquidity >= $100,000 (complete) | 903 | $402,054,388 | $17,152,426 | $4,049,884,237 |
| lifetime volume >= $100,000 (complete) | 1,754 | $390,905,246 | $23,857,771 | $4,903,336,990 |
| union of top 2,100 by each of three measures | 4,265 | $505,490,069 | $31,750,892 | $4,953,626,358 |

The two venues are the same order of magnitude on the axis that matters: **$44.3M
against $31.4M of 24-hour volume.** Kalshi gets there with 84,231 open markets,
Polymarket with a few thousand.

## 2. The four classes

The packet's classes, and the rule actually applied. It is deliberately structural,
because a structural rule can be stated, audited and re-run, and because the
substantive question - does that URL carry the resolving value - can only be settled
by fetching, which is section 4.

1. **named single official page or feed** - exactly one named source, and its URL has
   a specific path. IN SCOPE.
2. **official but requiring interpretation** - one named source but only a homepage,
   or two or more sources that must be reconciled.
3. **"credible reporting"** - resolution defers to press consensus.
4. **unspecified** - no source, or the source is the venue itself.

The load-bearing test is the path. `https://www.nfl.com` resolves nothing by itself;
you have to already know which page to read. `https://data.giss.nasa.gov/gistemp/
graphs/graph_data/Global_Mean_Estimates.../graph.txt` is a fetchable answer.

### The first rule set was wrong in both directions

Rule set one demoted on the *domain*: news and search domains went to class 3. The
seeded audit sample killed it inside one pass.

- **False negative.** `google.com/finance/quote/NDX:INDEXNASDAQ` (2,921 markets) and
  `apnews.com/hub/ap-top-25-college-football-poll` (323) are named single canonical
  pages. The domain is irrelevant; the path is the thing.
- **False positive.** `nass.org/can-I-vote` was the single largest class-1 bucket at
  3,954 markets. It is a voter-information portal. It carries no result.

Both survive into rule set two - the second is *still* misclassified, and is left in
deliberately rather than special-cased, because hand-patching the one false positive
I happened to notice would make the number look better than the method is. It cost
21.6% of the class-1 count and 0.8% of the class-1 open interest, which is the whole
argument for reporting notional alongside count in one line.

### Kalshi, rule set two

| class | markets | share | open interest | 24h volume |
|---|---:|---:|---:|---:|
| 1 named single official page/feed **[IN SCOPE]** | 22,966 | 27.3% | $113,568,941 | $6,638,643 |
| 2 official, needs interpretation | 61,205 | 72.7% | $637,586,122 | $37,636,812 |
| 3 credible reporting | 0 | - | - | - |
| 4 unspecified | 60 | 0.1% | $865,174 | $54,393 |

Class 3 is empty **by construction**: rule set two has no news-domain test, so the
news-sourced markets sit inside classes 1 and 2 according to their URL path. This is
a known departure from the packet's four-way scheme and it is stated rather than
hidden. Sports is 41,539 of class 2 - the sports book is almost entirely
"reconcile these several league and stats sites".

**Class 1 collapses to 547 distinct URLs.** That is the finding that makes the rest
of the programme tractable: 22,966 markets are polled by watching at most 547 pages.

### Polymarket, same rule

| class | markets | share | 24h volume | liquidity |
|---|---:|---:|---:|---:|
| 1 named single official page/feed **[IN SCOPE]** | 1,494 | 35.0% | $13,087,340 | $66,451,460 |
| 2 official, needs interpretation | 1,428 | 33.5% | $10,057,747 | $270,606,026 |
| 3 credible reporting | 1,217 | 28.5% | $7,753,404 | $101,613,507 |
| 4 unspecified | 126 | 3.0% | $852,401 | $66,819,076 |

Class 1 collapses to **211 distinct URLs**. The phrase "consensus of credible
reporting" appears verbatim in 2,398 of the 4,265 descriptions (56%) - on Polymarket
the modal resolution rule is not a source at all.

## 3. Polymarket cannot be enumerated from its public API, and the failure is silent

Four traps, each verified by probe, in the order they were found. The fourth voids a
previous result of mine.

| # | trap | verified by |
|---|---|---|
| T1 | `limit=500` **silently returns 100** | direct read of `len(markets)` |
| T2 | `offset` above ~2,000 returns **422**, body naming `/markets/keyset` | offset sweep 0/1000/2000/2100 |
| T3 | `active=` and `archived=` are **silently ignored** | `active=false` returns `active:true` rows; `archived=true` returns `archived:false` rows |
| T4 | `/markets/keyset` **ignores every cursor parameter** and returns page 1 forever | 410,196 rows pulled -> **100 distinct** `conditionId` |

T4 is the serious one. The endpoint returns a fresh 216-character `next_cursor` on
every call, and it is inert: `cursor`, `next_cursor`, `after`, `page_cursor` and
`start_cursor`, raw and percent-encoded, all returned the identical first five
conditionIds. Ten probes, ten HTTP 200s, zero advancement.

**This is the failure my own stop-reason rule does not catch.** The standing rule was
"only `cursor_exhausted` or `empty_page` may be read as a complete answer". A cursor
that never advances never exhausts and never empties, so the rule waits forever while
the row count climbs and looks like progress. An earlier pass reported 116,900
Polymarket rows and every aggregate computed on them was one market repeated 1,169
times.

> **New rule, same family as "a status code is produced by a layer and may not be the
> resource's": a cursor is produced by a layer and may not advance the resource.
> Assert the stream advances - count distinct keys per page - and stop when it does
> not. A stop reason is necessary and is not sufficient.**

What *is* honoured, each verified by an impossible value returning zero rows or a
422 next to a permissive value returning rows:

| parameter | honoured | control |
|---|---|---|
| `closed=` | yes | `closed=true` returns closed rows |
| `volume_num_min` | yes | `1e18` -> 0 rows; `0` -> rows |
| `liquidity_num_min` | yes | `1e18` -> 0 rows; `50000` -> rows |
| `end_date_min` | yes | year 3000 -> 0 rows |
| `order=` + `ascending=` | yes | desc -> $2.92M top liquidity, asc -> $0; impossible field -> **422** |
| `active=`, `archived=` | **no** | see T3 |

So the venue is reachable only through filtered slices, and the *count* has to come
from somewhere else. `clob.polymarket.com/markets` is that somewhere else - a
different host, a different layer, 1,000 rows a page, and a cursor that genuinely
advances. It enumerated 286,757+ distinct markets, of which the live set - `active`
and not `closed` and `accepting_orders` and `enable_order_book` - is small. That
enumeration is still running at the time of writing and its own stall guard fired
falsely once at 279,803 (three full pages of nothing new, then new markets resumed at
page 300), so its total is reported as a floor, not a total.

## 4. Reachability, and why 2xx is not enough

Every class-1 URL was fetched once: ranged GET, explicit User-Agent, `Expect:`
suppressed, redirects followed, status codes recorded. Then the control that makes
the number mean anything - **an impossible path on the same host at the same access
level**, paired with the host root as the positive side.

**On a third of hosts the control does not separate.** 88 of 257 Kalshi hosts and 34
of 91 Polymarket hosts answer an impossible path with 200, 202 or 206 - single-page
apps and catch-all routers. On those hosts a 2xx on the real URL is a fact about the
router, not about the resource.

Kalshi, 547 URLs over 257 hosts:

| | URLs | markets | open interest | 24h volume |
|---|---:|---:|---:|---:|
| **control separated, target 2xx** | **306** | **16,843** | **$99,061,869** | **$5,673,032** |
| control separated, target not 2xx | 7 | 33 | $134,700 | $44,299 |
| control did not separate, 2xx | 190 | 5,331 | $9,450,250 | $785,158 |
| control did not separate, not 2xx | 44 | 759 | $4,922,123 | $136,154 |

Polymarket, 211 URLs over 91 hosts: **117 URLs, 887 markets** in the separated-and-2xx
cell; 67 URLs / 524 markets reachable but on a non-separating host.

Taking only the cell where the control separates:

- **Kalshi: 16,843 markets, 20.0% of the open universe, $99,061,869 of open interest.**
- **Polymarket: 887 markets, 20.8% of the money-bearing universe.**

## 5. The source layer is HTML, not feeds

Weighted by markets, of everything that came back 2xx:

| content type | Kalshi markets | Polymarket markets |
|---|---:|---:|
| `text/html` | 22,116 | 1,404 |
| `application/pdf` | 55 | 1 |
| `text/plain` | 3 | 6 |

There is essentially no machine-readable feed behind either venue's in-scope
markets. Whatever B2 measures about change detection and polling economics, it will
be measuring **scraping**, and the false-positive rate B2 is asked for is a property
of page diffing, not of an API. This should be treated as a finding about the family,
not a detail of the sample: the resolution sources these venues name are pages built
for people to read.

## 6. Two fields that exist in the schema and are never populated

Both were caught the same way and both would have produced a confident wrong number.

- **Kalshi `liquidity_dollars` reads `"0.0000"` on all 84,290 open markets.** Not a
  measurement - an unpopulated field. Cross-checked on a second endpoint
  (`/markets/{ticker}`, same value) on the busiest market on the exchange, which
  carries 23.3M contracts of open interest and shows `yes_ask_size_fp: 42535.60`.
  There is a book; the field just does not report it. Open interest is the notional
  measure used here instead.
- **Polymarket `resolutionSource` was empty on every row the keyset stream returned.**
  It is in fact populated on 1,195 of 4,265 money-bearing markets (28%). The zero was
  an artefact of T4 - the 100 repeated markets all happen to have it blank.

And a third, of the opposite kind: `/markets/{ticker}/orderbook` returns HTTP 200
with the payload under **`orderbook_fp`**, not `orderbook`. Reading the wrong key
yields `{}` and reads exactly like an authentication gate. The live public book is
fully populated - five levels a side on the market checked, with sizes. This does not
contradict the recorded Kalshi depth ceiling, which is about *historical* depth, but
it is close enough to it to be worth stating explicitly, and it is parked for
verification against the exact wording in `docs/INFRA.md` rather than amended from
memory.

## 6.5 The two Kalshi endpoints disagree about the source, on one event in five

`settlement_sources` is carried on the **event** object and again on the **series**
object. They are not the same list.

| | events | markets |
|---|---:|---:|
| identical source list | 8,247 (80.8%) | 71,774 |
| **different source list** | **1,966 (19.2%)** | **12,457 (14.8%)** |
| series absent | 0 | 0 |

And the disagreement is not cosmetic - it moves the class, weighted by markets:
class 1 -> class 2 on 2,488 markets, class 1 -> class 4 on 978, class 2 -> class 1
on 1,026, class 2 -> class 4 on 2,954.

| in-scope count, by which endpoint you believe | markets | open interest |
|---|---:|---:|
| the event endpoint | 22,966 | $113,568,941 |
| the series endpoint | 20,526 | $103,651,866 |
| **both, agreeing** | **19,500** | **$97,318,212** |

**The choice of endpoint moves the gating number by 2,440 markets - 10.6%.** Nothing
in either response says which is authoritative. Agreement retains 84.9% of the count
and 85.7% of the open interest, and the 274 URLs it leaves are the ones B2 should
start from. Requiring both endpoints and then requiring the page to answer with a
separating control leaves **152 URLs and 14,540 markets**.

This is the cross-check rule earning its keep: the finding was checked against a
different endpoint rather than a second call to the same one, and the two did not
agree.

## 7. What this does not establish

- **Class 1 is a claim about the venue's stated source, not about the answer being
  at that URL.** `nass.org/can-I-vote` proves the gap: correctly classified by the
  rule, useless in fact. Section 4 narrows the claim to "the page exists and the host
  discriminates paths". It does not narrow it to "the resolving value is on that
  page". Nothing here has parsed a single one of those 547 pages.
- **The 20.0% / 20.8% agreement is not independent corroboration.** Same rule, same
  operator, same day, and the two denominators are not the same kind of object -
  Kalshi's is a complete open universe, Polymarket's is a money-bearing slice.
- **The Polymarket denominator is a slice, not a universe.** 4,265 markets, the union
  of the top ~2,100 by each of three money measures, reachable only because `order=`
  is honoured. Markets below rank ~2,091 on 24h volume each did under $1,399.61, and
  their count is unknown. The liquidity tail is fatter - rank 2,051 still had
  $44,228 - so $505,490,069 of liquidity is a floor with a materially incomplete tail.
- **The CLOB enumeration is incomplete.** 3,328 of the 4,265 money-bearing markets
  had not been reached when the intersection was computed, so "937 money-bearing and
  live" is a floor and not a universe count. Of the 937 that were reached, all 937
  were live, which is suggestive and is not a measurement of the rest.
- **The Kalshi classifier's error rate is not measured.** Two errors were found by
  a seeded 24-row audit and the rule was rewritten around them. A 24-row audit
  establishes that errors exist. It does not bound how many.
- **The class-1 figure is endpoint-dependent, and section 6.5 measures by how much.**
  The strict row in the headline is the intersection. The looser row is what you get
  by trusting one endpoint.
- **59 markets could not be joined** to an open event because the event closed between
  the two passes. 0.07%, recorded rather than dropped silently.

## 8. What B2 inherits

A concrete, small work list rather than a category.

- **A work list of 758 URLs, or 485 if you take the strict reading.** Every in-scope
  market on both venues sits behind 547 Kalshi URLs and 211 Polymarket ones; requiring
  the two Kalshi endpoints to agree cuts the Kalshi side to 274. Either way it is a
  list, not a category, and B2's "measured latency from publication to first
  meaningful price move" has a defined population on day one.
- **269 URLs are on hosts where an impossible path separates** (152 Kalshi under the
  strict reading, 117 Polymarket), so a change detected there is a change in the
  resource rather than in a router.
- The non-separating hosts - 99 of the strict Kalshi 274, 34 of 91 Polymarket hosts -
  need a different control before anything measured on them counts. Content hashing
  against a known-absent path on the same host is the obvious candidate and is
  untested. That is a B2 design constraint, not a B2 finding.
- Everything is HTML. Change detection is page diffing, and the false-positive rate
  is the rate at which those pages change without the answer changing.
- **Concentration to watch.** On Kalshi the top class-1 URL by open interest is
  `cfbenchmarks.com/data/indices/BRTI` at $8.1M; on Polymarket it is
  `binance.com/en/trade/BTC_USDT` at 120 markets. Crypto index pages carry a large
  share of the in-scope notional on both venues, which means the family's exposure is
  less diversified than 758 URLs makes it sound.

## 9. Reproduction

All scripts under `programmes/latency/b1/`. Every probe carries an impossible control
and a positive control at the same access level. Audit samples are seeded with
`20260818`. Raw HTTP throughout; no WebFetch was used at any point.
