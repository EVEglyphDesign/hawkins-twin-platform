# Hawkins Twin Intake Router — Specification

**Status:** Design specification. The surface-side (composer) is live. The server-side router is scheduled but not yet running against the sovereign Gmail inbox — that step turns on next.

## Purpose

Route intake messages sent from the Luke landing page directly from the sovereign Gmail account into the private compliance vault repo, without any third-party form vendor in the middle.

## Flow

```
Luke fills form on /luke/
        │
        ▼
Composer builds tagged message + opens Luke's mail client
        │
        ▼
Luke attaches documents and sends
        │
        ▼
Message lands in dany@silvatrading.com (sovereign Gmail, connected as gcal)
        │
        ▼
Intake router (scheduled) reads new [HAWKINS-INTAKE] mail
        │
        ├── parses header block (intake_id, system, kind, submitter, timestamp)
        ├── writes structured record to hawkins-twin-compliance-vault/intake/{intake_id}/
        │       ├── meta.yml       (parsed header block)
        │       ├── notes.md       (user-provided notes)
        │       └── attachments/   (all attachments, filenames preserved)
        ├── updates hawkins-twin-compliance-vault/intake/_index.md (append row)
        └── replies to Luke: "Intake IN-... on file"
```

## Message envelope

The composer produces messages with a fixed, machine-parseable shape.

**Subject:**
```
[HAWKINS-INTAKE] <System Name> · <Kind> · <Intake ID>
```

**Body header block (verbatim, do not modify):**
```
--- HAWKINS TWIN INTAKE ---
intake_id: IN-YYYYMMDDHHMM-xxxx
system: <System Name>
kind: <Kind>
submitted_by: <Name> <email>
submitted_at: <ISO 8601 timestamp>
--- NOTES ---
<free-form user notes>

--- INSTRUCTIONS ---
<static instructions to the sender>
```

The router uses the `[HAWKINS-INTAKE]` subject prefix as the filter and the `--- HAWKINS TWIN INTAKE ---` line as the parse anchor.

## Router behaviour (server-side)

Runs on a schedule (initial: every 15 minutes). Uses the `gcal` connector's `search_email` to find new mail matching `subject:[HAWKINS-INTAKE] is:unread`.

For each match:

1. Parse the header block. Fail-closed if the block is missing or malformed — do not attempt heuristics.
2. Create `hawkins-twin-compliance-vault/intake/<intake_id>/` in the private vault.
3. Write `meta.yml` with parsed fields.
4. Write `notes.md` with the free-form notes section.
5. Write each attachment into `attachments/` preserving original filename; if a filename collides with an existing file, suffix with `-01`, `-02`, etc.
6. Append a row to `intake/_index.md`:
   ```
   | Intake ID | System | Kind | Submitter | Received | Status |
   | IN-... | ... | ... | ... | ... | Received |
   ```
7. Send a reply to the submitter using `draft_email` → `send_email`:
   > Your intake `<intake_id>` is on file. Dany Theriault and Tim Hawkins will review it and follow up with a plain-English sign-off on next steps. You do not need to do anything else right now.
8. Mark the source message read.
9. Commit the vault changes with message `intake: <intake_id> filed (system: <name>, kind: <kind>)`.

## Failure modes and how they're handled

| Case | Router behaviour |
|---|---|
| No `[HAWKINS-INTAKE]` prefix | Ignore — not intake mail. |
| Missing/malformed header block | Do not file. Alert Dany with the message ID; leave message unread. |
| Duplicate `intake_id` | Do not overwrite. Alert Dany; leave message unread. |
| Attachment write fails | Do not file. Alert Dany; leave message unread. |
| Gmail connector error | Retry next scheduled run. |

Every failure keeps the source mail unread so it re-appears on the next run — nothing is silently dropped.

## What lives where

| Artifact | Location |
|---|---|
| Landing page + composer | `EVEglyphDesign/hawkins-twin-platform` (public) → GitHub Pages at `/luke/` |
| This spec | `EVEglyphDesign/hawkins-twin-platform/luke/intake-router-spec.md` (public) |
| Intake records | `EVEglyphDesign/hawkins-twin-compliance-vault/intake/<intake_id>/` (private vault) |
| Router code | To be committed to `hawkins-twin-compliance-vault/router/` when the router job is stood up |
| Scheduled job | Managed by the Perplexity Computer task scheduler, running under Dany's account |

## Sovereignty properties

- **No third-party form vendor.** The composer is a browser-local `mailto:` handoff; the receiver is Dany's own Gmail.
- **No hosted intake database.** All intake records live in a repo under Dany's GitHub account, in the private compliance vault.
- **No external webhook.** The router is scheduled work running under Dany's session, using the already-authorized `gcal` connector.
- **Reversible at any time.** If Dany turns off the router, intake stops flowing but nothing external needs to be torn down.

## Not yet in place

- The router job itself has not been scheduled yet. This spec documents what it will do; the next step is standing it up as a scheduled Perplexity Computer task and running an end-to-end test with a dummy intake.
- The `intake/` folder in the compliance vault will be created when the first real intake arrives (or via a one-time seed commit before the router turns on).

---

*Pour le bien-être du peuple.*
