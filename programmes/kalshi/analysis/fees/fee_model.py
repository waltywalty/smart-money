#!/usr/bin/env python3
"""Kalshi fee model, rounding explicit.

A1 of task packet 3. Built from Kalshi's own documentation
(docs.kalshi.com/getting_started/fee_rounding.md, retrieved 2026-08-15),
not inferred from observed charges.

WHAT IS ESTABLISHED, and what is not:

  ESTABLISHED - the ROUNDING model. Every fill produces three components:
    trade fee     - the fee model's output, rounded UP to the nearest $0.0001
                    (a centicent). NOT to the nearest whole cent.
    rounding fee  - restores the user's target balance precision. $0.0001 for
                    direct members, $0.01 for non-direct members.
    rebate        - a per-ORDER accumulator issues a whole $0.01 rebate each
                    time accumulated rounding exceeds $0.01, "so that the total
                    fee across many small fills converges to what a single
                    equivalent fill would cost".
    net fee = trade fee + rounding fee - rebate, floored at $0.00.
  All three documented worked examples are reproduced exactly by test().

  NOT ESTABLISHED - the BASE FEE FORMULA that produces `trade fee`. The
    rounding page states a trade fee of $0.0085 for 1 contract at $0.055.
    0.07*p*(1-p) gives $0.003638, which is not that number, and no page found
    states the model. Series carry a `fee_type` ('quadratic',
    'quadratic_with_maker_fees') and a `fee_multiplier`, but the mapping from
    fee_type to a formula is undocumented in what was reachable.
    So base_fee() below is a PARAMETER, never a constant.

WHY THIS MATTERS. docs/INFRA.md records the fee as
`ceil(M*0.07*p*(1-p))` "rounded up on order total" - whole cents. The
documentation says centicents, per fill. At p=0.9561 that is $0.0030 against
$0.01, a 3.3x difference, and it falls entirely in the extreme-price band where
this project has concentrated its work. The discrepancy is recorded, not
resolved: see registry/fees/A1-FEE-ROUNDING-2026-08-15.md.
"""
import math

CENTICENT = 0.0001
PRECISION_DIRECT = 0.0001
PRECISION_NON_DIRECT = 0.01


def _ceil_to(x, step):
    """Round up to a multiple of step, with a guard against float dust."""
    return math.ceil(round(x / step, 9)) * step


def _floor_to(x, step):
    """Floor toward negative infinity to a multiple of step."""
    return math.floor(round(x / step, 9)) * step


def quadratic_base_fee(contracts, price, multiplier=1.0, rate=0.07):
    """The formula this repo has used. Rate is a PARAMETER - see module docstring.

    This is NOT verified against Kalshi's documented worked example and must not
    be treated as established. It is here so callers can state what they assumed.
    """
    return multiplier * rate * contracts * price * (1.0 - price)


def fill_fee(revenue, trade_fee_raw, accumulator, target_precision):
    """One fill. Returns (trade_fee, rounding_fee, rebate, net_fee, balance_change, accumulator).

    revenue is signed: negative for a buyer. Mechanics verbatim from the docs.
    """
    trade_fee = _ceil_to(trade_fee_raw, CENTICENT)
    raw_change = revenue - trade_fee
    balance_change = _floor_to(raw_change, target_precision)
    rounding_fee = raw_change - balance_change
    accumulator = accumulator + rounding_fee
    reported = accumulator          # docs show the accumulator BEFORE the rebate
    rebate = 0.0
    if round(accumulator, 9) > 0.01:
        rebate = 0.01
        accumulator -= 0.01
    net = max(0.0, trade_fee + rounding_fee - rebate)
    return (round(trade_fee, 6), round(rounding_fee, 6), round(rebate, 6),
            round(net, 6), round(balance_change, 6), round(accumulator, 9),
            round(reported, 9))


def order_fees(fills, target_precision=PRECISION_NON_DIRECT):
    """fills: list of (contracts, price, trade_fee_raw). One order, many fills."""
    acc, rows, total = 0.0, [], 0.0
    for contracts, price, raw in fills:
        revenue = -price * contracts
        tf, rf, rb, net, bc, acc, shown = fill_fee(revenue, raw, acc, target_precision)
        rows.append({'trade_fee': tf, 'rounding': rf, 'accumulator': shown,
                     'rebate': rb, 'net_fee': net, 'balance_change': bc})
        total += net
    return rows, round(total, 6)


def effective_per_contract(contracts, price, multiplier=1.0, rate=0.07,
                           n_fills=1, target_precision=PRECISION_NON_DIRECT,
                           regime='documented'):
    """Effective cost per contract in CENTS.

    regime='documented'  - centicent ceiling per fill, plus balance rounding and
                           the per-order accumulator. What the docs describe.
    regime='inherited'   - ceil the whole-order fee to whole cents. What
                           docs/INFRA.md records and what H64's arithmetic used.
                           Retained so the difference can be quantified.
    """
    if regime == 'inherited':
        cents = math.ceil(multiplier * rate * price * (1 - price) * contracts * 100)
        return cents / contracts
    per_fill = contracts / n_fills
    raw = quadratic_base_fee(per_fill, price, multiplier, rate)
    _, total = order_fees([(per_fill, price, raw)] * n_fills, target_precision)
    return total * 100 / contracts


def test():
    """Reproduce all three documented worked examples exactly."""
    ok = True

    # Example 1 - subpenny: buy 3 at $0.055 as three 1-lot matches.
    rows, _ = order_fees([(1, 0.055, 0.0085)] * 3)
    want = [(0.0085, 0.0065, 0.0065, 0.0, 0.0150, -0.07),
            (0.0085, 0.0065, 0.0130, 0.01, 0.0050, -0.07),
            (0.0085, 0.0065, 0.0095, 0.0, 0.0150, -0.07)]
    for i, (tf, rf, acc, rb, net, bc) in enumerate(want):
        r = rows[i]
        got = (r['trade_fee'], round(r['rounding'], 4), round(r['accumulator'], 4),
               r['rebate'], round(r['net_fee'], 4), r['balance_change'])
        if got != (tf, rf, acc, rb, net, bc):
            print('  FAIL ex1 fill %d: got %s want %s' % (i + 1, got, (tf, rf, acc, rb, net, bc)))
            ok = False

    # Example 2 - fractional: buy 0.90 at $0.50 as three 0.30-lot matches.
    rows, _ = order_fees([(0.30, 0.50, 0.0041)] * 3)
    want = [(0.0041, 0.0059, 0.0059, 0.0, 0.0100, -0.16),
            (0.0041, 0.0059, 0.0118, 0.01, 0.0000, -0.16),
            (0.0041, 0.0059, 0.0077, 0.0, 0.0100, -0.16)]
    for i, (tf, rf, acc, rb, net, bc) in enumerate(want):
        r = rows[i]
        got = (r['trade_fee'], round(r['rounding'], 4), round(r['accumulator'], 4),
               r['rebate'], round(r['net_fee'], 4), r['balance_change'])
        if got != (tf, rf, acc, rb, net, bc):
            print('  FAIL ex2 fill %d: got %s want %s' % (i + 1, got, (tf, rf, acc, rb, net, bc)))
            ok = False

    # Example 3 - combined: buy 0.09 at $0.3301 as three 0.03-lot matches.
    rows, _ = order_fees([(0.03, 0.3301, 0.0005)] * 3)
    want = [(0.0005, 0.009597, 0.009597, 0.0, 0.010097, -0.02),
            (0.0005, 0.009597, 0.019194, 0.01, 0.000097, -0.02),
            (0.0005, 0.009597, 0.018791, 0.01, 0.000097, -0.02)]
    for i, (tf, rf, acc, rb, net, bc) in enumerate(want):
        r = rows[i]
        got = (r['trade_fee'], round(r['rounding'], 6), round(r['accumulator'], 6),
               r['rebate'], round(r['net_fee'], 6), r['balance_change'])
        if got != (tf, rf, acc, rb, net, bc):
            print('  FAIL ex3 fill %d: got %s want %s' % (i + 1, got, (tf, rf, acc, rb, net, bc)))
            ok = False

    print('documented rounding examples reproduced: %s' % ('ALL 3 PASS' if ok else 'FAILURES ABOVE'))
    return ok


def table():
    sizes = [1, 5, 10, 25, 100, 500]
    prices = [0.50, 0.90, 0.95, 0.97, 0.99]
    print()
    print('Effective fee, CENTS PER CONTRACT, multiplier 1.0, rate 0.07 (rate UNVERIFIED)')
    print('One fill per order. documented = centicent ceiling; inherited = whole-cent ceiling.')
    print()
    print('%7s | %s' % ('price', ' | '.join('%13s' % ('n=%d' % s) for s in sizes)))
    print('-' * (9 + 16 * len(sizes)))
    for p in prices:
        cells = []
        for s in sizes:
            d = effective_per_contract(s, p, regime='documented')
            i = effective_per_contract(s, p, regime='inherited')
            cells.append('%6.3f/%6.3f' % (d, i))
        print('%7.2f | %s' % (p, ' | '.join('%13s' % c for c in cells)))
    print()
    print('cells are documented/inherited. The inherited column is what H64 and')
    print('docs/INFRA.md assume; it is NOT what the documentation describes.')


if __name__ == '__main__':
    test()
    table()


def fills_table():
    """A1's central question: does fragmenting an order destroy the amortisation?

    The packet's worry was that "a 100-lot filling in ten pieces that rounds ten
    times has no amortisation at all". The documented per-ORDER accumulator is
    designed precisely to prevent that. This measures whether it does.
    """
    print()
    print('Effective fee, CENTS PER CONTRACT, by order size and FILL FRAGMENTATION')
    print('multiplier 1.0, rate 0.07 (rate UNVERIFIED), non-direct member ($0.01 precision)')
    for price in (0.95, 0.97, 0.99):
        print()
        print('  price %.2f' % price)
        print('  %8s | %10s | %10s | %10s | %10s' %
              ('size', '1 fill', '5 fills', '20 fills', 'size/1 fill'))
        for n in (1, 10, 100, 500):
            row = []
            for k in (1, 5, 20):
                if k > n:
                    row.append('       n/a')
                    continue
                row.append('%10.4f' % effective_per_contract(n, price, n_fills=k))
            single = effective_per_contract(n, price, n_fills=1)
            print('  %8d | %s | %10.4f' % (n, ' | '.join(row), single))


if __name__ == '__main__':
    pass
