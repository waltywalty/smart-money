/* wtest13 — POINT-IN-TIME RECORDER (worker §5c)
   The recorder is the one component whose failure is unrecoverable: a missed hour is an hour of
   book history that no API will ever sell back to us. So this tests the operational properties
   (cost, ceiling, retention) at least as hard as the correctness ones.
   Asserts:
     1. one KV write per cycle for the tape (288/day < ~1k/day free allowance)
     2. ZERO extra subrequests vs the same worker with the recorder disabled
     3. hour sharding — cost per cycle is FLAT, not ramping through the day
     4. state does NOT carry the gamma page (the saveState bloat bug)
     5. values survive the round trip at millicent precision
     6. /tape stitches hour shards into one time-ordered day, and gaps stay gaps
     7. the coverage index never advertises more days than the TTL keeps
     8. a recorder failure cannot take down the cycle                                            */
const fs = require('fs');
let src = fs.readFileSync('worker.js', 'utf8').replace(/export default/, 'const H =');
src += '\n;module.exports={cycle,HANDLER:H,TAPE_TTL_DAYS};';
fs.writeFileSync('/tmp/w13.cjs', src);

let subreqs = 0;
const PAGE = Array.from({ length: 40 }, (_, i) => ({
  conditionId: '0x' + String(i).padStart(4, '0') + 'abcdef0123456789',
  question: i % 2 ? `Will policy item ${i} pass?` : `Will the Fed do thing ${i}?`,
  bestBid: (0.30 + i * 0.005).toFixed(4), bestAsk: (0.32 + i * 0.005).toFixed(4),
  volume24hr: String(100000 - i * 137), clobTokenIds: `["t${i}"]`,
  endDate: new Date(Date.now() + 30 * 864e5).toISOString(),
}));
global.fetch = async (u) => {
  u = String(u); subreqs++;
  if (u.includes('ntfy.sh')) return { ok: true, json: async () => ({}) };
  if (u.includes('gamma-api') && u.includes('volume24hr')) return { ok: true, json: async () => PAGE };
  if (u.includes('/book')) return { ok: true, json: async () => ({ bids: [{ price: '0.30', size: '9000' }], asks: [{ price: '0.32', size: '9000' }] }) };
  if (u.includes('/markets/')) return { ok: true, json: async () => ({ closed: false, tokens: [] }) };
  return { ok: true, json: async () => [] };
};

let KV = {}, writes = [];
const mkEnv = () => ({ NTFY_TOPIC: 't', BOT_STATE: {
  get: async k => KV[k] || null,
  put: async (k, v, o) => { KV[k] = v; writes.push({ k, bytes: v.length, ttl: o && o.expirationTtl }); },
} });
const { cycle, HANDLER, TAPE_TTL_DAYS } = require('/tmp/w13.cjs');

/* Drive the clock so we can watch an hour roll over without waiting an hour. */
const T0 = Date.parse('2026-08-10T09:05:00Z');
let clock = T0;
const realNow = Date.now, RealDate = Date;
global.Date = class extends RealDate {
  constructor(...a) { return a.length ? new RealDate(...a) : new RealDate(clock); }
  static now() { return clock; }
  static parse(x) { return RealDate.parse(x); }
};

const ok = [], bad = [];
const check = (name, pass, detail) => { (pass ? ok : bad).push(name + (detail ? ` — ${detail}` : '')); };

(async () => {
  const env = mkEnv();
  KV.state = JSON.stringify({ bank: 1000, cash: 1000, runs: 0, equityLog: [], startedAt: T0, positions: [] });

  /* ---- 12 cycles across one hour, then 12 more in the next hour ---- */
  const perCycleBytes = [], ttls = [];
  for (let i = 0; i < 24; i++) {
    writes = [];
    await cycle(env);
    const tw = writes.filter(w => w.k.startsWith('tape:'));
    check(`cycle ${i}: exactly one tape write`, tw.length === 1, `${tw.length}`);
    if (tw.length === 1) { perCycleBytes.push(tw[0].bytes); ttls.push(tw[0].ttl); }
    clock += 5 * 60 * 1000;
  }

  /* 24 cycles at 5 min from 09:05 spans 09:05–11:00 — so three shards: 11 + 12 + 1. */
  const tapeKeys = Object.keys(KV).filter(k => k.startsWith('tape:')).sort();
  check('sharded by hour, not one fat daily key',
    tapeKeys.join(',') === 'tape:2026-08-10:09,tape:2026-08-10:10,tape:2026-08-10:11',
    tapeKeys.join(','));
  const shardCounts = tapeKeys.map(k => JSON.parse(KV[k]).snaps.length);
  check('snapshots land in the right hour', shardCounts.join(',') === '11,12,1', shardCounts.join(','));

  /* 3. FLAT cost. With a daily key, byte 24 would be ~24x byte 1. With hour shards it resets. */
  const first = perCycleBytes[0], peak = Math.max(...perCycleBytes), last = perCycleBytes[perCycleBytes.length - 1];
  check('per-cycle write cost stays flat (no intra-day ramp)', peak < first * 14 && last < first * 14,
    `first ${first}B, peak ${peak}B, last ${last}B`);
  check('a full hour shard stays small enough for a 10ms CPU budget', peak < 60000, `${peak}B peak`);

  /* 4. the saveState bloat bug: the gamma page must not be persisted */
  const st = JSON.parse(KV.state);
  check('state does not carry the gamma page', !st._gammaPage && !JSON.stringify(st).includes('bestAsk'),
    `state is ${KV.state.length}B`);

  /* 5. round-trip precision */
  const sh9 = JSON.parse(KV['tape:2026-08-10:09']);
  const row = sh9.snaps[0].m.find(r => r[0] === PAGE[3].conditionId.slice(2, 12));
  check('millicent round trip', !!row && row[1] === 315 && row[2] === 335 && row[3] === 99589,
    row ? row.join('/') : 'row missing');
  check('40 markets captured per snapshot', sh9.snaps[0].m.length === 40, `${sh9.snaps[0].m.length}`);
  check('every tape write carries the retention TTL',
    ttls.length === 24 && ttls.every(t => t === TAPE_TTL_DAYS * 86400),
    `${new Set(ttls).size} distinct ttl(s): ${[...new Set(ttls)].join(',')} vs expected ${TAPE_TTL_DAYS * 86400}`);

  /* 6. /tape stitching, with hour 10 deliberately left as the only other hour (gaps stay gaps) */
  const idx = JSON.parse(await (await HANDLER.fetch(new Request('https://x/tape'), env)).text());
  check('coverage index counts the day', idx.days['2026-08-10'] === 24, JSON.stringify(idx.days));
  const dayResp = JSON.parse(await (await HANDLER.fetch(new Request('https://x/tape?day=2026-08-10'), env)).text());
  check('day stitch returns every snapshot', dayResp.snaps.length === 24, `${dayResp.snaps.length}`);
  const sorted = dayResp.snaps.every((s2, i) => i === 0 || s2.t >= dayResp.snaps[i - 1].t);
  check('stitched series is time-ordered', sorted);
  const gapResp = JSON.parse(await (await HANDLER.fetch(new Request('https://x/tape?day=2026-08-09'), env)).text());
  check('a day with no shards returns empty, not fabricated zeros', gapResp.snaps.length === 0);
  const hourResp = JSON.parse(await (await HANDLER.fetch(new Request('https://x/tape?day=2026-08-10&hour=10'), env)).text());
  check('single-hour read works', hourResp.snaps.length === 12, `${hourResp.snaps.length}`);
  const badResp = await HANDLER.fetch(new Request('https://x/tape?day=../../state'), env);
  check('malformed day is rejected, not used as a KV key', badResp.status === 400, `${badResp.status}`);

  /* 7. index trimmed to the TTL window */
  const st2 = JSON.parse(KV.state);
  st2.tapeDays = {};
  for (let d = 1; d <= 90; d++) st2.tapeDays['2026-0' + (d < 10 ? '5-0' + d : d < 32 ? '5-' + d : '6-' + String(d - 31).padStart(2, '0'))] = 288;
  KV.state = JSON.stringify(st2);
  await cycle(env);
  const st3 = JSON.parse(KV.state);
  check('coverage index trimmed to the TTL window',
    Object.keys(st3.tapeDays).length <= TAPE_TTL_DAYS, `${Object.keys(st3.tapeDays).length} days, ttl ${TAPE_TTL_DAYS}`);

  /* 2. ZERO extra subrequests — a true A/B. The first draft of this check starved the recorder by
        returning an empty gamma page, but that also short-circuits house mode, so it compared two
        different workers and "proved" nothing. Instead: compile a second module with §5c physically
        removed and run BOTH against the identical mock. Same fetch count = the recorder is free. */
  const cut0 = src.indexOf('/* ---- 5c. POINT-IN-TIME RECORDER');
  const cut1 = src.indexOf('/* ---- 5. equity + housekeeping ---- */');
  check('recorder block located for A/B', cut0 > 0 && cut1 > cut0, `${cut0}..${cut1}`);
  fs.writeFileSync('/tmp/w13-norec.cjs', src.slice(0, cut0) + src.slice(cut1));
  const bare = require('/tmp/w13-norec.cjs');

  const runOnce = async (fn) => {
    KV = {}; writes = [];
    KV.state = JSON.stringify({ bank: 1000, cash: 1000, runs: 0, equityLog: [], startedAt: T0, positions: [] });
    subreqs = 0; await fn(mkEnv());
    return { subreqs, tapeWrites: writes.filter(w => w.k.startsWith('tape:')).length };
  };
  const withRec = await runOnce(cycle);
  const withoutRec = await runOnce(bare.cycle);
  check('recorder adds ZERO subrequests', withRec.subreqs === withoutRec.subreqs,
    `${withRec.subreqs} with vs ${withoutRec.subreqs} without`);
  check('the A/B control really has no recorder', withRec.tapeWrites === 1 && withoutRec.tapeWrites === 0,
    `${withRec.tapeWrites} vs ${withoutRec.tapeWrites}`);
  check('cycle stays far under the 50-subrequest ceiling', withRec.subreqs < 50, `${withRec.subreqs}`);

  /* 8. a KV failure in the recorder must not take down the cycle */
  KV = {}; KV.state = JSON.stringify({ bank: 1000, cash: 1000, runs: 0, equityLog: [], startedAt: T0, positions: [] });
  const brittle = { NTFY_TOPIC: 't', BOT_STATE: {
    get: async k => KV[k] || null,
    put: async (k, v) => { if (k.startsWith('tape:')) throw new Error('KV limit reached'); KV[k] = v; },
  } };
  let survived = true, note = '';
  try { const s = await cycle(brittle); note = (s.lastNotes || []).find(n => n.startsWith('recorder')) || ''; }
  catch (e) { survived = false; note = e.message; }
  check('recorder failure is caught and reported, not fatal', survived && note.startsWith('recorder'), note);

  global.Date = RealDate;
  console.log(ok.map(l => '  ok  ' + l).join('\n'));
  if (bad.length) console.log(bad.map(l => '  FAIL ' + l).join('\n'));
  console.log(`\n${ok.length} passed, ${bad.length} failed`);
  console.log(bad.length ? 'FAIL' : 'PASS — recorder is free at the margin, flat in cost, and cannot lose a day silently');
})();
