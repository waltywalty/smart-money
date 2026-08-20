import json,collections,urllib.parse as up
R=collections.defaultdict(dict); kind={}
for ln in open('b2/change.jsonl'):
    d=json.loads(ln); R[d['url']][d['round']]=d; kind[d['url']]=d['kind']
def host(u):
    p=up.urlparse(u); return p.scheme+'://'+p.netloc
ctl={host(u):u for u in R if kind[u]=='control'}
rounds=sorted({r for v in R.values() for r in v})
LBL={0:'T+0',1:'T+5m',2:'T+15m',3:'T+60m'}
def ok(u,a,b):
    return a in R[u] and b in R[u] and 200<=R[u][a].get('code',-1)<300 and 200<=R[u][b].get('code',-1)<300
for b in rounds[1:]:
    pairs=[]
    for u in R:
        if kind[u]!='target': continue
        c=ctl.get(host(u))
        if not c or not ok(u,0,b) or not ok(c,0,b): continue
        pairs.append((u,c))
    if not pairs: continue
    n=len(pairs)
    tr=sum(1 for u,c in pairs if R[u][0]['raw']!=R[u][b]['raw'])
    cr=sum(1 for u,c in pairs if R[c][0]['raw']!=R[c][b]['raw'])
    tc=sum(1 for u,c in pairs if R[u][0]['norm']!=R[u][b]['norm'])
    cc=sum(1 for u,c in pairs if R[c][0]['norm']!=R[c][b]['norm'])
    same=sum(1 for u,c in pairs if (R[u][0]['norm']!=R[u][b]['norm'])==(R[c][0]['norm']!=R[c][b]['norm']))
    print('%s vs T+0  PAIRED on the same host, n=%d url pairs'%(LBL.get(b,b),n))
    print('   raw hash changed        target %5.1f%%   control %5.1f%%   lift %+.1f pp'%(100.0*tr/n,100.0*cr/n,100.0*(tr-cr)/n))
    print('   normalised hash changed target %5.1f%%   control %5.1f%%   lift %+.1f pp'%(100.0*tc/n,100.0*cc/n,100.0*(tc-cc)/n))
    print('   target and control agreed on %d of %d pairs (%.0f%%)'%(same,n,100.0*same/n))
    print()
