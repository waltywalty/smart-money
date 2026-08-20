# B4 - population decay log

One row per run, appended, never edited. `resolving` requires 2xx **and** a
separating control on that host. A url that quietly 404s is indistinguishable
from a source that never publishes, so the decay is dated rather than assumed.

| run (UTC) | urls | resolving | not 2xx | 2xx, control void | markets resolving | OI resolving |
|---|---:|---:|---:|---:|---:|---:|
| 2026-08-20T07:36Z | 125 | **125** | 0 | 0 | 5274 | $70,790,897 |
| 2026-08-20T08:22Z | 125 | **119** | 6 | 0 | 5173 | $70,782,807 |

<details><summary>2026-08-20T08:22Z - not 2xx (6)</summary>

- `403` https://www.bloomberg.com/billionaires/  (52 markets, $8,090)
- `403` https://defillama.com/stablecoins  (1 markets, $0)
- `0` https://hitsdailydouble.com/sales_plus_streaming  (1 markets, $0)
- `403` https://kenpom.com/index.php  (43 markets, $0)
- `403` https://www.gov.il/en/departments/central-elections-committee/govil-landing-page  (1 markets, $0)
- `0` https://www.hitsdailydouble.com/charts/hits-top-50  (3 markets, $0)

</details>
