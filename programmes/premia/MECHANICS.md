# T3 - Venue mechanics, from documentation only

Programme: premia. Packet 8, task T3. Written after `KILL-CONDITION.md` was sealed
(sha256 `2a87dc4c...`, commit `2d07ad7`) and after `PRIORS.md` (commit `69a2723`).

**No account was opened. No API key was used. No live figure was requested.** Every endpoint hit
below is a published specification or documentation page. Where an endpoint exists that would
answer a question in this document, and answering it would require pulling data, **it was not
called and that is recorded as an out-of-scope boundary rather than an unknown** - see section 7.2.

Per T1 section 10, everything here is **INFERRED** - a venue's own account of itself, not measured
by this project.

---

## 0. Reachability, and why the status codes had to be controlled

Three of the six venue sites return a status that **is not the document's status**. Each was
caught by a paired control, and each would otherwise have produced a false finding.

| venue | probe | control | verdict |
|---|---|---|---|
| **Hyperliquid** (GitBook `.md`) | real pages `200`, 1,160-12,174 B | impossible page **also `200`**, 2,135 B, body begins `# Page Not Found` | **soft-404.** Usable only with a **content** discriminator, never the status |
| **Deribit** `www.deribit.com` | KB article `200`, 12,155 B | impossible path `200`, 12,155 B; ToS `200`, 12,155 B - **all three md5 `fc19b20663b941df...`, byte-identical** | **single SPA shell for every path.** A 200 here carries **no** information about whether a document exists |
| **Binance** `www.binance.com` | real FAQ `202`, **0 bytes** | impossible FAQ **also `202`, 0 bytes**; browser network stack returns `202` with `X-Amzn-Waf-Action: challenge`, `X-Cache: Error from cloudfront` | **AWS WAF bot challenge.** The 202 is the WAF's, not the article's |
| **Deribit** `docs.deribit.com` | OpenAPI spec `200`, 1,439,011 B `application/json` | impossible spec filename `404` | **usable** |
| **OKX** `www.okx.com/docs-v5/en/` | `200`, 5,242,371 B | a wrong help path returned `404` | **usable** |
| **BitMEX**, **Bybit** | `200`/`206` but 3,167 B and 24,532 B of JS shell | - | **not read.** No content retrieved |

> **Binance is the venue in He et al.'s magnitude estimate, and its documentation could not be
> reached from this vantage.** Per T1 section 4.4 that is **could not establish**, never "Binance
> does not publish it". The WAF header is the evidence that the instrument failed rather than the
> resource being absent.

---

## 1. Hyperliquid

The only venue whose documentation was reachable **in full** as static text. Everything below is
quoted or paraphrased from `hyperliquid.gitbook.io/hyperliquid-docs/*.md`.

### 1.1 Funding

| item | documented |
|---|---|
| **interval** | **every hour**, at one eighth of the computed 8-hour rate |
| **formula** | `F = Average Premium Index (P) + clamp(interest rate - P, -0.0005, 0.0005)` |
| **interest component** | fixed **0.01% per 8h**, stated by the venue as **"11.6% APR paid to short"** |
| **premium source** | **both.** `premium = impact_price_difference / oracle_price`, where the impact prices are **order-book** average execution prices for a stated notional, and `oracle_price` is *"the weighted median of CEX spot prices for each asset, with weights depending on the liquidity of the CEX"* - so an **off-venue index** |
| **sampling** | premium sampled **every 5 seconds**, averaged over the hour |
| **cap** | **4% per hour**, and the venue itself notes this is *"much less aggressive capping than CEX counterparts"* |
| **what happens at the cap** | **not documented.** Named as a silence, section 7.1 |
| **notional convention** | payment = `position_size x oracle_price x funding_rate`. **The spot oracle price is used, not the mark price** |
| **who receives it** | *"Funding is purely peer-to-peer and no fees are collected on the payments"* |

**The index-versus-book divergence question the packet asks** is answered structurally here: the
premium is the gap between the **book** (impact prices) and the **oracle** (off-venue median). When
the two diverge, the funding rate *is* the divergence. A carry receiver is therefore paid in
proportion to how far the venue's book has drifted from the rest of the market - which is also the
condition under which the venue's own price is least reliable.

**The 11.6% APR interest component is structurally paid to the short**, but only through the
`clamp(interest - P, +/-0.0005)` term, so it contributes fully only when the premium is small and
is progressively displaced as the premium grows. It is not a floor on the carry.

### 1.2 Margin and liquidation

| item | documented |
|---|---|
| **max leverage** | 3x to 40x by asset |
| **maintenance margin** | *"half of the initial margin at max leverage"* - i.e. **between 1.25% (40x assets) and 16.7% (3x assets)** |
| **first-stage liquidation** | market orders sent **to the book**, full size, may fill fully or partially. No clearance fee |
| **partial liquidation** | positions **> 100k USDC**: only **20%** sent as a market order, then a **30-second cooldown**; during the cooldown all market liquidation orders are for the **entire** position |
| **backstop trigger** | account equity below **2/3 of maintenance margin** without successful book liquidation |
| **backstop mechanism** | **the liquidator vault, a component strategy of HLP** |
| **price used** | **mark price**, *"which combines external CEX prices with Hyperliquid's book state"*; the venue warns *"During times of high volatility or on highly leveraged positions, mark price may be significantly different from book price"* |

**The magnitude of a backstop liquidation, in the venue's own words:**

> "When a cross position is backstop liquidated, **the trader's cross positions and cross margin are
> all transferred to the liquidator.** In particular, if the trader has no isolated positions, **the
> trader ends up with zero account equity.**"

> "**During backstop liquidation, the maintenance margin is not returned to the user.** This is
> because the liquidator vault requires a buffer to make sure backstop liquidations are profitable
> on average."

**Total loss of cross margin occurs at 2/3 of maintenance margin - which is well above
insolvency.** T1 section 2.1 defines a material loss event as removal of >= 25% of venue capital.
This mechanism removes **100%** of cross margin, and it is triggered by price movement plus a
venue rule rather than by the venue failing.

### 1.3 The loss backstop - **T3's most important item**

**Hyperliquid documents no insurance fund.** Its chain is: book liquidation, then the **HLP
liquidator vault**, then **auto-deleveraging**. The ADL page, quoted in full because it is the item
that matters:

> "Auto-deleveraging strictly ensures that the platform stays solvent. If a user's account value or
> isolated position value becomes negative, **the users on the opposite side of the position are
> ranked by unrealized pnl and leverage used.** Backstop liquidated positions have no special
> treatment in the ADL queue logic. The specific sorting index... is
> `(mark_price / entry_price) * (notional_position / account_value)`. **Those traders' positions are
> closed at the previous mark price against the now underwater user**, ensuring that the platform
> has no bad debt."
>
> "Auto-deleveraging is an important final safeguard on the solvency of the platform. **There is a
> strict invariant that under all operations, a user who has no open positions will not socialize
> any losses of the platform.**"

**T1 section 3.4 fires.** A profitable, fully-margined position can be closed without the holder's
consent, and the queue is **ordered by profitability**: the sorting index rises with
`mark_price / entry_price` and with position notional relative to account value.

**Read the invariant precisely.** It guarantees that a user **with no open positions** will not
socialise losses. It does **not** say that a user **with** open positions will not. The guarantee
is scoped to flat accounts, and a carry book is never flat.

### 1.4 Fees, and the search for an FX-floor equivalent

Fees are **proportional**, tiered on rolling 14-day weighted volume, with a stated baseline all-in
taker rate of **0.045%** for validator-operated perps. Sub-account volume aggregates to the master.
No per-trade minimum charge is published.

**But the fixed cost is not in the fee schedule, and it is not published.** The onboarding page
says only:

> "Depending on the withdrawal chain and method, **there may be small gas fees** to process the
> withdrawal."

> **No figure. This is the exact quantity T1 section 1.4(ii) requires** - the fixed monetary cost
> that does not scale with size and therefore sets the capital floor. Named as a silence in
> section 7.1, and it is the silence with the sharpest consequence.

### 1.5 Jurisdiction

**Not established in this packet.** The venue's terms page is served from `app.hyperliquid.xyz`
as a JS application and returned a shell; the docs site has no `risks` page (`risks.md` returned
the soft-404 body). **No determination of access is made or attempted** - per packet 8's
out-of-scope section, that is Walton's and possibly an adviser's.

---

## 2. OKX

Read from the `docs-v5` API specification, which was reachable as static HTML.

### 2.1 The loss backstop

OKX documents an **insurance fund first, then ADL**. The `adl` field description, verbatim:

> "Auto-Deleveraging (ADL) indicator. Range: 0-5, where 0 = lowest ADL priority (least likely to be
> forcibly deleveraged) and **5 = highest priority (first in queue if the insurance fund is
> depleted). Priority increases with higher unrealized pro[fit]...**"

**T1 section 3.4 fires again, and in the same direction.** Profitability moves a position **toward**
the front of the queue.

ADL is an **enumerated, routine event type** in the venue's own close-position taxonomy:
`1` close partially, `2` close all, `3` liquidation, `4` partial liquidation, **`5` ADL - position
not fully closed**, **`6` ADL - position fully closed**.

OKX also publishes a **public WebSocket "ADL warning channel"**. A venue that ships a warning
channel for a mechanism is telling you the mechanism fires often enough to warrant one.

### 2.2 Funding, margin, fees

**Not read in this packet.** The specification is 5.2 MB and only the backstop was extracted.
Recorded as a coverage gap of this packet, not a venue silence - section 7.3.

---

## 3. Deribit - the S2b venue

### 3.1 Ownership, and what it does to the vantage line

The page title returned by `www.deribit.com` is **"Crypto Futures and Options Exchange - Deribit by
Coinbase"**.

> **T1 section 4.2 fires: a change of ownership resets the per-venue vantage line.** Almeida et
> al.'s Bitcoin variance-risk-premium sample runs **July 2017 - December 2022** and predates this
> entirely. On T1's own terms, **that evidence describes a different venue.**

### 3.2 The loss backstop - socialised loss, documented as a settlement field

Deribit's OpenAPI specification defines the settlement record returned by
`public/get_last_settlements_by_currency` and `private/get_settlement_history_by_*`. Four of its
fields, with the venue's own descriptions verbatim:

| field | description, verbatim |
|---|---|
| `session_bankruptcy` | "value of session bankruptcy (in base currency; **bankruptcy only**)" |
| `session_tax` | "total amount of paid taxes/fees (in base currency; bankruptcy only)" |
| `session_tax_rate` | "**rate** of paid taxes/fees (in base currency; bankruptcy only)" |
| `socialized` | "**the amount of the socialized losses** (in base currency; bankruptcy only)" |

> **This is the mechanism packet 8 named as the one that matters and the one least written about:
> a solvent venue taking funds from profitable positions.** Deribit does not merely have it - it
> exposes it as a **first-class, publicly-queryable field with a rate**, which means socialisation
> is a designed part of settlement rather than an emergency measure.

Separately, the account-balance field description lists **"insurance refills"** among the
transaction categories that move a cash balance, so an insurance mechanism also exists. The word
"insurance" appears **zero** times elsewhere in the specification.

### 3.3 What could not be read

The **trigger** for socialisation, the size of the insurance fund, and the fee schedule are in the
knowledge base and terms pages, all of which are served by the single SPA shell of section 0.
**Could not establish**, with the byte-identity control as the evidence.

One fee figure survives from a secondary source read in T2 - Almeida et al. state Deribit option
trading fees are *"0.03% of the underlying or 0.0003 Bitcoin per option contract, capped"*. **That
is a paper's account of a venue's schedule, not the schedule**, and it is a 2024 paper describing a
pre-2023 sample. It is not used as a cost input.

---

## 4. Binance - could not establish

The venue whose figures underpin instrument A in `PRIORS.md`. Its funding-rate methodology article
- the one **cited by He et al. as their own source** - returned `202` with a zero-length body over
raw HTTP and over the browser network stack, with `X-Amzn-Waf-Action: challenge`.

**Nothing about Binance's funding formula, cap, margin, insurance fund, ADL or fee schedule is
recorded in this document**, and the reason is an instrument failure at this vantage rather than
anything about what Binance publishes.

---

## 5. BitMEX and Bybit - not read

Both returned JS shells of 3,167 and 24,532 bytes. No content was retrieved and no attempt was made
to render them. **Recorded as a coverage gap of this packet.**

---

## 6. The cross-venue picture on the backstop

| venue | insurance fund | socialised loss | ADL | ADL ordered by profit? |
|---|---|---|---|---|
| Hyperliquid | **none documented** | only for accounts **with** open positions; flat accounts are exempted by an explicit invariant | **yes, final safeguard** | **yes** - sorting index rises with `mark/entry` and with notional/account value |
| OKX | **yes**, ADL fires when it is **depleted** | not documented | **yes**, with a public warning channel | **yes** - "priority increases with higher unrealized profit" |
| Deribit | "insurance refills" exist as a balance category; **no fund documentation reachable** | **yes**, as a settlement field with a **rate** | present in the API vocabulary (17 mentions) | **not established** |
| Binance | **could not establish** | **could not establish** | **could not establish** | **could not establish** |

**Two venues out of two whose ADL ordering is documented rank the queue by profitability.** No
search was needed for this - it is in the field description and the mechanism page.

> **The delta-neutral book's hedge leg is its profitable leg in exactly the move that stresses the
> venue.** Both documented ADL queues put that leg at the front. This is recorded as a
> documentation finding; **T4 decides what it means**, and T1 section 3.4 has already committed
> that it is carried into T5 regardless of frequency.

---

## 7. The silences, named

### 7.1 Venue silences - the venue does not publish it

1. **Hyperliquid: what happens at the 4%/hour funding cap.** The cap is stated; the behaviour at
   it is not.
2. **Hyperliquid: the withdrawal cost.** *"there may be small gas fees"* with no figure. This is
   the fixed monetary cost T1 section 1.4(ii) needs, and its absence is what stops `K_min` being
   computed for this venue.
3. **Hyperliquid: no insurance fund is documented** - which is a design statement, not an omission,
   since ADL is named as the final safeguard.
4. **Deribit: the trigger for socialised loss.** The field exists, the rate exists, the amount
   exists. What causes a bankruptcy session, and at what threshold, is not in the specification.

### 7.2 Out of scope, not unknown - and this is the sharpest line in T3

> **Deribit publishes its socialised-loss history on a public, unauthenticated endpoint.**
> `public/get_last_settlements_by_currency` returns `socialized`, `session_tax_rate` and
> `session_bankruptcy` per settlement, with `search_start_timestamp` and `continuation` for paging.
>
> **It was not called.** Packet 8: *"Reading an exchange's published fee schedule, funding-rate
> methodology, insurance-fund documentation or historical statistics page is in scope. Pulling
> current funding rates, order books or price series is not."* A settlement history is a data pull.
>
> **So the frequency and magnitude of socialised loss at Deribit is not "not knowable from public
> sources". It is knowable, cheaply, and out of scope for this packet.** T4 must record it that
> way, and T5 must not convert it into a could-not-establish that implies the evidence does not
> exist.

### 7.3 Coverage gaps of this packet, not of any venue

- OKX funding, margin and fee schedules: reachable, not read.
- BitMEX and Bybit: not read at all.
- Jurisdiction statements for every venue: not read.
- Any venue's insurance-fund **balance history**: not sought, because retrieving it is a data pull.

---

## 8. What T4 inherits from this document

Stated as questions, not answers.

1. Both documented ADL queues rank by profitability. **Has that ever fired against a delta-neutral
   book, and is it recorded anywhere?**
2. Deribit's socialised-loss field implies bankruptcy sessions occur. **How often, and how large -
   from primary sources that are not the endpoint this packet may not call?**
3. Hyperliquid's backstop liquidation takes **all** cross margin at 2/3 of maintenance margin.
   **Is there an incident record of that firing at scale?**
4. The funding premium is the book-versus-oracle gap. **Do the documented failure episodes show
   that gap widening at the same venue where the position sits?** `PRIORS.md` section S1.7 already
   contains one instance and T4 must decide whether it is a pattern or an anecdote.
