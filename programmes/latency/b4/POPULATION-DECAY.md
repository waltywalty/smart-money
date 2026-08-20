# B4 - population decay log

One row per run, appended, never edited. `resolving` requires 2xx **and** a
separating control on that host. A url that quietly 404s is indistinguishable
from a source that never publishes, so the decay is dated rather than assumed.


> **Vantage note, added 2026-08-20 after run #2.** Rows are **only comparable within the
> same vantage.** Run #1 (research VM) reported 125 of 125 resolving; run #2 (GitHub CI
> runner) reported 119, and **all six "failures" returned 200 or 206 from the VM minutes
> later** - `bloomberg.com/billionaires` 403->206, `defillama.com/stablecoins` 403->200,
> `kenpom.com` 403->200, `gov.il` 403->200, `hitsdailydouble.com` (x2) transport-fail->200.
> Shared runner IPs are refused by anti-bot layers that do not refuse the VM. **A persistent
> 403 is exactly what real rot looks like**, so a url counts as decayed only when it fails
> from **both** vantages. The two rows below predate the `from` column: row 1 is `vm`,
> row 2 is `ci`.

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
