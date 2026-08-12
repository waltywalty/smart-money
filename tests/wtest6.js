/* Migration must repair the two real records currently in Walton's store. */
const fs=require('fs');
let src=fs.readFileSync('worker.js','utf8').replace(/export default/,'const H =');
src+='\n;module.exports={HANDLER:H,migrate};'; fs.writeFileSync('/tmp/w6.cjs',src);
global.fetch = async ()=>({ok:true,json:async()=>[]});
// the exact shape currently live on the Worker
let KV={ state: JSON.stringify({ bank:1000, cash:982.003825, runs:330, equityLog:[], startedAt:1,
  positions:[
    {status:'open', title:'Will the Fed decrease interest rates by 25 bps after the September 2026 meeting?',
     entryPx:0.983, shares:18, cost:17.9, score:62, shapeScore:51, ctxBonus:12},
    {status:'closed', title:'Will Marco Rubio win the 2028 Republican presidential nomination?',
     limitPx:0.7323, pnl:0, exitReason:'limit never filled — cancelled', score:62, shapeScore:42, ctxBonus:20},
  ]})};
const env={NTFY_TOPIC:'t',BOT_STATE:{get:async k=>KV[k]||null,put:async(k,v)=>{KV[k]=v;}}};
const {HANDLER}=require('/tmp/w6.cjs');
(async()=>{
  const v = JSON.parse(await (await HANDLER.fetch(new Request('https://x/'),env)).text());
  console.log('closed:', v.closed, '(expect 0 — the Rubio row was never a trade)');
  console.log('wins:', v.wins, '| cancelled:', v.cancelled, '| voided:', v.voided, '| open:', v.open);
  console.log('cash:', v.cash.toFixed(2), '(expect ~999.90 — the 98.3c stake refunded)');
  v.positions.forEach(p=>console.log('  ', p.status, '|', (p.exitReason||'').slice(0,80)));
  const ok = v.closed===0 && v.cancelled===1 && v.voided===1 && v.open===0;
  console.log(ok?'PASS — both bad records repaired':'FAIL');
})();
