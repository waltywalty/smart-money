"""A page that always returns the same empty body is maximally 'stable' and carries no
information at all.  binance.com returns 202/0 bytes and carbonarc.ai returns an
identical 4,665-byte shell for any path - both land in the stable set and neither can
ever signal anything.  So the usable subset is STABLE **intersected with** the hosts
where the content control separates (P21), not stability alone.
"""
import json,collections,urllib.parse as up
rows=json.load(open('b2/stability.json'))
hc={r['base']:r for r in json.load(open('b2/hash_control.json'))}
def base(u):
    p=up.urlparse(u); return p.scheme+'://'+p.netloc
def verdict(u):
    r=hc.get(base(u))
    if r is None: return 'not tested (status control already separated)'
    if r['status_sep']: return 'status control separates'
    return 'content control separates' if r['hash_differs'] else 'VOID - no control works'
iv=rows[0]['intervals']
st=[r for r in rows if r['norm_changes']==0]
G=collections.Counter(); GM=collections.Counter(); GO=collections.Counter()
for r in st:
    v=verdict(r['url']); G[v]+=1; GM[v]+=r['markets']; GO[v]+=r['oi']
print('The STABLE set, split by whether ANY control separates on that host:')
print('%-46s %6s %9s %16s'%('','urls','markets','open interest'))
for k,c in sorted(G.items(),key=lambda x:-x[1]):
    print('%-46s %6d %9d %16s'%(k,c,GM[k],'{:,.0f}'.format(GO[k])))
bad=[r for r in st if verdict(r['url']).startswith('VOID')]
print()
print('dropped as uncontrollable:')
for r in sorted(bad,key=lambda r:-r['markets'])[:10]: print('   %5d mk  %s'%(r['markets'],r['url'][:78]))
clean=[r for r in st if not verdict(r['url']).startswith('VOID')]
tot=sum(r['markets'] for r in rows); toto=sum(r['oi'] for r in rows)
print()
print('USABLE FOR CHANGE DETECTION: %d urls, %d markets, $%s open interest'%(len(clean),sum(r['markets'] for r in clean),'{:,.0f}'.format(sum(r['oi'] for r in clean))))
print('   = %.1f%% of the %d markets and %.1f%% of the $%s measured over all rounds'%(100.0*sum(r['markets'] for r in clean)/tot,tot,100.0*sum(r['oi'] for r in clean)/toto,'{:,.0f}'.format(toto)))
known_bad='https://www.nass.org/can-I-vote'
kb=[r for r in clean if r['url']==known_bad]
if kb:
    print()
    print('   NOTE: %d of those markets are %s, which P19 records as a false positive'%(kb[0]['markets'],known_bad))
    print('   Excluding it: %d urls, %d markets, $%s open interest'%(len(clean)-1,sum(r['markets'] for r in clean)-kb[0]['markets'],'{:,.0f}'.format(sum(r['oi'] for r in clean)-kb[0]['oi'])))
json.dump([r['url'] for r in clean],open('b2/usable_urls.json','w'))
