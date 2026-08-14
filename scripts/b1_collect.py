import sys, json, os, time, threading, urllib.request, urllib.error, urllib.parse
from concurrent.futures import ThreadPoolExecutor
BASE='https://api.elections.kalshi.com/trade-api/v2'
UA='smart-money-research/1.0 (+b1-historical-collection)'
OUT='/root/work/data/historical'
STATE='/root/work/data/state.json'
FIELDS=['ticker','event_ticker','close_time','open_time','settlement_ts','settlement_value_dollars',
        'result','expiration_value','market_type','strike_type','floor_strike','cap_strike',
        'yes_bid_dollars','yes_ask_dollars','no_bid_dollars','no_ask_dollars','last_price_dollars',
        'volume_fp','volume_24h_fp','open_interest_fp','status','title','subtitle']
_tl=threading.local()
def get(path, params, gap=0.55, tries=5):
    """Per-thread pacing: each worker waits `gap` between its own requests (packet: 3 threads @0.55s)."""
    url=BASE+path+'?'+urllib.parse.urlencode(params)
    last=getattr(_tl,'last',0.0)
    w=last+gap-time.time()
    if w>0: time.sleep(w)
    for a in range(tries):
        _tl.last=time.time()
        req=urllib.request.Request(url, method='GET')
        req.add_header('User-Agent',UA); req.add_header('Accept','application/json')
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                raw=r.read(); st=r.status
            try: return st, json.loads(raw)
            except Exception: return st, None
        except urllib.error.HTTPError as e:
            try: e.read()
            except Exception: pass
            e.close()
            if e.code in (429,500,502,503,504):
                time.sleep(min(8, 0.8*(2**a))); _tl.last=time.time(); continue
            return e.code, None
        except Exception:
            time.sleep(min(8, 0.6*(2**a))); _tl.last=time.time()
    return -1, None
lock=threading.Lock()
ST=json.load(open(STATE)) if os.path.exists(STATE) else {}
SER=json.load(open('/root/work/series.json'))
BUDGET=float(sys.argv[1]) if len(sys.argv)>1 else 46.0
T0=time.time()
def work(s):
    cur=ST.get(s)
    if cur and cur.get('stop') in ('cursor_exhausted','empty_page'): return None
    cur=cur or {'cursor':None,'pages':0,'rows':0,'kxmve':0,'stop':None,'codes':{}}
    fh=open(os.path.join(OUT,s+'.ndjson'),'a')
    try:
        while cur['stop'] is None:
            if time.time()-T0>BUDGET: break
            p={'series_ticker':s,'limit':1000}
            if cur['cursor']: p['cursor']=cur['cursor']
            code,j=get('/historical/markets',p)
            cur['codes'][str(code)]=cur['codes'].get(str(code),0)+1
            cur['pages']+=1
            if code!=200 or not isinstance(j,dict):
                cur['stop']='http_%s'%code; break
            ms=j.get('markets') or []
            buf=[]
            for m in ms:
                t=m.get('ticker') or ''
                if t.startswith('KXMVE'): cur['kxmve']+=1; continue
                row={k:m.get(k) for k in FIELDS if k in m}
                row['series_ticker']=s
                buf.append(json.dumps(row,separators=(',',':')))
            if buf: fh.write('\n'.join(buf)+'\n')
            cur['rows']+=len(buf)
            c=j.get('cursor')
            if not ms: cur['stop']='empty_page'
            elif not c: cur['stop']='cursor_exhausted'
            cur['cursor']=c
    finally:
        fh.close()
        with lock: ST[s]=cur
    return s
todo=[s for s in SER if not (ST.get(s) or {}).get('stop') in ('cursor_exhausted','empty_page')]
with ThreadPoolExecutor(max_workers=3) as ex:
    list(ex.map(work, todo))
json.dump(ST, open(STATE,'w'))
done=sum(1 for v in ST.values() if v.get('stop') in ('cursor_exhausted','empty_page'))
rows=sum(v.get('rows',0) for v in ST.values())
mve=sum(v.get('kxmve',0) for v in ST.values())
pages=sum(v.get('pages',0) for v in ST.values())
bad={k:v for k,v in ((s,c.get('stop')) for s,c in ST.items()) if v and not v.startswith(('cursor','empty'))}
codes={}
for v in ST.values():
    for k,n in v.get('codes',{}).items(): codes[k]=codes.get(k,0)+n
print('series done=%d/%d  rows=%d  kxmve_excluded=%d  pages=%d  codes=%s  elapsed=%.1fs'%(done,len(SER),rows,mve,pages,codes,time.time()-T0))
if bad: print('  non-terminal stops: %d e.g. %s'%(len(bad), list(bad.items())[:5]))
