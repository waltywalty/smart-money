import json, os, glob, hashlib, sys, collections
ST=json.load(open('/root/work/data/state.json'))
SER=json.load(open('/root/work/series.json'))
OUT='/root/work/data/historical'
rows=[]; tot=0; totu=0; dup=0
for f in sorted(glob.glob(OUT+'/*.ndjson')):
    s=os.path.basename(f)[:-7]
    sz=os.path.getsize(f)
    if sz==0: continue
    h=hashlib.sha256(); n=0; tk=set(); ev=set(); dates=[]
    with open(f,'rb') as fh:
        for line in fh:
            h.update(line)
            if not line.strip(): continue
            n+=1
            try: d=json.loads(line)
            except Exception: continue
            tk.add(d.get('ticker')); ev.add(d.get('event_ticker'))
            c=d.get('close_time') or ''
            if c: dates.append(c[:10])
    dates.sort()
    st=ST.get(s,{})
    meta=SER.get(s,{})
    rows.append({'series':s,'rows':n,'unique_tickers':len(tk),'unique_events':len(ev),
      'bytes':sz,'sha256':h.hexdigest(),'first_close':dates[0] if dates else None,
      'last_close':dates[-1] if dates else None,'distinct_close_dates':len(set(dates)),
      'stop':st.get('stop'),'pages':st.get('pages'),'category':meta.get('category'),
      'fee_type':meta.get('fee_type'),'fee_multiplier':meta.get('fee_multiplier')})
    tot+=n; totu+=len(tk)
    if n!=len(tk): dup+=1
term=sum(1 for v in ST.values() if v.get('stop') in ('cursor_exhausted','empty_page'))
summary={'generated_utc':None,'collector':'scripts/b1_collect.py','endpoint':'/historical/markets',
  'pacing':'3 threads, 0.55s per-thread gap','excluded':'ticker prefix KXMVE*',
  'series_in_frame':len(SER),'series_terminal':term,'series_with_rows':len(rows),
  'total_rows':tot,'total_unique_tickers':totu,'gate_rows_equal_unique':tot==totu,
  'series_with_duplicate_tickers':dup,
  'projection_fields':['ticker','event_ticker','series_ticker','close_time','open_time','settlement_ts','settlement_value_dollars','result','expiration_value','market_type','strike_type','floor_strike','cap_strike','yes_bid_dollars','yes_ask_dollars','no_bid_dollars','no_ask_dollars','last_price_dollars','volume_fp','volume_24h_fp','open_interest_fp','status','title','subtitle'],
  'note_open_interest':'open_interest_fp is 0.00 on the historical path for every market tested (P8). Do not use it.',
  'note_fee':'fee_type/fee_multiplier are series-level, carried here from /series/{ticker}; they are absent from market rows on both paths.'}
json.dump({'summary':summary,'files':rows}, open('/root/work/out/manifest.json','w'), indent=1)
print('files=%d rows=%d unique=%d gate=%s dupseries=%d terminal=%d/%d'%(len(rows),tot,totu,tot==totu,dup,term,len(SER)))
big=sorted(rows,key=lambda r:-r['rows'])[:12]
for b in big: print('  %-26s rows=%-7d ev=%-6d %s .. %s  pages=%s'%(b['series'],b['rows'],b['unique_events'],b['first_close'],b['last_close'],b['pages']))
