"""B1 v2 - Polymarket universe, rich fields.
Why a re-pull: v1 omitted resolutionSource (the B1 classification input) and the
liveness flags.  Three gamma traps now recorded, all verified by probe:
  T1 limit=500 SILENTLY returns 100.
  T2 offset>~2000 -> 422, pointing at /markets/keyset.
  T3 active= and archived= are SILENTLY IGNORED (active=false returns active rows;
     archived=true returns archived=false rows).  closed=, volume_num_min,
     liquidity_num_min and end_date_min ARE honoured - each verified by an
     impossible value returning 0 rows and a permissive value returning rows.
So liveness must be filtered CLIENT SIDE.  We pull the whole closed=false stream.
"""
import subprocess,json,time,os,collections,sys
UA='smart-money-research/1.0 (+B1 universe; contact rogerlgk@gmail.com)'
CK='b1/v2/pm_ck.json'
st=json.load(open(CK)) if os.path.exists(CK) else {'cur':'','pages':0,'stop':None,'hist':{}}
H=collections.Counter(st['hist'])
def get(u,t=40,tries=5):
    for i in range(tries):
        r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','--max-time',str(t),'-w','\n%{http_code}',u],capture_output=True,text=True)
        b,_,c=r.stdout.rpartition('\n')
        try: c=int(c)
        except Exception: c=-1
        H['http_%d'%c]+=1
        if c==200: return c,b
        if c in (0,429,500,502,503,504,-1): H['retry']+=1; time.sleep(0.8*(i+1)); continue
        return c,b
    return c,b
F=('conditionId','id','slug','question','description','resolutionSource','resolvedBy','umaResolutionStatuses',
   'active','closed','archived','acceptingOrders','enableOrderBook','approved','restricted','negRisk','funded',
   'startDate','endDate','endDateIso','createdAt','updatedAt','outcomes','outcomePrices','lastTradePrice',
   'bestAsk','bestBid','spread','volumeNum','volume24hr','volume1wk','liquidityNum','orderMinSize',
   'orderPriceMinTickSize','competitive','events')
out=open('b1/v2/pm.jsonl','a')
BUD=float(os.environ.get('BUD','1e9')); t0=time.time()
while st['stop'] is None and time.time()-t0<BUD:
    cur=st['cur']
    c,b=get('https://gamma-api.polymarket.com/markets/keyset?closed=false&limit=100'+('&cursor='+cur if cur else ''))
    if c!=200: st['stop']='http_%d'%c; break
    j=json.loads(b); mk=j.get('markets',[]); st['pages']+=1
    for m in mk:
        d={k:m.get(k) for k in F}
        ev=m.get('events') or []
        d['events']=[{'slug':e.get('slug'),'title':e.get('title'),'ticker':e.get('ticker')} for e in ev][:3]
        out.write(json.dumps(d)+'\n')
    nc=j.get('next_cursor') or ''
    if not nc: st['stop']='cursor_exhausted'
    elif not mk: st['stop']='empty_page'
    st['cur']=nc
    if st['pages']%200==0:
        out.flush(); st['hist']=dict(H); json.dump(st,open(CK,'w'))
        print('pages %d'%st['pages'],flush=True)
out.close(); st['hist']=dict(H); json.dump(st,open(CK,'w'))
n=sum(1 for _ in open('b1/v2/pm.jsonl'))
print('PM pages %d stop=%s rows %d hist %s'%(st['pages'],st['stop'],n,json.dumps(dict(H))),flush=True)
