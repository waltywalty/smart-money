import json,collections,urllib.parse as up
R=collections.defaultdict(dict); kind={}
for ln in open('b2/change.jsonl'):
    d=json.loads(ln); R[d['url']][d['round']]=d; kind[d['url']]=d['kind']
mk={}; oi={}
for fn in ('b1/v2/class1_both_urls.json','b1/v2/pm_class1_urls2.json'):
    j=json.load(open(fn))
    for u,n in j['url_mk'].items():
        mk[u]=mk.get(u,0)+n; oi[u]=oi.get(u,0.0)+j.get('url_oi',{}).get(u,0.0)
rounds=sorted({r for v in R.values() for r in v})
rows=[]
for u,v in R.items():
    if kind[u]!='target': continue
    seq=[v[r] for r in rounds if r in v]
    if len(seq)<len(rounds): continue
    if not all(200<=s.get('code',-1)<300 for s in seq): continue
    nch=sum(1 for a,b in zip(seq,seq[1:]) if a['norm']!=b['norm'])
    rch=sum(1 for a,b in zip(seq,seq[1:]) if a['raw']!=b['raw'])
    rows.append({'url':u,'norm_changes':nch,'raw_changes':rch,'intervals':len(seq)-1,
                 'markets':mk.get(u,0),'oi':oi.get(u,0.0)})
n=len(rows); iv=rows[0]['intervals'] if rows else 0
TM=sum(r['markets'] for r in rows); TO=sum(r['oi'] for r in rows)
print('URLs 2xx in all %d rounds: %d   markets %d   open interest $%s'%(len(rounds),n,TM,'{:,.0f}'.format(TO)))
print()
B=collections.Counter(); BM=collections.Counter(); BO=collections.Counter()
for r in rows:
    k='STABLE (0 changes)' if r['norm_changes']==0 else ('every interval' if r['norm_changes']==iv else 'intermittent (%d/%d)'%(r['norm_changes'],iv))
    B[k]+=1; BM[k]+=r['markets']; BO[k]+=r['oi']
print('%-26s %6s %9s %16s'%('normalised-hash churn','urls','markets','open interest'))
for k,c in sorted(B.items(),key=lambda x:-x[1]):
    print('%-26s %6d %9d %16s'%(k,c,BM[k],'{:,.0f}'.format(BO[k])))
st=[r for r in rows if r['norm_changes']==0]
print()
print('THE USABLE SUBSET - normalised content identical across every round:')
print('   %d of %d urls (%.1f%%)   %d markets (%.1f%%)   $%s open interest (%.1f%%)'%(
    len(st),n,100.0*len(st)/n,sum(r['markets'] for r in st),100.0*sum(r['markets'] for r in st)/max(1,TM),
    '{:,.0f}'.format(sum(r['oi'] for r in st)),100.0*sum(r['oi'] for r in st)/max(1.0,TO)))
print()
rawst=[r for r in rows if r['raw_changes']==0]
print('   for comparison, RAW-identical across every round: %d urls, %d markets'%(len(rawst),sum(r['markets'] for r in rawst)))
print('   normalisation (stripping script/style/comments) rescues %d urls and %d markets'%(len(st)-len(rawst),sum(r['markets'] for r in st)-sum(r['markets'] for r in rawst)))
print()
st.sort(key=lambda r:-r['markets'])
print('biggest stable urls by market count:')
for r in st[:14]: print('   %5d mk  $%-12s %s'%(r['markets'],'{:,.0f}'.format(r['oi']),r['url'][:78]))
ch=[r for r in rows if r['norm_changes']==iv]
ch.sort(key=lambda r:-r['markets'])
print()
print('biggest urls that changed at EVERY interval (change detection is meaningless there):')
for r in ch[:12]: print('   %5d mk  $%-12s %s'%(r['markets'],'{:,.0f}'.format(r['oi']),r['url'][:78]))
json.dump(rows,open('b2/stability.json','w'))
