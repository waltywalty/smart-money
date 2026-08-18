import os, glob, random, statistics as st

D='/home/claude/work/h50/data'
SERIES={'KXFED':'FED','KXCPIYOY':'CPI','KXPAYROLLS':'PAY','KXNHLGAME':'NHL','KXNBAGAME':'NBA','KXMLBGAME':'MLB'}

def load(fp):
    rows=[]
    for line in open(fp):
        line=line.strip()
        if not line: continue
        t,b,a,v=line.split('|')
        if b=='null' or a=='null': continue
        rows.append((int(t),float(b),float(a),float(v)))
    rows.sort()
    return rows

def ac1(x):
    n=len(x)
    if n<3: return None
    m=sum(x)/n
    den=sum((xi-m)**2 for xi in x)
    if den<=1e-12: return None
    num=sum((x[i]-m)*(x[i-1]-m) for i in range(1,n))
    return num/den

def diffs(p): return [p[i]-p[i-1] for i in range(1,len(p))]

res=[]
for fp in sorted(glob.glob(D+'/*.txt')):
    tick=os.path.basename(fp)[:-4]
    raw=load(fp)
    # filter: two-sided quote, spread <= 25c (drops settlement 0/1 artifact and one-sided books)
    keep=[r for r in raw if (r[2]-r[1])<=0.2500+1e-9 and r[2]>=r[1]]
    drop_wide=len(raw)-len(keep)
    if len(keep)<5: 
        res.append(dict(t=tick,n=len(keep),skip=True)); continue
    bid=[r[1] for r in keep]; ask=[r[2] for r in keep]
    mid=[(b+a)/2 for b,a in zip(bid,ask)]
    spread_c=sum((a-b)*100 for b,a in zip(bid,ask))/len(keep)
    # volume>0 variant
    kv=[r for r in keep if r[3]>0]
    mv=[(r[1]+r[2])/2 for r in kv]
    res.append(dict(t=tick, n=len(keep), nraw=len(raw), dropped=drop_wide,
        spread=spread_c, meanmid=sum(mid)/len(mid),
        acm=ac1(diffs(mid)), acb=ac1(diffs(bid)), aca=ac1(diffs(ask)),
        acv=ac1(diffs(mv)) if len(mv)>=5 else None, nv=len(kv),
        series=SERIES[tick.split('-')[0]], skip=False))

print('=== PER MARKET ===')
for r in res:
    if r.get('skip'): print(r['t'],'SKIP n=',r['n']); continue
    f=lambda x: 'undef' if x is None else f'{x:+.4f}'
    print(f"{r['t']} | n={r['n']} | spread={r['spread']:.2f} | ac1_mid={f(r['acm'])} | ac1_bid={f(r['acb'])} | ac1_ask={f(r['aca'])} | meanmid={r['meanmid']:.3f} | raw={r['nraw']} drop={r['dropped']} | volgt0 n={r['nv']} ac={f(r['acv'])}")

ok=[r for r in res if not r.get('skip')]
defm=[r for r in ok if r['acm'] is not None]
print()
print('markets total',len(res),'usable',len(ok),'with defined ac1_mid',len(defm))
for k,lab in [('acm','mid'),('acb','bid'),('aca','ask')]:
    v=[r[k] for r in ok if r[k] is not None]
    print(f"{lab}: n={len(v)} mean={sum(v)/len(v):+.4f} median={st.median(v):+.4f} positive={sum(1 for x in v if x>0)}/{len(v)}")

# bootstrap over MARKETS
random.seed(20260810)
def boot(vals,B=20000):
    n=len(vals); ms=[]
    for _ in range(B):
        s=[vals[random.randrange(n)] for _ in range(n)]
        ms.append(sum(s)/n)
    ms.sort()
    return ms[int(0.025*B)], ms[int(0.975*B)]
vm=[r['acm'] for r in ok if r['acm'] is not None]
lo,hi=boot(vm); print(f"bootstrap 95% CI on mean ac1_mid (resampling markets): [{lo:+.4f}, {hi:+.4f}]")
vb=[r['acb'] for r in ok if r['acb'] is not None]; lo2,hi2=boot(vb)
va=[r['aca'] for r in ok if r['aca'] is not None]; lo3,hi3=boot(va)
print(f"bootstrap 95% CI mean ac1_bid: [{lo2:+.4f}, {hi2:+.4f}]   ac1_ask: [{lo3:+.4f}, {hi3:+.4f}]")

# subsets
midr=[r for r in ok if 0.20<=r['meanmid']<=0.80 and r['acm'] is not None]
pin =[r for r in ok if not (0.20<=r['meanmid']<=0.80)]
pind=[r for r in pin if r['acm'] is not None]
def summ(lst,lab):
    if not lst: print(lab,'none'); return
    v=[r['acm'] for r in lst]
    print(f"{lab}: k={len(v)} mean_mid_ac={sum(v)/len(v):+.4f} median={st.median(v):+.4f} pos={sum(1 for x in v if x>0)}/{len(v)} meanspread={sum(r['spread'] for r in lst)/len(lst):.2f}c")
    vb=[r['acb'] for r in lst if r['acb'] is not None]; va=[r['aca'] for r in lst if r['aca'] is not None]
    if vb: print(f"    bid mean={sum(vb)/len(vb):+.4f} (k={len(vb)}) ask mean={sum(va)/len(va):+.4f} (k={len(va)})")
summ(midr,'MIDRANGE 0.20-0.80')
summ(pind,'PINNED (outside 0.20-0.80, defined)')
print('pinned markets total (incl undefined ac1):',len(pin))
if midr:
    lo4,hi4=boot([r['acm'] for r in midr]); print(f"midrange bootstrap 95% CI: [{lo4:+.4f}, {hi4:+.4f}]")

# vol>0 sensitivity
vv=[r['acv'] for r in ok if r['acv'] is not None]
print(f"SENSITIVITY vol>0 only: k={len(vv)} mean={sum(vv)/len(vv):+.4f} median={st.median(vv):+.4f} pos={sum(1 for x in vv if x>0)}/{len(vv)}")

# per series
print()
for s in sorted(set(r['series'] for r in ok)):
    g=[r['acm'] for r in ok if r['series']==s and r['acm'] is not None]
    if g: print(f"series {s}: k={len(g)} mean_ac1_mid={sum(g)/len(g):+.4f}")
# spread vs ac relationship
print()
pairs=[(r['spread'],r['acm']) for r in ok if r['acm'] is not None]
wide=[a for s,a in pairs if s>2.0]; narrow=[a for s,a in pairs if s<=2.0]
print(f"wide-book (>2c) k={len(wide)} mean_ac={sum(wide)/len(wide):+.4f}" if wide else 'no wide')
print(f"narrow-book (<=2c) k={len(narrow)} mean_ac={sum(narrow)/len(narrow):+.4f}" if narrow else 'no narrow')
