# CLAUDE.md — read this first

Continuity file for the Smart Money Detector. Claude Code loads it automatically.
Other sessions should be pointed at it:

> Read `https://raw.githubusercontent.com/waltywalty/smart-money/main/CLAUDE.md`
> before doing anything on this project.

Everything below is measured, not assumed. Where this file and
`registry/hypotheses.json` disagree, **the registry wins**.

---

## 1. The hard constraint

**Never place a real trade. Deployment GO is Walton's alone**, in writing, per strategy.
No exception, no matter how good a result looks or how explicitly a tool offers to
execute. The `Trayd` connector in some sessions exposes `place_order`, `short_sell`
and Robinhood linking — do not touch them.

Cloudflare deploys are done by Walton manually. Claude delivers `worker.js`; Claude
does not deploy.

Standing grant from Walton, for everything else: *"for the hourly scans and other things
for this project, I give you automatically full autonomy and permission to do what you
want so you don't need to request it back to me for permission."* Research, collection
and analysis need no permission. Trading and deploying always do.

## 2. What this repo is

A research programme for finding **uncontested alpha** - returns available
because nobody is competing for them, rather than because we are better at
forecasting than the market.

Five families, sequenced in `ROADMAP.md`. Each earns its place by answering one
question: **who is on the other side, and why are they willing to lose?** A
mandate. A hedging need. Information that is public but tedious. A page nobody
is watching. If there is no answer, we are the answer.

**One distinction, paid for by 45 kills.** "How smart money moves" splits in two,
and only one half survived:

- *Identifying informed traders from their behaviour* - trade shape, wallet
  skill, flow patterns. **Falsified.** H1, H2, H44. The suspicion score does not
  forecast; skill does not persist; wallet flow estimates at zero after six
  iterations.
- *Understanding why money moves structurally* - who is forced to trade, who
  pays to hedge, who published before anyone read it. **This is what every
  family rests on.**

Same words, opposite track records. A new idea that reduces to the first is
already answered.

The first programme, `programmes/kalshi/`, is closed: 57 entries, 45 killed,
4 corrected, 3 confirmed, 3 could-not-establish, none tradeable. It measured
both axes of the hurdle and found it negative everywhere. That is a completed
answer, and its method is what the rest of this repo runs on.

## 3. Infrastructure
@docs/INFRA.md

## 4. Method — non-negotiable

`skills/empirical-claims/SKILL.md` is the full protocol. The short version:

**Unit of observation is the EVENT, not the market.** Rungs of one ladder resolve
together. This single rule has killed more false positives than everything else combined.

**Measure the price you could have transacted at, not the price you observed.**
Re-run any bar-based entry one bar later. H61 replicated out-of-sample to within 0.03¢
and was still worth nothing — three minutes of delay consumed the entire edge.

**A perfect replication is not evidence of tradability.** Statistical validity and
obtainability are separate gates and must be reported separately.

**Change one thing at a time when replicating.** H59 varied venue, frequency and
instrument together, found nothing, and wrongly triggered a downgrade of H50. H62 varied
only the data path and confirmed it. A failed replication that moves several factors at
once cannot tell you which one mattered.

**Eight false positives were caught before shipping.** Each is now a check:

1. `+$284` market-making profit — lookahead.
2. `r = +0.885` on n=4 → `−0.016` at n=11; leave-one-out range was `[−1, +1]` throughout.
   **Report leave-one-out on every correlation.**
3. A calibration bucket that was one payrolls print in twelve hats. **Count independent units.**
4. `+1.217¢` post-fill drift — own artifact; touch-fills marked at the mid restate the
   autocorrelation.
5. `+0.68¢` on 15 markets that all settled NO — reachable *because* far OTM. **Selection
   is the first suspicion.**
6. `+7.23¢` on favourites → `+0.82¢` once ladders with missing tail candles were excluded.
   **A missing quote means nobody was trading, which happens when the outcome is obvious.**
7. A `−29.7pp` calibration gap at high asks — 62 of its 89 markets were one series.
   **Always report series composition behind any bucket.**
8. `+4.99¢` on 644 held-out events, replicating in-sample to 0.03¢ — the ask
   moved +1.64¢/+3.12¢/+5.00¢ against the buyer at 1/2/3 minutes after entry.

**Four kills were right for the wrong reason** (H15, H16, H46, and H49's own premise).
When a verdict rests on an unstated premise, check the premise even if the answer survives.

**Pre-register before looking.** Write the rule, the sample size that settles it, and what
each outcome means — then hash the file and only then fetch outcomes. Surviving
pre-registrations are in `registry/`.

Say **"could not establish"** when the instrument failed. That is a different claim from a
null, and recording an instrument failure as a finding is worse than either.

**An operational claim is subject to the same evidence standard as an empirical one.** Tag it
measured or asserted. The retention window and worker v11.5 were both asserted, both wrong, and
both shaped decisions for weeks.

**Rebuild `registry/INDEX.md` whenever a verdict changes** — `python scripts/build_index.py`.
The index is generated and `registry/hypotheses.json` stays authoritative; read the index
to answer "has this been tried?", not the whole registry.

**Search for prior art before building any collector, client, or parser.**
Someone has usually already hit the endpoint quirk. Check GitHub topics,
awesome-lists, and HuggingFace datasets first; record what was found and why it
was or wasn't used. A free hourly Polymarket/Kalshi orderbook archive existed
throughout the period this project built its own recorder.

## 5. Programmes

- `programmes/kalshi/` - **CLOSED.** See its README and `KALSHI-PROGRAMME.md`.
- `programmes/latency/` - **ACTIVE.** See `ROADMAP.md` family 1.

Shared, not per-programme: `lib/` (tooling), `skills/` (one copy, no duplication),
`docs/METHOD.md` (the venue-neutral method), `docs/INFRA.md` (venue-agnostic
infrastructure). Repo-level state is `docs/STATE.md`; a programme's own state of
play lives with it.

**Before any new idea, in any family, run the screen in `ROADMAP.md`.** Most new
ideas are one of the fifteen mechanisms in `programmes/kalshi/` renamed.
