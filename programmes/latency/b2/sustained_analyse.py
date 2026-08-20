import json,collections
rows=[json.loads(l) for l in open('b2/sustained.jsonl')]
ts=sorted(r['ts'] for r in rows); t0,t1=ts[0],ts[-1]
sw=sorted({r['sweep'] for r in rows})
print('SUSTAINED POLLING  %.0fs (%.1f min), %d sweeps, %d requests'%(t1-t0,(t1-t0)/60,len(sw),len(rows)))
print('achieved cadence %.1fs per sweep - the design was 9.0s.  See the note below.'%((t1-t0)/max(1,len(sw)-1)))
print()
B=collections.defaultdict(collections.Counter); N=collections.Counter()
for r in rows:
    u=r['url']; i=u.index('/',8); h=u[:i].replace('https://','')
    B[h][r['code']]+=1; N[h]+=1
print('%-32s %6s %10s  %s'%('host','reqs','1 per Ns','status codes'))
for h in sorted(N,key=lambda h:-N[h]):
    print('%-32s %6d %9.1fs  %s'%(h[:32],N[h],(t1-t0)/N[h],dict(sorted(B[h].items()))))
print()
Q=4
print('rejection over time - requests split into %d equal quarters of the run:'%Q)
print('%-32s %s'%('host',' | '.join('Q%d'%(i+1) for i in range(Q))))
for h in sorted(N,key=lambda h:-N[h]):
    cells=[]
    for q in range(Q):
        lo=t0+(t1-t0)*q/Q; hi=t0+(t1-t0)*(q+1)/Q
        c=collections.Counter(r['code'] for r in rows if lo<=r['ts']<=hi and r['url'].split('/')[2]==h.split('/')[0])
        bad=sum(v for k,v in c.items() if k in (0,429,403,503,-1)); tot=sum(c.values())
        cells.append('%3d/%-3d'%(bad,tot))
    print('%-32s %s'%(h[:32],' | '.join(cells)))
print()
ra=[r for r in rows if r.get('retry_after')]; rl=[r for r in rows if r.get('ratelimit')]
print('Retry-After headers seen: %d      RateLimit headers seen: %d'%(len(ra),len(rl)))
sl=collections.defaultdict(list)
for r in rows:
    if r.get('t') is not None and r['code']==200:
        u=r['url']; i=u.index('/',8); sl[u[:i].replace('https://','')].append((r['ts'],r['t']))
print()
print('fetch-time drift, first quarter vs last quarter (200s only):')
for h,v in sorted(sl.items()):
    v.sort(); n=len(v)
    if n<12: continue
    a=[t for _,t in v[:n//4]]; b=[t for _,t in v[-n//4:]]
    print('   %-30s n=%-4d first %.3fs  last %.3fs  %+.1f%%'%(h[:30],n,sum(a)/len(a),sum(b)/len(b),100.0*((sum(b)/len(b))/(sum(a)/len(a))-1)))
