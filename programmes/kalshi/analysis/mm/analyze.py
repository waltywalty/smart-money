import csv,random,statistics as st
random.seed(20260810)
FEE=0.0175
def load(meta):
    out=[]
    for tk,res,vol in meta:
        rows=list(csv.reader(open(tk+'.csv')))
        s=sum(float(r[2]) for r in rows)
        assert abs(s-float(vol))<0.005, (tk,s,vol)   # completeness gate
        outcome=1.0 if res=='yes' else 0.0
        eq=[];wt=[];cs=[];px=[]
        for p_s,side,c_s in rows:
            p=float(p_s); c=float(c_s)
            # taker_side = the outcome the TAKER BOUGHT.
            # taker bought YES  -> MAKER SOLD yes at p   -> pnl = p - outcome
            # taker bought NO   -> MAKER BOUGHT yes at p -> pnl = outcome - p
            pnl = (p-outcome) if side=='yes' else (outcome-p)
            pnl -= FEE*p*(1-p)          # Kalshi maker fee
            eq.append(pnl*100); cs.append(c); px.append(p*100)
        wmean=sum(e*c for e,c in zip(eq,cs))/sum(cs)
        out.append(dict(t=tk,res=res,n=len(rows),px=sum(px)/len(px),
                        eq=sum(eq)/len(eq),wt=wmean,vol=sum(cs)))
    return out

def boot(vals,B=20000):
    n=len(vals)
    ms=sorted(sum(random.choices(vals,k=n))/n for _ in range(B))
    return ms[int(.025*B)],ms[int(.975*B)]

meta=[tuple(r) for r in csv.reader(open('meta.csv'))]
M=load(meta)
print('```')
for m in M:
    print('%s | result=%s | trades=%d | meanPx=%.2f | makerPnL_eq=%+.2f | makerPnL_wt=%+.2f'
          %(m['t'],m['res'],m['n'],m['px'],m['eq'],m['wt']))
print('```')
eq=[m['eq'] for m in M]; wt=[m['wt'] for m in M]
lo1,hi1=boot(eq); lo2,hi2=boot(wt)
print('markets=%d  total_trades=%d  total_contracts=%.0f  yes_settled=%d'
      %(len(M),sum(m['n'] for m in M),sum(m['vol'] for m in M),sum(1 for m in M if m['res']=='yes')))
print('EQUAL-WEIGHTED : mean=%+.2f c  median=%+.2f c  95%%CI=[%+.2f, %+.2f]'%(st.mean(eq),st.median(eq),lo1,hi1))
print('SIZE-WEIGHTED  : mean=%+.2f c  median=%+.2f c  95%%CI=[%+.2f, %+.2f]'%(st.mean(wt),st.median(wt),lo2,hi2))
print('positive markets: eq %d/%d   wt %d/%d'%(sum(1 for v in eq if v>0),len(eq),sum(1 for v in wt if v>0),len(wt)))
print('mean traded price across markets: %.2f c'%(st.mean([m['px'] for m in M])))
# pooled (all trades together, ignoring market grouping)

print()
print('--- MECHANISM: taker direction (share of contracts where taker BOUGHT the yes side) ---')
tot_y=tot_all=0
for tk,res,vol in meta:
    rows=list(csv.reader(open(tk+'.csv')))
    y=sum(float(c) for p,s,c in rows if s=='yes'); a=sum(float(c) for p,s,c in rows)
    tot_y+=y; tot_all+=a
print('pooled: takers bought YES on %.1f%% of all contracts traded'%(100*tot_y/tot_all))

print()
print('--- POOLED (all 2156 trades pooled, ignoring market grouping) ---')
alleq=[];allc=[]
for tk,res,vol in meta:
    o=1.0 if res=='yes' else 0.0
    for p_s,side,c_s in csv.reader(open(tk+'.csv')):
        p=float(p_s);c=float(c_s)
        v=((p-o) if side=='yes' else (o-p))-FEE*p*(1-p)
        alleq.append(v*100);allc.append(c)
print('pooled equal-wt %+.3f c ; pooled size-wt %+.3f c'%(sum(alleq)/len(alleq),
      sum(a*c for a,c in zip(alleq,allc))/sum(allc)))

print()
print('--- EXCLUDED DIAGNOSTIC: KXHIGHCHI-26AUG09-B85.5 (result=YES, only 94.48% of volume in feed) ---')
rows=list(csv.reader(open('KXHIGHCHI-26AUG09-B85.5.csv')))
o=1.0; eq=[];cs=[];px=[]
for p_s,side,c_s in rows:
    p=float(p_s);c=float(c_s)
    v=((p-o) if side=='yes' else (o-p))-FEE*p*(1-p)
    eq.append(v*100);cs.append(c);px.append(p*100)
print('trades=%d meanPx=%.2f makerPnL_eq=%+.2f c  makerPnL_wt=%+.2f c  (takers bought YES on %.1f%% of contracts)'
      %(len(rows),sum(px)/len(px),sum(eq)/len(eq),sum(e*c for e,c in zip(eq,cs))/sum(cs),
        100*sum(c for (p,s,c8),c in zip(rows,cs) if s=='yes')/sum(cs)))
