"""B2: the rejection curve under SUSTAINED polling.

The concurrency result (170 urls, ~9s sweep at concurrency 8) is a BURST measurement.
Sustained, it is a request to a government host every nine seconds, indefinitely, and
no declared Crawl-delay is silence rather than permission.  This project's own finding
is that the rejection curve is a property of (endpoint, source, recent history) - so it
has to be measured, not assumed, before B3 depends on it.

Design:
  ARM A  7 hosts, one url each, one request every 9s for an hour - the load B3 would
         impose on a host that carries a single in-scope url.
  ARM B  wunderground, 6 urls per sweep every 9s - the many-urls-per-host case, which
         is n times heavier and is the real risk.

Control, matched on the confounder: on ARM A the request ALTERNATES between the target
and an impossible path on the same host, so total load is unchanged and any rejection
can be attributed to the host rather than to the page.  If both arms 429 together it is
host-level rate limiting; if only the target does, it is page-level.

Status codes are recorded, never availability.  A host that starts refusing is the
result, not a failure of the run.
"""
import json,subprocess,time,os,collections,sys
UA='smart-money-research/1.0 (+B2 sustained-polling study; contact rogerlgk@gmail.com)'
A=['https://www.bls.gov/bls/news-release/cpi.htm',
   'https://www.bea.gov/data/gdp/gross-domestic-product',
   'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm',
   'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve',
   'https://earthquake.usgs.gov/earthquakes/browse/',
   'https://www.eia.gov/coal/production/quarterly/',
   'https://oklahoma.gov/elections.html']
IMP='/__impossible_control_20260820__'
def base(u):
    i=u.index('/',8); return u[:i]
WU=[u for u in json.load(open('b2/usable_urls.json')) if 'wunderground.com' in u][:6]
STEP=9.0; DUR=float(os.environ.get('DUR','3600'))
out=open('b2/sustained.jsonl','a')
def hit(u):
    t0=time.time()
    try:
        r=subprocess.run(['curl','-sS','-o','/dev/null','-D','-','-A',UA,'-H','Expect:','--max-time','20','-w','|C|%{http_code}|%{time_total}',u],capture_output=True,text=True,timeout=30)
    except Exception as e:
        return {'url':u,'code':-1,'err':str(e)[:60],'ts':round(t0,1)}
    o=r.stdout or ''
    hdr,_,tail=o.rpartition('|C|')
    p=tail.split('|')
    code=int(p[0]) if p and p[0].isdigit() else -1
    tt=float(p[1]) if len(p)>1 and p[1].replace('.','',1).isdigit() else None
    ra=None; rl=None
    for line in hdr.splitlines():
        L=line.lower()
        if L.startswith('retry-after:'): ra=line.split(':',1)[1].strip()[:40]
        if 'ratelimit' in L and rl is None: rl=line.strip()[:70]
    return {'url':u,'code':code,'t':tt,'ts':round(t0,1),'retry_after':ra,'ratelimit':rl}
stop=set(); consec=collections.Counter(); n=0
t_start=time.time()
while time.time()-t_start<DUR:
    sweep_t=time.time(); n+=1
    batch=[]
    for u in A:
        if base(u) in stop: continue
        batch.append(('A', u if n%2==1 else base(u)+IMP, 'target' if n%2==1 else 'control'))
    for u in WU:
        if base(u) in stop: continue
        batch.append(('B',u,'target'))
    if n%2==0 and base(WU[0]) not in stop:
        batch.append(('B',base(WU[0])+IMP,'control'))
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=8) as ex:
        for meta,r in zip(batch,ex.map(lambda b: hit(b[1]),batch)):
            r['arm']=meta[0]; r['kind']=meta[2]; r['sweep']=n
            out.write(json.dumps(r)+chr(10))
            b=base(r['url'])
            if r['code'] in (429,403,503) or r['code']==-1:
                consec[b]+=1
                if consec[b]>=6:
                    stop.add(b); print('STOPPING %s after 6 consecutive refusals at sweep %d'%(b,n),flush=True)
            else: consec[b]=0
    out.flush()
    if n%20==0: print('sweep %d  t+%.0fs  stopped hosts %d'%(n,time.time()-t_start,len(stop)),flush=True)
    d=STEP-(time.time()-sweep_t)
    if d>0: time.sleep(d)
out.close(); print('SUSTAINED DONE sweeps %d stopped %s'%(n,sorted(stop)),flush=True)
