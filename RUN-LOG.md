# RUN-LOG — autonomous run, task packet 3

Append-only. One block per session. Newest at the bottom.

---

## Session 1 — 2026-08-15 06:05 UTC

**Constitution re-read:** yes — `CLAUDE.md` §4 and `skills/empirical-claims/SKILL.md`
Part 1 (all eleven rules, including 10 and 11 added on 2026-08-14).

**Resumed at:** run start. No prior RUN-LOG existed.

**Completed this session:** *(updated as work lands)*
- Direct commit path established and **proven by a real write**, not by the
  `permissions.push` field. `scripts/gh_commit.py check` reports
  `200 waltywalty/smart-money push=True`, and `scripts/gh_commit.py` was itself
  committed as `f4557da`. That field reflects the USER's repo access rather than the
  token's and misled this project on 2026-08-12, when a PAT reporting `push=True`
  returned 403 on the first blob POST. The only proof of write access is a write.
  **The patch-and-apply cycle is retired.**
- Token held as `GH_TOKEN` in the VM environment, mode 600, outside the repo, never
  printed and never committed. Deviation flagged to Walton: it is sourced from a
  mode-600 file in the VM rather than held only in memory, because `exec_command`
  starts a fresh login shell per call and passing it inline would place it in the
  conversation on every commit — more exposure, not less.

**Parked this session:** none yet.

**STOP conditions hit:** none.

**Next action:** A1 — establish Kalshi's fee rounding rule from documentation
(per order / per fill / per contract), find and reproduce a worked example, then build
`analysis/fees/fee-model.py`.

**Completed this session (A1):**
- **A1 done.** Fee rounding established from Kalshi documentation, not inference. Trade fee
  rounds up to a **centicent per fill**, not a whole cent; whole-cent behaviour comes from a
  separate balance-precision rounding fee that a **per-order accumulator** rebates. All three
  documented worked examples reproduce exactly.
- **Fragmentation does not destroy amortisation** — 100 contracts at p=0.97 cost 0.2100¢ each
  whether filled in 1, 5 or 20 pieces. **Size does matter, and only at the extremes**: 1 contract
  is 1.0000¢ at any price above 0.9, against 0.2100¢ at 100 contracts (p=0.97) and 0.0700¢
  (p=0.99). At p=0.50 the ratio is 1.14×.
- Delivered `analysis/fees/fee_model.py` (rounding regime a parameter, documented examples as
  unit tests) and `registry/fees/A1-FEE-ROUNDING-2026-08-15.md`.
- Base fee formula **could not be established** — the docs example gives \$0.0085 for 1 contract
  at \$0.055 against \$0.003638 from `0.07·p·(1−p)`. `rate` left a parameter everywhere.

**Parked this session:** P1–P5 → `PARKED.md`.

**STOP conditions hit:**
- **STOP 1** — A1 contradicts `docs/INFRA.md` ("rounded up on order total"). Both versions
  recorded, neither built on, INFRA.md unchanged.
- **STOP 2** — A1 overturns H64's stated fee conclusion. H64's verdict and figures untouched;
  its result does not depend on the fee.

**Next action:** A2 — depth-probe `/historical` per series for the earliest reachable settled
market, re-derive the 2026-06-07→06-11 window from `/historical` and compare against the live
path's 4,787 events, check field parity (`fee_multiplier` especially), and candlestick reach.
Deliver `registry/historical/REACH-2026-08-15.md`.
