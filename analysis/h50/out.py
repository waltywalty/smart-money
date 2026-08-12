import os,glob
D='/home/claude/work/h50/data'
def load(fp): return sorted((int(a),float(b),float(c),float(d)) for a,b,c,d in (l.strip().split('|') for l in open(fp) if l.strip()))
def ac1(x):
    n=len(x)
    if n<3: return None
    m=sum(x)/n; den=sum((i-m)**2 for i in x)
    if den<=1e-12: return None
    return sum((x[i]-m)*(x[i-1]-m) for i in range(1,n))/den
def dif(p): return [p[i]-p[i-1] for i in range(1,len(p))]
for fp in sorted(glob.glob(D+'/*.txt')):
    t=os.path.basename(fp)[:-4]
    k=[r for r in load(fp) if (r[2]-r[1])<=0.25+1e-9]
    bid=[r[1] for r in k]; ask=[r[2] for r in k]; mid=[(b+a)/2 for b,a in zip(bid,ask)]
    s=sum((a-b)*100 for b,a in zip(bid,ask))/len(k)
    f=lambda v:'  undef' if v is None else f'{v:+.4f}'
    print(f"{t} | n={len(k)} | spread={s:.2f} | ac1_mid={f(ac1(dif(mid)))} | ac1_bid={f(ac1(dif(bid)))} | ac1_ask={f(ac1(dif(ask)))}")
