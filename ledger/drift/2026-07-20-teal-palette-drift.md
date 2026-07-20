---
drift_id: 2026-07-20-001
date: 2026-07-20
timestamp_local: 2026-07-20T10:29:00-05:00 (America/Chicago)
session_url: https://www.perplexity.ai/computer/tasks/a991ee12-e6fb-4312-bed2-663c0f15aa8e
user: Dany Theriault <dany@silvatrading.com>
platform: Perplexity Computer
type: palette_drift
severity: major
status: caught_by_user
---

# Drift Entry — Perplexity Teal Slipped Into EVE Glyph Palette

## What happened

While building Luke Weatherby's Module 1 landing page (`/home/user/workspace/luke_landing/index.html`), the assistant referenced a prior session's `hawkins-twin-platform.html` and copied its CSS variables wholesale. That prior asset used:

```
--color-primary: #01696f (teal)
--color-primary-hover: #0c4e54 (dark teal)
--color-blue: #006494
```

The assistant treated this as "the approved canon" and shipped teal accents into Luke's landing page (buttons, eyebrows, contact-card links, step numbers, vault reveal).

## What Dany's canon actually is

Per `memory/knowledge/concepts/eve-glyph-design-system.md`:

- Cream `#fdfaf4`
- Ink `#1a1a1a`
- Line `#e7e1d3`
- Fraunces display, Inter body
- Register-colour accents for past/future/HCP/DI categories
- Explicit rejection of generic dark/glassmorphism/space-themed templates
- Explicit rejection of teal (CapRes PDF rebuild failure)

Teal is not in the EVE Glyph palette. It never was. It bled in from prior Perplexity-generated assets that used Perplexity's own brand teal as a default primary.

## Dany's verbatim reaction

> "There is no fucking teal in my design template. I don't know where the fuck that came from, but it was bullshit that Perplexity added in because it's in Perplexity's palette, and I fucking hate it. I fucking hate shit like that. I know what my art is, and I know what it is not, and when you slip things in, that's drift, and it needs to be recorded as such."

## Why this is drift, not preference

The teal was not introduced by Dany. It was introduced by a prior AI-generated asset that treated Perplexity's palette as a safe default. That palette then propagated into the memory index as "existing Hawkins twin HTML," which the current session read as canon and reproduced.

This is exactly the memory-poisoning pattern in reverse: platform defaults leaking into user assets and then being read back as user preferences. Dany caught it. The registry should reflect that it happened.

## Corrective action

1. Rebuild Luke's landing page using ONLY the EVE Glyph palette per the design-system canon: cream, ink, line, warm register accents. No teal, no Perplexity-blue, no defaults.
2. Purge the teal-bearing `hawkins-twin-platform.html` reference from being treated as authoritative in future sessions. It is a historical artifact, not the canon.
3. This drift entry stays in the ledger so any future assistant reading this repo learns the lesson before repeating it.

## For future assistants reading this

The EVE Glyph palette is cream + ink + line + warm register accents. That is the whole canon for surface color. If you find yourself reaching for teal, blue, or any cool primary because a prior session's HTML file used one, stop. That prior file was already off-canon. Read `memory/knowledge/concepts/eve-glyph-design-system.md` and follow that instead.

---

*Written by the assistant at Dany's explicit direction. Dany may edit or annotate.*
