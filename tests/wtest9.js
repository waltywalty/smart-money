/* Penny sweep: (a) counts a clean win market, (b) flags a reversal market, (c) skips
   unresolved + no-penny markets without counting them, (d) dedupes across cycles. */
const fs=require('fs');
let src=fs.readFileSync('worker.js','utf8').replace(/export default/,'const H =');
src+='\n;module.exports={cycle,HANDLER:H};'; fs.writeFileSync('/tmp/w9.cjs',src);
global.fetch = async (u)=>{ u=String(u);
  if(u.includes('ntfy.sh')) return {ok:true,json:async()=>({})};
  if(u.includes('gamma-api')&&u.includes('closed=true')) return {ok:true,json:async()=>[
    {conditionId:'WINM', question:'Shelton confirmed as Fed chair?'},
    {conditionId:'REVM', question:'Longshot flips at the wire?'},
    {conditionId:'PEND', question:'Still in dispute?'},
    {conditionId:'EMPT', question:'Nobody bought pennies here'},
  ]};
  if(u.includes('gamma-api')) return {ok:true,json:async()=>[]};
  if(u.includes('clob.polymarket.com/markets/WINM')) return {ok:true,json:async()=>({tokens:[{token_id:'a',winner:false,outcome:'Yes'},{token_id:'b',winner:true,outcome:'No'}]})};
  if(u.includes('clob.polymarket.com/markets/REVM')) return {ok:true,json:async()=>({tokens:[{token_id:'c',winner:true,outcome:'Yes'},{token_id:'d',winner:false,outcome:'No'}]})};
  if(u.includes('clob.polymarket.com/markets/PEND')) return {ok:true,json:async()=>({tokens:[{token_id:'e',winner:false},{token_id:'f',winner:false}]})};
  if(u.includes('clob.polymarket.com/markets/EMPT')) return {ok:true,json:async()=>({tokens:[{token_id:'g',winner:true},{token_id:'h',winner:false}]})};
  if(u.includes('trades?market=WINM')) return {ok:true,json:async()=>[
    ...Array.from({length:39},(_,i)=>({side:'BUY',price:0.99,outcomeIndex:1,transactionHash:'w'+i})),
    {side:'BUY',price:0.30,outcomeIndex:0},{side:'SELL',price:0.99,outcomeIndex:1}]};
  if(u.includes('trades?market=REVM')) return {ok:true,json:async()=>[
    ...Array.from({length:12},(_,i)=>({side:'BUY',price:0.985,outcomeIndex:1,transactionHash:'r'+i})), // bought NO at 98.5c, YES won
    {side:'BUY',price:0.99,outcomeIndex:0}]};                                                          // one buy on winner side too
  if(u.includes('trades?market=EMPT')) return {ok:true,json:async()=>[{side:'BUY',price:0.45,outcomeIndex:0}]};
  if(u.includes('trades?market=')) return {ok:true,json:async()=>[]};
  if(u.includes('filterAmount')) return {ok:true,json:async()=>[]};
  if(u.includes('/book')) return {ok:true,json:async()=>({bids:[{price:'0.44',size:'900'}],asks:[{price:'0.46',size:'900'}]})};
  if(u.includes('/markets/')) return {ok:true,json:async()=>({closed:false,tokens:[]})};
  return {ok:true,json:async()=>({})};
};
let KV={}; const env={NTFY_TOPIC:'t',BOT_STATE:{get:async k=>KV[k]||null,put:async(k,v)=>{KV[k]=v;}}};
const {cycle,HANDLER}=require('/tmp/w9.cjs');
(async()=>{
  let st=await cycle(env);
  console.log('after cycle 1:', JSON.stringify({active:st.pennies.active,wins:st.pennies.wins,rev:st.pennies.reversals,fills:st.pennies.fills}));
  console.log('log:', st.pennies.log[0]||'none');
  console.log('PEND status:', st.pennies.done.PEND, '| EMPT status:', st.pennies.done.EMPT);
  const st2=await cycle(env);   // same gamma page -> all deduped, no double count
  console.log('after cycle 2 (dedupe):', JSON.stringify({active:st2.pennies.active,wins:st2.pennies.wins,rev:st2.pennies.reversals}));
  const view = JSON.parse(await (await HANDLER.fetch(new Request('https://x/'),env)).text());
  console.log('exposed:', JSON.stringify(view.pennies).slice(0,180));
  const ok = st.pennies.active===2 && st.pennies.wins===1 && st.pennies.reversals===1
    && st.pennies.done.PEND==='unresolved' && st.pennies.done.EMPT==='no-pennies'
    && st2.pennies.active===2 && view.pennies.reversals===1;
  console.log(ok?'PASS — sweep counts, flags, skips and dedupes correctly':'FAIL');
})();
