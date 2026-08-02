# 2026-08-01 — Customer 360 and the Reference-Model Position

**Recorded:** 2026-08-01 (21:15 local, direct message thread)
**From:** Dany Theriault, EVEglyphDesign
**To:** Peterbilt Atlantic principals — thread copied to Luke Weatherbie
**Subjects referenced:** Craig Allen (systems register), CDK dealer management system, TELUS call history
**Class:** Direction set. Confirmed by the sender; awaiting acknowledgement from the recipients.
**Redaction:** Non-working content in the same thread is out of scope and is not reproduced here.

---

## The direction, as stated

> "If we pull the customer and sales data from CDK we can merge it with the calls and the
> systems Craig uses in a single combined schema. It would be the HawkinsTwin customer 360
> meta data repository in GitHub and a Postgres database in your Azure tenant with all your
> actual business data. We set up custom models within your architecture to scale
> components commercially but yours becomes the de facto reference model for your industry."

That is the whole of it. Five design decisions are carried inside those four sentences,
and each one closes a question that had been open in the twin since the July working
sessions.

## What it decides

**1. One combined schema, not three connected systems.**
CDK customer and sales records, TELUS call history, and the systems in Craig Allen's
register stop being three integrations that reference each other and become one schema
with one customer key. Prior to this the twin held the CDK lane
([20 Group data contract](../architecture/20-GROUP-DATA-CONTRACT.md)) and the call lane
(the TELUS twin) as separate surfaces that happened to concern the same dealership. The
direction is to resolve them against a single customer identity.

**2. Craig's register is inside the schema, not adjacent to it.**
The sixteen systems Craig Allen runs have been treated as substrate for the twin since the
register was first catalogued. This makes it explicit: those systems are sources into the
combined schema, on the same footing as CDK and the call platform.

**3. Metadata is public and portable; business data is not.**
The split is the governing constraint of the whole design. The **HawkinsTwin Customer 360
metadata repository in GitHub** carries the schema, the field dictionary, the identity
resolution rules, the lineage, the model definitions — everything that describes the data.
The **Postgres database in Hawkins's own Azure tenant** carries the actual business data
and never leaves it. No customer record is in GitHub. No schema decision is invisible.

**4. Custom models are built inside the customer's architecture.**
The models that make the twin useful commercially are set up within Hawkins's own
environment. They are not hosted by EVEglyphDesign and rented back. This is what makes
component-level commercial scaling possible without the dealership handing custody of its
data to a vendor to get it.

**5. The reference-model position is the actual commercial argument.**
The value to Hawkins is not the dashboard. It is that a dealership operating a fully
described, portable, self-owned customer model becomes the shape the rest of the industry
gets measured against. Components can be scaled and sold; the reference model stays theirs.

## What it obligates

| Obligation | Where it lands |
|---|---|
| Combined-schema design, identity resolution, metadata/data split | [customer-sphere/CUSTOMER-SPHERE-DESIGN.md](../customer-sphere/CUSTOMER-SPHERE-DESIGN.md) |
| CDK customer and sales extraction scope | [architecture/20-GROUP-DATA-CONTRACT.md](../architecture/20-GROUP-DATA-CONTRACT.md) |
| Two-lane acquisition and variance handling | [architecture/RECONCILIATION-CONTRACT.md](../architecture/RECONCILIATION-CONTRACT.md) |
| Model layer reusing the SAP-shaped analytical structure | [architecture/DATA-MART-LIBRARY.md](../architecture/DATA-MART-LIBRARY.md) |
| Azure tenant provisioning, Postgres sizing, service identity | Open — requires Tim's agreement and Luke's access |

## Gates that still hold

Nothing in this direction moves real dealership data. The existing gates are unchanged and
are restated here so the record cannot be read as permission:

- Tim Hawkins's executed agreement is required before any dealership data moves.
- Luke Weatherbie's 20 Group access is required before peer comparison is populated.
- Call-history ingestion runs under a Peterbilt-owned service identity, never a personal
  credential.
- The live CDK dealer management system is never written to.
- Until those clear, every surface runs on synthetic or mock composite data.

## Status

Direction stated and recorded. Design written. Awaiting acknowledgement from Tim and Luke,
and awaiting Craig's confirmation that the sixteen-system register is complete and current
before the source inventory in the customer sphere design is treated as closed.

---

© 2026 Dany Theriault. EVE “digital stem cell” glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
