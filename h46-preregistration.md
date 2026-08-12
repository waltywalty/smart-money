# H46 — the same event, two rulebooks. Pre-registration.

Written before any pair is fetched.

## Why this is not a forty-sixth variation

All 45 prior hypotheses asked whether a PRICE was wrong. The answer, measured on both venues, is no:
calibration curves sit on the diagonal, the taker pays 4.03c, the maker grosses at most 1c against
adverse selection at 2.7x the spread. Looking for a mispricing in a calibrated market is finished.

H46 asks a different question. It is about the CONTRACT, not the price.

## The claim

H16 killed cross-venue arbitrage on the arithmetic: the price gap (2.46c) was smaller than the round
trip (4.83c). But that calculation assumed something never checked — that the two venues' contracts
are the SAME contract, so exactly one leg pays.

They are not the same contract. Kalshi settles on named statistical sources with explicit rounding
conventions; Polymarket settles on free-text criteria, often "as reported by credible sources", with
a default-to-NO clause on ambiguity. Where those diverge, buying YES on one venue and NO on the other
is not a riskless box. It can pay **$2** (both resolve YES) or **$0** (both resolve NO).

**H46: for cross-listed events, settlement criteria diverge often enough that both-pay and both-fail
are real outcomes, and the market prices the pair as though exactly one leg pays.**

If both-pay is more common than both-fail, the box is underpriced and buying it has positive expected
value beyond any arbitrage. If both-fail dominates, the box is a trap and the correct trade is the
reverse — which would be the first SHORT this project has found.

## Method

1. Find events listed on BOTH venues covering the same underlying fact — macro prints, elections,
   named-entity outcomes. Match on the underlying event, never on title text.
2. For each pair, extract the settlement criteria VERBATIM: Kalshi `rules_primary`, Polymarket
   `description`. **Record the divergence BEFORE looking at any price** — the same blind discipline
   that H32's scan used, because H28 and H29 both died of reading a value earlier than anyone could.
3. Classify each pair: IDENTICAL (both-pay impossible), DIVERGENT-UP (both-pay possible),
   DIVERGENT-DOWN (both-fail possible), or BOTH.
4. Only then fetch prices and compute what the box costs.

## Bar

- At least 15 cross-listed pairs with criteria read verbatim from both venues.
- The divergence classification committed before prices are seen, every time.
- To claim anything: a stated mechanism for WHY one direction dominates, not just a count.
- Depth beside every hit. A price without size is not a price and this project has paid twice.

## What would make me abandon it

- Cross-listed pairs are rare — if fewer than 15 exist, the question is moot regardless of the answer.
- Criteria are effectively identical on inspection, so exactly one leg always pays and H16's
  arithmetic was right for the right reason.
- Divergence exists but is symmetric, so both-pay and both-fail cancel and the box is fairly priced.
- **The most likely outcome and I expect it:** divergence exists, is real, and is already in the
  price — because the participants writing these boxes have read both rulebooks too.
