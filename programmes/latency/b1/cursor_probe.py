import json,subprocess,urllib.parse as up
UA='smart-money-research/1.0 (+B1 universe; contact rogerlgk@gmail.com)'
G='https://gamma-api.polymarket.com/markets/keyset'
def get(u):
    r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','--max-time','30','-w',chr(10)+'%{http_code}',u],capture_output=True,text=True)
    b,_,c=r.stdout.rpartition(chr(10))
    return (int(c) if c.isdigit() else -1), b
c,b=get(G+'?closed=false&limit=5')
j=json.loads(b); ids0=[m['conditionId'][:12] for m in j['markets']]; nc=j.get('next_cursor')
print('page1',c,'ids',ids0)
print('next_cursor len',len(nc or ''),'head',(nc or '')[:44])
for name in ('cursor','next_cursor','after','page_cursor','start_cursor'):
    for enc in (False,True):
        v=up.quote(nc,safe='') if enc else nc
        c2,b2=get(G+'?closed=false&limit=5&%s=%s'%(name,v))
        try:
            j2=json.loads(b2); ids=[m['conditionId'][:12] for m in j2['markets']]
        except Exception:
            print('  %-12s enc=%-5s -> %d  %s'%(name,enc,c2,b2[:90])); continue
        print('  %-12s enc=%-5s -> %d  advanced=%-5s ids %s'%(name,enc,c2,ids!=ids0,ids[:3]))
print()
print('--- the other pager: /markets with offset ---')
for off in (0,100,1000,2000,2100):
    c3,b3=get('https://gamma-api.polymarket.com/markets?closed=false&limit=5&offset=%d'%off)
    try:
        j3=json.loads(b3)
        arr=j3 if isinstance(j3,list) else j3.get('markets',[])
        print('  offset=%-5d -> %d  n=%d  ids %s'%(off,c3,len(arr),[m.get('conditionId','')[:10] for m in arr][:2]))
    except Exception:
        print('  offset=%-5d -> %d  %s'%(off,c3,b3[:110]))
