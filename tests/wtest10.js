/* Risk layer: (a) a position at the cap edge must NOT breach it, (b) aggregate cap halts new
   exposure, (c) skew stats + tail are reported, (d) normal two-sided fills still work. */
const fs=require('fs');
let src=fs.readFileSync('worker.js','utf8').replace(/export default/,'const H =');
src+='\n;module.exports={cycle,HANDLER:H};'; fs.writeFileSync('/tmp/w10.cjs',src);
let n=0;
global.fetch = async (u)=>{ u=String(u); n++;
  if(u.includes('ntfy.sh')) return {ok:true,json:async()=>({})};
  if(u.includes('gamma-api')&&u.includes('volume24hr')) return {ok:true,json:async()=>[
    {conditionId:'M1', question:'Will the Fed cut rates in September?', bestBid:'0.48', bestAsk:'0.50',
     clobTokenIds:'["t1"]', endDate:'2026-09-20T00:00:00Z'},
    {conditionId:'M2', question:'Will the US invade Iran before 2027?', bestBid:'0.30', bestAsk:'0.32',
     clobTokenIds:'["t2"]', endDate:'2026-12-31T00:00:00Z'}]};
  if(u.includes('gamma-api')) return {ok:true,json:async()=>[]};
  if(u.includes('closed=true')) return {ok:true,json:async()=>[]};
  if(u.includes('/book')) return {ok:true,json:async()=>({bids:[{price:'0.48',size:'9000'}],asks:[{price:'0.50',size:'9000'}]})};
  if(u.includes('trades?market=')) return {ok:true,json:async()=>[
    {side:'BUY', price:0.50,timestamp:Date.now()/1000+50+n,transactionHash:'b'+n},   // lifts our ask -> we sell
    {side:'SELL',price:0.48,timestamp:Date.now()/1000+50+n,transactionHash:'s'+n}]}; // hits our bid  -> we buy
  if(u.includes('filterAmount')) return {ok:true,json:async()=>[]};
  if(u.includes('/markets/')) return {ok:true,json:async()=>({closed:false,tokens:[]})};
  return {ok:true,json:async()=>({})};
};
// seed a book already at the very edge of the cap on M2 (-$149) to test post-trade enforcement
let KV={ state: JSON.stringify({ bank:1000, cash:982, runs:400, equityLog:[], startedAt:1, positions:[],
  house:{ cash:0, rebates:0, fills:0, lastTs:{}, log:[], startedAt:1,
    pos:{ M2:{shares:-480, q:'Will the US invade Iran before 2027?', tok:'t2', mid:0.31} },
    mkts:[{cid:'M1',tok:'t1',q:'Will the Fed cut rates in September?'},
          {cid:'M2',tok:'t2',q:'Will the US invade Iran before 2027?'}] } })};
const env={NTFY_TOPIC:'t',BOT_STATE:{get:async k=>KV[k]||null,put:async(k,v)=>{KV[k]=v;}}};
const {cycle,HANDLER}=require('/tmp/w10.cjs');
(async()=>{
  let st;
  for(let i=0;i<6;i++) st=await cycle(env);
  const v = JSON.parse(await (await HANDLER.fetch(new Request('https://x/'),env)).text());
  const inv = v.house.inventory;
  console.log('inventory:'); inv.forEach(i=>console.log(`   ${String(i.q).slice(0,34).padEnd(34)} ${String(i.shares).padStart(6)} sh  $${i.usd}`));
  console.log('\nriskFilter:', JSON.stringify(v.houseRisk));
  const maxAbs = Math.max(...inv.map(i=>Math.abs(i.usd)));
  const gross = v.houseRisk.gross;
  console.log(`\nlargest single position $${maxAbs} (cap 150)`);
  console.log(`gross $${gross} (cap 400)`);
  console.log(`breaches reported: ${v.houseRisk.breaches}`);
  console.log(`buy/sell fills: ${v.houseRisk.buyFills}/${v.houseRisk.sellFills} — two-sided still working`);
  const ok = maxAbs <= 152 && gross <= 402 && v.houseRisk.breaches===0
           && v.houseRisk.buyFills>0 && v.houseRisk.sellFills>0;
  console.log(ok ? 'PASS — caps hold post-trade, aggregate respected, both sides still fill'
                 : 'FAIL');
})();
