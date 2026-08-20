# B4 - population decay log

One row per run, appended, never edited. `resolving` requires 2xx **and** a separating
control on that host. Rows are comparable **only within a vantage**, and a url counts as
**decayed only when it fails from both**.

## Prior readings, preserved - they predate the vantage-comparison format

| run | when | from | resolving | note |
|---|---|---|---:|---|
| #1 | 2026-08-20T07:36Z | vm | 125 / 125 | manual, seeding the series |
| #2 | 2026-08-20T08:22Z | **ci** | **119 / 125** | committed `e4e37b7` by `github-actions[bot]` |

**Run #2's six "failures" all returned 200 or 206 from the VM minutes later** -
`bloomberg.com/billionaires/` 403 -> 206 (52 markets), `kenpom.com/index.php` 403 -> 200
(43), `hitsdailydouble.com/charts/hits-top-50` transport-fail -> 200 (3),
`defillama.com/stablecoins` 403 -> 200 (1), `gov.il/.../central-elections-committee/...`
403 -> 206 (1), `hitsdailydouble.com/sales_plus_streaming` transport-fail -> 200 (1).
**None of it was decay.** That is why the format changed: the two readings now travel
together, with the age of the other vantage's reading stated, so a comparison against a
stale baseline is visible as one.

## The series

| run (UTC) | from | urls | resolving | not 2xx | control void | vs other vantage | DECAYED (both) | markets resolving |
|---|---|---:|---:|---:|---:|---|---:|---:|
| 2026-08-20T09:17Z | vm | 125 | **125** | 0 | 0 | no ci reading yet | **0** | 5274 |

```b4state
{"vantage": "vm", "stamp": "2026-08-20T09:17Z", "epoch": 1787217456, "resolving": 125, "failed": []}
```
