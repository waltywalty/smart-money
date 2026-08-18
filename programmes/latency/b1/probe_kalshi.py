import subprocess,json
UA='smart-money-research/1.0 (+B1 universe; contact rogerlgk@gmail.com)'
K='https://api.elections.kalshi.com/trade-api/v2'
def get(u,t=30):
    r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','--max-time',str(t),'-w','\n%{http_code}',u],capture_output=True,text=True)
    b,_,c=r.stdout.rpartition('\n')
    try: c=int(c)
    except Exception: c=-1
    return c,b
c,b=get(K+'/markets?status=open&limit=3')
print('status',c)
j=json.loads(b); m=j['markets']
print('market keys:',sorted(m[0].keys()))
print()
for x in m[:2]:
    print(json.dumps({k:x.get(k) for k in sorted(x) if 'volume' in k or 'liquid' in k or 'interest' in k or k in ('ticker','status','yes_ask','no_ask','last_price','can_close_early','expiration_time','close_time')},indent=None))
print()
# does the market object carry a resolution-source field at all?
print('rules_primary head:',(m[0].get('rules_primary') or '')[:300])
print()
# EVENT object - may carry more
c2,b2=get(K+'/events?limit=2&status=open&with_nested_markets=false')
print('events status',c2)
if c2==200:
    e=json.loads(b2).get('events',[])
    if e: print('event keys:',sorted(e[0].keys()))
# SERIES object
c3,b3=get(K+'/series/KXHIGHNY')
print('series status',c3)
if c3==200:
    s=json.loads(b3); s=s.get('series',s)
    print('series keys:',sorted(s.keys()))
    print('series sample:',json.dumps({k:s.get(k) for k in ('ticker','title','category','frequency','settlement_sources','contract_url','fee_type','fee_multiplier')})[:700])
# IMPOSSIBLE control on the same endpoint family
c4,b4=get(K+'/series/__IMPOSSIBLE_CONTROL_20260818__')
print('series IMPOSSIBLE control ->',c4,b4[:120])
