/* wtest16 — CALIBRATION CURVE (audit Idea 7, redone as a portfolio question).
   The crowd-bias hypothesis was tested once and came back null, but it was asked of the wrong
   population: trades sampled from a tape. That measures what traders did. The portfolio question
   is different — across resolved markets, does an outcome priced at 8c win 8% of the time? — and
   it is the one the favourite-longshot literature actually answers.

   The trap this test exists to prevent: a calibration curve is a machine for manufacturing false
   findings. Twenty buckets, each with its own noise, and the eye lands on whichever one looks
   biggest. So every band carries a Wilson interval and a band may only be called OVERPRICED or
   UNDERPRICED when that interval excludes its own implied price. Everything else is 'no call'.

   Asserts:
     1. one observation per market — never both outcomes of a binary market
     2. prices are taken from BEFORE the horizon, never after (no lookahead)
     3. a band whose interval straddles its implied price returns 'no call'
     4. a genuinely mispriced band with enough n is detected
     5. markets whose tape does not reach back are SKIPPED and counted, not defaulted
     6. calibration costs zero extra subrequests                                            */
const fs = require('fs');
let src = fs.readFileSync('worker.js', 'utf8').replace(/export default/, 'const H =');
src += '\n;module.exports={cycle,HANDLER:H};'; fs.writeFileSync('/tmp/w16.cjs', src);

const DAY = 86400, END = Date.parse('2026-08-01T00:00:00Z');
const iso = ms => new Date(ms).toISOString();

/* 120 resolved markets. Outcome 0 is priced at 10c in 60 of them and wins 30% of the time — a
   large, deliberate longshot mispricing that a working curve must find. The other 60 are priced
   at 50c and win exactly half the time, which must come back 'no call'. */
const MK = [], TAPES = {};
for (let i = 0; i < 120; i++) {
  const cheap = i < 60;
  const cid = (cheap ? 'L' : 'F') + i;
  const px = cheap ? 0.10 : 0.50;
  const wins0 = cheap ? (i % 10 < 3) : (i % 2 === 0);      // 30% vs 50%
  MK.push({ conditionId: cid, question: `Resolved market ${i}`, endDate: iso(END), feesEnabled: false });
  TAPES[cid] = [
    /* the honest observation: outcome 0, comfortably before both horizons */
    { side: 'BUY', price: px, outcomeIndex: 0, timestamp: END / 1000 - 9 * DAY },
    /* a LATER trade at a wildly different price, AFTER the 24h horizon. If the code takes this,
       it is peeking at information the trader could not have had. */
    { side: 'BUY', price: 0.97, outcomeIndex: 0, timestamp: END / 1000 - 600 },
    /* the complementary outcome, which must NOT create a second observation */
    { side: 'BUY', price: 1 - px, outcomeIndex: 1, timestamp: END / 1000 - 9 * DAY },
  ];
  TAPES[cid]._wins0 = wins0;
}
/* one market whose tape starts after the 24h horizon — must be skipped, not guessed */
MK.push({ conditionId: 'SHORTTAPE', question: 'Busy market, tape does not reach back', endDate: iso(END), feesEnabled: false });
TAPES.SHORTTAPE = [{ side: 'BUY', price: 0.42, outcomeIndex: 0, timestamp: END / 1000 - 60 }];

let subreqs = 0, page = 0;
global.fetch = async (u) => {
  u = String(u); subreqs++;
  if (u.includes('ntfy.sh')) return { ok: true, json: async () => ({}) };
  if (u.includes('closed=true')) {
    const off = page * 20; page++;
    return { ok: true, json: async () => MK.slice(off % 140, (off % 140) + 20) };
  }
  if (u.includes('gamma-api')) return { ok: true, json: async () => [] };
  if (u.includes('clob.polymarket.com/markets/')) {
    const cid = decodeURIComponent(u.split('/markets/')[1]);
    const w0 = cid === 'SHORTTAPE' ? true : !!(TAPES[cid] && TAPES[cid]._wins0);
    return { ok: true, json: async () => ({ closed: true, tokens: [
      { token_id: cid + '-0', winner: w0 }, { token_id: cid + '-1', winner: !w0 }] }) };
  }
  if (u.includes('trades?market=')) {
    const cid = decodeURIComponent(u.split('trades?market=')[1].split('&')[0]);
    return { ok: true, json: async () => (TAPES[cid] || []) };
  }
  if (u.includes('/book')) return { ok: true, json: async () => ({ bids: [], asks: [] }) };
  return { ok: true, json: async () => [] };
};
let KV = {};
const env = { NTFY_TOPIC: 't', BOT_STATE: { get: async k => KV[k] || null, put: async (k, v) => { KV[k] = v; } } };
const { cycle, HANDLER } = require('/tmp/w16.cjs');

const ok = [], bad = [];
const check = (n, p, d) => { (p ? ok : bad).push(n + (d ? ` — ${d}` : '')); };

(async () => {
  let st;
  for (let i = 0; i < 80; i++) st = await cycle(env);      // grind through the resolved list
  const v = JSON.parse(await (await HANDLER.fetch(new Request('https://x/'), env)).text());
  const c = v.calibration;
  const band = (rows, label) => rows.find(r => r.band === label);

  const cheap = band(c.h24, '10-15c'), fair = band(c.h24, '50-55c');
  check('cheap band populated', !!cheap && cheap.n > 30, cheap ? `n=${cheap.n}` : 'missing');
  check('fair band populated', !!fair && fair.n > 30, fair ? `n=${fair.n}` : 'missing');

  /* 1. one observation per market — outcome 1 at 90c must NOT have created an 85-90c row */
  const total = c.h24.reduce((a, r) => a + r.n, 0);
  check('1. one observation per market, not one per outcome',
    total <= 121 && !band(c.h24, '85-90c'), `total obs ${total} across ${c.h24.length} bands`);

  /* 2. no lookahead — the 97c trade sits inside the 24h window and must be ignored */
  check('2. price taken from before the horizon, not the 97c print at T-10min',
    !band(c.h24, '95-100c'), c.h24.map(r => r.band).join(','));

  /* 4. the planted 30%-at-10c mispricing must be found */
  check('4. planted longshot mispricing detected',
    cheap && cheap.verdict === 'UNDERPRICED' && cheap.realizedPct > 20,
    cheap ? `implied ${cheap.impliedPct}% realized ${cheap.realizedPct}% [${cheap.loPct},${cheap.hiPct}] -> ${cheap.verdict}` : 'missing');

  /* 3. the fair band must NOT be called */
  check('3. a correctly-priced band returns "no call"',
    fair && fair.verdict === 'no call',
    fair ? `implied ${fair.impliedPct}% realized ${fair.realizedPct}% [${fair.loPct},${fair.hiPct}] -> ${fair.verdict}` : 'missing');
  check('3. no band is called on noise alone',
    c.h24.every(r => r.verdict === 'no call' || r.n >= 20),
    c.h24.filter(r => r.verdict !== 'no call').map(r => `${r.band}:n=${r.n}`).join(',') || 'none called');

  /* 5. short-tape market skipped and counted */
  check('5. market whose tape does not reach the horizon is skipped and counted',
    c.coverage.skipped >= 1 && c.coverage.used >= 100,
    `used ${c.coverage.used}, skipped ${c.coverage.skipped}`);

  /* 6. zero extra subrequests: calibration reuses the sweep's tape */
  const cut0 = src.indexOf('/* ---- CALIBRATION');
  const cut1 = src.indexOf("if (winSide + loseSide === 0) { s.pennies.done[cid] = 'no-pennies'; continue; }");
  fs.writeFileSync('/tmp/w16-nocal.cjs', src.slice(0, cut0) + src.slice(cut1));
  const bare = require('/tmp/w16-nocal.cjs');
  KV = {}; page = 0; subreqs = 0;
  for (let i = 0; i < 6; i++) await cycle(env);
  const withCal = subreqs;
  KV = {}; page = 0; subreqs = 0;
  for (let i = 0; i < 6; i++) await bare.cycle(env);
  check('6. calibration adds ZERO subrequests', withCal === subreqs, `${withCal} with vs ${subreqs} without`);

  console.log(ok.map(l => '  ok  ' + l).join('\n'));
  if (bad.length) console.log(bad.map(l => '  FAIL ' + l).join('\n'));
  console.log('\nh24 curve:');
  for (const r of c.h24) console.log(`  ${r.band.padEnd(9)} n=${String(r.n).padStart(3)} implied ${String(r.impliedPct).padStart(5)}%  realized ${String(r.realizedPct).padStart(5)}% [${r.loPct}, ${r.hiPct}]  ${r.verdict}`);
  console.log(`\n${ok.length} passed, ${bad.length} failed`);
  console.log(bad.length ? 'FAIL' : 'PASS — calibration finds a planted bias and stays silent on noise');
})();
