#!/usr/bin/env python3
"""Generate registry/INDEX.md from registry/hypotheses.json.

The index is generated; hypotheses.json is authoritative.
Rebuild after ANY verdict change:  python scripts/build_index.py

Schema notes (read from the real file on 2026-08-13, not guessed):

  * There is no `verdict` or `status` field that is present on every entry.
    The verdict IS THE BUCKET the entry sits in: the top-level keys
    `confirmed`, `killed`, `corrected`, `could_not_establish`, `open`,
    `parked` each hold a list of entry dicts. That is the only field that is
    100% populated and unambiguous, so the index reads the verdict from the
    bucket name and never from an entry field.
  * `id` is the only key present on all 54 entries.
  * There is no `mechanism` or `category` field anywhere in the schema.
    `state_of_play_*.the_mechanisms` is a flat list of 15 prose mechanisms
    with no per-hypothesis mapping. The topic column is therefore an
    EXPLICIT HAND-AUTHORED MAP (TOPIC below), not an extraction. It is
    labelled "topic" rather than "mechanism" so nobody mistakes it for a
    JSON field. Unmapped IDs render as "—" and are reported on stderr.
  * There is no `one_line` or `summary` field. The one-line is extracted by
    the ONE_LINE_FIELDS fallback chain below, whitespace-squeezed and
    truncated. 20 of the 45 killed entries carry their text only in
    `verdict_2026_08_10` (they were reconstructed after the 2026-08-10
    rollback and have no `claim`).
  * `method_rules_added` is a list of dicts but holds no `id` and is not a
    hypothesis bucket. It is excluded.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "registry" / "hypotheses.json"
OUT = ROOT / "registry" / "INDEX.md"

# Buckets, in the order their verdicts are printed. The bucket name is the verdict.
BUCKETS = ["confirmed", "killed", "corrected", "could_not_establish", "open", "parked"]

# Lost to the 2026-08-10 container rollback; see `_gaps` in the JSON.
LOST = ["H22", "H23", "H24", "H25", "H26", "H27", "H32", "H45"]

# First field present wins. Ordered most-specific-result first, claim last.
# The index answers "has this been tried?", so the one-line carries the CLAIM.
# The verdict column already carries the outcome; repeating it there wasted the
# width and, with the ECHO strip, left dangling conjunctions ("and it fails in
# the direction that..."). Result fields are the fallback only, for the 20
# rollback-reconstructed entries that have no `claim`.
ONE_LINE_FIELDS = [
    "claim", "why_it_matters",
    "verdict_2026_08_10", "result", "THE_KILL", "the_result_KILLS_it",
    "found", "verdict", "the_real_answer", "evidence", "status", "note",
]

# Hand-authored topic labels. Derived by reading each entry's own claim /
# verdict text; NOT present in the JSON. Keep in sync when an entry is added.
TOPIC = {
    "H1": "trade-shape", "H2": "skill-persistence", "H3": "crowd-bias",
    "H4": "news-market-making", "H5": "in-play-quoting", "H6": "maker-rebate",
    "H7": "penny-breakeven", "H8": "backtest-vs-live", "H9": "settlement-pennies",
    "H10": "boring-vs-news-mm", "H11": "fed-futures-fade", "H12": "pro-benchmark-gap",
    "H13": "funding-carry", "H14": "form4-insider-clusters", "H15": "negrisk-sum",
    "H16": "cross-venue-macro-arb", "H17": "cohort-labels", "H18": "cpi-ladder-vs-nowcast",
    "H19": "nested-ladder-monotone", "H20": "yes-no-book-mirror", "H21": "stale-enddate",
    "H28": "iem-archive-lag", "H29": "weather-settle-asym", "H30": "metar-publication-lag",
    "H31": "pm-liquidity-rewards", "H33": "tail-collateral-drag", "H34": "far-tail-bid",
    "H35": "cli-issuance-lag", "H36": "free-asos-feed", "H37": "spotmax-gap-bias",
    "H38": "weather-calibration", "H39": "last-price-instrument", "H40": "kalshi-calibration",
    "H41": "pm-calibration", "H42": "adverse-selection", "H43": "see-H10",
    "H44": "wallet-flow-skill", "H46": "settlement-divergence", "H47": "strict-superset",
    "H48": "multi-leg-payout", "H49": "non-exclusive-sum", "H50": "martingale-property",
    "H51": "h42-vs-h50", "H52": "executed-markout", "H53": "far-otm-tick-floor",
    "H54": "mass-conservation", "H55": "near-certainty-fees", "H56": "the-hurdle",
    "H57": "kxrain-overpricing", "H58": "calibration-clean-path", "H59": "pm-reversion-replication",
    "H60": "hurdle-horizon-dependent", "H61": "obtainability", "H62": "mean-reversion",
    "H63": "reversion-in-trades",
    "H64": "depth-unanswered",
    "H65": "hurdle-size-axis",
}

W_ID, W_VERDICT, W_TOPIC, W_ONE = 4, 9, 24, 42

HEADER = """# Registry index — GENERATED, do not edit by hand

Rebuild with `python scripts/build_index.py` after any verdict change.
`registry/hypotheses.json` is authoritative; where this disagrees, it is stale.
Verdict = the JSON bucket. Topic = a hand-authored label in the build script;
the schema has no mechanism field. LOST = the 2026-08-10 rollback gaps.

```
"""
FOOTER = "```\n"


def hnum(hid):
    return int("".join(c for c in hid if c.isdigit()) or 0)


# The verdict column already carries the verdict, so a leading echo of it is
# dead width on the fallback path. Strip it ONLY when what follows starts a new
# sentence — otherwise "KILLED, and the most informative death" becomes "and the
# most informative death", a dangling conjunction that reads as a fragment.
ECHO = re.compile(r"^(KILLED|CONFIRMED|CORRECTED|OPEN|UNVERIFIED|"
                  r"COULD NOT ESTABLISH)\b[\s,.:;–—-]*(?=[A-Z0-9])")

# A verdict word at the head of the `now` field, where one exists.
NOW_VERDICT = re.compile(r"^(CONFIRMED|KILLED|CORRECTED|UNVERIFIED|OPEN)\b")


def one_line(entry):
    for f in ONE_LINE_FIELDS:
        v = entry.get(f)
        if isinstance(v, str) and v.strip():
            s = ECHO.sub("", " ".join(v.split()))
            if len(s) > W_ONE:
                s = s[:W_ONE - 1].rstrip() + "…"
            return s
    return "—"


def superseded_by(entry, bucket):
    """Return the verdict named in `now`, if it contradicts the bucket.

    The registry has entries whose bucket is stale relative to their own
    `now` field — H50 sits in `killed` and reads "CONFIRMED, restored the
    same day by H62". The bucket cannot be corrected here (hypotheses.json
    is not ours to edit), so the disagreement is marked instead of hidden.
    """
    m = NOW_VERDICT.match(" ".join((entry.get("now") or "").split()))
    if m and m.group(1) != bucket.upper():
        return m.group(1)
    return None


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    rows, seen, unmapped, notes = [], set(), [], []

    for bucket in BUCKETS:
        for e in data.get(bucket, []):
            hid = e.get("id")
            if not hid:
                continue
            seen.add(hid)
            if hid not in TOPIC:
                unmapped.append(hid)
            verdict, sup = bucket.upper(), superseded_by(e, bucket)
            if sup:
                verdict += "*"
                nowtxt = " ".join(e["now"].split())
                notes.append("* %s sits in the `%s` bucket; its own `now` field reads \"%s\". "
                             "Ruled by Walton 2026-08-14: killed as a TRADE, confirmed as an "
                             "EFFECT. It stays in `killed`; see its audit_note."
                             % (hid, bucket, nowtxt[:46].rstrip() + "…"
                                if len(nowtxt) > 46 else nowtxt))
            rows.append((hnum(hid), "%-*s | %-*s | %-*s | %s" % (
                W_ID, hid, W_VERDICT, verdict,
                W_TOPIC, TOPIC.get(hid, "—"), one_line(e))))

    for hid in LOST:
        if hid in seen:
            continue
        rows.append((hnum(hid), "%-*s | %-*s | %-*s | %s" % (
            W_ID, hid, W_VERDICT, "LOST", W_TOPIC, "—",
            "rollback 2026-08-10, not reconstructed")))

    rows.sort()
    tail = FOOTER + ("\n" + "\n".join(notes) + "\n" if notes else "")
    OUT.write_text(HEADER + "\n".join(r[1] for r in rows) + "\n" + tail,
                   encoding="utf-8")

    n_sub = len(seen)
    n_lost = len(rows) - n_sub
    size = OUT.stat().st_size
    print("wrote %s — %d rows (%d substantive + %d LOST), %d bytes"
          % (OUT, len(rows), n_sub, n_lost, size))
    if unmapped:
        print("WARNING: no topic label for: %s" % ", ".join(unmapped), file=sys.stderr)
    if size > 6144:
        print("WARNING: %d bytes exceeds the 6 KB budget" % size, file=sys.stderr)


if __name__ == "__main__":
    main()
