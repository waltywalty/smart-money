import json,subprocess,collections,os,sys,time
import urllib.parse as up
from concurrent.futures import ThreadPoolExecutor
UA='smart-money-research/1.0 (+B1 source reachability; contact rogerlgk@gmail.com)'
FMT='%{http_code} %{time_total} %{size_download} %{num_redirects} %{content_type} %{url_effective}'
def probe(u,rng=True):
    cmd=['curl','-sS','-A',UA,'-H','Expect:','-L','--max-redirs','5','--max-time','25','-o','/dev/null','-w',FMT]
    if rng: cmd+=['-r','0-4095']
    cmd+=[u]
    try:
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=40)
        p=(r.stdout or '').strip().split(' ')
    except Exception as e:
        return {'url':u,'code':-1,'err':str(e)[:80]}
    if len(p)<6: return {'url':u,'code':-1,'raw':(r.stdout or '')[:80],'err':(r.stderr or '')[:120]}
    return {'url':u,'code':int(p[0]) if p[0].isdigit() else -1,'t':float(p[1]),'bytes':int(p[2]),
            'redirects':int(p[3]),'ctype':p[4],'final':' '.join(p[5:])[:200]}
d=json.load(open('b1/v2/pm_class1_urls2.json'))
urls=sorted(d['url_mk'],key=lambda u:-d['url_mk'][u])
print('distinct class-1 urls',len(urls),flush=True)
hosts=sorted({up.urlparse(u).scheme+'://'+up.urlparse(u).netloc for u in urls if up.urlparse(u).netloc})
print('distinct hosts',len(hosts),flush=True)
out=open('b1/v2/pm_reach.jsonl','w')
with ThreadPoolExecutor(max_workers=6) as ex:
    for i,r in enumerate(ex.map(probe,urls)):
        r['kind']='target'; r['markets']=d['url_mk'].get(r['url'],0)
        out.write(json.dumps(r)+chr(10))
        if i%100==0: out.flush(); print('target',i,flush=True)
out.flush(); print('targets done',flush=True)
ctl_neg=[h+'/__impossible_control_20260818__' for h in hosts]
ctl_pos=hosts[:]
with ThreadPoolExecutor(max_workers=6) as ex:
    for r in ex.map(probe,ctl_neg):
        r['kind']='control_impossible'; out.write(json.dumps(r)+chr(10))
out.flush(); print('impossible controls done',flush=True)
with ThreadPoolExecutor(max_workers=6) as ex:
    for r in ex.map(probe,ctl_pos):
        r['kind']='control_positive'; out.write(json.dumps(r)+chr(10))
out.close(); print('ALL DONE',flush=True)
