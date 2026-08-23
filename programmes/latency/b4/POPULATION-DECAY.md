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
| 2026-08-21T06:03Z | ci | 125 | **121** | 4 | 0 | 0 both, 4 ci-only, 0 vm-only (vm 20.8h old) | **0** | 5177 |

<details><summary>2026-08-21T06:03Z [ci] - not 2xx (4)</summary>

- `403` https://www.bloomberg.com/billionaires/  (52 markets, $8,090)  `retry-after=0 server=Varnish x-served-by=cache-chi-kmdw8640085-CHI`
- `403` https://defillama.com/stablecoins  (1 markets, $0)  `cf-ray=a2e76e9ae8a36abb-MSP server=cloudflare`
- `403` https://kenpom.com/index.php  (43 markets, $0)  `cf-ray=a2e76eaf9a7fa1d1-MSP server=cloudflare`
- `403` https://www.gov.il/en/departments/central-elections-committee/govil-landing-page  (1 markets, $0)  `cf-ray=a2e76edcedc56abb-MSP server=cloudflare`

</details>

```b4state
{"vantage": "ci", "stamp": "2026-08-21T06:03Z", "epoch": 1787292198, "resolving": 121, "failed": ["https://defillama.com/stablecoins", "https://kenpom.com/index.php", "https://www.bloomberg.com/billionaires/", "https://www.gov.il/en/departments/central-elections-committee/govil-landing-page"]}
```
| 2026-08-22T05:59Z | ci | 125 | **119** | 6 | 0 | 0 both, 6 ci-only, 0 vm-only (vm 44.7h old) | **0** | 4801 |

<details><summary>2026-08-22T05:59Z [ci] - not 2xx (6)</summary>

- `0` https://pythdata.app/explore  (370 markets, $148,059)  `-`
- `0` https://nces.ed.gov/nationsreportcard/  (6 markets, $42,169)  `-`
- `403` https://www.bloomberg.com/billionaires/  (52 markets, $8,090)  `retry-after=0 server=Varnish x-served-by=cache-iad-kiad7000044-IAD`
- `403` https://defillama.com/stablecoins  (1 markets, $0)  `cf-ray=a2efa5c2be9ec971-IAD server=cloudflare`
- `403` https://kenpom.com/index.php  (43 markets, $0)  `cf-ray=a2efa5cf9ab1b8b1-IAD server=cloudflare`
- `403` https://www.gov.il/en/departments/central-elections-committee/govil-landing-page  (1 markets, $0)  `cf-ray=a2efa6005a3073f7-IAD server=cloudflare`

</details>

```b4state
{"vantage": "ci", "stamp": "2026-08-22T05:59Z", "epoch": 1787378353, "resolving": 119, "failed": ["https://defillama.com/stablecoins", "https://kenpom.com/index.php", "https://nces.ed.gov/nationsreportcard/", "https://pythdata.app/explore", "https://www.bloomberg.com/billionaires/", "https://www.gov.il/en/departments/central-elections-committee/govil-landing-page"]}
```
| 2026-08-23T05:59Z | ci | 125 | **117** | 8 | 0 | 0 both, 8 ci-only, 0 vm-only (vm 68.7h old) | **0** | 4944 |

<details><summary>2026-08-23T05:59Z [ci] - not 2xx (8)</summary>

- `403` https://www.ice.com/report-center  (10 markets, $2,915,972)  `cf-ray=a2f7e4777c584624-DFW server=cloudflare`
- `403` https://www.theice.com/products/213/WTI-Crude-Futures  (152 markets, $500,391)  `cf-ray=a2f7e4840807f0c2-DFW server=cloudflare`
- `403` https://www.theice.com/index  (23 markets, $104,934)  `cf-ray=a2f7e4840f4d6c5b-DFW server=cloudflare`
- `403` https://www.ice.com/report/10  (48 markets, $24,618)  `cf-ray=a2f7e47778fc42f9-DFW server=cloudflare`
- `403` https://www.bloomberg.com/billionaires/  (52 markets, $8,090)  `retry-after=0 server=Varnish x-served-by=cache-dfw-kdal2120046-DFW`
- `403` https://defillama.com/stablecoins  (1 markets, $0)  `cf-ray=a2f7e429bd7a2145-ORD server=cloudflare`
- `403` https://kenpom.com/index.php  (43 markets, $0)  `cf-ray=a2f7e434fa8c4ff4-ATL server=cloudflare`
- `403` https://www.gov.il/en/departments/central-elections-committee/govil-landing-page  (1 markets, $0)  `cf-ray=a2f7e476d821d83b-DFW server=cloudflare`

</details>

```b4state
{"vantage": "ci", "stamp": "2026-08-23T05:59Z", "epoch": 1787464783, "resolving": 117, "failed": ["https://defillama.com/stablecoins", "https://kenpom.com/index.php", "https://www.bloomberg.com/billionaires/", "https://www.gov.il/en/departments/central-elections-committee/govil-landing-page", "https://www.ice.com/report-center", "https://www.ice.com/report/10", "https://www.theice.com/index", "https://www.theice.com/products/213/WTI-Crude-Futures"]}
```
