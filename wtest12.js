/* Deadlock fix: a book already OVER the aggregate cap must still be able to trade DOWN,
   while risk-increasing trades stay blocked. */
const fs=require('fs');
let src=fs.readFileSync('worker.js','utf8').replace(/export default/,'const H =');
src+='\n;module.exports={cycle,HANDLER:H};'; fs.writeFileSync('/tmp/w12.cjs',src);
let n=0;
global.fetch = async (u)=>{ u=String(u); n++;
  if(u.includes('ntfy.sh')) return {ok:true,json:async()=>({})};
  if(u.includes('gamma-api')&&u.includes('volume24hr')) return {ok:true,json:async()=>[
    {conditionId:'A', question:'Will the Fed cut rates in September?', bestBid:'0.48', bestAsk:'0.50', clobTokenIds:'["ta"]', endDate:'2026-09-20T00:00:00Z'}]};
  if(u.includes('closed=true')) return {ok:true,json:async()=>[]};
  if(u.includes('gamma-api')) return {ok:true,json:async()=>[]};
  if(u.includes('/book')) return {ok:true,json:async()=>({bids:[{price:'0.48',size:'9000'}],asks:[{price:'0.50',size:'9000'}]})};
  if(u.includes('trades?market=')) return {ok:true,json:async()=>[
    {side:'SELL',price:0.48,timestamp:Date.now()/1000+90+n,transactionHash:'s'+n},   // hits our bid -> we BUY (reduces short)
    {side:'BUY', price:0.50,timestamp:Date.now()/1000+90+n,transactionHash:'b'+n}]}; // lifts our ask -> we SELL (increases short)
  if(u.includes('filterAmount')) return {ok:true,json:async()=>[]};
  if(u.includes('/markets/')) return {ok:true,json:async()=>({closed:false,tokens:[]})};
  return {ok:true,json:async()=>({})};
};
// legacy book: massively over the $400 aggregate cap, all short — exactly Walton's situation
let KV={ state: JSON.stringify({ bank:1000, cash:982, runs:500, equityLog:[], startedAt:1, positions:[],
  house:{ cash:0, rebates:0, fills:0, buyFills:0, sellFills:0, lastTs:{}, log:[], startedAt:1,
    pos:{ A:{shares:-300, q:'Will the Fed cut rates in September?', tok:'ta', mid:0.49},
          B:{shares:-500, q:'Legacy short B', tok:'tb', mid:0.40},
          C:{shares:-400, q:'Legacy short C', tok:'tc', mid:0.45} },
    mkts:[{cid:'A',tok:'ta',q:'Will the Fed cut rates in September?'}] } })};
const env={NTFY_TOPIC:'t',BOT_STATE:{get:async k=>KV[k]||null,put:async(k,v)=>{KV[k]=v;}}};
const {cycle,HANDLER}=require('/tmp/w12.cjs');
(async()=>{
  const g0=(-300*0.49)+(-500*0.40)+(-400*0.45); console.log(`starting gross: $${Math.abs(g0).toFixed(0)} (cap 400) — deadlock condition`);
  let st;
  for(let i=0;i<5;i++) st=await cycle(env);
  const v=JSON.parse(await (await HANDLER.fetch(new Request('https://x/'),env)).text());
  console.log(`buyFills ${v.houseRisk.buyFills}  sellFills ${v.houseRisk.sellFills}`);
  console.log(`market A shares: -300 -> ${Math.round(st.house.pos.A.shares)}  (should rise toward flat)`);
  console.log(`gross now: $${v.houseRisk.gross}`);
  const unwound = st.house.pos.A.shares > -300;
  const backInsideCap = v.houseRisk.gross <= 400;
  const bothSidesLive = v.houseRisk.buyFills > 0 && v.houseRisk.sellFills > 0;
  console.log(unwound && backInsideCap && bothSidesLive
    ? 'PASS — over-cap book unwinds, returns inside the ceiling, and normal quoting resumes'
    : 'FAIL');
})();
