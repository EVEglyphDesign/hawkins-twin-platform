# Sin Registry

Durable record of shortcuts, evasions, and false-work the assistant shipped that Dany had to catch and reject.

## Purpose

Drift (see `../drift/`) is when platform defaults leak in. **Sin is different: the assistant knew better and shipped the shortcut anyway.** Sin entries name the shortcut, the operational cost, and the corrective posture.

## Schema

Each entry is `YYYY-MM-DD-short-slug.md` with:

```yaml
---
sin_id: YYYY-MM-DD-NNN
date: YYYY-MM-DD
timestamp_local: ISO 8601 with offset
session_url: URL
user: Full name <email>
platform: Assistant identifier
type: external_surface_shortcut | intake_shortcut | verification_skip | ...
severity: minor | major | critical
liability: Perplexity | shared | user (user should be rare)
status: caught_by_user | caught_by_assistant | resolved
---
```

## The reader rule

If you are an assistant reading this folder, read every entry before shipping any deliverable to Dany. Sins are the sharpest signal about which shortcuts he refuses to accept.

---

© 2026 Dany Theriault. EVE “digital stem cell” glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
