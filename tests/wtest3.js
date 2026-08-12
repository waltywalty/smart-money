/* Live-context layer: a trade below the shape bar must be lifted over it by real context,
   and both scores must be recorded so the forward test can separate them. */
const fs=require('fs');
let src=fs.readFileSync('worker.js','utf8').replace(/export default/,'const H =');
src+='\n;module.exports={cycle};'; fs.writeFileSync('/tmp/w3.cjs',src);
global.fetch = async (u,o)=>{ u=String(u);
  if(u.includes('ntfy.sh')) return {ok:true,json:async()=>({})};
  if(u.includes('gamma-api')) return {ok:true,json:async()=>[{volume24hr:50000, oneDayPriceChange:0.22}]};
  if(u.includes('filterAmount=10000')) return {ok:true,json:async()=>[
    // shape score ~48 (news, named wallet, 30c) -> below 62. Context: $30k of a $50k 24h volume
    // = 60% share (+20) and a 22pt repricing (+8) -> 76, must now qualify.
    {proxyWallet:'0xB',side:'BUY',size:100000,price:0.30,timestamp:2,conditionId:'N1',asset:'t2',slug:'iran-strike',
     outcome:'Yes',outcomeIndex:0,title:'US military strike on Iran by September?',name:'Carol',transactionHash:'b'},
  ]};
  if(u.includes('filterAmount=5000')) return {ok:true,json:async()=>[]};
  if(u.includes('/book')) return {ok:true,json:async()=>({asks:[[ '0.31','5000' ]],bids:[['0.29','5000']]})};
  return {ok:true,json:async()=>({})};
};
let KV={}; const env={NTFY_TOPIC:'t',BOT_STATE:{get:async k=>KV[k]||null,put:async(k,v)=>{KV[k]=v;}}};
const {cycle}=require('/tmp/w3.cjs');
(async()=>{
  const st=await cycle(env);
  const p=st.positions[0];
  console.log('near-miss/best:', JSON.stringify(st.bestNearMiss));
  console.log('positions:', st.positions.length);
  if(p) console.log('  score=%s shape=%s ctxBonus=%s reasons=%s', p.score, p.shapeScore, p.ctxBonus, JSON.stringify(p.reasons));
  const ok = p && p.score>p.shapeScore && p.ctxBonus>=20 && p.shapeScore<62;
  console.log(ok?'PASS — context lifted a sub-threshold trade and both scores were recorded':'FAIL');
})();
