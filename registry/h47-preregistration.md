# H47 — the strictly-more-paths leg. Pre-registration.

Written from H46's result, before any new price is fetched.

## What H46 established, and the door it left open

H46 found that on 15 of 16 cross-listed pairs the two venues' settlement criteria diverge, and that
the market prices the cross-venue BOX at roughly $1 regardless of class — so the criteria risk is
real and genuinely unpriced. It died as a trade only because the box costs above a dollar before the
divergence matters: you pay two round trips to hold it.

**A single leg pays one round trip, not two.** And the divergence is directional.

## The claim

Polymarket's descriptions carry explicit fallback clauses — resolve on the prior month if the print
is missing, count a VP tiebreak, any lapse within the day rather than a snapshot, a precedence rule
for shared prizes — where Kalshi's `rules_primary` is a single silent sentence. Those clauses give
the Polymarket YES **strictly more paths to resolving YES** than its Kalshi twin on the same fact.

**H47: where one venue's contract has strictly more winning paths than the other's on the same
underlying fact, it should trade at a HIGHER price. Where it trades at the same price or lower, the
cheaper leg is mispriced, and buying it is a single-leg trade needing no hedge.**

This is not an arbitrage and I will not present it as one. It is a directional claim with a stated
mechanism, and it is the first hypothesis in this project whose edge comes from a rulebook rather
than from a price, a feed, a model or a structure.

## The strictly-more-paths test, fixed now

A leg qualifies ONLY if its criteria are a strict SUPERSET of the twin's — every state that resolves
the twin YES also resolves this leg YES, plus at least one more. Anything requiring a judgement call
about which is broader is EXCLUDED, not guessed at. That exclusion is the whole discipline: a
superset relation is checkable, a "probably broader" is not.

## Method

- Both legs priced at the **ASK**, since that is what you can buy. H46's price leg compared a Kalshi
  ask against a Polymarket bid, which is not the same trade — this run must not repeat it.
- Depth at the touch reported beside every hit.
- Kalshi quotes verified against `/orderbook` with an explicit depth parameter; Polymarket against
  two of gamma / `/book` / `/midpoint`. Both venues' APIs fabricated quotes during H46 and were only
  caught by cross-checking.

## Bar

- At least 8 pairs with a verified strict-superset relation.
- The superset leg must be cheaper on a majority of them, and the mean gap must be material against
  the ~4c hurdle already measured.
- Depth of at least a few hundred contracts on the cheap leg, or it is the penny study again.

## What would make me abandon it

- Strict supersets are rare — most divergences are two-way, and H46 classified 7 of 16 as BOTH.
  If fewer than 8 clean supersets exist the question is moot.
- The superset leg is already dearer, meaning the rulebook is priced and H46's box result was a
  depth artifact rather than a pricing one.
- The gap exists but sits inside the spread, which is how most of this registry died.
