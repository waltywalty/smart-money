# STATE.md — rewritten every session

Last updated: 2026-08-13 by Cowork
This file is the fast-changing third of the project. If it disagrees with
`registry/hypotheses.json`, the registry wins.

## 5. State of play

- **45 killed, 4 corrected, 2 confirmed, 1 open, 2 could-not-establish.** Numbering gaps at
  H22–H27, H32, H45 were lost to a rollback and are recorded as lost, not reconstructed.
- **The one confirmed effect.** Hourly prices mean-revert on Kalshi: lag-1 autocorrelation
  **−0.1896, 95% CI [−0.2147, −0.1650]**, over 90 markets and 87,315 candles, measured on a
  raw-HTTP path that cannot fabricate (H62). Negative in 88 of 90 markets, stable under
  leave-one-market-out and leave-one-series-out, and present independently in the bid and the
  ask. It is **not tradeable**: expected reversion is 0.146¢ against a spread of 1.3¢ at the
  very best — roughly 9× short of covering a single crossing. Scope is Kalshi at an hourly
  horizon; it is absent on Polymarket at 5 minutes (H59).
- **H50 is restored to CONFIRMED**, having spent part of 2026-08-13 wrongly marked UNVERIFIED.
  Cite H62's figures, never the original −0.2472 [−0.3471, −0.1416] on n=19 — that stands as
  the first observation, superseded in precision. H59 is a scope limit, not a refutation.
- **H60 is the other confirmed result.** The cost of crossing is horizon-dependent, roughly
  halving between a 24-hour and a 10-minute lead — a property of the exchange, not an edge.
- **H61 is the sharpest lesson**: a real, out-of-sample-replicated ~5¢ effect that is
  unobtainable, needing sub-60-second detect-to-fill against a 5-minute cron. Walton decided
  on 2026-08-13 not to invest in latency infrastructure; the line stays closed.
- **H58 is the only open lead** — H40's calibration curve re-run on the clean path.
  H55 and H57 are could-not-establish: their samples do not exist, which is a calendar
  problem rather than a compute one. Neither may be carried as a live lead.
- Fifteen mechanisms explain all the kills — see `state_of_play_*.the_mechanisms` in the
  registry. Read them before proposing anything; most new ideas are one of them renamed.

## 6. Two external doors, still unopened

- A **MADIS data application** (free form) — the one demonstrated timing edge needs it.
- An **SEC / Dune bulk pull**.

## 7. Housekeeping

Scheduled tasks exist including `Smart Money autonomous` (`3 */3 * * *`) and a weekly deep
dive. An hourly whale/insider scan and several stale one-shot reminders are also live and
could be cleaned up. A trigger for an H32 tornado-count re-check fires 2026-09-02T14:00Z.
