#!/usr/bin/env python3
"""H56 - implements the sealed pre-registration exactly. Fixed seed.
Input: rows.json from grab.py.  Output: the primary statistic + 4 robustness checks."""
import json, math, random
from collections import defaultdict

random.seed(20260812)                      # fixed in advance
rows = json.load(open('rows.json'))
print('rows fetched:', len(rows))
print('fetch failures:', sum(1 for r in rows if not r.get('fetched')))
print('no candle at lead:', sum(1 for r in rows if 'ask' not in r))


def cents(x):
    try:
        return round(float(x) * 100)
    except Exception:
        return None


# ---- the pre-registered entry rule ----
Q = []
for r in rows:
    if 'ask' not in r:
        continue
    if r.get('off') is None or r['off'] > 3600:     # candle must be within 1h of the lead
        continue
    a = cents(r['ask'])
    if a is None or a <= 0 or a >= 100:             # 0 or 100 is not a tradeable quote
        continue
    fee = math.ceil(0.07 * (a / 100) * (1 - a / 100) * 100)     # Kalshi taker
    pnl = (100 if r['res'] == 'yes' else 0) - a - fee
    Q.append({'ev': r['ev'], 's': r['s'], 'ask': a, 'pnl': pnl, 'yes': r['res'] == 'yes'})
print('qualifying markets:', len(Q))

# ---- unit of observation = THE EVENT (rungs of one ladder resolve together) ----
ev = defaultdict(list)
for q in Q:
    ev[q['ev']].append(q)
EV = [{'ev': k, 's': v[0]['s'], 'n': len(v),
       'pnl': sum(x['pnl'] for x in v) / len(v),
       'ask': sum(x['ask'] for x in v) / len(v)} for k, v in ev.items()]
print('independent events:', len(EV))
if len(EV) < 150:
    print('*** BELOW PRE-REGISTERED MINIMUM 150 -> COULD NOT ESTABLISH ***')


def boot(vals, B=10000):
    n = len(vals)
    m = sum(vals) / n
    s = sorted(sum(vals[random.randrange(n)] for _ in range(n)) / n for _ in range(B))
    return m, s[int(.025 * B)], s[int(.975 * B)]


P = [e['pnl'] for e in EV]
m, lo, hi = boot(P)
print()
print('=' * 66)
print('PRIMARY  mean P&L per event  %+.2fc  95%% CI [%+.2f, %+.2f]  n=%d' % (m, lo, hi, len(EV)))
print('         prior              -4.03c  95%% CI [-7.40, -0.70]  n=41')
print('=' * 66)
verdict = ('HURDLE CONFIRMED' if hi < 0 else
           'BUYING AT ASK PAYS' if lo > 0 else
           'SPANS ZERO - HURDLE NOT ESTABLISHED')
print('VERDICT:', verdict)
print()

# ---- R1: equal-weight by market ----
mm, ml, mh = boot([q['pnl'] for q in Q])
print('R1 equal-weight by MARKET  %+.2fc [%+.2f, %+.2f] n=%d' % (mm, ml, mh, len(Q)))

# ---- R2: the H54 candle-availability selection check ----
totr, qr = defaultdict(int), defaultdict(int)
for r in rows:
    totr[r['ev']] += 1
for q in Q:
    qr[q['ev']] += 1
comp = [e for e in EV if totr[e['ev']] == qr[e['ev']]]
if len(comp) >= 30:
    cm, cl, ch = boot([e['pnl'] for e in comp])
    print('R2 every-rung-quoted events %+.2fc [%+.2f, %+.2f] n=%d' % (cm, cl, ch, len(comp)))
else:
    print('R2 too few complete events (%d)' % len(comp))

# ---- R3: leave-one-series-out ----
print('R3 leave-one-series-out:')
ser = sorted(set(e['s'] for e in EV))
lor = []
for s in ser:
    v = [e['pnl'] for e in EV if e['s'] != s]
    if len(v) > 30:
        mv = sum(v) / len(v)
        lor.append(mv)
        print('    without %-13s %+.2fc (n=%d)' % (s, mv, len(v)))
if lor:
    print('    RANGE %+.2f to %+.2f  %s' % (min(lor), max(lor),
          'STABLE' if min(lor) * max(lor) > 0 else '*** SIGN FLIPS ***'))

# ---- R4: concentration ----
tot = sum(P)
if tot:
    big = max(EV, key=lambda e: abs(e['pnl']))
    print('R4 largest single event %.1f%% of total P&L' % (100 * big['pnl'] / tot))

print()
print('per-series:')
for s in ser:
    v = [e['pnl'] for e in EV if e['s'] == s]
    if v:
        print('   %-14s %+7.2fc n=%3d meanask %.0fc' % (
            s, sum(v) / len(v), len(v),
            sum(e['ask'] for e in EV if e['s'] == s) / len(v)))

json.dump({'mean': m, 'lo': lo, 'hi': hi, 'n': len(EV), 'verdict': verdict},
          open('result.json', 'w'))
