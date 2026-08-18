"""B1 v2 - Kalshi source layer.
Key discovery: settlement_sources is a STRUCTURED [{name,url}] array carried on the
EVENT object and on the SERIES object.  That is the B1 classification input direct
from the venue - no free-text parsing of rules_primary needed (which is empty on the
MVE shards anyway).  Markets join to events by event_ticker, events to series by
series_ticker.
"""
import subprocess,json,time,os,collections
UA='smart-money-research/1.0 (+B1 universe; contact rogerlgk@gmail.com)'
K='https://api.elections.kalshi.com/trade-api/v2'
CK='b1/v2/k_ck.json'
st=json.load(open(CK)) if os.path.exists(CK) else {'cur':'','pages':0,'stop':None,'hist':{},'series_done':False}
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
ef=open('b1/v2/events.jsonl','a')
while st['stop'] is None:
    cur=st['cur']
    c,b=get(K+'/events?status=open&limit=200&with_nested_markets=false'+('&cursor='+cur if cur else ''))
    if c!=200: st['stop']='http_%d'%c; break
    j=json.loads(b); ev=j.get('events',[]); st['pages']+=1
    for e in ev:
        ef.write(json.dumps({k:e.get(k) for k in ('event_ticker','series_ticker','title','sub_title','category','settlement_sources','mutually_exclusive','collateral_return_type','available_on_brokers','strike_period')})+'\n')
    nc=j.get('cursor') or ''
    if not nc: st['stop']='cursor_exhausted'
    elif not ev: st['stop']='empty_page'
    st['cur']=nc
    if st['pages']%50==0:
        ef.flush(); st['hist']=dict(H); json.dump(st,open(CK,'w')); print('event pages',st['pages'],flush=True)
    time.sleep(0.15)
ef.close(); st['hist']=dict(H); json.dump(st,open(CK,'w'))
ne=sum(1 for _ in open('b1/v2/events.jsonl'))
print('EVENTS pages %d stop=%s rows %d'%(st['pages'],st['stop'],ne),flush=True)
# --- series pass over the unique series tickers seen in the OPEN market universe ---
ser=set()
for ln in open('b1/v2/events.jsonl'):
    d=json.loads(ln)
    if d.get('series_ticker'): ser.add(d['series_ticker'])
print('unique open series:',len(ser),flush=True)
have=set()
if os.path.exists('b1/v2/series.jsonl'):
    for ln in open('b1/v2/series.jsonl'):
        try: have.add(json.loads(ln)['ticker'])
        except Exception: pass
sf=open('b1/v2/series.jsonl','a')
todo=sorted(ser-have); done=0
for t in todo:
    c,b=get(K+'/series/'+t,t=20,tries=3)
    if c!=200:
        sf.write(json.dumps({'ticker':t,'_http':c})+'\n'); continue
    s=json.loads(b); s=s.get('series',s)
    sf.write(json.dumps({k:s.get(k) for k in ('ticker','title','category','frequency','settlement_sources','contract_url','contract_terms_url','fee_type','fee_multiplier','tags','additional_prohibitions')})+'\n')
    done+=1
    if done%100==0: sf.flush(); print('series',done,'/',len(todo),flush=True)
    time.sleep(0.12)
sf.close(); st['hist']=dict(H); st['series_done']=True; json.dump(st,open(CK,'w'))
print('SERIES done %d  hist %s'%(done,json.dumps(dict(H))),flush=True)
