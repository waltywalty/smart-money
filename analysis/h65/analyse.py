"""A1 - the surface. Unit of observation is the EVENT. Seed declared before use."""
import json,collections,random,statistics as st,sys
sys.path.insert(0,'.')
import fee_model
SEED=20260818            # declared before any resampling
B=10000                  # bootstrap resamples, per the sealed design
GRID=[1,2,5,10,25,50,100,250,500]
MULT=1.0                 # both bounds coincide: every family reports fee_multiplier=1 today
R=[json.loads(l) for l in open('surf_rows.jsonl')]
use=[r for r in R if 'skip' not in r and r['result'] in ('yes','no') and r['best_ask'] is not None]
def pnl(r,N):
    px=r['fills'][str(N)]
    if px is None: return None
    fee=fee_model.effective_per_contract(N,px,multiplier=MULT,rate=0.07,regime='documented')
    payoff=100.0 if r['result']=='yes' else 0.0
    return payoff - px*100.0 - fee
def events(rows,N):
    d=collections.defaultdict(list)
    for r in rows:
        v=pnl(r,N)
        if v is not None: d[r['event']].append(v)
    return {k:sum(v)/len(v) for k,v in d.items()}
def boot(vals,seed):
    rnd=random.Random(seed); n=len(vals); out=[]
    for _ in range(B):
        out.append(sum(vals[rnd.randrange(n)] for _ in range(n))/n)
    out.sort(); return out[int(.025*B)], out[int(.975*B)]
print('unit = EVENT. seed=%d, %d resamples. fee regime=documented, multiplier=%.1f'%(SEED,B,MULT))
print('scope: quiet hours on Kalshi in June 2026. NOT a property of the exchange.')
print()
print('| size | events | mean P&L (c) | 95%% CI | LOO-market | LOO-series |')
print('|---|---:|---:|---|---|---|')
surf={}
for N in GRID:
    ev=events(use,N); vals=list(ev.values())
    m=sum(vals)/len(vals); lo,hi=boot(vals,SEED+N)
    loo_m=[]
    ks=list(ev)
    for k in ks:
        v=[ev[x] for x in ks if x!=k]; loo_m.append(sum(v)/len(v))
    fams=sorted({r['fam'] for r in use})
    loo_s=[]
    for f in fams:
        sub=[r for r in use if r['fam']!=f]; e2=events(sub,N)
        if e2: loo_s.append(sum(e2.values())/len(e2))
    surf[N]={'n':len(vals),'mean':m,'lo':lo,'hi':hi,'loo_m':[min(loo_m),max(loo_m)],'loo_s':[min(loo_s),max(loo_s)]}
    print('| %d | %d | **%.2f** | [%.2f, %.2f] | [%.2f, %.2f] | [%.2f, %.2f] |'%(N,len(vals),m,lo,hi,min(loo_m),max(loo_m),min(loo_s),max(loo_s)))
json.dump({str(k):v for k,v in surf.items()},open('surface.json','w'),indent=1)
print()
best=max(surf,key=lambda k:surf[k]['mean']); worst=min(surf,key=lambda k:surf[k]['mean'])
print('best size point: %d at %.2fc ; worst: %d at %.2fc ; span %.2fc'%(best,surf[best]['mean'],worst,surf[worst]['mean'],surf[best]['mean']-surf[worst]['mean']))
print('positive anywhere?', any(v['mean']>0 for v in surf.values()))
print('any CI excluding zero on the positive side?', any(v['lo']>0 for v in surf.values()))
