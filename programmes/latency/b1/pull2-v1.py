"""B1 - the universe, paged to real exhaustion on both venues.

Two paging traps found and worked around, both recorded:
  gamma  limit=500 SILENTLY returns 100, and offset>~2000 returns 422 pointing at
         /markets/keyset. Cursor paging is the only complete route.
  kalshi status=open is flooded with KXMVE* combinatorials; excluded a priori.
Only cursor_exhausted or empty_page may be read as a complete answer.
"""
import subprocess,json,time,os,collections
UA='smart-money-research/1.0 (+B1 universe; contact rogerlgk@gmail.com)'
CK='b1/ck.json'
st=json.load(open(CK)) if os.path.exists(CK) else {'kalshi':{'cur':'','pages':0,'stop':None},'pm':{'cur':'','pages':0,'stop':None},'hist':{}}
H=collections.Counter(st['hist'])
def get(u,t=40,tries=5):
    for i in range(tries):
        r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','--max-time',str(t),'-w','\n%{http_code}',u],capture_output=True,text=True)
        b,_,c=r.stdout.rpartition('\n')
        try: c=int(c)
        except Exception: c=-1
        H['http_%d'%c]+=1
        if c==200: return c,b
        if c in (429,500,502,503,504,-1): H['retry']+=1; time.sleep(0.8*(i+1)); continue
        return c,b
    return c,b
K='https://api.elections.kalshi.com/trade-api/v2'
BUD=float(os.environ.get('BUD','42')); t0=time.time()
kf=open('b1/kalshi.jsonl','a'); pf=open('b1/pm.jsonl','a')
while st['kalshi']['stop'] is None and time.time()-t0<BUD:
    cur=st['kalshi']['cur']
    c,b=get(K+'/markets?status=open&limit=1000'+('&cursor='+cur if cur else ''))
    if c!=200: st['kalshi']['stop']='http_%d'%c; break
    j=json.loads(b); mk=j.get('markets',[]); st['kalshi']['pages']+=1
    for m in mk:
        if m['ticker'].startswith('KXMVE'): continue
        kf.write(json.dumps({'venue':'kalshi','id':m['ticker'],'event':m.get('event_ticker'),'title':m.get('title'),
          'sub':m.get('yes_sub_title'),'rules':(m.get('rules_primary') or ''),'rules2':(m.get('rules_secondary') or ''),
          'close':m.get('close_time'),'oi':float(m.get('open_interest_fp') or 0),'vol24':float(m.get('volume_24h_fp') or 0),
          'vol':float(m.get('volume_fp') or 0),'liq':float(m.get('liquidity_dollars') or 0),'ask':m.get('yes_ask_dollars')})+'\n')
    nc=j.get('cursor') or ''
    if not nc: st['kalshi']['stop']='cursor_exhausted'
    elif not mk: st['kalshi']['stop']='empty_page'
    st['kalshi']['cur']=nc
    time.sleep(0.15)
while st['pm']['stop'] is None and time.time()-t0<BUD:
    cur=st['pm']['cur']
    c,b=get('https://gamma-api.polymarket.com/markets/keyset?closed=false&limit=100'+('&cursor='+cur if cur else ''))
    if c!=200: st['pm']['stop']='http_%d'%c; break
    j=json.loads(b); mk=j.get('markets',[]); st['pm']['pages']+=1
    for m in mk:
        pf.write(json.dumps({'venue':'polymarket','id':str(m.get('conditionId')),'event':(m.get('slug') or ''),
          'title':m.get('question'),'sub':'','rules':(m.get('description') or ''),'rules2':'',
          'close':m.get('endDateIso') or m.get('endDate'),'oi':0.0,'vol24':float(m.get('volume24hr') or 0),
          'vol':float(m.get('volumeNum') or 0),'liq':float(m.get('liquidityNum') or 0),'ask':m.get('bestAsk')})+'\n')
    nc=j.get('next_cursor') or ''
    if not nc: st['pm']['stop']='cursor_exhausted'
    elif not mk: st['pm']['stop']='empty_page'
    st['pm']['cur']=nc
    time.sleep(0.15)
kf.close(); pf.close(); st['hist']=dict(H); json.dump(st,open(CK,'w'))
nk=sum(1 for _ in open('b1/kalshi.jsonl')); npm=sum(1 for _ in open('b1/pm.jsonl'))
print('kalshi pages %-4d stop=%-18s rows %d'%(st['kalshi']['pages'],st['kalshi']['stop'],nk))
print('polymkt pages %-4d stop=%-18s rows %d'%(st['pm']['pages'],st['pm']['stop'],npm))
print('hist',json.dumps(dict(H)))
