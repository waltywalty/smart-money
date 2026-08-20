import json,collections,sys,urllib.parse as up
R=collections.defaultdict(dict)
kind={}
for ln in open('b2/change.jsonl'):
    d=json.loads(ln)
    R[d['url']][d['round']]=d; kind[d['url']]=d['kind']
mk={}
for fn in ('b1/v2/class1_both_urls.json','b1/v2/pm_class1_urls2.json'):
    for u,n in json.load(open(fn))['url_mk'].items(): mk[u]=mk.get(u,0)+n
rounds=sorted({r for v in R.values() for r in v})
LBL={0:'T+0',1:'T+5m',2:'T+15m',3:'T+60m'}
print('rounds present:',[LBL.get(r,r) for r in rounds])
for b in rounds[1:]:
    print()
    print('='*84)
    print('%s vs T+0'%LBL.get(b,b))
    for k in ('target','control'):
        us=[u for u in R if kind[u]==k and 0 in R[u] and b in R[u]]
        ok=[u for u in us if 200<=R[u][0].get('code',-1)<300 and 200<=R[u][b].get('code',-1)<300]
        raw=sum(1 for u in ok if R[u][0]['raw']!=R[u][b]['raw'])
        nrm=sum(1 for u in ok if R[u][0]['norm']!=R[u][b]['norm'])
        both=sum(1 for u in ok if R[u][0]['raw']!=R[u][b]['raw'] and R[u][0]['norm']==R[u][b]['norm'])
        wm=sum(mk.get(u,0) for u in ok); wraw=sum(mk.get(u,0) for u in ok if R[u][0]['raw']!=R[u][b]['raw'])
        wnrm=sum(mk.get(u,0) for u in ok if R[u][0]['norm']!=R[u][b]['norm'])
        print('  %-8s n=%-4d  raw changed %4d (%5.1f%%)   normalised changed %4d (%5.1f%%)   raw-only %d'%(k,len(ok),raw,100.0*raw/max(1,len(ok)),nrm,100.0*nrm/max(1,len(ok)),both))
        if k=='target' and wm: print('           weighted by markets: raw %5.1f%%  normalised %5.1f%%  (of %d markets)'%(100.0*wraw/wm,100.0*wnrm/wm,wm))
    # the decisive comparison
    tus=[u for u in R if kind[u]=='target' and 0 in R[u] and b in R[u] and 200<=R[u][0].get('code',-1)<300 and 200<=R[u][b].get('code',-1)<300]
    cus=[u for u in R if kind[u]=='control' and 0 in R[u] and b in R[u] and 200<=R[u][0].get('code',-1)<300 and 200<=R[u][b].get('code',-1)<300]
    if cus:
        tn=100.0*sum(1 for u in tus if R[u][0]['norm']!=R[u][b]['norm'])/max(1,len(tus))
        cn=100.0*sum(1 for u in cus if R[u][0]['norm']!=R[u][b]['norm'])/max(1,len(cus))
        print('  --> normalised change: targets %.1f%%  vs  impossible-path controls %.1f%%   (lift %+.1f pp)'%(tn,cn,tn-cn))
# hosts whose CONTROL churns - a change there proves nothing
last=rounds[-1]
bad=collections.Counter()
for u in R:
    if kind[u]!='control': continue
    for b in rounds[1:]:
        if 0 in R[u] and b in R[u] and R[u][0].get('norm') and R[u][0]['norm']!=R[u][b].get('norm'): bad[u]+=1
print()
print('impossible-path controls that changed at least once: %d of %d hosts'%(len(bad),sum(1 for u in R if kind[u]=='control')))
hb={up.urlparse(u).scheme+'://'+up.urlparse(u).netloc for u in bad}
mkbad=sum(n for u,n in mk.items() if (up.urlparse(u).scheme+'://'+up.urlparse(u).netloc) in hb)
print('in-scope markets on those hosts: %d'%mkbad)
for u in list(bad)[:12]: print('   ',u[:76])
