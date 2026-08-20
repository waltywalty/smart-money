"""For the churning half, hashing is the wrong mechanism - those pages carry a live
quote that never stops moving.  The question that decides whether they are usable at
all is narrower: **is the quote in the served HTML, or only in JavaScript?**

Test: fetch the page twice, 30s apart, and extract every number with 3+ significant
digits.  If the numeric set MOVES between the two fetches, a live value is being
server-rendered and can be read without a browser.  If it is identical while the page
hash churns, the churn is markup and the value is not there.

Control, same access level: run the identical extraction on an impossible path on the
same host.  Any number that appears there too is boilerplate, not the quote.
"""
import json,subprocess,re,time,collections,urllib.parse as up
from concurrent.futures import ThreadPoolExecutor
UA='smart-money-research/1.0 (+B2 source-layer study; contact rogerlgk@gmail.com)'
NUM=re.compile(r'(?<![\w.])\d{1,3}(?:,\d{3})*(?:\.\d+)?(?![\w])')
SCRIPT=re.compile(r'<(script|style)\b.*?</\1>',re.I|re.S)
def get(u,t=25):
    try:
        r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','-L','--max-redirs','5','--max-time',str(t),u],capture_output=True,text=True,timeout=40)
        return r.stdout or ''
    except Exception:
        return ''
def nums(b,strip_js=True):
    x=SCRIPT.sub(' ',b) if strip_js else b
    out=set()
    for m in NUM.findall(x):
        s=m.replace(',','')
        try: v=float(s)
        except Exception: continue
        if len(s.replace('.','').lstrip('0'))>=3: out.add(m)
    return out
rows=json.load(open('b2/stability.json'))
iv=rows[0]['intervals']
ch=sorted([r for r in rows if r['norm_changes']==iv],key=lambda r:-r['markets'])[:22]
print('testing %d churning urls (top by market count)'%len(ch),flush=True)
def test(r):
    u=r['url']; p=up.urlparse(u); base=p.scheme+'://'+p.netloc
    a=get(u); ca=get(base+'/__impossible_control_20260820__')
    time.sleep(30)
    b=get(u); cb=get(base+'/__impossible_control_20260820__')
    na,nb=nums(a),nums(b); ka,kb=nums(ca),nums(cb)
    body_moved=sorted((na^nb)-(ka|kb))
    ctl_moved=len(ka^kb)
    inc=sorted((na^nb)&(ka|kb))
    return {'url':u,'markets':r['markets'],'oi':r['oi'],'len_a':len(a),'len_b':len(b),
            'n_a':len(na),'n_b':len(nb),'moved':len(body_moved),'ctl_moved':ctl_moved,
            'boilerplate_moved':len(inc),'sample':body_moved[:6]}
res=[]
with ThreadPoolExecutor(max_workers=5) as ex:
    for r in ex.map(test,ch): res.append(r)
json.dump(res,open('b2/extractability.json','w'))
res.sort(key=lambda r:-r['markets'])
print()
print('%-56s %6s %6s %5s %5s %s'%('url','mk','bytes','nums','moved','ctl'))
for r in res:
    print('%-56s %6d %6d %5d %5d %3d  %s'%(r['url'][:56],r['markets'],r['len_a'],r['n_a'],r['moved'],r['ctl_moved'],','.join(r['sample'][:4])))
yes=[r for r in res if r['moved']>0 and r['ctl_moved']==0]
no=[r for r in res if r['moved']==0]
print()
print('SERVER-RENDERED live value (numbers moved, control did not): %d urls, %d markets, $%s oi'%(len(yes),sum(r['markets'] for r in yes),'{:,.0f}'.format(sum(r['oi'] for r in yes))))
print('NO numeric movement in the served HTML at all:               %d urls, %d markets, $%s oi'%(len(no),sum(r['markets'] for r in no),'{:,.0f}'.format(sum(r['oi'] for r in no))))
