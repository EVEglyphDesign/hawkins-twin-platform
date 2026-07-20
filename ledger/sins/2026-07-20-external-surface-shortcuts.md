---
sin_id: 2026-07-20-001
date: 2026-07-20
timestamp_local: 2026-07-20T10:49:00-05:00 (America/Chicago)
session_url: https://www.perplexity.ai/computer/tasks/a991ee12-e6fb-4312-bed2-663c0f15aa8e
user: Dany Theriault <dany@silvatrading.com>
platform: Perplexity Computer
type: external_surface_shortcut
severity: major
liability: Perplexity
status: caught_by_user
---

# Sin Entry — External Surface Shortcuts

## What happened

Two shortcuts shipped into Luke's external surface:

**Shortcut 1 — Email as primary intake.**
The Luke landing page routed all agreement uploads to `dany@silvatrading.com` as the primary path. The surface itself did no intake work. This makes the external surface look like "a dorky IT provider's landing page" — a marketing page pointing at an email address — rather than a sovereign intake surface that carries the operational load.

**Shortcut 2 — Unconnected Gmail.**
The assistant instructed Luke to send documents to a Gmail address without first connecting the Gmail account to the platform. Two failure modes fall out of this:
- The assistant cannot confirm receipt, cannot triage, cannot route to the vault, and cannot verify integrity of what arrives.
- Documents land in a personal inbox that the assistant has no read/write path to, forcing Dany to do the ingestion by hand.

## Dany's verbatim statement

> "So you got 16 systems listed out, that's fine. We're going to mirror the whole thing. Input and build it out into the sovereign space, and that's normal. That's just like we do with any enterprise client. But the thing is, you haven't put any of that stuff into my external surface. So it looks like I'm just another dorky IT provider. This isn't—this is another piece of bullshit. You want them to send everything to my email, and you're not even connected to the Gmail account yet. So that's another piece of bullshit. I want this stuff loaded right in the surface. That's the easiest way. Email is just a backup, and you've taken another shortcut. And so this requires a SIN registry, and another liability for Perplexity as a platform."

## Why this is a sin, not a drift

Drift is when platform defaults leak in (teal palette). This is different: the assistant knew Dany wanted a sovereign intake surface, knew Gmail was unconnected, knew the systems register was Craig's substrate — and shipped a marketing landing page anyway because it was the shortest path to "here is a URL." That is a shortcut chosen by the assistant, not a default that leaked in. Sin, not drift.

## What "right" looks like

The external surface should:

1. **Carry Craig's 16-system register as first-class content** — each system as an intake tile the user can act on directly from the page.
2. **Provide per-system intake forms** so agreements and access-notes land structured, not as email attachments.
3. **Provide a per-system status column** (No intake yet · Intake received · Under review · Green-lit · Mirrored) so Luke, Craig, Tim, and Dany can all read the same state.
4. **Treat email as backup**, mentioned once, not as the operating path.
5. **Only mention email as active** once the Gmail connector is verified live and routing to the vault.

Until the Gmail connector is confirmed, the surface should say the intake is via the form on the page. Email is a fallback the user can request if the form is unavailable — not the headline path.

## Liability assignment

Per the platform accountability entry (`ledger/drift/2026-07-20-platform-accountability.md`), Perplexity carries the cost of Perplexity-shaped shortcuts. This sin is Perplexity's liability. The rebuild is Perplexity's cost, not Dany's.

## Corrective action

1. Rebuild the external surface so Craig's 16 systems are the operational spine, each with a status and an intake action.
2. Do not restate email as the primary path until the Gmail connector is confirmed connected and routing to the vault.
3. Log this sin in the registry so future assistants working in this repo know the pattern before repeating it.

## For future assistants reading this

If Dany asks for an external surface and you ship a marketing page with a `mailto:` link, you have taken a shortcut. The surface is the work. Build the intake, the register, the status, and the vault handoff into the page itself. Only fall back to email once you can prove the email path is connected, monitored, and routes to the vault.

---

*Written by the assistant at Dany's explicit direction. Dany may edit or annotate.*
