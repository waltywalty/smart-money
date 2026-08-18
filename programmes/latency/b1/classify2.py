"""B1 step 3-4, second rule set.  The first one was wrong in BOTH directions and the
audit sample is what showed it:
  FALSE NEGATIVE  google.com/finance/quote/NDX:INDEXNASDAQ (2,921 markets) and
                  apnews.com/hub/ap-top-25-college-football-poll (323) are named
                  single canonical pages.  Demoting them on the DOMAIN was wrong.
  FALSE POSITIVE  nass.org/can-I-vote (3,954 markets - the single largest class-1
                  bucket) is a voter-information portal.  It carries no result.
So the domain is not the discriminator; the presence of a specific path is, and even
that only bounds the answer from above.  Rule set two is therefore PURELY structural
and is reported as an UPPER BOUND, to be narrowed by actually fetching the distinct
URLs.  A homepage is demoted whatever the domain; a specific path is class 1 whatever
the domain; a search QUERY string and a personalised endpoint are not sources.
"""
import json,collections,urllib.parse as up,random
VENUE={'kalshi.com','polymarket.com','assets.kalshi.com'}
NOT_A_SOURCE={('x.com','home'),('twitter.com','home'),('google.com','search'),('bing.com','search')}
def parse(u):
    p=up.urlparse((u or '').strip()); h=p.netloc.lower()
    if h.startswith('www.'): h=h[4:]
    return h,(p.path or '').strip('/'),(p.query or '')
def classify(srcs):
    srcs=[s for s in (srcs or []) if (s.get('url') or '').strip() or (s.get('name') or '').strip()]
    if not srcs: return 4,'no settlement source','' 
    P=[parse(s.get('url')) for s in srcs]
    if all(h in VENUE or not h for h,_,_ in P): return 4,'source is the venue itself',''
    if len(srcs)==1:
        h,pa,q=P[0]
        if not h or h in VENUE: return 4,'no host, or the venue itself',''
        if (h,pa.split('/')[0]) in NOT_A_SOURCE: return 4,'a query or a personalised endpoint, not a source',''
        if pa: return 1,'single named source, specific path','%s/%s'%(h,pa)
        return 2,'single named source, homepage only',h
    deep=[x for x in P if x[1]]
    return 2,'%d sources must be reconciled (%d with a specific path)'%(len(P),len(deep)),''
ev={}
for ln in open('b1/v2/events.jsonl'):
    d=json.loads(ln); ev[d['event_ticker']]=d
cls=collections.Counter(); oi=collections.Counter(); v24=collections.Counter()
liveN=collections.Counter(); liveOI=collections.Counter(); liveV=collections.Counter()
unmatched=0; url_mk=collections.Counter(); url_oi=collections.Counter(); url_v24=collections.Counter()
catby=collections.defaultdict(collections.Counter); rows=[]
for ln in open('b1/kalshi.jsonl'):
    m=json.loads(ln); e=ev.get(m.get('event'))
    if e is None: unmatched+=1; continue
    c,why,key=classify(e.get('settlement_sources'))
    o=float(m['oi']); v=float(m['vol24'])
    cls[c]+=1; oi[c]+=o; v24[c]+=v
    if v>0: liveN[c]+=1; liveOI[c]+=o; liveV[c]+=v
    catby[c][e.get('category') or '?']+=1
    if c==1:
        u=(e['settlement_sources'][0].get('url') or '').strip()
        url_mk[u]+=1; url_oi[u]+=o; url_v24[u]+=v
    rows.append((c,m['id'],e.get('series_ticker'),why,key,o,v))
N={1:'1 named single official page/feed  [IN SCOPE]',2:'2 official, needs interpretation',3:'3 credible reporting',4:'4 unspecified'}
T=sum(cls.values())
print('='*104)
print('KALSHI  open non-MVE markets: %d classified, %d unmatched to an open event (0.07%%)'%(T,unmatched))
print('%-44s %8s %7s %15s %14s %9s %14s'%('class','markets','share','open interest $','24h vol $','w/vol24','their OI $'))
for c in (1,2,3,4):
    print('%-44s %8d %6.1f%% %15s %14s %9d %14s'%(N[c],cls[c],100.0*cls[c]/T,'{:,.0f}'.format(oi[c]),'{:,.0f}'.format(v24[c]),liveN[c],'{:,.0f}'.format(liveOI[c])))
print('%-44s %8d %6.1f%% %15s %14s %9d %14s'%('TOTAL',T,100.0,'{:,.0f}'.format(sum(oi.values())),'{:,.0f}'.format(sum(v24.values())),sum(liveN.values()),'{:,.0f}'.format(sum(liveOI.values()))))
print()
print('class 3 is now EMPTY BY CONSTRUCTION - rule set two has no news-domain test.')
print('Where the old rule put news domains:')
for c in (1,2,4): print('   class %d categories: %s'%(c,catby[c].most_common(6)))
print()
print('CLASS 1 COLLAPSES TO %d DISTINCT URLs.  Top 25 by market count:'%len(url_mk))
print('  %7s %15s %13s  %s'%('markets','open interest $','24h vol $','url'))
for u,n in url_mk.most_common(25):
    print('  %7d %15s %13s  %s'%(n,'{:,.0f}'.format(url_oi[u]),'{:,.0f}'.format(url_v24[u]),u[:88]))
json.dump({'url_mk':dict(url_mk),'url_oi':dict(url_oi),'url_v24':dict(url_v24)},open('b1/v2/class1_urls.json','w'))
json.dump([{'cls':r[0],'id':r[1],'series':r[2],'why':r[3],'key':r[4],'oi':r[5],'vol24':r[6]} for r in rows],open('b1/v2/kalshi_classified2.json','w'))
