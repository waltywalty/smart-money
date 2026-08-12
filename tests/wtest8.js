/* Sports exclusion — rewritten when the news-only allowlist became a two-cohort A/B.
   The old test asserted that a Bayern market was excluded by its TITLE. That defence was always
   an accident: the title regex misses "Will Bayern Munich win on 2026-08-07?" (no "vs", no league
   word), and it only looked like it worked because the old rule quoted news markets exclusively,
   so everything unclassified was dropped anyway. The moment 'other' became a cohort we want to
   quote, that accident turned into an open door.
   So this now tests the defence that actually holds: the exchange's OWN sports metadata. Real
   Polymarket sports markets carry feeType 'sports_fees_v2' plus game fields, and those are what
   the selector reads. Three separate ways in are checked:
     A. a sports market offered in the page must never be picked, however its title reads
     B. a legacy stored position with no metadata must be re-verified against the API and purged
     C. a market inside the resolution blackout must still be excluded
   Plus: the boring cohort must actually open (otherwise the A/B has one arm). */
const fs = require('fs');
let src = fs.readFileSync('worker.js', 'utf8').replace(/export default/, 'const H =');
src += '\n;module.exports={cycle,HANDLER:H};'; fs.writeFileSync('/tmp/w8.cjs', src);

/* Fixtures mirror the real API shape, including the fee schedules quoted in worker.js. */
const SPORTS_SCHED = '{"exponent":1,"rate":0.05,"takerOnly":true,"rebateRate":0.15}';
const POLI_SCHED = '{"exponent":1,"rate":0.04,"takerOnly":true,"rebateRate":0.25}';
const GEN_SCHED = '{"exponent":1,"rate":0.05,"takerOnly":true,"rebateRate":0.25}';
const FAR = '2026-12-20T00:00:00Z';
const PAGE = [
  /* A: title the regex cannot catch, but the exchange labels it sports */
  { conditionId: 'SPT1', question: 'Will Bayern Munich win on 2026-08-07?', bestBid: '0.48', bestAsk: '0.50',
    clobTokenIds: '["tokS"]', endDate: FAR, feesEnabled: true, feeType: 'sports_fees_v2',
    feeSchedule: SPORTS_SCHED, gameStartTime: '2026-08-07T18:00:00Z', sportsMarketType: 'moneyline' },
  /* C: news, but inside the 4-day resolution blackout */
  { conditionId: 'SOON', question: 'US announces end of Iranian blockade by August 9, 2026?', bestBid: '0.40',
    bestAsk: '0.42', clobTokenIds: '["tokSoon"]', endDate: '2026-08-09T00:00:00Z', feesEnabled: false },
  { conditionId: 'NEWS', question: 'Will the Fed cut rates in September?', bestBid: '0.48', bestAsk: '0.50',
    clobTokenIds: '["tokN"]', endDate: FAR, feesEnabled: true, feeType: 'politics_fees', feeSchedule: POLI_SCHED },
  /* the boring arm of the A/B */
  { conditionId: 'BORE', question: 'How many times will the word "synergy" be said this quarter?',
    bestBid: '0.48', bestAsk: '0.50', clobTokenIds: '["tokB"]', endDate: FAR,
    feesEnabled: true, feeType: 'mentions_fees', feeSchedule: GEN_SCHED },
];

global.fetch = async (u) => {
  u = String(u);
  if (u.includes('ntfy.sh')) return { ok: true, json: async () => ({}) };
  if (u.includes('gamma-api') && u.includes('volume24hr')) return { ok: true, json: async () => PAGE };
  /* B: the legacy re-verification lookup by conditionId */
  if (u.includes('gamma-api') && u.includes('condition_ids=')) {
    const cid = decodeURIComponent(u.split('condition_ids=')[1].split('&')[0]);
    const hit = PAGE.find(m => m.conditionId === cid);
    return { ok: true, json: async () => (hit ? [hit] : []) };
  }
  if (u.includes('gamma-api')) return { ok: true, json: async () => [] };
  if (u.includes('/book')) return { ok: true, json: async () => ({ bids: [{ price: '0.44', size: '900' }], asks: [{ price: '0.46', size: '900' }] }) };
  if (u.includes('trades?market=')) return { ok: true, json: async () => [] };
  if (u.includes('filterAmount')) return { ok: true, json: async () => [] };
  if (u.includes('/markets/')) return { ok: true, json: async () => ({ closed: false, tokens: [] }) };
  return { ok: true, json: async () => ({}) };
};

/* Seed the real damage: short 292 Bayern at mid 0.505, stored with NO metadata — exactly how a
   position from the pre-cohort era looks on disk. runs=13 so the next cycle hits both the
   selection refresh (%12==1... after increment) and, later, the verification cadence. */
const seed = () => JSON.stringify({ bank: 1000, cash: 982, runs: 12, equityLog: [], startedAt: 1, positions: [],
  house: { cash: 148.5, rebates: 2.8, fills: 9, lastTs: {}, log: [], startedAt: 1,
    pos: { SPT1: { shares: -292, q: 'Will Bayern Munich win on 2026-08-07?', tok: 'tokS', mid: 0.505 },
           NEWS: { shares: 2, q: 'Will the Fed cut rates in September?', tok: 'tokN', mid: 0.48 } },
    mkts: [{ cid: 'SPT1', tok: 'tokS', q: 'Will Bayern Munich win on 2026-08-07?' },
           { cid: 'NEWS', tok: 'tokN', q: 'Will the Fed cut rates in September?' }] } });
let KV = { state: seed() };
const env = { NTFY_TOPIC: 't', BOT_STATE: { get: async k => KV[k] || null, put: async (k, v) => { KV[k] = v; } } };
const { cycle } = require('/tmp/w8.cjs');

const ok = [], bad = [];
const check = (n, p, d) => { (p ? ok : bad).push(n + (d ? ` — ${d}` : '')); };

(async () => {
  /* runs 12 -> 13: %12==1, selection refresh */
  let st = await cycle(env);
  const picked = (st.house.mkts || []).map(m => m.cid).sort();
  check('A: exchange-labelled sports never picked, whatever the title says',
    !picked.includes('SPT1'), picked.join(','));
  check('C: market inside the resolution blackout excluded', !picked.includes('SOON'), picked.join(','));
  check('both cohorts open, so the A/B has two arms',
    picked.includes('NEWS') && picked.includes('BORE'), picked.join(','));
  const cohorts = (st.house.mkts || []).map(m => `${m.cid}:${m.cohort}`).sort().join(',');
  check('cohorts tagged from the classifier', cohorts === 'BORE:boring,NEWS:news', cohorts);

  /* fee terms must come from the market, not from a constant */
  const feeOf = c => ((st.house.mkts || []).find(m => m.cid === c) || {}).fee || {};
  check('politics rebate = 0.04 x 0.25', Math.abs((feeOf('NEWS').rebate || 0) - 0.01) < 1e-9, String(feeOf('NEWS').rebate));
  check('general rebate = 0.05 x 0.25', Math.abs((feeOf('BORE').rebate || 0) - 0.0125) < 1e-9, String(feeOf('BORE').rebate));

  /* B: drive to the verification cadence (%12==2) and confirm the legacy short is purged */
  let n = 0;
  while (st.house.pos.SPT1 && n++ < 15) st = await cycle(env);
  check('B: legacy sports position re-verified against the API and removed',
    !st.house.pos.SPT1, `after ${n} extra cycles`);
  const removedLog = (st.house.log || []).find(l => /REMOVED.*Bayern/i.test(l));
  check('removal is logged, not silent', !!removedLog, removedLog || 'MISSING');
  check('closed at the mark, not at zero',
    Math.abs(st.house.cash - (148.5 + (-292 * 0.505))) < 1.5 || /at 5[01]c/.test(removedLog || ''),
    `cash ${st.house.cash.toFixed(2)}, log: ${(removedLog || '').slice(-24)}`);

  /* the fee-free market must credit no rebate at all */
  KV = { state: seed() };
  let st2 = await cycle(env);
  for (let i = 0; i < 3; i++) st2 = await cycle(env);
  const audit = st2.house.rebateAudit;
  check('legacy assumed-rebate total quarantined once, with the reason recorded',
    !!audit && audit.discarded === 2.8 && /1\.25%/.test(audit.why), JSON.stringify(audit));

  console.log(ok.map(l => '  ok  ' + l).join('\n'));
  if (bad.length) console.log(bad.map(l => '  FAIL ' + l).join('\n'));
  console.log(`\n${ok.length} passed, ${bad.length} failed`);
  console.log(bad.length ? 'FAIL' : 'PASS — sports barred by exchange metadata, legacy books re-verified, fees read not assumed');
})();
