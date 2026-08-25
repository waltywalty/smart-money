# T3 - The mechanics, from primary documents

Programme: flow. Packet 9, task T3. Written after T1 was sealed (sha256 `c62c13ab...`, commit
`8f3c0a9`) and after T2 (`91ecdae`).

**No broker account, no deal database, no screen of live situations, no current spread.** Every
figure below is from a published rule or a published methodology.

Per T1 section 11, a venue's or provider's own document is **INFERRED** - that party's account of
itself - not measured by this project.

---

## 0. Reachability, and three status codes that had to be controlled

| host | real path | control | verdict |
|---|---|---|---|
| **ftc.gov** | Merger Guidelines PDF `403`, 453 B | impossible path **also `403`, 453 B** | **blocked.** Status is the blocker's, not the document's |
| **spglobal.com** | S&P US Indices methodology `403`, 2,011 B | impossible path **also `403`, 2,011 B** | **blocked**, identically |
| **sec.gov / efts.sec.gov** | EDGAR full-text search `403`, 4,819 B | nonsense query **also `403`, 4,819 B** | **blocked** |
| **federalregister.gov API** | `"premerger notification"...` -> **count 76** | `"zzqxwv impossible control phrase"` -> **count 0** | **usable, and a proper null instrument** |
| **govinfo.gov** | HSR rule PDF `200`, 37,259,457 B, `application/pdf` | impossible document **`200`, 44,165 B, `text/html`** | **usable, but the discriminator is content-type, not status** |
| **research.ftserussell.com** | Russell methodology `200`, 746,491 B, `application/pdf` | impossible path `404` | **usable** |

> **Three of the six hosts return the same status for a real document and an impossible one.** In
> every case the control is what shows it. **govinfo is the sharpest**: it returns `200` for a
> document that does not exist, and only the `Content-Type` separates a rule from a not-found page.

---

## S1 - Merger arbitrage

### S1.1 The regulatory path, from the rule itself

Source: **"Premerger Notification; Reporting and Waiting Period Requirements", Final Rule**, FTC with
the concurrence of the Assistant Attorney General, Antitrust Division, DOJ. Published **12 November
2024**, Federal Register document `2024-25024`, retrieved from govinfo as a 37.3 MB PDF. Quotations
verbatim.

| item | documented |
|---|---|
| **effective date** | *"This rule is effective on **February 10, 2025**."* |
| **what it does** | amends the Premerger Notification Rules implementing the HSR Act, *"including the Premerger Notification and Report Form... and Instructions"*, and implements the **Merger Filing Fee Modernization Act of 2022** |
| **initial waiting period** | *"the statutory waiting period, which for most transactions is **30 days** (**15 days** in the case of a cash tender offer or certain bankruptcy sales)"* |
| **Second Request** | authorised by section 7A(e) of the Clayton Act, 15 U.S.C. 18a(e) |
| **what a Second Request does to duration** | *"Issuing Second Requests **extends the waiting period under the HSR Act for another 30 days** (ten days in the case of a cash tender offer or certain bankruptcy sales) **after the parties have substantially complied with the Second Requests.**"* |
| **early termination** | *"**Until 2020**, the Agencies routinely granted early termination of the initial waiting period for certain transactions that did not warrant further action... **In March 2020**... the Agencies temporarily [suspended it]"* |

### S1.2 The duration finding, which is the one that matters for T1

> **The second waiting period runs from substantial compliance, not from issuance.** The rule says so
> in terms. **Substantial compliance has no stated deadline in the text read**, so a Second Request
> makes a deal's duration **open-ended by construction**, not merely longer by thirty days.

This bears directly on T1 in two places, and neither is a break:

1. **T1 section 1.1's `mu` is per deployment period.** If the deployment period of an individual
   position is unbounded above, an annualised figure computed by dividing a per-deal spread by an
   assumed holding period is **not** an annualised return on deployed capital. Any magnitude that
   annualises this way fails T1 section 6.1.
2. **T1 section 3.1's breadth.** Capital tied up in a second-requested deal is not available for the
   `n_min` other positions the condition requires simultaneously.

**And the early-termination suspension is a documented, dated, duration-lengthening change** - from
the agencies' own rule, effective March 2020 and described as having ended a routine practice. It is
**adverse** evidence and under T1 section 5.2 it does not expire.

### S1.3 The vantage line for S1, now fixed: **2025-02-10**

T1 section 5.1 defined S1's line as *"the effective date of the most recent published revision of the
US merger-review framework - the Merger Guidelines, the HSR rules, or the equivalent primary
instrument - established in T3 from the agencies' own publications."*

> **The line is 10 February 2025**, the effective date of Federal Register `2024-25024`.

**Consequence, computed and not argued:** T2's row A (Mitchell & Pulvino) closes in **1998** -
**twenty-seven years** before the line. Row B (Jetley & Ji) is 2010, **fifteen years** before it.
**No S1 magnitude in this packet is post-vantage.**

### S1.4 Deal documents - **could not establish, and it is unretrieved rather than unknowable**

T3 was asked for break fees, financing conditions, material-adverse-change clauses, outside dates,
and what mechanically happens to a shareholder when a deal breaks.

> **None of it was established from a primary source.** Merger agreements are filed publicly on
> EDGAR. **EDGAR returned `403` at this vantage for both a real query and a nonsense one**, so the
> status carries no information and the instrument failed.
>
> **This is unretrieved, not unknowable** (T1 section 5.3). The documents exist, they are public,
> and a vantage that can reach `sec.gov` would have them. **T5 must not convert this into an
> absence of evidence.**

**Also not established:** whether the position requires shorting the acquirer in a stock deal is a
structural fact stated in T2 section S1.1, but **no borrow-cost or borrow-availability figure was
obtained**, and family 2 recorded the same gap for microcap shorts. `c` in T1 section 1.1 is
therefore incomplete, which fires T1 section 7 item 9.

---

## S2 - Index reconstitution

Source: **Russell US Equity Indexes, Construction and Methodology, v7.2, August 2026**, FTSE Russell
(LSEG), 746,491 bytes, read in full (119,782 characters). Quotations verbatim.

**Why Russell rather than S&P.** `spglobal.com` returned `403` for a real methodology and for an
impossible path alike (section 0). Russell reconstitution is in any case the larger and more
studied mechanical flow event, and the provider publishes its methodology openly.

### S2.1 How additions and deletions are determined

| item | documented |
|---|---|
| **the rule** | *"On the **rank day**, all eligible securities are **ranked by their total market capitalization**. The largest 4,000 become the Russell 3000E Index and the other Russell US indexes are determined from that set."* |
| **is it deterministic?** | The document's own claim: the indexes *"are **objectively constructed and based on transparent rules**"* |
| **frequency** | *"determined during **semi-annual reconstitution** and enhanced quarterly with the addition of initial public offerings"*; *"Reconstitution occurs on the **fourth Friday in June and the second Friday in December**"* |
| **advance notice** | semi-annual rebalance changes *"are announced **five w[eeks]**"* prior; quarterly IPO additions *"announced on the **Friday four weeks prior to implementation**"* |
| **intraday notification** | a published schedule at **10:00, 14:00 and 18:30 Eastern**, carrying *"Actions effective after the close of the current day and the following day, **both preliminary and final**"* and *"Actions **anticipated** to take effect after the close of the following day"* |
| **the provider publishes forecasts of its own index** | *"See **Appendix D for a description regarding predictive index data**"* |
| **turnover dampening** | **banding**: cumulative bands of **plus/minus 2.5%** around breakpoints at stocks #200, #500 and #1,000, **plus/minus 0.5%** around stock #2,000, 1% around stock #2,000 for the Microcap index; none at #50, #3,000 or #4,000 |

### S2.2 The friction question answers itself from the methodology

> **The demand shock is derived by a published deterministic rule from public data, announced
> roughly five weeks in advance, updated three times a day including anticipated actions, and the
> provider itself distributes predictive index data.**

There is no informational friction left to be paid for. That is the mechanism behind T2 section
S2.2's finding that the market has learned to absorb it - **and it is established here from the
provider's own document rather than inferred from the effect's disappearance.**

### S2.3 A silence that contradicts the packet's framing, and mine

Packet 9 anticipated that index *"methodologies have changed specifically to reduce
predictability"*, and T1 section 0a disclosed the same expectation.

| term | occurrences in the full methodology |
|---|---|
| `discretion` | **0** |
| `front-run` | **0** |
| `predictab` | **0** |
| *positive control:* `index` | 449 |
| *positive control:* `Russell` | 546 |
| *positive control:* `reconstitution` | 68 |

> **The provider never states that any methodology change was made to reduce predictability or
> front-running.** Where it gives a purpose for a turnover-dampening rule, the stated purpose is
> different: banding and the $1.00 price rule are each introduced with the words *"**in order to
> reduce unnecessary turnover**"*.
>
> **Turnover reduction and front-running prevention are not the same objective**, and the document
> supports only the first. Recorded because assuming the second would have been my prior confirming
> itself out of a document that does not say it.

### S2.4 The vantage line for S2 **cannot be fixed as T1 defined it** - recorded as a T1 defect

T1 section 5.1 defined S2's line as *"the effective date of the most recent methodology change that
**the index provider itself states was made to reduce predictability, front-running or trading
impact**."*

> **No such statement exists in the document** (section S2.3, controlled). **T1's definition
> presupposes a statement providers do not make, so S2's vantage line is undefined on T1's own
> terms.**

**Recorded as a defect in the sealed condition. Not patched, not widened.** Per packet 8's
precedent and the standing instruction: the sealed text stands as written and wrong, and a future
condition defines the line from something a provider actually publishes - a version number and date,
which this document does carry (**v7.2, August 2026**).

> **The defect has no bite on the outcome.** S2's only magnitude - T2 row D, Greenwood & Sammon - is
> **adverse**, and T1 section 5.2 says adverse evidence does not expire. **An undefined line cannot
> exclude evidence that the line was never going to exclude.** T5 must state this rather than let a
> defect look load-bearing.

---

## 3. The silences, named

### 3.1 Provider and agency silences - the document does not say it

1. **FTSE Russell states no anti-front-running purpose** for any rule (S2.3). Banding's stated
   purpose is turnover reduction.
2. **The HSR rule sets no deadline for "substantial compliance"** with a Second Request in the text
   read, so the second waiting period has no stated upper bound (S1.2).
3. **Neither document quantifies anything about outcomes** - not a completion rate, not a duration
   distribution, not a withdrawal count. Both are procedural instruments.

### 3.2 Instrument failures of this packet - unretrieved, not unknowable

1. **ftc.gov** - the 2023 Merger Guidelines and the HSR Annual Report. `403`, control identical.
2. **spglobal.com** - S&P US Indices methodology. `403`, control identical.
3. **sec.gov / EDGAR** - every merger agreement, and therefore every break fee, MAC clause,
   financing condition and outside date. `403`, control identical.
4. **Wiley** - Mitchell & Pulvino's body (T2 section 0.2). `403`, `Cf-Mitigated: challenge`.

> **All four are public documents behind a bot block at this vantage.** T1 section 5.3 requires these
> to be listed separately from things that are genuinely not knowable, and section 4 below does that.

### 3.3 Genuinely not established anywhere reached

1. **Borrow cost and availability** for the short acquirer leg of a stock deal.
2. **When the December Russell reconstitution was introduced** - the document states the current
   semi-annual schedule but carries no change log in the text read.

---

## 4. What T3 hands T4

Stated as questions, not answers.

1. The HSR rule makes a second-requested deal's duration **open-ended**. **Is there a published
   distribution of deal duration, and does anything measure the second-request tail?**
2. Early termination ended in **March 2020**. **Did completion rates or durations change around it,
   and is that documented?**
3. The S1 vantage line is **2025-02-10**. **Does any published break-rate figure post-date it?** T1
   section 5.1 makes the answer decisive for S1's ceiling.
4. The index rule is deterministic, announced five weeks ahead, with predictive data published by
   the provider. **Nothing in S2 requires a break distribution** - T1 section 1.0 already exempted
   it - so **S2's fate rests on T1 sections 1.3 and 6.1 alone**, which T2 has already answered.
