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
| 2026-08-24T06:08Z | ci | 125 | **118** | 7 | 0 | 0 both, 7 ci-only, 0 vm-only (vm 92.8h old) | **0** | 5157 |

<details><summary>2026-08-24T06:08Z [ci] - not 2xx (7)</summary>

- `0` https://international.tse.jus.br/en  (16 markets, $26,156)  `-`
- `403` https://www.bloomberg.com/billionaires/  (52 markets, $8,090)  `retry-after=0 server=Varnish x-served-by=cache-hhr-khhr2060021-HHR`
- `403` https://defillama.com/stablecoins  (1 markets, $0)  `cf-ray=a3002d3f0e1f08ab-LAX server=cloudflare`
- `0` https://hitsdailydouble.com/sales_plus_streaming  (1 markets, $0)  `-`
- `403` https://kenpom.com/index.php  (43 markets, $0)  `cf-ray=a3002d52684f14a7-LAX server=cloudflare`
- `403` https://www.gov.il/en/departments/central-elections-committee/govil-landing-page  (1 markets, $0)  `cf-ray=a3002d8fac0df835-LAX server=cloudflare`
- `0` https://www.hitsdailydouble.com/charts/hits-top-50  (3 markets, $0)  `-`

</details>

```b4state
{"vantage": "ci", "stamp": "2026-08-24T06:08Z", "epoch": 1787551684, "resolving": 118, "failed": ["https://defillama.com/stablecoins", "https://hitsdailydouble.com/sales_plus_streaming", "https://international.tse.jus.br/en", "https://kenpom.com/index.php", "https://www.bloomberg.com/billionaires/", "https://www.gov.il/en/departments/central-elections-committee/govil-landing-page", "https://www.hitsdailydouble.com/charts/hits-top-50"]}
```
| 2026-08-25T06:03Z | ci | 125 | **119** | 6 | 0 | 0 both, 6 ci-only, 0 vm-only (vm 116.8h old) | **0** | 5175 |

<details><summary>2026-08-25T06:03Z [ci] - not 2xx (6)</summary>

- `403` https://www.bloomberg.com/billionaires/  (52 markets, $8,090)  `retry-after=0 server=Varnish x-served-by=cache-bur-kbur8200064-BUR`
- `403` https://defillama.com/stablecoins  (1 markets, $0)  `cf-ray=a308635d4b4c2adf-LAX server=cloudflare`
- `301` https://hitsdailydouble.com/sales_plus_streaming  (1 markets, $0)  `server=Netlify`
- `403` https://kenpom.com/index.php  (43 markets, $0)  `cf-ray=a308636b0bd0490e-LAX server=cloudflare`
- `0` https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=WCSSTUS1&f=W  (1 markets, $0)  `-`
- `403` https://www.gov.il/en/departments/central-elections-committee/govil-landing-page  (1 markets, $0)  `cf-ray=a30863bbff738c16-LAX server=cloudflare`

</details>

```b4state
{"vantage": "ci", "stamp": "2026-08-25T06:03Z", "epoch": 1787637786, "resolving": 119, "failed": ["https://defillama.com/stablecoins", "https://hitsdailydouble.com/sales_plus_streaming", "https://kenpom.com/index.php", "https://www.bloomberg.com/billionaires/", "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=WCSSTUS1&f=W", "https://www.gov.il/en/departments/central-elections-committee/govil-landing-page"]}
```
| 2026-08-26T06:04Z | ci | 125 | **120** | 5 | 0 | 0 both, 5 ci-only, 0 vm-only (vm 140.8h old) | **0** | 5167 |

<details><summary>2026-08-26T06:04Z [ci] - not 2xx (5)</summary>

- `403` https://www.bloomberg.com/billionaires/  (52 markets, $8,090)  `retry-after=0 server=Varnish x-served-by=cache-iad-kcgs7200171-IAD`
- `0` https://portwatch.imf.org/pages/chokepoint4  (10 markets, $2,729)  `-`
- `403` https://defillama.com/stablecoins  (1 markets, $0)  `cf-ray=a310a38def7d81f4-IAD server=cloudflare`
- `403` https://kenpom.com/index.php  (43 markets, $0)  `cf-ray=a310a398fd059c54-IAD server=cloudflare`
- `403` https://www.gov.il/en/departments/central-elections-committee/govil-landing-page  (1 markets, $0)  `cf-ray=a310a3babea4780e-IAD server=cloudflare`

</details>

```b4state
{"vantage": "ci", "stamp": "2026-08-26T06:04Z", "epoch": 1787724286, "resolving": 120, "failed": ["https://defillama.com/stablecoins", "https://kenpom.com/index.php", "https://portwatch.imf.org/pages/chokepoint4", "https://www.bloomberg.com/billionaires/", "https://www.gov.il/en/departments/central-elections-committee/govil-landing-page"]}
```
| 2026-08-27T16:48Z | ci | 125 | **120** | 5 | 0 | 0 both, 5 ci-only, 0 vm-only (vm 175.5h old) | **0** | 5176 |

<details><summary>2026-08-27T16:48Z [ci] - not 2xx (5)</summary>

- `403` https://www.bloomberg.com/billionaires/  (52 markets, $8,090)  `retry-after=0 server=Varnish x-served-by=cache-sjc1000142-SJC`
- `403` https://defillama.com/stablecoins  (1 markets, $0)  `cf-ray=a31c8f6b7e2fdcfe-SJC server=cloudflare`
- `308` https://hitsdailydouble.com/sales_plus_streaming  (1 markets, $0)  `server=Netlify`
- `403` https://kenpom.com/index.php  (43 markets, $0)  `cf-ray=a31c8f7afe7aeb26-SJC server=cloudflare`
- `403` https://www.gov.il/en/departments/central-elections-committee/govil-landing-page  (1 markets, $0)  `cf-ray=a31c8fe26a67cefe-SJC server=cloudflare`

</details>

```b4state
{"vantage": "ci", "stamp": "2026-08-27T16:48Z", "epoch": 1787849297, "resolving": 120, "failed": ["https://defillama.com/stablecoins", "https://hitsdailydouble.com/sales_plus_streaming", "https://kenpom.com/index.php", "https://www.bloomberg.com/billionaires/", "https://www.gov.il/en/departments/central-elections-committee/govil-landing-page"]}
```
| 2026-08-28T17:42Z | ci | 125 | **113** | 12 | 0 | 0 both, 12 ci-only, 0 vm-only (vm 200.4h old) | **0** | 4908 |

<details><summary>2026-08-28T17:42Z [ci] - not 2xx (12)</summary>

- `403` https://www.ice.com/report-center  (10 markets, $2,915,972)  `cf-ray=a3251c9658e26e66-DFW server=cloudflare`
- `403` https://www.theice.com/products/213/WTI-Crude-Futures  (152 markets, $500,391)  `cf-ray=a3251cb23b10a9f5-DFW server=cloudflare`
- `403` https://www.theice.com/index  (23 markets, $104,934)  `cf-ray=a3251cb10868e95a-DFW server=cloudflare`
- `0` https://international.tse.jus.br/en  (16 markets, $26,156)  `-`
- `403` https://www.ice.com/report/10  (48 markets, $24,618)  `cf-ray=a3251c9708986c66-DFW server=cloudflare`
- `403` https://www.bloomberg.com/billionaires/  (52 markets, $8,090)  `retry-after=0 server=Varnish x-served-by=cache-dfw-kdfw8210079-DFW`
- `403` https://defillama.com/stablecoins  (1 markets, $0)  `cf-ray=a3251c0e4b77eb02-DFW server=cloudflare`
- `0` https://hitsdailydouble.com/sales_plus_streaming  (1 markets, $0)  `-`
- `403` https://kenpom.com/index.php  (43 markets, $0)  `cf-ray=a3251c22dc38b6f4-DFW server=cloudflare`
- `403` https://www.gov.il/en/departments/central-elections-committee/govil-landing-page  (1 markets, $0)  `cf-ray=a3251c942d475cf4-DFW server=cloudflare`
- `0` https://www.hitsdailydouble.com/charts/hits-top-50  (3 markets, $0)  `-`
- `0` https://www.un.org/dgacm/en/content/protocol/hshgnfa  (16 markets, $0)  `-`

</details>

```b4state
{"vantage": "ci", "stamp": "2026-08-28T17:42Z", "epoch": 1787938966, "resolving": 113, "failed": ["https://defillama.com/stablecoins", "https://hitsdailydouble.com/sales_plus_streaming", "https://international.tse.jus.br/en", "https://kenpom.com/index.php", "https://www.bloomberg.com/billionaires/", "https://www.gov.il/en/departments/central-elections-committee/govil-landing-page", "https://www.hitsdailydouble.com/charts/hits-top-50", "https://www.ice.com/report-center", "https://www.ice.com/report/10", "https://www.theice.com/index", "https://www.theice.com/products/213/WTI-Crude-Futures", "https://www.un.org/dgacm/en/content/protocol/hshgnfa"]}
```
