"""B4: the dependency worth watching hardest is not a source. It is the population file.

`programmes/latency/b3/population.json` freezes 125 urls, and urls rot - pages move,
departments restructure, series retire. **A url that quietly starts 404ing is
indistinguishable, in the detection data, from a source that simply never publishes.**
That is the same confusion between absence and failure this project has hit before, and
it would silently deflate every B3 rate without touching a single number.

So this probe dates the decay, the way the census dates the archive's stop: one row per
run, appended, never edited.

Every url is paired with an impossible path on the same host. Where the status control is
void (the host answers any path), the content control is used instead (P21). A url counts
as RESOLVING only if it returns 2xx **and** some control separates on its host - a 2xx from
a catch-all router is not evidence the page exists.

Runs from the repo root, in CI or locally. One request per url per run honours every
declared Crawl-delay in the corpus.
"""
import json,subprocess,hashlib,os,sys,time,collections
import urllib.parse as up
from concurrent.futures import ThreadPoolExecutor
UA='smart-money-research/1.0 (+B4 population-decay probe; contact rogerlgk@gmail.com)'
ROOT=os.environ.get('REPO_ROOT','.')
P=os.path.join(ROOT,'programmes/latency/b3/population.json')
S=os.path.join(ROOT,'programmes/latency/b2/data/strata_volatility.json')
LOG=os.path.join(ROOT,'programmes/latency/b4/POPULATION-DECAY.md')
IMP='/__b4_impossible_control__'
def base(u):
    p=up.urlparse(u); return p.scheme+'://'+p.netloc
def fetch(u,t=25,tries=3):
    # A single shot conflates a transient failure with decay.  The first seeded run
    # recorded weather.com/kalshi as -1; three immediate retries returned 206 in 0.3s.
    # A blip is not a curve, and a decay log full of false decay is worse than no log.
    last=(-1,'')
    for i in range(tries):
        try:
            r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','-L','--max-redirs','5','-r','0-8191','--max-time',str(t),'-w',chr(10)+'%{http_code}',u],capture_output=True,timeout=40)
        except Exception:
            time.sleep(1.0*(i+1)); continue
        # NEVER text=True.  A gzip or PDF body raises UnicodeDecodeError, the except
        # swallows it, and a source that answered 206 is recorded as unreachable.
        b,_,c=r.stdout.decode('utf-8','replace').rpartition(chr(10))
        code=int(c) if c.isdigit() else -1
        last=(code,(b or ''))
        if code!=-1 and code<500: return last
        time.sleep(1.0*(i+1))
    return last
urls=json.load(open(P))
meta={r['url']:r for r in json.load(open(S))} if os.path.exists(S) else {}
hosts=sorted({base(u) for u in urls})
ctl={}
with ThreadPoolExecutor(max_workers=6) as ex:
    for h,(c,b) in zip(hosts,ex.map(lambda h: fetch(h+IMP),hosts)):
        ctl[h]=(c,hashlib.sha256(b.encode('utf-8','replace')).hexdigest())
res={}
with ThreadPoolExecutor(max_workers=6) as ex:
    for u,(c,b) in zip(urls,ex.map(fetch,urls)):
        h=base(u); cc,ch=ctl[h]
        sep = cc in (404,410) or hashlib.sha256(b.encode('utf-8','replace')).hexdigest()!=ch
        res[u]={'code':c,'ctl':cc,'sep':sep,'ok':(200<=c<300) and sep}
ok=[u for u in urls if res[u]['ok']]
not2xx=[u for u in urls if not (200<=res[u]['code']<300)]
void=[u for u in urls if (200<=res[u]['code']<300) and not res[u]['sep']]
def agg(S_):
    return sum(meta.get(u,{}).get('markets',0) for u in S_), sum(meta.get(u,{}).get('oi',0.0) for u in S_)
mk_ok,oi_ok=agg(ok); mk_bad,oi_bad=agg(not2xx); mk_void,oi_void=agg(void)
stamp=time.strftime('%Y-%m-%dT%H:%MZ',time.gmtime())
new=not os.path.exists(LOG)
with open(LOG,'a') as f:
    if new:
        f.write('# B4 - population decay log\n\n')
        f.write('One row per run, appended, never edited. `resolving` requires 2xx **and** a\n')
        f.write('separating control on that host. A url that quietly 404s is indistinguishable\n')
        f.write('from a source that never publishes, so the decay is dated rather than assumed.\n\n')
        f.write('| run (UTC) | urls | resolving | not 2xx | 2xx, control void | markets resolving | OI resolving |\n')
        f.write('|---|---:|---:|---:|---:|---:|---:|\n')
    f.write('| %s | %d | **%d** | %d | %d | %d | $%s |\n'%(stamp,len(urls),len(ok),len(not2xx),len(void),mk_ok,'{:,.0f}'.format(oi_ok)))
    if not2xx:
        f.write('\n<details><summary>%s - not 2xx (%d)</summary>\n\n'%(stamp,len(not2xx)))
        for u in sorted(not2xx,key=lambda u:-meta.get(u,{}).get('oi',0)):
            f.write('- `%d` %s  (%d markets, $%s)\n'%(res[u]['code'],u,meta.get(u,{}).get('markets',0),'{:,.0f}'.format(meta.get(u,{}).get('oi',0.0))))
        f.write('\n</details>\n')
print('%s  urls %d  resolving %d  not2xx %d  control-void %d'%(stamp,len(urls),len(ok),len(not2xx),len(void)))
print('  markets resolving %d  open interest $%s'%(mk_ok,'{:,.0f}'.format(oi_ok)))
print('  at risk: not-2xx %d markets $%s ; control-void %d markets $%s'%(mk_bad,'{:,.0f}'.format(oi_bad),mk_void,'{:,.0f}'.format(oi_void)))
print('  control separated on %d of %d hosts'%(sum(1 for h in hosts if ctl[h][0] in (404,410)),len(hosts)))
