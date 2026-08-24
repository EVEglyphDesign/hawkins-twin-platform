# Warranty GENE — Registration and Terms & Conditions data-source inventory

Two questions the operator asked, answered separately because they answer to different PACCAR surfaces. First, how the twin gathers **warranty registration** per VIN — retail sale date, in-service date, PDI status, coverage codes sold with the chassis. Second, how the twin gathers **terms and conditions** — the months, miles, hours, and exclusions that apply to that chassis — from a machine-readable API rather than by interpreting a contract PDF.

The answer is: PRWS on Fortellis for registration, PACCAR Powertrain product pages and Extended Warranty PDF for T&Cs, PSSM (Decisiv OWL / VIP) for point-of-service coverage read-back, and PACCAR Connect for structured telemetry pending North-American scope confirmation. Every surface below is either named directly by PACCAR or by a first-tier integrator (CDK, Decisiv, Procede). None of the field names is invented.

## The one-paragraph answer

The registration record of truth is **PRWS** — PACCAR's Registration and Warranty System — published as REST APIs on **Fortellis**, CDK Global's OpenAPI-specified automotive integration marketplace at `api.fortellis.io`. That is the machine-readable pipe for VIN-level registration, PDI status, retail-sale date, and claim/coverage read-back into the twin. It requires a Fortellis developer account, an App listing on the Fortellis Marketplace, and a `Subscription-Id` header per call — not a personal credential. The dealer-workflow-facing surface, **PACCAR Solutions Service Management (PSSM)**, is built on **Decisiv** and exposes coverage through the **OWL (Online Warranty Link)** system and truck specs through the **VIP (Vehicle Information Portal)** database at the point of service — reached from the DMS side via CDK Drive, Karmak, Procede Excede, or SERTI. The terms-and-conditions record of truth for PACCAR MX engines is **not** a contract that needs interpreting — PACCAR Powertrain publishes coverage-duration tables as structured markup on each engine product page and as a controlled MX Extended Warranty PDF, and NHTSA republishes the same emissions coverage numbers as government-source PDFs for cross-reference. Neither T&C source is an authenticated API, but both are stably URL-addressable and machine-fetchable, and the coverage math the twin needs is a compact table, not a full contract.

## The registration surfaces

### PRWS on Fortellis — record of truth

Publisher: CDK Global (Fortellis marketplace and gateway) · PACCAR (PRWS). Machine-readable via REST over HTTPS. Fortellis supports OpenAPI Specification 2.0 and 3.0. Base URL `https://api.fortellis.io`. Authentication is a Fortellis service-account OAuth2 credential with a `Subscription-Id` header per call. Partner requirement: yes — a Fortellis developer account is required to build against the API, and the App must be listed in the Fortellis Marketplace at a $129 App listing fee.

Returns: vehicle registration record per VIN (retail sale date, delivery-to-first-purchaser date — the coverage anchor — and PDI completion status); warranty claim drafts, submitted claims, and dynamic status of each; and read-back of coverage codes recorded to SIR for that chassis through the PRWS integration's SIR Sheet Access.

Does **not** return: live SmartLINQ telemetry (that is PACCAR Solutions Portal or PACCAR Connect, separately), and does not return the T&C math itself — PRWS returns which coverage packages a chassis holds, not the coverage-duration text.

Observed evidence:

- CDK Global Heavy Truck: "PRWS (PACCAR's newest Registration and Warranty system): Streamlines the filing of PACCAR warranty claims by creating drafts in the PACCAR PRWS (warranty system) with information from the RO and tracking via a dynamic status screen. **PRWS is now available on Fortellis.**" — [CDK Global Heavy Truck](https://www2.cdkglobal.com/ht-oem)
- Fortellis: "A Fortellis API spec is formatted in a YAML or JSON descriptor file that follows the OpenAPI Specification, and both **OAS 2.0 and OAS 3.0** are supported." — [Fortellis Docs · Developing APIs](https://docs.fortellis.io/docs/general/developing-on-fortellis/developing-apis)
- Fortellis: "`Subscription-Id`: The Subscription ID assigned to the solution you are developing on the Fortellis platform." — [Fortellis Docs · Request Components](https://docs.fortellis.io/docs/general/making-calls/request-components/)
- Base URL confirmed by CDK Tealium connector documentation: "API Endpoint: `https://api.fortellis.io`" — [Tealium · CDK Connector](https://docs.tealium.com/server-side-connectors/cdk-connector/)
- Procede Software's PRWS Integration v1.2 release notes (December 2025): "SIR Sheet Access: Pull Service Information Record (SIR) Sheets (PDF) directly from PACCAR." Confirms SIR data flows through the PRWS integration pipe.

### PACCAR Solutions Service Management (Decisiv-built) — point of service

Publisher: PACCAR (product) · Decisiv (platform). Partially machine-readable — reached through DMS integrations with CDK Drive, Karmak, Procede Excede, and SERTI. Not a public REST API. UI at [paccar.decisiv.net](https://paccar.decisiv.net/). Authentication is the dealer's SSO account from paccarsolutions.com — same account as SmartLINQ Service Management.

Returns: **OWL (Online Warranty Link)** system — warranty coverage information at the point of service. **VIP (Vehicle Information Portal)** truck specs database — truck specification build data and vehicle configuration data. Standard Repair Times (SRTs) for the estimating process. Open recalls and campaigns per VIN, auto-displayed on case open.

Does **not** return: bulk registration data (go to PRWS on Fortellis for bulk) and does not return T&C coverage duration by option code as structured data (PSSM shows the current-coverage read-out for a specific case, not the underlying rule table).

Observed evidence:

- "The PACCAR Solutions Service Management (PSSM) platform is developed by Decisiv for PACCAR." — [PACCAR Solutions on Decisiv](https://paccar.decisiv.net/)
- Decisiv SRM Case Estimator fact sheet: "Real time data is made available at the point of service and includes SRTs, warranty coverage, truck specification build data, and more, through connections with **Express WriteUp, OWL (Online Warranty Link) system, and VIP (Vehicle Information Portal) truck specs database**."
- Decisiv PACCAR support: "To inquire about integration with Decisiv, please start with contacting your DMS provider." — [Decisiv PACCAR Support](https://support.paccar.decisiv.net/hc/en-us/articles/360034411713)

### PACCAR Connect Data Integration Services — telemetry API

Publisher: PACCAR Global Connected Services (Eindhoven, DAF-branded). Machine-readable REST API described as "our secure interface API" in the PACCAR Connect brochure. Portal at connect.paccar.com. Authentication is a PACCAR Connect service account under a Data Integration Partner Organization; the customer must approve a Data Sharing Request from PACCAR Connect before the partner can read their VIN data.

Partner requirement: yes. An integrator must first apply as a PACCAR Connect Data Integration Partner and then buy a data package from the PACCAR Connect Webshop.

Returns: original vehicle data from DAF trucks in real time. Data-package specifics are only revealed inside the webshop after partner onboarding. Categories overlap with the paccar.com/telematicsterms Truck Connectivity Services agreement — GPS location, speed, direction of travel, time of travel, service data, odometer, fault codes, engine data, mechanical condition, mileage, diagnostic and health data.

Provenance: inferred. The DAF-branded PACCAR Connect page does not itself claim Kenworth/Peterbilt coverage. Third-party integrator [Navixy · OEM Telematics by Brand](https://navixy.com/ko/learn-more/oem-telematics/brands/) states "PACCAR Connect provides a unified telematics ecosystem covering DAF, Kenworth, and Peterbilt vehicles under the PACCAR umbrella," but this is unconfirmed on the PACCAR North America side.

Evidence:

- [DAF · PACCAR Connect Data Integration Services](https://www.daf.global/en-us/daf-services/connected-services/data-integration-services)
- [DAF · Become a PACCAR Connect Data Integration Partner](https://www.daf.global/en-us/daf-services/connected-services/data-integration-services/become-a-paccar-connect-data-services-partner)

Pending for the operator: confirm with PACCAR North America whether Data Integration Services covers Peterbilt VINs at the level of vendor claims, or whether Peterbilt telemetry remains behind PACCAR Solutions Portal and SmartLINQ only for the U.S. and Canada.

### PACCAR Solutions Portal — telemetry read-only UI

Publisher: PACCAR. Customer-facing telemetry portal at [paccarsolutions.paccar.com](https://paccarsolutions.paccar.com), fed by the PeopleNet Mobile Gateway on the truck. Read-only web UI; no public API. Subscription-based per [paccar.com/telematicsterms](https://www.paccar.com/telematicsterms).

Returns: live fault-code notifications at four severities (Stop Now, Service Now, Service Soon, Informational); fuel economy, mileage, engine hours, idle time, GPS location, dealer proximity; open-recall visibility; and Over-The-Air software update delivery for MY2017+ MX-engine trucks.

Does **not** return: structured data for a downstream system. For that path, use PACCAR Connect (above) or the PSSM/DMS integration (above). Evidence: [Peterbilt Connected Services](https://www.peterbilt.com/why-peterbilt/connected-services).

### SIR through PRWS

Publisher: PACCAR. The Service Information Record has no direct public API — but its content flows out through PRWS on Fortellis (SIR Sheet Access, per the Procede v1.2 release notes) and is displayed in PSSM.

Returns: chassis-serial-anchored coverage codes and campaign/recall status. Field-level mapping is already in [`warranty-gene/mappings/field-mappings.json`](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/mappings/field-mappings.json).

Evidence: Warranty Procedure Manual v2026.7 §4.1 page 56 — "Check the chassis serial number monthly against the Service Information Record (SIR) system for open field campaigns and federal safety recalls."

## The terms-and-conditions surfaces

### PACCAR Powertrain EPA MX-11 / MX-13 product pages — the canonical T&C table

Publisher: PACCAR Powertrain. Machine-readable HTML (structured list markup, extractable by any HTML parser). Public, no authentication. Base URL `https://paccarpowertrain.com/products/{engine}/` where `{engine}` is one of `epa-mx-11`, `epa-mx-13`, `carb-mx-13`, `epa-mx-13-fire-apparatus`, and so on.

Returns per engine: Base Engine Warranty duration (months, miles, kilometers, engine hours); Major Components Warranty duration; Base Emissions Warranty split by jurisdiction (EPA vs CARB) and by heavy-duty vs medium-duty engine displacement; and Towing Coverage duration and scope of tow (to the nearest authorized U.S. or Canadian PACCAR engine dealer).

Example values for EPA MX-13:

| Coverage | Months | Miles | Kilometers | Engine Hours |
|---|---|---|---|---|
| Base Engine Warranty | 24 | 250,000 | 400,000 | 6,250 |
| Major Components Warranty | 60 | 500,000 | 800,000 | 12,500 |
| Base Emissions (EPA, heavy-duty) | 60 | 100,000 | 160,000 | — |
| Base Emissions (CARB, heavy-duty > 10.0 L) | 60 | 350,000 | 563,000 | — |
| Towing Coverage | 24 | 250,000 | 400,000 | 6,250 |

Evidence: [PACCAR Powertrain · EPA MX-13](https://paccarpowertrain.com/products/epa-mx-13/) and [PACCAR Powertrain · EPA MX-11](https://paccarpowertrain.com/products/epa-mx-11/).

### PACCAR Powertrain MX Extended Warranty controlled PDF

Publisher: PACCAR Powertrain. Machine-readable PDF (parsed at ingest into JSON, same way the twin reads the 2025.4 Warranty Quick Reference Guide). Public, no authentication. Named on the [PACCAR Powertrain Resources](https://paccarpowertrain.com/resources/) page and directly downloadable.

Returns: every plan tier (base standard, Major Component, Aftertreatment, PACCAR Protection, Towing); extended plan increments (yearly, 50,000 mi / 80,000 km); Class 8 vs Class 6/7 differentiation; EPA vs CARB differentiation; and the full T&C text — what is applied, what is excluded, engine-hour treatment.

Evidence: [MX Extended Warranty 2025 · English PDF](https://paccarpowertrain.com/wp-content/uploads/2024/11/MX-Extended-Warranty_2025_English.pdf) — "PACCAR Engine extended warranty plans can be purchased in yearly and 50,000 MI. (80,000 KM.) increments. Plan coverage durations and mileages vary with engine horsepower and intended service."

### Peterbilt Operator's Manuals — per-engine warranty statement PDFs

Publisher: Peterbilt Motors Company. Machine-readable PDF. Public, no authentication. Base URL `https://www.peterbilt.com/static-assets/documents/resources/paccar_{engine}_operators_manual_{year}.pdf`.

Returns: base engine warranty coverage text with exact durations; extended-coverage text and the deductible language ("The owner is responsible for a $100 (U.S. Dollars) deductible per each service visit under this plan in the 3rd, 4th, and 5th years of base engine warranty"); and towing-coverage language and scope.

Evidence: [PACCAR MX-13 Operator's Manual (Y53-1181-1K1)](https://www.peterbilt.com/static-assets/documents/resources/paccar_mx-13_operators_manual_2017.pdf) — "Base Engine Warranty… begins on the date of delivery and ends two years or 250,000 miles (400,000 kilometers) or 6,250 hours, whichever occurs first, after the date of delivery of the engine to the first purchaser or first lessee."

### NHTSA Technical and Emission Service Bulletins — government cross-reference

Publisher: U.S. National Highway Traffic Safety Administration. Machine-readable PDF, trust level 3. Public, no authentication. Base URL `https://static.nhtsa.gov/odi/tsbs/{year}/{bulletin_id}.pdf`.

Returns: exact emissions-warranty coverage in duration, miles, kilometers, and hours, tied to specific engine model years and displacement. The warranty registration anchor date is named explicitly.

Evidence: [NHTSA MC-11021404-0001](https://static.nhtsa.gov/odi/tsbs/2025/MC-11021404-0001.pdf) — "U.S. and Canadian Federal emissions regulations require that the warranty coverage is a period of ten (10) years or 435,000 miles / 700,000 km / 22,000 engine hours, whichever comes first, from the original warranty registration date for these specific components on the EMY2023 PACCAR MX-11 and MX-13 engines." And [NHTSA MC-11008567-0001](https://static.nhtsa.gov/odi/tsbs/2024/MC-11008567-0001.pdf) — "5yr/100k mi 5yr/160k km Federal Emissions Warranty; 2yr/250k mi 2yr/402k km Base Engine Warranty."

### Peterbilt Warranty Procedure Manual v2026.7 — dealer application layer

Publisher: Peterbilt Motors Company. Machine-readable PDF (already parsed into the workspace). Dealer distribution. Held at `workspace/uploaded_attachments/…/Warranty-Procedure-Manual-Version-2026.7-August-10-2026-1.pdf`.

Returns: coverage-window anchors (in-service date, retail-sale date, delivery-to-first-purchaser date); option-code specific T&C — for example the 7/700 Engine Major Component Extended Service Agreement, option codes 9485633 (original owner / used before 2023-05-22) and 9485634 (used vehicles purchased/sold 2023-05-22 through 2024-11-15), with reimbursement tiers running from $10,000 (5.0–5.5 yr / 500–550K mi) down to $4,000 (6.5–7.0 yr / 650–700K mi); the eight Emission Service Action bulletin types (already captured in [`field-mappings.json`](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/mappings/field-mappings.json)); and Prior Approval requirements and PA-number field placement on claims.

### Peterbilt Warranty Quick Reference Guide 2025.4

Publisher: Peterbilt Motors Company. Machine-readable XLSX (already parsed into the workspace). Dealer distribution. Held at `workspace/uploaded_attachments/…/WARRANTY-QUICK-REFERENCE-GUIDE-for-2025.4.xlsx`. Returns every coverage bucket in the rich-target schema with months, miles, hours, and exclusions.

## Component-supplier T&Cs (63 suppliers)

Warranty Procedure Manual v2026.7 Section 7 (pages 130–177) enumerates 63 component suppliers with per-supplier T&Cs — Bendix, Cummins (older Roadrelay units), Eaton, Meritor, Allison, Sensata, Pana-Pacific, Sanden, National Seating, RH Sheppard, and so on. Each has its own coverage window, RMA number, and shipping instructions.

- **Supplier Warranty Bulletins on PACCAR.net** — the Warranty Procedure Manual references PACCAR.net seventeen times as the location for supplier bulletins. Machine-readable PDFs behind a PACCAR.net dealer login. Returns per-supplier coverage duration and exclusions, RMA/CARE numbers (for example 50047 for Sensata MX Pressure Sensors and for Sensata Vehicle Sensors and Switches), shipping accounts (FedEx 1388868281, UPS 012981), and labor SRTs / VMRS codes per supplier.
- **Cummins RAPIDSERVE Web** — for Cummins-engine chassis outside the PACCAR MX line, Cummins publishes a separate self-service warranty filing surface. Named in a [Decisiv customer story with Papé Kenworth](https://www.decisiv.com/pape-kenworth-2/): "By linking to Cummins RAPIDSERVE Web, a self-service warranty filing resource that allows certified dealers and repair locations to file claims, Papé Kenworth is able to automate the process and speed approval from Cummins on behalf of its customer." Only relevant if Hawkins carries Cummins-engine chassis — confirm scope with the operator.

## What the twin does

Registration lane. The twin reads PRWS on Fortellis as the registration record of truth, authenticated with an EVEglyphDesign Fortellis Organization service account and per-App `Subscription-Id` header. It reads SIR Sheet Access through PRWS for the coverage-codes and campaign-status payload. It reads PSSM (Decisiv) via the CDK Drive integration Hawkins already runs for case-level coverage read-back at the point of service. It reads PACCAR Connect Data Integration Services for structured telemetry — pending PACCAR North America's confirmation that Peterbilt VINs are in scope. The twin never writes to PRWS. The Warranty GENE is a read lane; PRWS submission remains a dealer action via the existing CDK–PRWS workflow. The twin never asserts a coverage code it has not read from PRWS or SIR — if PRWS is unreachable, it holds the last-known coverage state, stamps it with a staleness age, and does not synthesize.

Terms-and-conditions lane. The twin pulls the PACCAR Powertrain product pages (EPA MX-11, EPA MX-13, CARB variants, fire-apparatus variants) at ingest and refreshes weekly, extracting the coverage-duration table into JSON keyed by engine model, jurisdiction, and displacement class. It pulls the PACCAR Powertrain MX Extended Warranty PDF at ingest and refreshes monthly, parsing the extended-plan matrix. It pulls NHTSA Emission Service Bulletins for cross-reference and audit trail. It relies on the Peterbilt Warranty Procedure Manual v2026.7 and the 2025.4 Warranty Quick Reference Guide as the dealer-facing companions — both held in workspace and never re-fetched to resolve a coverage question. The twin does not interpret free-text contract language when a structured table exists. PACCAR Powertrain publishes the exact coverage math — the twin reads it as data, not prose.

## Pending walkthrough items

- Fortellis Organization setup at Hawkins — the App listing (recommended under the EVEglyphDesign Organization, consumed by the Hawkins tenant), the OAuth2 credential path, and the `Subscription-Id` provisioning. Confirm whether the CDK Drive Fortellis App is already installed at the eight rooftops.
- PACCAR Connect scope for North America — confirm with PACCAR whether Data Integration Services covers Peterbilt VINs, or whether Peterbilt telemetry remains PACCAR Solutions and SmartLINQ only for U.S. and Canada.
- Cummins RAPIDSERVE Web scope — does Hawkins service any Cummins-engine chassis outside PACCAR MX, and if so, does that warrant a separate Cummins-side read lane.
- PACCAR.net service-account credential for supplier-bulletin retrieval — same rule as elsewhere, never a personal credential.

## Non-movement covenant

The Warranty GENE reads registration and T&C data into the twin. Registration reads are recorded to Hawkins-owned Azure Postgres and never syndicated. T&C tables and coverage-duration data are non-confidential public T&Cs and may be cached in the twin's data layer alongside the schema. No customer PII enters the mapping documents in this public repository.

---

## Structured inventory

The complete data-source inventory in machine-readable form: [`registration-and-terms.json`](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/registration/registration-and-terms.json).

*Pour le bien-être du peuple.*
