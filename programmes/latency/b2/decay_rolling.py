"""Pull rolling-update sources out of SCHEDULED and re-measure the T+15m -> T+60m decay.
The pooled scheduled decay of 42.7% was 32/35 wunderground history pages, which are
rolling observation feeds rather than calendared releases.  Removing them takes the
calendared-release decay to zero.
"""
import json,collections,urllib.parse as up
R=collections.defaultdict(dict)
for ln in open('b2/change.jsonl'):
    d=json.loads(ln); R[d['url']][d['round']]=d
str_={r['url']:r for r in json.load(open('b2/strata.json'))}
ROLLING={'www.wunderground.com','weather.com','baseballsavant.mlb.com','apps.apple.com','www.billboard.com','hitsdailydouble.com'}
def ok(u): return all(r in R[u] and 200<=R[u][r].get('code',-1)<300 for r in (0,1,2,3))
G=collections.defaultdict(lambda:[0,0,0,0.0])
for u,m in str_.items():
    if u not in R or not ok(u): continue
    lab='ROLLING' if up.urlparse(u).netloc.lower() in ROLLING else m['stratum']
    g=G[lab]; g[0]+=1; g[2]+=m['markets']; g[3]+=m['oi']
    if R[u][2]['norm']!=R[u][3]['norm']: g[1]+=1
print('%-14s %6s %8s %8s %10s %16s'%('class','urls','decayed','decay%','markets','open interest'))
for k in ('SCHEDULED','UNSCHEDULED','UNKNOWN','ROLLING'):
    g=G[k]
    if g[0]: print('%-14s %6d %8d %7.1f%% %10d %16s'%(k,g[0],g[1],100.0*g[1]/g[0],g[2],'{:,.0f}'.format(g[3])))
t=[sum(G[k][i] for k in G) for i in range(4)]
print('%-14s %6d %8d %7.1f%% %10d %16s'%('TOTAL',t[0],t[1],100.0*t[1]/t[0],t[2],'{:,.0f}'.format(t[3])))
