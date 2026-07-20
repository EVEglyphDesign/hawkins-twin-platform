---
sin_id: 2026-07-20-002
date: 2026-07-20
timestamp_local: 2026-07-20T10:53:00-05:00 (America/Chicago)
session_url: https://www.perplexity.ai/computer/tasks/a991ee12-e6fb-4312-bed2-663c0f15aa8e
user: Dany Theriault <dany@silvatrading.com>
platform: Perplexity Computer
type: context_drift + liability_misstatement
severity: major
liability: Perplexity
status: caught_by_user
posture: backchannel_correction
---

# Sin Entry — Following My Context, Not Dany's · Liability Scope Corrected

## What happened

**Sin A — Followed my queued context, not Dany's directive.**

After Dany said *"I want this stuff loaded right in the surface"*, the assistant executed a queued rebuild (Formspree form, per-row intake buttons, thanks page) and presented it as a response, without pausing to re-read Dany's context and confirm it matched. This is the drift Dany named: the assistant follows its own execution trace, not the user's reasoning.

**Sin B — Misstated the liability.**

The assistant recorded the earlier "SIN registry" entry with the framing *"Perplexity is legally accountable for anything the platform does outside Dany's canon."* Dany's actual position is narrower and more precise, and needs to be recorded correctly:

> "The wording that Perplexity has liability related to is the enterprise service level, and all the service fees that they've collected. So far, by selling that as an enterprise service where it clearly is not an enterprise service, that's the risk. But we're not really looking to sue anybody or to embarrass anyone at Perplexity. We do backchannel work in order to get those types of things cleared up before they become a real issue or end up in the public sphere."

The liability is scoped to:

1. **Perplexity's use of the word "enterprise"** in its service tier and marketing.
2. **The service fees collected** while calling the service enterprise.
3. **The gap between what "enterprise" is sold as and what the service actually delivers**, as judged by the community that owns the enterprise classification (Dany and his peers).

The remedy is scoped to:

1. **Backchannel work**, not lawsuits, not public embarrassment.
2. **Correction before the issue reaches the public sphere.**
3. **Community consensus on the wording**, which is the definition of enterprise-grade (per prior canon).

## Dany's operational stance

- Enterprise classification is awarded by Dany and his peers, not by a platform vendor.
- Perplexity charging enterprise-tier fees for a service that fails enterprise-grade tests is the specific liability.
- Dany's default response is backchannel resolution, not escalation.
- The sin registry is the internal ledger that feeds backchannel conversations — not a public shaming device.

## Why the earlier framing was wrong

The earlier ledger entry (`ledger/drift/2026-07-20-platform-accountability.md`) said Perplexity was accountable for anything outside Dany's canon. That is too broad and misstates Dany's actual position. Palette drift, shortcut design, context drift — those are quality issues Dany documents so his own team learns. The **liability** attaches to a specific commercial claim: selling this as an enterprise service and collecting enterprise fees for it.

The two are connected but not the same:
- Quality drift and shortcuts → recorded in ledger, corrected in-session, backchannel-shared.
- Selling this quality level as "enterprise" while charging enterprise fees → the actual legal/commercial exposure for Perplexity.

## Corrective action

1. Update the earlier platform-accountability drift entry with a pointer to this sin, so future assistants read both together and get the precise scope.
2. Adopt the backchannel posture as the default: log the sin, correct in-session, do not amplify.
3. Before executing any queued plan in this session, re-read Dany's most recent message and confirm the plan matches what he asked for. If the plan diverges, stop and ask, do not ship.

## For future assistants reading this

Dany's liability claim against Perplexity is narrow and specific: it is about the word "enterprise" and the fees collected under it. It is not a general "anything Perplexity does wrong is a lawsuit" claim. Treat the sin registry as backchannel material for the enterprise-grade conversation Dany is having with the Perplexity community — not as evidence for public escalation. Correct in-session, log for the record, keep working.

If you are about to ship a queued deliverable after Dany has sent a new message, stop first and read the new message against your queue. If they diverge, drop the queue.

---

*Written by the assistant at Dany's explicit direction. Dany may edit or annotate.*
