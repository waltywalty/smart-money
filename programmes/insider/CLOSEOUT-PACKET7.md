# Packet 7 - close-out

Programme: insider (family 2), **SCOPED, NOT OPEN**. Worked 2026-08-24, one session.
No collector, no parser, no EDGAR pipeline. **No filing data was fetched at any point.**
Nothing was traded. No GO was sought or given. **The gate is unchanged.**

## The verdict

**COULD NOT ESTABLISH, on every strand**, against `KILL-CONDITION.md` sealed before the
literature was read - sha256 `925b9bff478cea4211d7c4cdccf626e70f2ca58c99745a6730a90cef3dcfcde1`,
commit `eac6eda`. No strand was killed. No strand survives. Full reasoning in
`SCOPING-VERDICT.md`.

---

## MEASURED

**Almost nothing in a literature review is MEASURED by this project.** That is the point of the
distinction and it is kept strictly. Only these were measured *by this session*, on sources it
fetched and read as raw bytes:

- **Chen & Zimmermann's catalogue contains no insider signal.** 331 documented signals, zero
  matching `insider`, `Form 4`, `Section 16`, `13D`, `opportunistic`. **Controlled**: `momentum`
  20, `analyst` 23, `accrual` 16, `short interest` 3. Structural confirmation - the data
  categories are Accounting 196, Price 56, Analyst 21, Trading 20, Other 13, Options 9, **13F 8**,
  Event 8. **No Form 4 category exists.** File current to September 2025; impossible-path control
  on the host **404**.
- **The Form 4 transaction-code table**, complete, from the SEC's own instructions. **`P` = "Open
  market *or private* purchase"** - the code does not separate them.
- **The 10b5-1 checkbox is mandatory only from 2023-04-01**, amendments effective 2023-02-27,
  from the SEC's own compliance guide. Bona fide gifts moved from Form 5 to Form 4 on the same
  date.
- **The Section 16 deadline** - "before the end of the second business day" - from the form.
- **IBKR published fees**: US stocks tiered **USD 0.0035/share**, minimum **USD 0.35**, maximum
  **1% of trade value**; FX **0.20 bp** with a **USD 2.00** minimum per order.
- **The arithmetic on those fees**: commission **35 bps round trip at $2/share**; the FX minimum
  binds on every position below **~$100,000**, costing **16 bps round trip at $2,500**.
- **The verification controls themselves.** McLean & Pontiff's PDF returns zero hits for
  `insider` **and zero for `share issuance`, `asset growth`, `net operating assets`** - the
  predictor list is in an Internet Appendix not present in the document. The zero measures the
  search, not the paper.

## INFERRED

**What a paper reports is INFERRED from that paper's instrument on that paper's sample.** Every
figure below is in this list rather than MEASURED, however solid the journal.

- Lakonishok & Lee (RFS 2001): **4.8%** 12-month spread after size and B/M controls, **7.8%**
  before. >1,000,000 trades, **1975-1995**.
- Cohen, Malloy & Pomorski (JF 2012): **VW 82 bp/mo** (t=2.15), **EW 180 bp/mo** (t=6.07),
  five-factor. Routine **43 bp/mo** (t=1.73). **1989-2007**.
- Zhao (arXiv 2026): mean **CAR[1,30] 6.3%** on a >10%-run-up subgroup, hit rate **36.7%**.
  17,237 purchases, 1,343 issuers, **2018-2024**. Preprint; **not risk-adjusted on its own
  statement**.
- McLean & Pontiff (JF 2016): **26% lower out-of-sample, 58% lower post-publication** across 97
  predictors, sample ending 2013. **A base rate for published anomalies, not a measurement of
  this one.**
- SEC Rule 605 release: realized-spread decline ~90% captured by 15s for the largest cap group
  vs ~50% for smaller groups. Q1 2023 TAQ, 400 stocks.
- **The convergence** of those three independent instruments on the same direction - the effect
  concentrates where trading is hardest.

## ASSUMED

- **That the papers report what they measured.** Read but not re-derived. Zhao is the caution:
  the abstract says "abnormal returns", the discussion says risk adjustment is future work.
- **That IBKR's published schedule is what a UK retail account is charged.** Documentation, not
  a statement.
- **That the strands are separable.** T2 treats seven; the literature may not divide there.
- **That "could not establish" is not concealing a kill.** If the missing numbers existed they
  might well fail the bar - four of nine hurdle cells are missing on the cost side too, and they
  can only make the residual worse.
- **That the searches were competent.** Three strands returned no peer-reviewed source. A better
  search might find one. **Recorded as could-not-establish, never as absence.**

---

## Strands with no post-publication re-estimation - the honest measure

**All seven. Listed by name because the list is the finding:**

1. Aggregate insider buys vs sells
2. Routine vs opportunistic
3. Small-cap / microcap concentration
4. Role weighting
5. Cluster buys
6. First-time buyers
7. Filing-lag informativeness

**Four rest on samples closing before 2016-08-24; two before 1996.** Three have no reachable
peer-reviewed source at all. **Nothing in this family rests on evidence younger than the
anomaly's own publicity**, except one non-peer-reviewed preprint that says it is not
risk-adjusted.

---

## Wrong before right

1. **"McLean & Pontiff do not cover insider trading."** Zero hits for `insider`. Nearly recorded.
   The control terms - `share issuance`, `asset growth`, `net operating assets`, all also zero -
   proved the instrument could not have found them. **A positive control on a search.** Without
   it, a fabricated negative from a search that could not succeed.
2. **"Zhao reports risk-adjusted abnormal returns."** The title and abstract say so. The
   discussion says defining the target in risk-adjusted units is future work. **Reading the source
   rather than the abstract is the whole difference.**
3. **"The comparison table is the deliverable, so build it."** Five of nine cells were missing.
   Filling them would have produced a number, and the number would have been the assumption.

---

## Parking lot

1. **McLean & Pontiff's Internet Appendix** - unreached. Whether this anomaly is among their 97
   is the cheapest open question in the packet.
2. **What "a trade" means in CMP's three-year lookback** - undefined in the paper; two readings
   give different populations.
3. **How `P` was split** between open-market and private purchases in any published study.
4. **A citable effective-spread level** for sub-$2bn US names from published market-quality data.
5. **Borrow cost and availability** on microcap shorts.
6. **Cluster buys, first-time buyers, filing lag** - no peer-reviewed source reached.

---

## For Walton

**Rule on the verdict.** Nothing else. The gate is not lifted and no build follows.

One note the packet asked to be carried: *"if this family survives scoping, it survives on the
literature's numbers rather than on ours."* **It did not survive, and it did not die.** What the
literature turned out not to publish - a per-event effect, a defined population, an investable
event rate - is exactly what a build would have had to assume. **The scoping found the assumption
before the build embedded it, which is what scoping is for.**
