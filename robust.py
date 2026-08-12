import os,glob,random,statistics as st
D='/home/claude/work/h50/data'
def load(fp):
    rows=[]
    for l in open(fp):
        l=l.strip()
        if not l: continue
        t,b,a,v=l.split('|')
        rows.append((int(t),float(b),float(a),float(v)))
    return sorted(rows)
def ac1(x):
    n=len(x)
    if n<3: return None
    m=sum(x)/n; den=sum((i-m)**2 for i in x)
    if den<=1e-12: return None
    return sum((x[i]-m)*(x[i-1]-m) for i in range(1,n))/den
def dif(p): return [p[i]-p[i-1] for i in range(1,len(p))]

rows=[]
for fp in sorted(glob.glob(D+'/*.txt')):
    t=os.path.basename(fp)[:-4]
    keep=[r for r in load(fp) if (r[2]-r[1])<=0.2500+1e-9]
    mid=[(r[1]+r[2])/2 for r in keep]
    # A: full  B: drop last 3 candles (settlement / in-play endgame)
    a=ac1(dif(mid)); b=ac1(dif(mid[:-3])) if len(mid)>8 else None
    # C: contiguous-hour pairs only  (dP computed only where gap==3600)
    ts=[r[0] for r in keep]
    seq=[]; run=[mid[0]]
    for i in range(1,len(keep)):
        if ts[i]-ts[i-1]==3600: run.append(mid[i])
        else:
            if len(run)>3: seq.append(run)
            run=[mid[i]]
    if len(run)>3: seq.append(run)
    dd=[]
    for s in seq: dd+= dif(s)
    c=ac1(dd) if len(dd)>=5 else None
    mad=sum(abs(x) for x in dif(mid))*100/max(1,len(mid)-1)
    zer=sum(1 for x in dif(mid) if abs(x)<1e-9)/max(1,len(mid)-1)
    rows.append((t,a,b,c,mad,zer,len(mid)))
print(f"{'ticker':34} {'full':>8} {'drop_last3':>11} {'contig':>8} {'mean|dP|c':>9} {'zero%':>6}")
for t,a,b,c,mad,z,n in rows:
    f=lambda x:'undef' if x is None else f'{x:+.4f}'
    print(f"{t:34} {f(a):>8} {f(b):>11} {f(c):>8} {mad:9.2f} {z*100:5.0f}%")
for idx,lab in [(1,'full'),(2,'drop last 3 candles'),(3,'contiguous-hour pairs only')]:
    v=[r[idx] for r in rows if r[idx] is not None]
    print(f"{lab:30} k={len(v):2d} mean={sum(v)/len(v):+.4f} median={st.median(v):+.4f} pos={sum(1 for x in v if x>0)}/{len(v)}")
v=[r[4] for r in rows]; print(f"mean |dP| across markets = {sum(v)/len(v):.2f} cents/hour")
z=[r[5] for r in rows]; print(f"mean fraction of zero hourly changes = {sum(z)/len(z)*100:.0f}%")
