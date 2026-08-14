# worker v12.3 — recovered 2026-08-13

`worker-v12.3.js` in this directory is the build the repo recorded as **permanently lost**.
Walton found it in Cloudflare's own version history and supplied it on 2026-08-13. It is stored
here **byte-identical to what he supplied** — sha256 `db26c93bcfd351bc547c0ab7f090518b8f4fc3918efce297f974f7c9f48c4d9f`,
115,115 bytes. Nothing in it has been edited.

**It is not `worker.js` and must not be made `worker.js`.** Live is v11.4, and the repo's
`worker.js` matches live — that invariant is the point of `DEPLOY.md`. This is an archived
artifact, and it does not run today (see the defect below).

## What the record said, and what was actually true

`registry/hypotheses.json` `_gaps` and `CLAUDE.md` both recorded v12.3 as lost to the 2026-08-10
container rollback and unrecoverable. That was true *of the sandboxes*, and the claim was
generalised past its evidence. **Cloudflare kept its own version history and nobody looked for
three days.** The lesson is not about Cloudflare; it is that "unrecoverable" was asserted about
one storage location and then written down as a fact about the world.

## What is in it

623 lines added against v11.4, 14 removed. Almost purely additive; no top-level function was
renamed or deleted.

| Addition | What it is |
|---|---|
| **Kalshi leg on the tape recorder** | The point-in-time recorder captures **both venues on the same clock, in the same KV shard**, for one extra subrequest and no extra write. Built to catch a post-surprise cross-venue lag that snapshot-when-someone-looks can never see. |
| **H23 forward recording** (§5i) | Writes met.no forecasts into the same tape as prices, for four cities with the station coordinates Kalshi actually settles on — Central Park, Midway, Denver Intl, Sky Harbor. |
| **H23 backtest** (§5j) | The bigger find. It records that **IEM archives NWS MOS guidance by station and run time**, and that those station IDs are the exact gauges Kalshi settles against, so the forecast-vs-market question is testable on *history* rather than needing a month of forward recording. It notes IEM's daily maxima matched Kalshi's own `expiration_value` exactly on every day checked. |
| **negRisk set scanner** (§5e) | H15, with an asymmetry the first version had backwards. |

**H23 is one of the hypotheses `_gaps` lists as lost and unreconstructable (H22–H27).** Its
implementation and its reasoning survive here in full. That does not un-lose the *result*, but the
method is no longer gone, and `_gaps` should not be read as if it were.

## The defect that stops it deploying — measured, not assumed

**v12.3's Kalshi leg reads field names that no longer exist.** Kalshi migrated its market schema;
`yes_bid`, `yes_ask` and `volume` are absent from the response today. Checked against the live API
on 2026-08-13 (`GET /markets?series_ticker=KXFED&status=open`, raw HTTP from the Kernel VM):

```
yes_bid            present=False
yes_ask            present=False
volume             present=False
yes_bid_dollars    present=True   0.1700
yes_ask_dollars    present=True   0.3300
volume_fp          present=True   10251.97
```

The three reads at lines 961–963 are `r.yes_bid`, `r.yes_ask`, `r.volume`. Each returns
`undefined`, and the normaliser directly above them —

```js
const px = v => { const n = parseFloat(v); if (!Number.isFinite(n)) return 0; return n >= 1 ? n / 100 : n; };
```

— converts `undefined` to **0** rather than failing.

**So the recorder would write a complete, well-formed, 60-day Kalshi tape of nothing but zeros,
and report no error.** That is the same failure this whole project was built around — a
plausible-looking value invented where a measurement should be — except it would be our own code
doing it, into an archive that would then be trusted. The "do not deploy without checking" warning
was right, and this is what it was protecting against.

**A second, subtler one comes free with the fix.** `px()` maps anything `>= 1` from cents to
probability. That was correct for the integer-cent fields it was written against. The `_dollars`
fields are already probabilities, so a contract quoted at **$1.00 would be recorded as 1¢**. The
comment beside it says the ambiguous case "does not occur as a live quote" — true of the old
schema, false of the new one.

The candlestick paths are unaffected: `yes_bid.close_dollars` / `yes_ask.close_dollars` at lines
1057–1058 and 1483 are still correct, because Kalshi's candlestick schema did not migrate. So the
H23 backtest reads a field set that still exists; only the tape leg is broken.

**Not fixed here, deliberately.** This file is preserved as recovered. Any repair belongs in a new
version, written and tested on its own terms, and deployed by Walton in writing.

## If v12.3 is ever revived

1. `r.yes_bid` → `r.yes_bid_dollars`, `r.yes_ask` → `r.yes_ask_dollars`, `r.volume` → `r.volume_fp`.
2. Make `px()` schema-aware, or drop it — the `_dollars` fields need no normalisation, and the
   cents branch is now a bug at the $1.00 boundary.
3. Re-check every other Kalshi field it touches against the live API before trusting any of them.
   Two were found by looking; the file has not been audited line by line.
4. Bump `VERSION`. A build that reports a version it is not is worse than no version at all.
