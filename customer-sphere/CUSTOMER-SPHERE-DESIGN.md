# Customer Sphere Design — HawkinsTwin Customer 360

**Programme:** EVEglyphDesign — Peterbilt Atlantic Digital Twin
**Direction record:** [2026-08-01 — Customer 360 and the reference-model position](../interactions/2026-08-01-customer-360-and-reference-model.md)
**Agreement holder:** Tim Hawkins · **20 Group access:** Luke Weatherbie · **Systems register:** Craig Allen
**Constraint:** the live CDK dealer management system is never written to.
**Status: draft. No dealership data has moved.**

---

## 1. Why a sphere and not a pipeline

A pipeline has a direction. Data leaves a system, is transformed, and lands somewhere
downstream where someone looks at it. That shape is adequate for reporting and inadequate
for a customer, because a customer is not downstream of anything. The same fleet owner is
simultaneously a sales record in CDK, a parts account, a service history, an open warranty
claim, six unreturned voicemails, a finance file, and a name Craig's marketing systems
know under a different spelling.

The customer sphere is the surface on which all of those faces resolve to one entity. The
integrator's job, as it has been stated across this programme, is to hold economics,
operations, and relationship in a single event horizon and let the sphere emerge from the
triangulation. This document is that principle applied to one dealership's customers.

Practically: **one combined schema, one customer key, many faces.** No face is authoritative
over the others. Each face carries its own source, its own timestamp, and its own
confidence, and the sphere records disagreement rather than averaging it away.

## 2. The two-body split

This is the governing constraint of the design and every other decision is subordinate to it.

| | **Metadata repository** | **Business data store** |
|---|---|---|
| **What** | Schema, field dictionary, identity rules, lineage, model definitions, DDL, validators, tests, change history | Actual customer, sales, service, parts, finance and call records |
| **Where** | GitHub — `HawkinsTwin` Customer 360 metadata repository | Postgres, inside Hawkins's own Azure tenant |
| **Custody** | EVEglyphDesign authors, Hawkins owns; readable by any party that needs to understand the model | Hawkins alone. EVEglyphDesign holds no copy |
| **Contains a customer record?** | **Never** | Yes, all of them |
| **Portable?** | Yes, deliberately — it is the reference model | Yes, but it moves only on Hawkins's instruction |

The split answers the question every dealership principal eventually asks, which is not
*what does it do* but *who ends up holding my data*. The answer here is that the description
of the data is public and forkable, and the data itself never leaves the tenant Hawkins
already pays for and already controls. A vendor cannot hold the dealership hostage with a
schema it refuses to document, and cannot hold it hostage with data it refuses to hand
back, because it never had either.

A secondary consequence matters for the commercial case in §7: because the metadata is
complete enough to rebuild the model from scratch, the model is separable from the data.
That is what makes it sellable as a reference model without selling anyone's customers.

## 3. Sources into the sphere

Three source families, one schema.

### 3a. CDK — customer and sales
The dealer management system is the spine. Customer master, sales transactions, deals and
F&I, repair orders, parts invoices, warranty claims, and the general ledger tie-out.
Acquisition follows the existing two-lane design in the
[reconciliation contract](../architecture/RECONCILIATION-CONTRACT.md): the restored-backup
lane for completeness, the API and export lane for currency, both landing in the same
Postgres and reconciled on demand rather than silently merged. The field-level model —
21 objects and 443 confidence-tagged fields — is the starting dictionary for the customer
and sales portion of the combined schema, not a separate artefact.

### 3b. Call history — the relationship record
The TELUS call platform supplies inbound and outbound call events, direction, duration,
extension, disposition and voicemail state. This is the only source in the sphere that
records what the dealership *did about* a customer rather than what it *sold* one. Its
three standing cohorts — voicemail not returned within two hours, repeat caller without
callback, and never reached — are the sphere's first behavioural signals. Ingestion runs
under a Peterbilt-owned service identity so custody and audit trail stay with the company.
Where call direction or extension identity is missing, the record contributes to cohort
counts but is never used to score an individual.

### 3c. Craig's register — the operating surface
The sixteen systems catalogued by Craig Allen are treated as first-class sources, not as
context. Marketing and lead platforms, inventory and ePortal surfaces, scheduling, and
whatever else the register holds each contribute a face to the customer. Craig's register
is the authority on what exists; this design's obligation is only to give each entry a
defined landing in the schema, an owner, an access path, and a confidence tag — or an
explicit note that it is deferred.

**Open item.** The source inventory is not closed until Craig confirms the register is
complete and current, and until each system has a stated access route — API, export, or
manual. Systems without an access route are recorded as known-but-unreachable rather than
quietly dropped.

## 4. Identity — how a customer becomes one customer

Identity resolution is the hardest part of the sphere and the part most likely to be got
wrong quietly, so it is specified before any model is built.

- **A durable internal key.** Every resolved entity carries a `customer_sphere_id` minted
  inside the sphere. No source system's primary key is promoted to the master key, because
  every one of them is a key for its own purposes and will eventually be reused, merged,
  or retired by its vendor.
- **Source keys are retained, never overwritten.** The CDK customer number, the phone
  identifier, and each of Craig's system keys are all kept against the resolved entity.
  Losing a source key destroys the audit path back to the record it came from.
- **Deterministic before probabilistic.** Exact matches on CDK customer number, on a
  normalised phone number, and on VIN-to-owner links are applied first. Only what remains
  unmatched goes to fuzzy matching on name, address, and business name.
- **Match confidence is stored, not thresholded away.** Each link carries a score and the
  rule that produced it. Low-confidence links are held as *candidate* links and surface in
  a stewardship queue rather than being auto-merged.
- **Merges are reversible.** Every merge is an appended, timestamped, attributed event. An
  unmerge restores both sides. A destructive merge is a defect, not a design choice.
- **Person and organisation are distinct.** A fleet is not a driver. The sphere carries
  both, with an explicit affiliation edge between them, because dealership relationships
  are almost always one organisation to several people.
- **Vehicle is a third axis.** Customer, organisation, and vehicle form the three anchors;
  service and warranty history hang from the vehicle, not from the person who happened to
  book the appointment.

## 5. Schema shape

Five layers, each with a job, all in the same Postgres and all described in the metadata
repository.

1. **Landing.** Source-native. Original field names, original widths, nothing coerced.
   Where a source column is wider than the SAP-shaped default, the source width wins and
   the widening is recorded explicitly — dealer data is never truncated to fit a model.
2. **Conformed.** Types normalised, phone and address standardised, currency and dates
   unified, source keys preserved. Still one row per source record.
3. **Identity.** The resolution layer of §4 — entity tables, link tables, candidate queue,
   merge event log.
4. **Sphere.** The combined customer model. One customer, all faces: commercial history,
   service history, parts, warranty, finance, contact and call behaviour, marketing
   presence, and the cohort flags derived from them.
5. **Marts.** Analytical structures for the 20 Group performance set, service and parts
   performance, and the decision surfaces. These reuse the SAP-shaped analytical model and
   the [data mart library](../architecture/DATA-MART-LIBRARY.md) rather than inventing a
   Hawkins-only structure — reuse is what lets a component be lifted to another dealership
   later without a rewrite.

Every field at every layer carries source, extraction timestamp, and confidence tag. A
number that reaches a decision surface can always be walked back to the record and the
extraction that produced it.

## 6. Governance and the gates

- **Nothing moves before the agreement.** Tim Hawkins's executed agreement gates any real
  dealership data. Until then the sphere runs on synthetic and mock composite data.
- **Peer comparison waits on access.** 20 Group peer figures populate only once Luke has
  access; blank variance fields stay blank rather than being guessed.
- **The live DMS is never written to.** Unchanged, in every phase.
- **Service identities, not personal credentials.** Every source connection is a
  company-owned identity with an attributable audit trail.
- **Tenant identity is checked centrally.** Every pull resolves the authenticated account
  and aborts on mismatch, in the shared token path, so no individual workflow can skip it.
- **Personal data stays in the tenant.** Names, phone numbers, addresses, account numbers
  and VINs exist only in Azure Postgres. The metadata repository holds field definitions
  and synthetic examples. Any commit that would place a real record in GitHub is a
  durability and privacy defect and is treated as one.
- **Retention and erasure are schema features.** Because Canadian privacy obligations apply
  to a New Brunswick dealership, the sphere carries retention policy per source and an
  erasure path that resolves through the identity layer, so a deletion request can be
  executed once and propagate rather than being chased across sixteen systems by hand.

## 7. Why this makes Hawkins the reference model

The commercial argument is not that the dealership gets better reports. It is structural.

A dealership that owns a fully described customer model — schema public, data private,
lineage complete, models running in its own tenant — is in a position no vendor-hosted
dealership can occupy. Its numbers are defensible to PACCAR and to a 20 Group because the
derivation is inspectable. Its data is portable because the description of it is complete.
Its components can be scaled and sold to peers without the underlying business data ever
being part of the transaction.

That is the reference-model position: the industry ends up measuring itself against a
shape that Hawkins owns, and Hawkins carries none of the custody risk that would normally
be the price of being the example. Components scale commercially; the reference model
stays with the dealership.

## 8. Open questions

1. Is the sixteen-system register complete and current, and what is the access route for
   each entry?
2. Which Azure subscription and region hosts the Postgres, and who administers it on the
   Hawkins side?
3. Does CDK entitlement permit the Data Export Tool over SFTP/PGP plus Dealer Data
   Exchange, which is the preferred route, or is a per-data-type third-party path required?
4. What is the retention policy per source, and who signs it off?
5. Which of Craig's systems hold customer contact data that duplicates CDK, and which is
   authoritative when they disagree?

---

© 2026 Dany Theriault. EVE “digital stem cell” glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
