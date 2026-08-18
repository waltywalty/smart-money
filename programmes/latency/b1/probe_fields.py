import subprocess,json
UA='smart-money-research/1.0 (+B1 universe; contact rogerlgk@gmail.com)'
G='https://gamma-api.polymarket.com/markets/keyset'
def get(u,t=30):
    r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','--max-time',str(t),'-w','\n%{http_code}',u],capture_output=True,text=True)
    b,_,c=r.stdout.rpartition('\n')
    try: c=int(c)
    except Exception: c=-1
    return c,b
# 1. field inventory
c,b=get(G+'?closed=false&limit=2')
print('A field-inventory status',c)
if c==200:
    j=json.loads(b); ks=sorted(j.keys()); print('  top keys',ks)
    m=j.get('markets',[])
    if m: print('  market keys',sorted(m[0].keys()))
# 2. does it honour active=true ?
for q in ['?closed=false&active=true&limit=2','?closed=false&active=false&limit=2','?closed=true&limit=2','?active=true&closed=false&enableOrderBook=true&limit=2']:
    c,b=get(G+q)
    if c==200:
        j=json.loads(b); m=j.get('markets',[])
        print('B %-52s -> %d n=%d act=%s clo=%s aop=%s eob=%s'%(q,c,len(m),
           [x.get('active') for x in m],[x.get('closed') for x in m],
           [x.get('acceptingOrders') for x in m],[x.get('enableOrderBook') for x in m]))
    else: print('B %-52s -> %d %s'%(q,c,b[:120]))
# 3. IMPOSSIBLE CONTROL: a filter value that cannot match
c,b=get(G+'?closed=false&slug=__impossible_control_key_20260818__&limit=2')
j=json.loads(b) if c==200 else {}
print('C impossible-control  ->',c,'n=',len(j.get('markets',[])))
# 4. POSITIVE CONTROL: a slug we have already seen in the pull
import itertools
seen=None
for ln in itertools.islice(open('b1/pm.jsonl'),3000,3001): seen=json.loads(ln)['event']
c,b=get(G+'?closed=false&slug=%s&limit=2'%seen)
j=json.loads(b) if c==200 else {}
mm=j.get('markets',[])
print('D positive-control  slug=%s ->'%seen,c,'n=',len(mm))
if mm: print('   sample:',json.dumps({k:mm[0].get(k) for k in ('question','active','closed','acceptingOrders','enableOrderBook','endDate','volumeNum','liquidityNum','bestAsk','umaResolutionStatuses')})[:600])
