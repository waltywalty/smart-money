import subprocess,json,time
UA='smart-money-research/1.0 (+B1 universe; contact rogerlgk@gmail.com)'
G='https://gamma-api.polymarket.com/markets/keyset'
def get(u,t=30):
    r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','--max-time',str(t),'-w','\n%{http_code}',u],capture_output=True,text=True)
    b,_,c=r.stdout.rpartition('\n')
    try: c=int(c)
    except Exception: c=-1
    return c,b
def probe(label,q,field=None):
    c,b=get(G+q)
    if c!=200: print('%-34s -> %d %s'%(label,c,b[:140])); return None
    j=json.loads(b); m=j.get('markets',[])
    vals=[x.get(field) for x in m][:4] if field else None
    print('%-34s -> 200 n=%-3d %s'%(label,len(m),('%s=%s'%(field,vals)) if field else ''))
    return m
# --- is a numeric filter honoured?  permissive vs impossible pair ---
probe('vol_min=0 (permissive)','?closed=false&volume_num_min=0&limit=3','volumeNum')
probe('vol_min=1e6','?closed=false&volume_num_min=1000000&limit=3','volumeNum')
probe('vol_min=1e18 (IMPOSSIBLE)','?closed=false&volume_num_min=1000000000000000000&limit=3','volumeNum')
probe('liq_min=1e18 (IMPOSSIBLE)','?closed=false&liquidity_num_min=1000000000000000000&limit=3','liquidityNum')
probe('liq_min=50000','?closed=false&liquidity_num_min=50000&limit=3','liquidityNum')
probe('end_date_min future','?closed=false&end_date_min=2026-08-18T00:00:00Z&limit=3','endDate')
probe('end_date_min yr3000 (IMPOSS)','?closed=false&end_date_min=3000-01-01T00:00:00Z&limit=3','endDate')
probe('accepting_orders=true','?closed=false&accepting_orders=true&limit=3','acceptingOrders')
probe('archived=true','?closed=false&archived=true&limit=3','archived')
# --- page latency over 5 pages of the plain closed=false stream ---
cur=''; t0=time.time(); n=0
for i in range(5):
    c,b=get(G+'?closed=false&limit=100'+('&cursor='+cur if cur else ''))
    if c!=200: break
    j=json.loads(b); n+=len(j.get('markets',[])); cur=j.get('next_cursor') or ''
    if not cur: break
print('latency: %d rows over 5 pages in %.2fs -> %.3f s/page'%(n,time.time()-t0,(time.time()-t0)/5))
