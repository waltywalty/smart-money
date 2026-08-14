# A1 — the fee rounding rule. 2026-08-15.

Established from Kalshi's own documentation
(`docs.kalshi.com/getting_started/fee_rounding.md`, retrieved 2026-08-15 by raw HTTP from
the Kernel VM, explicit User-Agent, with an impossible-path control returning 404), not
inferred from observed charges.

**Two STOP conditions fired. Both are recorded and parked; nothing was changed.**

---

## The four questions A1 asked

**1. Is `ceil` applied per order, per fill, or per contract?**
**PER FILL — and to a centicent, not a whole cent.** Every fill produces three components:

| Component | Rule |
|---|---|
| **Trade fee** | the fee model's output, rounded **up to the nearest \$0.0001** |
| **Rounding fee** | restores the user's target balance precision — **\$0.0001 direct, \$0.01 non-direct** |
| **Rebate** | a **per-order accumulator** issues a whole \$0.01 rebate each time accumulated rounding exceeds \$0.01 |

`net fee = trade fee + rounding fee − rebate`, floored at \$0.00.

**2. Is there a minimum fee per order or trade?** No stated minimum. The effective floor for a
non-direct member is the \$0.01 balance quantum, reached through the *rounding fee* rather than
through any fee minimum.

**3. Does the maker formula round identically?** Yes. The accumulator is documented as maintained
"per order across all fills regardless of whether the fills are taker or maker", and carries over
when an order takes and then rests. Series also carry a `fee_type` — `quadratic` on KXHIGHNY and
KXATPCHALLENGERMATCH, `quadratic_with_maker_fees` on KXMLBGAME — **a field this project has never
read.**

**4. Reproduce a documented worked example.** All three reproduce **exactly**, including the
accumulator and rebate schedule: `analysis/fees/fee_model.py test()` → `ALL 3 PASS`.

---

## What this does to the amortisation thesis

The packet asked whether fragmenting an order destroys the size advantage — "a 100-lot filling in
ten pieces that rounds ten times has no amortisation at all". **It does not. The accumulator is
built to prevent exactly that**, and measurement confirms it:

```
effective cents per contract, price 0.97, multiplier 1.0
size     1 fill    5 fills   20 fills
   1     1.0000        n/a        n/a
  10     0.3000     0.3000        n/a
 100     0.2100     0.2100     0.2100
 500     0.2040     0.2040     0.2060
```

Fragmentation is free to within a rounding residual. **Size, however, matters enormously, and
only at the extremes:**

```
price    n=1      n=100    ratio
0.50   2.000¢   1.750¢    1.14x
0.90   1.000¢   0.630¢    1.59x
0.95   1.000¢   0.340¢    2.94x
0.97   1.000¢   0.210¢    4.76x
0.99   1.000¢   0.070¢   14.29x
```

At p=0.50 the theoretical fee is large and rounding is noise. At p=0.99 the theoretical fee is
0.069¢ and the \$0.01 balance quantum is **fourteen times** it. **The quantisation binds precisely
and exclusively in the extreme-price band where this project has concentrated its work** — H7, H9,
H33, H34, H53, H55, H64.

---

## STOP 1 — this contradicts a stated fact in `docs/INFRA.md`

`docs/INFRA.md` records: *"Fees: taker `ceil(M·0.07·p·(1−p))`, maker `ceil(M·0.0175·p·(1−p))`,
rounded up on order total."*

The documentation says the **trade fee** rounds up to a **centicent per fill**, and that whole-cent
behaviour comes from a *separate* balance-precision rounding fee that a per-order accumulator then
partially rebates. "Rounded up on order total" is not what the exchange describes.

**Both versions recorded. Neither built on. `docs/INFRA.md` unchanged pending Walton's ruling**,
per STOP condition 1.

## STOP 2 — and it overturns H64's stated conclusion

`registry/H64-RESULT.md` says: *"All 254 rungs were charged exactly 1 cent... because Kalshi rounds
fees up to whole cents on the order total... The cheapness this idea was reaching for does not exist
in practice."*

Three corrections, none of them applied:

1. **Nothing was "charged".** H64 was a paper study. The 1¢ was **computed by my own code** as
   `ceil(M*0.07*p*(1-p)*100)`, using the inherited INFRA.md formula. I reported a property of my
   fee function as a property of the exchange. That is the exact failure C2 exists to catch.
2. **The number happens to be right, for one contract and a non-direct member.** The documented
   model at n=1, p≈0.95 also gives 1.0000¢ — via balance rounding, not via the trade-fee ceiling.
   Right answer, wrong reason.
3. **The conclusion is wrong at size.** The "3.43× overcharge" is a one-contract artifact. At 100
   contracts and p=0.97 the ratio is **1.03×**. **The fee advantage H55 was reaching for is not
   dead — it is dead at one contract and alive at size.**

**H64's verdict, figures and text are untouched.** Its headline result — could not establish, CI
spanning zero, LOSO crossing zero, split-half failing — does not depend on the fee: correcting the
fee shifts the mean by well under the interval's half-width and changes no robustness check. What
changes is one sentence of its explanation and the whole extreme-price family's cost model.
Parked, see `PARKED.md`.

---

## What is NOT established

**The base fee formula.** The rounding page states a trade fee of **\$0.0085 for 1 contract at
\$0.055**. `0.07·p·(1−p)` gives **\$0.003638**. These do not agree and no reachable page states the
model that produces \$0.0085. Series expose `fee_type` (`quadratic`, `quadratic_with_maker_fees`)
and `fee_multiplier`, but the mapping from `fee_type` to a formula is undocumented in what was
found.

**So `0.07` is an assumption, not a measurement**, and every effective-cost figure above inherits
that. `fee_model.py` takes `rate` as a parameter and never as a constant. The *rounding* model is
established; the *formula it rounds* is not. **Could not establish**, and the shape of the table —
that quantisation binds only at the extremes and that size relieves it — holds for any small
base fee, so the qualitative finding survives the unknown.

## Deliverable

`analysis/fees/fee_model.py` — `fee(contracts, price, multiplier, side)` with rounding explicit and
the regime (`documented` / `inherited`) as a parameter, all three documented examples as unit
tests, plus the size and fragmentation tables.

## The tension, stated plainly

The size that amortises the fee is the same size that must be resting at the ask. **Fee rounding
and depth are one question asked twice**, and H64 could not answer the depth half. Nothing here is
an edge until A4 and B2 land.
