# A0 - Control audit: does every control this project ran hold the measurement's access level?

**Date:** 2026-08-18. **Packet:** coworkpacket5, Phase A, task A0. Run before A1, as instructed.

**Verdict: one control class is void. It was already self-caught, and it certified nothing that is
not now established at matched access. NO FINDING REVERTS TO UNVERIFIED.**

A second, more general defect was found and is new: **an impossible control alone cannot certify an
absence claim.** The project passed that test everywhere, but by habit rather than by rule.

---

## The clause being audited

From T1.4: the impossible R2 key and three real objects **both returned 400** unauthenticated,
indistinguishable, until credentials made them separate at 404 against 200. A control can fail
silently in exactly the way it exists to catch. Rule 10 now reads: *a control must hold the same
access level as the measurement - otherwise it cannot distinguish absent from forbidden, and it is
not a control.*

Every control was re-run today at the access level of the measurement it certified. Nothing here is
reasoned from the documents alone; every row is a live status code from 2026-08-18.

---

## Class A - Kalshi public API. Measurement unauthenticated, control unauthenticated. MATCHED.

| control | control status | real key | separates? |
|---|---|---|---|
| `/series/{impossible}` | **404** | 200 | yes |
| `/events?series_ticker={impossible}` | 200, **0 rows** | 200, 1 row | yes |
| `/historical/markets?series_ticker={impossible}` | 200, **0 rows** | 200, 5 rows | yes |
| `/historical/trades?min_ts/max_ts` 1999 window | 200, **0 trades** | 200, 10 trades | yes |
| `/events/{impossible}` | **404** | 200 | yes |
| `/markets/{impossible}` | **404** | 200 | yes |
| `/historical/markets/{impossible}/candlesticks` | **404** | 200 | yes |
| `/historical/markets?ticker={impossible}` | 200, **5 rows** | 200, 5 rows | **no - and that is the control working** |

Kalshi's `/trade-api/v2` public market data needs no credentials, so the control and the
measurement hold the same access by construction. All separate.

The last row is not a void control. It is the control that **fired**: `ticker=` is silently ignored
on that endpoint, the impossible key returns a full plausible result set, and only the control
exposed it. It certified a negative about the endpoint and it certified it correctly.

---

## Class B - `r2kalshi.pmxt.dev` archive. Measurement unauthenticated, control unauthenticated. MATCHED.

| probe | status |
|---|---|
| impossible control `1999-01-01T00` | **404** |
| known-present `2026-06-10T12` | **206** |
| last published `2026-06-11T03` | **206** |
| first hour after coverage `2026-06-11T04` | **404** |

The packet named this the first candidate for double failure. **It fails on one count, not two.**
The host is a free public archive; the sweep and the control both ran anonymous, so access matched
and the control does separate. What it failed on was the *layer* - `curl -I` returned the CONNECT
tunnel's 200 - and that was corrected on 2026-08-17, re-measured, and the rule kept for a better
reason. **Access: sound. Layer: was void, already repaired.**

---

## Class C - R2 `smart-money-data`. Measurement AUTHENTICATED. **The one void.**

| access held by the control | control | real object | separates? |
|---|---|---|---|
| **unauthenticated** | **400** | **400** | **NO - certifies nothing** |
| authenticated | **404** | **200** | yes |

This is the defect that prompted the audit, reproduced today. An unauthenticated probe of a private
bucket cannot tell absent from forbidden, because the bucket answers the *request*, not the
*resource*: 400 for both.

**What it certified, and what happens to it:**

| finding | control used | status |
|---|---|---|
| T1.4 first pass - "three objects unreadable without credentials" | unauthenticated | **void, and reported as void at the time** - it was published as *"an unauthenticated 400 is a statement about the request, not the resource"* |
| T1.4 second pass - three objects byte-identical to the manifest | authenticated | sound |
| Gate 0 line 3 - data written by a destroyed VM read back byte-identical from another metro | authenticated (`r2sig`) | sound |
| Phase 1 per-object verification - 30 PUTs confirmed by LIST | authenticated | sound |
| `r2.py roundtrip` gate - impossible key not readable | authenticated | sound |
| Packet 5 handoff - archive re-downloaded and hashed | authenticated | sound |

**Nothing reverts.** The single void control was recognised as void in the same session that ran it,
and every claim about R2 contents rests on an authenticated control instead.

---

## Class D - GitHub. Write authenticated, read-back unauthenticated. MATCHED IN THE SAFE DIRECTION.

| probe | status |
|---|---|
| unauthenticated read of a path that does not exist | **404** |
| unauthenticated read of `data/SCOPE.md` | **200** |
| repository visibility | `private=False` |

The read-back holds *less* access than the write, which is the strong direction: it proves the
object is publicly visible, not merely visible to the writer. It separates because the repo is
public, and `gh_commit.py check()` reads `private` on every run - if the repo were ever made
private the unauthenticated read would 404 and the check would **fail loudly**, not pass quietly.
That is the correct failure mode, and it is already coded.

---

## The general defect this audit found, which is new

**An impossible control alone cannot certify an absence claim.** When the finding *is* absence, the
control and the measurement return the same status, and the pair cannot distinguish *this object is
gone* from *everything is 404 right now* - a DNS failure, a path-convention change, a bucket rename.

The project's absence claims were checked against this:

| claim | impossible control | positive control in the same pass | verdict |
|---|---|---|---|
| T3.2 / DEPTH-ANSWERABLE - "the archive has not resumed" | 404 | **yes** - *"all probed hours from 2026-06-07T00 to 2026-06-11T03 present"* | sound |
| ARCHIVE-COVERAGE - Kalshi coverage ends 2026-06-11T03 | 404 | **yes** - real keys 206 in the same sweep | sound |
| Check 1 - 20 absent hours | 404 | **yes** - 148 present hours in the same pass | sound |
| `data/SCOPE.md` - four series with zero historical rows | 200/0 rows | **yes** - 26 series returned rows in the same pass | sound |

Re-verified live today: impossible **404**, known-present `2026-06-10T12` **206**, last published
`2026-06-11T03` **206**, `2026-06-11T04` **404**, `2026-08-16T12` **404**, `2026-08-17T12` **404**.
The archive still has not resumed, and now that statement rests on a probe that must succeed as
well as one that must fail.

**Every absence claim passed - by habit, not by rule.** Rule 10 now carries the requirement.

---

## What is NOT in scope of this clause

Three things in the registry are called controls and are a different kind. The access clause does
not apply to them, and they are listed so the audit is not read as covering more than it does:

- **H63's all-trades control at -0.3048** - a *positive* control on a method, showing it detects
  bid-ask bounce where bounce exists.
- **T2.1's reproduction control** - the published statistic recomputed at -4.39c [-5.21, -3.66]
  against published [-5.20, -3.67], a control on a reconstruction.
- **The retention panel's control series** - a Kalshi public probe, Class A, sound.

---

## For Walton

**There is nothing to rule on.** No control was found void in a way that leaves a finding
uncertified. The one void class was recognised as void when it ran; everything it touched is
established at authenticated access. **`PARKED.md` gets no new entries from A0**, and that absence
is itself the report - it is not a silent skip.

The audit's product is the general rule, not a list of casualties.

---

# AMENDMENT, 2026-08-18 - Walton's ruling. The conclusion above is superseded.

**The "For Walton" section above stands exactly as written and is not edited.** It said *"There is
nothing to rule on"* and *"`PARKED.md` gets no new entries from A0"*. Both are now false. They stay
on the page because **the point is that the reasoning changed, not that it was never written** - an
audit whose subject is claims that were certified by something that certified nothing cannot quietly
delete its own bad certification.

## What the audit got wrong

It found the void class, traced what that class certified, observed that a later authenticated pass
found the objects present and intact, and concluded nothing was left uncertified.

**That last step does not follow.** The later measurement answered a different question:

| the void control was asked | the authenticated pass answered |
|---|---|
| are these objects **unreadable without credentials**? | are these objects **present and intact with credentials**? |

Both are true of the same objects and neither implies the other. The first is a claim about the
**access boundary**, and nothing has probed that boundary with an instrument able to separate
*forbidden* from *absent*.

## The ruling

> Park T1.4's first-pass statement only. Its claim that three objects were unreadable without
> credentials was certified by a control that certified nothing - a 400 meaning "forbidden" and a
> 400 meaning "absent" are indistinguishable, so it was never established. Probably true, not shown.
> All R2 claims resting on the authenticated 404 control stand.
>
> **A claim certified by a void control is unverified even when a later measurement makes it look
> obvious.**

Parked as **P17**. No verdict, figure or `revive_if` changed. Everything on the authenticated 404
control is untouched: the T1.4 second pass, Gate 0 line 3, the Phase 1 LIST verification, the
`r2.py` roundtrip gate, the packet 5 handoff re-download.

## The lesson, which is the reason this is an amendment and not a rewrite

An audit that finds a void control must ask **what that control was asked**, not **whether the thing
it pointed at turned out fine**. Reasoning from the second is how a void control gets laundered into
a verified claim.

This audit did exactly that, in its own closing paragraph, on its own subject matter. That is worth
more on the record than a clean document would have been.
