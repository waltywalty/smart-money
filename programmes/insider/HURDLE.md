# T4 - The hurdle at Walton's size

Programme: insider. Packet 7, task T4. Written 2026-08-24.

**No live quotes and no market data were pulled.** Every figure is from published broker
documentation or a regulator's own release, fetched as raw bytes. Where a component could not
be established from documentation, it says so rather than carrying an estimate.

| source read | fetch | control |
|---|---|---|
| `interactivebrokers.co.uk/en/pricing/commissions-stocks.php` | HTTP 200, 517,583 B | impossible path on host -> **404** |
| `interactivebrokers.co.uk/en/pricing/commissions-spot-currencies.php` | HTTP 200, 103,808 B | same host |
| `interactivebrokers.co.uk/en/trading/us-stock-trading-costs-for-uk-and-eu.php` | HTTP 200, 127,957 B | same host |
| `sec.gov/files/rules/final/2024/34-99679.pdf` - Disclosure of Order Execution Information | HTTP 200, 3,458,479 B | impossible path on `sec.gov` -> **404** |

---

## 1. Commission - ESTABLISHED

Verbatim from the published schedule, United States stocks:

> "Monthly Volume (shares) Tiered Fixed **<= 300,000 USD 0.0035 USD 0.005** [...] **Minimum
> per order USD 0.35** [Tiered] **USD 1.00** [Fixed] **Maximum per order 1% of Trade Value**"

Third-party fees, verbatim: "SEC Transaction Fee: **USD 0.0000206 * Value of Aggregate
Sales**. FINRA Trading Activity Fee: **USD 0.000195 * Quantity Sold**. FINRA Consolidated
Audit Trail Fees: **USD 0.000003 * Quantity**."

### The commission is per SHARE, so its cost in basis points is a function of share price

This is the single most decision-relevant piece of arithmetic in T4, and it is computed
entirely from the quoted schedule.

| share price | commission one way (bps) | round trip (bps) |
|---|---:|---:|
| $100.00 | 0.4 | 0.7 |
| $50.00 | 0.7 | 1.4 |
| $20.00 | 1.8 | 3.5 |
| $10.00 | 3.5 | 7.0 |
| $5.00 | 7.0 | **14.0** |
| $2.00 | 17.5 | **35.0** |
| $1.00 | 35.0 | **70.0** |
| $0.50 | 70.0 | **140.0** |

**A per-share commission is a percentage cost that rises as the share price falls.** The
literature's effect concentrates in small and microcap names; low-priced shares are common
there. At $2 a share the commission alone is 35 bps round trip - **more than
`KILL-CONDITION.md` section 1a's entire 25 bp floor, before spread, before borrow, before
FX.**

> **The 1% cap does not rescue this.** It binds only below roughly $0.35 a share
> (0.0035/0.35 = 1%). Everywhere above that, the per-share charge applies in full.

---

## 2. FX on GBP-USD, both ways - ESTABLISHED

Verbatim: "Spot Currencies Monthly Trade Value (USD) Tiered **<= 1,000,000,000 0.20 basis
point * Trade Value** [...] **Minimum per order Tier I - USD 2.00**"

Charged **twice** - in on entry, out on exit.

| position (USD) | FX charge each way | round trip (bps) |
|---|---:|---:|
| $1,000 | $2.00 | **40.0** |
| $2,500 | $2.00 | **16.0** |
| $5,000 | $2.00 | 8.0 |
| $10,000 | $2.00 | 4.0 |
| $25,000 | $2.00 | 1.6 |
| $100,000 | $2.00 | 0.4 |
| $250,000 | $5.00 | 0.4 |

> **The USD 2.00 minimum binds on every position below roughly $100,000.** 0.20 bp of
> $100,000 is exactly $2.00. Below that the headline rate is irrelevant and the fee is fixed,
> so **the cost in basis points is inversely proportional to position size.** At $2,500 the
> advertised 0.2 bp is really **16 bps round trip - eighty times the headline.**

This is the H7/H9 shape from the Kalshi programme in a different currency: **a fixed cost
against a small position is a large percentage, and the schedule's headline rate describes
nobody at retail size.**

---

## 3. Spread - COULD NOT ESTABLISH

The packet asks for typical quoted and effective spread on sub-$2bn US names from published
exchange or academic market-quality data.

**A spread level in basis points for that universe was not obtained.** The SEC's 2024 Rule
605 final release was read in full (1,403,664 characters extracted). It discusses spreads by
market capitalisation **qualitatively and by horizon**, but no level in basis points or cents
for a size group was extracted. Verbatim, what it does establish:

> "approximately **90% of the cumulative decline in realized spread is captured by the
> 15-second horizon for the largest market capitalization group**, compared to only about
> **50% for the smaller market capitalization groups**."
>
> "the Commission analyzed realized spreads calculated over time horizons ranging from 10
> milliseconds to five minutes, as well as how they differ based on market capitalization
> size, using **TAQ data from Q1 2023 for a sample of 400 stocks** from four different market
> capitalization [groups]"

So: spread behaviour **differs materially by market cap**, on the regulator's own current
data, and price impact persists roughly twice as long in smaller names. **The magnitude is
not established here.**

Obtaining it requires pulling market data, which this packet forbids. Per
`KILL-CONDITION.md` section 4a this is recorded as **could not establish**, not as "spread is
small" and not as "spread is large".

**One documented anchor on the liquidity of the relevant universe**, from Zhao (2026): the
investable filter was "a minimum average daily dollar volume (ADDV) of **$200,000** over the
trailing 30 days". A name trading $200,000 a day is not a name where a headline spread
statistic applies.

---

## 4. Borrow on the short leg - COULD NOT ESTABLISH

Not obtained from documentation. Borrow rates are quoted per name and vary daily; a current
rate is market data.

**What is structurally true and worth stating:** the strategies in `PRIORS.md` that produce
the headline figures are **long-short** - Cohen, Malloy & Pomorski's alphas are "long
opportunistic buys and short opportunistic sells". A long-short implementation requires
borrow on the short leg **in exactly the small names where borrow is scarcest and most
expensive, and where it may not be available at all.** The packet's instruction to include
the possibility of unavailability is not a hypothetical: it is the modal case in microcaps.

**Unquantified. Not zero.** A long-only implementation avoids it and forfeits whatever part
of the reported spread comes from the short leg - which `PRIORS.md` does not decompose.

---

## 5. Capital lockup

Arithmetic, not a measurement. `KILL-CONDITION.md` section 1c:

```
annualised net residual = per-event net residual x (365 / horizon_days)
```

Applied to the horizons in `PRIORS.md`:

| strand | horizon | turns per year (serial redeployment) |
|---|---|---:|
| Cohen, Malloy & Pomorski | 1 month, rebalanced monthly | ~12 |
| Lakonishok & Lee | 12 months | 1 |
| Zhao | 30 trading days | ~8.7 |

> **Turnover multiplies the cost, not just the return.** A monthly-rebalanced long-short pays
> the round-trip commission and spread **twelve times a year on both legs**. The Lakonishok &
> Lee 12-month horizon pays once. **The strand with the largest reported alpha is the one that
> pays the hurdle most often**, and `PRIORS.md` reports its alpha gross of that.

---

## 6. Tax - A STATED UNKNOWN, NOT AN ESTIMATE

UK tax treatment of US equity trading, and specifically whether a long-short implementation
is treated differently from long-only, **requires professional advice and is not modelled
here.** It is not a modelling question and no figure is offered.

Recorded because it is a real leg of the arithmetic that is deliberately absent, not because
it is small.

---

## 7. The comparison table

The packet: *"express the T2 effect sizes and this hurdle in the same units, on the same
horizon. That single table is the point of the packet."*

### The table cannot be built. This is could-not-establish on the arithmetic, not a hurdle failure.

The two verdicts are different and are kept separate. A hurdle failure would mean the residual
was computed and found negative. **Nothing was computed**, for reasons that sit on both sides
of the subtraction.

| what the comparison needs | status | why |
|---|---|---|
| Effect size **per event** | **MISSING** | Every figure in `PRIORS.md` is a portfolio alpha or a subgroup mean. No strand reports a per-event abnormal return. |
| A **defined population** | **MISSING** | T3: `P` conflates open-market and private purchases; "a trade" in the routine lookback is undefined; two defensible readings give different samples. |
| **Investable event rate** | **MISSING** | Not reported by any strand, and not derivable without the classifiable-share figure T3 could not extract. |
| **Spread** | **MISSING** | Section 3 - not obtainable without market data. |
| **Borrow** | **MISSING** | Section 4 - same. |
| Commission | **ESTABLISHED** | Section 1. |
| FX | **ESTABLISHED** | Section 2. |
| Capital lockup | **ESTABLISHED** as arithmetic | Section 5, given a horizon. |
| Tax | **DECLINED** | Section 6 - requires advice. |

**Five of nine inputs are missing, and three of the five are missing from the literature
rather than from this session's reach.** Filling any cell with an assumption would produce a
number, and the number would be the assumption.

### What can be said without the table

Two of the nine components are established, and **they alone can exceed the kill
condition's floor** in the region where the effect is reported to live:

> A $2,500 position in a $2 share pays **35 bps commission + 16 bps FX = 51 bps round trip**,
> before spread, before borrow, before tax. `KILL-CONDITION.md` section 1a sets a floor of
> **25 bps net**.

That is not a verdict. It is two of nine cost lines against a residual that has not been
computed, and stating it as a verdict would be exactly the assumption-filling the table
refuses.

---

## 8. The effect and the hurdle live in the same place

Stated plainly because it survives the table's absence.

Cohen, Malloy & Pomorski report **equal-weight 180 bp/month against value-weight 82
bp/month** for the same strategy on the same data. The gap is where the effect lives:
**more than half of the measured alpha is in the smaller names.**

And every established cost line in this document worsens in exactly those names:

| cost | direction in small / low-priced names |
|---|---|
| Commission (per share) | **worse** - 35 bps round trip at $2/share against 1.4 at $50 |
| FX minimum | **worse** - small positions, fixed $2.00 fee, inversely proportional |
| Spread | **worse** - magnitude unestablished, but the SEC's own analysis shows impact persisting twice as long in smaller caps |
| Borrow | **worse** - scarcest and most expensive, possibly unavailable |

**The equal-weight figure is the one that looks investable and the one that cannot be
harvested at retail size; the value-weight figure is the one that can be harvested and is
less than half as large.** The literature reports both without resolving which a small
account should read, and `PRIORS.md` records that as contested rather than settled.

McLean & Pontiff, read in T2, point the same way from the other side: post-publication
returns are "**higher for portfolios concentrated in stocks with high idiosyncratic risk and
low liquidity**". The part of the effect that survived publication is the part that is
hardest to trade.
