"""The ROLLING class was found by hand - 32 of 35 scheduled decayers were one host.  A
hand list fitted to the outcome is not a classifier, so the durable form is a MEASURED
flag per url rather than a fourth semantic stratum:

  volatile = the normalised content changed at least once across the four rounds,
             with nothing happening in the world.

Stratum stays semantic (does the source publish on a calendar).  Volatility is measured.
B3's bar is then: in stratum X, AND not volatile.  Reported as a cross-tab so neither
hides inside the other.
"""
import json,collections
R=collections.defaultdict(dict)
for ln in open('b2/change.jsonl'):
    d=json.loads(ln); R[d['url']][d['round']]=d
str_={r['url']:r for r in json.load(open('b2/strata.json'))}
def ok(u): return all(r in R[u] and 200<=R[u][r].get('code',-1)<300 for r in (0,1,2,3))
out=[]; X=collections.defaultdict(lambda:[0,0,0.0])
for u,m in str_.items():
    if u not in R or not ok(u):
        m2=dict(m); m2['volatile']=None; out.append(m2); X[(m['stratum'],'unmeasured')][0]+=1
        X[(m['stratum'],'unmeasured')][1]+=m['markets']; X[(m['stratum'],'unmeasured')][2]+=m['oi']; continue
    seq=[R[u][r] for r in (0,1,2,3)]
    v=any(a['norm']!=b['norm'] for a,b in zip(seq,seq[1:]))
    m2=dict(m); m2['volatile']=v; out.append(m2)
    k=(m['stratum'],'volatile' if v else 'quiet')
    X[k][0]+=1; X[k][1]+=m['markets']; X[k][2]+=m['oi']
print('%-14s %-11s %6s %9s %16s'%('stratum','volatility','urls','markets','open interest'))
for s in ('SCHEDULED','UNSCHEDULED','UNKNOWN'):
    for v in ('quiet','volatile','unmeasured'):
        g=X[(s,v)]
        if g[0]: print('%-14s %-11s %6d %9d %16s'%(s,v,g[0],g[1],'{:,.0f}'.format(g[2])))
q=[r for r in out if r.get('volatile') is False]
print()
print('B3 ELIGIBLE - quiet across all four rounds, any stratum: %d urls, %d markets, $%s'%(
    len(q),sum(r['markets'] for r in q),'{:,.0f}'.format(sum(r['oi'] for r in q))))
for s in ('SCHEDULED','UNSCHEDULED','UNKNOWN'):
    qq=[r for r in q if r['stratum']==s]
    if qq: print('   %-12s %3d urls  %5d markets  $%s'%(s,len(qq),sum(r['markets'] for r in qq),'{:,.0f}'.format(sum(r['oi'] for r in qq))))
json.dump(out,open('b2/strata_volatility.json','w'))
