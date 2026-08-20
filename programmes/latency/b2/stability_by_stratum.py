"""Stability reported BY STRATUM, per the 2026-08-20 ruling: scheduled pages should be
trivially stable between releases, so pooling would flatter the unscheduled ones.

Also reports how many urls that were stable at T+15m had changed by T+60m - the number
that says whether a short observation window overstates stability.
"""
import json,collections
R=collections.defaultdict(dict); kind={}
for ln in open('b2/change.jsonl'):
    d=json.loads(ln); R[d['url']][d['round']]=d; kind[d['url']]=d['kind']
str_={r['url']:r for r in json.load(open('b2/strata.json'))}
rounds=sorted({r for v in R.values() for r in v})
LBL={0:'T+0',1:'T+5m',2:'T+15m',3:'T+60m'}
def ok(u,rs): return all(r in R[u] and 200<=R[u][r].get('code',-1)<300 for r in rs)
for upto in ([0,1,2],[0,1,2,3]):
    if not all(r in rounds for r in upto): continue
    print('='*82)
    print('window %s -> %s'%(LBL[upto[0]],LBL[upto[-1]]))
    G=collections.defaultdict(lambda:[0,0,0,0.0,0.0])
    for u,meta in str_.items():
        if u not in R or not ok(u,upto): continue
        seq=[R[u][r] for r in upto]
        ch=sum(1 for a,b in zip(seq,seq[1:]) if a['norm']!=b['norm'])
        g=G[meta['stratum']]
        g[0]+=1; g[3]+=meta['markets']; g[4]+=meta['oi']
        if ch==0: g[1]+=1; g[2]+=meta['markets']
    print('%-14s %6s %8s %8s %10s %10s'%('stratum','urls','stable','stable%','mk stable','mk total'))
    for k in ('SCHEDULED','UNSCHEDULED','UNKNOWN'):
        g=G[k]
        if not g[0]: continue
        print('%-14s %6d %8d %7.1f%% %10d %10d'%(k,g[0],g[1],100.0*g[1]/g[0],g[2],g[3]))
    tot=[sum(G[k][i] for k in G) for i in range(4)]
    print('%-14s %6d %8d %7.1f%% %10d %10d'%('POOLED',tot[0],tot[1],100.0*tot[1]/max(1,tot[0]),tot[2],tot[3]))
    print()
if 3 in rounds:
    print('='*82)
    print('DECAY - urls stable through T+15m that had changed by T+60m')
    D=collections.defaultdict(lambda:[0,0,0,0])
    for u,meta in str_.items():
        if u not in R or not ok(u,[0,1,2,3]): continue
        s15=all(R[u][a]['norm']==R[u][b]['norm'] for a,b in ((0,1),(1,2)))
        if not s15: continue
        d=D[meta['stratum']]; d[0]+=1; d[2]+=meta['markets']
        if R[u][2]['norm']!=R[u][3]['norm']: d[1]+=1; d[3]+=meta['markets']
    print('%-14s %10s %10s %9s %12s'%('stratum','stable@15m','changed@60m','decay%','mk lost'))
    for k in ('SCHEDULED','UNSCHEDULED','UNKNOWN'):
        d=D[k]
        if not d[0]: continue
        print('%-14s %10d %10d %8.1f%% %12d'%(k,d[0],d[1],100.0*d[1]/d[0],d[3]))
    t=[sum(D[k][i] for k in D) for i in range(4)]
    print('%-14s %10d %10d %8.1f%% %12d'%('POOLED',t[0],t[1],100.0*t[1]/max(1,t[0]),t[3]))
