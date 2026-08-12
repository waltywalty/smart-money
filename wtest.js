/* Worker radar unit test — no network. Stubs fetch + KV, feeds a synthetic batch. */
const fs=require('fs');
let src=fs.readFileSync('worker.js','utf8').replace(/export default/,'const HANDLER =');
src+='\n;module.exports={HANDLER,scoreTrade,classifyTitle,cycle};';
fs.writeFileSync('/tmp/w.cjs',src);

const pushes=[];
global.fetch = async (u,o)=>{
  u=String(u);
  if(u.includes('ntfy.sh')){ pushes.push(o.body); return {ok:true,json:async()=>({})}; }
  if(u.includes('filterAmount=5000')){
    const out=[];
    // 3 wallets converging on the SAME side of one market -> cluster
    for(let i=0;i<3;i++) out.push({proxyWallet:'0xC'+i,side:'BUY',size:60000,price:0.09,timestamp:100+i,
      conditionId:'CLUS',outcome:'Yes',outcomeIndex:0,asset:'tC',title:'US military strike on Iran by September?',
      name:'',transactionHash:'c'+i});
    // one lone high-score whale
    out.push({proxyWallet:'0xW',side:'BUY',size:400000,price:0.06,timestamp:200,conditionId:'SOLO',
      outcome:'Yes',outcomeIndex:0,asset:'tW',title:'Fed cuts rates in September?',name:'',transactionHash:'w1'});
    // noise that must NOT push: small sports bet
    out.push({proxyWallet:'0xS',side:'BUY',size:6000,price:0.5,timestamp:300,conditionId:'SPT',
      outcome:'Yes',outcomeIndex:0,asset:'tS',title:'Lakers vs Celtics Game 4',name:'Bob',transactionHash:'s1'});
    return {ok:true,json:async()=>out};
  }
  if(u.includes('filterAmount=25000')) return {ok:true,json:async()=>[]};
  if(u.includes('/book')) return {ok:true,json:async()=>({asks:[],bids:[]})};
  return {ok:true,json:async()=>({})};
};
let KV={};
const env={ NTFY_TOPIC:'t', BOT_STATE:{ get:async k=>KV[k]||null, put:async(k,v)=>{KV[k]=v;} } };
const {cycle}=require('/tmp/w.cjs');
(async()=>{
  const s1=await cycle(env);
  console.log('--- cycle 1 ---');
  console.log('alerts:', (s1.alerts||[]).map(a=>`${a.score} cl=${a.cluster} ${a.title.slice(0,32)}`));
  console.log('pushes:', pushes.length); pushes.forEach(p=>console.log('   ', String(p).slice(0,95)));
  const n1=pushes.length;
  const s2=await cycle(env);
  console.log('--- cycle 2 (same data — must NOT re-push) ---');
  console.log('new pushes:', pushes.length-n1, '(expect 0)');
  console.log('alerts retained:', (s2.alerts||[]).length);
  const sports=(s2.alerts||[]).filter(a=>/Lakers/.test(a.title)).length;
  console.log('sports noise alerted:', sports, '(expect 0)');
  console.log(sports===0 && pushes.length-n1===0 && n1>=2 ? 'PASS' : 'FAIL');
})();
