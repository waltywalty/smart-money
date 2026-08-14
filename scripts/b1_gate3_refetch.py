import json, os, gzip, random, sys, time, collections, functools
print=functools.partial(print,flush=True)
sys.path.insert(0,'/root/work')
from kx import get
from concurrent.futures import ThreadPoolExecutor
OUT='/root/work/data/historical'
STATE='/root/work/data/g3.json'
S=json.load(open(STATE)) if os.path.exists(STATE) else None
if S is None:
    C=json.load(open('/root/work/data/mfcache.json'))
    picks=[[v['series'],v['file'],max(1,round(v['unique_events']*0.01)),v['rows']] for v in C.values() if v['rows']>0]
    random.Random(20260814).shuffle(picks)
    S={'picks':picks,'seen':[],'checked':0,'ok':0,'mkts':0,'bad':[],'http':{},'target':sum(p[2] for p in picks)}
    print('frame: %d series, 1%%-of-events target = %d events'%(len(picks),S['target']))
BUD=float(sys.argv[1]) if len(sys.argv)>1 else 40
t0=time.time(); done=set(S['seen'])
def opener(f):
    p=os.path.join(OUT,f)
    return (gzip.open if f.endswith('.gz') else open)(p,'rt')
BIG=int(sys.argv[2]) if len(sys.argv)>2 else 60000
KCAP=int(sys.argv[3]) if len(sys.argv)>3 else 12
for s,f,k,nrow in S['picks']:
    if s in done: continue
    if time.time()-t0>BUD: break
    if nrow>BIG:
        S.setdefault('deferred',[]).append(s); done.add(s); continue
    try:
        evs=set()
        with opener(f) as fh:
            for line in fh:
                if not line.strip(): continue
                i=line.find('"event_ticker":"')
                if i<0: continue
                j=line.find('"',i+16)
                evs.add(line[i+16:j])
        if not evs: done.add(s); continue
        pick=set(random.Random(abs(hash(s))%10**8).sample(sorted(evs), min(k,len(evs),KCAP)))
        bulk=collections.defaultdict(dict)
        with opener(f) as fh:
            for line in fh:
                if not line.strip(): continue
                d=json.loads(line)
                if d['event_ticker'] in pick: bulk[d['event_ticker']][d['ticker']]=d
    except Exception as e:
        S['bad'].append([s,'load:%s'%type(e).__name__]); done.add(s); continue
    def chk(e):
        code,j,_=get('/historical/markets',{'event_ticker':e,'limit':1000},min_gap=0.3)
        if code!=200 or not isinstance(j,dict): return (e,'http_%s'%code,0)
        live={m['ticker']:m for m in (j.get('markets') or [])}
        b=bulk[e]
        if set(live)!=set(b): return (e,'ticker_set live=%d bulk=%d'%(len(live),len(b)),len(b))
        for t,row in b.items():
            for kk,vv in row.items():
                if kk=='series_ticker': continue
                if live[t].get(kk)!=vv: return (e,'field %s bulk=%r refetch=%r'%(kk,vv,live[t].get(kk)),len(b))
        return (e,None,len(b))
    with ThreadPoolExecutor(max_workers=3) as ex:
        for e,err,nm in ex.map(chk,sorted(pick)):
            if err and err.startswith('http_'):
                S['http'][err]=S['http'].get(err,0)+1     # a status code is not a mismatch
            elif err:
                S['checked']+=1; S['mkts']+=nm; S['bad'].append([e,err])
            else:
                S['checked']+=1; S['mkts']+=nm; S['ok']+=1
    done.add(s)
    if time.time()-t0>BUD: break
S['seen']=sorted(done)
json.dump(S,open(STATE,'w'))
print('GATE3 deferred_big=%d'%len(set(S.get('deferred',[]))))
print('GATE3 series=%d/%d events_checked=%d (%.2f%% of the 1%% target) matched=%d MISMATCH=%d markets_compared=%d http=%s %.1fs'%(
  len(done),len(S['picks']),S['checked'],100.0*S['checked']/max(1,S['target']),S['ok'],len(S['bad']),S['mkts'],S['http'],time.time()-t0))
if S['bad']: print('  mismatches:',S['bad'][:4])
