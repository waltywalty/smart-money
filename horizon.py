import os,glob,statistics as st,random
D='/home/claude/work/h50/data'
def load(fp):
    return sorted((int(a),float(b),float(c),float(d)) for a,b,c,d in (l.strip().split('|') for l in open(fp) if l.strip()))
def ac1(x):
    n=len(x)
    if n<3: return None
    m=sum(x)/n; den=sum((i-m)**2 for i in x)
    if den<=1e-12: return None
    return sum((x[i]-m)*(x[i-1]-m) for i in range(1,n))/den
def dif(p): return [p[i]-p[i-1] for i in range(1,len(p))]
r1=[];r3=[];r6=[];sp=[]
for fp in sorted(glob.glob(D+'/*.txt')):
    k=[r for r in load(fp) if (r[2]-r[1])<=0.25+1e-9]
    mid=[(r[1]+r[2])/2 for r in k]
    sp.append(sum((r[2]-r[1])*100 for r in k)/len(k))
    for lag,acc in ((1,r1),(3,r3),(6,r6)):
        s=mid[::lag]
        v=ac1(dif(s))
        if v is not None: acc.append(v)
for lab,acc in (('1h',r1),('3h',r3),('6h',r6)):
    print(f"sampling {lab}: k={len(acc)} mean ac1={sum(acc)/len(acc):+.4f} median={st.median(acc):+.4f} pos={sum(1 for x in acc if x>0)}/{len(acc)}")
print(f"mean quoted spread across 22 markets = {sum(sp)/len(sp):.2f} cents")
print(f"mean quoted spread across the 19 non-degenerate = {sum(sorted(sp))/len(sp):.2f}")
