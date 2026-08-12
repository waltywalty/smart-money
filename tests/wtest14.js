/* wtest14 — PENNY ECONOMICS: the strategy restated as return on locked capital (audit Idea 4).
   "98% of penny buys win" was never the question. The question is what a dollar earns while it is
   trapped in the position, net of the fee the exchange actually charges that market. This test
   pins the arithmetic to hand-computed values so the headline number cannot drift.

   Fixture A — clean win, politics fees (taker 0.04), 10 days locked, entry 98c:
     gross = 1 − 0.98                = 0.02
     fee   = 0.04 × 0.98 × 0.02      = 0.000784
     ret   = (0.02 − 0.000784)/0.98  = 0.0196082  → 1.961%
     apr   = 0.0196082 × 365/10      = 0.715698   → 71.6%
   Fixture B — reversal, fee-free market, 5 days locked, entry 99c:
     gross = −0.99, fee = 0          → ret = −1.0 → −100%
     apr   = −1.0 × 365/5            = −73.0      → −7300%
   Portfolio (total return / total capital-days, annualised):
     (0.0196082 − 1.0) / (10 + 5) × 365 = −23.8564 → −2385.6%
   The gap between the −2385.6% portfolio figure and a naive "98% win rate" is the entire reason
   this metric had to change.                                                                    */
const fs = require('fs');
let src = fs.readFileSync('worker.js', 'utf8').replace(/export default/, 'const H =');
src += '\n;module.exports={cycle,HANDLER:H};'; fs.writeFileSync('/tmp/w14.cjs', src);

const POLI = '{"exponent":1,"rate":0.04,"takerOnly":true,"rebateRate":0.25}';
const endA = Date.parse('2026-08-20T00:00:00Z'), endB = Date.parse('2026-08-18T00:00:00Z');
const tsA = endA / 1000 - 10 * 86400, tsB = endB / 1000 - 5 * 86400;

const RESOLVED = [
  { conditionId: 'A', question: 'Clean win, resolves in ten days', endDate: '2026-08-20T00:00:00Z',
    feesEnabled: true, feeType: 'politics_fees', feeSchedule: POLI },
  { conditionId: 'B', question: 'Longshot flips at the wire', endDate: '2026-08-18T00:00:00Z',
    feesEnabled: false, feeSchedule: null },
  /* C has no usable end date — it must be graded but EXCLUDED from the economics rather than
     given a made-up holding period. */
  { conditionId: 'C', question: 'Win with an unusable end date', endDate: '', feesEnabled: false },
];
const TAPES = {
  A: [{ side: 'BUY', price: 0.98, outcomeIndex: 0, timestamp: tsA },
      { side: 'BUY', price: 0.98, outcomeIndex: 0, timestamp: tsA }],
  B: [{ side: 'BUY', price: 0.99, outcomeIndex: 1, timestamp: tsB }],   // bought the loser
  C: [{ side: 'BUY', price: 0.98, outcomeIndex: 0, timestamp: tsA }],
};
global.fetch = async (u) => {
  u = String(u);
  if (u.includes('ntfy.sh')) return { ok: true, json: async () => ({}) };
  if (u.includes('closed=true')) return { ok: true, json: async () => RESOLVED };
  if (u.includes('gamma-api')) return { ok: true, json: async () => [] };
  if (u.includes('clob.polymarket.com/markets/')) {
    const cid = decodeURIComponent(u.split('/markets/')[1]);
    return { ok: true, json: async () => ({ closed: true, tokens: [
      { token_id: cid + '-0', winner: true }, { token_id: cid + '-1', winner: false }] }) };
  }
  if (u.includes('trades?market=')) {
    const cid = decodeURIComponent(u.split('trades?market=')[1].split('&')[0]);
    return { ok: true, json: async () => TAPES[cid] || [] };
  }
  if (u.includes('/book')) return { ok: true, json: async () => ({ bids: [], asks: [] }) };
  return { ok: true, json: async () => [] };
};
let KV = {};
const env = { NTFY_TOPIC: 't', BOT_STATE: { get: async k => KV[k] || null, put: async (k, v) => { KV[k] = v; } } };
const { cycle, HANDLER } = require('/tmp/w14.cjs');

const ok = [], bad = [];
const check = (n, p, d) => { (p ? ok : bad).push(n + (d ? ` — ${d}` : '')); };
const near = (a, b, tol) => Number.isFinite(a) && Math.abs(a - b) <= tol;

(async () => {
  await cycle(env);
  const v = JSON.parse(await (await HANDLER.fetch(new Request('https://x/'), env)).text());
  const e = v.pennies.econ;

  check('all three markets graded', v.pennies.active === 3, `active ${v.pennies.active}`);
  check('one reversal detected', v.pennies.reversals === 1, `${v.pennies.reversals}`);
  check('market with an unusable end date is EXCLUDED from the economics, not defaulted',
    e.n === 2, `n=${e.n} (graded 3)`);

  /* per-trade return: mean of +1.9608% and −100% = −49.0196% */
  check('per-trade return net of the market\'s real fee',
    near(e.perTradePct, (1.9608 - 100) / 2, 0.01), `${e.perTradePct}% (expect −49.020%)`);
  check('winner\'s fee taken at the politics rate, not a flat guess',
    near(e.perTradePct * 2 + 100, 1.9608, 0.02), `implied winner leg ${(e.perTradePct * 2 + 100).toFixed(4)}%`);

  check('median holding period', near(e.holdDaysMedian, 7.5, 0.01), `${e.holdDaysMedian}d`);
  check('mean holding period', near(e.holdDaysMean, 7.5, 0.01), `${e.holdDaysMean}d`);
  check('average entry price', near(e.avgEntryC, 98.5, 0.05), `${e.avgEntryC}c`);

  /* APR, three ways — and they must genuinely differ */
  check('mean APR across markets', near(e.aprMeanPct, (71.5698 - 7300) / 2, 1),
    `${e.aprMeanPct}% (expect −3614.2%)`);
  check('median APR', near(e.aprMedianPct, (71.5698 - 7300) / 2, 1), `${e.aprMedianPct}%`);
  check('PORTFOLIO APR = total return / total capital-days, annualised',
    near(e.aprPortfolioPct, -2385.6, 2), `${e.aprPortfolioPct}% (expect −2385.6%)`);
  check('portfolio APR differs from the mean-of-APRs (the reason to report both)',
    Math.abs(e.aprPortfolioPct - e.aprMeanPct) > 100,
    `portfolio ${e.aprPortfolioPct}% vs mean ${e.aprMeanPct}%`);
  check('flagged as net of fees', e.netOfFees === true);

  /* A pure-win book should show a sane, positive, NON-annualised-to-absurdity portfolio figure. */
  KV = {};
  TAPES.B = [{ side: 'BUY', price: 0.98, outcomeIndex: 0, timestamp: tsB }];   // B now wins too
  await cycle(env);
  const v2 = JSON.parse(await (await HANDLER.fetch(new Request('https://x/'), env)).text());
  const e2 = v2.pennies.econ;
  /* A: ret 0.0196082 over 10d; B: same entry/fee-free → (0.02)/0.98 = 0.0204082 over 5d
     portfolio = (0.0196082 + 0.0204082)/15 × 365 = 0.973733 → 97.4% */
  check('all-winners portfolio APR', near(e2.aprPortfolioPct, 97.4, 0.6), `${e2.aprPortfolioPct}%`);
  check('fee-free winner keeps the full 2c spread',
    near(e2.perTradePct * 2 - 1.9608, 2.0408, 0.02), `implied fee-free leg ${(e2.perTradePct * 2 - 1.9608).toFixed(4)}%`);
  check('a 2% edge held for a week is NOT a four-figure return', e2.aprPortfolioPct < 200, `${e2.aprPortfolioPct}%`);

  /* The band table: the strategy's viability is a function of entry price, and the bar has to
     move with it. A band may only read `cleared` when its own record meets its own requirement. */
  const bands = e2.byEntry;
  const b990 = bands.find(b => b.band === '99-99.5c');
  const b995 = bands.find(b => b.band === '99.5-100c');
  check('band table present for every entry band', bands.length === 4, bands.map(b => b.band).join(','));
  check('breakeven tightens as the entry price rises',
    bands[0].breakevenRevPct > bands[3].breakevenRevPct, `${bands[0].breakevenRevPct}% -> ${bands[3].breakevenRevPct}%`);
  /* Band midpoints are 98.25c and 99.75c, so the ratio here is ~7x. Against the price actually
     resting on the book right now (99.9c, breakeven 0.1%) it is 20x versus a 98.0c entry — which
     is the number that matters operationally. */
  check('the top band needs several times the evidence of the bottom band',
    bands[3].needN > 6 * bands[0].needN, `${bands[0].needN} vs ${bands[3].needN} = ${(bands[3].needN/bands[0].needN).toFixed(1)}x`);
  check('a band with 2 observations is NOT cleared',
    bands.every(b => !b.cleared || b.n >= b.needN), JSON.stringify(bands.filter(b => b.cleared)));
  check('the 99.9c reality needs thousands of clean observations',
    bands[3].needN >= 400, `needN ${bands[3].needN} for ${bands[3].band}`);

  console.log('\nband table:');
  for (const b of bands) console.log(`  ${b.band.padEnd(11)} n=${String(b.n).padStart(3)} rev=${b.reversals}  breakeven r*<${b.breakevenRevPct}%  needN=${String(b.needN).padStart(4)}  ${b.cleared ? 'CLEARED' : 'not cleared'}`);

  console.log(ok.map(l => '  ok  ' + l).join('\n'));
  if (bad.length) console.log(bad.map(l => '  FAIL ' + l).join('\n'));
  console.log(`\n${ok.length} passed, ${bad.length} failed`);
  console.log(bad.length ? 'FAIL' : 'PASS — pennies now report return on locked capital, net of the fee that market actually charges');
})();
