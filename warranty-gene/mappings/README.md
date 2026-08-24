# Warranty GENE — SIR / SmartLINQ / PACCAR Solutions field mappings

**Purpose.** This lane names the PACCAR-owned surfaces that feed every field in the [rich-target schema](../schema/rich-target.schema.json), and it tags each mapping honestly. No field is invented. When a field label is not confirmed against a document I hold, it is marked **pending** and Tim will name it out loud when Luke opens the real screen.

**Provenance tags.**

- **observed** — the field name appears verbatim in an authoritative source held in `uploaded_attachments/` or on a public PACCAR page. Evidence line names the source, section, and page.
- **inferred** — the field is named by category in an authoritative source and the twin encodes it under a working key. Marked as such so it is not mistaken for a live label.
- **pending** — the field is needed but has not yet been source-confirmed. Waits on the SIR walkthrough with Luke or on the PACCAR Solutions API contract.

## What the file says

The [field-mappings.json](field-mappings.json) file is a single JSON document with four top-level parts.

1. **`authoritative_surfaces`** — the seven PACCAR-owned surfaces the twin reads from, each with an operator, an access path, the role it plays for warranty, and a citation into the [Peterbilt Warranty Procedure Manual v2026.7](https://www.peterbilt.com/) or a public Peterbilt page.
2. **`mappings`** — one entry per schema field. Each entry names the surface, the source field, the provenance tag, the evidence line, and any notes. Twin-derived fields are labelled `surface: derived` so the reader knows the twin, not PACCAR, is the author.
3. **`smartlinq_severity_map`** — the four SmartLINQ Remote Diagnostics notification levels — **Stop Now / Service Now / Service Soon / Informational** — with their driver-facing dash indicators, verbatim from the SmartLINQ Operators Manual, and the twin action taken at each level.
4. **`authority_ladder_source_table`** — the eight bulletin types PACCAR distinguishes, verbatim from the Warranty Procedure Manual v2026.7 §4.1 (page 57): **Recall**, **MX Component Specific**, **Government Agency Mandated**, **Retrofit**, **Prognostic**, **Campaign**, **Fix-as-Fail**, **Information Only**. Each row carries the manual's own definition and whether applicable warranty coverage is required.
5. **`pending_walkthrough_items`** — the short list of things I still owe the walkthrough. This is the working agenda for the first SIR session with Luke.

## The seven surfaces

| Surface | Operator | Role for Warranty GENE |
|---|---|---|
| Service Information Record (SIR) | PACCAR | Field of record for coverage, open recalls and campaigns, prior-approval status, and warranty coverage windows per chassis serial number. |
| SmartLINQ Service Management | PACCAR | Dealership case surface. Auto-displays SIR content when a case opens; in-process campaigns show as "Quoted MM/DD/YYYY". |
| PACCAR Solutions Portal | PACCAR | Telemetry surface. Four severity notifications, plain-English fault-code translations, dealer proximity. Fed by the on-truck PeopleNet Mobile Gateway. |
| PACCAR Prognostics | PACCAR | Predictive-replacement bulletins delivered into SIR / SmartLINQ Service Management. Same authority ladder as Recall and Campaign. |
| DAVIE + PRS | PACCAR | Bay-side diagnostic capture. Required for MX engine campaigns and for troubleshooting escalation. |
| Total Customer Solutions (TCS365) | PACCAR | 24×7 dealer support line; case number is a first-class field on PRWS claims. |
| PACCAR Registration and Warranty System (PRWS) | PACCAR | Authoritative claim-submission and reimbursement surface. The Warranty GENE never submits to PRWS; it reads back historical claim status. |

The [Peterbilt Connected Services page](https://www.peterbilt.com/why-peterbilt/connected-services) confirms the SmartLINQ / PACCAR Solutions telemetry pipe publicly.

## What is observed, what is inferred, what is pending

The current count across the schema is roughly:

- **observed** — every coverage bucket named in the [2025.4 Warranty Quick Reference Guide](../schema/rich-target.schema.json) and in the Warranty Procedure Manual §5.1 (in-service date, MX engine, Basic Vehicle, Extended Major Component 7/700 with option codes 9485633 and 9485634, and the SIR flag that eligible chassis carry Extended Major Component coverage); the four SmartLINQ severities; every bulletin type on the authority ladder; PRWS field labels named in §1.18 (Causal part model number, Causal part serial number, TCS365 case number, Diagnostic case number, DTC/SPN-FMI, Exit step, Prior Approval #); the SIR Campaign Field "I" code; the SmartLINQ Service Management "Quoted MM/DD/YYYY" display.
- **inferred** — a small set of schema keys where the manual describes the field by category but never publishes the SIR-screen label (`chassis.model`, `chassis.vocational_use`, `owner.home_rooftop`), plus every twin-derived field (`chassis.class`, all `score.*`, `open_jobs[].coverage_bucket`, `open_jobs[].customer_pay_at_risk_cad`, all `telemetry.*` regionality computations, `source_provenance[].source`).
- **pending** — the short list of SIR-screen labels and the PACCAR Solutions telemetry contract that the first walkthrough with Luke will close.

## Non-movement covenant

This mapping file names PACCAR fields for the purpose of reading them into the twin. No customer PII, no VIN histories, and no coverage payload land in this public repository. The Warranty GENE's rich-target worklist stays in Hawkins-owned Azure Postgres; only the schema, the mapping, and the synthetic sample fixture are public.

## References

- [Warranty GENE design canon](../WARRANTY-GENE.pdf)
- [Rich-target schema v1](../schema/rich-target.schema.json)
- [Sample worklist (synthetic, 7 VINs)](../samples/rich-targets.sample.json)
- [Peterbilt Connected Services](https://www.peterbilt.com/why-peterbilt/connected-services)
- [Peterbilt SmartLINQ Operators Manual (PDF)](https://www.peterbilt.com/static-assets/documents/resources/smartlinq_operators_manual.pdf)
- [Peterbilt SmartLINQ Sales Sheet, 2023 (PDF)](https://www.peterbilt.com/static-assets/documents/resources/2%202%2023%20SmartLINQ_SalesSheet%20v10.pdf)

---

© 2026 EVEglyphDesign. All rights reserved. Controlled copy.
*Pour le bien-être du peuple.*
