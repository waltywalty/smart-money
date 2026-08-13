# Are H55 and H57 revivable from public archives? — 2026-08-13

Task 10 of the Cowork workflow packet. **Report only.** Neither hypothesis was re-run and no
outcome data was fetched. All measurement is raw HTTP from the Kernel VM.

Both H55 and H57 are **Kalshi** hypotheses, which decides two of the four sources immediately.

---

## Verdict

| | Coverage | Sample if revived | Verdict |
|---|---|---|---|
| **H55** — near-certainties at a shorter lead | **Sufficient, and closing** | ≥ 233 events (measured, lower bound) against a bar of 150 | **Revivable, at T-1h only, before ~2026-08-17** |
| **H57** — KXRAIN above ~70¢ | **Zero** | 0 | **Not revivable. And the recorded reason is wrong.** |

---

## The finding that matters more than either hypothesis

**Kalshi does not retain settled-market history. It serves a rolling window.**

Measured today across 80 series (21,982 reachable settled events), the earliest reachable
`close_time` anywhere is **2026-06-07** — 67 days back. Per series:

```
KXRAIN      2026-07-16 .. 2026-08-12    23 events,  460 markets
KXFED       2026-06-17 .. 2026-07-29     2 events,   22 markets
KXCPIYOY    2026-06-10 .. 2026-08-12     3 events,   69 markets
KXEGGS      2026-06-10 .. 2026-08-12     3 events,    3 markets
KXNBAGAME   2026-06-09 .. 2026-06-14     3 events,    6 markets
KXHIGHNY    2026-06-07 .. 2026-08-12    67 events,  402 markets
KXMLBGAME   2026-06-07 .. 2026-08-13   863 events, 1726 markets
```

**Cross-checks (the rule: never a second call to the same endpoint).**

1. `/events?series_ticker=KXRAIN&status=settled` returns **23 events** — identical to the count
   derived from `/markets`. Two different endpoints, same window.
2. Independent third party: the NBER replication package `jdkatz21/Prediction_Markets_Public`
   states in its README, verbatim — *"The current code will work to pull data before the
   historical cutoff (100 days is how Kalshi has it set currently)."* A disinterested source
   documenting the same mechanism. Their figure is 100 days; the window measured here is 67 days
   exchange-wide and 28 for KXRAIN. The mechanism is corroborated, the number is not — cite the
   measurement, not the README.

**This reframes H57's recorded verdict.** H57 says its sample problem is *"a calendar problem
rather than a compute one"* — wait, and events accumulate. They do not. The window **slides**: on
2026-08-12 the project reached 22 KXRAIN events; today it reaches 23, and the oldest will fall off
as new ones arrive. Waiting does not grow the sample. The only route to 100 KXRAIN events is to
**record them as they settle**, at ~11–12 events/month — roughly **9 months of continuous
self-collection**. That is a standing infrastructure decision for Walton, not a calendar wait.

The same constraint sits under every historical Kalshi measurement this project has made or will
make. The ground is moving.

---

## H55 — revivable at a one-hour lead, and the window shuts in about four days

**`revive_if`:** *"Re-tested at a shorter lead where the band is populated — a different hypothesis
needing its own pre-registration, with H7/H9's capital-lockup arithmetic applied."*

**Coverage: sufficient.** `archive.pmxt.dev` publishes free hourly Kalshi orderbook snapshots as
Parquet, CC BY 4.0. Kalshi coverage measured: **2026-05-14 → 2026-06-11T03:00 UTC**, one file per
hour, 20–90 MB each. That is the right instrument — a full-exchange book at every hour lets any
market be read at T-1h instead of T-24h, which is exactly what H55's structural finding demands.

**But quotes are only half of it, and outcomes are the binding half.** The archive is orderbook
only; settlements must still come from Kalshi, which reaches back only to 2026-06-07. So the usable
region is the intersection:

```
archive quotes     2026-05-14 ────────────────────────► 2026-06-11
Kalshi outcomes                          2026-06-07 ──────────────────────► today
usable overlap                           2026-06-07 ─► 2026-06-11   (5 days)
```

**Measured sample in that overlap: 233 independent events**, from 80 series — a lower bound, since
1,624 series carry settled events. The pre-registration bar was 150. It clears.

**Three constraints that must go into any pre-registration:**

1. **Granularity is hourly.** The finest testable lead is T-1h. A T-10m test — the horizon where
   H60 measured the hurdle at its lowest, −1.94¢ — is not reachable from this archive at all.
2. **Five consecutive calendar days is one regime, and series concentration will be severe.**
   This is the exact shape of false positive #7 (62 of 89 markets in one series). Leave-one-series-out
   is mandatory, and no result from this window may be stated as a property of the exchange.
3. **The overlap is closing at one day per day.** The archive's end is frozen at 2026-06-11;
   Kalshi's floor advances daily. At a 67-day retention the floor reaches 2026-06-11 on or about
   **2026-08-17**. After that the overlap is empty, permanently, unless the archive resumes.

**The archive has stopped.** The site advertises *"updated every hour"*; the newest Kalshi file is
2026-06-11T03, two months stale. Do not plan on it resuming.

A pre-registration stub is written to `registry/h64-preregistration-STUB.md`. No outcome data was
fetched.

---

## H57 — not revivable, coverage zero

**`revive_if`:** *"At least 100 NEW KXRAIN events have settled that were not in the 2026-08-12
universe."*

- The only source holding Kalshi data covers **2026-05-14 → 2026-06-11**. KXRAIN settlements are
  reachable from Kalshi only from **2026-07-16**. The two windows do not touch. The archive would
  supply KXRAIN quotes for events whose outcomes cannot be obtained from anywhere.
- Even granting outcomes, 28 days of a ~11-events/month series is **~11 events against a bar of 100**.
- Taking the archive's last pre-expiry quote as a settlement proxy would close the gap on paper.
  **It is the instrument failure H39 died on** — `last_price` on settled markets is converged or
  stale — and it is not endorsed here.

Coverage is zero on every reading. H57 stays could-not-establish.

---

## Source-by-source

| Source | What it actually is | Use to H55/H57 |
|---|---|---|
| `archive.pmxt.dev` | Free hourly Parquet orderbooks, CC BY 4.0. Kalshi **2026-05-14 → 2026-06-11T03**, then stops. Polymarket, Limitless, Opinion also present. | **The only source with any Kalshi data.** H55 yes, within 5 days of usable overlap. H57 no. |
| `jdkatz21/Prediction_Markets_Public` | **Contains no data.** Full recursive tree is 530 entries / 1.6 MB; `.gitignore` excludes `data/` and `output/`. It is a scraper needing your own `KALSHI_KEYID`/`KALSHI_PRIVATE_KEY`, bound by the same cutoff. Last push 2026-06-30 — the weekly Friday action has not run in six weeks. | None as data. Valuable only as the independent corroboration of the retention cutoff. |
| `huggingface.co/datasets/godss1985/Polymarket_data` | Polymarket only — `markets`, `orderfilled`, `quant`, `trades`, `users` Parquet. Last modified **2026-02-20**. | **None.** Both hypotheses are Kalshi. |
| `pmxt-dev/pmxt` | TypeScript client, 2,077 stars, last push 2026-07-18. Depth-aware `getExecutionPrice(orderBook, side, size)` with partial fills. | None as data. Worth reading for the execution model this repo lacks. |

---

## Two instrument failures caught, both worth keeping

**1. `HEAD` on `r2kalshi.pmxt.dev` returns 200 for files that do not exist.** A control key,
`kalshi_orderbook_1999-01-01T00.parquet`, returns `200` to `curl -I` and `404` to a `GET`. The first
coverage sweep, built on HEAD, reported the archive as complete from April through August. It is not.
**Probe object stores with a ranged GET (`Range: bytes=0-0`) and always include an impossible key as
a control.**

**2. A bare `python-urllib` User-Agent is blocked at the edge.** The requests returned an HTTPError
that a `try/except` mapped to "file absent" — so the second sweep reported *everything* absent,
including files already proven present. Silent, and in the same direction as a real answer.
**Send an explicit User-Agent, and report status codes rather than booleans**, so a 403 can never be
read as a 404.

Both were caught by disagreement between two methods, not by inspection. Neither announced itself.
