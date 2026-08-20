"""P21: on a third of hosts an impossible path returns 2xx, so the status-code control
cannot separate.  Proposed replacement: a CONTENT control - hash the body for the
impossible path and for the target and require them to differ.  An app shell served
twice fails; a real page passes.

Tested on the hosts where the status control is already known to fail, plus - as the
positive side of the pair - a seeded sample of hosts where it is known to succeed,
because a control that only fires on the broken cases is not a control.
"""
import json,subprocess,hashlib,collections,random,urllib.parse as up
from concurrent.futures import ThreadPoolExecutor
UA='smart-money-research/1.0 (+B2 source-layer study; contact rogerlgk@gmail.com)'
def body(u,t=25):
    r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','-L','--max-redirs','5','--max-time',str(t),'-w',chr(10)+'%{http_code}',u],capture_output=True,text=True,timeout=40)
    b,_,c=r.stdout.rpartition(chr(10))
    return (int(c) if c.isdigit() else -1), b
imp={}; tgt={}
for fn in ('b1/v2/reach.jsonl','b1/v2/pm_reach.jsonl'):
    for ln in open(fn):
        r=json.loads(ln)
        p=up.urlparse(r['url']); b=p.scheme+'://'+p.netloc
        if r['kind']=='control_impossible': imp[b]=r.get('code',-1)
        elif r['kind']=='target': tgt.setdefault(b,r['url'])
nonsep=[b for b,c in imp.items() if c not in (404,410) and 200<=c<300]
sep=[b for b,c in imp.items() if c in (404,410)]
print('hosts where the status control FAILS to separate: %d'%len(nonsep))
print('hosts where it succeeds (positive side): %d, sampling 40'%len(sep))
random.seed(20260818)
sample=nonsep+random.sample(sep,min(40,len(sep)))
def test(b):
    t=tgt.get(b)
    if not t: return None
    c1,b1=body(b+'/__impossible_control_20260818__')
    c2,b2=body(t)
    h1=hashlib.sha256((b1 or '').encode('utf-8','replace')).hexdigest()
    h2=hashlib.sha256((b2 or '').encode('utf-8','replace')).hexdigest()
    return {'base':b,'status_sep':imp.get(b) in (404,410),'imp_code':c1,'tgt_code':c2,
            'imp_len':len(b1 or ''),'tgt_len':len(b2 or ''),'hash_differs':h1!=h2}
res=[]
with ThreadPoolExecutor(max_workers=5) as ex:
    for r in ex.map(test,sample):
        if r: res.append(r)
json.dump(res,open('b2/hash_control.json','w'))
C=collections.Counter()
for r in res: C[(r['status_sep'],r['hash_differs'])]+=1
print()
print('%-22s %-16s %s'%('status control','content control','hosts'))
for k in sorted(C): print('%-22s %-16s %d'%('separates' if k[0] else 'DOES NOT separate','differs' if k[1] else 'IDENTICAL',C[k]))
ns=[r for r in res if not r['status_sep']]
rec=sum(1 for r in ns if r['hash_differs'])
print()
print('On the %d hosts where the status control is void, the content control separates on %d (%.0f%%).'%(len(ns),rec,100.0*rec/max(1,len(ns))))
bad=[r for r in ns if not r['hash_differs']]
print('Still void on %d:'%len(bad))
for r in sorted(bad,key=lambda r:-r['tgt_len'])[:14]: print('   %-44s imp %d/%dB  tgt %d/%dB'%(r['base'][:44],r['imp_code'],r['imp_len'],r['tgt_code'],r['tgt_len']))
ps=[r for r in res if r['status_sep']]
fp=sum(1 for r in ps if not r['hash_differs'])
print()
print('Positive side: of %d hosts where the status control works, the content control agreed on %d and disagreed on %d.'%(len(ps),len(ps)-fp,fp))
