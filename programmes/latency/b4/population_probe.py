"""B4: the frozen population is the dependency worth watching hardest.

`programmes/latency/b3/population.json` freezes 125 urls, and urls rot.  A url that quietly
stops resolving is indistinguishable, in the detection data, from a source that never
publishes - so the decay is dated rather than assumed.

**WHERE the probe runs from is part of the measurement.**  Run #1 (research VM) read 125 of
125 resolving.  Run #2 (GitHub CI runner) read 119 - and all six "failures" returned 200 or
206 from the VM minutes later.  Shared runner IPs are refused by anti-bot layers that do not
refuse the VM.  A persistent 403 is exactly what real rot looks like, so:

  * rows are comparable ONLY within a vantage, and
  * a url counts as decayed only when it fails from BOTH.

Every run therefore writes its own per-url reading to `b4/data/last_<vantage>.json`, reads
the other vantage's most recent reading, and carries the comparison - including how stale
the other reading is, because a comparison against a week-old baseline is not a comparison.

Refusal headers (`server`, `cf-ray`, `retry-after`) are captured on every non-2xx, so the
*kind* of block is on the record: an IP-reputation bounce and a blanket datacenter ban look
identical as a status code and behave completely differently over time.
"""
import json,subprocess,hashlib,os,time,collections
import urllib.parse as up
from concurrent.futures import ThreadPoolExecutor
UA='smart-money-research/1.0 (+B4 population-decay probe; contact rogerlgk@gmail.com)'
ROOT=os.environ.get('REPO_ROOT','.')
P=os.path.join(ROOT,'programmes/latency/b3/population.json')
S=os.path.join(ROOT,'programmes/latency/b2/data/strata_volatility.json')
D=os.path.join(ROOT,'programmes/latency/b4/data')
LOG=os.path.join(ROOT,'programmes/latency/b4/POPULATION-DECAY.md')
IMP='/__b4_impossible_control__'
VANTAGE='ci' if os.environ.get('GITHUB_ACTIONS')=='true' else 'vm'
OTHER='vm' if VANTAGE=='ci' else 'ci'
def base(u):
    p=up.urlparse(u); return p.scheme+'://'+p.netloc
def fetch(u,t=25,tries=3):
    # A single shot conflates a transient failure with decay.  NEVER text=True: a gzip or
    # PDF body raises UnicodeDecodeError, the except swallows it, and a source that
    # answered 206 is recorded as unreachable.
    last=(-1,'',{})
    for i in range(tries):
        try:
            r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','-L','--max-redirs','5','-r','0-8191','-D','-','--max-time',str(t),'-w',chr(10)+'%{http_code}',u],capture_output=True,timeout=40)
        except Exception:
            time.sleep(1.0*(i+1)); continue
        s=r.stdout.decode('utf-8','replace')
        body,_,c=s.rpartition(chr(10))
        code=int(c) if c.isdigit() else -1
        hdr={}
        for line in body.splitlines():
            L=line.lower()
            for k in ('server:','cf-ray:','retry-after:','x-served-by:'):
                if L.startswith(k): hdr[k.rstrip(':')]=line.split(':',1)[1].strip()[:48]
        last=(code,body,hdr)
        if code!=-1 and code<500: return last
        time.sleep(1.0*(i+1))
    return last
urls=json.load(open(P))
meta={r['url']:r for r in json.load(open(S))} if os.path.exists(S) else {}
hosts=sorted({base(u) for u in urls})
ctl={}
with ThreadPoolExecutor(max_workers=6) as ex:
    for h,(c,b,_h) in zip(hosts,ex.map(lambda h: fetch(h+IMP),hosts)):
        ctl[h]=(c,hashlib.sha256(b.encode('utf-8','replace')).hexdigest())
res={}
with ThreadPoolExecutor(max_workers=6) as ex:
    for u,(c,b,hdr) in zip(urls,ex.map(fetch,urls)):
        h=base(u); cc,ch=ctl[h]
        sep = cc in (404,410) or hashlib.sha256(b.encode('utf-8','replace')).hexdigest()!=ch
        res[u]={'code':c,'ctl':cc,'sep':sep,'ok':(200<=c<300) and sep}
        if not res[u]['ok'] and hdr: res[u]['hdr']=hdr
ok=[u for u in urls if res[u]['ok']]
not2xx=[u for u in urls if not (200<=res[u]['code']<300)]
void=[u for u in urls if (200<=res[u]['code']<300) and not res[u]['sep']]
os.makedirs(D,exist_ok=True)
stamp=time.strftime('%Y-%m-%dT%H:%MZ',time.gmtime())
now=int(time.time())
failed=sorted(u for u in urls if not res[u]['ok'])
# --- the vantage comparison ---
# The CI workflow commits ONLY POPULATION-DECAY.md, so the per-run state lives INSIDE that
# file as a fenced json block.  A separate data file would be written by CI and never
# committed, and the comparison would silently never populate - which is the same class of
# failure this probe exists to catch.
prev={}
if os.path.exists(LOG):
    txt=open(LOG).read()
    for blk in txt.split('```b4state')[1:]:
        try: d=json.loads(blk.split('```')[0])
        except Exception: continue
        if d.get('vantage')==OTHER and d.get('epoch',0)>=prev.get('epoch',0): prev=d
cmp_txt='no %s reading yet'%OTHER
both=[]
if prev:
    age=(now-prev.get('epoch',0))/3600.0
    theirs=set(prev.get('failed',[]))
    mine=set(failed)
    both=sorted(mine&theirs)
    cmp_txt='%d both, %d %s-only, %d %s-only (%s %.1fh old)'%(len(both),len(mine-theirs),VANTAGE,len(theirs-mine),OTHER,OTHER,age)
def agg(S_):
    return sum(meta.get(u,{}).get('markets',0) for u in S_), sum(meta.get(u,{}).get('oi',0.0) for u in S_)
mk_ok,oi_ok=agg(ok); mk_both,oi_both=agg(both)
new=not os.path.exists(LOG)
with open(LOG,'a') as f:
    if new:
        f.write('# B4 - population decay log\n\n')
        f.write('One row per run, appended, never edited.  `resolving` requires 2xx **and** a\n')
        f.write('separating control on that host.  Rows are comparable **only within a vantage**;\n')
        f.write('a url counts as **decayed only when it fails from both**.\n\n')
        f.write('| run (UTC) | from | urls | resolving | not 2xx | control void | vs other vantage | DECAYED (both) | markets resolving |\n')
        f.write('|---|---|---:|---:|---:|---:|---|---:|---:|\n')
    f.write('| %s | %s | %d | **%d** | %d | %d | %s | **%d** | %d |\n'%(stamp,VANTAGE,len(urls),len(ok),len(not2xx),len(void),cmp_txt,len(both),mk_ok))
    if not2xx:
        f.write('\n<details><summary>%s [%s] - not 2xx (%d)</summary>\n\n'%(stamp,VANTAGE,len(not2xx)))
        for u in sorted(not2xx,key=lambda u:-meta.get(u,{}).get('oi',0)):
            hd=res[u].get('hdr',{})
            tag=' '.join('%s=%s'%(k,v) for k,v in sorted(hd.items())) or '-'
            f.write('- `%d` %s  (%d markets, $%s)  `%s`\n'%(res[u]['code'],u,meta.get(u,{}).get('markets',0),'{:,.0f}'.format(meta.get(u,{}).get('oi',0.0)),tag[:110]))
        f.write('\n</details>\n')
    f.write('\n```b4state\n'+json.dumps({'vantage':VANTAGE,'stamp':stamp,'epoch':now,'resolving':len(ok),'failed':failed})+'\n```\n')
    if both:
        f.write('\n**%s - FAILED FROM BOTH VANTAGES (%d urls, %d markets, $%s) - this is the decay signal:**\n\n'%(stamp,len(both),mk_both,'{:,.0f}'.format(oi_both)))
        for u in both: f.write('- %s\n'%u)
print('%s [%s]  urls %d  resolving %d  not2xx %d  control-void %d'%(stamp,VANTAGE,len(urls),len(ok),len(not2xx),len(void)))
print('  vs other vantage: %s'%cmp_txt)
print('  DECAYED (failed from both): %d urls, %d markets'%(len(both),mk_both))
print('  control separated on %d of %d hosts'%(sum(1 for h in hosts if ctl[h][0] in (404,410)),len(hosts)))
