"""Cross-check: Kalshi carries settlement_sources on the EVENT object and again on the
SERIES object.  The standing rule is to check a finding against a DIFFERENT endpoint,
never a second call to the same one.  They disagree on 19.2% of open events, and the
disagreement moves the class-1 count by 10.6%.  Nothing in either response says which
is authoritative, so the defensible figure is the intersection.
Usage: python3 crosscheck_event_series.py   (reads events.jsonl, series.jsonl, kalshi.jsonl)
"""
import json,collections,urllib.parse as up
VENUE={'kalshi.com','polymarket.com','assets.kalshi.com'}
NOT_A_SOURCE={('x.com','home'),('twitter.com','home'),('google.com','search'),('bing.com','search')}
def parse(u):
    p=up.urlparse((u or '').strip()); h=p.netloc.lower()
    if h.startswith('www.'): h=h[4:]
    return h,(p.path or '').strip('/')
def cls(srcs):
    srcs=[s for s in (srcs or []) if (s.get('url') or '').strip() or (s.get('name') or '').strip()]
    if not srcs: return 4,''
    P=[parse(s.get('url')) for s in srcs]
    if all(h in VENUE or not h for h,_ in P): return 4,''
    if len(srcs)==1:
        h,pa=P[0]
        if not h or h in VENUE: return 4,''
        if (h,pa.split('/')[0]) in NOT_A_SOURCE: return 4,''
        return (1,(srcs[0].get('url') or '').strip()) if pa else (2,'')
    return 2,''
def norm(ss): return tuple(sorted((s.get('url') or '').strip().rstrip('/').lower() for s in (ss or [])))
ser={}
for ln in open('b1/v2/series.jsonl'):
    d=json.loads(ln)
    if '_http' not in d: ser[d['ticker']]=d
ev={}
for ln in open('b1/v2/events.jsonl'):
    d=json.loads(ln); ev[d['event_ticker']]=d
mkc=collections.Counter()
for ln in open('b1/kalshi.jsonl'): mkc[json.loads(ln).get('event')]+=1
agree=diff=0; wa=wd=0; chg=collections.Counter()
for t,e in ev.items():
    s=ser.get(e.get('series_ticker'))
    if s is None: continue
    w=mkc.get(t,0)
    if norm(e.get('settlement_sources'))==norm(s.get('settlement_sources')): agree+=1; wa+=w
    else:
        diff+=1; wd+=w
        chg[(cls(e.get('settlement_sources'))[0],cls(s.get('settlement_sources'))[0])]+=w
print('events identical %d  different %d (%.1f%%)   markets identical %d different %d'%(agree,diff,100.0*diff/(agree+diff),wa,wd))
print('class shift event->series, weighted by markets:',chg.most_common())
ce=cs=cb=0; oe=osr=ob=0.0; ub=collections.Counter(); ubo=collections.Counter()
for ln in open('b1/kalshi.jsonl'):
    m=json.loads(ln); e=ev.get(m.get('event'))
    if e is None: continue
    o=float(m['oi'])
    a,ua=cls(e.get('settlement_sources')); b,ubu=cls((ser.get(e.get('series_ticker')) or {}).get('settlement_sources'))
    if a==1: ce+=1; oe+=o
    if b==1: cs+=1; osr+=o
    if a==1 and b==1: cb+=1; ob+=o; ub[ua]+=1; ubo[ua]+=o
print('class1 event %d ($%.0f)  series %d ($%.0f)  both %d ($%.0f)  urls %d'%(ce,oe,cs,osr,cb,ob,len(ub)))
json.dump({'url_mk':dict(ub),'url_oi':dict(ubo),'url_v24':{k:0 for k in ub}},open('b1/v2/class1_both_urls.json','w'))
