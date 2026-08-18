---
name: empirical-claims
description: >
  Use whenever a numerical result is produced, checked, replicated, or
  questioned — including casual phrasings like "is this real", "sanity check
  this", "does this hold up", "I got X, check it", "why is this so good", or
  "too good to be true". Also use before writing any pre-registration, before
  promoting or downgrading a hypothesis verdict, and whenever a result looks
  unexpectedly strong. Covers unit-of-observation errors, selection effects,
  lookahead, series composition behind a bucket, leave-one-out stability, and
  the distinction between statistical validity and obtainability.
---

# Empirical claims

A number that someone will act on is not the same artifact as a number in a report. This skill is the
procedure for producing the first kind. It exists because both halves of the pipeline lie: the data
layer fabricates, and the statistics manufacture significance out of the wrong unit.

Both failures produce **confident, plausible, specific** output. Neither announces itself.

## Part 1 — the data layer fabricates. Assume it.

When a fetch goes through a summarizing model rather than returning raw bytes, it invents values.
Observed, repeatedly, in production:

- A quote returned as `0.29/0.30` where the order book said `0.05/0.06`.
- A stated `COUNT=101` for a page enumerating exactly 100 rows; `COUNT=62` for a window that can hold
  at most 61.
- `limit=100` silently returning **92 rows** — and, on another probe, **34** — truncating with no error.
- The *same wrong answer* reproduced across two independent fetches — so re-fetching alone does not
  catch systematic failure.
- An entire order book invented, showing `0.409/0.415` where the true midpoint was `0.2685`.
- A large payload truncated to a **different window per URL**, so three passes gave three row counts.
- An empty book reported as `0.0000/1.0000`, injecting a phantom 50%-probability midpoint.

### The rules

1. **Never trust a self-reported count.** Count the lines yourself, in code.
2. **Cross-check against a different endpoint, not a second call to the same one.** Systematic
   fabrication reproduces; only a different source breaks it.
3. **Prefer the most primitive endpoint available.** An order book beats a market summary; a
   per-item read beats an aggregate. Aggregates fabricate near boundaries.
4. **Cap payloads.** Truncation is silent. Small pages plus your own pagination beat one large call.
5. **Verify page joins.** Adjacent pages must overlap or abut on a monotone key. A gap is data loss
   presenting as data.
6. **Never ask the fetch layer to do arithmetic**, especially timestamp conversion. Compute values in
   code and embed them literally in the prompt as strings to match.
7. **Add a completeness gate.** Find an invariant the data must satisfy — summed sizes equal reported
   volume, probabilities sum near one, a monotone series stays monotone — and check it. This catches
   what re-fetching cannot.
8. When a source is blocked by policy or `robots.txt`, **report it blocked**. Do not route around it.
9. **Close what you open.** An unclosed HTTP response leaks a file descriptor; a few hundred of them
   exhaust the socket pool and the client hangs *below* the timeout layer, alive and making no
   progress. Use `with urlopen(...) as r:` or a pooled session. Add a heartbeat file and treat a stale
   heartbeat as a stall, because this failure is silent by construction.
10. **Probe object stores with a ranged `GET`, never `HEAD`, and always include an impossible
    control key.** A coverage sweep built on `HEAD` reported an archive complete through August
    that ends in June. **Corrected 2026-08-17 — right rule, wrong mechanism.** This said `HEAD`
    returns `200` for keys that do not exist. It does not. Re-measured with the status read at the
    resource layer: `HEAD` on the impossible 1999 control returns **404**, ranged `GET` returns
    **404**, and on a real key they return **200** and **206**. The original `200` was
    `HTTP/1.1 200 Connection Established` — the CONNECT tunnel's status, printed first by
    `curl -I` and by `curl -D -` for **every** request through the VM's proxy, HEAD and GET alike
    (see rule 11). **Keep the rule**: ranged `GET` gives 206-vs-404, a sharper distinction than
    HEAD's 200-vs-404, and it survives proxies that mangle HEAD. Only the reason was wrong.
11. **Report status codes, never booleans, and send an explicit User-Agent.** A bare
    `python-urllib` UA is blocked at some edges; the resulting `HTTPError` was mapped by a
    `try/except` to "file absent", and the sweep reported everything missing — including files
    already proven present. A 403 must never be readable as a 404.
    **And report the status code *of the resource*, knowing which layer produced it.** Through a
    CONNECT proxy the first header line is the tunnel's `200`, not the object's. A sweep that read
    it with `head -1` reported `http=200` for six keys that do not exist; `-w '%{http_code}'`
    returns their real `404`. A code read from the wrong layer is worse than a boolean, because it
    looks like evidence.
12. **Verify a write by reading it back through a different path.** Rendered HTML, CDN-fronted
    pages and the writing process itself are all the same instrument as each other in the ways
    that matter. Read back through the API, unauthenticated where the resource is public. A count
    that matches the pre-write state is evidence *for* a stale read, not against it.
13. **Never assume a query parameter is honoured. Verify it with an impossible
    control, on every endpoint you use it on.** Filter honouring is per-endpoint
    and does not generalise: `ticker=` works on `/historical/trades` and is
    silently ignored on `/markets` and `/historical/markets`, while
    `series_ticker=` is the reverse. An ignored filter returns a full, plausible,
    wrong result set - six different crypto markets once arrived reporting the
    same close time. Record the verification per endpoint, not per parameter.
14. **The general form of rules 10-13: a status, a count or a body may have been
    produced by a layer other than the resource. Name the layer before you believe
    the number.** Four instances, all in this project, all silent, all in the
    direction of a plausible wrong answer:

    | what was read | what produced it | how it presented |
    |---|---|---|
    | a quote of `0.29/0.30` where the book said `0.05/0.06` | the summarising fetch layer | a confident, specific, invented value |
    | `http=200` for six keys that do not exist | the **CONNECT tunnel** (`HTTP/1.1 200 Connection Established`) | `curl -D - \| head -1` on every request, present or absent |
    | "file absent" across a whole sweep | a **TLS failure on the proxy leg** - some VMs export `HTTPS_PROXY=https://…`, which `urllib` cannot use | a generic exception a `try/except` maps to absence |
    | `http=100` after 120 s on a 16 MB PUT | an **unanswered `Expect: 100-continue`** | an interim 1xx returned as if it were final |

    The defences are the same each time and they are cheap: **read the status of the
    resource specifically** (`-w '%{http_code}'`, not the first header line); **an
    interim 1xx is never a success**; **an exception is not evidence of absence**
    until you have shown the request reached the resource; and **a control that
    must fail, run in the same pass**, because every one of these was caught by a
    control disagreeing and none by inspection.

Every one of those was caught by disagreement between two methods, not by inspection. None of
them announced itself, and none of them looked like a failure at the moment it happened.

### A single ordering of arms is not a control - counterbalance it or wash it out

When an experiment varies one factor and the arms run in sequence, **elapsed history is a
second factor and it was not randomised.** Anything with memory - a rate limiter, a cache, a
connection pool, a warmed index, a quota - loads that memory into whichever arm runs later.

**The operational rule, for every endpoint A/B in this project:**

1. **Counterbalance.** Run each arm in **both positions**: A-then-B and B-then-A. Report both
   orderings. If the effect flips with the order, the order was the cause.
2. **Or wash out.** Idle until the shared state has recovered, and show that it recovered -
   a baseline arm that returns to its clean value - before the next arm starts.
3. **Report the position.** Every rate or latency figure carries *what ran before it*. A number
   without its predecessor is not reproducible.
4. **Hold the source constant.** Two arms from two machines are not an A/B. See below.
5. **One repeat is the minimum.** The cost of the defence is one extra arm. Run it especially
   when the result is the one you wanted, because that is when the sequence stops early.

> **2026-08-17, T1.2.** Testing whether `/historical/markets` is rate-limited differently from
> `/markets`. Three arms on `/historical` at up to 69 req/s: **0% rejection**. One arm on
> `/markets` at 69 req/s, seconds later, same VM, same concurrency, same page size:
> **28.4% rejection**. One variable differed. The conclusion wrote itself, and it answered
> exactly the question the packet had asked.
>
> It was wrong. Repeating the `/historical` arm gave **32.5%**, and again **44.1%**. The limiter
> is shared and it has memory; `/historical` had simply been measured first, with the bucket
> full. The apparent property of the endpoint was a property of the running order.

> **The same day, one level deeper.** With the ordering rule applied, the arms were re-run from
> a **different VM in a different metro**: 3,200 requests at up to 64 threads, **zero 429s**,
> where the first machine had started rejecting after roughly 600. So the rejection curve is not
> a property of the API either - it is a property of *(API, source, recent history)*. Having
> stopped attributing to the endpoint what belonged to the ordering, the next available mistake
> was to attribute to the API what belonged to the source. **Both are the same error: crediting
> the variable you varied when an uncontrolled one moved too.**

The general form is the one already stated for status codes: **a number produced by a layer you
did not name is not a measurement of the thing you meant.** Ordering, source and warm state are
layers.

## Part 2 — the verification gate

Run every candidate finding through these before it is reported. Each one caught a real false
positive that would otherwise have shipped.

### The unit of observation

**Ask what is independent, then count that.** Rungs of one ladder are mutually exclusive; trades by
one wallet are one wallet; contracts in one event resolve together.

> Twelve markets showed a departure with an interval excluding zero. All seven adverse outcomes came
> from a **single event**. The honest count was two observations, not twelve.

Resample the independent unit, never the row.

### Leave-one-out, on every correlation

Report the range of the statistic recomputed with each point dropped. If it spans zero — or spans
`[-1, +1]` — there is no result, whatever the headline says.

> `r = +0.885` on n=4 became `r = -0.016` at n=11. The leave-one-out range had been `[-1, +1]` the
> whole time and said so.

### A price without size is not a price

Report depth beside every opportunity. A 3-cent edge on 20 shares is $0.60.

> One candidate rested on **five contracts**. Another on 38. A third bucket's entire opportunity was
> $789 of collateral for $7.41.

### Measure the price you could have TRANSACTED at

This is the gate that survives every statistical check and still kills the finding.

**For any entry taken from a bar, re-run the identical strategy entering one bar later.** If the edge
does not survive one bar of delay, it is a measurement of the past, not an opportunity. A bar's
closing price is not knowable until the bar has closed, so acting on it is lookahead by construction.

> A strategy returned **+4.96¢** in-sample and **+4.99¢** out-of-sample on 644 held-out events —
> matching to 0.03¢ — with leave-one-out stable, the largest single event a *loser*, and 98%
> coverage. It passed every check in this document. Then the entry ask was measured one, two and
> three minutes later: **+1.64¢, +3.12¢, +5.00¢ against the buyer.** Three minutes of delay consumed
> the entire edge. The effect was real, replicable, and belonged to whoever was fastest.

Corollary: when the same instrument shows an attractive price and no obtainable size, that is a
recurring structural fact, not bad luck. Four independent routes to it have been measured — far-OTM
tails carry no bid, cheap rungs never win, near-certainties are not quoted at the horizon you would
enter, and short-horizon favourites reprice away faster than a polling architecture can act.

### Name the moment the fact became public

For anything time-sensitive, state when the information existed and refuse any entry before it.

> An entry rule looked profitable until the settlement source's own publication timestamp showed the
> value became public **33 minutes after** the entry. The headline result was a coin flip.

### Selection is the first suspicion

If the sample was reachable *because* of a property correlated with the outcome, the result measures
the selection.

> Fifteen markets all settled the same way — not by chance, but because only far-out-of-the-money
> strikes were small enough to page fully. The single reachable counterexample flipped the mean.

Missing data is itself a selection variable. A missing quote means nobody was trading, which happens
when the outcome is already obvious.

### Report the composition of any subgroup you highlight

Before calling a bucket, print what is inside it.

> A calibration table showed a **−29.7pp** departure at high prices. 62 of its 89 markets were a
> single series — already the worst performer in the study. The dramatic version of the table was one
> series wearing a disguise.

### State the hurdle, then clear it

Find the cost of acting — spread, fee, slippage, collateral drag — and **measure it** rather than
assuming it. Compare every gross figure to it.

> A measured round-trip cost retroactively priced out a dozen findings that had reported gross edges
> against zero.

And check whether the hurdle is a constant or a function. The same measurement gave **−3.81¢** at a
24-hour horizon and **−1.94¢** at ten minutes; quoting the first as universal made a whole registry
of verdicts calibrate against the wrong bar. Fee schedules can also vary by instrument — one series
charged half of what the code assumed.

## Part 3 — pre-registration

Before looking at outcomes, write down: the rule, the sample size that would settle it, what would
make you abandon it, and the direction you expect. Then look. Hash the file so the order is provable.

Where a classification and a price are both involved, **seal the classification first, blind to the
price.** Have one agent classify with an explicit bar on reading any price; only then fetch prices.
This makes it structurally impossible to fit the reading to the payoff.

If the motivating observation is what suggested the hypothesis, **it cannot also be evidence for
it.** Exclude it from the verdict and say so.

**Check that held-out data exists before designing an out-of-sample test.** A hypothesis found by
slicing can have consumed its own test set.

> A post-hoc lead was found in a series with 22 events in its entire universe. All 22 had already
> been used by the study that produced the lead. No amount of further collection creates held-out
> data — only time does.

## Part 4 — reporting

- Lead with what would overturn it, not with the number.
- Give the interval, the n, and the unit that n counts.
- Say **"could not establish"** when the instrument failed. That is a different claim from a null and
  the distinction matters — recording an instrument failure as a finding is worse than either.
- A conclusion can be **right for the wrong reason**. When a verdict rests on an unstated premise,
  check the premise; if it is false, the verdict needs re-deriving even when the answer survives.
- **A perfect replication is not evidence of tradability.** Statistical validity and obtainability are
  separate gates and must be reported separately.
