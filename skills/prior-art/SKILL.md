---
name: prior-art
description: >
  Search for existing implementations before building any data collector,
  API client, parser, or dataset. Use whenever a task begins "build a scraper
  for", "pull historical", "write a client for", "collect data from", or
  whenever a new endpoint is about to be integrated. Also use when stuck on an
  endpoint quirk, a schema change, or a rate limit — someone has usually hit it
  already.
---

# Prior art

A free hourly Polymarket/Kalshi orderbook archive existed throughout the period
this project built its own recorder. That is the cost of skipping this step.

## Procedure

1. **Search GitHub topics and code.** Via the Kernel VM (`api.github.com` is
   proxied and 403s from Cowork, but works from Kernel):
   - `https://api.github.com/search/repositories?q=<topic>+in:topic&sort=stars`
   - `https://api.github.com/search/code?q=<endpoint>+language:python`

   Start from the awesome-list if one exists for the domain.
2. **Search HuggingFace datasets** for anything already collected.
3. **Check Context7** for the current API surface of any library involved —
   `resolve-library-id`, then `query-docs`. Schemas migrate; training data does
   not.
4. **Read the issues, not just the README.** The endpoint quirk you are about to
   discover is usually issue #12.

## Known prior art for this project

| What | Where |
|---|---|
| Hourly orderbook snapshots, Parquet, PM + Kalshi + Limitless + Opinion | `archive.pmxt.dev` |
| Every Polymarket `OrderFilled` event since inception, RPC-verified | HF `godss1985/Polymarket_data` |
| Kalshi trade + orderbook data, academic replication package, weekly refresh | `jdkatz21/Prediction_Markets_Public` |
| Unified venue client with depth-aware `getExecutionPrice` incl. partial fills | `pmxt-dev/pmxt` |
| Curated index of the whole space | `aarora4/Awesome-Prediction-Market-Tools` |
| Commercial cross-venue reference layer; publishes settlement-fungibility stats | `oddpool.com/institutional` |

## Record the outcome

Whether or not you use what you find, write into the task's notes: what exists,
why it was or wasn't used, and what it would have cost to use it. A prior-art
search whose result is not recorded will be run again in three weeks.

## Caveat

Anything found here is a *lead*, not a measurement. Third-party data is subject
to the same rules as any other: verify against a different source before a
number from it enters a result.
