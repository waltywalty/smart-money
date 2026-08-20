"""Is the White House EOP page actually UNCONTESTED?

The stratum split rests on a competitive claim: nobody refreshes the BLS page, so the
unscheduled stratum is uncontested.  The EOP page carries 60.8% of the eligible open
interest, and a White House personnel page during a shake-up is one of the most-refreshed
pages on the internet.  If it is contested, that is a stratum-ASSIGNMENT error rather than
a weighting problem, and the genuinely uncontested money is $7.8M rather than $50.9M.

Proxy: quoted spread and book depth from the live public order book (`orderbook_fp`).
Tight and deep = someone is competing to quote it.

**What this proxy does and does not measure.**  It measures competition to QUOTE.  A market
can be tightly quoted by patient market makers with nobody racing the source at all.  So a
wide book is decent evidence of an uncontested market; a tight book is suggestive, not
conclusive, about a latency race.  Stated here so it cannot be quoted as more than it is.
"""
import json,subprocess,collections,statistics as S
UA='smart-money-research/1.0 (+B2 contestedness proxy; contact rogerlgk@gmail.com)'
K='https://api.elections.kalshi.com/trade-api/v2'
def get(u,t=20,tries=3):
    for i in range(tries):
        r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','--max-time',str(t),'-w',chr(10)+'%{http_code}',u],capture_output=True,text=True)
        b,_,c=r.stdout.rpartition(chr(10)); c=int(c) if c.isdigit() else -1
        if c==200: return c,b
        if c in (0,429,500,502,503,504,-1): continue
        return c,b
    return c,b
EOP='https://www.whitehouse.gov/administration/executive-office-of-the-president/'
str_={r['url']:r for r in json.load(open('b2/strata_volatility.json'))}
urls_by={'EOP':[EOP],
         'UNSCHED_other':[u for u,r in str_.items() if r['stratum']=='UNSCHEDULED' and r.get('volatile') is False and u!=EOP],
         'SCHEDULED':[u for u,r in str_.items() if r['stratum']=='SCHEDULED' and r.get('volatile') is False]}
ev=collections.defaultdict(list)
for ln in open('b1/v2/events.jsonl'):
    e=json.loads(ln); ss=e.get('settlement_sources') or []
    if len(ss)!=1: continue
    u=(ss[0].get('url') or '').strip()
    for g,us in urls_by.items():
        if u in us: ev[g].append(e['event_ticker'])
print('events per group:',{g:len(v) for g,v in ev.items()},flush=True)
def book(t):
    c,b=get(K+'/markets/'+t+'/orderbook?depth=20')
    if c!=200: return None
    ob=json.loads(b).get('orderbook_fp') or {}
    yes=[(float(p),float(s)) for p,s in (ob.get('yes_dollars') or [])]
    no=[(float(p),float(s)) for p,s in (ob.get('no_dollars') or [])]
    if not yes or not no: return None
    bid=max(p for p,_ in yes); ask=1.0-max(p for p,_ in no)
    if ask<=bid: return None
    bs=sum(s for p,s in yes if p>=bid-0.05); as_=sum(s for p,s in no if p>=(1.0-ask)-0.05)
    return {'spread_c':100.0*(ask-bid),'mid':50.0*(ask+bid),'depth5c':bs+as_}
res=collections.defaultdict(list)
for g,evs in ev.items():
    seen=0
    for et in evs:
        c,b=get(K+'/markets?event_ticker='+et+'&status=open&limit=200')
        if c!=200: continue
        for m in json.loads(b).get('markets',[]):
            if float(m.get('open_interest_fp') or 0)<=0: continue
            bk=book(m['ticker'])
            if bk: bk['oi']=float(m['open_interest_fp']); res[g].append(bk); seen+=1
            if seen>=60: break
        if seen>=60: break
    print('%s: %d markets with a two-sided book'%(g,len(res[g])),flush=True)
print()
print('%-16s %5s %11s %11s %13s %13s'%('group','n','med spread','p25 spread','med depth5c','med OI'))
for g in ('EOP','UNSCHED_other','SCHEDULED'):
    v=res[g]
    if not v: continue
    sp=sorted(x['spread_c'] for x in v); dp=sorted(x['depth5c'] for x in v); oi=sorted(x['oi'] for x in v)
    print('%-16s %5d %10.2fc %10.2fc %13.0f %13.0f'%(g,len(v),sp[len(sp)//2],sp[len(sp)//4],dp[len(dp)//2],oi[len(oi)//2]))
c,b=get(K+'/markets/__IMPOSSIBLE_CONTROL_20260820__/orderbook')
print()
print('impossible-ticker orderbook control ->',c)
json.dump({g:v for g,v in res.items()},open('b2/contested.json','w'))
