# H48 — the ladder that is not a partition. Pre-registration.

Written from H47's structural finding, before the sum is computed.

## The fact H47 established

Kalshi's `KXNOBELPEACE` legs read, verbatim, a bare "If X wins the 2026 Nobel Peace Prize, then the
market resolves to Yes" — with **no mutual-exclusivity clause**. Polymarket's twin explicitly forces
a shared prize to a single winner via a precedence list. So on Kalshi, if the prize is shared, EVERY
listed co-laureate's leg pays $1.

That means the Kalshi ladder is **not a partition**. Its YES probabilities should sum to

    1 + P(shared prize) x E[extra listed laureates | shared]

and not to 1.

## The claim

**H48: Kalshi ladders lacking a mutual-exclusivity clause can pay multiple legs simultaneously, and
the market prices them as though exactly one can win.**

If the ladder sums to ~1.00, it is underpriced by the whole shared-prize term, and buying the set is
positive expected value. If it sums visibly above 1.00, the multi-winner risk is already in the
price and this dies.

This matters beyond the Nobel: **H15 scanned negRisk sets on the premise that at most one outcome
wins, and concluded a short receiving more than $1 is riskless whatever the exhaustiveness.** That
premise is false for any set without an exclusivity clause. A short would be uncapped, not capped at
$1. H15's kill may be right for the wrong reason, exactly as H16's was.

## The base rate, stated before the sum is seen

The Nobel Peace Prize is shared among two or more laureates in a substantial minority of years — I
will take the actual historical frequency from the Nobel Foundation's own record rather than assert
one here, and I will state it before comparing to any price.

## Bar

- The ladder's sum of asks and sum of bids, both computed, with the count of legs.
- The historical shared-prize frequency from a citable source, fetched independently.
- To claim anything: `sum(asks) < 1 + P(shared)` by a margin exceeding the ~4c hurdle already
  measured, AND depth on enough legs to actually buy the set.
- Kalshi's "Other/Field" leg, if one exists, must be handled explicitly — it changes what the sum
  means.

## What would make me abandon it

- The ladder sums well above 1.00 → multi-winner is priced.
- Kalshi's ladder carries an exclusivity clause elsewhere (in `rules_secondary`, or in the event
  metadata) that H47's read of `rules_primary` missed. **This is the most likely failure and it must
  be checked first**, because a single sentence in a field I have not read would void the entire
  hypothesis.
- The listed candidates are individually so unlikely that the shared-prize term is negligible against
  the spread.
