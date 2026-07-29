# Data Mart Library Specification

**Programme:** EVEglyphDesign — Peterbilt Atlantic Digital Twin, Phase 1
**Site:** Hawkins / Peterbilt Atlantic (New Brunswick), on PACCAR-affiliated CDK dealer management system
**Agreement holder:** Tim Hawkins
**20 Group access:** Luke Weatherbie
**16-system register:** Craig Allen

---

## 1. Purpose

The data mart library is the conformed structural layer that both landing lanes — backup and API — resolve into inside the same Postgres instance. It is not a hand-drawn logical model produced ahead of the data. It is derived from harvested application metadata: the actual object inventory, column definitions, keys, and code domains present in the source CDK system. The library is the target shape that the field-level model (21 objects, 443 confidence-tagged fields, with generated Postgres/Snowflake DDL and a preflight validator) is asked to fill.

The governing principle: **structure is discovered, not invented.** No table, column, or relationship enters the library because it looks plausible or because an SAP analogue exists in the abstract. It enters because the harvest found it, or because a gap it fills has been explicitly flagged and back-filled from a verified source under the precedence rules in Section 6. Where SAP-style patterns are used (Section 3), they are used as a target shape into which discovered structure is mapped — the shape does not manufacture structure that was not found.

---

## 2. Metadata harvest

The harvest runs against the pulled backup, not the API, because a full database restore exposes structure the API surface may never expose — internal keys, code tables that are never returned by an endpoint, indexes that reveal intended access paths, and screen/report definitions that describe how the business actually reads the data. This is the specific reason the harvest is anchored to Lane A (BACKUP): restore-then-harvest sees the whole schema; the API sees only what its contract chooses to expose.

What is harvested, and how each artefact contributes to the library:

- **Object and table inventory** — the full list of physical tables/objects in the restored database. This is the census against which the 21-object CDK field model is checked for completeness, and against which undocumented ledger-side objects are identified as the first admin-access verification target.
- **Column names and data types** — the literal column definitions, used to fix native type and precision in the generated DDL rather than inferring type from sampled API payloads.
- **Nullability** — column-level null constraints from the source schema, used to distinguish a structurally-optional field from a field that merely has not been populated yet (see Section 5).
- **Keys and relationships** — primary keys, foreign keys, and any declared or inferable relationships, used to derive the grain and join paths for each mart before any measure is defined.
- **Indexes** — read as a signal of the source system's own access patterns; an indexed combination of columns is treated as evidence of a natural grain or lookup path even where no formal key is declared.
- **Code and lookup tables with their value domains** — harvested in full, not sampled, so that code-to-description mappings (status codes, department codes, job type codes, and similar) are complete conformed lookups rather than partial value lists built up empirically from whatever appears in early API pulls.
- **Screen or form definitions, where available** — used to confirm field intent and business labelling where a column name alone is ambiguous, and to identify fields that are entered but not exposed through the API.
- **Report definitions** — used as a cross-check on which joins and aggregations the business already relies on, so the mart grains chosen here are not novel inventions but a superset of what the dealership already reports against.
- **Application dictionary, where one exists** — treated as the authoritative source of field definitions and takes precedence over inferred meaning from column naming alone.

Each of these artefacts feeds a specific part of the conformed layer: inventory and keys fix the mart grain; types and nullability fix the DDL; code tables become conformed dimension value domains; screens, reports, and the dictionary resolve ambiguity and confirm business meaning.

---

## 3. Reuse of the SAP model

The instruction is to reuse as much of the SAP model as can be reused. This is a statement about **structural pattern reuse**, not a claim that Peterbilt Atlantic runs SAP or that its data will be forced into an ERP it does not use. Established SAP-style modelling gives a mature, well-understood target shape for dealership data that is structurally the same class of problem: master data with attributes, documents with header and line items, movements, postings, and organisational hierarchies.

Patterns reused, and the dealership objects they receive:

- **Conformed dimensions and shared master data** — a customer, a part, and a technician are each single conformed entities referenced by every mart that touches them, rather than being redefined per subject area.
- **Organisational and hierarchy structures** — dealership location, department, and cost-centre hierarchies are modelled as an org-unit hierarchy in the SAP sense, giving a single structure that service, parts, and financial marts all hang off.
- **Document header and line-item pattern** — any dealership transaction that has a header (customer, date, status) and one or more line items (parts, labour operations) is modelled as header/line pairs, matching the SAP sales-document and purchasing-document pattern.
- **Movement/posting document pattern** — any event that changes a quantity or a balance is modelled as a movement or posting document with a type, a quantity or amount, a direction, and references back to the master data and the originating header document, matching the SAP material-movement and accounting-document pattern.
- **Period and fiscal calendar handling** — all time-based aggregation resolves through a conformed fiscal calendar dimension (period, fiscal year, period status) rather than raw transaction date alone, consistent with SAP period-based reporting.
- **Account and cost-object dimensions** — financial postings resolve through conformed account and cost-object dimensions (cost centre, department, profit centre equivalent) rather than free-text general-ledger descriptions.
- **Distinction between master data, transactional documents, and derived analytical structures** — the library keeps these three classes structurally separate: master data changes slowly and is versioned by validity, transactional documents are immutable once posted, and analytical structures (the marts themselves) are derived and rebuildable, never a system of record.

Specific dealership-to-pattern mapping:

| Dealership object | SAP-style pattern reused |
|---|---|
| Parts master, unit (truck) master | Material-style master data |
| Repair orders | Document header and line items |
| Parts movements (issues, receipts, returns) | Movement document |
| Ledger postings | Accounting document |
| Customers and vendors | Business-partner-style master data |

This mapping fixes the target shape only. Field content, code values, and cardinalities are still supplied entirely by the harvest in Section 2 — the pattern does not pre-populate data or invent fields the harvest did not find.

---

## 4. Star schemas the library must produce

| Mart | Grain | Conformed dimensions | Core measures | Source objects | Lane |
|---|---|---|---|---|---|
| Parts inventory and movement | One row per part movement transaction | Part (material master), warehouse/location, movement type, date | Quantity moved, on-hand quantity, unit cost, extended cost | Parts master, parts movement/transaction objects, warehouse code tables | Lane A (BACKUP), overwritten within entitled scope by Lane B (API) |
| Service repair order and labour | One row per repair order line item (parts or labour) | Customer, unit, technician, service advisor, department, date | Labour hours, labour amount, parts amount, line status | Repair order header, repair order line items, labour/operation codes | Lane B (API) primary, Lane A (BACKUP) fills gaps |
| Work in process | One row per open repair order as of a given as-of date | Repair order, department, status, date | Open WIP amount, days open, aged WIP bucket | Repair order header, status/history objects | Lane B (API) primary, Lane A (BACKUP) fills gaps |
| Unit sales | One row per unit (truck) sale transaction | Unit (material master), customer, salesperson, deal type, date | Sale price, cost, gross, unit count | Unit master, sales deal/document objects | Lane B (API) primary, Lane A (BACKUP) fills gaps |
| Dealership financial performance / absorption | One row per account/cost-object/period combination | Account, cost object/department, fiscal period | Posted amount, absorption ratio inputs (fixed expense, gross profit by department) | General ledger postings, cost-centre/department master, fiscal calendar | Lane A (BACKUP) primary — pending verification of undocumented ledger-side objects |

The financial performance/absorption mart is explicitly dependent on the ledger-side objects that are the first admin-access verification target (Section 8); its column-level completeness cannot be asserted until that verification is complete.

---

## 5. Filling the blanks

The operator's rule is explicit: the API-derived structure will have blanks, and those blanks are filled from the backup-and-recovery lane, not guessed. This is implemented as field-level provenance carried on every column in the conformed layer, not as a one-time backfill that then loses its lineage.

Every column in the conformed layer carries:

- **Supplying lane** — which lane (A/BACKUP or B/API) supplied the current value.
- **Confidence tag** — the confidence tag inherited from the 443-field CDK field dictionary, carried through unchanged rather than re-derived.
- **As-of marker** — the timestamp or extraction batch the value was current as of, so that a value is never presented without its currency being known.

A **blank** (a field the API-derived structure defines a slot for but has not yet been populated by either lane) is distinguished from two other conditions that must not be confused with it:

- **Genuine null** — the source system's own nullability (harvested in Section 2) declares the field optional, and the harvested backup confirms no value was ever entered. This is a fact about the business record, not a gap in the pipeline, and is not eligible for backfill.
- **Not-entitled field** — the field exists in the harvested schema but the current access grant (see Craig Allen's 16-system register and the entitlements underlying Luke Weatherbie's 20 Group access) does not authorise either lane to read it. This is recorded distinctly from a blank so that it is never silently treated as fillable; it requires an entitlement decision, not a data-quality fix.

Only true blanks — slots the target structure requires, that the source schema does not mark as intentionally null, and that are within granted entitlement — are candidates for backfill from Lane A.

---

## 6. Precedence and exceptions

Within its entitled and authoritative scope, the API (Lane B) may overwrite a backup-supplied (Lane A) value. This never happens silently: both the incoming API value and the previously-held backup value are retained, not just the winner. A later change that shows variance against a value that was previously reconciled does not quietly win by recency — it raises an exception for review rather than being auto-accepted.

The full precedence rules, variance thresholds, and exception-handling workflow are governed by the [reconciliation contract](RECONCILIATION-CONTRACT.md), which this library defers to for anything beyond the storage of both values and the raising of the exception itself.

---

## 7. Library governance

- The library is **versioned**. Every published schema is a numbered, dated artefact, not a moving target.
- A **schema change in either lane** — a new or altered object discovered on a subsequent backup harvest, or a new or altered field exposed by the API — is a versioned event, logged against the library version it produced, not applied as a silent in-place edit.
- The **preflight validator gates every load**. No load, from either lane, reaches the conformed layer without passing the validator that was generated alongside the current DDL.
- **Generated DDL is regenerated from the harvest**, never hand-edited. Any correction required is made by correcting the harvest or the mapping logic that produces the DDL, and then regenerating.
- **Confidence tags are carried through as column metadata into the marts.** A mart consumer can always see the confidence tag inherited from the field dictionary for any given column, not only at the raw landing layer.

---

## 8. What stays out of Phase 1

The following are explicitly excluded from Phase 1 scope:

- Anything requiring **write access** to the source CDK system. Phase 1 is read/harvest/land only.
- Anything requiring **entitlement not yet granted** under the current access register (Craig Allen's 16-system register and the access underlying Luke Weatherbie's 20 Group access). These fields are marked not-entitled (Section 5), not omitted silently.
- **Any mart that cannot be sourced without the unverified ledger-side objects.** The dealership financial performance/absorption mart in Section 4 depends on ledger-side objects that are the first admin-access verification target and are not yet confirmed present, complete, or entitled. These objects are flagged for verification, not guessed at or approximated from other objects.

---

## 9. Open questions

1. Which specific ledger-side objects exist in the CDK schema beyond the 21 documented objects, and can admin access be granted to confirm their structure? — **CDK administrator**
2. Does the current agreement's data-access scope extend to the ledger/general-ledger objects needed for the financial performance and absorption mart, or does that require a separate entitlement request? — **Tim Hawkins**
3. Which fields within the 443-field dictionary does Luke Weatherbie's 20 Group access actually cover, versus fields visible in the schema but outside that access grant? — **Luke Weatherbie**
4. Is Craig Allen's 16-system register the complete and current list of systems in scope, or are there systems pending addition that would introduce further undocumented objects? — **Craig Allen**
5. Can the CDK administrator confirm whether report definitions and screen/form definitions are exportable from the backup, or only inspectable interactively? — **CDK administrator**
6. Does Tim Hawkins want the financial performance/absorption mart withheld entirely from Phase 1 delivery, or delivered with the ledger-dependent columns explicitly marked not-entitled/pending? — **Tim Hawkins**
7. Are there existing 20 Group benchmark definitions that should constrain the grain or measures of the unit sales and financial performance marts, so the library matches what Luke Weatherbie already reports against? — **Luke Weatherbie**
8. Who holds authority to approve entitlement changes once not-entitled fields are identified — is that a CDK administrator function or does it route through Craig Allen's system register process? — **Craig Allen**

---

© 2026 EVEglyphDesign. Controlled copy. Key ID EgD-KEY-2026-07.

*Pour le bien-être du peuple.*
