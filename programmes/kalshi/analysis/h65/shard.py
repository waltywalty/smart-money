"""A1 - per-shard admission and extraction, exactly per B1's sealed instrument.

Bracketable: a snapshot row is placeable if delta rows share its timestamp_received;
its bracket is [min(timestamp), max(timestamp)] over that batch. Admission: >=80%
bracketable AND the shard contains delta rows. Never selected by date.
"""
import duckdb,json,os,sys,subprocess,time
FAM=('KXATPCHALLENGERMATCH','KXCS2MAP','KXCS2GAME','KXATPSETWINNER','KXBNB15M')
LIKE=' or '.join("market_ticker like '%s-%%'"%f for f in FAM)
UA='smart-money-research/1.0 (+A1 depth surface)'
CK='shard_ck.json'
st=json.load(open(CK)) if os.path.exists(CK) else {}
shards=json.load(open('shards_in.json'))
BUDGET=float(os.environ.get('BUDGET','40'))
t0=time.time()
for h in shards:
    if h in st: continue
    if time.time()-t0>BUDGET: break
    url='https://r2kalshi.pmxt.dev/kalshi_orderbook_%s.parquet'%h
    p='/root/w/shards/s.parquet'
    r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','--max-time','120','-o',p,'-w','%{http_code}'],capture_output=True,text=True) if False else subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','--max-time','120','-o',p,'-w','%{http_code}',url],capture_output=True,text=True)
    code=r.stdout.strip()
    if code!='200':
        st[h]={'http':code}; json.dump(st,open(CK,'w')); print(h,'http',code,flush=True); continue
    c=duckdb.connect()
    c.execute("create view s as select * from '%s'"%p)
    c.execute("""create table b as
      select timestamp_received tr, min(timestamp) lo, max(timestamp) hi, count(*) nd
      from s where event_type='orderbook_delta' group by 1""")
    tot=c.execute("select count(*) from s where event_type='orderbook_snapshot'").fetchone()[0]
    br=c.execute("select count(*) from s join b on s.timestamp_received=b.tr where s.event_type='orderbook_snapshot'").fetchone()[0]
    frac=(br/tot) if tot else 0.0
    w=c.execute("select quantile_cont(epoch(hi-lo),0.5), quantile_cont(epoch(hi-lo),0.99), max(epoch(hi-lo)) from b").fetchone()
    nd=c.execute("select count(*) from s where event_type='orderbook_delta'").fetchone()[0]
    adm = (nd>0) and (frac>=0.80)
    rec={'snap':tot,'bracketable':br,'frac':round(frac,4),'deltas':nd,
         'bw_p50':round(w[0] or 0,3),'bw_p99':round(w[1] or 0,3),'bw_max':round(w[2] or 0,3),'admitted':adm}
    if adm:
        c.execute("""copy (select s.timestamp_received, s.timestamp, s.market_ticker, s.event_type,
                    s.yes_bids, s.no_bids, s.price, s.delta, s.side, b.lo, b.hi
                    from s left join b on s.timestamp_received=b.tr
                    where (%s)) to 'ext/%s.parquet' (format parquet, compression zstd)"""%(LIKE,h))
        rec['extract_bytes']=os.path.getsize('ext/%s.parquet'%h)
        rec['extract_rows']=c.execute("select count(*) from 'ext/%s.parquet'"%h).fetchone()[0]
    c.close(); os.remove(p)
    st[h]=rec; json.dump(st,open(CK,'w'))
    print('%s frac=%.3f %s p99=%.1fs %s'%(h,frac,'ADMIT ' if adm else 'reject',rec['bw_p99'],('rows=%d'%rec.get('extract_rows',0)) if adm else ''),flush=True)
d=[v for v in st.values() if 'frac' in v]
print('--- %d/%d shards done, %d admitted'%(len(st),len(shards),sum(1 for v in d if v['admitted'])))
