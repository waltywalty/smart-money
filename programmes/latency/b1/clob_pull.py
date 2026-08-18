"""Polymarket enumeration via the CLOB API.
Gamma cannot enumerate: /markets caps at offset ~2000 (422) and /markets/keyset
IGNORES every cursor parameter name and returns page 1 forever - 410,196 rows pulled
from it decoded to 100 distinct conditionIds.  So the stop reason is not enough;
this puller asserts the stream ADVANCES by counting distinct condition_ids and
stopping if a page adds nothing new.
"""
import json,subprocess,time,os,collections
UA='smart-money-research/1.0 (+B1 universe; contact rogerlgk@gmail.com)'
C='https://clob.polymarket.com/markets'
CK='b1/v2/clob_ck.json'
st=json.load(open(CK)) if os.path.exists(CK) else {'cur':'','pages':0,'stop':None,'hist':{}}
H=collections.Counter(st['hist'])
def get(u,t=40,tries=5):
    for i in range(tries):
        r=subprocess.run(['curl','-sS','-A',UA,'-H','Expect:','--max-time',str(t),'--retry','2','-w',chr(10)+'%{http_code}',u],capture_output=True,text=True)
        b,_,c=r.stdout.rpartition(chr(10))
        try: c=int(c)
        except Exception: c=-1
        H['http_%d'%c]+=1
        if c==200: return c,b
        if c in (0,429,500,502,503,504,-1): H['retry']+=1; time.sleep(0.8*(i+1)); continue
        return c,b
    return c,b
seen=set()
if os.path.exists('b1/v2/clob.jsonl'):
    for ln in open('b1/v2/clob.jsonl'):
        try: seen.add(json.loads(ln)['condition_id'])
        except Exception: pass
out=open('b1/v2/clob.jsonl','a')
F=('condition_id','question_id','market_slug','question','description','end_date_iso','game_start_time',
   'active','closed','archived','accepting_orders','enable_order_book','neg_risk','tags','minimum_tick_size',
   'minimum_order_size','tokens','rewards','seconds_delay','is_50_50_outcome')
stall=0
while st['stop'] is None:
    c,b=get(C+('?next_cursor='+st['cur'] if st['cur'] else ''))
    if c!=200: st['stop']='http_%d'%c; break
    try:
        j=json.loads(b)
    except Exception:
        H['truncated_body']+=1
        if H['truncated_body']>40: st['stop']='too_many_truncated_bodies'; break
        time.sleep(1.0); continue
    data=j.get('data') or []; st['pages']+=1
    new=0
    for m in data:
        cid=m.get('condition_id')
        if cid in seen: continue
        seen.add(cid); new+=1
        out.write(json.dumps({k:m.get(k) for k in F})+chr(10))
    nc=j.get('next_cursor') or ''
    if new==0:
        stall+=1
        if stall>=60: st['stop']='stream_stopped_advancing_60_pages'; break
    else: stall=0
    if not nc or nc=='LTE=': st['stop']='cursor_end'; break
    if nc==st['cur']: st['stop']='cursor_repeated'; break
    st['cur']=nc
    if st['pages']%50==0:
        out.flush(); st['hist']=dict(H); json.dump(st,open(CK,'w'))
        print('pages %d distinct %d'%(st['pages'],len(seen)),flush=True)
out.close(); st['hist']=dict(H); json.dump(st,open(CK,'w'))
print('CLOB pages %d stop=%s DISTINCT %d hist %s'%(st['pages'],st['stop'],len(seen),json.dumps(dict(H))),flush=True)
