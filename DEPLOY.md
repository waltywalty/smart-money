# DEPLOY.md — what is live, where, and since when

The repo is the source of truth. Cloudflare is a deployment target. Never the
reverse. If these disagree, something has gone wrong and the divergence is the
first thing to fix.

## Current

| | |
|---|---|
| Live version | TBD |
| Deployed | TBD |
| Repo tag | TBD |
| Matches repo `worker.js` | TBD |

## History

| Version | Deployed | Tag | Notes |
|---|---|---|---|
| v12.3 | 2026-08-?? | — | Lost to container rollback 2026-08-10. Cloudflare version history: TBD |
| v11.5 | TBD | TBD | Was live and absent from git until TBD |
| v11.4 | — | — | Committed as history |

## Rules

1. Nothing is deployed that is not committed and tagged first.
2. Walton deploys, manually. Claude delivers `worker.js` and stops.
3. Subrequest ceiling is 50 per invocation; worst measured cycle is 22.
   Exceeding it silently kills scheduled runs and looks like a broken cron.
4. KV writes ~288/day against a ~1k/day free tier.
5. After every deploy, update this file in the same commit.
