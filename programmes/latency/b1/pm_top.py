import json,subprocess
UA='smart-money-research/1.0 (+B1 universe; contact rogerlgk@gmail.com)'
G='https://gamma-api.polymarket.com/markets'
def get(u,t=30):
    r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','--max-time',str(t),'-w',chr(10)+'%{http_code}',u],capture_output=True,text=True)
    b,_,c=r.stdout.rpartition(chr(10))
    return (int(c) if c.isdigit() else -1), b
def arr(b):
    j=json.loads(b); return j if isinstance(j,list) else j.get('markets',[])
F=('conditionId','slug','question','description','resolutionSource','endDate','startDate','volumeNum','volume24hr','liquidityNum','bestAsk','bestBid','spread','outcomes','outcomePrices','negRisk','events','umaResolutionStatuses','resolvedBy')
def top(order,fn):
    out=open(fn,'w'); off=0; n=0; last=None; ids=set()
    while off<2100:
        c,b=get(G+'?closed=false&limit=100&offset=%d&order=%s&ascending=false'%(off,order))
        if c!=200: break
        a=arr(b)
        for m in a:
            i=m.get('conditionId')
            if i in ids: continue
            ids.add(i); n+=1; last=float(m.get(order) or 0)
            d={k:m.get(k) for k in F}
            d['events']=[{'slug':e.get('slug'),'title':e.get('title')} for e in (m.get('events') or [])][:2]
            out.write(json.dumps(d)+chr(10))
        if len(a)<100: break
        off+=100
    out.close(); return n,last
for order,fn in [('volume24hr','b1/v2/pm_top_v24.jsonl'),('liquidityNum','b1/v2/pm_top_liq.jsonl'),('volumeNum','b1/v2/pm_top_vol.jsonl')]:
    n,last=top(order,fn)
    tot=0.0
    for ln in open(fn):
        tot+=float(json.loads(ln).get(order) or 0)
    print('top by %-12s n=%-5d sum $%-16s tail value at rank n = %s'%(order,n,'{:,.0f}'.format(tot),'{:,.2f}'.format(last or 0)),flush=True)
