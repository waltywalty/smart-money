import json,subprocess
UA='smart-money-research/1.0 (+B1 universe; contact rogerlgk@gmail.com)'
def get(u,t=30):
    r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','--max-time',str(t),'-w',chr(10)+'%{http_code}',u],capture_output=True,text=True)
    b,_,c=r.stdout.rpartition(chr(10))
    return (int(c) if c.isdigit() else -1), b
def n_of(b):
    try:
        j=json.loads(b)
    except Exception: return None,None
    if isinstance(j,list): return len(j),j
    for k in ('markets','data','events'):
        if k in j: return len(j[k]),j
    return None,j
print('--- limit caps ---')
for u in ['https://gamma-api.polymarket.com/markets?closed=false&limit=500',
          'https://gamma-api.polymarket.com/markets/keyset?closed=false&limit=500',
          'https://gamma-api.polymarket.com/markets/keyset?closed=false&limit=1000',
          'https://gamma-api.polymarket.com/events?closed=false&limit=500']:
    c,b=get(u); n,_=n_of(b); print('  %-72s -> %s n=%s'%(u.split('gamma-api.polymarket.com')[1][:70],c,n))
print()
print('--- gamma /events offset ceiling ---')
for off in (0,1000,2000,2100,5000):
    c,b=get('https://gamma-api.polymarket.com/events?closed=false&limit=5&offset=%d'%off)
    n,_=n_of(b); print('  events offset=%-5d -> %s n=%s %s'%(off,c,n,'' if c==200 else b[:90]))
print()
print('--- CLOB API, a DIFFERENT host and layer ---')
c,b=get('https://clob.polymarket.com/markets')
n,j=n_of(b)
print('  /markets -> %s n=%s'%(c,n))
if c==200 and isinstance(j,dict):
    print('  keys',list(j.keys())[:8],'next_cursor',str(j.get('next_cursor'))[:40],'count',j.get('count'))
    nc=j.get('next_cursor')
    c2,b2=get('https://clob.polymarket.com/markets?next_cursor='+str(nc))
    n2,j2=n_of(b2)
    a=[m.get('condition_id','')[:10] for m in (j.get('data') or [])][:3]
    a2=[m.get('condition_id','')[:10] for m in (j2.get('data') or [])][:3] if isinstance(j2,dict) else []
    print('  page2 -> %s n=%s advanced=%s'%(c2,n2,a!=a2))
    print('  p1 ids',a); print('  p2 ids',a2)
    if (j.get('data') or []): print('  sample market keys:',sorted((j['data'][0]).keys())[:40])
print()
print('--- CLOB sampling-markets / simplified ---')
for u in ['https://clob.polymarket.com/sampling-markets','https://clob.polymarket.com/simplified-markets']:
    c,b=get(u); n,j=n_of(b); print('  %-52s -> %s n=%s count=%s'%(u,c,n,(j or {}).get('count') if isinstance(j,dict) else None))
print()
print('--- IMPOSSIBLE control on the clob host ---')
c,b=get('https://clob.polymarket.com/__impossible_control_20260818__'); print('  ->',c,b[:100])
c,b=get('https://clob.polymarket.com/markets?next_cursor=__IMPOSSIBLE__'); print('  bad cursor ->',c,b[:140])
