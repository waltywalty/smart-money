import json,re,collections,random
URL=re.compile(r'https?://[^\s\)\]"<>,;]+')
VENUE=('polymarket.com','polymarket-upload.s3','xtracker.polymarket')
DESIG=re.compile(r'(resolution source[^.]{0,200}?|will be resolved (?:using|by|according to)[^.]{0,160}?|available at\s+)(https?://[^\s\)\]"<>,;]+)',re.I|re.S)
CRED=re.compile(r'consensus of credible reporting|credible reporting',re.I)
OFFI=re.compile(r'\bofficial\b',re.I)
def urls(t):
    out=[]
    for u in URL.findall(t or ''):
        u=u.rstrip('.,;')
        if any(v in u.lower() for v in VENUE): continue
        if u not in out: out.append(u)
    return out
def classify(d):
    rs=(d.get('resolutionSource') or '').strip()
    desc=(d.get('description') or '')
    cred=bool(CRED.search(desc))
    cand=None
    if rs and rs.lower().startswith('http') and not any(v in rs.lower() for v in VENUE): cand=rs.split()[0]
    if cand is None:
        m=DESIG.search(desc)
        if m and not any(v in m.group(2).lower() for v in VENUE): cand=m.group(2).rstrip('.,;')
    if cand is None:
        u=urls(desc)
        if len(u)==1: cand=u[0]
    if cand:
        import urllib.parse as up
        p=up.urlparse(cand); pa=(p.path or '').strip('/')
        if pa and pa.lower() not in ('index.html','home','en','index.php'):
            return 1,'designated url with a specific path',cand
        return 2,'designated url but homepage only',cand
    if rs: return 2,'named source, not a url: %s'%rs[:40],''
    if len(urls(desc))>1: return 2,'%d urls, must be reconciled'%len(urls(desc)),''
    if cred: return 3,'consensus of credible reporting, no url',''
    if OFFI.search(desc): return 2,'official body named in prose, no url',''
    return 4,'no source named',''
U={}
for fn in ('b1/v2/pm_top_v24.jsonl','b1/v2/pm_top_liq.jsonl','b1/v2/pm_top_vol.jsonl'):
    for ln in open(fn):
        d=json.loads(ln); U[d['conditionId']]=d
cls=collections.Counter(); v24=collections.Counter(); liq=collections.Counter(); vol=collections.Counter()
urlc=collections.Counter(); rows=[]
for d in U.values():
    c,why,u=classify(d)
    cls[c]+=1; v24[c]+=float(d.get('volume24hr') or 0); liq[c]+=float(d.get('liquidityNum') or 0); vol[c]+=float(d.get('volumeNum') or 0)
    if c==1 and u: urlc[u]+=1
    rows.append((c,d.get('slug'),why,u,float(d.get('volume24hr') or 0),float(d.get('liquidityNum') or 0)))
N={1:'1 named single official page/feed  [IN SCOPE]',2:'2 official, needs interpretation',3:'3 credible reporting',4:'4 unspecified'}
T=sum(cls.values())
print('POLYMARKET  money-bearing union of top-2100 by 24h vol / liquidity / lifetime vol: %d markets'%T)
print('%-44s %8s %7s %14s %15s %16s'%('class','markets','share','24h vol $','liquidity $','lifetime vol $'))
for c in (1,2,3,4):
    print('%-44s %8d %6.1f%% %14s %15s %16s'%(N[c],cls[c],100.0*cls[c]/T,'{:,.0f}'.format(v24[c]),'{:,.0f}'.format(liq[c]),'{:,.0f}'.format(vol[c])))
print('%-44s %8d %6.1f%% %14s %15s %16s'%('TOTAL',T,100.0,'{:,.0f}'.format(sum(v24.values())),'{:,.0f}'.format(sum(liq.values())),'{:,.0f}'.format(sum(vol.values()))))
print()
print('class 1 collapses to %d distinct urls.  top 18:'%len(urlc))
for u,n in urlc.most_common(18): print('   %5d  %s'%(n,u[:96]))
json.dump({'url_mk':dict(urlc)},open('b1/v2/pm_class1_urls2.json','w'))
print()
random.seed(20260818)
print('AUDIT SAMPLE 5 per class:')
for c in (1,2,3,4):
    p=[r for r in rows if r[0]==c]
    for r in random.sample(p,min(5,len(p))): print('  [%d] %-52s %s %s'%(c,(r[1] or '')[:52],r[2][:44],(r[3] or '')[:46]))
