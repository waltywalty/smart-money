"""B1 step 3-4: classify the resolution source, then count and value the universe.

Four classes, per the packet.  ONLY class 1 is in scope.
  1 named single official page or feed  - one source, a URL with a real path, not a
                                          news/search/venue domain.  A poller can be
                                          pointed at exactly one address.
  2 official but requiring interpretation- one official body but only a homepage, or
                                          2+ non-news sources that must be reconciled.
  3 'credible reporting'                 - the named sources are news organisations,
                                          or a search engine, in any number.
  4 unspecified                          - no source, or the source is the venue itself.

The URL-path test is the load-bearing one and it is structural, not semantic:
https://www.nfl.com resolves nothing by itself; you must know which page to read.
https://data.giss.nasa.gov/.../graph.txt is a fetchable answer.
"""
import json,collections,urllib.parse as up,random,sys

NEWS={'nytimes.com','apnews.com','reuters.com','axios.com','theguardian.com','bloomberg.com',
'cnn.com','bbc.com','bbc.co.uk','washingtonpost.com','wsj.com','nbcnews.com','abcnews.go.com',
'cbsnews.com','foxnews.com','politico.com','thehill.com','npr.org','usatoday.com','forbes.com',
'cnbc.com','ft.com','economist.com','variety.com','hollywoodreporter.com','deadline.com',
'newsweek.com','time.com','apnews.co','sportsillustrated.com','theathletic.com','yahoo.com',
'nypost.com','dailymail.co.uk','telegraph.co.uk','independent.co.uk','aljazeera.com',
'semafor.com','businessinsider.com','vulture.com','rollingstone.com','people.com','tmz.com',
'decider.com','ew.com','indiewire.com','thewrap.com','screenrant.com','collider.com'}
SEARCH={'google.com','google.co.uk','bing.com','duckduckgo.com','x.com','twitter.com',
'youtube.com','wikipedia.org','en.wikipedia.org','reddit.com','facebook.com','instagram.com',
'truthsocial.com','t.me','threads.net'}
VENUE={'kalshi.com','polymarket.com','assets.kalshi.com'}

def host(u):
    p=up.urlparse((u or '').strip())
    return p.netloc.lower().lstrip('www.') if p.netloc.lower().startswith('www.') else p.netloc.lower()
def path(u):
    p=up.urlparse((u or '').strip())
    return (p.path or '').strip('/')+ (('?'+p.query) if p.query else '')

def classify(srcs):
    """srcs: list of {name,url}. returns (class:int, why:str)"""
    srcs=[s for s in (srcs or []) if (s.get('url') or '').strip() or (s.get('name') or '').strip()]
    if not srcs: return 4,'no settlement source'
    hs=[host(s.get('url')) for s in srcs]
    if all(h in VENUE or not h for h in hs): return 4,'source is the venue itself'
    if len(srcs)==1:
        h,pa=hs[0],path(srcs[0].get('url'))
        if h in SEARCH: return 3,'single source is a search/social domain'
        if h in NEWS:   return 3,'single source is a news organisation'
        if h in VENUE or not h: return 4,'single source is the venue or has no host'
        if pa: return 1,'single official source with a specific path: %s/%s'%(h,pa[:60])
        return 2,'single official source but homepage only: %s'%h
    nn=sum(1 for h in hs if h in NEWS or h in SEARCH)
    if nn*2>=len(hs): return 3,'%d of %d named sources are news/search'%(nn,len(hs))
    return 2,'%d sources must be reconciled'%len(hs)

# ---------- KALSHI ----------
ev={}
for ln in open('b1/v2/events.jsonl'):
    d=json.loads(ln); ev[d['event_ticker']]=d
cls=collections.Counter(); oi=collections.Counter(); v24=collections.Counter(); vol=collections.Counter()
liveN=collections.Counter(); liveOI=collections.Counter()
unmatched=0; rows=[]
catby=collections.defaultdict(collections.Counter)
for ln in open('b1/kalshi.jsonl'):
    m=json.loads(ln); e=ev.get(m.get('event'))
    if e is None: unmatched+=1; continue
    c,why=classify(e.get('settlement_sources'))
    cls[c]+=1; oi[c]+=float(m['oi']); v24[c]+=float(m['vol24']); vol[c]+=float(m['vol'])
    if float(m['vol24'])>0: liveN[c]+=1; liveOI[c]+=float(m['oi'])
    catby[c][e.get('category') or '?']+=1
    rows.append((c,m['id'],e.get('series_ticker'),why,float(m['oi']),float(m['vol24'])))
NAMES={1:'1 named single official page/feed  [IN SCOPE]',2:'2 official, needs interpretation',3:'3 credible reporting',4:'4 unspecified'}
T=sum(cls.values())
print('='*100)
print('KALSHI  open non-MVE markets classified: %d   (unmatched to an open event: %d)'%(T,unmatched))
print('%-42s %8s %7s %16s %16s %10s'%('class','markets','share','open interest $','24h volume $','w/ vol24'))
for c in (1,2,3,4):
    print('%-42s %8d %6.1f%% %16s %16s %10d'%(NAMES[c],cls[c],100.0*cls[c]/T,'{:,.0f}'.format(oi[c]),'{:,.0f}'.format(v24[c]),liveN[c]))
print('%-42s %8d %6.1f%% %16s %16s %10d'%('TOTAL',T,100.0,'{:,.0f}'.format(sum(oi.values())),'{:,.0f}'.format(sum(v24.values())),sum(liveN.values())))
print()
for c in (1,2,3,4): print('  class %d categories: %s'%(c,catby[c].most_common(6)))
json.dump([{'cls':r[0],'id':r[1],'series':r[2],'why':r[3],'oi':r[4],'vol24':r[5]} for r in rows],open('b1/v2/kalshi_classified.json','w'))
print()
print('AUDIT SAMPLE (seed 20260818) - 6 per class, for hand checking:')
random.seed(20260818)
for c in (1,2,3,4):
    pool=[r for r in rows if r[0]==c]
    for r in random.sample(pool,min(6,len(pool))):
        print('  [%d] %-34s %-22s %s'%(c,r[1][:34],r[2],r[3][:78]))
