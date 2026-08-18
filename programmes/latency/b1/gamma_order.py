import json,subprocess
UA='smart-money-research/1.0 (+B1 universe; contact rogerlgk@gmail.com)'
G='https://gamma-api.polymarket.com/markets'
def get(u,t=30):
    r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','--max-time',str(t),'-w',chr(10)+'%{http_code}',u],capture_output=True,text=True)
    b,_,c=r.stdout.rpartition(chr(10))
    return (int(c) if c.isdigit() else -1), b
def arr(b):
    j=json.loads(b); return j if isinstance(j,list) else j.get('markets',[])
print('--- is order= honoured? ---')
for q in ['?closed=false&limit=5&order=liquidityNum&ascending=false',
          '?closed=false&limit=5&order=liquidityNum&ascending=true',
          '?closed=false&limit=5&order=__impossible_field__&ascending=false']:
    c,b=get(G+q)
    try: print('  %-56s -> %d liq %s'%(q[:56],c,[round(float(m.get('liquidityNum') or 0)) for m in arr(b)]))
    except Exception: print('  %-56s -> %d %s'%(q[:56],c,b[:90]))
def exact(q,cap=21):
    n=0; off=0; A={'vol':0.0,'v24':0.0,'liq':0.0}; stop=None
    while True:
        c,b=get(G+'?closed=false&limit=100&offset=%d'%off+q)
        if c!=200: stop='http_%d'%c; break
        a=arr(b); n+=len(a)
        for m in a:
            A['vol']+=float(m.get('volumeNum') or 0); A['v24']+=float(m.get('volume24hr') or 0); A['liq']+=float(m.get('liquidityNum') or 0)
        if len(a)<100: stop='short_page'; break
        off+=100
        if off>=cap*100: stop='offset_cap'; break
    return n,stop,A
print()
print('  %-30s %8s %-12s %14s %13s %14s'%('stratum','markets','stop','volume $','24h vol $','liquidity $'))
STR=[('liq>=100000','&liquidity_num_min=100000'),('liq>=10000','&liquidity_num_min=10000'),
     ('liq>=1000','&liquidity_num_min=1000'),('vol>=1000000','&volume_num_min=1000000'),
     ('vol>=100000','&volume_num_min=100000'),('vol>=10000','&volume_num_min=10000'),
     ('IMPOSSIBLE liq>=1e18','&liquidity_num_min=1000000000000000000')]
for lab,q in STR:
    n,s,A=exact(q)
    print('  %-30s %8d %-12s %14s %13s %14s'%(lab,n,s,'{:,.0f}'.format(A['vol']),'{:,.0f}'.format(A['v24']),'{:,.0f}'.format(A['liq'])),flush=True)
