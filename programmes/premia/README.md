# programmes/premia - **SCOPED, NOT OPEN**

Family 4 of `ROADMAP.md`: structural risk premia - perpetual funding carry and the variance risk
premium.

**This programme is not open and no capital, account, API key or collector exists for it.** The
gate in `ROADMAP.md` - *venue access confirmed post-move, and capital deployable through the
relocation without being needed elsewhere* - is unchanged, and packet 8 did not address it.

## The verdict

| strand | verdict |
|---|---|
| **S1** perpetual funding carry | **could not establish** |
| **S2a** equity index variance risk premium | **KILL** |
| **S2b** Bitcoin variance risk premium | **could not establish** |

**Family 4 does not survive scoping.** No strand survives, and the only strand whose magnitude was
actually measurable was killed.

**Read the verdict with its caution attached:** every unestablished item is on the cost or risk
side, and the one measured thing on the return side came in at roughly a fifth of the pre-committed
floor. The verdict is agnostic; the evidence is not.

## The documents, in the order they were written

| file | what it is |
|---|---|
| `KILL-CONDITION.md` | **T1.** Sealed alone, before any source was read. Thresholds derived from this family's own cost structure. **Not to be edited** - dated amendments only |
| `PRIORS.md` | **T2.** Both strands: mechanism as a cash flow, why it persists, published magnitudes, re-estimation record |
| `MECHANICS.md` | **T3.** Venue documentation only - funding, margin, liquidation, the loss backstop, fees. Every silence named |
| `TAIL.md` | **T4.** Venue failures and loss events from primary sources; ADL and socialised loss specifically; what cannot be quantified |
| `SCOPING-VERDICT.md` | **T5.** The comparison against T1, quoted verbatim |
| `registry/F4-PREMIA-SCOPING.md` | Registry entry `F4-01`, with `revive_if` and an explicit statement of what is **not** a revive condition |
| `CLOSEOUT-PACKET8.md` | MEASURED / INFERRED / ASSUMED; the item-5 answer per strand; what is not knowable |

## The one-line finding

> **The premium was the friction.** Family 2 survived publication because it was uneconomic to
> arbitrage; perpetual funding carry persists because arbitrage capital is constrained by regulation
> and margin; the equity variance risk premium was a restriction on who could sell options, and it
> decayed to zero when the restriction eased.

## The cheapest open question

Tail frequency is recorded as could-not-establish, and that is a **scope boundary rather than a
limit of public knowledge**. Hyperliquid labels ADL fills on its public REST API and Deribit returns
`socialized` and `session_tax_rate` per settlement on a public endpoint. Neither was called, because
packet 8 forbids data pulls. See `registry/F4-PREMIA-SCOPING.md`.
