"""Rejection over time in blocks of 20 SWEEPS, not blocks of wall-clock time.

The first pass split the run into four equal time quarters and one quarter came back
0/0 - because the VM was suspended for a single 1,808s gap, so a whole time-quarter
contained no requests at all.  Splitting by sweep index is immune to that: it counts
requests, which is what a rejection curve is a function of.  Wall-clock quarters were
measuring the scheduler, not the host.

Arm A (1 url per host per sweep) and arm B (wunderground, 6 urls per sweep) are reported
separately: arm B is the many-urls-per-host case and carries 6x the per-host rate.
"""
import json,collections
rows=[json.loads(l) for l in open('b2/sustained.jsonl')]
def host(u):
    i=u.index('/',8); return u[:i].replace('https://','')
BAD={0,429,503,-1}
mx=max(r['sweep'] for r in rows); B=20
for arm in ('A','B'):
    sub=[r for r in rows if r['arm']==arm]
    if not sub: continue
    hosts=sorted({host(r['url']) for r in sub})
    print('=== ARM %s === %d requests over %d sweeps, %d host(s)'%(arm,len(sub),mx,len(hosts)))
    hdr=' | '.join('%-9s'%('sw %d-%d'%(lo,min(lo+B-1,mx))) for lo in range(1,mx+1,B))
    print('%-30s %s'%('host',hdr))
    for h in hosts:
        cells=[]
        for lo in range(1,mx+1,B):
            hi=min(lo+B-1,mx)
            c=collections.Counter(r['code'] for r in sub if host(r['url'])==h and lo<=r['sweep']<=hi)
            n=sum(c.values())
            refused=sum(v for k,v in c.items() if k in BAD)
            blocked=c.get(403,0)
            if n==0: cells.append('%-9s'%'-')
            elif blocked: cells.append('%-9s'%('403x%d/%d'%(blocked,n)))
            elif refused: cells.append('%-9s'%('REF%d/%d'%(refused,n)))
            else: cells.append('%-9s'%('ok %d'%n))
        print('%-30s %s'%(h[:30],' | '.join(cells)))
    print()
print('legend: "ok N" = every request 2xx/3xx or a 404 control; "403xN/M" = path block;')
print('        "REFn/M" = n of M were 429/503/transport-failure.')
print()
first_bad={}
for r in sorted(rows,key=lambda r:r['sweep']):
    h=host(r['url'])
    if r['code'] in BAD or r['code']==403:
        first_bad.setdefault(h,(r['sweep'],r['code']))
print('first refusal per host (sweep, code) - request-1 means a block, later means a curve:')
for h,(s,c) in sorted(first_bad.items()): print('   %-30s sweep %-4d code %s  %s'%(h[:30],s,c,'BLOCK - refused from the first request' if s<=2 else 'refused after %d sweeps'%s))
none_bad=sorted({host(r['url']) for r in rows}-set(first_bad))
print('   hosts that never refused:',', '.join(h[:28] for h in none_bad))
