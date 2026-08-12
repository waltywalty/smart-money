/* House mode mechanics + fee economics.
   The last assertion here used to be `rebates > 0`, which passed for years against a hardcoded
   1.25%. That constant turned out to be the top of the real range and flatly wrong for the markets
   this book actually holds — geopolitics is fee-free and funds no rebate pool at all, yet $142 of a
   $436 mark had accrued from it. So the test now checks the ARITHMETIC against the schedule the
   exchange publishes per market, and checks that a fee-free market earns exactly nothing.
   Covers: (a) a SELL through our bid fills our buy, (b) a BUY through our ask fills our sell,
   (c) rebate credited at the market's own rate, (d) fee-free markets credit zero, (e) equity
   finite, (f) markout accrues per cohort with the correct sign. */
const fs = require('fs');
let src = fs.readFileSync('worker.js', 'utf8').replace(/export default/, 'const H =');
src += '\n;module.exports={cycle,HANDLER:H};'; fs.writeFileSync('/tmp/w7.cjs', src);

const POLI_SCHED = '{"exponent":1,"rate":0.04,"takerOnly":true,"rebateRate":0.25}';
const FAR = '2026-12-20T00:00:00Z';
let cycleN = 0, FEEFREE = false;
const mkt = () => (FEEFREE
  ? { conditionId: 'HM1', question: 'Will the U.S. invade Iran before 2027?', bestBid: '0.48', bestAsk: '0.50',
      clobTokenIds: '["tokHM1","tokHM1b"]', volume24hr: 900000, endDate: FAR, feesEnabled: false, feeSchedule: null }
  : { conditionId: 'HM1', question: 'Will the Fed cut rates in September?', bestBid: '0.48', bestAsk: '0.50',
      clobTokenIds: '["tokHM1","tokHM1b"]', volume24hr: 900000, endDate: FAR,
      feesEnabled: true, feeType: 'politics_fees', feeSchedule: POLI_SCHED });

global.fetch = async (u) => {
  u = String(u);
  if (u.includes('ntfy.sh')) return { ok: true, json: async () => ({}) };
  if (u.includes('gamma-api') && u.includes('volume24hr')) return { ok: true, json: async () => [mkt()] };
  if (u.includes('gamma-api') && u.includes('condition_ids=')) return { ok: true, json: async () => [mkt()] };
  if (u.includes('gamma-api')) return { ok: true, json: async () => [] };
  if (u.includes('/book')) return { ok: true, json: async () => ({ bids: [{ price: '0.48', size: '4000' }], asks: [{ price: '0.52', size: '200' }, { price: '0.50', size: '4000' }] }) };
  if (u.includes('trades?market=HM1')) return { ok: true, json: async () => [
    { side: 'SELL', price: 0.48, timestamp: Date.now() / 1000 + 9 + cycleN, transactionHash: 's' + cycleN },
    { side: 'BUY', price: 0.50, timestamp: Date.now() / 1000 + 9 + cycleN, transactionHash: 'b' + cycleN },
  ] };
  if (u.includes('filterAmount')) return { ok: true, json: async () => [] };
  if (u.includes('/markets/')) return { ok: true, json: async () => ({ closed: false, tokens: [] }) };
  return { ok: true, json: async () => ({}) };
};
let KV = {};
const env = { NTFY_TOPIC: 't', BOT_STATE: { get: async k => KV[k] || null, put: async (k, v) => { KV[k] = v; } } };
const { cycle, HANDLER } = require('/tmp/w7.cjs');

/* Markout matures at 10 and 60 minutes, so the clock has to move — otherwise every cycle happens
   inside the same millisecond and no horizon is ever reached. Five minutes per cycle, matching the
   real cron. */
let clock = Date.parse('2026-08-10T09:00:00Z');
const RealDate = Date;
global.Date = class extends RealDate {
  constructor(...a) { return a.length ? new RealDate(...a) : new RealDate(clock); }
  static now() { return clock; }
  static parse(x) { return RealDate.parse(x); }
};
const tick = () => { clock += 5 * 60 * 1000; };

const ok = [], bad = [];
const check = (n, p, d) => { (p ? ok : bad).push(n + (d ? ` — ${d}` : '')); };

(async () => {
  let st = await cycle(env); cycleN++; tick();
  const h = st.house;
  check('both sides fill from the tape', h.buyFills > 0 && h.sellFills > 0, `${h.buyFills} buy / ${h.sellFills} sell`);

  /* (c) exact arithmetic: politics is rate 0.04 x rebate 0.25 = 0.01 per C*p*(1-p).
     Buy of `sh` at 0.48 and sell of `sh2` at 0.50 in the same cycle. */
  const pos = h.pos.HM1;
  check('fee terms read from the market object',
    pos.fee && Math.abs(pos.fee.rebate - 0.01) < 1e-12 && Math.abs(pos.fee.taker - 0.04) < 1e-12,
    JSON.stringify(pos.fee));
  const buys = (h.log || []).filter(l => l.startsWith('BUY'));
  const sells = (h.log || []).filter(l => l.startsWith('SELL'));
  check('one fill each side logged', buys.length === 1 && sells.length === 1, `${buys.length}/${sells.length}`);
  /* reconstruct expected rebate from the pending markout records, which carry exact size+price */
  const expected = (h.pend || []).reduce((a, e) => a + 0.01 * e.sh * e.px * (1 - e.px), 0);
  check('rebate credited at the market rate, to the cent',
    Math.abs(h.rebates - expected) < 1e-9, `booked ${h.rebates.toFixed(6)} vs expected ${expected.toFixed(6)}`);
  check('rebate is materially below the old flat 1.25% assumption',
    h.rebates > 0 && h.rebates < 0.81 * (expected / 0.01 * 0.0125),
    `${h.rebates.toFixed(4)} vs ${(expected / 0.01 * 0.0125).toFixed(4)} under the old constant`);

  /* (e) equity stays finite over repeated cycles */
  for (let i = 0; i < 6; i++) { st = await cycle(env); cycleN++; tick(); }
  const view = JSON.parse(await (await HANDLER.fetch(new Request('https://x/'), env)).text());
  check('equity finite after 7 cycles', Number.isFinite(view.house.equity), String(view.house.equity));
  check('fills continue each cycle', view.house.fills >= 8, String(view.house.fills));
  check('markout endpoint present with a news cohort', !!(view.markout && view.markout.news), JSON.stringify(view.markout));

  /* (f) markout sign: mid is flat at 0.49 here. A buy at 0.48 marks out +1c, a sell at 0.50
         marks out +1c — both favourable, because a flat mid means we simply earned the spread. */
  let guard = 0;
  while (!(view.markout && view.markout.news && view.markout.news.m10) && guard++ < 4) {
    st = await cycle(env); cycleN++; tick();
  }
  const v2 = JSON.parse(await (await HANDLER.fetch(new Request('https://x/'), env)).text());
  const m10 = v2.markout && v2.markout.news && v2.markout.news.m10;
  check('markout accrues at the 10-minute horizon', !!m10, JSON.stringify(v2.markout));
  if (m10) check('flat mid => positive markout (we earned the spread)', m10.centsPerShare > 0.5,
    `${m10.centsPerShare}c/share over ${m10.fills} fills`);

  /* (d) the fee-free case: same flow, zero rebate, forever */
  FEEFREE = true; KV = {}; cycleN = 0;
  let st3 = await cycle(env); cycleN++; tick();
  for (let i = 0; i < 3; i++) { st3 = await cycle(env); cycleN++; tick(); }
  check('fee-free market fills but credits ZERO rebate',
    st3.house.fills > 0 && st3.house.rebates === 0,
    `${st3.house.fills} fills, rebates ${st3.house.rebates}`);

  global.Date = RealDate;
  console.log(ok.map(l => '  ok  ' + l).join('\n'));
  if (bad.length) console.log(bad.map(l => '  FAIL ' + l).join('\n'));
  console.log(`\n${ok.length} passed, ${bad.length} failed`);
  console.log(bad.length ? 'FAIL' : 'PASS — fills work, rebates match the published schedule, fee-free markets pay nothing');
})();
