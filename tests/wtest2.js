/* Bot must EXPLAIN an empty book. Feed only sub-threshold trades and check the diagnostics. */
const fs=require('fs');
let src=fs.readFileSync('worker.js','utf8').replace(/export default/,'const H =');
src+='\n;module.exports={cycle};';
fs.writeFileSync('/tmp/w2.cjs',src);
global.fetch = async (u,o)=>{ u=String(u);
  if(u.includes('ntfy.sh')) return {ok:true,json:async()=>({})};
  if(u.includes('filterAmount=10000')) return {ok:true,json:async()=>[
    {proxyWallet:'0xA',side:'BUY',size:200000,price:0.5,timestamp:1,conditionId:'S1',asset:'t1',
     outcome:'Yes',outcomeIndex:0,title:'Lakers vs Celtics Game 4',name:'Bob',transactionHash:'a'},
    {proxyWallet:'0xB',side:'BUY',size:60000,price:0.25,timestamp:2,conditionId:'N1',asset:'t2',
     outcome:'Yes',outcomeIndex:0,title:'US military strike on Iran by September?',name:'Carol',transactionHash:'b'},
  ]};
  if(u.includes('filterAmount=5000')) return {ok:true,json:async()=>[]};
  if(u.includes('/book')) return {ok:true,json:async()=>({asks:[],bids:[]})};
  return {ok:true,json:async()=>({})};
};
let KV={}; const env={NTFY_TOPIC:'t',BOT_STATE:{get:async k=>KV[k]||null,put:async(k,v)=>{KV[k]=v;}}};
const {cycle}=require('/tmp/w2.cjs');
(async()=>{
  let st; for(let i=0;i<3;i++) st=await cycle(env);
  console.log('positions:', st.positions.length, '(expect 0)');
  console.log('cyclesSinceFill:', st.cyclesSinceFill);
  console.log('gates:', JSON.stringify(st.gates));
  console.log('bestNearMiss:', JSON.stringify(st.bestNearMiss));
  const ok = st.positions.length===0 && st.bestNearMiss && /needs 62/.test(st.bestNearMiss.why) && st.cyclesSinceFill===3;
  console.log(ok?'PASS — empty book is now explained':'FAIL');
})();
