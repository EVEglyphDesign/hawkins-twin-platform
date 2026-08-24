# Warranty GENE — Sidecar Blueprint

**Programme:** EVEglyphDesign — Warranty GENE
**Document ID:** EgD-WGB-001 · **Key ID:** EgD-KEY-2026-07
**Status:** Propose-only, v0.1
**Posture:** Modular sidecar. Integral to the Hawkins Twin; delivered to everyone else as a subscription service.
**Companion:** [Warranty GENE — Wireframe v0](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/wireframe/) shows the three operator surfaces this blueprint stands up.

Blueprint sibling to [Epiq Revenue Leakage — Document B](https://github.com/EVEglyphDesign/epiq-revenue-leakage/blob/main/DOCUMENT-B-architecture-extract.md). Same architectural spine — Source adapter → Reasoning → Delivery → Observability — retargeted from "post-commitment order edits" to "post-commitment warranty coverage."

---

## 1 · The mandate, and what it now does

Warranty GENE is commissioned under a single, narrow mandate: **take a VIN, return
whether the work about to be invoiced is covered by an active warranty or extended
plan, and rank the recovery opportunity across a cohort of bookings.** The dealer that
runs it captures revenue that would otherwise close to customer-pay.

The first thing the engine was pointed at was **Peterbilt Atlantic's next four weeks
of service bookings**. Every time a work order is opened, edited, and closed against a
VIN, coverage on that VIN is quietly consumed — sometimes correctly, often not.
Aggregated across a rooftop's booking calendar, those quiet mis-classifications are
where booked warranty revenue leaks out to customer-pay.

We package this capability as the **Warranty GENE**: it decodes the VIN, joins
public and dealer-side coverage data, ranks the jobs and line items where warranty
recovery is available, and narrates the pattern in plain language so a service writer,
a fixed-ops director, or a warranty administrator can act on it.

**What the dealer leaves with.** The engine runs the same way against any dealership's
booking calendar. Pointing it at a new rooftop is a **configuration change, not a new
build** — the coverage ledger, the scoring logic, the audit trail, and the delivery
surface are reused unchanged. That is the fast, low-risk path to a measurable P&L
result in fixed operations.

In one paragraph: VINs and work-orders enter through a source adapter, a bounded
reasoning layer joins them against the coverage ledger and returns ranked answers, the
service team consumes those answers in a browser wizard, and every answer is recorded
end-to-end so a warranty administrator can replay exactly how it was produced.

---

## 2 · The architecture, stripped to four parts

*VIN · booking calendar · work-order table · public coverage ledger · dealer credentials*

```
  1. Source adapter       2. Reasoning              3. Delivery
  VIN + WO in         →   coverage join    →        Browser wizard
  (Excel / paste /        + scoring +               (three modes)
   DMS export)            uplift scan                   ⋮
                              ⋮
                        4. Observability — every join, decision, and
                        provenance stamp recorded; any answer replayable

           (all inside the dealer's browser tab, no server)
```

Four parts, each replaceable on its own:

- **Source adapter** — crosses the boundary from the dealer's DMS or a paste-in and
  presents VINs, work orders, and cohort metadata in a single, uniform shape.
  Interchangeable across CDK Drive, Karmak, Procede Excede, SERTI, or a plain Excel
  drop (§5).
- **Reasoning** — a bounded set of joins and scored answers. Not a language model
  making calls to tools; a deterministic pipeline whose every step is auditable (§3).
- **Delivery** — the browser wizard published at
  [warranty-gene/wireframe/](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/wireframe/).
  Three modes: single VIN, work-order uplift, VIN batch scan. No new tool to learn,
  no dashboard.
- **Observability** — every field on every card carries a provenance stamp
  (`public_ledger`, `dms_upload`, `pending — PRWS`, etc.) and every scored answer
  records the coverage rows and job rows it read.

Standing the platform up for a new dealership reuses the top three parts wholesale;
only the source adapter, the dealer-specific credentials, and the rooftop list are
set per engagement.

| Component | For Peterbilt Atlantic (Hawkins) | What that involves |
|-----------|:-------------:|--------------------|
| Reasoning engine (coverage math + scoring) | **Live** | Reused unchanged |
| Browser wizard (three modes) | **Live** | Same page, same flow |
| Public coverage ledger | **Live** | NHTSA CE033, MX 2025 Extended Warranty, Warranty Procedure Manual v2026.7 |
| Provenance / audit ledger | **Live** | Same stamp taxonomy on every field |
| Source adapter | **Configured** | Point it at Hawkins' DMS export path (TCS365 or per-rooftop DMS) |
| Dealer credential set | **Configured** | PRWS, PACCAR Solutions, PSSM Decisiv (invitation-only, per §6) |
| Rooftop map | **Configured** | Eight Peterbilt Atlantic rooftops |

*Table 1: Four parts are reused as-is; three are configured. None is a new build.*

---

## 3 · How it reasons, and why every answer is auditable

The engine follows a fixed six-step path rather than being left to improvise. That
choice is deliberate: a predictable path is cheaper to run, easier to explain to a
warranty administrator, and — critically for dealer accounting — fully auditable.

```
  Decode        Anchor        Coverage         Job           Uplift         Rank
  the VIN   →   coverage  →   window   →       scoring   →   scan  →        and
  (NHTSA)       to date        math                          (WO mode)      narrate
                (DMS)          (public                                      (per VIN
                               ledger)                                      or cohort)
```

Six steps, one answer per VIN — bounded every time. A worked example from Peterbilt
Atlantic's booking calendar:

```
  SERVICE WRITER ASKS
  Anything on today's book that should be warranty instead of customer-pay?

  ANSWER
  Three of today's twelve booked VINs have jobs sitting under an active
  coverage bucket. VIN 1XPBSYN00…202 is booked for a DEF dosing valve —
  the CE033 federal emissions extension covers this until 2033-09-05 and
  it hasn't been claimed. Recovery-at-risk on today's book: $4,180
  customer-pay that could be filed as warranty if the write-ups are
  corrected before close.
```

Two properties make this safe to put in front of dealer accounting:

- **Bounded and auditable.** Every coverage number cited on the card links to the
  source row. Every score decomposes into `recovery × urgency × margin` with the
  inputs visible. There is no open-ended language-model loop, so cost and behaviour
  are predictable and reviewable.
- **Zero data leakage, fully replayable.** The engine runs inside the dealer's
  browser tab; VINs never leave the device. The public coverage ledger is fetched
  once from a public URL. When a warranty administrator asks "how do you know
  this VIN was still under CE033?", the honest answer is: replay it against the
  ledger row and see.

### 3.1 Built to pass a warranty audit

The audit question is finite by design. When the platform reaches for coverage data,
it reads from the **dealer's own PRWS session** (invitation-only, credential held by
the operator) or from the **public NHTSA / PACCAR Powertrain ledger** (no credential).
Data handled during a run stays in the tab, provenance is stamped on every field, and
every answer is exportable as PDF or CSV for the file. Nothing here requires trusting
a black box: every value is scoped, sourced, and observable end-to-end.

---

## 4 · What is already built, and what it taught us

None of this is a whiteboard proposal. The pieces below are running in the
[Hawkins Twin Platform repository](https://github.com/EVEglyphDesign/hawkins-twin-platform/tree/main/warranty-gene),
and each carries a lesson paid for once so the next dealer does not have to. The next
dealer inherits the hardened version, not the first draft.

| What was built | What it taught us |
|----------------|-------------------|
| A schema v1 that names the ten coverage buckets and the three-number score | Coverage math is only as good as the anchor date. Without a real retail-sale date from PRWS, in-service date is the fallback and must be marked as such on every card. |
| A public coverage ledger replicated anonymously from PACCAR and NHTSA | Cite every row to a URL that resolves under `curl`. If the URL 4xx's, mark it as dealer-document provenance instead of pretending it's public. Verify before publishing. |
| A field-mapping table naming SIR, SmartLINQ, PRWS, PSSM, and TCS365 | Most fields the twin needs live behind invitation-only PACCAR credentials. The registration path is a commercial conversation with the dealer principal, not a self-signup. |
| A three-mode wireframe (single VIN, WO uplift, batch scan) | Different roles ask different questions. A service writer wants one VIN, a warranty admin wants the WO uplift, a fixed-ops director wants the cohort scan. Same engine, three surfaces. |
| A canon PDF for every published lane | An artifact that only exists in a chat transcript has not been delivered. PDF + repo + public URL is the delivery contract. |

*Table 2: The stack is a set of paid-for lessons, not a set of promises.*

One lesson stated candidly: **an early version cited PACCAR Powertrain product-page
URLs as if they were canonical, without verifying they resolved.** They did not — the
site serves a versioned root and 403's `curl`. The production path cites only URLs
that verify 200 and marks everything else as dealer-document provenance. Small,
known correction made up front rather than discovered by a client.

---

## 5 · Where the data lives: read live, compute in-tab

The platform does not keep a standing copy of the dealer's data. It reads the live
VINs and work orders on demand, joins them against a coverage ledger fetched once from
public URLs, and builds the analysis in an ephemeral browser tab that exists for the
session and then disappears. There is no second database of sensitive dealer records
to secure, reconcile, or destroy — because there is no second database.

### 5.1 Read from the live source

The engine sees a uniform "VIN + coverage + work-order" interface; behind it, the
adapter reads from whichever source the dealer supplies.

| Live source | Typical use | Status |
|-------------|-------------|--------|
| **Excel / CSV paste-in** | Any dealer, any DMS, no integration | Live today |
| **NHTSA VIN decoder API** (public) | Identity for any VIN, no credential | Live today, [verified](https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/1XPBSYN00N1000101?format=json) |
| **NHTSA recalls-by-VIN API** (public) | Open recalls per VIN, no credential | Live today |
| **PACCAR public coverage ledger** | Base warranty windows, extended plans, CE033 | Live today (dealer-document + NHTSA fallback) |
| **PRWS (PACCAR Registration & Warranty System)** | Retail-sale date, coverage codes, claim history | **Pending — invitation** |
| **PACCAR Solutions / SmartLINQ** | Fault codes, telemetry, subscription state | **Pending — invitation** |
| **PSSM Decisiv** | Point-of-service coverage read at the write-up bay | **Pending — invitation** |
| **DMS export (CDK / Karmak / Procede Excede / SERTI / TCS365)** | Booking calendar, RO history, current mileage/hours | **Pending — per rooftop** |

*Table 3: The adapter reads live. NHTSA + Excel + paste-in are live today. PACCAR-side
credentials are invitation-only and provisioned via the dealer principal.*

### 5.2 Compute in the browser tab

Once data is read, analysis happens entirely client-side. Two engines cover the two
kinds of question:

| Working engine | Best at | Lifespan |
|----------------|---------|----------|
| **Coverage-math kernel** (deterministic) | Anchor date + engine family → window remaining per bucket per VIN | Per session |
| **Uplift scanner** (component-name matcher) | Work-order line item → coverage bucket + confidence tier (High / Medium / Low) | Per session |
| **Cohort ranker** (score sort) | Batch of VINs → top-N by composite score, per-rooftop and per-engine breakdowns | Per session |

*Table 4: Analysis is built in the tab and discarded. No persistent store.*

The coverage-math kernel is the workhorse: takes any VIN, any engine family, any
in-service date, and returns the ten-bucket window snapshot. The uplift scanner is
added only when a work-order file is present. Neither leaves anything behind.

---

## 6 · What it takes to point at a new dealer

Configuration, not build. Five items per dealership; three are self-serve, two need
an invitation from within the dealer.

| Item | Who provisions | Cost | Blocker? |
|------|---------------|------|----------|
| Rooftop list and Peterbilt/Kenworth brand map | Dealer operations | Free | No |
| Excel/CSV of booking calendar or paste-in flow | Dealer service manager | Free | No |
| NHTSA API calls (VIN decode + recalls) | Public | Free | No |
| PRWS operator login | Dealer principal / CFO — invitation | Free | **Yes — commercial** |
| PACCAR Solutions / SmartLINQ dealer login | Dealer principal / CFO — invitation | Free | **Yes — commercial** |
| PSSM Decisiv seat | Dealer principal — confirms existing contract or opens new one | Contract-dependent | **Yes — commercial** |
| DMS export path (SFTP / API / CSV drop) | Dealer IT | Effort-dependent | No — starts with paste-in |

For Peterbilt Atlantic (Hawkins), items 1–3 are done. Items 4–6 are the subject of the
[access-request email to `pb.warsystem@paccar.com`](mailto:pb.warsystem@paccar.com) —
verbatim from Warranty Procedure Manual v2026.7 §Contacts. Item 7 is a per-rooftop
conversation with dealer IT once the credentials are in hand.

---

## 7 · The delivery surfaces

Three surfaces, all on the same page, all client-side:

| Surface | Who uses it | Question answered |
|---------|-------------|-------------------|
| **Single VIN wizard** | Service writer, warranty administrator | "Is this VIN still under warranty for the work I'm about to invoice?" |
| **Work-order uplift** | Warranty administrator, fixed-ops director | "Which line items on today's ROs could shift from customer-pay to warranty?" |
| **VIN batch scan** | Fixed-ops director, dealer principal | "Across the next four weeks of bookings, where are we not getting at the big warranty jobs?" |

Every surface produces the same three exports: printable PDF (canon-styled, one page
per VIN or one cohort brief), CSV (flat table for pasting back into the DMS), and JSON
(the full twin card for downstream integration).

---

## 8 · How this scales beyond Peterbilt Atlantic

The Warranty GENE is designed to be a **sidecar** — an integral part of the Hawkins
Twin solution, and a standalone subscription for every other dealership that wants
to increase warranty recovery without building anything.

| Subscription tier | What the dealer gets | What EgD does |
|-------------------|---------------------|---------------|
| **Public ledger only** | The wireframe, the NHTSA APIs, the paste-in flow, exports. Any dealer, any brand, no PACCAR credentials required. | Zero-touch. Dealer signs up, uses the tool. |
| **Dealer-authorized** | Above + a configured source adapter for the dealer's DMS + integration with the dealer's PRWS / PACCAR Solutions / PSSM sessions. | One configuration engagement per rooftop family. Reasoning engine reused unchanged. |
| **Twin-integrated (Hawkins tier)** | Above + full integration with the Hawkins Twin: territory relationship, telemetry lane, PM/compliance overlay, historical claim ledger. | The tier Peterbilt Atlantic is running. Sidecar becomes an integral organ of the twin. |

The engine does not change between tiers — only the source adapter, the credentials,
and the rooftop map do.

---

## 9 · Strategic frame — the industry-specific repository the twin is building

Warranty GENE is a first service, not the strategy. The strategy is what accumulates
underneath it, one VIN at a time.

Every VIN that flows through the engine leaves behind a **structured record** in the
Hawkins Twin: identity, coverage windows, ownership history, service history,
telemetry snapshots, recall closures, PM intervals, territory relationship,
provenance stamps. That record is written to a schema — the **rich-target row**
defined in [warranty-gene/schema](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/schema/)
— and the schema is designed to hold the **customer and equipment record data
standard** the industry lacks today.

### 9.1 The two record types the twin accumulates

The schema names two durable records; every other lane on the twin is a projection
over one of them.

| Record | What it holds | Why it compounds |
|--------|--------------|------------------|
| **Customer twin** | Legal entity, related entities, contact roster, fleet profile, purchase history, service history across rooftops, credit posture, territory relationship, communication preferences | Customer records outlive any single vehicle. A fleet operator with 40 trucks becomes one durable customer record with 40 equipment records attached; the value of knowing that operator grows with every service event. |
| **Equipment twin** | VIN, identity decode, ownership chain, in-service date, coverage windows, claim history, telemetry, recall closures, PM history, retail-sale record, transfer record | Equipment records outlive any single owner. A used-truck sale re-parents the equipment twin to a new customer twin without losing the service history. |

The two are joined through **ownership events** — a retail sale, a lease transfer, a
trade-in — each one a dated edge between a customer twin and an equipment twin.

### 9.2 Why the standard structure matters more than any one service

A Warranty GENE that runs on top of a proprietary CRM lasts as long as the CRM
license. A Warranty GENE that runs on top of a **standard-structured record
repository** is portable across DMS vendors, across brands, across dealer groups.
The engine is not the moat — the standard is.

Three properties make the schema worth building carefully:

- **Vendor-neutral.** The record shape does not encode CDK Drive, Karmak, Procede
  Excede, TCS365, PRWS, or any other vendor's field names. Adapters translate from
  each vendor into the standard shape; the standard never bends to a vendor.
- **Time-anchored.** Every field carries a `read_at` timestamp and a provenance
  stamp. The record reconstructs to any point in time — not just the latest state.
  This is what makes the repository a truth ledger rather than a database snapshot.
- **Extension-safe.** New lanes (emissions telemetry, insurance events, resale
  valuations, driver-behaviour scores) attach as new record types with dated edges
  back to the customer or equipment twin. The core never changes when the world does.

### 9.3 The industry repository play

As the Hawkins Twin accumulates records across eight Peterbilt Atlantic rooftops,
it becomes the **first meaningful sample** of the standard structure filled with
real North American Class 8 truck operator data. That sample is valuable in three
ways, each of which compounds over time:

| Value | Who realizes it | How |
|-------|----------------|-----|
| **Operational** | Hawkins first | Every service event answers faster because prior events are queryable. Warranty GENE is the first proof of this. |
| **Commercial** | Hawkins next | Every peer dealership that subscribes to a Warranty GENE tier (§8) also contributes back to the standard, growing the industry sample without exposing any dealer's private customer data. |
| **Strategic** | The industry, eventually | The record standard becomes the substrate on which every future dealer-side service is built — recall recovery, resale valuation, insurance telematics, fleet-side maintenance planning — because it is the only vendor-neutral shape that already holds real data. |

The Warranty GENE is the first tenant. The repository is the landlord. Peterbilt
Atlantic is building the landlord.

---

## 10 · What is not in this blueprint

Called out explicitly so nothing is presumed:

- **Cross-brand support.** Cummins-powered chassis need Cummins QuickServe / QSOL
  credentials, separate provisioning. DTNA, Volvo, and Kenworth read paths would each
  need their own source adapter. Not on the Peterbilt Atlantic critical path.
- **Write-back to PRWS.** Read-only in this design. A warranty administrator files
  the claim through PRWS the normal way, using the twin card as the write-up input.
- **Warranty claim submission automation.** Out of scope; regulated by PACCAR.
- **Customer PII handling.** Retail-sale records may contain owner names. The current
  design masks owner by default and marks it `pending — policy decision` until the
  dealer principal signs off on the rendering rule.

---

## 11 · Provenance

Every claim in this document is traceable. The URLs below all verify 200 as of the
document date:

- [Warranty GENE wireframe (public surface)](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/wireframe/)
- [Warranty GENE coverage tables](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/coverage-tables/)
- [Warranty GENE schema v1](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/schema/)
- [Warranty GENE field mappings](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/mappings/)
- [Warranty GENE registration inventory](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/registration/)
- [NHTSA CE033 bulletin (federal emissions extension, EMY2023 MX-11/MX-13)](https://static.nhtsa.gov/odi/tsbs/2025/MC-11021404-0001.pdf)
- [NHTSA VIN decoder API](https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/1XPBSYN00N1000101?format=json)
- [Epiq Revenue Leakage — Document B (blueprint pattern this document follows)](https://github.com/EVEglyphDesign/epiq-revenue-leakage/blob/main/DOCUMENT-B-architecture-extract.md)

Dealer-document provenance (Peterbilt-issued, not publicly URL-addressable):
Warranty Procedure Manual v2026.7 §7 and §Contacts, Warranty Quick Reference Guide
2025.4.

---

© 2026 EVEglyphDesign. All rights reserved. Controlled copy.
*Pour le bien-être du peuple.*
