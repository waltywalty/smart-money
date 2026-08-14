# DEPLOY.md — what is live, where, and since when

The repo is the source of truth. Cloudflare is a deployment target. Never the
reverse. If these disagree, something has gone wrong and the divergence is the
first thing to fix.

## Current

| | |
|---|---|
| Live version | **v11.4** |
| Deployed | on or before 2026-08-06T02:54Z (worker `startedAt`; the deploy itself is not timestamped by the endpoint) |
| Repo tag | none yet — tag this commit `v11.4` |
| Matches repo `worker.js` | **Yes** |

**v12.3 is no longer an open question.** It was recovered on 2026-08-13 and is archived, not
deployed. The claim that it was unrecoverable was true of the sandboxes and false of Cloudflare.

**How that was established, 2026-08-13.** Not from the dashboard. The worker reports its own
build: `VERSION` is a source constant returned as `version` by `GET /`. A raw HTTP fetch of
`https://smart-money-bot.rogerlgk.workers.dev/` returned `"version":"v11.4"`, with `runs: 2044`
and `lastRun` four minutes old, so it is the running build and not a cached page. Walton
independently read the deployed source in the Cloudflare dashboard the same day and its constant
also reads `v11.4`. The repo file was then checked against that source on the version constant and
twelve distinctive markers — `TAPE_TTL_DAYS = 60`, `HOUSE_MAX_GROSS_USD: 400`, `RADAR_MIN_SCORE:
62`, `aprPortfolioPct`, `rebateAudit`, `needN`, `tailIfShortsResolveYes`, `REBATES RESET`,
`cyclesSinceFill`, `bestNearMiss`, `unverified` — all present, all matching.

**This corrects the record.** The repo carried a warning that production ran **v11.5** and that
`worker.js` was one build behind. Three independent reads say otherwise: live is v11.4 and the repo
matches it. No evidence of a v11.5 deployment was found. The claim appears to have propagated
without ever being checked against the endpoint that answers it.

That check is twelve distinctive markers, not a byte-for-byte diff — the deployed source was read
through a chat paste, which cannot be hashed. Strong, not conclusive. A `wrangler download` would
settle it outright.

## History

| Version | Deployed | Tag | Notes |
|---|---|---|---|
| v12.3 | 2026-08-?? | — | **RECOVERED 2026-08-13** from Cloudflare's version history, which the repo never checked. Archived verbatim at `archive/worker-v12.3.js`; see `archive/WORKER-V12.3-RECOVERY.md`. **Does not run today** — its Kalshi leg reads pre-migration field names and would silently record zeros |
| v11.5 | — | — | **No evidence it was ever deployed.** The live endpoint reports v11.4 and the deployed source reads v11.4. Treat the earlier claim as unverified until Cloudflare's version list says otherwise |
| v11.4 | ≤ 2026-08-06 | — | **LIVE.** Matches repo `worker.js` (73,451 bytes) |

## Rules

1. Nothing is deployed that is not committed and tagged first.
2. Walton deploys, manually. Claude delivers `worker.js` and stops.
3. Subrequest ceiling is 50 per invocation; worst measured cycle is 22.
   Exceeding it silently kills scheduled runs and looks like a broken cron.
4. KV writes ~288/day against a ~1k/day free tier.
5. After every deploy, update this file in the same commit.
6. **Ask the worker, not the dashboard.** `GET /` returns `version` from the source constant.
   That is the cheapest true answer to "what is live", and the question that produced this
   file went unanswered for days because nobody fetched it.
