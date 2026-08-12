/* Subrequest budget: a gamma page full of unresolved markets must NOT burn more than
   BUDGET calls, and coverage must still advance via the offset. */
const fs=require('fs');
let src=fs.readFileSync('worker.js','utf8').replace(/export default/,'const H =');
src+='\n;module.exports={cycle,HANDLER:H};'; fs.writeFileSync('/tmp/w11.cjs',src);
let calls={clob:0,trades:0,gamma:0,total:0};
global.fetch = async (u)=>{ u=String(u); calls.total++;
  if(u.includes('ntfy.sh')) return {ok:true,json:async()=>({})};
  if(u.includes('clob.polymarket.com/markets/')) { calls.clob++;
    const id=u.split('/markets/')[1].split('?')[0];
    // every market unresolved -> the pathological case that burned the old budget
    if(id.startsWith('U')) return {ok:true,json:async()=>({tokens:[{winner:false},{winner:false}]})};
    return {ok:true,json:async()=>({tokens:[{token_id:'a',winner:true},{token_id:'b',winner:false}]})};
  }
  if(u.includes('closed=true')) { calls.gamma++;
    return {ok:true,json:async()=>Array.from({length:20},(_,i)=>({conditionId:'U'+i,question:'Unresolved '+i}))};
  }
  if(u.includes('trades?market=')) { calls.trades++; return {ok:true,json:async()=>[]}; }
  if(u.includes('gamma-api')) return {ok:true,json:async()=>[]};
  if(u.includes('/book')) return {ok:true,json:async()=>({bids:[{price:'0.48',size:'900'}],asks:[{price:'0.50',size:'900'}]})};
  if(u.includes('filterAmount')) return {ok:true,json:async()=>[]};
  if(u.includes('/markets/')) return {ok:true,json:async()=>({closed:false,tokens:[]})};
  return {ok:true,json:async()=>({})};
};
let KV={}; const env={NTFY_TOPIC:'t',BOT_STATE:{get:async k=>KV[k]||null,put:async(k,v)=>{KV[k]=v;}}};
const {cycle,HANDLER}=require('/tmp/w11.cjs');
(async()=>{
  const before={...calls};
  let st=await cycle(env);
  const pennyCalls = (calls.clob-before.clob)+(calls.trades-before.trades)+(calls.gamma-before.gamma);
  console.log(`penny-sweep subrequests this cycle: ${pennyCalls} (budget 7)`);
  console.log(`TOTAL subrequests this cycle: ${calls.total} (Cloudflare limit 50)`);
  console.log(`offset after cycle 1: ${st.pennies.offset} (must advance)`);
  const o1=st.pennies.offset;
  const c1=calls.total;
  st=await cycle(env);
  console.log(`offset after cycle 2: ${st.pennies.offset} (coverage marching)`);
  console.log(`cycle 2 subrequests: ${calls.total-c1}`);
  const ok = pennyCalls<=7 && calls.total<50 && st.pennies.offset>o1;
  console.log(ok?'PASS — budget held, cycle fits well under the ceiling, coverage advances'
                :'FAIL');
})();
