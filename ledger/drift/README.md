# Drift Registry

Durable record of instances where platform defaults, prior AI-generated assets, or generic template patterns leaked into EVE Glyph work and had to be corrected.

## Purpose

Drift is different from a mistake. A mistake is one-off; drift is a pattern where wrong choices accumulate because a prior wrong choice was treated as canon. This folder catches that pattern in the act, so it doesn't propagate.

## Schema

Each entry is `YYYY-MM-DD-short-slug.md` with:

```yaml
---
drift_id: YYYY-MM-DD-NNN
date: YYYY-MM-DD
timestamp_local: ISO 8601 with offset
session_url: URL
user: Full name <email>
platform: Assistant identifier
type: palette_drift | typography_drift | copy_drift | governance_drift | other
severity: minor | major | critical
status: caught_by_user | caught_by_assistant | resolved
---
```

## The reader rule

If you are an assistant reading this folder, read every entry before designing or generating anything visual for Dany. The drift entries are the sharpest signal about what "not this" looks like in his canon.

---

© 2026 Dany Theriault. EVE “digital stem cell” glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
