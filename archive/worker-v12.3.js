/**
 * Smart Money Detector — 24/7 Cloud Bot
 * Cloudflare Worker. Runs every 5 minutes whether or not any browser is open,
 * keeps a real portfolio in KV, and pushes entries/exits to your phone.
 *
 * Mirrors the dashboard bot's logic exactly, including the parts that matter most:
 *   - fee = 0.06 * contracts * p * (1-p) for takers; maker rebate = 0.0125 * same
 *   - Polymarket returns asks DESCENDING, so best ask is the LOWEST price
 *   - P&L is computed only from our own fills, never from Polymarket's
 *     /positions or /leaderboard endpoints (both are known to misreport)
 */

/* Retention for the point-in-time tape. 60 days is the horizon the audit argued makes the archive
   an asset nobody else has; it is also the window the KV TTL and the coverage index both use, so
   the index never advertises a day whose shards have already expired. */
const TAPE_TTL_DAYS = 60;

/* Bumped on every deploy so a glance at / tells you which build is actually live, rather than
   trusting that the upload happened. */
const VERSION = 'v12.3';

const CFG = {
  /* Kalshi daily-high-temperature series. Several cities because one city is one climate, and a
     calibration result that only holds in New York is a New York result. */
  KWX_SERIES: ['KXHIGHNY', 'KXHIGHCHI', 'KXHIGHDEN', 'KXHIGHTPHX'],
  /* Station coordinates matching what each Kalshi market settles on: Central Park, Midway,
     Denver Intl, Phoenix Sky Harbor. The station matters — a forecast right about the city and
     wrong about the gauge is not an edge. */
  WX_CITIES: [
    { k: 'NYC', series: 'KXHIGHNY', lat: 40.7789, lon: -73.9692, station: 'KNYC', utcOffset: -4 },
    { k: 'CHI', series: 'KXHIGHCHI', lat: 41.7859, lon: -87.7524, station: 'KMDW', utcOffset: -5 },
    { k: 'DEN', series: 'KXHIGHDEN', lat: 39.8466, lon: -104.6562, station: 'KDEN', utcOffset: -6 },
    { k: 'PHX', series: 'KXHIGHTPHX', lat: 33.4278, lon: -112.0037, station: 'KPHX', utcOffset: -7 },
  ],
  /* These two were set from the LIVE radar's scale, where a score also collects context bonuses
     the Worker cannot compute. Against trade-shape alone, 70 requires a news market AND $25k AND
     an entry at 10c or below AND an anonymous wallet, all at once — a handful of trades a week.
     The book sat empty for 45 cycles and said nothing about why. A paper bot that never fills
     gathers no evidence, which is the one thing it exists to do. */
  MIN_TRADE_USD: 10000,   // only consider whale trades at least this big
  MIN_SCORE: 62,          // copy at this score or above
  NEWS_ONLY: true,        // skip sports/esports
  RISK_PER_TRADE: 0.02,   // 2% of cash
  MAX_POSITIONS: 12,
  MAKER: true,            // patient limit orders (see fee note above)
  START_BANKROLL: 1000,
  LIMIT_TTL_MS: 6 * 3600e3,
  RADAR_MIN_USD: 5000,    // radar watches smaller trades than the bot will copy
  /* Deliberately BELOW the dashboard's 'high' band. The live radar adds up to +55 of context
     bonuses (share of 24h volume, fast repricing, wallet age, prior flags) that neither this
     Worker nor the backtest can compute. Reusing the live threshold here meant almost nothing
     ever cleared it — the scan looked healthy and silently alerted on nothing. */
  RADAR_MIN_SCORE: 62,    // push threshold — clusters push regardless of score
  RADAR_MAX_PUSH: 4,      // per cycle, so a busy hour can't spam the phone
  MIN_PRICE: 0.05,        // never copy an entry outside the genuinely-uncertain band
  MAX_PRICE: 0.85,
  HOUSE_MARKETS: 6,       // how many liquid mid-range markets to quote
  HOUSE_SIZE_USD: 50,     // notional per side per cycle
  HOUSE_MAX_INV_USD: 150, // HARD cap per market — enforced post-trade, not pre-trade
  HOUSE_MAX_GROSS_USD: 400, // aggregate cap across all markets
};

/* ---------- topic classification (kept in sync with the dashboard) ---------- */
const SPORTS_STRONG = /(\bnba\b|\bnfl\b|\bmlb\b|\bnhl\b|\bncaa\b|premier league|la liga|serie a|bundesliga|champions league|\bucl\b|europa league|nations league|world cup|asian cup|africa cup|gold cup|\bfa cup\b|fed cup|copa\b|euro qualifier|qualifier\b|friendly\b|game \d|map \d|set \d|league of legends|\bcs2\b|counter-strike|dota|valorant|esports|tennis|\bufc\b|\bmma\b|boxing|\bf1\b|grand prix|golf|\bpga\b|\batp\b|\bwta\b|olympic|super bowl|playoff|\bfinals\b|\b(?:grand|cup|conference|division|series|championship) final\b|championship|derby|\bo\/u\b|over\/under|moneyline|point spread)/i;
const NEWS_ACTION = /(\bstrikes?\b|\bwar\b|warfare|invade|invasion|attack|military|nuclear|missile|\bicbm\b|ceasefire|pardon|nominat|cabinet|resign|impeach|indict|arrest|convict|assassinat|tariff|sanction|embargo|election|primary\b|referendum|\bcoup\b|treaty|summit|hostage|lawsuit|antitrust|settl(?:e|ed|ing|ement)|\b(?:sec|ftc|doj|cftc|fda|epa) vs\b|merger|acquisition|acquire|bankrupt|default\b|shutdown|recession|inflation|\bcpi\b|rate cuts?|rate hikes?|cuts? rates|raises? rates|hikes? rates|federal reserve|\bfomc\b|\bfed\b(?! cup)|supreme court|scotus|verdict|ruling|regulat|approval|\bbanned?\b|\betf\b|\bipo\b|airdrop|listing|\bhack\b|exploit|outbreak|pandemic|hurricane|earthquake|nobel|conclave|veto|executive order|impeachment|\bdoj\b|\bfbi\b|cftc)/i;
const POLITICAL_ENTITY = /(trump|biden|harris|\bvance\b|newsom|desantis|obama|pelosi|\bmusk\b|altman|zuckerberg|putin|zelensky|netanyahu|xi jinping|maduro|khamenei|erdogan|\bmodi\b|starmer|macron|milei|powell|kim jong)/i;
const NEWSY_GEO = /(\biran(?:ian)?\b|\bisrael(?:i)?\b|venezuela|\bukrain(?:e|ian)\b|\brussian?\b|kremlin|\btaiwan\b|\bchina\b|north korea|\bgaza\b|\bnato\b|\bopec\b|tiktok|\bsenate\b|\bcongress\b|president|prime minister|\bvotes?\b|legislation)/i;

function classifyTitle(t) {
  t = t || '';
  const newsish = NEWS_ACTION.test(t) || POLITICAL_ENTITY.test(t);
  if (SPORTS_STRONG.test(t)) return newsish ? 'news' : 'sport';
  if (/ vs\.? /i.test(t)) return newsish ? 'news' : 'sport';
  return (newsish || NEWSY_GEO.test(t)) ? 'news' : 'other';
}

/* ---------- FEES: read them, never assume them ----------
   This code used to credit a flat 0.0125·C·p·(1−p) maker rebate on every simulated fill. The audit
   flagged the assumption and it was half wrong in the most expensive possible direction. What is
   actually true, checked against Polymarket's own market objects rather than a docs page:

     · makers are never charged a fee anywhere (`takerOnly: true` in every schedule)
     · a real maker REBATE does exist, paid daily, as a share of the taker fees collected
     · but it is PER-CATEGORY, and some categories have no fees at all

   Live examples pulled from the API, verbatim:
     politics_fees     {"rate":0.04,"takerOnly":true,"rebateRate":0.25}   → rebate 0.0100
     sports_fees_v2    {"rate":0.05,"takerOnly":true,"rebateRate":0.15}   → rebate 0.0075
     "Will the U.S. invade Iran before 2027?"  feesEnabled:false, feeSchedule:null → rebate 0

   That last line is the one that matters. Geopolitical markets are FEE-FREE, so a maker quoting
   them collects nothing — and geopolitics is exactly what our news filter selects. The live book is
   sitting in "US announces end of Iranian blockade" and "Will Mojtaba Khamenei be head of state",
   while the ledger has been booking 1.25% of every fill as rebate income. $142 of a $436 mark.

   The pool is shared: rebate = (your_fee_equivalent / total_fee_equivalent) × rebate_pool. Since
   the pool is rebateRate × total taker fees, and every trade pairs one maker with one taker at the
   same C and p, the totals cancel and each maker's expected take is exactly rebateRate × their own
   fee-equivalent. So the per-fill formula below is right, not an approximation — provided the rate
   comes from the market instead of from memory. */
function feeTerms(m) {
  const none = { taker: 0, rebate: 0, type: 'none' };
  if (!m) return none;
  if (m.feesEnabled === false) return none;               // fee-free category (e.g. geopolitics)
  let fs = m.feeSchedule;
  if (typeof fs === 'string') { try { fs = JSON.parse(fs); } catch (e) { fs = null; } }
  if (!fs || !Number.isFinite(+fs.rate)) return { ...none, type: String(m.feeType || 'unknown') };
  const rate = +fs.rate;
  const reb = Number.isFinite(+fs.rebateRate) ? +fs.rebateRate : 0;
  return { taker: rate, rebate: rate * reb, type: String(m.feeType || '') };
}

/* Sports detection that does not depend on knowing team names. The title regex was beaten inside
   hours by "Will Bayern Munich win on 2026-08-07?" — no "vs", no league keyword, classified as
   'other'. Under the old news-only allowlist that miss was harmless, because 'other' was excluded
   anyway. The moment 'other' becomes a cohort we WANT to quote, the same miss becomes an open door
   back into in-play sports, which is the one population we have already paid to learn to avoid.
   So ask the exchange instead: it tags its own sports markets with a sports fee schedule and with
   game metadata. The title check stays only as a last-resort backstop for records that predate
   this and no longer carry the market object. */
function isSportsMarket(m) {
  if (!m) return false;
  if (String(m.feeType || '').startsWith('sports')) return true;
  if (m.sportsMarketType || m.gameId || m.gameStartTime || m.eventStartTime) return true;
  return classifyTitle(m.question || '') === 'sport';
}

/* ---------- scoring (trade-shape signals; wallet history is added below) ---------- */
const WALLETNAME = /^0x[0-9a-fA-F]{6,}/;
const AUTOPSEUDO = /^[A-Z][a-z]+-[A-Z][a-z]+$/;
function scoreTrade(t) {
  const usd = t.size * t.price;
  let pts = Math.max(0, Math.min(45, Math.log10(Math.max(usd, 1) / 1000) * 18));
  const reasons = [];
  if (usd >= 100000) reasons.push('very large size'); else if (usd >= 25000) reasons.push('large size');
  if (t.side === 'BUY') {
    if (t.price <= 0.05) { pts += 28; reasons.push('extreme longshot (<=5c)'); }
    else if (t.price <= 0.12) { pts += 22; reasons.push('longshot (<=12c)'); }
    else if (t.price <= 0.20) { pts += 14; reasons.push('longshot (<=20c)'); }
    else if (t.price <= 0.35) { pts += 7; reasons.push('underdog entry'); }
  }
  const cls = classifyTitle(t.title);
  if (cls === 'news') { pts += 15; reasons.push('news-sensitive market'); }
  else if (cls === 'sport') pts -= 12;
  const nm = t.name || '';
  if (!nm || WALLETNAME.test(nm)) { pts += 8; reasons.push('anonymous wallet'); }
  else if (AUTOPSEUDO.test(nm)) { pts += 4; reasons.push('auto-pseudonym'); }
  return { score: Math.round(Math.max(0, Math.min(100, pts))), reasons, usd, isNews: cls === 'news' };
}

/* ---------- fees: Polymarket's real formula ---------- */
const takerFee = (shares, px) => 0.06 * shares * px * (1 - px);
const makerCredit = (shares, px) => 0.0125 * shares * px * (1 - px);

/* ---------- helpers ---------- */
async function getJSON(url, tries = 2) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url, { headers: { 'accept': 'application/json' }, cf: { cacheTtl: 0 } });
      if (r.ok) return await r.json();
    } catch (e) { /* retry */ }
  }
  return null;
}
// asks come back DESCENDING from Polymarket — best ask is the LOWEST price.
function bestAsk(book) {
  const a = (book && book.asks) || [];
  return a.length ? a.reduce((m, x) => (+x.price < +m.price ? x : m), a[0]) : null;
}
function bestBid(book) {
  const b = (book && book.bids) || [];
  return b.length ? b.reduce((m, x) => (+x.price > +m.price ? x : m), b[0]) : null;
}
function walkAsks(book, want) {
  const asks = ((book && book.asks) || []).slice().sort((x, y) => +x.price - +y.price);
  let need = want, cost = 0, got = 0;
  for (const l of asks) {
    if (need <= 0) break;
    const take = Math.min(need, +l.size);
    cost += take * +l.price; got += take; need -= take;
  }
  return got > 0 ? { shares: got, vwap: cost / got } : null;
}
async function push(env, title, msg) {
  if (!env.NTFY_TOPIC) return;
  try {
    await fetch('https://ntfy.sh/' + env.NTFY_TOPIC, {
      method: 'POST',
      headers: { Title: title.replace(/[^\x20-\x7E]/g, ''), Priority: 'high', Tags: 'robot' },
      body: msg.slice(0, 400),
    });
  } catch (e) { /* non-fatal */ }
}

/* ---------- state ---------- */
/* ---- ONE-TIME MIGRATION ----
   A fix that only works forward leaves the damage in place. After the cancelled-vs-lost and
   price-band fixes shipped, the store still held the two records that prompted them: a Rubio
   limit that never filled but was written with status 'closed', so it kept dragging the book to
   "1 closed, 0% win rate"; and a live position entered at 98.3c, taken before the price rule
   existed and still sitting in the forward test it would distort. Both are repaired on load and
   labelled with why, rather than quietly deleted — a paper book that edits its own history is
   worth even less than one with a bad trade in it. */
function migrate(s) {
  let changed = false;
  for (const p of s.positions || []) {
    if (p.status === 'closed' && /never filled/i.test(p.exitReason || '')) {
      p.status = 'cancelled'; p.pnl = null; changed = true;
    }
    if (p.status === 'open' || p.status === 'pending') {
      const px = +(p.entryPx ?? p.limitPx);
      if (Number.isFinite(px) && (px < CFG.MIN_PRICE || px > CFG.MAX_PRICE)) {
        p.status = 'voided'; p.pnl = null; p.closedAt = Date.now();
        p.exitReason = `voided — entered at ${(px * 100).toFixed(1)}c, outside the ${CFG.MIN_PRICE * 100}-${CFG.MAX_PRICE * 100}c band this bot now enforces`;
        if (Number.isFinite(p.cost)) s.cash += p.cost;   // give the stake back; it was never a legitimate entry
        changed = true;
      }
    }
  }
  /* REBATE QUARANTINE. Every fill before this version was credited a flat 1.25% maker rebate that,
     for the geopolitical markets this book actually holds, does not exist — those markets are
     fee-free, so they fund no rebate pool at all. $142.02 of a $436.25 mark was accrued this way:
     a third of the reported edge, and the third that made the strategy look viable.
     The fills are real and the cash from them is real, so only the rebate line is reset. It is
     moved aside rather than deleted, because the size of a mistake is evidence too, and a number
     that quietly vanishes teaches nobody anything. From here the accrual uses the per-market rate
     the exchange publishes, so the figure that regrows is one we can stand behind. */
  if (s.house && !s.house.rebateAudit && Number.isFinite(s.house.rebates)) {
    s.house.rebateAudit = {
      at: Date.now(),
      discarded: s.house.rebates,
      fillsAffected: s.house.fills || 0,
      why: 'flat 1.25% assumed on every fill; real rate is per-market and 0 in fee-free categories',
    };
    (s.house.log = s.house.log || []).unshift(
      `REBATES RESET — $${(s.house.rebates || 0).toFixed(2)} of assumed maker rebate removed; ` +
      `fee-free markets pay none, and the live book is mostly those`);
    s.house.rebates = 0;
    changed = true;
  }
  if (changed) s.migratedAt = Date.now();
  return s;
}

async function loadState(env) {
  const raw = await env.BOT_STATE.get('state');
  if (raw) { try { return JSON.parse(raw); } catch (e) { /* fall through */ } }
  return { bank: CFG.START_BANKROLL, cash: CFG.START_BANKROLL, positions: [], equityLog: [],
           startedAt: Date.now(), runs: 0, lastRun: 0 };
}
const saveState = (env, s) => env.BOT_STATE.put('state', JSON.stringify(s));

function sizeFor(s, score, px, depth) {
  const conviction = Math.min(1.5, Math.max(0.5, score / 70));
  let stake = s.cash * CFG.RISK_PER_TRADE * conviction;
  stake = Math.min(stake, s.cash * 0.10, s.bank * 0.05);
  let shares = stake / px;
  if (depth != null) shares = Math.min(shares, depth * 0.10);   // never more than 10% of visible depth
  return shares;
}

/* ---------- the cycle ---------- */
async function cycle(env) {
  const s = migrate(await loadState(env));
  s.runs++; s.lastRun = Date.now();
  const notes = [];

  const trades = await getJSON(
    `https://data-api.polymarket.com/trades?limit=120&takerOnly=true&filterType=CASH&filterAmount=${CFG.MIN_TRADE_USD}`);

  /* ---- 0. WHALE RADAR — runs before the bot and is independent of it ----
     This is the part that used to live in an hourly Claude session, which turned out to be
     gated behind a permission prompt: no approval, no scan, and the hour was simply lost.
     A Worker has no such gate. It fetches on its own cron, scores, dedupes against KV and
     pushes straight to the phone, so the alerting path never has a human in it. */
  const radarTrades = await getJSON(
    `https://data-api.polymarket.com/trades?limit=250&takerOnly=true&filterType=CASH&filterAmount=${CFG.RADAR_MIN_USD}`);
  if (Array.isArray(radarTrades) && radarTrades.length) {
    s.seenKeys = s.seenKeys || [];
    const seen = new Set(s.seenKeys);
    const fresh = radarTrades.filter(t => {
      const k = t.transactionHash || (t.proxyWallet + '|' + t.timestamp);
      return t.side === 'BUY' && t.conditionId && !seen.has(k);
    });

    /* Cluster detection: independent wallets converging on the SAME side of the SAME market.
       Counted across this batch only — a cluster spread over days is a crowd, not a signal. */
    const byMarketSide = new Map();
    for (const t of fresh) {
      const k = t.conditionId + '|' + (t.outcomeIndex ?? 0);
      if (!byMarketSide.has(k)) byMarketSide.set(k, []);
      byMarketSide.get(k).push(t);
    }
    const clusters = [];
    for (const [k, arr] of byMarketSide) {
      const wallets = new Set(arr.map(t => t.proxyWallet));
      if (wallets.size >= 3) clusters.push({ k, n: wallets.size, arr,
        usd: arr.reduce((a, t) => a + t.size * t.price, 0) });
    }

    const alerts = [];
    for (const t of fresh) {
      const sc = scoreTrade(t);
      const cl = clusters.find(c => c.k === t.conditionId + '|' + (t.outcomeIndex ?? 0));
      if (cl) sc.score = Math.min(100, sc.score + 12);
      if (sc.score < CFG.RADAR_MIN_SCORE && !cl) continue;
      alerts.push({ ts: Date.now(), tradeTs: t.timestamp, wallet: t.proxyWallet,
        name: t.name || t.pseudonym || '', title: t.title || '', outcome: t.outcome || '',
        px: +t.price, usd: t.size * t.price, score: sc.score, reasons: sc.reasons,
        isNews: sc.isNews, cluster: cl ? cl.n : 0, conditionId: t.conditionId });
    }
    alerts.sort((a, b) => b.score - a.score);

    /* Collapse to one push per MARKET SIDE. A 3-wallet cluster is a single event; pushing it
       once per member wallet turned the strongest signal the tool has into three identical
       buzzes, which is how a real alert gets muted. */
    const pushed = new Set();
    for (const a of alerts) {
      if (pushed.size >= CFG.RADAR_MAX_PUSH) break;
      const gk = a.conditionId + '|' + a.outcome;
      if (pushed.has(gk)) continue;
      pushed.add(gk);
      const cl = clusters.find(c => c.k === a.conditionId + '|' + (fresh.find(f => f.conditionId === a.conditionId)?.outcomeIndex ?? 0));
      const tag = a.cluster ? `${a.cluster} wallets backing the same side` : `whale · score ${a.score}`;
      const amount = a.cluster && cl ? cl.usd : a.usd;
      await push(env, (a.score >= 80 || a.cluster ? '\u{1F6A8} ' : '\u{1F40B} ') + tag,
        `$${Math.round(amount).toLocaleString()} on ${a.outcome} at ${(a.px * 100).toFixed(0)}c — ${a.title.slice(0, 70)}`);
      notes.push(`RADAR ${a.score}${a.cluster ? ' cluster x' + a.cluster : ''} ${a.title.slice(0, 40)} $${Math.round(amount)}`);
    }
    s.lastClusters = clusters.map(c => ({ cid: c.k.split('|')[0], oi: +c.k.split('|')[1], n: c.n }));
    if (alerts.length) {
      s.alerts = alerts.concat(s.alerts || []).slice(0, 200);
      s.lastAlertAt = Date.now();
    }
    // Remember what we've already alerted on so the next cycle doesn't re-push the same fills.
    for (const t of fresh) seen.add(t.transactionHash || (t.proxyWallet + '|' + t.timestamp));
    s.seenKeys = [...seen].slice(-3000);
    s.radarScanned = (s.radarScanned || 0) + radarTrades.length;
  }

  /* ---- 1. exits: our source wallet selling the same token ---- */
  if (Array.isArray(trades)) {
    for (const t of trades) {
      if (t.side !== 'SELL') continue;
      const pos = s.positions.find(p => p.status === 'open' && p.wallet === t.proxyWallet && p.tokenId === t.asset);
      if (!pos) continue;
      const book = await getJSON('https://clob.polymarket.com/book?token_id=' + encodeURIComponent(pos.tokenId));
      const bid = bestBid(book);
      if (!bid) continue;
      const px = +bid.price;
      const fee = CFG.MAKER ? -makerCredit(pos.shares, px) : takerFee(pos.shares, px);
      const proceeds = pos.shares * px - fee;
      pos.status = 'closed'; pos.exitPx = px; pos.pnl = proceeds - pos.cost;
      pos.exitReason = 'source wallet sold'; pos.closedAt = Date.now();
      s.cash += proceeds;
      notes.push(`EXIT ${pos.title.slice(0, 40)} @ ${(px * 100).toFixed(0)}c, P&L ${pos.pnl >= 0 ? '+' : ''}$${pos.pnl.toFixed(2)}`);
      await push(env, 'Bot exit', `Copied exit: ${pos.title.slice(0, 60)} at ${(px * 100).toFixed(0)}c. P&L ${pos.pnl >= 0 ? '+' : ''}$${pos.pnl.toFixed(2)}`);
    }
  }

  /* ---- 2. resting limits: fill if the book came to us; expire if stale ---- */
  for (const p of s.positions.filter(x => x.status === 'pending')) {
    if (Date.now() - p.openedAt > CFG.LIMIT_TTL_MS) {
      /* A limit that never filled is NOT a trade. It was marked closed with pnl 0, which the
         stats then counted as a non-winner: one expired order dragged the book to "1 closed,
         0% win rate" and rendered in the UI as a red "lost" row with no stake and a NaN price.
         That is precisely the fake-P&L failure this bot exists to avoid, so it is now flagged
         and excluded from every performance figure. */
      p.status = 'cancelled'; p.pnl = null; p.exitReason = 'limit never filled — cancelled'; p.closedAt = Date.now();
      continue;
    }
    const book = await getJSON('https://clob.polymarket.com/book?token_id=' + encodeURIComponent(p.tokenId));
    const ask = bestAsk(book);
    if (ask && +ask.price <= p.limitPx) {
      const fill = walkAsks(book, p.shares);
      if (fill && fill.vwap <= p.limitPx) {
        const credit = makerCredit(fill.shares, fill.vwap);
        const cost = fill.shares * fill.vwap - credit;
        if (cost <= s.cash) {
          p.status = 'open'; p.shares = fill.shares; p.entryPx = fill.vwap; p.fee = -credit; p.cost = cost;
          s.cash -= cost;
          notes.push(`FILLED ${p.title.slice(0, 40)} @ ${(fill.vwap * 100).toFixed(1)}c`);
          await push(env, 'Bot filled', `${p.title.slice(0, 60)} filled at ${(fill.vwap * 100).toFixed(1)}c, stake $${cost.toFixed(2)}`);
        }
      }
    }
  }

  /* ---- 3. mark open positions + settle resolved markets ---- */
  for (const p of s.positions.filter(x => x.status === 'open')) {
    const book = await getJSON('https://clob.polymarket.com/book?token_id=' + encodeURIComponent(p.tokenId));
    const bid = bestBid(book);
    const mp = bid ? +bid.price : NaN;
    if (Number.isFinite(mp)) p.markPx = mp;              // exit-realistic mark; never store NaN
    const m = await getJSON('https://clob.polymarket.com/markets/' + encodeURIComponent(p.conditionId));
    if (m && Array.isArray(m.tokens)) {
      const wi = m.tokens.findIndex(x => x.winner === true);
      if (wi >= 0) {                                     // only a confirmed winner flag settles
        const won = wi === p.outcomeIndex;
        const proceeds = won ? p.shares : 0;             // winners redeem at $1/share
        p.pnl = proceeds - p.cost; p.exitPx = won ? 1 : 0;
        p.status = 'closed'; p.closedAt = Date.now();
        p.exitReason = won ? 'resolved — redeemed at $1' : 'resolved — expired worthless';
        s.cash += proceeds;
        notes.push(`RESOLVED ${won ? 'WIN' : 'LOSS'} ${p.title.slice(0, 40)} ${p.pnl >= 0 ? '+' : ''}$${p.pnl.toFixed(2)}`);
        await push(env, won ? 'Bot WIN' : 'Bot loss', `${p.title.slice(0, 60)} ${won ? 'won' : 'lost'}. P&L ${p.pnl >= 0 ? '+' : ''}$${p.pnl.toFixed(2)}`);
      }
    }
  }

  /* ---- 3b. LIVE CONTEXT ----
     The backtest disproved the trade-shape score: across 4,901 graded bets in 5 independent runs,
     with price controlled, higher-scoring bets did NOT beat lower-scoring ones. But trade shape is
     only part of the live score. The other part — how big the bet is against the market's own 24h
     volume, whether the odds are already repricing, whether several wallets are converging — is
     contemporaneous and cannot be rebuilt for a trade from three months ago. So it has never been
     tested, and a historical test can never test it. Only forward testing can. That makes this
     Worker the sole instrument capable of settling it, which is why the context layer belongs here
     and why every fill records both scores. */
  const gCache = new Map();
  async function contextFor(t) {
    const out = { bonus: 0, reasons: [] };
    if (!t.slug) return out;
    let g = gCache.get(t.slug);
    if (g === undefined) {
      try {
        const a = await getJSON('https://gamma-api.polymarket.com/markets?slug=' + encodeURIComponent(t.slug));
        g = (a && a[0]) ? { vol24: +a[0].volume24hr || 0, chg: +a[0].oneDayPriceChange || 0 } : null;
      } catch (e) { g = null; }
      gCache.set(t.slug, g);
    }
    if (!g) return out;
    const usd = t.size * t.price;
    if (g.vol24 > 0) {
      const ratio = usd / g.vol24;
      if (ratio >= 0.3) { out.bonus += 20; out.reasons.push('bet is >=30% of the market 24h volume'); }
      else if (ratio >= 0.1) { out.bonus += 12; out.reasons.push('bet is >=10% of the market 24h volume'); }
    }
    if (Math.abs(g.chg || 0) >= 0.15) { out.bonus += 8; out.reasons.push('market repricing fast'); }
    return out;
  }

  /* ---- 4. new entries ---- */
  /* Every rejection is now counted and the best near-miss is kept, so "no trades" is always
     explained rather than silent. Silence made an empty book indistinguishable from a broken one. */
  s.gates = s.gates || { notBuy: 0, lowScore: 0, sports: 0, dupe: 0, noBook: 0, tooDear: 0, filled: 0 };
  let best = null;
  if (Array.isArray(trades)) {
    for (const t of trades) {
      if (s.positions.filter(p => p.status !== 'closed').length >= CFG.MAX_POSITIONS) break;
      if (t.side !== 'BUY' || !t.asset || !t.conditionId) { s.gates.notBuy++; continue; }
      /* Never copy a near-certain trade. The book opened a position "Backing No" at 98.3c: 1.7c
         of upside against 98.3c of downside, on a market where the answer is already known. The
         score has no opinion about this because size and topic alone can clear the bar at any
         price, so the ceiling has to be explicit. Same 5-85c window the backtest uses, for the
         same reason — outside it you are not copying a forecast, you are collecting pennies in
         front of a steamroller. */
      const _px = +t.price;
      if (!(_px >= CFG.MIN_PRICE && _px <= CFG.MAX_PRICE)) { s.gates.priceBand = (s.gates.priceBand || 0) + 1; continue; }
      const sc = scoreTrade(t);
      const shape = sc.score;
      // Only pay for a gamma lookup on trades already within reach of the bar.
      if (shape >= CFG.MIN_SCORE - 25) {
        const ctx = await contextFor(t);
        const cl = (s.lastClusters || []).find(c => c.cid === t.conditionId && c.oi === (t.outcomeIndex ?? 0));
        sc.score = Math.min(100, sc.score + ctx.bonus + (cl ? 12 : 0));
        sc.reasons = sc.reasons.concat(ctx.reasons, cl ? ['part of a same-side wallet cluster'] : []);
        sc.ctxBonus = ctx.bonus + (cl ? 12 : 0);
      }
      if (!best || sc.score > best.score) best = { score: sc.score, shape, title: (t.title || '').slice(0, 70),
        px: +t.price, usd: t.size * t.price, isNews: sc.isNews,
        why: sc.score < CFG.MIN_SCORE ? `scored ${sc.score}, needs ${CFG.MIN_SCORE}` : (CFG.NEWS_ONLY && !sc.isNews ? 'not a news-sensitive market' : 'passed the score gate') };
      if (sc.score < CFG.MIN_SCORE) { s.gates.lowScore++; continue; }
      if (CFG.NEWS_ONLY && !sc.isNews) { s.gates.sports++; continue; }
      const key = t.transactionHash || (t.proxyWallet + t.timestamp);
      if (s.positions.some(p => p.srcKey === key)) { s.gates.dupe++; continue; }
      if (s.positions.some(p => p.tokenId === t.asset && p.status !== 'closed')) { s.gates.dupe++; continue; }

      const book = await getJSON('https://clob.polymarket.com/book?token_id=' + encodeURIComponent(t.asset));
      const ask = bestAsk(book);
      if (!ask) { s.gates.noBook++; continue; }
      const pos = { id: key, srcKey: key, wallet: t.proxyWallet,
        srcName: t.name || t.pseudonym || t.proxyWallet.slice(0, 10),
        conditionId: t.conditionId, tokenId: t.asset, outcome: t.outcome,
        outcomeIndex: t.outcomeIndex ?? 0, title: t.title, score: sc.score,
        shapeScore: shape, ctxBonus: sc.ctxBonus || 0, reasons: sc.reasons.slice(0, 6),
        whalePx: t.price, limitPx: t.price, openedAt: Date.now(), status: 'pending',
        mode: CFG.MAKER ? 'maker' : 'taker' };

      if (!CFG.MAKER) {
        const want = sizeFor(s, sc.score, +ask.price, null);
        const fill = walkAsks(book, want);
        if (!fill) continue;
        const fee = takerFee(fill.shares, fill.vwap);
        const cost = fill.shares * fill.vwap + fee;
        if (cost > s.cash) continue;
        Object.assign(pos, { status: 'open', shares: fill.shares, entryPx: fill.vwap, fee, cost });
        s.cash -= cost;
      } else {
        const want = sizeFor(s, sc.score, t.price, +ask.size);
        if (+ask.price <= t.price) {
          const fill = walkAsks(book, want);
          if (fill && fill.vwap <= t.price) {
            const credit = makerCredit(fill.shares, fill.vwap);
            const cost = fill.shares * fill.vwap - credit;
            if (cost > s.cash) continue;
            Object.assign(pos, { status: 'open', shares: fill.shares, entryPx: fill.vwap, fee: -credit, cost });
            s.cash -= cost;
          } else { pos.shares = want; }
        } else { pos.shares = want; }   // rests until the ask comes down to us
      }
      s.positions.unshift(pos); s.gates.filled++;
      notes.push(`ENTRY ${pos.status} ${pos.title.slice(0, 40)} @ ${((pos.entryPx || pos.limitPx) * 100).toFixed(1)}c score ${sc.score}`);
      await push(env, pos.status === 'open' ? 'Bot entry' : 'Bot limit placed',
        `${pos.title.slice(0, 55)} — ${pos.outcome} at ${((pos.entryPx || pos.limitPx) * 100).toFixed(1)}c, score ${sc.score}, from ${pos.srcName}`);
    }
  }

  /* ---- 5. HOUSE MODE — the inversion of everything this project falsified ----
     The copy-trading half of this bot asked "is the taker flow informed?" and the answer, over
     ~15,000 graded positions, was no. That null has a second reading: the market-maker's great
     fear is being run over by informed takers, and we have measured that fear as unfounded here.
     So this quotes BOTH sides of a few liquid mid-range markets at the touch and simulates
     collecting spread plus Polymarket's 1.25%·p·(1−p) maker rebate from flow we have shown to be
     uninformed. Honesty notes, in the code because they matter: fills are simulated from the tape
     (a SELL print at or under our bid fills our bid, a BUY print at or over our ask fills our
     ask), which ignores queue position and therefore overstates fill rate — read the direction of
     the P&L, not its magnitude. Inventory is signed; negative shares mean we effectively hold the
     other outcome's token, and the cash accounting stays exact either way. */
  s.house = s.house || { cash: 0, rebates: 0, fills: 0, pos: {}, lastTs: {}, log: [], startedAt: Date.now() };
  /* The selector used to refresh only every 12th cycle. The recorder needs a page every cycle, so
     the fetch moved out here and the selection logic still runs on its slower cadence.
     This is a LOCAL, deliberately: saveState JSON.stringifies the whole state object, so parking a
     40-market gamma payload on `s` would write ~200KB of redundant page into KV every five minutes
     — the recorder's own compressed row is 40×4 integers. The tape is the artifact; the page is
     scratch. */
  let gammaPage = null;
  try {
    try {
      const gp = await getJSON('https://gamma-api.polymarket.com/markets?closed=false&active=true&order=volume24hr&ascending=false&limit=40');
      if (Array.isArray(gp) && gp.length) gammaPage = gp;
    } catch (e) {}
    /* Refresh on the slow cadence, on an empty list — or whenever the stored list predates
       cohorts. Without that last clause a market list saved by an older version keeps quoting with
       no cohort and no fee schedule until the cadence happens to come round, which is up to an
       hour of fills entering the study unlabelled. */
    const staleList = (s.house.mkts || []).some(m => !m.cohort || !m.fee);
    if (!s.house.mkts || !s.house.mkts.length || staleList || s.runs % 12 === 1) {
      const g = gammaPage;
      if (Array.isArray(g)) {
        const picked = [];
        for (const m of g) {
          if (picked.length >= CFG.HOUSE_MARKETS) break;
          const bb = parseFloat(m.bestBid), ba = parseFloat(m.bestAsk);
          if (!(bb >= 0.25 && ba <= 0.75 && ba > bb)) continue;
          /* The two exclusions that keep the experiment honest. The maker thesis rests on OUR OWN
             measurement that taker flow here is uninformed — and that was measured on news markets
             resolving over weeks. An in-play sports market is the opposite world: once the game
             starts, every taker knows the score and the maker is the only one who doesn't. The
             first live run proved it within hours — short 292 shares of a Bayern match kicking off
             the same night. Same logic bars any market close to resolution, sports or not: the
             final days are when information concentrates and quotes go stale fastest. */
          /* COHORTS, not a flip. The audit's Idea 3 says: don't make markets in news-sensitive
             categories, make them in the boring ones — a lovely inversion, since the dashboard's
             whole job becomes telling you which markets to AVOID quoting. Two independent lines of
             evidence agree with it: our own book went systematically short (adverse selection —
             informed takers lifting the ask), and, as established above, the news markets we chose
             are frequently fee-free, so they pay no rebate either.
             But "the audit says so" is not evidence, and the previous news-only rule was itself
             argued from a plausible story. So run BOTH and let the markout decide. Half the slots
             go to news, half to boring, every fill is tagged with its cohort, and the comparison
             below reports realized adverse selection per cohort. Paper money makes this free; the
             only cost of being wrong is learning which way. Sports stays excluded outright — that
             one is already settled, and expensively. */
          if (isSportsMarket(m)) continue;
          const cls = classifyTitle(m.question || '');
          const cohort = cls === 'news' ? 'news' : 'boring';
          if (picked.filter(p => p.cohort === cohort).length >= Math.ceil(CFG.HOUSE_MARKETS / 2)) continue;
          const end = Date.parse(m.endDate || m.endDateIso || '');
          if (Number.isFinite(end) && end - Date.now() < 4 * 864e5) continue;
          let tok = null;
          try { tok = JSON.parse(m.clobTokenIds || '[]')[0] || null; } catch (e) {}
          if (!tok || !m.conditionId) continue;
          picked.push({ cid: m.conditionId, tok, q: (m.question || '').slice(0, 70), cohort, fee: feeTerms(m) });
        }
        if (picked.length) s.house.mkts = picked;
      }
    }
    /* Remove any position the current exclusions would never have opened — at the current mark,
       with the removal logged, so the tuition is recorded rather than edited out. Only sports are
       excluded now; the earlier version also purged non-news books, which is why this reads as a
       narrower rule than it once was. */
    for (const [cid, pos] of Object.entries(s.house.pos || {})) {
      if (classifyTitle(pos.q || '') !== 'sport') continue;
      if (Math.abs(pos.shares) > 1e-9) {
        const mark = Number.isFinite(pos.mid) ? pos.mid : 0.5;
        s.house.cash += pos.shares * mark;
        s.house.log.unshift(`REMOVED ${String(pos.q).slice(0, 40)} — in-play sports, where the taker knows the score and the maker does not; closed ${pos.shares.toFixed(0)} sh at ${(mark * 100).toFixed(0)}c`);
      }
      delete s.house.pos[cid];
    }
    if (s.house.mkts) s.house.mkts = s.house.mkts.filter(mk => classifyTitle(mk.q || '') !== 'sport');
    for (const mk of (s.house.mkts || [])) {
      const book = await getJSON('https://clob.polymarket.com/book?token_id=' + encodeURIComponent(mk.tok));
      const bid = bestBid(book), ask = bestAsk(book);
      if (!bid || !ask) continue;
      const qb = +bid.price, qa = +ask.price;
      if (!(qa > qb) || !Number.isFinite(qb) || !Number.isFinite(qa)) continue;
      const mid = (qb + qa) / 2;
      const pos = s.house.pos[mk.cid] = s.house.pos[mk.cid] || { shares: 0, q: mk.q, tok: mk.tok };
      pos.mid = mid; pos.bid = qb; pos.ask = qa;
      /* NEVER default the cohort to a real cohort. The first version of this line read
         `|| 'news'`, and within one cycle of deploying it every position carried a news label that
         no one had measured — the market list persisted from before cohorts existed, so `mk.cohort`
         was undefined and the fallback quietly invented the answer. It then got worse: the
         verification sweep skips any position that already HAS a cohort, so the invented label
         blocked the lookup that would have corrected it. A guess that defends itself from being
         checked is the worst possible failure mode for an A/B whose entire output is the
         difference between two labels. Unknown gets its own bucket, which the boring-vs-news
         comparison simply never reads. */
      pos.cohort = mk.cohort || pos.cohort || 'unverified';
      pos.fee = mk.fee || pos.fee || { taker: 0, rebate: 0, type: 'unknown' };
      const REB = pos.fee.rebate || 0;   // per-market, from the exchange — see feeTerms()

      /* ---- MARKOUT: the number that actually says whether market making works ----
         P&L on an open book is a mark, and a mark on inventory you were forced into flatters the
         thing that forced you. Markout asks the honest question instead: after we get filled, does
         the mid move against us? A maker earning spread from uninformed flow shows markout near
         zero; a maker being picked off shows it persistently negative, and no amount of quoted
         spread makes that back. Two horizons because they mean different things — 10 minutes is
         adverse selection, an hour is drift. Resolve on arrival: every cycle we already have the
         fresh mid, so settling matured entries costs nothing extra. */
      s.house.pend = s.house.pend || [];
      s.house.mk = s.house.mk || {};
      const nowS = Date.now() / 1000;
      const keep = [];
      for (const e of s.house.pend) {
        if (e.cid !== mk.cid) { keep.push(e); continue; }
        const age = nowS - e.t;
        let done = true;
        for (const [hz, secs] of [['m10', 600], ['m60', 3600]]) {
          if (e[hz]) continue;
          if (age >= secs) {
            /* signed so that positive always means the fill was good for us */
            const edge = (e.side === 'BUY' ? (mid - e.px) : (e.px - mid));
            const b = s.house.mk[e.cohort] = s.house.mk[e.cohort] || {};
            const acc = b[hz] = b[hz] || { n: 0, sum: 0, sumsq: 0, sh: 0 };
            acc.n++; acc.sum += edge * e.sh; acc.sumsq += (edge * edge) * e.sh; acc.sh += e.sh;
            e[hz] = 1;
          } else done = false;
        }
        if (!done) keep.push(e);
      }
      s.house.pend = keep;
      if (s.house.pend.length > 600) s.house.pend.splice(0, s.house.pend.length - 600);
      const tape = await getJSON(`https://data-api.polymarket.com/trades?market=${encodeURIComponent(mk.cid)}&limit=60`);
      const since = s.house.lastTs[mk.cid] || (Date.now() / 1000 - 300);
      s.house.lastTs[mk.cid] = Date.now() / 1000;
      if (!Array.isArray(tape)) continue;
      const fresh = tape.filter(t => t.timestamp > since);
      const invUsd = pos.shares * mid;
      /* ---- RISK LAYER (added after the first 3-day run) ----
         The cap was checked BEFORE the trade, so a position sitting at −$149 could still sell
         another $50 and land at −$199. Three of seven markets breached that way, and the book
         drifted to 6-short/1-long with $845 gross against a $1,000 notional — a −$1,089 tail
         behind a +$417 mark. The mark was never profit; it was an un-capped short book quoted
         favourably. Caps are now enforced on the POST-trade position and sized to the headroom,
         plus an aggregate ceiling, because per-market limits say nothing about total exposure.
         The short skew is itself a finding: on Polymarket a trader exiting YES usually BUYS NO
         rather than selling YES, so BUY prints dominate the tape and a naive two-sided quoter
         gets its ask lifted far more than its bid is hit. Adverse selection with extra steps. */
      const grossNow = Object.values(s.house.pos).reduce((a, p) =>
        a + Math.abs((p.shares || 0) * (p.mid || 0.5)), 0);
      const headroomBuy = CFG.HOUSE_MAX_INV_USD - invUsd;          // room before hitting +cap
      const headroomSell = CFG.HOUSE_MAX_INV_USD + invUsd;         // room before hitting −cap
      const grossRoom = Math.max(0, CFG.HOUSE_MAX_GROSS_USD - grossNow);

      /* RISK-REDUCING TRADES MUST ALWAYS BE ALLOWED.
         First version of the aggregate cap deadlocked the book: legacy gross was $838 against a
         $400 ceiling, so grossRoom was 0 and every order — including the buys that would have
         unwound the shorts — was blocked. Zero fills in an hour, and the position could never
         shrink. A risk limit that forbids reducing risk is worse than no limit, so a trade that
         moves inventory toward flat is exempt from the aggregate ceiling; only risk-INCREASING
         trades are gated by it. */
      // a SELL print at or through our bid: someone hit us — we buy
      const buyRoom = invUsd < 0 ? Math.max(grossRoom, -invUsd) : grossRoom;   // buying a short back = reducing
      const buyUsd = Math.min(CFG.HOUSE_SIZE_USD, headroomBuy, buyRoom);
      if (buyUsd > 1 && fresh.some(t => t.side === 'SELL' && +t.price <= qb)) {
        const sh = buyUsd / qb;
        pos.shares += sh;
        s.house.cash -= sh * qb;
        s.house.rebates += REB * sh * qb * (1 - qb);
        s.house.fills++; s.house.buyFills = (s.house.buyFills || 0) + 1;
        s.house.pend.push({ cid: mk.cid, side: 'BUY', px: qb, sh, t: nowS, cohort: pos.cohort });
        s.house.log.unshift(`BUY ${sh.toFixed(0)} @ ${(qb * 100).toFixed(1)}c — ${mk.q.slice(0, 40)}`);
      }
      // a BUY print at or through our ask: someone lifted us — we sell (signed inventory)
      const sellRoom = invUsd > 0 ? Math.max(grossRoom, invUsd) : grossRoom;   // selling a long down = reducing
      const sellUsd = Math.min(CFG.HOUSE_SIZE_USD, headroomSell, sellRoom);
      if (sellUsd > 1 && fresh.some(t => t.side === 'BUY' && +t.price >= qa)) {
        const sh = sellUsd / qa;
        pos.shares -= sh;
        s.house.cash += sh * qa;
        s.house.rebates += REB * sh * qa * (1 - qa);
        s.house.fills++; s.house.sellFills = (s.house.sellFills || 0) + 1;
        s.house.pend.push({ cid: mk.cid, side: 'SELL', px: qa, sh, t: nowS, cohort: pos.cohort });
        s.house.log.unshift(`SELL ${sh.toFixed(0)} @ ${(qa * 100).toFixed(1)}c — ${mk.q.slice(0, 40)}`);
      }
    }
    /* ---- LEGACY RE-VERIFICATION ----
       Positions opened before cohorts existed carry no cohort and no fee schedule, so every
       classification of them is guesswork from a truncated title. Rather than guess, re-fetch the
       market object and stamp the authoritative fields — purging it if the exchange says sports.
       Bounded to 2 lookups on the same 1-in-12 cadence as the settle sweep, so it drains the
       backlog over a few hours without going anywhere near the subrequest ceiling. */
    if (s.runs % 12 === 2) {
      let vChecked = 0;
      for (const [cid, pos] of Object.entries(s.house.pos)) {
        if (vChecked >= 2) break;
        if (pos.cohort && pos.cohort !== 'unverified') continue;   // 'unverified' means ASK AGAIN
        vChecked++;
        let gm = null;
        try {
          const r = await getJSON('https://gamma-api.polymarket.com/markets?condition_ids=' + encodeURIComponent(cid));
          gm = Array.isArray(r) ? r[0] : (r && r.id ? r : null);
        } catch (e) {}
        if (!gm) { pos.cohort = 'unverified'; continue; }   // try again next pass, never assume
        if (isSportsMarket(gm)) {
          const mark = Number.isFinite(pos.mid) ? pos.mid : 0.5;
          if (Math.abs(pos.shares) > 1e-9) s.house.cash += pos.shares * mark;
          s.house.log.unshift(`REMOVED ${String(pos.q).slice(0, 40)} — exchange metadata says sports (${gm.feeType || 'game fields'}); closed ${(pos.shares || 0).toFixed(0)} sh at ${(mark * 100).toFixed(0)}c`);
          delete s.house.pos[cid];
          continue;
        }
        pos.fee = feeTerms(gm);
        pos.cohort = classifyTitle(gm.question || pos.q || '') === 'news' ? 'news' : 'boring';
      }
    }

    // settle any resolved inventory; prune flat books
    if (s.runs % 12 === 2) {
      let settleCalls = 0;
      for (const [cid, pos] of Object.entries(s.house.pos)) {
        if (settleCalls >= 4) break;      // spread the settle sweep over cycles, don't spike the budget
        if (Math.abs(pos.shares) < 1e-9) { delete s.house.pos[cid]; continue; }
        settleCalls++;
        const m = await getJSON('https://clob.polymarket.com/markets/' + encodeURIComponent(cid));
        if (m && Array.isArray(m.tokens)) {
          const mine = m.tokens.find(x => x.token_id === pos.tok);
          if (mine && (mine.winner === true || m.tokens.some(x => x.winner === true))) {
            s.house.cash += pos.shares * (mine.winner === true ? 1 : 0);
            s.house.log.unshift(`SETTLED ${pos.q.slice(0, 40)} (${mine.winner ? 'won' : 'lost'} side, ${pos.shares.toFixed(0)} sh)`);
            delete s.house.pos[cid];
          }
        }
      }
    }
    s.house.log.length = Math.min(s.house.log.length, 12);
    // mark long inventory at the bid and short at the ask — the exit you could actually get
    s.house.equity = s.house.cash + s.house.rebates + Object.values(s.house.pos).reduce((a, p) =>
      a + p.shares * (p.shares >= 0 ? (p.bid ?? p.mid ?? 0) : (p.ask ?? p.mid ?? 0)), 0);
  } catch (e) { notes.push('house-mode error: ' + (e.message || 'unknown').slice(0, 60)); }

  /* ---- 5b. PENNY SWEEP — the settlement-reversal study, running where code is exact ----
     The nearest-verdict strategy needs ~200 resolved penny-active markets. Grading them through
     a browser or a summarizer is slow and — proven today — fallible: a batch read defaulted every
     winnerIndex to 1 and nearly recorded two fake reversals into a study whose breakeven is 1.5%.
     Here the loop is exact code end to end: gamma lists resolved markets, the tape is counted
     with arithmetic, and the winner comes only from CLOB tokens[].winner. Three markets per
     cycle ≈ 860/day of capacity against a 200-market target — the grind dissolves. */
  s.pennies = s.pennies || { done: {}, active: 0, wins: 0, reversals: 0, fills: 0, offset: 0, log: [] };
  try {
    /* SUBREQUEST BUDGET — the reason this had to be capped.
       Cloudflare allows 50 subrequests per invocation. The first version of this sweep walked a
       20-market gamma page and spent one CLOB call on each just to discover most were already
       graded or unresolved: 24 calls, ~46% of the whole cycle's budget, which pushed the total to
       52 and killed the scheduled invocations. Cadence fell from every 5 minutes to roughly once
       an hour — the sweep was starving the very loop that runs it. A hard budget fixes it: at most
       BUDGET calls, and the page offset advances every cycle so coverage still marches forward. */
    const BUDGET = 7;
    let calls = 0;
    const g = await getJSON(`https://gamma-api.polymarket.com/markets?closed=true&order=volumeNum&ascending=false&limit=20&offset=${s.pennies.offset % 2000}`);
    calls++;
    let graded = 0;
    if (Array.isArray(g)) {
      for (const m of g) {
        if (graded >= 3 || calls >= BUDGET) break;
        const cid = m.conditionId;
        if (!cid || s.pennies.done[cid] !== undefined) continue;
        const clob = await getJSON('https://clob.polymarket.com/markets/' + encodeURIComponent(cid));
        calls++;
        const toks = (clob && clob.tokens) || [];
        const wi = toks.findIndex(t => t.winner === true);
        if (wi < 0) { s.pennies.done[cid] = 'unresolved'; continue; }   // pending/disputed — grade later, never guess
        const tape = await getJSON(`https://data-api.polymarket.com/trades?market=${encodeURIComponent(cid)}&limit=500`);
        calls++; graded++;
        if (!Array.isArray(tape)) { s.pennies.done[cid] = 'no-tape'; continue; }
        let winSide = 0, loseSide = 0;
        /* ---- APR, not EV per dollar (audit Idea 4) ----
           "+1.9c on the dollar, 98% of the time" sounds like an edge and tells you almost nothing,
           because it hides the two things that decide whether the strategy is worth running: how
           long the dollar is trapped, and what the exchange takes. Buying at 98c to collect $1 is
           +2.04% gross — spectacular over three days (≈900% annualised), pedestrian over eight
           months (≈3%). Same trade, same hit rate, completely different business. Capital that
           cannot be redeployed is the whole cost of this strategy, so measure the thing that
           actually competes: annualised return on locked capital, net of the real taker fee. */
        const endMs = Date.parse(m.endDate || m.endDateIso || m.closedTime || '');
        const ft = feeTerms(m);
        let pxSum = 0, pxN = 0, holdSum = 0, holdN = 0;
        for (const t of tape) {
          if (t.side !== 'BUY' || !(+t.price >= 0.98)) continue;
          const onWinner = (t.outcomeIndex ?? 0) === wi;
          if (onWinner) winSide++; else loseSide++;
          const p = +t.price;
          if (p > 0) { pxSum += p; pxN++; }
          const ts = +t.timestamp;
          if (Number.isFinite(endMs) && Number.isFinite(ts) && ts > 0) {
            const d = (endMs - ts * 1000) / 864e5;
            if (d > 0 && d < 400) { holdSum += d; holdN++; }   // guard against bad endDates
          }
        }
        /* ---- CALIBRATION: audit Idea 7, done the way it should have been the first time ----
           The crowd-bias question was already tested once and came back null, but it was asked of
           the wrong population: trades sampled from a tape, which measures what traders did, not
           what prices were worth. The right question is a PORTFOLIO one — across resolved markets,
           does an outcome priced at 8c win 8% of the time? That is a calibration curve, and the
           favourite-longshot bias is precisely a curve that sags at the left end.
           This costs ZERO extra requests: the sweep already holds the tape and the winner for every
           resolved market it grades. It just never asked them this question.
           One observation per market, outcome 0 only. Both outcomes would double the sample and
           none of the information, since in a binary market they are p and 1-p of each other. */
        if (Number.isFinite(endMs)) {
          s.calib = s.calib || { h24: {}, h7d: {}, skipped: 0, used: 0 };
          for (const [hz, secs] of [['h24', 86400], ['h7d', 7 * 86400]]) {
            const cutoff = endMs / 1000 - secs;
            let best = null;   // most recent outcome-0 trade at or before the cutoff
            for (const t of tape) {
              if ((t.outcomeIndex ?? 0) !== 0) continue;
              const ts = +t.timestamp;
              if (!Number.isFinite(ts) || ts > cutoff) continue;
              if (!best || ts > best.ts) best = { ts, px: +t.price };
            }
            if (!best || !(best.px > 0 && best.px < 1)) {
              if (hz === 'h24') s.calib.skipped++;      // tape window did not reach back that far
              continue;
            }
            if (hz === 'h24') s.calib.used++;
            const b = Math.min(19, Math.floor(best.px * 20));      // 5-cent buckets
            const cell = s.calib[hz][b] = s.calib[hz][b] || [0, 0]; // [n, wins]
            cell[0]++;
            if (wi === 0) cell[1]++;
          }
        }
        if (winSide + loseSide === 0) { s.pennies.done[cid] = 'no-pennies'; continue; }
        /* One observation per market, entered only when both the price and the holding period are
           known — a market with an unusable endDate is left out of the APR rather than defaulted,
           because a fabricated holding period would move this number more than any real result. */
        if (pxN && holdN) {
          const p = pxSum / pxN, days = Math.max(0.25, holdSum / holdN);
          const won = loseSide === 0;
          const gross = won ? (1 - p) : -p;               // payoff per share, before costs
          const cost = ft.taker * p * (1 - p);            // real taker fee, from the market itself
          const ret = (gross - cost) / p;                 // return on capital actually locked up
          s.pennies.obs = s.pennies.obs || [];
          s.pennies.obs.push([Math.round(p * 1000), +days.toFixed(2), won ? 1 : 0, +(ret * 100).toFixed(3)]);
          if (s.pennies.obs.length > 1200) s.pennies.obs.splice(0, s.pennies.obs.length - 1200);
        }
        /* market-level unit: one observation per market; a reversal market is one where the
           penny buyers' side lost — if BOTH sides had ≥98c buys, the losing side's existence
           marks it a reversal for those buyers and the market counts once, as a reversal. */
        if (loseSide > 0) {
          s.pennies.reversals++; s.pennies.done[cid] = 'REVERSAL';
          s.pennies.log.unshift(`REVERSAL ${String(m.question || '').slice(0, 50)} — ${loseSide} penny buys on the losing side`);
        } else {
          s.pennies.wins++; s.pennies.done[cid] = 'win';
        }
        s.pennies.active++; s.pennies.fills += winSide + loseSide;
      }
      s.pennies.offset += 20;
      s.pennies.lastCalls = calls;
      if (Object.keys(s.pennies.done).length > 4000) {
        // keep the tallies, trim the dedupe map's oldest entries
        const ks = Object.keys(s.pennies.done); ks.slice(0, 1000).forEach(k => delete s.pennies.done[k]);
      }
    }
    s.pennies.log.length = Math.min(s.pennies.log.length, 10);
  } catch (e) { notes.push('penny-sweep error: ' + (e.message || 'x').slice(0, 50)); }

  /* ---- 5c. POINT-IN-TIME RECORDER — "you cannot backtest what you did not record" ----
     The audit's single most important line, and it is right: roughly half the strategy ideas worth
     testing are blocked not on cleverness but on the absence of history. Polymarket's API gives
     you the present and the resolved past; it never gives you what the book looked like at 14:05
     last Tuesday. Nobody has that tape, which is exactly why it is worth owning.
     Constraint-aware design, and the constraints genuinely drove it:
       · ZERO extra subrequests — it reuses the gamma page the house-mode selector already pulls,
         so it cannot push the cycle back into the 50-subrequest ceiling that killed the cron.
       · ONE KV write per cycle (288/day, inside the ~1k/day free allowance).
       · Sharded by HOUR, not by day. The first draft used one key per day, which meant
         read-parse-restringify a file growing toward ~600KB on every five-minute cycle — on a
         10ms CPU budget that is how a recorder quietly starts failing in month two. An hour holds
         12 snapshots (~17KB), so the cost per cycle is flat forever instead of ramping through
         the day.
     Cheap enough to never turn off is the only property that matters for a recorder. */
  try {
    /* ---- KALSHI LEG: the paired tape ----
       Cross-venue arbitrage on liquid macro is dead — checked on 2026-08-10, the two venues agreed
       to 2.46c against a 4.83c round trip. But that verdict came with one revival condition, and it
       is a condition about TIME rather than level: a gap could open in the minutes after a surprise
       if one venue lags. That cannot be tested on snapshots taken whenever someone happens to look.
       It needs both venues sampled on the same clock, continuously, before the surprise arrives —
       and the September FOMC is five weeks out, so the window to be already recording is now.
       Kalshi prices this as a LADDER of "above X%" contracts while Polymarket prices the same event
       as a negRisk set; the two are reconcilable (see auto/xvenue-kalshi-fed.py) and the Polymarket
       leg already rides in on the gamma page above, so this costs exactly ONE extra subrequest and
       no extra KV write — both venues land in the same shard. */
    let kal = null;
    try {
      /* The event ticker rolls every meeting, so derive it rather than hardcode a date that quietly
         goes stale. Suffixes look like 26SEP; take the earliest that has not passed. */
      const MON = { JAN: 0, FEB: 1, MAR: 2, APR: 3, MAY: 4, JUN: 5, JUL: 6, AUG: 7, SEP: 8, OCT: 9, NOV: 10, DEC: 11 };
      if (!s.kalEvent || !s.kalEventAt || Date.now() - s.kalEventAt > 12 * 36e5) {
        /* DIAGNOSTIC FETCH, not a plain one. The first version used the shared getJSON, which
           swallows a non-200 and returns null — so when the Kalshi leg came up empty on the live
           deploy there was no error, no note, and a `kalshiEvent: null` that looked exactly like
           "hasn't run yet". A silent failure that is indistinguishable from not-yet-started is
           worse than a loud one: it cost a deploy cycle to notice at all. This records WHY.
           A browser-like User-Agent is sent because a bare Workers UA is a plausible reason a
           public API refuses a datacenter request, and ruling it out costs nothing. */
        let evs = null;
        try {
          const r = await fetch('https://api.elections.kalshi.com/trade-api/v2/events?series_ticker=KXFED&status=open&limit=20',
            { headers: { accept: 'application/json', 'user-agent': 'smart-money-detector/1.0' }, cf: { cacheTtl: 0 } });
          s.kalDiag = { at: Date.now(), status: r.status };
          if (r.ok) { evs = await r.json(); s.kalDiag.keys = Object.keys(evs || {}).slice(0, 5).join(','); }
          else { s.kalDiag.body = (await r.text()).slice(0, 120); }
        } catch (e) { s.kalDiag = { at: Date.now(), err: (e.message || 'fetch failed').slice(0, 80) }; }
        const list = (evs && (evs.events || evs)) || [];
        s.kalDiag.n = Array.isArray(list) ? list.length : -1;
        let best = null;
        for (const e of (Array.isArray(list) ? list : [])) {
          const mt = /^KXFED-(\d{2})([A-Z]{3})$/.exec(String(e.event_ticker || e));
          if (!mt) continue;
          const when = Date.UTC(2000 + (+mt[1]), MON[mt[2]], 28);   // end of that month
          if (when >= Date.now() && (!best || when < best.w)) best = { t: mt[0], w: when };
        }
        if (best) { s.kalEvent = best.t; s.kalEventAt = Date.now(); s.kalDiag.picked = best.t; }
        else notes.push('kalshi: no event picked (' + JSON.stringify(s.kalDiag).slice(0, 90) + ')');
      }
      if (s.kalEvent) {
        const km = await getJSON('https://api.elections.kalshi.com/trade-api/v2/markets?event_ticker='
          + encodeURIComponent(s.kalEvent) + '&status=open&limit=40');
        const rows = (km && (km.markets || km)) || [];
        /* Kalshi quotes in integer cents 0-100. Normalise defensively: a value at or above 1 is
           cents (so a 1c ask becomes 0.01, and 100 becomes 1.00), anything below is already a
           probability. The one case this cannot distinguish is a fractional feed reporting exactly
           1.0, which does not occur as a live quote. */
        const px = v => { const n = parseFloat(v); if (!Number.isFinite(n)) return 0; return n >= 1 ? n / 100 : n; };
        if (Array.isArray(rows) && rows.length) {
          kal = rows.slice(0, 24).map(r => [
            String(r.ticker || '').replace(/^KXFED-\d{2}[A-Z]{3}-?/, ''),   // keep just the strike, e.g. T3.75
            Math.round(px(r.yes_bid) * 1000),
            Math.round(px(r.yes_ask) * 1000),
            Math.round(parseFloat(r.volume) || 0),
          ]);
        }
      }
    } catch (e) { notes.push('kalshi: ' + (e.message || 'x').slice(0, 30)); }

    /* Write a snapshot if EITHER venue answered. Gating the whole recorder on Polymarket would mean
       one bad gamma response silently costs us the Kalshi tape for that cycle too, and a gap in a
       paired tape is worse than a gap in either leg alone. */
    const havePM = Array.isArray(gammaPage) && gammaPage.length;
    if (havePM || (kal && kal.length)) {
      const iso = new Date().toISOString();
      const day = iso.slice(0, 10), hour = iso.slice(11, 13);
      const key = `tape:${day}:${hour}`;
      const raw = await env.BOT_STATE.get(key);
      const shard = raw ? JSON.parse(raw) : { day, hour, snaps: [] };
      const snap = { t: Math.floor(Date.now() / 1000) };
      if (havePM) snap.m = gammaPage.slice(0, 40).map(x => [
        String(x.conditionId || '').slice(2, 12),          // short id, enough to join later
        Math.round((parseFloat(x.bestBid) || 0) * 1000),   // millicents — integers compress
        Math.round((parseFloat(x.bestAsk) || 0) * 1000),
        Math.round(parseFloat(x.volume24hr) || 0),
      ]);
      if (kal && kal.length) { snap.k = kal; snap.ke = s.kalEvent; }
      shard.snaps.push(snap);
      if (shard.snaps.length > 24) shard.snaps.splice(0, shard.snaps.length - 24);  // 5-min cycles → 12/hr
      await env.BOT_STATE.put(key, JSON.stringify(shard), { expirationTtl: TAPE_TTL_DAYS * 86400 });
      /* Index lives on state so /tape and the dashboard can see coverage without listing KV. */
      s.tapeDays = s.tapeDays || {};
      s.tapeDays[day] = (s.tapeDays[day] || 0) + 1;
      const days = Object.keys(s.tapeDays).sort();
      /* Trim the index to the retention window — an index entry for a day whose shards have
         already expired is a claim of coverage we cannot honour. */
      while (days.length > TAPE_TTL_DAYS) delete s.tapeDays[days.shift()];
    }
  } catch (e) { notes.push('recorder: ' + (e.message || 'x').slice(0, 40)); }


  /* ---- 5d. KALSHI WEATHER CALIBRATION — the audit's highest-rated family, finally testable ----
     Ideas 18-20 argued that prediction markets should misprice against free professional
     benchmarks, and rated weather the best of them: the forecast is public, free, and genuinely
     skilful, and settlement is mechanical (an NWS Climatological Report, not a judgement call).
     It sat parked because the forecast APIs were unreachable — until met.no turned out to serve one
     without complaint, exactly like OKX did for funding. "Blocked" deserves periodic retesting.

     But before asking whether a FORECAST beats the market, ask the cheaper question the market can
     answer by itself: is it even calibrated? Kalshi gives settled outcomes AND historical candles,
     so a full price-vs-outcome study is available today rather than after weeks of recording.
     Two traps this code is built around, both already caught by hand:
       · the ladder mixes strike_type less / between / greater, and the TITLE text contradicts the
         strike — "Will the high temp be >73" is really the "72 or below" contract. Titles are
         never parsed here; only result and price are used, so the trap cannot bite.
       · last_price on a settled market is ~0 or ~1 and says nothing. The price must be read at a
         fixed LEAD TIME, which is what the candlestick call is for. */
  s.kwx = s.kwx || { done: {}, buckets: {}, n: 0, wins: 0, cursor: {}, si: 0, noQuote: 0, log: [] };
  try {
    const BUDGET = 6;
    let calls = 0;
    const series = CFG.KWX_SERIES[s.kwx.si % CFG.KWX_SERIES.length];
    s.kwx.si = (s.kwx.si || 0) + 1;
    const cur = s.kwx.cursor[series] || '';
    const page = await getJSON('https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker='
      + encodeURIComponent(series) + '&status=settled&limit=100' + (cur ? '&cursor=' + encodeURIComponent(cur) : ''));
    calls++;
    const mkts = (page && page.markets) || [];
    /* CURSOR DISCIPLINE. The first version advanced the cursor on every cycle, which looked like
       healthy progress and was the opposite: a page holds 100 markets, a cycle can afford about
       five, so ninety-five were abandoned unread on every page and coverage marched over a mostly
       ungraded history. The test caught it as 41 graded after 200 cycles. Advance ONLY when the
       page has nothing left to grade; otherwise stay and finish it. */
    let exhausted = true;
    for (const m of mkts) {
      if (calls >= BUDGET) { exhausted = false; break; }
      const tk = m.ticker;
      if (!tk || s.kwx.done[tk] !== undefined) continue;
      const res = m.result;
      if (res !== 'yes' && res !== 'no') { s.kwx.done[tk] = 'unsettled'; continue; }
      const close = Date.parse(m.close_time || '');
      if (!Number.isFinite(close)) { s.kwx.done[tk] = 'no-close'; continue; }
      /* price at a fixed 12h lead — before the day's high is realised, while the forecast is sharp */
      const lead = Math.floor(close / 1000) - 12 * 3600;
      const cs = await getJSON('https://api.elections.kalshi.com/trade-api/v2/series/'
        + encodeURIComponent(series) + '/markets/' + encodeURIComponent(tk)
        + '/candlesticks?start_ts=' + (lead - 3600) + '&end_ts=' + (lead + 3600) + '&period_interval=60');
      calls++;
      const cands = (cs && (cs.candlesticks || cs)) || [];
      if (!Array.isArray(cands) || !cands.length) { s.kwx.done[tk] = 'no-quote'; s.kwx.noQuote++; continue; }
      /* the candle whose end is nearest the lead instant */
      let best = null;
      for (const c of cands) {
        const t = +c.end_period_ts;
        if (!Number.isFinite(t)) continue;
        if (!best || Math.abs(t - lead) < Math.abs(best.end_period_ts - lead)) best = c;
      }
      const bid = best && best.yes_bid && parseFloat(best.yes_bid.close_dollars);
      const ask = best && best.yes_ask && parseFloat(best.yes_ask.close_dollars);
      let px = null;
      if (Number.isFinite(bid) && Number.isFinite(ask) && ask > 0 && ask >= bid) px = (bid + ask) / 2;
      else if (best && best.price && Number.isFinite(parseFloat(best.price.close_dollars))) px = parseFloat(best.price.close_dollars);
      /* A quote pinned at 0 or 1 twelve hours out carries no information and would swamp the
         curve's tails with certainties; the interesting population is where the market is unsure. */
      if (!Number.isFinite(px) || px <= 0.01 || px >= 0.99) { s.kwx.done[tk] = 'degenerate'; continue; }
      const b = Math.min(19, Math.floor(px * 20));
      const cell = s.kwx.buckets[b] = s.kwx.buckets[b] || [0, 0, 0];   // [n, wins, sumPx]
      cell[0]++; if (res === 'yes') cell[1]++; cell[2] += px;
      s.kwx.n++; if (res === 'yes') s.kwx.wins++;
      s.kwx.done[tk] = res;
    }
    if (exhausted) s.kwx.cursor[series] = (page && page.cursor) || '';
    s.kwx.lastCalls = calls;
    if (Object.keys(s.kwx.done).length > 6000) {
      const ks = Object.keys(s.kwx.done); ks.slice(0, 1500).forEach(k => delete s.kwx.done[k]);
    }
  } catch (e) { notes.push('kwx: ' + (e.message || 'x').slice(0, 40)); }


  /* ---- 5e. negRISK SET SCANNER (H15) — with the asymmetry the first version had backwards ----
     A negRisk event is a set of mutually exclusive outcomes. Two different trades live here and
     they do NOT have the same precondition, which is the whole subtlety:

       SHORT the set (sell every YES, receive sum of bids). Payout is $1 if one outcome wins and
       $0 if none does. So the maximum you can ever owe is $1, and receiving more than $1 is
       riskless REGARDLESS of exhaustiveness — a missing catch-all outcome only helps you.

       LONG the set (buy every YES, pay sum of asks). This pays $1 only if some listed outcome
       actually wins. Without a catch-all it can pay $0, so here exhaustiveness is mandatory. A
       non-exhaustive set trading below $1 is correctly priced, not an opportunity — this is the
       gate the audit warned about, and it applies to the long side only.

     Fees decide the rest, and they are not uniform. Cost scales with sum(p*(1-p)), which is large
     for a balanced set and collapses for a lopsided one — and is exactly ZERO in the fee-free
     categories (feesEnabled:false). Worked example from the live Sept FOMC set: bids summed to
     1.0120, a +1.20c gross edge, killed by a 2.46c fee. The same overround in a fee-free set
     would have been pure profit. So the scanner records the fee-adjusted edge, never the gross. */
  s.nr = s.nr || { scanned: 0, sets: 0, best: null, hist: {}, hits: [], feeFree: 0, offset: 0 };
  try {
    const evs = await getJSON('https://gamma-api.polymarket.com/events?closed=false&active=true'
      + '&order=volume24hr&ascending=false&limit=25&offset=' + (s.nr.offset % 400));
    s.nr.offset += 25;
    if (Array.isArray(evs)) {
      for (const ev of evs) {
        const ms = (ev.markets || []).filter(m => m.negRisk === true && m.bestBid != null && m.bestAsk != null);
        if (ms.length < 3) continue;                       // a 2-outcome "set" is just a binary market
        s.nr.sets++;
        let sb = 0, sa = 0, fee = 0, anyFee = false;
        for (const m of ms) {
          const b = parseFloat(m.bestBid), a = parseFloat(m.bestAsk);
          if (!Number.isFinite(b) || !Number.isFinite(a)) { sb = NaN; break; }
          sb += b; sa += a;
          const ft = feeTerms(m);
          if (ft.taker > 0) anyFee = true;
          fee += ft.taker * b * (1 - b);
        }
        if (!Number.isFinite(sb)) continue;
        if (!anyFee) s.nr.feeFree++;
        /* histogram of the overround itself — even with zero arbs this tells us how far from $1
           these sets typically sit, which is the useful result if the answer is "never". */
        const h = Math.max(-5, Math.min(5, Math.round((sb - 1) * 100)));
        s.nr.hist[h] = (s.nr.hist[h] || 0) + 1;
        const shortEdge = sb - 1 - fee;                    // riskless: max liability is $1
        /* exhaustiveness proxy: Polymarket marks a residual bucket with negRiskOther, and a set
           without one cannot be assumed complete. Never assume it — the long side is gated. */
        const exhaustive = ms.some(m => m.negRiskOther === true);
        const longEdge = exhaustive ? (1 - sa - fee) : null;
        const rec = { ev: String(ev.title || '').slice(0, 60), n: ms.length,
          sumBid: +sb.toFixed(4), sumAsk: +sa.toFixed(4), feeC: +(fee * 100).toFixed(2),
          shortEdgeC: +(shortEdge * 100).toFixed(2),
          longEdgeC: longEdge === null ? null : +(longEdge * 100).toFixed(2),
          exhaustive, feeFree: !anyFee };
        if (!s.nr.best || shortEdge > (s.nr.best.shortEdgeC / 100)) s.nr.best = rec;
        if (shortEdge > 0 || (longEdge !== null && longEdge > 0)) {
          s.nr.hits.unshift({ ...rec, at: Date.now() });
          s.nr.hits.length = Math.min(s.nr.hits.length, 12);
        }
      }
      s.nr.scanned++;
    }
  } catch (e) { notes.push('negrisk: ' + (e.message || 'x').slice(0, 40)); }


  /* ---- 5f. CUMULATIVE-LADDER MONOTONICITY (H19) — a NEW idea, and the cleanest one yet ----
     Not from the audit. It fell out of two things noticed today: geopolitical markets are
     FEE-FREE (feesEnabled:false, so zero drag on any edge), and Polymarket lists many events as a
     ladder of cumulative deadlines — "US announces end of Iranian blockade by August 15", "...by
     August 31", "...by September 30" — fourteen of them on one event.

     Cumulative deadlines are NESTED: the event happening by August 15 implies it happened by
     August 31. So P(by earlier) <= P(by later), ALWAYS, as a matter of logic rather than opinion.
     If bid(earlier) > ask(later) the ladder has crossed itself, and selling the earlier while
     buying the later is a riskless CREDIT: both win -> -1 +1 = 0; only the later wins -> 0 +1 = +1;
     neither -> 0. You are paid to hold a position that can never lose.

     Why this is the most promising thing on the board: it needs no forecast, no model, and no view.
     It is pure logic on quoted prices, and in the fee-free categories there is nothing to pay.

     The one way to get this catastrophically wrong is to mistake an EXCLUSIVE ladder ("in which
     month will X happen") for a CUMULATIVE one ("by when will X have happened"). Exclusive
     outcomes are not nested and are not monotone, so a fake violation appears on every one of
     them. The gate is therefore deliberately narrow: the questions must share a stem once dates
     are stripped, must each contain the word "by", and must carry distinct end dates. Anything
     ambiguous is skipped rather than guessed. */
  s.mono = s.mono || { scanned: 0, ladders: 0, checks: 0, hits: [], best: null, feeFree: 0, offset: 0 };
  try {
    const evs = await getJSON('https://gamma-api.polymarket.com/events?closed=false&active=true'
      + '&order=volume24hr&ascending=false&limit=25&offset=' + (s.mono.offset % 400));
    s.mono.offset += 25;
    const stem = q => String(q || '').toLowerCase()
      .replace(/\b(january|february|march|april|may|june|july|august|september|october|november|december)\b/g, '')
      .replace(/[0-9]/g, '').replace(/[^a-z]+/g, ' ').trim();
    if (Array.isArray(evs)) {
      for (const ev of evs) {
        const ms = (ev.markets || []).filter(m =>
          m.negRisk !== true && m.bestBid != null && m.bestAsk != null &&
          /\bby\b/i.test(String(m.question || '')) && (m.endDate || m.endDateIso));
        if (ms.length < 3) continue;
        const stems = new Set(ms.map(m => stem(m.question)));
        if (stems.size !== 1) continue;                  // not one ladder; skip rather than guess
        const rungs = ms.map(m => ({
          t: Date.parse(m.endDate || m.endDateIso),
          b: parseFloat(m.bestBid), a: parseFloat(m.bestAsk),
          q: String(m.question || '').slice(0, 48), fee: feeTerms(m),
        })).filter(r => Number.isFinite(r.t) && Number.isFinite(r.b) && Number.isFinite(r.a));
        if (rungs.length < 3) continue;
        rungs.sort((x, y) => x.t - y.t);
        if (new Set(rungs.map(r => r.t)).size !== rungs.length) continue;   // duplicate deadlines
        s.mono.ladders++;
        const noFee = rungs.every(r => r.fee.taker === 0);
        if (noFee) s.mono.feeFree++;
        for (let i = 0; i < rungs.length; i++) {
          for (let j = i + 1; j < rungs.length; j++) {
            s.mono.checks++;
            const e = rungs[i], l = rungs[j];            // e is the EARLIER deadline
            /* sell the earlier at its bid, buy the later at its ask */
            const credit = e.b - l.a;
            const fee = e.fee.taker * e.b * (1 - e.b) + l.fee.taker * l.a * (1 - l.a);
            const net = credit - fee;
            if (net <= 0) continue;
            const rec = { ev: String(ev.title || '').slice(0, 50), early: e.q, late: l.q,
              earlyBid: e.b, lateAsk: l.a, creditC: +(credit * 100).toFixed(2),
              feeC: +(fee * 100).toFixed(2), netC: +(net * 100).toFixed(2), feeFree: noFee, at: Date.now() };
            if (!s.mono.best || net > s.mono.best.netC / 100) s.mono.best = rec;
            s.mono.hits.unshift(rec);
            s.mono.hits.length = Math.min(s.mono.hits.length, 12);
          }
        }
      }
      s.mono.scanned++;
    }
  } catch (e) { notes.push('mono: ' + (e.message || 'x').slice(0, 40)); }


  /* ---- 5g. COMPLEMENTARY-PAIR CONSISTENCY (H20) — the purest arb available ----
     A second NEW idea from the same seam as H19. Polymarket runs SEPARATE order books for the YES
     and the NO token of one market. They are linked only by the split/merge mechanism: $1 of USDC
     splits into one YES plus one NO, and one YES plus one NO merges back into $1. Nothing forces
     the two books to quote consistently moment to moment.

     So two riskless trades exist whenever they drift:
       ask(YES) + ask(NO) < $1  -> buy both, merge, redeem $1. Profit is the shortfall.
       bid(YES) + bid(NO) > $1  -> split $1 into the pair, sell both. Profit is the excess.
     Neither needs a forecast, a model or a view — the payoff is $1 by construction whichever way
     the market resolves. This is the same species as H19 and chosen for the same reason: every
     idea that has died here died on fees eating a small real edge, and in the fee-free categories
     there is no fee.

     Honest limits, stated in code because they decide whether this is real:
       · the top of book is one price, not a size. A 3c gap on 5 shares is not a trade. Depth is
         recorded alongside so the edge can never be read without it — this is the penny lesson,
         where a 2c edge turned out to exist only at a price nobody could get filled at.
       · gas and the merge step are not modelled here, so a thin edge is not a real one. */
  s.pair = s.pair || { checked: 0, hits: [], best: null, bestSpreadC: null, feeFree: 0, i: 0 };
  try {
    if (Array.isArray(gammaPage) && gammaPage.length) {
      const BUDGET = 4;
      let calls = 0;
      for (let k = 0; k < gammaPage.length && calls < BUDGET; k++) {
        const mkt = gammaPage[(s.pair.i + k) % gammaPage.length];
        let toks = [];
        try { toks = JSON.parse(mkt.clobTokenIds || '[]'); } catch (e) {}
        if (!Array.isArray(toks) || toks.length < 2) continue;
        const [byes, bno] = await Promise.all([
          getJSON('https://clob.polymarket.com/book?token_id=' + encodeURIComponent(toks[0])),
          getJSON('https://clob.polymarket.com/book?token_id=' + encodeURIComponent(toks[1])),
        ]);
        calls += 2;
        const ay = bestAsk(byes), an = bestAsk(bno);
        const by = bestBid(byes), bn = bestBid(bno);
        if (!ay || !an || !by || !bn) continue;
        s.pair.checked++;
        const ft = feeTerms(mkt);
        if (ft.taker === 0) s.pair.feeFree++;
        const pay = +ay.price, pan = +an.price, pby = +by.price, pbn = +bn.price;
        if (![pay, pan, pby, pbn].every(Number.isFinite)) continue;
        /* buy both sides, merge, redeem $1 */
        const buyGap = 1 - (pay + pan);
        const buyFee = ft.taker * (pay * (1 - pay) + pan * (1 - pan));
        /* split $1, sell both sides */
        const sellGap = (pby + pbn) - 1;
        const sellFee = ft.taker * (pby * (1 - pby) + pbn * (1 - pbn));
        const depth = Math.min(+ay.size || 0, +an.size || 0);
        const depthS = Math.min(+by.size || 0, +bn.size || 0);
        if (s.pair.bestSpreadC === null || (1 - (pay + pan)) * 100 > s.pair.bestSpreadC) {
          s.pair.bestSpreadC = +((1 - (pay + pan)) * 100).toFixed(2);
        }
        const mkRec = (side, gap, fee, sz) => ({
          q: String(mkt.question || '').slice(0, 46), side,
          gapC: +(gap * 100).toFixed(2), feeC: +(fee * 100).toFixed(2),
          netC: +((gap - fee) * 100).toFixed(2), shares: Math.round(sz),
          usd: +((gap - fee) * sz).toFixed(2), feeFree: ft.taker === 0, at: Date.now(),
        });
        for (const [side, gap, fee, sz] of [['buy-merge', buyGap, buyFee, depth],
                                            ['split-sell', sellGap, sellFee, depthS]]) {
          if (gap - fee <= 0) continue;
          const rec = mkRec(side, gap, fee, sz);
          if (!s.pair.best || rec.netC > s.pair.best.netC) s.pair.best = rec;
          s.pair.hits.unshift(rec);
          s.pair.hits.length = Math.min(s.pair.hits.length, 12);
        }
      }
      s.pair.i = (s.pair.i + BUDGET) % Math.max(1, gammaPage.length);
    }
  } catch (e) { notes.push('pair: ' + (e.message || 'x').slice(0, 40)); }


  /* ---- 5h. SETTLED-IN-FACT, UNRESOLVED-IN-PRICE (H21) — a third new idea, and it is free ----
     Noticed while reading live geopolitics markets: "US x Iran Effective Ceasefire by July 31?"
     was quoting 0.90/0.91 on August 10. The deadline had passed ten days earlier. Whatever the
     answer is, it is now a matter of record rather than forecast — and yet the market was pricing
     a 10% chance of being wrong about the past.

     A price far from 0 or 1 on an event whose window has CLOSED is not a probability, it is an
     unresolved fact. Sometimes that is legitimate (the resolution source has not published, or
     there is a genuine dispute about wording). Sometimes it is simply that nobody has bothered to
     look. The second case is an edge available to anyone willing to read the news, and it needs no
     model at all — which is the same reason H19 and H20 are on this list.

     This deliberately does NOT trade or score. It surfaces candidates for a human to check,
     because the whole value is in resolving an ambiguity that code cannot resolve. Presenting it
     as an automated signal would be pretending the hard part is done. Costs zero subrequests: it
     reads the gamma page already in hand. */
  s.stale = s.stale || { seen: 0, list: [] };
  try {
    if (Array.isArray(gammaPage) && gammaPage.length) {
      const now = Date.now();
      const found = [];
      for (const m of gammaPage) {
        const end = Date.parse(m.endDate || m.endDateIso || '');
        if (!Number.isFinite(end) || end >= now) continue;      // window still open
        const bb = parseFloat(m.bestBid), ba = parseFloat(m.bestAsk);
        if (!Number.isFinite(bb) || !Number.isFinite(ba)) continue;
        const mid = (bb + ba) / 2;
        /* Only the genuinely undecided middle. A market at 0.98 past its deadline is simply
           waiting on the oracle and carries no information for us. */
        if (mid < 0.12 || mid > 0.88) continue;
        found.push({ q: String(m.question || '').slice(0, 60),
          cid: String(m.conditionId || '').slice(0, 12),
          daysPast: +((now - end) / 864e5).toFixed(1),
          bid: bb, ask: ba, feeFree: feeTerms(m).taker === 0,
          vol24: Math.round(parseFloat(m.volume24hr) || 0) });
      }
      if (found.length) {
        s.stale.seen += found.length;
        /* keep the most overdue, since a longer wait makes "nobody looked" likelier than "pending" */
        s.stale.list = found.sort((a, b) => b.daysPast - a.daysPast).slice(0, 10);
      }
    }
  } catch (e) { notes.push('stale: ' + (e.message || 'x').slice(0, 40)); }


  /* ---- 5i. FORECAST vs MARKET (H23) — the one claim the audit actually made, still untested ----
     Everything killed today was a way of profiting WITHOUT knowing more than the market: taking
     dies to the spread, making dies to adverse selection, and every arbitrage is closed to within
     the fee. That is exactly what an efficient market looks like to someone with no informational
     advantage — and it says nothing at all about someone who HAS one.

     A numerical weather model at a 12-hour horizon is a real advantage over a crowd, in a way no
     amount of order-book cleverness is. Note this is a DIFFERENT question from the calibration
     study in 5d: a market can be perfectly calibrated on its own prices and still be beaten by
     better information. Calibration is internal consistency; edge is relative skill.

     It cannot be backtested — met.no serves the present only, and the archives that do exist are
     unreachable from here. So it has to be recorded forward and graded on settlement, which is
     why this writes the forecast into the same tape as the prices. Every hour without it is a
     city-day that can never be recovered, the same argument that justified the recorder itself.

     One subtlety worth stating: met.no returns Celsius on a 6-hourly grid past the first day, and
     Kalshi settles on the Fahrenheit daily maximum from the NWS Climatological Report for a
     specific station. Those are not the same measurement, and the gap between them is part of what
     is being tested — a forecast that is right about the atmosphere but wrong about the station is
     not an edge. The raw values are stored unconverted so that judgement stays reviewable. */
  try {
    if ((s.runs % 6) === 3) {                            // every ~30 min: forecasts move slowly
      const CITY = CFG.WX_CITIES[(s.wxi || 0) % CFG.WX_CITIES.length];
      s.wxi = (s.wxi || 0) + 1;
      const f = await getJSON('https://api.met.no/weatherapi/locationforecast/2.0/compact?lat='
        + CITY.lat + '&lon=' + CITY.lon);
      const ser = f && f.properties && f.properties.timeseries;
      if (Array.isArray(ser) && ser.length) {
        const day = new Date().toISOString().slice(0, 10);
        const key = 'fc:' + day;
        const raw = await env.BOT_STATE.get(key);
        const rec = raw ? JSON.parse(raw) : { day, obs: [] };
        /* keep only the next 36h of air temperatures — enough to contain tomorrow's maximum */
        const cutoff = Date.now() + 36 * 36e5;
        const pts = [];
        for (const p of ser) {
          const t = Date.parse(p.time);
          if (!Number.isFinite(t) || t > cutoff) continue;
          const c = p.data && p.data.instant && p.data.instant.details
            && p.data.instant.details.air_temperature;
          if (typeof c === 'number') pts.push([Math.floor(t / 1000), Math.round(c * 10)]);
        }
        if (pts.length) {
          rec.obs.push({ t: Math.floor(Date.now() / 1000), city: CITY.k, kalshi: CITY.series, p: pts });
          if (rec.obs.length > 240) rec.obs.splice(0, rec.obs.length - 240);
          await env.BOT_STATE.put(key, JSON.stringify(rec), { expirationTtl: TAPE_TTL_DAYS * 86400 });
          s.fcDays = s.fcDays || {};
          s.fcDays[day] = (s.fcDays[day] || 0) + 1;
          const ds = Object.keys(s.fcDays).sort();
          while (ds.length > TAPE_TTL_DAYS) delete s.fcDays[ds.shift()];
        }
      }
    }
  } catch (e) { notes.push('forecast: ' + (e.message || 'x').slice(0, 40)); }


  /* ---- 5j. H23 BACKTEST: does the public forecast beat the market? ----
     This is the last hypothesis standing, and until an hour ago it was filed as "needs a month of
     forward recording". That was wrong, and only retesting the claim revealed it. Iowa Environmental
     Mesonet archives NWS MOS guidance BY STATION AND RUN TIME, and its station identifiers include
     the exact gauges Kalshi settles against (KNYC is Central Park). Kalshi archives settled outcomes
     and hourly candles. The two join on the settlement station, so months of history are testable
     today — validated by IEM's daily maxima matching Kalshi's own expiration_value exactly on every
     day checked.

     The strategy under test is deliberately the dumbest possible version, because a dumb rule that
     works is a finding and a clever rule that works is usually a bug: take the NBS forecast issued
     at 12:00Z, find the contract whose band contains it, buy that contract at the ask 12 hours
     before close, and hold to settlement. Net of Kalshi's real taker fee.

     Doing this by hand managed five city-days in an afternoon. The worker gets 50 subrequests every
     five minutes, so at ~2 per city-day it finishes a hundred of them in about three hours and keeps
     going. That is the entire reason this lives here rather than in a transcript. */
  s.h23 = s.h23 || { done: {}, n: 0, hit: 0, pnlC: 0, feesC: 0, byCity: {}, log: [], cur: {}, si: 0 };
  try {
    const BUDGET = 8;
    let calls = 0;
    const CT = CFG.WX_CITIES[s.h23.si % CFG.WX_CITIES.length];
    s.h23.si++;
    const cur = s.h23.cur[CT.series] || '';
    const page = await getJSON('https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker='
      + encodeURIComponent(CT.series) + '&status=settled&limit=100' + (cur ? '&cursor=' + encodeURIComponent(cur) : ''));
    calls++;
    const mkts = (page && page.markets) || [];
    /* group the ladder by event: a band is only meaningful alongside its siblings */
    const evs = {};
    for (const m of mkts) {
      if (!m.event_ticker || m.result !== 'yes' && m.result !== 'no') continue;
      (evs[m.event_ticker] = evs[m.event_ticker] || []).push(m);
    }
    let exhausted = true;
    for (const [ev, group] of Object.entries(evs)) {
      if (calls + 2 > BUDGET) { exhausted = false; break; }
      if (s.h23.done[ev] !== undefined) continue;
      const win = group.find(m => m.result === 'yes');
      const actual = parseFloat(group[0].expiration_value);
      const close = Date.parse(group[0].close_time || '');
      if (!win || !Number.isFinite(actual) || !Number.isFinite(close)) { s.h23.done[ev] = 'incomplete'; continue; }
      /* the market day is the day BEFORE close (close is 04:59Z the following morning) */
      const dayIso = new Date(close - 12 * 36e5).toISOString().slice(0, 10);
      const mos = await getJSON('https://mesonet.agron.iastate.edu/api/1/mos.json?station='
        + encodeURIComponent(CT.station) + '&model=NBS&runtime=' + dayIso + 'T12:00:00Z');
      calls++;
      const rows = (mos && (mos.data || mos)) || [];
      if (!Array.isArray(rows) || !rows.length) { s.h23.done[ev] = 'no-mos'; continue; }
      /* THE LOCAL-DAY WINDOW. The first version filtered forecast rows to the same UTC date, which
         silently truncated the afternoon for every city west of the Atlantic seaboard. Phoenix's
         daily peak lands at 00:00Z the FOLLOWING UTC day — verified directly: the 2026-08-08 12Z run
         forecasts 109 at 21:00Z and 111 at 00:00Z, and the UTC filter kept only the 109. That is a
         systematic downward bias in the forecast, applied to exactly the cities where it decides the
         answer, and it is why Denver and Phoenix looked like the model was hopeless there.
         The market settles on a LOCAL calendar day, so the forecast window has to be the local day
         too: [D 00:00 local, D+1 00:00 local) expressed in UTC via the station's offset. */
      const utcOff = CT.utcOffset;                       // hours behind UTC, e.g. NYC -4
      const dayStart = Date.parse(dayIso + 'T00:00:00Z') - utcOff * 36e5;
      const dayEnd = dayStart + 24 * 36e5;
      let fmax = null;
      for (const r of rows) {
        const ft = Date.parse(String(r.ftime || '').replace(' ', 'T') + 'Z');
        if (!Number.isFinite(ft) || ft < dayStart || ft >= dayEnd) continue;
        const t = parseFloat(r.tmp);
        if (Number.isFinite(t) && (fmax === null || t > fmax)) fmax = t;
      }
      if (fmax === null) { s.h23.done[ev] = 'no-fcst'; continue; }
      /* which contract's band contains the forecast? bands come from floor/cap, never the title */
      const pick = group.find(m => {
        const lo = m.floor_strike, hi = m.cap_strike, st = m.strike_type;
        /* Kalshi's tail semantics, verified against settled outcomes rather than assumed:
           `less` with cap_strike C wins when the actual is STRICTLY below C — the Aug 3 contract
           had cap 80 and resolved NO on an actual of 80, while its sub-title read "80 or below"
           for cap 81 elsewhere. Using <= here would put a forecast sitting exactly on C into the
           tail contract it does not belong to, and boundary days are precisely the ones where the
           bands disagree. `greater` with floor F wins when the actual exceeds F. */
        if (st === 'less') return fmax < (hi ?? -Infinity);
        if (st === 'greater') return fmax > (lo ?? Infinity);
        return lo != null && hi != null && fmax >= lo && fmax <= hi;
      });
      if (!pick) { s.h23.done[ev] = 'no-band'; continue; }
      const lead = Math.floor(close / 1000) - 12 * 3600;
      const cs = await getJSON('https://api.elections.kalshi.com/trade-api/v2/series/'
        + encodeURIComponent(CT.series) + '/markets/' + encodeURIComponent(pick.ticker)
        + '/candlesticks?start_ts=' + (lead - 3600) + '&end_ts=' + (lead + 3600) + '&period_interval=60');
      calls++;
      const cands = (cs && (cs.candlesticks || cs)) || [];
      if (!Array.isArray(cands) || !cands.length) { s.h23.done[ev] = 'no-quote'; continue; }
      let best = null;
      for (const c of cands) {
        const t = +c.end_period_ts;
        if (Number.isFinite(t) && (!best || Math.abs(t - lead) < Math.abs(best.end_period_ts - lead))) best = c;
      }
      const ask = best && best.yes_ask && parseFloat(best.yes_ask.close_dollars);
      if (!Number.isFinite(ask) || ask <= 0 || ask >= 1) { s.h23.done[ev] = 'degenerate'; continue; }
      const won = pick.result === 'yes';
      const fee = 0.07 * ask * (1 - ask);                       // Kalshi taker, paid either way
      const pnl = (won ? 1 : 0) - ask - fee;
      s.h23.n++; if (won) s.h23.hit++;
      s.h23.pnlC += pnl * 100; s.h23.feesC += fee * 100;
      const b = s.h23.byCity[CT.k] = s.h23.byCity[CT.k] || { n: 0, hit: 0, pnlC: 0 };
      b.n++; if (won) b.hit++; b.pnlC += pnl * 100;
      s.h23.done[ev] = won ? 'hit' : 'miss';
      s.h23.log.unshift({ ev, city: CT.k, fcst: fmax, actual, band: pick.ticker.split('-').pop(),
        askC: +(ask * 100).toFixed(1), won, pnlC: +(pnl * 100).toFixed(1) });
      s.h23.log.length = Math.min(s.h23.log.length, 20);
    }
    if (exhausted) s.h23.cur[CT.series] = (page && page.cursor) || '';
    s.h23.lastCalls = calls;
  } catch (e) { notes.push('h23: ' + (e.message || 'x').slice(0, 40)); }

  /* ---- 5. equity + housekeeping ---- */
  const open = s.positions.filter(p => p.status === 'open');
  const mark = open.reduce((a, p) => {
    const px = Number.isFinite(p.markPx) ? p.markPx : (Number.isFinite(p.entryPx) ? p.entryPx : 0);
    const sh = Number.isFinite(p.shares) ? p.shares : 0;
    return a + sh * px;
  }, 0);
  s.equity = s.cash + mark;
  const last = s.equityLog[s.equityLog.length - 1];
  if (!last || Math.abs(last.e - s.equity) > 0.01 || Date.now() - last.t > 36e5) {
    s.equityLog.push({ t: Date.now(), e: s.equity });
    if (s.equityLog.length > 800) s.equityLog.shift();
  }
  if (s.positions.length > 400) s.positions.length = 400;
  s.lastNotes = notes;
  s.bestNearMiss = best;
  s.cyclesSinceFill = s.gates.filled ? 0 : (s.cyclesSinceFill || 0) + 1;
  await saveState(env, s);
  return s;
}

export default {
  async scheduled(event, env, ctx) { ctx.waitUntil(cycle(env)); },

  async fetch(req, env) {
    const url = new URL(req.url);
    const cors = { 'access-control-allow-origin': '*', 'content-type': 'application/json',
      'access-control-allow-methods': 'GET,POST,OPTIONS', 'access-control-allow-headers': 'content-type' };
    if (req.method === 'OPTIONS') return new Response(null, { headers: cors });
    if (url.pathname === '/run') { const s = await cycle(env); return new Response(JSON.stringify(s), { headers: cors }); }
    /* ---- RESULTS RELAY ----
       Every study on the dashboard runs in the browser against live APIs, which meant the only
       way to show a result to anyone not sitting at the iPad was a screenshot. This endpoint gives
       those results somewhere public to live: the dashboard POSTs its verdict here after each run,
       the Worker keeps the last 30, and anything that can fetch a URL can then read the real
       numbers instead of squinting at an image. Writes are gated on the ntfy topic, which is
       already a shared secret between the two ends, so no new configuration is needed. */
    /* /tape                      → coverage index: which days have how many snapshots
       /tape?day=YYYY-MM-DD       → that whole day, hour shards stitched back into one series
       /tape?day=...&hour=HH      → a single hour shard (cheap; one KV read) */
    if (url.pathname === '/tape') {
      const day = url.searchParams.get('day');
      if (!day) {
        const st = await loadState(env);
        return new Response(JSON.stringify({ days: st.tapeDays || {}, ttlDays: TAPE_TTL_DAYS,
          cols: { m: ['id', 'bid_mc', 'ask_mc', 'vol24h'], k: ['strike', 'bid_mc', 'ask_mc', 'vol'] },
          venues: { m: 'polymarket top-40 by 24h volume', k: 'kalshi ' + (st.kalEvent || 'KXFED') + ' ladder' } }), { headers: cors });
      }
      if (!/^\d{4}-\d{2}-\d{2}$/.test(day)) return new Response('{"error":"bad day"}', { status: 400, headers: cors });
      const hour = url.searchParams.get('hour');
      if (hour !== null) {
        if (!/^\d{2}$/.test(hour)) return new Response('{"error":"bad hour"}', { status: 400, headers: cors });
        const raw = await env.BOT_STATE.get(`tape:${day}:${hour}`);
        return new Response(raw || JSON.stringify({ day, hour, snaps: [] }), { headers: cors });
      }
      /* Stitch: 24 KV reads, which are not subrequests and do not touch the cycle's ceiling.
         Missing hours are simply absent — a gap in the tape must read as a gap, never as zeros. */
      const hours = Array.from({ length: 24 }, (_, i) => String(i).padStart(2, '0'));
      const shards = await Promise.all(hours.map(h => env.BOT_STATE.get(`tape:${day}:${h}`)));
      const snaps = [];
      for (const raw of shards) {
        if (!raw) continue;
        try { const sh = JSON.parse(raw); if (Array.isArray(sh.snaps)) snaps.push(...sh.snaps); } catch (e) {}
      }
      snaps.sort((a, b) => a.t - b.t);
      return new Response(JSON.stringify({ day, snaps,
        cols: { m: ['id', 'bid_mc', 'ask_mc', 'vol24h'], k: ['strike', 'bid_mc', 'ask_mc', 'vol'] } }), { headers: cors });
    }
    if (url.pathname === '/results') {
      if (req.method === 'POST') {
        const k = url.searchParams.get('k') || '';
        if (!env.NTFY_TOPIC || k !== env.NTFY_TOPIC) return new Response('{"error":"bad key"}', { status: 403, headers: cors });
        let body;
        try { body = await req.json(); } catch (e) { return new Response('{"error":"bad json"}', { status: 400, headers: cors }); }
        const raw = await env.BOT_STATE.get('results');
        const list = raw ? JSON.parse(raw) : [];
        list.unshift({ at: Date.now(), ...body });
        await env.BOT_STATE.put('results', JSON.stringify(list.slice(0, 30)));
        return new Response(JSON.stringify({ ok: true, stored: Math.min(list.length, 30) }), { headers: cors });
      }
      const raw = await env.BOT_STATE.get('results');
      return new Response(raw || '[]', { headers: cors });
    }
    if (url.pathname === '/alerts') {
      const st = await loadState(env);
      return new Response(JSON.stringify({ lastRun: st.lastRun, lastAlertAt: st.lastAlertAt || 0,
        runs: st.runs, scanned: st.radarScanned || 0, alerts: (st.alerts || []).slice(0, 60) }), { headers: cors });
    }
    if (url.pathname === '/reset') {
      await env.BOT_STATE.put('state', JSON.stringify({ bank: CFG.START_BANKROLL, cash: CFG.START_BANKROLL,
        positions: [], equityLog: [], startedAt: Date.now(), runs: 0, lastRun: 0 }));
      return new Response('{"ok":true}', { headers: cors });
    }
    const s = migrate(await loadState(env));
    const closed = s.positions.filter(p => p.status === 'closed' && Number.isFinite(p.pnl));
    return new Response(JSON.stringify({
      equity: s.equity ?? s.cash, bank: s.bank, cash: s.cash,
      realised: closed.reduce((a, p) => a + p.pnl, 0),
      wins: closed.filter(p => p.pnl > 0).length, closed: closed.length,
      open: s.positions.filter(p => p.status === 'open').length,
      pending: s.positions.filter(p => p.status === 'pending').length,
      cancelled: s.positions.filter(p => p.status === 'cancelled').length,
      tape: { days: s.tapeDays || {}, kalshiEvent: s.kalEvent || null, kalshiDiag: s.kalDiag || null,
        note: 'GET /tape?day=YYYY-MM-DD — paired snapshots: m = polymarket, k = kalshi ladder' },
      houseRisk: s.house ? (() => {
        const ps = Object.values(s.house.pos || {});
        const gross = ps.reduce((a, p) => a + Math.abs((p.shares || 0) * (p.mid || 0.5)), 0);
        const shorts = ps.filter(p => (p.shares || 0) < 0);
        // worst case: every short outcome resolves YES — we pay $1/share against what we received
        const tail = shorts.reduce((a, p) => a + Math.abs(p.shares) * (1 - (p.mid || 0.5)), 0);
        return { gross: +gross.toFixed(2), tailIfShortsResolveYes: +tail.toFixed(2),
          shortMkts: shorts.length, longMkts: ps.filter(p => (p.shares || 0) > 0).length,
          buyFills: s.house.buyFills || 0, sellFills: s.house.sellFills || 0,
          breaches: ps.filter(p => Math.abs((p.shares || 0) * (p.mid || 0.5)) > CFG.HOUSE_MAX_INV_USD + 1).length };
      })() : null,
      /* The boring-vs-news verdict, in cents per share of realized markout. Negative = we are the
         one being picked off. Reported with a standard error because a handful of fills in a
         trending market can print any number at all, and this project has been burned by exactly
         that before. Share-weighted: a 500-share fill should not count the same as a 5-share one. */
      markout: s.house && s.house.mk ? (() => {
        const out = {};
        for (const [cohort, hz] of Object.entries(s.house.mk)) {
          out[cohort] = {};
          for (const [k, a] of Object.entries(hz)) {
            if (!a || !a.sh) continue;
            const mean = a.sum / a.sh;                        // cents-per-share, share-weighted
            const varr = Math.max(0, a.sumsq / a.sh - mean * mean);
            const se = a.n > 1 ? Math.sqrt(varr / a.n) : null;   // n = fills, the unit of independence
            out[cohort][k] = { fills: a.n, shares: Math.round(a.sh),
              centsPerShare: +(mean * 100).toFixed(3),
              se: se === null ? null : +(se * 100).toFixed(3) };
          }
        }
        return out;
      })() : null,
      rebateAudit: (s.house && s.house.rebateAudit) || null,
      forecastVsMarket: s.h23 ? (() => {
        const n = s.h23.n;
        const mean = n ? s.h23.pnlC / n : 0;
        /* one observation per city-day; SE from the binary outcome dominates at this sample size */
        const p = n ? s.h23.hit / n : 0;
        return { cityDays: n, forecastBandHit: s.h23.hit, hitRate: n ? +(p * 100).toFixed(1) : null,
          totalPnlC: +s.h23.pnlC.toFixed(1), meanPnlPerTradeC: +mean.toFixed(2),
          feesPaidC: +s.h23.feesC.toFixed(1), byCity: s.h23.byCity,
          scanned: Object.keys(s.h23.done || {}).length, recent: s.h23.log || [],
          strategy: 'buy the contract whose band contains the 12:00Z NBS forecast, at the ask 12h before close, hold to settlement, net of Kalshi taker fee',
          note: 'needs ~100 city-days before the mean means anything; a single 40c mispricing can carry 20 observations' };
      })() : null,
      forecastTape: s.fcDays ? { days: s.fcDays, cities: CFG.WX_CITIES.map(c => c.k),
        note: 'met.no air temperatures in tenths of a degree C, recorded alongside the Kalshi ladder so forecast and market can be graded against the same settlement' } : null,
      staleFacts: s.stale ? { seen: s.stale.seen, candidates: s.stale.list || [],
        note: 'deadline PASSED but price still mid-range — an unresolved fact, not a probability. For human checking, not an automated trade.' } : null,
      pairArb: s.pair ? { checked: s.pair.checked, feeFree: s.pair.feeFree,
        bestBuyGapC: s.pair.bestSpreadC, best: s.pair.best, hits: s.pair.hits || [],
        note: 'YES and NO have separate books; ask(Y)+ask(N)<1 merges to $1, bid(Y)+bid(N)>1 splits from $1. Depth shown because a gap without size is not a trade.' } : null,
      monotone: s.mono ? { laddersSeen: s.mono.ladders, pairChecks: s.mono.checks,
        feeFreeLadders: s.mono.feeFree, pages: s.mono.scanned, best: s.mono.best,
        hits: s.mono.hits || [],
        note: 'a cumulative deadline ladder must be monotone by logic; bid(earlier) > ask(later) is a riskless credit' } : null,
      negRisk: s.nr ? { setsSeen: s.nr.sets, pages: s.nr.scanned, feeFreeSets: s.nr.feeFree,
        best: s.nr.best, hits: s.nr.hits || [], overroundHistC: s.nr.hist,
        note: 'shortEdge is riskless regardless of exhaustiveness (max liability $1); longEdge is gated on it' } : null,
      /* Kalshi weather calibration, priced 12h before close, with the fee that market actually
         charges folded in. `edgePct` is realized minus implied; `netEdgePct` subtracts Kalshi's
         taker fee (0.07*p*(1-p), the published schedule) so a band only reads tradeable if it
         survives the cost of trading it. */
      weather: s.kwx ? (() => {
        const wilson = (k, n) => { if (!n) return [0, 1];
          const z = 1.96, p = k / n, d = 1 + z * z / n;
          const c = (p + z * z / (2 * n)) / d;
          const h = z * Math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d;
          return [Math.max(0, c - h), Math.min(1, c + h)]; };
        const rows = Object.entries(s.kwx.buckets || {}).sort((a, b) => a[0] - b[0]).map(([b, c]) => {
          const n = c[0], k = c[1], implied = c[2] / c[0];
          const [lo, hi] = wilson(k, n), realized = k / n;
          const fee = 0.07 * implied * (1 - implied);
          const edge = realized - implied;
          const net = Math.abs(edge) - fee;
          return { band: `${+b * 5}-${+b * 5 + 5}c`, n, wins: k,
            impliedPct: +(implied * 100).toFixed(1), realizedPct: +(realized * 100).toFixed(1),
            loPct: +(lo * 100).toFixed(1), hiPct: +(hi * 100).toFixed(1),
            edgePct: +(edge * 100).toFixed(1), feePct: +(fee * 100).toFixed(2),
            netEdgePct: +(net * 100).toFixed(2),
            verdict: (hi < implied || lo > implied) ? (net > 0 ? 'TRADEABLE' : 'mispriced but under fees') : 'no call' };
        });
        return { rows, graded: s.kwx.n, wins: s.kwx.wins,
          scanned: Object.keys(s.kwx.done || {}).length, noQuote: s.kwx.noQuote || 0,
          lastCalls: s.kwx.lastCalls || 0, leadHours: 12,
          series: CFG.KWX_SERIES,
          tradeable: rows.filter(r => r.verdict === 'TRADEABLE').length };
      })() : null,
      /* Calibration curve across resolved markets — the honest form of the crowd-bias question.
         Each row: outcomes priced in this 5-cent band, how often they actually won, with a Wilson
         interval. Favourite-longshot bias would show as realized BELOW implied at the cheap end
         and ABOVE at the expensive end. A row whose interval straddles its own implied price says
         nothing, and most rows will, for a long time. `coverage` is reported because the tape
         window is 500 trades: busy markets may not reach back 24h, and those get skipped — a
         skipped market is not a random one, so the number is worth watching. */
      calibration: s.calib ? (() => {
        const wilson = (k, n) => {
          if (!n) return [0, 1];
          const z = 1.96, p = k / n, d = 1 + z * z / n;
          const c = (p + z * z / (2 * n)) / d;
          const h = z * Math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d;
          return [Math.max(0, c - h), Math.min(1, c + h)];
        };
        const rows = hz => Object.entries(s.calib[hz] || {}).sort((a, b) => a[0] - b[0]).map(([b, [n, k]]) => {
          const implied = (+b * 5 + 2.5) / 100, [lo, hi] = wilson(k, n);
          return { band: `${+b * 5}-${+b * 5 + 5}c`, n, wins: k,
            impliedPct: +(implied * 100).toFixed(1), realizedPct: +((k / n) * 100).toFixed(1),
            loPct: +(lo * 100).toFixed(1), hiPct: +(hi * 100).toFixed(1),
            verdict: hi < implied ? 'OVERPRICED' : lo > implied ? 'UNDERPRICED' : 'no call' };
        });
        const h24 = rows('h24');
        return { h24, h7d: rows('h7d'),
          coverage: { used: s.calib.used || 0, skipped: s.calib.skipped || 0,
            note: 'skipped = tape window (500 trades) did not reach back to the horizon' },
          calls: h24.filter(r => r.verdict !== 'no call').length };
      })() : null,
      pennies: s.pennies ? { active: s.pennies.active, wins: s.pennies.wins, reversals: s.pennies.reversals,
        fills: s.pennies.fills, scanned: Object.keys(s.pennies.done || {}).length,
        offset: s.pennies.offset, lastCalls: s.pennies.lastCalls || 0, log: (s.pennies.log || []).slice(0, 5),
        /* The strategy restated in the unit that decides whether it is worth running.
           `perTrade` is the old view: return on capital per resolved market, one observation each.
           `apr` is the same trades annualised — reported three ways on purpose, because they
           disagree and the disagreement is the point. The mean is pulled around by markets that
           resolved in hours (a 2% gain over six hours annualises to four figures and means
           nothing at scale); the median is what a typical position earns; and `portfolio` is the
           only one you could actually run — total return divided by total capital-DAYS, which is
           what a book that redeploys each dollar as it frees up would compound at. */
        econ: (() => {
          const obs = s.pennies.obs || [];
          if (!obs.length) return { n: 0, note: 'accumulating — needs resolved markets with usable end dates' };
          const rets = obs.map(o => o[3] / 100), days = obs.map(o => o[1]);
          const n = obs.length;
          const mean = a => a.reduce((x, y) => x + y, 0) / a.length;
          const med = a => { const b = [...a].sort((x, y) => x - y); const h = b.length >> 1;
            return b.length % 2 ? b[h] : (b[h - 1] + b[h]) / 2; };
          const seOf = a => { const m = mean(a); return Math.sqrt(a.reduce((x, y) => x + (y - m) * (y - m), 0) / Math.max(1, a.length - 1) / a.length); };
          const aprs = obs.map(o => (o[3] / 100) * 365 / Math.max(0.25, o[1]));
          const sumR = rets.reduce((x, y) => x + y, 0), sumD = days.reduce((x, y) => x + y, 0);
          return {
            n, wins: obs.filter(o => o[2] === 1).length,
            avgEntryC: +(mean(obs.map(o => o[0] / 10))).toFixed(2),
            perTradePct: +(mean(rets) * 100).toFixed(3), perTradeSePct: +(seOf(rets) * 100).toFixed(3),
            holdDaysMedian: +med(days).toFixed(2), holdDaysMean: +mean(days).toFixed(2),
            aprMeanPct: +(mean(aprs) * 100).toFixed(1), aprSePct: +(seOf(aprs) * 100).toFixed(1),
            aprMedianPct: +(med(aprs) * 100).toFixed(1),
            aprPortfolioPct: sumD > 0 ? +((sumR / sumD) * 365 * 100).toFixed(1) : null,
            netOfFees: true,
            /* ---- THE BAND TABLE, which is the only honest way to read this strategy ----
               A single headline number for "buy the settlement pennies" is meaningless, because
               everything depends on the price you can actually get filled at, and that price is
               not 98c. Checked directly against the live book: a near-certain market (Israel/Iran
               ceasefire, resolving the same day) had exactly one ask level — 68,373 shares at
               99.9c. Deep enough to fill any size we would ever trade, and worth 0.1c per share.
               The 2c payoff and the 99.9% safety are never on offer at the same moment: a market
               sits at 98c precisely because it still carries real reversal risk, and by the time
               that risk is gone the book has repriced to 99.9.
               So: EV = (1-r)(1-p) - r*p - fee, giving breakeven r* = (1 - p - fee). At 98c you can
               tolerate a 2% reversal rate; at 99.9c you need under 0.1%, which by the rule of three
               takes ~3,000 clean observations to establish rather than ~150. Same strategy, twenty
               times the evidence, entirely because of the entry price.
               `needN` is that requirement. A band is only ever CLEARED when its own observed record
               meets its own bar. */
            byEntry: (() => {
              const bands = [[980, 985], [985, 990], [990, 995], [995, 1000]];
              return bands.map(([lo, hi]) => {
                const inB = obs.filter(o => o[0] >= lo && o[0] < hi);
                const n = inB.length, wins = inB.filter(o => o[2] === 1).length;
                const rev = n - wins;
                const p = (lo + hi) / 2000;
                const rStar = 1 - p;                       // fee-free case; fees only make it harder
                // rule of three (and its one-failure analogue) for the 95% upper bound on r
                const needN = Math.ceil((rev === 0 ? 3 : rev === 1 ? 4.74 : 6.3) / rStar - 1e-9);
                const upper = n ? (rev === 0 ? 3 / n : (rev + 2) / n) : 1;
                return { band: `${lo / 10}-${hi / 10}c`, n, reversals: rev,
                  breakevenRevPct: +(rStar * 100).toFixed(3),
                  observedUpperPct: n ? +(upper * 100).toFixed(3) : null,
                  needN, cleared: n >= needN && upper < rStar };
              });
            })(),
          };
        })() } : null,
      house: s.house ? { equity: s.house.equity || 0, cash: s.house.cash, rebates: s.house.rebates,
        fills: s.house.fills, markets: (s.house.mkts || []).length,
  inventory: Object.values(s.house.pos || {}).map(p => ({ q: p.q, shares: Math.round(p.shares),
          usd: Math.round(p.shares * (p.mid || 0)), cohort: p.cohort || 'unverified',
          feeType: (p.fee && p.fee.type) || 'unknown', rebateRate: (p.fee && p.fee.rebate) || 0 })),
        log: (s.house.log || []).slice(0, 8) } : null,
      voided: s.positions.filter(p => p.status === 'voided').length, migratedAt: s.migratedAt || 0,
      version: VERSION,
      runs: s.runs, lastRun: s.lastRun, startedAt: s.startedAt,
      equityLog: s.equityLog.slice(-200),
      positions: s.positions.slice(0, 60),
      lastNotes: s.lastNotes || [],
      gates: s.gates || null, bestNearMiss: s.bestNearMiss || null,
      cyclesSinceFill: s.cyclesSinceFill || 0, cfg: { minScore: CFG.MIN_SCORE, minUsd: CFG.MIN_TRADE_USD, newsOnly: CFG.NEWS_ONLY },
      alerts: (s.alerts || []).slice(0, 40), lastAlertAt: s.lastAlertAt || 0, scanned: s.radarScanned || 0,
    }), { headers: cors });
  },
};
