import json,subprocess,time,collections
UA='smart-money-research/1.0 (+B2 stratum classification; contact rogerlgk@gmail.com)'
K='https://api.elections.kalshi.com/trade-api/v2'
def get(u,t=20,tries=4):
    for i in range(tries):
        r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','--max-time',str(t),'-w',chr(10)+'%{http_code}',u],capture_output=True,text=True)
        b,_,c=r.stdout.rpartition(chr(10))
        c=int(c) if c.isdigit() else -1
        if c==200: return c,b
        if c in (0,429,500,502,503,504,-1): time.sleep(0.8*(i+1)); continue
        return c,b
    return c,b
S=json.load(open('b1/v2/usable_series.json'))['series']
out=open('b1/v2/series_subset.jsonl','w'); H=collections.Counter()
for i,t in enumerate(S):
    c,b=get(K+'/series/'+t); H['http_%d'%c]+=1
    if c!=200: out.write(json.dumps({'ticker':t,'_http':c})+chr(10)); continue
    s=json.loads(b); s=s.get('series',s)
    out.write(json.dumps({k:s.get(k) for k in ('ticker','title','category','frequency','settlement_sources','contract_url','tags')})+chr(10))
    if i%75==0: out.flush(); print(i,'/',len(S),flush=True)
    time.sleep(0.1)
out.close()
c,b=get(K+'/series/__IMPOSSIBLE_CONTROL_20260820__'); print('impossible-series control ->',c)
c,b=get(K+'/series/'+S[0]); print('positive control ->',c)
print('done',json.dumps(dict(H)),flush=True)
