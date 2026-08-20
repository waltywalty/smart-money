"""B2: the false-positive floor.  How often does an in-scope resolution page change
when nothing has happened?

Four rounds at T+0, +5, +15, +60 minutes.  Every round fetches the target AND an
impossible path on the same host.  **The impossible path is the control: it cannot
have changed for a real reason, so whatever rate IT changes at is the floor below
which a target change means nothing.**

Compliance: paths disallowed by robots.txt are excluded outright (measured 2026-08-20,
14 hosts / 204 markets).  The minimum gap per host is 5 minutes, which exceeds every
declared Crawl-delay in the corpus (max 60s), so no additional throttle is needed.

Two hashes per fetch:
  raw  - sha256 of the whole body
  norm - sha256 after stripping <script>/<style> blocks and HTML comments and
         collapsing whitespace.  A page whose raw hash moves but whose norm hash does
         not is churning on markup, not on content.
"""
import json,subprocess,hashlib,re,time,os,collections,urllib.parse as up
from concurrent.futures import ThreadPoolExecutor
UA='smart-money-research/1.0 (+B2 change detection; contact rogerlgk@gmail.com)'
SCRIPT=re.compile(r'<(script|style)\b.*?</\1>',re.I|re.S)
COMMENT=re.compile(r'<!--.*?-->',re.S)
WS=re.compile(r'\s+')
def norm(b):
    b=SCRIPT.sub(' ',b or ''); b=COMMENT.sub(' ',b); return WS.sub(' ',b).strip()
def fetch(u,t=25):
    try:
        r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','-L','--max-redirs','5','--max-time',str(t),'-w',chr(10)+'%{http_code}',u],capture_output=True,timeout=40)
    except Exception:
        return {'url':u,'code':-1}
    b,_,c=r.stdout.decode('utf-8','replace').rpartition(chr(10))
    return {'url':u,'code':(int(c) if c.isdigit() else -1),'len':len(b or ''),
            'raw':hashlib.sha256((b or '').encode('utf-8','replace')).hexdigest()[:32],
            'norm':hashlib.sha256(norm(b).encode('utf-8','replace')).hexdigest()[:32]}
# --- build the work list, honouring robots ---
blocked=set()
for ln in open('b2/robots.jsonl'):
    d=json.loads(ln)
    if d['n_blocked']: blocked.add(d['base'])
urls=[]; hosts=set()
for fn in ('b1/v2/class1_both_urls.json','b1/v2/pm_class1_urls2.json'):
    for u in json.load(open(fn))['url_mk']:
        p=up.urlparse(u); b=p.scheme+'://'+p.netloc
        if b in blocked: continue
        urls.append(u); hosts.add(b)
urls=sorted(set(urls)); hosts=sorted(hosts)
ctl=[h+'/__impossible_control_20260820__' for h in hosts]
work=[('target',u) for u in urls]+[('control',u) for u in ctl]
print('targets %d  impossible-path controls %d  (robots-excluded hosts: %d)'%(len(urls),len(ctl),len(blocked)),flush=True)
SCHED=[0,300,900,3600]
CK='b2/change_ck.json'
st=json.load(open(CK)) if os.path.exists(CK) else {'t0':None,'done':[]}
if st['t0'] is None: st['t0']=time.time(); json.dump(st,open(CK,'w'))
out=open('b2/change.jsonl','a')
for i,off in enumerate(SCHED):
    if i in st['done']: continue
    due=st['t0']+off
    while time.time()<due: time.sleep(min(20,due-time.time()))
    ts=time.time()
    with ThreadPoolExecutor(max_workers=6) as ex:
        for kind,r in zip([k for k,_ in work],ex.map(lambda w: fetch(w[1]),work)):
            r['round']=i; r['kind']=kind; r['ts']=round(ts,1)
            out.write(json.dumps(r)+chr(10))
    out.flush(); st['done'].append(i); json.dump(st,open(CK,'w'))
    print('round %d (T+%ds) done at %.0f'%(i,off,ts),flush=True)
out.close(); print('ALL ROUNDS DONE',flush=True)
