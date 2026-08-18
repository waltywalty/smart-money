"""A1 - replay the book to T-10m and price the sealed size grid. SQL-side aggregation."""
import duckdb,json,os,sys,time,collections,datetime as dt,re
GRID=[1,2,5,10,25,50,100,250,500]
CK='surf_ck.json'
done=json.load(open(CK)) if os.path.exists(CK) else {}
surv=json.load(open('surv.json'))
bysh=collections.defaultdict(list)
for r in surv: bysh[r['shard']].append(r)
def ep(s):
    s=s.replace('Z','+00:00'); s=re.sub(r'\.(\d+)',lambda m:'.'+(m.group(1)+'000000')[:6],s)
    return dt.datetime.fromisoformat(s)
BUDGET=float(os.environ.get('BUDGET','40')); t0=time.time()
fh=open('surf_rows.jsonl','a')
for sh in sorted(bysh):
    if sh in done: continue
    if time.time()-t0>BUDGET: break
    p='ext/%s.parquet'%sh
    if not os.path.exists(p): done[sh]={'err':'no extract'}; continue
    c=duckdb.connect(); c.execute("create view e as select * from '%s'"%p)
    inlist=','.join("'%s'"%r['ticker'] for r in bysh[sh])
    snaps=c.execute("select market_ticker, hi, lo, yes_bids, no_bids from e where event_type='orderbook_snapshot' and hi is not null and market_ticker in (%s)"%inlist).fetchall()
    S=collections.defaultdict(list)
    for mt,hi,lo,yb,nb in snaps: S[mt].append((hi,lo,yb,nb))
    chosen={}; skipped=[]
    for r in bysh[sh]:
        T=ep(r['entry']); cand=[x for x in S.get(r['ticker'],[]) if x[0]<=T]
        if not cand: skipped.append(r); continue
        chosen[r['ticker']]=(max(cand,key=lambda x:x[0]),T,r)
    for r in skipped:
        fh.write(json.dumps({**r,'skip':'no_snapshot_before_T','n_snap':len(S.get(r['ticker'],[]))})+'\n')
    if chosen:
        c.execute('create table bnd(market_ticker VARCHAR, hi TIMESTAMPTZ, tt TIMESTAMPTZ)')
        c.executemany('insert into bnd values (?,?,?)',[(k,v[0][0],v[1]) for k,v in chosen.items()])
        agg=c.execute("""select e.market_ticker, e.side, e.price, sum(e.delta)
            from e join bnd b on e.market_ticker=b.market_ticker
            where e.event_type='orderbook_delta' and e.timestamp>b.hi and e.timestamp<=b.tt
            group by 1,2,3""").fetchall()
        DA=collections.defaultdict(list)
        for mt,sd,pr,s in agg: DA[mt].append((sd,float(pr),float(s)))
        for mt,((hi,lo,yb,nb),T,r) in chosen.items():
            yes={float(d['1']):float(d['2']) for d in (yb or [])}
            no={float(d['1']):float(d['2']) for d in (nb or [])}
            for sd,pr,s in DA.get(mt,[]):
                bk = yes if sd=='yes' else no
                bk[pr]=bk.get(pr,0.0)+s
            ladder=sorted([(round(1.0-q,4),sz) for q,sz in no.items() if sz>0.5])
            ybest=max([q for q,sz in yes.items() if sz>0.5],default=None)
            rec={**r,'bracket_s':round((hi-lo).total_seconds(),3),
                 'best_ask':ladder[0][0] if ladder else None,
                 'depth_at_best':ladder[0][1] if ladder else 0.0,
                 'total_depth':round(sum(sz for _,sz in ladder),2),'levels':len(ladder),
                 'best_yes_bid':ybest,
                 'spread':(round(ladder[0][0]-ybest,4) if (ladder and ybest is not None) else None),
                 'fills':{}}
            for N in GRID:
                need=N; cost=0.0
                for px,sz in ladder:
                    take=min(need,sz); cost+=take*px; need-=take
                    if need<=0: break
                rec['fills'][str(N)] = None if need>0 else round(cost/N,6)
            fh.write(json.dumps(rec)+'\n')
    c.close()
    done[sh]={'markets':len(bysh[sh]),'priced':len(chosen),'no_snap':len(skipped)}
    json.dump(done,open(CK,'w'))
    print('%s m=%d priced=%d nosnap=%d'%(sh,len(bysh[sh]),len(chosen),len(skipped)),flush=True)
fh.close(); print('--- %d/%d shards'%(len(done),len(bysh)))
