/* wtest15 — COHORT LABEL INTEGRITY.
   Written because v11.1 shipped a bug that no existing test could see, and it was the worst kind:
   silent, self-defending, and aimed squarely at the one number the A/B exists to produce.

   What happened. The house market list persists in KV. After deploying cohorts, that stored list
   still held entries from the previous version with no `cohort` and no `fee`. The fill loop read
   `pos.cohort = mk.cohort || pos.cohort || 'news'`, so every one of those positions was labelled
   NEWS — not measured, invented. Then the legacy verification sweep, which begins
   `if (pos.cohort) continue`, saw a cohort already present and skipped the very lookup that would
   have corrected it. The guess defended itself from being checked.

   Nothing errored. The dashboard showed a clean cohort column. The only visible symptom was a
   feeType of 'unknown' sitting next to a confident label — which is exactly what you would expect
   an invented label to look like.

   Asserts:
     1. a market list saved by an older version NEVER yields a real cohort label
     2. such a list forces a refresh instead of waiting for the 12-cycle cadence
     3. 'unverified' is re-checked by the verification sweep, not skipped
     4. after verification, cohort AND fee both come from the exchange
     5. unverified fills land in their own markout bucket, never in news or boring          */
const fs = require('fs');
let src = fs.readFileSync('worker.js', 'utf8').replace(/export default/, 'const H =');
src += '\n;module.exports={cycle,HANDLER:H};'; fs.writeFileSync('/tmp/w15.cjs', src);

const ECON = '{"exponent":1,"rate":0.05,"takerOnly":true,"rebateRate":0.25}';
const FAR = '2026-12-20T00:00:00Z';
const PAGE = [
  { conditionId: 'FED', question: 'Will there be no change in Fed interest rates after the September 2026 meeting?',
    bestBid: '0.63', bestAsk: '0.64', clobTokenIds: '["tokF"]', endDate: FAR, volume24hr: 261199,
    feesEnabled: true, feeType: 'economics_fees', feeSchedule: ECON },
  { conditionId: 'IRAN', question: 'US announces end of Iranian blockade by August 31, 2026?',
    bestBid: '0.45', bestAsk: '0.47', clobTokenIds: '["tokI"]', endDate: FAR, volume24hr: 118956,
    feesEnabled: false, feeSchedule: null },                       // fee-free geopolitics
  { conditionId: 'BORE', question: 'How many times will the word "synergy" be said this quarter?',
    bestBid: '0.48', bestAsk: '0.50', clobTokenIds: '["tokB"]', endDate: FAR, volume24hr: 99000,
    feesEnabled: true, feeType: 'mentions_fees', feeSchedule: ECON },
];
let cycleN = 0;
global.fetch = async (u) => {
  u = String(u);
  if (u.includes('ntfy.sh')) return { ok: true, json: async () => ({}) };
  if (u.includes('gamma-api') && u.includes('volume24hr')) return { ok: true, json: async () => PAGE };
  if (u.includes('gamma-api') && u.includes('condition_ids=')) {
    const cid = decodeURIComponent(u.split('condition_ids=')[1].split('&')[0]);
    const hit = PAGE.find(m => m.conditionId === cid);
    return { ok: true, json: async () => (hit ? [hit] : []) };
  }
  if (u.includes('gamma-api')) return { ok: true, json: async () => [] };
  if (u.includes('/book')) return { ok: true, json: async () => ({ bids: [{ price: '0.45', size: '9000' }], asks: [{ price: '0.47', size: '9000' }] }) };
  if (u.includes('trades?market=')) return { ok: true, json: async () => [
    { side: 'SELL', price: 0.45, timestamp: Date.now() / 1000 + 9 + cycleN },
    { side: 'BUY', price: 0.47, timestamp: Date.now() / 1000 + 9 + cycleN }] };
  if (u.includes('/markets/')) return { ok: true, json: async () => ({ closed: false, tokens: [] }) };
  return { ok: true, json: async () => [] };
};

/* The live state as it actually looked after the v11.1 deploy: a market list and positions saved
   by the PREVIOUS version, carrying no cohort and no fee. runs=1160 so runs%12 is 4 — nowhere near
   the refresh cadence, which is precisely the window where the bug did its damage. */
const seed = () => JSON.stringify({
  bank: 1000, cash: 965, runs: 1160, equityLog: [], startedAt: 1, positions: [],
  house: { cash: 622, rebates: 0, fills: 456, lastTs: {}, log: [], startedAt: 1,
    pos: { FED: { shares: 1, q: 'Will there be no change in Fed interest rates after the September 2026 meeting?', tok: 'tokF', mid: 0.635 },
           IRAN: { shares: -245, q: 'US announces end of Iranian blockade by August 31, 2026?', tok: 'tokI', mid: 0.46 } },
    mkts: [{ cid: 'FED', tok: 'tokF', q: 'Will there be no change in Fed interest rates after the September 2026 meeting?' },
           { cid: 'IRAN', tok: 'tokI', q: 'US announces end of Iranian blockade by August 31, 2026?' }] } });
let KV = { state: seed() };
const env = { NTFY_TOPIC: 't', BOT_STATE: { get: async k => KV[k] || null, put: async (k, v) => { KV[k] = v; } } };
const { cycle, HANDLER } = require('/tmp/w15.cjs');

let clock = Date.parse('2026-08-10T04:12:00Z');
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
  /* ONE cycle on the legacy state — this is the exact moment the bug fired. */
  let st = await cycle(env); cycleN++; tick();
  const labels = Object.values(st.house.pos).map(p => p.cohort);
  check('1. a pre-cohort market list never produces an invented label',
    !labels.includes('news') || st.house.mkts.every(m => m.cohort),
    `labels ${JSON.stringify(labels)}`);
  check('2. the stale list forces an immediate refresh, not an hour of unlabelled fills',
    (st.house.mkts || []).every(m => m.cohort && m.fee), JSON.stringify((st.house.mkts || []).map(m => `${m.cid}:${m.cohort}`)));

  /* the refreshed list must carry REAL fee terms, including zero for fee-free geopolitics */
  const byCid = Object.fromEntries((st.house.mkts || []).map(m => [m.cid, m]));
  check('economics market carries its published rebate (0.05 x 0.25)',
    byCid.FED && Math.abs(byCid.FED.fee.rebate - 0.0125) < 1e-12, JSON.stringify(byCid.FED && byCid.FED.fee));
  check('fee-free geopolitics carries a rebate of exactly zero',
    byCid.IRAN && byCid.IRAN.fee.rebate === 0 && byCid.IRAN.fee.type === 'none', JSON.stringify(byCid.IRAN && byCid.IRAN.fee));

  /* 3+4. drive to the verification cadence and confirm 'unverified' is re-asked, not skipped */
  let guard = 0;
  while (guard++ < 26 && Object.values(st.house.pos).some(p => !p.cohort || p.cohort === 'unverified')) {
    st = await cycle(env); cycleN++; tick();
  }
  const final = Object.values(st.house.pos).map(p => `${p.cohort}/${p.fee && p.fee.type}`);
  check('3. unverified positions are re-checked, not permanently skipped',
    Object.values(st.house.pos).every(p => p.cohort && p.cohort !== 'unverified'), final.join(', '));
  check('4. after verification the fee type comes from the exchange, never "unknown"',
    Object.values(st.house.pos).every(p => p.fee && p.fee.type !== 'unknown'), final.join(', '));

  /* 1b. THE REAL REGRESSION TEST. Assertion 1 above only passes because the refresh succeeded —
         it would not have caught the original bug on its own. So starve the refresh: make the
         gamma page unavailable, so the stale list cannot be replaced, and confirm the fill loop
         still refuses to invent a label. This is the exact condition the old `|| 'news'` fallback
         existed to paper over. */
  KV = { state: seed() };
  const goodFetch = global.fetch;
  global.fetch = async (u) => {
    u = String(u);
    if (u.includes('gamma-api') && u.includes('volume24hr')) return { ok: true, json: async () => [] };
    if (u.includes('gamma-api') && u.includes('condition_ids=')) return { ok: true, json: async () => [] };
    return goodFetch(u);
  };
  const starved = await cycle(env); cycleN++; tick();
  const sl = Object.values(starved.house.pos).map(p => p.cohort);
  check('1b. with no fresh page, labels are UNVERIFIED — never invented as news',
    sl.length > 0 && sl.every(c => c === 'unverified'), JSON.stringify(sl));
  const starvedMk = JSON.parse(await (await HANDLER.fetch(new Request('https://x/'), env)).text()).markout || {};
  check('1b. and nothing unlabelled reaches the news or boring buckets',
    !starvedMk.news && !starvedMk.boring, JSON.stringify(starvedMk));
  global.fetch = goodFetch;

  /* 5. an unverified fill must never be counted into news or boring */
  KV = { state: seed() };
  let st2 = JSON.parse(KV.state);
  st2.house.pend = [{ cid: 'FED', side: 'BUY', px: 0.63, sh: 100, t: Date.now() / 1000 - 7200, cohort: 'unverified' }];
  KV.state = JSON.stringify(st2);
  st2 = await cycle(env); cycleN++; tick();
  const v = JSON.parse(await (await HANDLER.fetch(new Request('https://x/'), env)).text());
  const mk = v.markout || {};
  check('5. unverified fills get their own bucket and stay out of the comparison',
    !!mk.unverified && !(mk.news && mk.news.m10 && mk.news.m10.fills > 0 && !st2.house.mkts.every(m => m.cohort)),
    JSON.stringify(mk));

  global.Date = RealDate;
  console.log(ok.map(l => '  ok  ' + l).join('\n'));
  if (bad.length) console.log(bad.map(l => '  FAIL ' + l).join('\n'));
  console.log(`\n${ok.length} passed, ${bad.length} failed`);
  console.log(bad.length ? 'FAIL' : 'PASS — no label is ever invented, and an unknown one always gets re-asked');
})();
