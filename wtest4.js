/* Bot correctness: (a) never enter at 98c, (b) an expired limit is 'cancelled' not a loss
   and must not appear in win-rate, (c) equity never goes NaN. */
const fs=require('fs');
let src=fs.readFileSync('worker.js','utf8').replace(/export default/,'const H =');
src+='\n;module.exports={cycle,HANDLER:H};'; fs.writeFileSync('/tmp/w4.cjs',src);
let clock = 1;
global.fetch = async (u,o)=>{ u=String(u);
  if(u.includes('ntfy.sh')) return {ok:true,json:async()=>({})};
  if(u.includes('gamma-api')) return {ok:true,json:async()=>[{volume24hr:20000,oneDayPriceChange:0.3}]};
  if(u.includes('filterAmount=10000')) return {ok:true,json:async()=>[
    // near-certain: huge, newsy, would score well — must be REJECTED on price alone
    {proxyWallet:'0xN',side:'BUY',size:50000,price:0.983,timestamp:1,conditionId:'FED',asset:'tFED',slug:'fed',
     outcome:'No',outcomeIndex:1,title:'Will the Fed decrease interest rates by 25 bps?',name:'',transactionHash:'n1'},
    // legitimate mid-price entry -> should rest as a maker limit
    {proxyWallet:'0xG',side:'BUY',size:200000,price:0.30,timestamp:2,conditionId:'IRAN',asset:'tIRAN',slug:'iran',
     outcome:'Yes',outcomeIndex:0,title:'US military strike on Iran by September?',name:'',transactionHash:'g1'},
  ]};
  if(u.includes('filterAmount=5000')) return {ok:true,json:async()=>[]};
  // book never comes to us -> the limit expires unfilled
  if(u.includes('/book')) return {ok:true,json:async()=>({asks:[['0.90','100']],bids:[['0.10','100']]})};
  if(u.includes('/markets/')) return {ok:true,json:async()=>({closed:false,tokens:[]})};
  return {ok:true,json:async()=>({})};
};
let KV={}; const env={NTFY_TOPIC:'t',BOT_STATE:{get:async k=>KV[k]||null,put:async(k,v)=>{KV[k]=v;}}};
const {cycle}=require('/tmp/w4.cjs');
(async()=>{
  let st = await cycle(env);
  console.log('after cycle 1 — positions:', st.positions.map(p=>`${p.title.slice(0,28)} @${p.limitPx||p.entryPx} ${p.status}`));
  console.log('priceBand rejections:', st.gates.priceBand, '(expect 1 — the 98.3c trade)');
  // age the resting limit past its TTL
  st = JSON.parse(KV.state); st.positions.forEach(p=>{ if(p.status==='pending') p.openedAt = Date.now() - 7*3600e3; });
  KV.state = JSON.stringify(st);
  st = await cycle(env);
  const cancelled = st.positions.filter(p=>p.status==='cancelled');
  console.log('cancelled:', cancelled.length, cancelled.map(p=>p.exitReason));
  const view = JSON.parse(await (await require('/tmp/w4.cjs').HANDLER.fetch(new Request('https://x/'), env)).text());
  console.log('reported closed:', view.closed, '(expect 0 — a cancelled order is not a trade)');
  console.log('reported wins:', view.wins, '| cancelled field:', view.cancelled);
  console.log('equity:', view.equity, Number.isFinite(view.equity)?'(finite)':'(NaN — BAD)');
  const ok = st.gates.priceBand>=1 && cancelled.length===1 && view.closed===0 && Number.isFinite(view.equity);
  console.log(ok?'PASS':'FAIL');
})();
