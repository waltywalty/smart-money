"""B3 stratum split, per the 2026-08-20 ruling.

  SCHEDULED   - the source publishes on a calendar and you know the instant.
                CPI 08:30 ET, FOMC 14:00 ET, BEA GDP, Treasury daily curve.
                Poll hard in a narrow window.  HFT already lives there.
  UNSCHEDULED - it will happen, but not at an announced moment.  Court dockets,
                FDA press announcements, election certifications, USGS events.
                Needs continuous polling.  Genuinely uncontested.
  UNKNOWN     - not matched by a stated rule.  NOT forced into a bucket.

The two have opposite cost structures and opposite competition, so pooling them would
average an HFT race against an empty field.

The rule is over the SOURCE, because that is what the distinction is about.  Kalshi's
series `frequency` is reported alongside as a weak cross-check only: it describes the
MARKET's cadence, not the source's release schedule - `home.treasury.gov` daily yields
carries markets marked one_off, and `oscars.org` carries 21 annual and 9 one_off.
"""
import json,collections,re,random,urllib.parse as up
SCHED_HOST={'www.bls.gov','data.bls.gov','www.bea.gov','apps.bea.gov','www.eia.gov','www.census.gov',
 'fred.stlouisfed.org','home.treasury.gov','www.fhfa.gov','www.billboard.com','hitsdailydouble.com',
 'www.wunderground.com','weather.com','eng.koreabaseball.com','www.oscars.org','www.emmys.com',
 'nces.ed.gov','www.federalreserve.gov','ec.europa.eu','www.ons.gov.uk','www.statcan.gc.ca',
 'baseballsavant.mlb.com','www.theice.com','www.ice.com','newsroom.spotify.com','apps.apple.com'}
UNSCHED_HOST={'www.fda.gov','www.whitehouse.gov','www.who.int','earthquake.usgs.gov','cneos.jpl.nasa.gov',
 'commission.europa.eu','georgerrmartin.com','www.justice.gov','www.supremecourt.gov','oklahoma.gov',
 'www.in.gov','www.sos.state.tx.us','sos.ca.gov','dos.fl.gov','elections.hawaii.gov','elections.ri.gov',
 'sos.texas.gov','www.michigan.gov','international.tse.jus.br','dumatv.ru','6abc.com','www.cdc.gov',
 'stacks.cdc.gov','arena.ai','lmarena.ai','app.parcllabs.com','claude.com','ai.google.dev','defillama.com',
 'app.rwa.xyz','www.sec.gov','secure.actblue.com','data.worldbank.org','gol.gg','dashboard.ornnai.com',
 'www.carbonarc.ai','www.carbonarc.co','portwatch.imf.org','pythdata.app','kenpom.com'}
UNSCHED_PATH=re.compile(r'/(elections?|docket|press-announcements|newsroom|executive-|nominations|situations|browse|fireballs|leaderboard)',re.I)
SCHED_PATH=re.compile(r'/(cpi|gdp|news\.release|calendars?|charts/|schedule|history/daily|quarterly|interest-rates)',re.I)
def host(u):
    h=up.urlparse(u).netloc.lower(); return h
def stratum(u):
    h=host(u); p=up.urlparse(u).path
    if h in SCHED_HOST: return 'SCHEDULED','host on the published-calendar list'
    if h in UNSCHED_HOST: return 'UNSCHEDULED','host publishes without an announced instant'
    if SCHED_PATH.search(p): return 'SCHEDULED','path names a calendared release'
    if UNSCHED_PATH.search(p): return 'UNSCHEDULED','path names an event stream'
    return 'UNKNOWN','no stated rule matched'
usable=[u for u in json.load(open('b2/usable_urls.json')) if u!='https://www.nass.org/can-I-vote']
mk={}; oi={}
for fn in ('b1/v2/class1_both_urls.json','b1/v2/pm_class1_urls2.json'):
    j=json.load(open(fn))
    for u,n in j['url_mk'].items():
        mk[u]=mk.get(u,0)+n; oi[u]=oi.get(u,0.0)+j.get('url_oi',{}).get(u,0.0)
S={}
for ln in open('b1/v2/series_subset.jsonl'):
    d=json.loads(ln)
    if '_http' not in d: S[d['ticker']]=d
byurl=json.load(open('b1/v2/usable_series.json'))['byurl']
G=collections.Counter(); GM=collections.Counter(); GO=collections.Counter(); rows=[]
for u in usable:
    s,why=stratum(u); G[s]+=1; GM[s]+=mk.get(u,0); GO[s]+=oi.get(u,0.0)
    rows.append({'url':u,'stratum':s,'why':why,'markets':mk.get(u,0),'oi':oi.get(u,0.0)})
T=sum(G.values()); TM=sum(GM.values()); TO=sum(GO.values())
print('%-14s %6s %9s %16s'%('stratum','urls','markets','open interest'))
for k in ('SCHEDULED','UNSCHEDULED','UNKNOWN'):
    print('%-14s %6d %9d %16s   %5.1f%% of urls, %5.1f%% of oi'%(k,G[k],GM[k],'{:,.0f}'.format(GO[k]),100.0*G[k]/T,100.0*GO[k]/max(1.0,TO)))
print('%-14s %6d %9d %16s'%('TOTAL',T,TM,'{:,.0f}'.format(TO)))
print()
X=collections.defaultdict(collections.Counter)
for r in rows:
    for t in byurl.get(r['url'],[]):
        if t in S: X[r['stratum']][S[t].get('frequency')]+=1
print('cross-check against Kalshi series frequency (describes the MARKET, not the source):')
for k in ('SCHEDULED','UNSCHEDULED','UNKNOWN'):
    if X[k]: print('   %-12s %s'%(k,dict(X[k].most_common())))
random.seed(20260820)
print()
print('AUDIT SAMPLE, 7 per stratum:')
for k in ('SCHEDULED','UNSCHEDULED','UNKNOWN'):
    pool=[r for r in rows if r['stratum']==k]
    for r in random.sample(pool,min(7,len(pool))):
        print('   [%-11s] %5d mk  %s'%(k,r['markets'],r['url'][:74]))
json.dump(rows,open('b2/strata.json','w'))
