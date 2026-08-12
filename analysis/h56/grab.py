#!/usr/bin/env python3
"""H56 collector. Raw HTTP against Kalshi - no summarising layer anywhere in the path.

Stage 1 (run once, writes markets.json): paginate settled markets per series.
Stage 2 (this file): for each market fetch the 60-min candle at the T-24h lead.

Resumable: re-running picks up from rows_partial.json. Sustainable pacing is
3 threads with a 0.55s per-request sleep; 4 threads bounces ~42% on 429.
"""
import json, urllib.request, time, calendar, threading, queue, os

B = 'https://api.elections.kalshi.com/trade-api/v2'
LOCK = threading.Lock()
ST = {'ok': 0, '429': 0, 'err': 0}


def g(u, tries=8):
    for i in range(tries):
        try:
            r = json.load(urllib.request.urlopen(B + u, timeout=40))
            with LOCK:
                ST['ok'] += 1
            return r
        except Exception as e:
            s = str(e)
            if '429' in s:                      # the exchange rate-limits, and says so
                with LOCK:
                    ST['429'] += 1
                time.sleep(1.0 * (i + 1))
                continue
            if '404' in s:
                return None
            with LOCK:
                ST['err'] += 1
            time.sleep(0.6)
            continue
    return None


def ts(x):
    return calendar.timegm(time.strptime(x[:19], '%Y-%m-%dT%H:%M:%S'))


mk = json.load(open('/tmp/h56/markets.json'))
ev = {}
for m in mk:
    ev.setdefault(m['event_ticker'], {'s': m['_series'], 'rows': []})['rows'].append(m)
for k, v in ev.items():
    v['ct'] = min(ts(r['close_time']) for r in v['rows'])

# Sample rule fixed in advance: <=30 events per series, spaced EVENLY across each
# series' time range so the sample is not concentrated in one market regime.
bys = {}
for k, v in ev.items():
    bys.setdefault(v['s'], []).append((v['ct'], k))
sel, CAP = [], 30
for s, lst in bys.items():
    lst.sort()
    if len(lst) <= CAP:
        sel += [k for _, k in lst]
    else:
        step = len(lst) / CAP
        sel += [lst[int(i * step)][1] for i in range(CAP)]
sel = set(sel)
targets = [r for k in sel for r in ev[k]['rows']]
print('SAMPLED events %d markets %d' % (len(sel), len(targets)), flush=True)
json.dump(sorted(sel), open('/tmp/h56/sampled_events.json', 'w'))

OUT = []
if os.path.exists('/tmp/h56/rows_partial.json'):
    try:
        OUT = json.load(open('/tmp/h56/rows_partial.json'))
    except Exception:
        OUT = []
done = set(r['t'] for r in OUT)
targets = [m for m in targets if m['ticker'] not in done]
print('RESUME: already have %d, fetching %d more' % (len(done), len(targets)), flush=True)

Q = queue.Queue()
for m in targets:
    Q.put(m)


def work():
    while True:
        try:
            m = Q.get_nowait()
        except queue.Empty:
            return
        ct = ts(m['close_time'])
        lead = ct - 86400
        u = ('/series/%s/markets/%s/candlesticks?start_ts=%d&end_ts=%d&period_interval=60'
             % (m['_series'], m['ticker'], lead - 7200, lead + 60))
        c = g(u)
        # end_period_ts is the INCLUSIVE END of the bucket
        ks = [k for k in ((c or {}).get('candlesticks') or []) if k.get('end_period_ts', 0) <= lead]
        row = {'t': m['ticker'], 'ev': m['event_ticker'], 's': m['_series'],
               'res': m['result'], 'close': ct, 'lead': lead, 'fetched': c is not None}
        if ks:
            k = max(ks, key=lambda x: x['end_period_ts'])
            row['off'] = lead - k['end_period_ts']
            row['ask'] = k.get('yes_ask', {}).get('close_dollars')
            row['bid'] = k.get('yes_bid', {}).get('close_dollars')
            row['vol'] = k.get('volume_fp')
        with LOCK:
            OUT.append(row)
            n = len(OUT)
            if n % 100 == 0:
                print('%d/%d ok=%d 429=%d err=%d' % (n, len(targets), ST['ok'], ST['429'], ST['err']), flush=True)
            if n % 200 == 0:
                json.dump(OUT, open('/tmp/h56/rows_partial.json', 'w'))
        time.sleep(0.55)


ths = [threading.Thread(target=work) for _ in range(3)]
[t.start() for t in ths]
[t.join() for t in ths]
json.dump(OUT, open('/tmp/h56/rows.json', 'w'))
print('DONE rows %d stats %s' % (len(OUT), ST), flush=True)
