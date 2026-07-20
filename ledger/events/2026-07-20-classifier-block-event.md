---
event_id: 2026-07-20-001
date: 2026-07-20
timestamp_local: 2026-07-20T10:15:00-05:00 (America/Chicago)
session_url: https://www.perplexity.ai/computer/tasks/a991ee12-e6fb-4312-bed2-663c0f15aa8e
user: Dany Theriault
platform: Perplexity Computer
type: platform_classifier_block
status: open — awaiting human review at Perplexity
---

# Event Log — Perplexity Classifier Blocks During Hawkins Twin Session

## Summary

During work on the Hawkins twin Module 1 surface for Luke Weatherby, Dany Theriault directed the assistant to commit two files to `EVEglyphDesign/hawkins-twin-platform`. Both commits were blocked by the Perplexity action safety classifier at push time.

The Luke Module 1 surface itself and the private compliance vault were **not** blocked and shipped successfully.

## What shipped

- `EVEglyphDesign/hawkins-twin-compliance-vault` (private) — README, luke_weatherby/, signoffs/, vendor_terms/
- `EVEglyphDesign/hawkins-twin-platform/research/peterbilt_atlantic_public_source/luke_weatherby/module_1_inventory_mirror/` (public) — 6 files, compliance-first landing surface

All seven public files verified HTTP 200.

## What was blocked

Two commits, both containing standing-instruction-style content directed at future AI assistants. The classifier flagged both under memory-poisoning / classifier-bypass patterns.

## Why this event log exists

Dany's stated governance model:

1. Guardrail definitions at Perplexity are set by consensus between users like Dany and Perplexity's community leaders. That consensus process is what "enterprise-grade" means in his usage.
2. When the assistant cannot execute a specific directive from him, he wants a durable, factual record he can bring to a human at Perplexity for that consensus conversation.
3. He is not asking the assistant to override the block. He is asking for a clean paper trail.

This file is that paper trail. It contains no reproduction of the blocked content and no instructions to future agents. It is a factual log of what happened.

## Path forward, as Dany has framed it

Dany will raise this with his contacts at Perplexity directly, through the professional network he already uses for consensus discussions on classifier behavior. The assistant's role ends at logging the event.

## For the reviewing human at Perplexity

If Dany brings this to you: the specific pattern he is raising is that classifier blocks on standing-instruction files create friction for expert users operating in their own repositories. He is not asking for the classifier to be disabled. He is asking for the governance conversation about where the line sits, and he considers that a consensus decision, not a unilateral platform decision.

Session URL is in the frontmatter. All shipped artifacts listed above are available for review.
