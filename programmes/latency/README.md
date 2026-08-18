# programmes/latency - ACTIVE, not yet started

Family 1 of `ROADMAP.md`. **Nothing has been measured yet.** This directory exists because Phase A
built the structure; Phase B fills it.

## The claim, stated before any data

A market resolves to a named public page. The price updates when traders notice. We act when the
source publishes. **This is not a forecasting claim** - the edge is tens of cents against a hurdle
of a few, rather than a few basis points against it.

## What has to be answered first, in order

1. **Does the raw material exist?** How many open markets resolve to a *named single official page
   or feed* - not "credible reporting", not "official but requiring interpretation". **Report count
   and notional.** A hundred markets worth $200 each is not a business. This is the gating number
   for the whole family and it should be known in week one.
2. **What does the source layer look like?** Per source class: change detection, permissible polling
   cadence under terms and robots.txt, false-positive rate, and **measured latency from publication
   to first meaningful price move**. That last number is what the family lives on.
3. **Alert-only. No auto-fire. No capital.**

## The prior to hold, from H61

A real, replicable effect can belong entirely to whoever is fastest. H61 returned **+4.99c
out-of-sample on 644 held-out events** and was worth nothing, because the ask moved 5c against the
buyer within three minutes. **The question is not whether a gap exists** - it is whether it is wide
enough and lasts long enough that polling without co-location can act inside it.

## The kill criterion, to be sealed before events accumulate

After **50 detected events**, if median detection-to-first-price-move is **under 10 seconds**, this
family closes in this form and falls back to the long tail of obscure markets. Stated in advance so
the fallback cannot be invented later to rescue a null.

## Infrastructure it inherits rather than builds

The durable write path, R2, `lib/gh_commit.py`, and the scheduled-probe-with-control-pair pattern.
**Standing limit:** census-scale scheduled measurement is established; **bulk collection from CI is
unmeasured**, and a shared runner IP's rate-limit history is set by strangers and is not observable.

Add a scheduled probe with a separating control pair to **every** external dependency this family
acquires. It does not prevent a source stopping. It **dates** the stop.
