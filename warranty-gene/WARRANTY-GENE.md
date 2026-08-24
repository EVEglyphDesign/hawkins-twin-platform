# Warranty GENE

## Peterbilt Atlantic Digital Twin — the rich-target lane

**EVEglyphDesign** · Hawkins Twin Platform · Warranty GENE v0.1
Prepared for Tim Hawkins and Luke Weatherbie · August 24, 2026

---

## 1. What the Warranty GENE is

The Warranty **GENE** — *G*ather, *E*ligibility, *N*otify, *E*arn — is the module of the Hawkins/Peterbilt twin that answers one question per VIN, per day, ahead of the customer's next visit:

> *What warranty jobs should be performed on this truck, and how do we get it into a Hawkins bay before someone else does?*

Warranty labor is the highest-margin work in Tim's shop. A job that costs the customer nothing can still return several thousand dollars of margin per event to the dealership. The Warranty GENE exists so no eligible truck ever leaves the region unclaimed. It is a *rich-target identifier*, not a claim submission tool — PACCAR Registration and Warranty System (PRWS) remains the authority for filing[^wpm-audit].

The GENE reuses the twin's existing plumbing. It does not invent a parallel data model:

- VIN-keyed lookups against **SIR** (Service Information Record) and **SmartLINQ Service Management**, which already auto-display open recall, campaign, and warranty coverage against every VIN as it arrives at the dealership[^wpm-campaigns].
- Coverage math against the **2025.4 Warranty Quick Reference Guide** (413 covered components across ten coverage buckets, plus the Coverage Time & Exclusions table)[^wqrg].
- Emissions eligibility from the **CARB / EPA / ECCC Emission Component Coverage** register (60 mo / 350,000 mi Class 8 CARB; 60 mo / 100,000 mi (160,000 km) EPA/ECCC)[^carb].
- The **Warranty Bot** prompt pattern already ratified in the twin: VIN-keyed booking-time scans flag *possible* OEM or aftermarket coverage for human review; the manufacturer system stays authoritative[^twin-warranty-bot].

Everything downstream — the customer outreach, the shop schedule, the parts pre-order — is fed by the same VIN row.

---

## 2. Where the signal comes from — the earlier, the better

The GENE ranks its sources by how far ahead of the customer's next visit they see the truck. The earlier the signal, the more time Tim has to book the bay, stage the parts, and win the job.

| Rung | Source | Latency | What it tells us | Who else sees it |
|------|--------|---------|------------------|------------------|
| 1 | **SmartLINQ / PACCAR Solutions telematics** | Live | Fault codes, prognostics, geofence entry into the Hawkins region | PACCAR + fleet + any Peterbilt dealer the truck rolls into |
| 2 | **SIR + SmartLINQ Service Management** | On arrival | Every open recall, campaign, and warranty coverage flag against the VIN[^wpm-campaigns] | Any Peterbilt dealer that runs the VIN |
| 3 | **PACCAR Prognostics bulletins** | Proactive | "Proactive Replacement Using PACCAR's Prognostic Prediction Algorithm to Maximize Uptime"[^wpm-campaigns] | Any Peterbilt dealer |
| 4 | **Fault-code stream via DAVIE / PRS files** | On shop visit | Confirmed fault codes and diagnostic log, required on Prior Approval and MX Engine work[^wpm-mx-engine] | Only the servicing dealer |
| 5 | **Customer complaint (CCC) at booking** | Booking call | Complaint, Cause, Correction narrative[^wpm-audit] | Only the servicing dealer |
| 6 | **Post-repair audit trail** | After the fact | Retention, PRWS submission, RMA returns | PACCAR audit |

The rich-target discipline is rung 1. **Any vehicle whose VIN matches a PACCAR-open warranty job and whose GPS track will put it inside the Hawkins region overnight is a booking to protect.** That is the sentence the whole module is written to satisfy.

### 2.1 The PACCAR telemetry integration — where the twin adds value

PACCAR Solutions / SmartLINQ already streams truck-level events to the dealer network. Today, per Tim's read of the field: dealers can *see* trucks entering the network with some diagnostic context, but the surface is treated as an **emergency system** — it keeps a truck on the road, it does not proactively convert an inbound truck into a scheduled warranty appointment.

The Warranty GENE closes that gap. For every VIN broadcasting into the Hawkins region:

1. **Match** the VIN against the SIR / SmartLINQ open-job set (recalls, campaigns, prognostics, active fault codes with warrantable ATA components).
2. **Score** the match against Hawkins bay availability, parts on hand, and coverage window remaining (months and miles/km against the Coverage Time & Exclusions table).
3. **Alert** the dispatcher when the VIN's projected overnight location is inside Tim's region *and* the score crosses a booking threshold — with enough lead time to place the parts order the same afternoon (per §4.1's parts-order-immediately rule for recalls[^wpm-campaigns]).
4. **Present** the customer contact as a rich target in the same three-tile decision surface the TELUS twin already uses (voicemail-not-returned, repeat-caller, never-reached)[^twin-three-tile] — the fourth cohort becomes *"warrantable job available, no booking scheduled"*.

The twin does not need to replace the PACCAR ePortal or SmartLINQ — it needs to consume their VIN-keyed truth and put it beside Hawkins's own booking calendar and parts on hand.

---

## 3. The VIN-by-VIN diagnostic set

For every VIN the GENE evaluates, it fills a single row with the following fields. This is the twin's on-disk contract; nothing else the GENE emits (dashboards, alerts, worklists) reads any other shape.

### 3.1 Identity

- **VIN** (17-char, PACCAR-validated)
- **Chassis series** (Class 8, Class 6/7, Battery Electric, MX-equipped)
- **In-service date** and **odometer / hours** (with source and as-of timestamp)
- **Registered owner** and **fleet parent** (from Hawkins CDK customer master; DSFW/Direct-Fleet flag if applicable[^wpm-fleet])
- **Home rooftop** (which of the eight Peterbilt Atlantic locations owns the relationship[^twin-locations])

### 3.2 Coverage window

For each of the ten coverage buckets in the Warranty Quick Reference Guide[^wqrg]:

| Bucket | Class 8 | Class 6/7 |
|--------|---------|-----------|
| Base Emissions — CARB | 60 mo / 350,000 mi | 60 mo / 150,000 mi |
| Base Emissions — EPA / ECCC | 60 mo / 100,000 mi (160,000 km) | 60 mo / 100,000 mi (160,000 km) |
| Standard Vehicle | 12 mo / 100,000 mi (160,000 km) | 12 mo / Unlimited |
| Standard MX Engine | 24 mo / 250,000 mi (400,000 km) / 6,250 hr | n/a |
| Engine Major Components | 60 mo / 500,000 mi (800,000 km) / 12,500 hr | n/a |
| Vehicle Major Components | 36 mo / 300,000 mi (480,000 km) | 24 mo / Unlimited |
| Severe Service | 12 mo / 50,000 mi (80,000 km) | 12 mo / 50,000 mi (80,000 km) |
| PACCAR Alternator & Starter | 36 mo / 350,000 mi (560,000 km) | n/a |
| PACCAR Front Axles | 60 mo / 750,000 mi (1,200,000 km) | 60 mo / 750,000 mi (1,200,000 km) |
| Non-PACCAR Front Axles | 36 mo / 300,000 mi (480,000 km) | 48 mo / Unlimited |

Each bucket carries `months_remaining` and `distance_remaining` (miles and km). Battery-electric powertrain buckets are tracked separately with the ESS 60 mo / 500,000 mi / 80%-charge floor[^wqrg].

### 3.3 Open jobs

Every open job on the VIN, sourced in order of authority:

1. **Recalls** and **field-repair campaigns** (SIR-visible; parts order placed immediately when the VIN appears on an active list[^wpm-campaigns])
2. **Prognostic** proactive-replacement bulletins (PACCAR's prognostic prediction algorithm, no warranty coverage gate)[^wpm-campaigns]
3. **Fix-as-fail** with applicable warranty required[^wpm-campaigns]
4. **Live fault codes** (ATA-decoded; only warrantable ATA components enter the target list)
5. **Extended service agreements** — 7/700 MX Engine ESA and Limited ESA where present[^wpm-esa]

### 3.4 Job scoring

Per job, three numbers the dispatcher can read at a glance:

- **Margin estimate** — SRT hours × Hawkins warranty labor rate + parts markup, all bounded by the Standard Repair Time table.
- **Time-to-expiry** — the smaller of `months_remaining` and `distance_remaining` for the covering bucket.
- **Booking urgency** — computed from telemetry: is the truck currently inbound to the Hawkins region, and how many hours until it leaves?

### 3.5 Compliance flags

The GENE refuses to score a job when the audit posture is not clean. Any of the following blocks the alert and routes the VIN to a review lane instead of a booking lane:

- Missing technician identity on prior claims
- Repair not documented against RMI
- Overlapping or unsupported labor time
- Repeat/ineffective repair pattern on the same VIN
- Prior Approval required and not yet obtained via TCS365[^wpm-audit]

This matters because Peterbilt's audit language is explicit: improper claims are chargeable back to the dealer, and the zero-tolerance rule on altered or misrepresented data can expand an audit's scope[^wpm-audit]. The GENE's job is to increase warranty *volume*, not audit *exposure*.

---

## 4. What "rich target" means, operationally

A rich target is one VIN that satisfies all four:

1. **PACCAR-visible open job** — recall, campaign, prognostic, or warrantable fault code on the SIR / SmartLINQ record.
2. **Coverage window intact** — months and miles/km remaining on the relevant bucket.
3. **Hawkins-adjacent** — either currently owned by a Hawkins customer, or telemetry says the truck is inbound and will sleep overnight in Tim's region.
4. **Audit-clean** — no open compliance flags against prior work on this VIN.

Every rich target is a booking Hawkins should offer to the customer, framed the same way the twin has framed outreach from the beginning: *cards on the table, no pressure on staff to change how they schedule*[^twin-outreach]. The recipient sees an offer of no-cost service; Hawkins sees several thousand dollars of margin per event.

---

## 5. Where it lands in the twin

The Warranty GENE ships as a module of the existing Hawkins Twin Platform. It reuses:

- The **customer sphere index** — GitHub records what exists, where it lives, and what governs it; customer data remains only in Hawkins-controlled Azure Postgres[^twin-customer-sphere].
- The **ACDOCA / ACDOCI split** — warranty jobs post to ACDOCA as transaction records; customer interactions around booking outreach post to ACDOCI as customer-interaction vectors[^twin-customer-sphere].
- The **three-tile executive control surface** — the warranty rich-target cohort becomes the fourth named cohort alongside the TELUS three, using the same fixed case shape and drilling into a capped worklist[^twin-three-tile].
- The **twin MCP explicit-scope discipline** — every GENE call names `peterbilt` or `torque`; no dealership is default-selected[^twin-mcp].
- The **Warranty Bot prompt pattern** — GENE output is a review filter, not a verdict; the manufacturer system stays authoritative on eligibility[^twin-warranty-bot].

Public surface: `warranty-gene/` under [hawkins-twin-platform](https://github.com/EVEglyphDesign/hawkins-twin-platform).
Private surface: rich-target worklists remain in Hawkins-owned Azure Postgres, indexed but not copied to the repository.

---

## 6. Build order

1. **Ingest** the 2025.4 quick-reference matrix as coverage rules (buckets, months, miles, km).
2. **Ingest** the CARB/EPA/ECCC component register as emissions-bucket tags per ATA component.
3. **Wire** the SIR / SmartLINQ VIN lookup as a first-class read, with the PACCAR service-account credential (not a personal one, per the TELUS precedent[^twin-telus-service]).
4. **Consume** the PACCAR Solutions telemetry stream — geofence + fault-code events — into an inbound-VIN queue.
5. **Score** each VIN using the fields in §3, emit the rich-target row.
6. **Publish** the worklist to the executive control surface as the fourth cohort.
7. **Prove** the loop end-to-end against ten historical Hawkins warranty claims before any customer-facing outreach.

Nothing in this order requires new data movement out of PACCAR. It requires the twin to *listen* to what PACCAR already broadcasts and put the answer beside Hawkins's own booking calendar.

---

## 7. What this deliberately is not

- **Not a claim submission tool.** PRWS remains authoritative; the GENE flags candidates, humans file claims[^wpm-audit].
- **Not a bypass of PACCAR authority.** SIR and SmartLINQ Service Management remain the eligibility source of record; the GENE consumes them, it does not overrule them[^wpm-campaigns].
- **Not a substitute for the Warranty Bot's human-review discipline.** Every rich target is a prompt for a human to decide, not a booking made without a human in the loop[^twin-warranty-bot].
- **Not a data movement out of Hawkins.** Customer data stays in Hawkins-owned Azure Postgres. The repository holds the index, the rules, and the schema — not the payload[^twin-customer-sphere].

---

## References

[^wpm-audit]: Peterbilt Motors Company, *Warranty Procedure Manual — Version 2026.7*, August 10, 2026. §1.6 Repair Story (Complaint, Cause, Correction); §11 Warranty Audit — improper-claim register and zero-tolerance policy on altered or misrepresented data.
[^wpm-campaigns]: Peterbilt Motors Company, *Warranty Procedure Manual — Version 2026.7*, §4.1 Federal Safety Recall and Field Repair Campaigns — bulletin types (Recall, MX Component Specific Emissions Warranty, Government Agency Mandated, Retrofit, Prognostic, Campaign, Fix-as-Fail, Information Only); "SmartLINQ Service Management will automatically display open recall/campaign and warranty coverage."
[^wpm-mx-engine]: Peterbilt Motors Company, *Warranty Procedure Manual — Version 2026.7*, §4.2 Completing MX Engine Campaign Procedure — SIR / SmartLINQ pre-check, DAVIE PRS-file capture, TCS365 escalation, PDF log-file retention.
[^wpm-esa]: Peterbilt Motors Company, *Warranty Procedure Manual — Version 2026.7*, §5.1 MX Engine Major Component Service Agreements — 7/700 Extended Service Agreement (option code 9485634) and 7/700 Limited Extended Service Agreement, effective for repair orders opened after November 15, 2024.
[^wpm-fleet]: Peterbilt Motors Company, *Warranty Procedure Manual — Version 2026.7*, §6.8 Dealer Sponsored Fleet (DSFW) & Direct Fleet Warranty Administration; §6.8.3 Fleet MX Addendums.
[^wqrg]: Peterbilt Motors Company, *Warranty Quick Reference Guide for 2025.4* — 413-row Warranty Coverage matrix across ten coverage buckets, plus the Coverage Time & Exclusions table (Class 8 / Class 6/7 months, miles, km) and Battery Electric Powertrain bucket.
[^carb]: Peterbilt Motors Company, *CARB / EPA / ECCC Emission Component Coverage*, February 14, 2022 — component-to-emissions-family register across Aftertreatment, Engine, and Vehicle families; Class 8 CARB 60 mo / 350,000 mi; Class 6/7 CARB 60 mo / 150,000 mi; EPA/ECCC 60 mo / 100,000 mi (160,000 km).
[^twin-warranty-bot]: EVEglyphDesign, [hawkins-twin-platform](https://github.com/EVEglyphDesign/hawkins-twin-platform) — Warranty Bot as a booking-time VIN-keyed prompt, not an authority; Luke Weatherbie's dictated source record stays verbatim, interpretation lives in a separate lane.
[^twin-locations]: EVEglyphDesign, hawkins-twin-platform — Peterbilt Atlantic has eight published locations; billing-account count and rooftop count are not a mapping until source-confirmed.
[^twin-three-tile]: EVEglyphDesign, [eve-hawkins-telus-twin](https://github.com/EVEglyphDesign/eve-hawkins-telus-twin) — fixed three-tile decision surface (voicemail-not-returned-in-two-hours, repeat-caller-without-callback, never-reached) with one fixed case shape and capped worklists.
[^twin-mcp]: EVEglyphDesign, hawkins-twin-platform — twin MCP names `peterbilt` or `torque` explicitly on every call; no dealership is default-selected.
[^twin-customer-sphere]: EVEglyphDesign, [hawkins-twin-platform/customer-sphere/CUSTOMER-SPHERE-DESIGN.md](https://github.com/EVEglyphDesign/hawkins-twin-platform/blob/main/customer-sphere/CUSTOMER-SPHERE-DESIGN.md) — repository is the index, customer data stays in Hawkins-owned Azure Postgres; ACDOCA preserved, ACDOCI added for customer interactions.
[^twin-outreach]: EVEglyphDesign, hawkins-twin-platform — supportive outreach stance: cards on the table for Tim and Luke without pressuring staff to change schedules or processes.
[^twin-telus-service]: EVEglyphDesign, eve-hawkins-telus-twin — call-history ingestion uses a Peterbilt-owned service account rather than a personal credential, preserving company custody and audit trail.

---

© 2026 EVEglyphDesign. All rights reserved. Controlled copy.
Key ID `EgD-KEY-2026-07`.
*Pour le bien-être du peuple.*
