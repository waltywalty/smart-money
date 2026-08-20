"""B2 prep: robots.txt and Crawl-delay for every host behind an in-scope resolution
source.  This is the 'polling economics under terms/robots.txt' input, and it is
fetched before anything is polled, not after.  Purely observational - nothing here
fetches a target page.
"""
import json,subprocess,collections,urllib.parse as up
from concurrent.futures import ThreadPoolExecutor
UA='smart-money-research/1.0 (+B2 source-layer study; contact rogerlgk@gmail.com)'
FMT='%{http_code} %{size_download} %{content_type}'
def hosts():
    H={}
    for fn,tag in (('b1/v2/class1_both_urls.json','kalshi'),('b1/v2/pm_class1_urls2.json','polymarket')):
        d=json.load(open(fn))
        for u,n in d['url_mk'].items():
            p=up.urlparse(u); b=p.scheme+'://'+p.netloc
            e=H.setdefault(b,{'base':b,'venues':set(),'markets':0,'paths':[]})
            e['venues'].add(tag); e['markets']+=n; e['paths'].append(p.path or '/')
    return H
def fetch(b):
    u=b+'/robots.txt'
    r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','-L','--max-redirs','3','--max-time','20','-w',chr(10)+FMT,u],capture_output=True,text=True,timeout=35)
    body,_,tail=r.stdout.rpartition(chr(10))
    p=tail.split(' ')
    code=int(p[0]) if p and p[0].isdigit() else -1
    return b,code,body
def parse_robots(txt,ua='*'):
    groups=collections.defaultdict(lambda:{'dis':[],'allow':[],'delay':None})
    cur=[]
    for raw in (txt or '').splitlines():
        line=raw.split('#')[0].strip()
        if not line or ':' not in line: continue
        k,v=line.split(':',1); k=k.strip().lower(); v=v.strip()
        if k=='user-agent': cur=[v.lower()]
        elif cur:
            for c in cur:
                if k=='disallow': groups[c]['dis'].append(v)
                elif k=='allow': groups[c]['allow'].append(v)
                elif k=='crawl-delay':
                    try: groups[c]['delay']=float(v)
                    except Exception: pass
    return groups.get(ua,{'dis':[],'allow':[],'delay':None})
def blocked(rule,path):
    best=''
    for d in rule['dis']:
        if d and path.startswith(d) and len(d)>len(best): best=d
    ab=''
    for a in rule['allow']:
        if a and path.startswith(a) and len(a)>len(ab): ab=a
    if best and len(ab)>=len(best): return False
    if any(d=='/' for d in rule['dis']) and not ab: return True
    return bool(best)
H=hosts()
print('hosts behind in-scope sources:',len(H),flush=True)
res={}
with ThreadPoolExecutor(max_workers=6) as ex:
    for b,code,body in ex.map(fetch,sorted(H)): res[b]=(code,body)
out=open('b2/robots.jsonl','w')
st=collections.Counter(); dl=collections.Counter(); blk=collections.Counter(); blkm=collections.Counter()
for b,e in H.items():
    code,body=res.get(b,(-1,''))
    st[code]+=1
    rule=parse_robots(body if code==200 else '')
    d=rule['delay']
    dl['delay=%s'%(d if d is not None else 'none')]+=1
    nb=sum(1 for p in e['paths'] if blocked(rule,p))
    blk['blocked' if nb else 'allowed']+=1
    blkm['blocked' if nb else 'allowed']+=e['markets']
    out.write(json.dumps({'base':b,'http':code,'venues':sorted(e['venues']),'markets':e['markets'],
        'n_paths':len(e['paths']),'n_blocked':nb,'crawl_delay':d,'n_disallow':len(rule['dis']),
        'robots_bytes':len(body or '')})+chr(10))
out.close()
print('robots.txt status:',dict(sorted(st.items())))
print('crawl-delay declared for UA *:',dl.most_common(8))
print('hosts with at least one in-scope path disallowed:',dict(blk))
print('markets behind those hosts:',dict(blkm))
