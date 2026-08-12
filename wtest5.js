/* Results relay: POST with the right key stores, wrong key is rejected, GET returns the list. */
const fs=require('fs');
let src=fs.readFileSync('worker.js','utf8').replace(/export default/,'const H =');
src+='\n;module.exports={HANDLER:H};'; fs.writeFileSync('/tmp/w5.cjs',src);
global.fetch = async ()=>({ok:true,json:async()=>[]});
let KV={}; const env={NTFY_TOPIC:'secret-topic',BOT_STATE:{get:async k=>KV[k]||null,put:async(k,v)=>{KV[k]=v;}}};
const {HANDLER}=require('/tmp/w5.cjs');
const call=(url,opts)=>HANDLER.fetch(new Request(url,opts),env);
(async()=>{
  const bad = await call('https://x/results?k=wrong',{method:'POST',body:JSON.stringify({study:'x'})});
  console.log('wrong key ->', bad.status, '(expect 403)');
  const ok = await call('https://x/results?k=secret-topic',{method:'POST',
    headers:{'content-type':'application/json'},
    body:JSON.stringify({study:'score-validation',verdict:'No ranking power — gap +0.0 ± 3.8',n:5378})});
  console.log('right key ->', ok.status, await ok.text());
  await call('https://x/results?k=secret-topic',{method:'POST',headers:{'content-type':'application/json'},
    body:JSON.stringify({study:'free-money-scanner',verdict:'No arbitrage right now',sets:39})});
  const got = JSON.parse(await (await call('https://x/results')).text());
  console.log('stored:', got.length, got.map(r=>r.study));
  console.log('first verdict:', got[0].verdict);
  const pre = await call('https://x/results',{method:'OPTIONS'});
  console.log('CORS preflight ->', pre.status, pre.headers.get('access-control-allow-methods'));
  console.log(bad.status===403 && got.length===2 ? 'PASS' : 'FAIL');
})();
