# T3 - The classifier rules, as specifications

Programme: insider. Packet 7, task T3. Written 2026-08-24.

**Specifications, not code. No filing data was fetched.** Everything below is from the SEC's
own published form and instructions, its compliance guide, or a paper read as raw bytes.
Reading documentation to learn what a field means was in scope; pulling a filing to see what
is in the field was not.

| source read | fetch | control |
|---|---|---|
| `sec.gov/files/form4.pdf` - form and instructions | HTTP 200, 406,632 B | impossible path on `sec.gov` -> **404** |
| `sec.gov/resources-small-businesses/.../insider-trading-arrangements-and-related-disclosures` | HTTP 200, 74,632 B | same host |
| `nber.org/.../w16454.pdf` - Cohen, Malloy & Pomorski | HTTP 200, 219,222 B | - |

**An extraction caveat that limits some citations.** The Form 4 PDF's *instructions* extracted
cleanly; the *form grid* did not. Control check on headings that must be present:
`Transaction Date` 1, `Transaction Code` 3, `Securities Acquired` 4, but **`Ownership Form` 0
and `Title of Security` 0** - both certainly on the form. So where a column *number* is not
quoted below, the numbering was **not verified from this extraction** and is marked
UNVERIFIED rather than asserted.

---

## 1. Transaction codes - the one that contaminates everything downstream

Complete table, verbatim from the Form 4 instructions:

| code | meaning |
|---|---|
| **P** | **Open market or private purchase of non-derivative or derivative security** |
| **S** | **Open market or private sale of non-derivative or derivative security** |
| V | Transaction voluntarily reported earlier than required |
| A | Grant, award or other acquisition pursuant to Rule 16b-3(d) |
| D | Disposition to the issuer of issuer equity securities pursuant to Rule 16b-3(e) |
| F | Payment of exercise price or tax liability by delivering or withholding securities |
| I | Discretionary transaction in accordance with Rule 16b-3(f) |
| M | Exercise or conversion of derivative security exempted pursuant to Rule 16b-3 |
| C | Conversion of derivative security |
| E | Expiration of short derivative position |
| H | Expiration (or cancellation) of long derivative position with value received |
| O | Exercise of out-of-the-money derivative security |
| X | Exercise of in-the-money or at-the-money derivative security |
| **G** | **Bona fide gift** |
| L | Small acquisition under Rule 16a-6 |
| W | Acquisition or disposition by will or the laws of descent and distribution |
| Z | Deposit into or withdrawal from voting trust |
| J | Other acquisition or disposition (describe transaction) |
| K | Transaction in equity swap or instrument with similar characteristics |
| U | Disposition pursuant to a tender of shares in a change of control transaction |

**Specification.** An open-market purchase event is `code == P` on a non-derivative security.
Grants (`A`), option exercises (`M`, `X`, `O`, `C`), tax withholding (`F`), gifts (`G`) and
dispositions to the issuer (`D`) are **excluded**. `A` and `M` are the two that most inflate a
naive "insider bought" count: compensation arrives as `A` and is converted at `M`, and neither
is a decision to buy.

> **GAP - `P` is not "open market".** The code reads "Open market **or private** purchase". A
> private placement participation and an open-market buy carry the same code. **Form 4 does not
> distinguish them in the code field.** Separating them needs footnote text or a second source,
> and no paper reached in T2 states how it handled this. Recorded as unresolved.

---

## 2. Routine versus opportunistic

Verbatim from Cohen, Malloy & Pomorski:

> "we define a **routine trader** as an insider who placed a trade in the **same calendar
> month** for at least a certain number of years in the past."
>
> "We require an insider to make **at least one trade in each of the three preceding years** in
> order to define her as either an opportunistic or a routine trader."
>
> "We then define **opportunistic traders as everyone else**"
>
> "roughly **45% of all trades** originating from opportunistic traders, and **55%** from
> routine traders"

**Specification.**

1. **Lookback: three full calendar years** before the trade being classified.
2. **Admission:** classifiable only if the insider made **at least one trade in each** of those
   three years. An insider failing this is **neither routine nor opportunistic** - their trades
   fall outside the classified universe entirely.
3. **Routine:** traded in the **same calendar month** in each of the three prior years.
4. **Opportunistic:** classifiable, but not routine.
5. Classification is assigned **once**; "all subsequent trades that are made after we classify
   each insider" inherit it. It is not re-derived per trade.

> **GAP - what "a trade" means for the lookback is not stated in what was read.** Whether it is
> any Form 4 transaction or `P`/`S` only materially changes who is classifiable: an insider
> receiving an annual `A` grant every March looks routine on an any-transaction reading and is
> unclassifiable on a `P`/`S` reading. **The single most consequential ambiguity here.**

> **GAP - the admission filter is an event-rate problem, not a detail.** Requiring a trade in
> each of three prior years excludes every new insider, every infrequent trader, and every
> insider at a firm younger than three years. The paper reports the split of *classified* trades
> (45/55); **the share of the whole universe that is classifiable was not extracted.**
> `KILL-CONDITION.md` section 2 is stated in investable events per year, so this gap sits
> directly on a threshold.

> **GAP - gaps in the lookback.** An insider who traded in years 1 and 3 but not 2 is
> unclassifiable on a literal reading. Not stated in what was read.

---

## 3. Rule 10b5-1 exclusion

**The field**, verbatim from Form 4:

> "Check this box to indicate that a transaction was made pursuant to a contract, instruction
> or written plan that is intended to satisfy the affirmative defense conditions of Rule
> 10b5-1(c)"

And: "Provide the **date of adoption** of the Rule 10b5-1(c) plan in the **'Explanation of
Responses'** portion of the Form" - the adoption date is **free text**, not a structured field.

**When it became mandatory**, from the SEC's compliance guide:

> "Add a **new checkbox** to Forms 4 and 5 that **requires** a filer of either form to indicate
> whether a transaction reported on that form was made pursuant to a contract, instruction or
> written plan"
>
> "The amendments are **effective February 27, 2023**."
>
> "**Section 16 reporting persons** Filers will be required to comply with the amendments to
> Forms 4 and 5 for beneficial ownership reports **filed on or after April 1, 2023**."

| period | 10b5-1 status |
|---|---|
| before 2023-04-01 | **No structured field exists.** Identification only from free-text footnotes, filed voluntarily and inconsistently. |
| 2023-04-01 onward | Structured checkbox, **mandatory** on Forms 4 and 5. |

> **The largest single constraint in T3.** A 10b5-1-excluding classifier has structured data for
> **about 3.4 years**. **Every strand in `PRIORS.md` was estimated on samples predating the
> field** - CMP's closes 2007, Lakonishok & Lee's 1995, and Zhao's 2018-2024 straddles the
> change. Their handling of plan trades is inference from footnotes, or nothing.

> **A second structural break on the same date.** The same amendments require dispositions by
> **bona fide gift** to be reported on **Form 4 rather than Form 5**. Any series spanning
> 2023-04-01 has a discontinuity in `G` that is regulatory, not behavioural.

---

## 4. Role weighting

**The field.** Form 4 Item 6, "Relationship of Reporting Person(s) to Issuer", offers exactly
four boxes: **Director**, **Officer (give title below)**, **10% Owner**, **Other (specify
below)**. More than one may apply.

Instruction, verbatim: "If a reporting person is not an officer, director, or ten percent
holder, the person should check '**other**' in Item 6 and **describe the reason** for reporting
status in the space provided."

**Specification.** Role is a set of up to four flags, not a single value. **Officer title is
free text** - there is no controlled vocabulary for CEO, CFO or anything else.

**What the literature weights.** Lakonishok & Lee, verbatim: the predictive power of "**large
shareholders' trades is not robust over time**" across 1976-1985 and 1986-1995.

> **GAP - officer seniority is not a field.** Any CEO/CFO weighting requires parsing free-text
> titles, with no authoritative mapping, and no paper reached in T2 states how it was done.

> **GAP - the role the literature most doubts is the one cleanest to extract.** `10% Owner` is
> an unambiguous checkbox; the seniority distinctions that might matter are the free-text ones.

---

## 5. Filing lag

**The deadline**, verbatim:

> "This Form must be filed **before the end of the second business day** following the day on
> which a transaction resulting in a change in beneficial ownership has been executed"

**Specification.** `filing_lag = business_days(transaction_date -> filing_date)`; **late** when
it exceeds two business days. Requires a US market holiday calendar - business days are not
derivable from the filing alone.

**Code `V`** - "Transaction voluntarily reported earlier than required" - flags the opposite
case and is structured.

> **GAP - what the literature claims about lateness was not established.** T2 reached no
> peer-reviewed source on filing-lag informativeness. **Could not establish.**

> **A regime break, from CMP:** "nearly all of the trades in our sample were reported to the SEC
> within a few [days]". The two-business-day rule dates from Sarbanes-Oxley in 2002, so a sample
> beginning 1986 spans a far looser deadline. **A filing-lag study across that boundary measures
> a rule change as well as behaviour.**

---

## 6. Cluster definition

> **COULD NOT ESTABLISH.** T2 reached **no peer-reviewed source** defining a cluster buy - not
> the number of distinct insiders, not the window, not the role composition. The search returned
> vendor trackers and brokerage blogs.

**What Form 4 would support**, stated so the build cost is visible: grouping filings by issuer
and date window and counting **distinct reporting persons**. Distinctness needs a stable person
identifier across filings; the filing carries a reporting-person CIK, but whether that is stable
across issuers and name changes **was not verified from documentation in this session**.

**No cluster rule is specified here.** Any threshold chosen would be invented, and inventing a
threshold and then testing it is the failure mode `KILL-CONDITION.md` exists to prevent.

---

## 7. Size relative to existing holdings

**What Form 4 reports.** "**Beneficially Owned**" (7 occurrences) and "**Following Reported**"
(1) appear in the extracted instructions, so the form reports holdings **after** the reported
transaction. **Column number UNVERIFIED.**

Also present: **Direct (D) or Indirect (I)** ownership form, with "The nature of indirect
ownership shall be stated **as specifically as possible**; for example, 'By Self as Trustee for
X,' 'By Spouse,' 'By X Trust'" - free text.

**Specification.** `relative_size = shares_transacted / shares_owned_after`, computable from a
single filing. Prior holdings back out arithmetically.

> **GAP - the denominator is not the insider's economic stake.** Direct and indirect holdings are
> reported separately, indirect nature is free text, and derivatives sit in Table II. **"Size
> relative to holdings" is computable per filing, not per insider**, without aggregating across a
> person's filings - which returns to the identifier problem in section 6.

> **GAP - price.** For an exercise or conversion the instructions say "leave column 8 blank". A
> value-weighted scheme must handle blanks rather than assume them absent.

---

## Summary - what needs a second data source

`KILL-CONDITION.md` treats a rule that cannot be computed from the filing as a build cost the
gate is protecting against. These are those rules.

| requirement | Form 4 alone? | what else is needed |
|---|---|---|
| Open-market vs private purchase | **No** - `P` covers both | footnote parsing, or a second source |
| Officer seniority (CEO/CFO weighting) | **No** - free-text title | a title normalisation mapping |
| Business-day filing lag | **No** | a US market holiday calendar |
| Insider identity across filings | **Unverified** | a stable person identifier |
| Total economic stake | **No** - direct/indirect/derivative split | aggregation across filings |
| Market cap for a size screen | **No** | market data - **out of scope for this packet** |
| Abnormal return / benchmark | **No** | market data - **out of scope for this packet** |
| 10b5-1 status before 2023-04-01 | **No - the field did not exist** | nothing recovers it |
| Cluster parameters | n/a | **the literature, which was not reached** |

**Computable from Form 4 alone:** transaction-code filtering, the routine/opportunistic lookback
(given a resolved definition of "a trade"), role flags, 10b5-1 status **from 2023-04-01**,
calendar-day filing lag, and size relative to reported holdings **per filing**.
