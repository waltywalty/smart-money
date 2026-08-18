"""liquidity_dollars reads 0.0000 on ALL 84,290 open markets from /markets.
A field that is present in the schema and never populated is a layer artefact,
not a measurement.  Cross-check on a DIFFERENT endpoint before believing it."""
import subprocess,json
UA='smart-money-research/1.0 (+B1 universe; contact rogerlgk@gmail.com)'
K='https://api.elections.kalshi.com/trade-api/v2'
def get(u,t=30):
    r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','--max-time',str(t),'-w','\n%{http_code}',u],capture_output=True,text=True)
    b,_,c=r.stdout.rpartition('\n')
    try: c=int(c)
    except Exception: c=-1
    return c,b
# pick a market with real activity from the v1 pull
best=None
for ln in open('b1/kalshi.jsonl'):
    d=json.loads(ln)
    if best is None or float(d['vol24'])>float(best['vol24']): best=d
t=best['id']
print('busiest open market by 24h volume:',t,'vol24=',best['vol24'],'oi=',best['oi'],'liq(from /markets)=',best['liq'])
c,b=get(K+'/markets/'+t)
print('\nENDPOINT 2  /markets/{ticker} ->',c)
if c==200:
    m=json.loads(b)['market']
    print('  ',json.dumps({k:m.get(k) for k in ('liquidity_dollars','open_interest_fp','volume_fp','volume_24h_fp','notional_value_dollars','yes_bid_size_fp','yes_ask_size_fp','yes_bid_dollars','yes_ask_dollars','status')}))
c,b=get(K+'/markets/'+t+'/orderbook?depth=100')
print('\nENDPOINT 3  /markets/{ticker}/orderbook ->',c)
if c==200:
    ob=json.loads(b).get('orderbook',{})
    ks=list(ob.keys()); print('   keys',ks)
    tot=0.0
    for side in ks:
        lv=ob.get(side) or []
        if lv and isinstance(lv[0],dict):
            s=sum(float(x.get('size_fp') or x.get('size') or 0)*float(x.get('price_dollars') or 0) for x in lv)
        else:
            s=sum(float(x[1])*float(x[0])/100.0 for x in lv) if lv else 0.0
        print('   %-4s levels=%-4d notional=$%.2f'%(side,len(lv),s)); tot+=s
    print('   BOOK NOTIONAL $%.2f  <- vs liquidity_dollars %s from /markets'%(tot,best['liq']))
print('\nIMPOSSIBLE control (same endpoint family):')
c,b=get(K+'/markets/__IMPOSSIBLE_CONTROL_20260818__')
print('   /markets/{impossible} ->',c,b[:100])
c,b=get(K+'/markets/'+t)
print('   POSITIVE control same path ->',c,'(len %d)'%len(b))
