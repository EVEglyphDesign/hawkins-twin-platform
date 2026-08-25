# Warranty GENE — Blueprint v2 (Two-rooftop, Azure-custody)

**Programme:** EVEglyphDesign — Warranty GENE
**Document ID:** EgD-WGB-006 · **Key ID:** EgD-KEY-2026-07
**Status:** For Tobias review, v0.2
**Posture:** Modular sidecar to the Hawkins Twin. Business data lives in the client-owned Azure server. Public replica of record lives in the [Hawkins Twin GitHub repository](https://github.com/EVEglyphDesign/hawkins-twin-platform). **EVE holds custody of nothing at rest.**
**Supersedes:** [EgD-WGB-001](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/blueprint/EgD-WGB-001-Warranty-GENE-Blueprint.pdf) — same architectural spine, retargeted to two rooftops (Peterbilt Atlantic + Torque Motorsports), custody split made explicit, AI surface made interchangeable.
**Companions:** [Wireframe v0](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/wireframe/) · [Schema v1](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/schema/) · [Luke access prep (Peterbilt)](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-prep/EgD-WGB-003-Luke-Access-Prep.pdf) · [Luke access prep (BRP)](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-prep-brp/EgD-WGB-004-Luke-Access-Prep-BRP.pdf) · [Luke contact table](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-contacts/EgD-WGB-005-Luke-Contact-Table.pdf)

---

## 1 · The POC mandate — automated OEM check first, human second step for the rest

**The POC has one job: surface, on the current book, the warranty coverage that is still valid on each VIN so the service writer knows it exists before the job closes to customer-pay.** Everything else in this blueprint is downstream of that.

The POC runs in two steps.

**Step 1 — automated OEM check.** For every VIN with an active work order on the current book at either rooftop, the engine reads what CDK Drive already carries on the Peterbilt Atlantic side and what Lightspeed EVO already carries on the Torque Motorsports side, joins it against the public OEM coverage references, and returns which OEM warranty buckets are still active on that VIN. On the Peterbilt side that is PACCAR base and extended warranty windows and the CE033 federal emissions extension. On the Torque Motorsports side that is BRP base warranty and any B.E.S.T. extended coverage the DMS record already reflects. **This step touches no third party, requires no new credential, and needs no integration built.** It uses the DMS logins Luke has today and the public references already committed to the repository.

**Step 2 — human-driven third-party check.** Third-party and extended coverage the DMS does not know about is surfaced by the humans in the loop. The service writer asks the customer whether they hold any extended warranty, service contract, or VSC on the unit — the customer knows what they bought, they usually have the paperwork with them, and if they do not know we can rely on them to check. Hawkins staff then verify manually against whichever administrator the customer names (phone or portal, whichever exists). The engine records what the customer surfaced, what Hawkins verified, and against which administrator, so the sovereign replica grows one VIN at a time — tier-3 (unknown) moves to tier-1/2 (known) for that VIN's next visit.

**Why this split is right for the POC.** Step 1 is where the automation earns its keep: the engine is faster than the service writer at seeing which OEM bucket is still open on a VIN, and it is doing that already-visible check on every VIN on the book rather than only the ones the writer thought to check. Step 2 is where the humans earn theirs: customers know their own coverage, and Hawkins staff can verify a named administrator in a minute or two. Automating step 2 needs the third-party integrations in [EgD-WGB-005](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-contacts/EgD-WGB-005-Luke-Contact-Table.pdf); the POC does not.

**Inputs the POC uses — all in hand today.**

- Luke's existing **CDK Drive** login (Peterbilt Atlantic).
- Luke's existing **Lightspeed EVO** login (Torque Motorsports).
- The **public NHTSA VIN decoder and recalls API**.
- The **public PACCAR coverage references** already committed to the [Hawkins Twin GitHub repository](https://github.com/EVEglyphDesign/hawkins-twin-platform/tree/main/warranty-gene) — base warranty windows, MX extended, CE033 federal emissions extension, WPM v2026.7 §7.
- The **public BRP base-warranty and B.E.S.T. component references**.
- The **customer's own knowledge and paperwork** for anything the DMS record does not carry — read by Hawkins staff, verified manually.

**The economic formula being tested.**

```
  additional_margin =
    Σ (line items on the current book that the engine flags in step 1 as
       covered under an active OEM warranty bucket AND that the current
       write-up path is billing customer-pay)
    + Σ (line items the customer or Hawkins staff surface in step 2 as
         covered under a third-party or extended contract AND that the
         current write-up path is billing customer-pay)
    × (labour + parts recovered at the coverage payer's rate)
    − (time cost of the automated step + the human second step)
```

The test passes if `additional_margin` is a number that clearly rewards the effort of running the POC and justifies the integration work behind it. The exact bar is Peter's to set; the POC's job is to make the number legible so Peter can set it.

**Test population.** The current booking calendar at both rooftops for a bounded window — the next few weeks the service writers are already working. Not a synthetic set, not a historical replay, not a subsample chosen to look favourable.

**What proof looks like.** A one-page rollup Tobias and Peter can read in one sitting:

- Ranked list of VINs on the current book with at least one flagged line, split into two columns: what step 1 caught automatically, what step 2 caught with a human in the loop.
- For each flagged VIN, the delta: what the current write-up bills customer-pay versus what the engine and the second-step review believe should file against a coverage bucket, cited to the coverage row.
- A warranty-administrator review column: confirm, override with reason, or reject — recorded in the choice record (§9.1).
- One rolled-up dollar figure: additional margin surfaced on the current book that the current process was not catching, over the tested window.
- A projection to a full year at the current book's cadence.

**Same engine, both rooftops.** The reasoning layer, the scoring math, the provenance stamps, and the export contract are shared. Only the source adapter and the coverage-feed roster change.

---

## 2 · Custody model — EVE holds nothing at rest

This blueprint is written to a strict custody rule Tobias should evaluate first, because every other design choice descends from it.

```
     ┌─────────────────────────┐        ┌──────────────────────────┐
     │   Azure (Hawkins-owned) │        │   GitHub (public replica │
     │   Business data of      │◄──────►│   of record — sovereign) │
     │   record. Encrypted at  │  sync  │   Non-PII. Auditable.    │
     │   rest. Access-controlled│        │   Byte-faithful mirror.  │
     └────────────┬────────────┘        └────────────┬─────────────┘
                  │                                  │
                  │  ephemeral read                  │  ephemeral read
                  ▼                                  ▼
     ┌────────────────────────────────────────────────────────────┐
     │  AI surface — interchangeable                              │
     │  (Perplexity Computer for wireframing, Claude on the       │
     │   Peterbilt-Atlantic / BRP surfaces for ad hoc use)        │
     │  Reads live. Computes in-session. Writes back to           │
     │  Azure and mirrors to GitHub. Retains nothing.             │
     └────────────────────────────────────────────────────────────┘
```

Three lanes, three custody rules:

| Layer | Who owns it | What sits there | Retention |
|-------|-------------|-----------------|-----------|
| **Azure server** (client-owned tenant) | Hawkins | Business data of record: customer records, retail-sale records, contract paperwork, VIN-linked service history, credentials for OEM and third-party portals, feed pulls from every source in §5. Encrypted at rest, access-controlled per rooftop. | Permanent, client-controlled |
| **GitHub — hawkins-twin-platform** | Hawkins (repository owner) | Public replica of record: schema, coverage ledger, blueprints, wireframes, provenance-stamped derived tables, non-PII analyses. Anything that is not in Azure gets replicated here. | Permanent, versioned, publicly auditable |
| **AI surface — Perplexity Computer / Peterbilt-Atlantic Claude / BRP Claude** | Interchangeable, session-only | Wireframing today; ad hoc queries, drafts, and one-off analyses tomorrow. Reads live from Azure and GitHub, computes in the session, writes results back to Azure and mirrors to GitHub. | **Zero at rest — session only** |

**The rule this enforces.** In the end state, EVE has custody of nothing. Every artifact EVE produces during a session lands in Hawkins's Azure server (business data) or in the Hawkins Twin GitHub repository (replica of record). Everything not in Azure gets replicated to GitHub. The AI surface — whichever one is being used — is a **compute lane, not a storage lane**.

**Interchangeable AI surface.** The reasoning is designed so that anything currently being set up in Perplexity Computer can be re-run tomorrow from the Peterbilt-Atlantic or Torque Motorsports Claude surfaces without loss. The AI surface is the wireframe; the value is in the schema, the replica of record, and the compounding decision dataset (§9). Whichever surface the operator prefers reads the same Azure lane and writes back to the same GitHub replica.

---

## 3 · The architecture, stripped to four parts (unchanged from v1)

*VIN · booking calendar · work-order table · public coverage ledger · dealer credentials · third-party VSC feeds*

```
  1. Source adapter       2. Reasoning              3. Delivery
  VIN + WO in         →   coverage join    →        Browser wizard
  (CDK Drive /            + scoring +               (three modes)
   Lightspeed EVO /       uplift scan                   ⋮
   Excel drop)                ⋮
                        4. Observability — every join, decision, and
                        provenance stamp recorded; every answer replayable
                        against the Azure record and the GitHub replica

           (compute in-session; state in Azure + GitHub)
```

Four parts, each replaceable on its own — identical to the v1 spine.

- **Source adapter** — crosses the boundary from CDK Drive (Peterbilt side), Lightspeed EVO (BRP side), OEM portals, and third-party administrator portals into a uniform "VIN + coverage + work-order + owner + contract" shape.
- **Reasoning** — a bounded set of joins and scored answers. Deterministic pipeline; no open-ended language-model loop. Same on both sides.
- **Delivery** — the browser wizard (single VIN / work-order uplift / cohort scan). Same page, same flow, both rooftops.
- **Observability** — provenance stamps on every field. Every answer replayable against the Azure record and the GitHub replica.

| Component | Peterbilt Atlantic | Torque Motorsports | What that involves |
|-----------|:-------------:|:-------------:|--------------------|
| Reasoning engine (coverage math + scoring) | **Live** | **Live** | Reused unchanged both sides |
| Browser wizard (three modes) | **Live** | **Live** | Same page, same flow |
| Public coverage ledger | **Live** | Configured | Truck: NHTSA CE033, MX 2025 Extended, WPM v2026.7. Powersports: BRP B.E.S.T., third-party VSC references |
| Provenance / audit ledger | **Live** | **Live** | Same stamp taxonomy |
| Source adapter | Configured (CDK Drive) | Configured (Lightspeed EVO) | Point at rooftop DMS export path |
| Dealer credential set | Pending Luke | Pending Luke | Twenty-one counterparties from [EgD-WGB-005](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-contacts/EgD-WGB-005-Luke-Contact-Table.pdf) |
| Rooftop map | Peterbilt Atlantic rooftops | Torque Motorsports rooftops | Configured per engagement |

*Table 1: Four parts are reused as-is on both sides; three are configured per rooftop. None is a new build.*

---

## 4 · How it reasons, and why every answer is auditable

Fixed path, same on both sides:

```
  Decode        Anchor        Coverage         Job           Uplift         Rank
  the VIN   →   coverage  →   window   →       scoring   →   scan  →        and
  (NHTSA on     to date        math                          (WO mode)      narrate
   truck;       (DMS or        (public                                      (per VIN
   BRP VIN      contract)      + private                                    or cohort)
   decode                      ledger)
   on power-
   sports)
```

Two worked examples — one per side.

```
  PETERBILT ATLANTIC — SERVICE WRITER
  Anything on today's book that should be warranty instead of customer-pay?

  ANSWER
  Three of today's twelve booked VINs have jobs under an active coverage bucket.
  VIN 1XPBSYN00…202 is booked for a DEF dosing valve — the CE033 federal
  emissions extension covers this until 2033-09-05 and it has not been claimed.
  Recovery-at-risk on today's book: $4,180 customer-pay that could be filed as
  warranty if the write-ups are corrected before close.
```

```
  TORQUE MOTORSPORTS — SERVICE WRITER
  Sea-Doo in the bay for a supercharger rebuild. Anything on the coverage side
  I should know before I write this up customer-pay?

  ANSWER
  This VIN has an active BRP B.E.S.T. plan that runs through 2027-05-14; the
  supercharger clutch and drive shaft are in the B.E.S.T. component list. The
  customer also has an Assurant policy on file — the sovereign replica already
  holds the contract number. B.E.S.T. is the first-position payer for this
  component; file B.E.S.T. before Assurant. Recovery-at-risk if written
  customer-pay: $2,340.
```

Two properties, unchanged from v1 and now more important given the custody model:

- **Bounded and auditable.** Every coverage number cited on the card links to the source row in Azure or the mirrored copy in GitHub. Every score decomposes into `recovery × urgency × margin`.
- **Zero data leakage at rest, fully replayable.** The reasoning runs in-session on whichever AI surface the operator chose. Business data is read live from Azure; the public coverage ledger is read from GitHub. When a warranty administrator asks "how do you know this VIN was still under CE033?" or "how do you know B.E.S.T. covers the supercharger clutch?", the honest answer is: replay it against the Azure record and the GitHub ledger row.

### 4.1 Built to pass a warranty audit on both sides

The audit question is finite by design. Truck-side: reads the dealer's own PRWS session (invitation-only, credential held in Azure) or the public NHTSA / PACCAR ledger (no credential). Powersports side: reads the dealer's BOSSWeb session and third-party administrator portals (invitation-only, credentials held in Azure) or the BRP public B.E.S.T. references. **Nothing sensitive leaves Azure; nothing at all stays on the AI surface.**

---

## 5 · Where the data lives — Azure of record, GitHub replica, in-session compute

The custody model in §2 dictates the data-locality picture. There is no third database. There is Azure (of record), GitHub (replica of record), and the session tab (compute only).

### 5.1 Live sources, both rooftops

The adapter reads live. Everything read is written back to Azure and mirrored to GitHub as a non-PII derived row.

| Live source | Rooftop | Typical use | Custody after read |
|-------------|:---:|-------------|--------------------|
| **NHTSA VIN decoder API** (public) | Peterbilt | Identity for any Class 8 VIN | GitHub (public), Azure (audit copy) |
| **NHTSA recalls-by-VIN API** (public) | Peterbilt | Open recalls per VIN | GitHub (public), Azure (audit copy) |
| **PACCAR public coverage ledger** | Peterbilt | Base warranty, extended, CE033 | GitHub (public), Azure (audit copy) |
| **PRWS** — retail-sale, coverage codes | Peterbilt | Invitation-only | Azure only; non-PII summary to GitHub |
| **PACCAR Solutions / SmartLINQ** — telemetry, DTCs | Peterbilt | Invitation-only | Azure only; non-PII summary to GitHub |
| **PSSM Decisiv** — point-of-service coverage | Peterbilt | Invitation-only | Azure only; non-PII summary to GitHub |
| **CDK Drive / Fortellis** — DMS | Peterbilt | Booking calendar, RO, service history | Azure only; non-PII summary to GitHub |
| **Big-5 truck component portals** — Cummins QuickServe, Eaton my.eaton.com, Allison HUB, Cummins-Meritor OnTrac, Bendix, ZF, Dana RTW | Peterbilt | Component-level coverage and warranty claim | Azure only; non-PII summary to GitHub |
| **BRP VIN decoder / B.E.S.T. lookup** | BRP | Identity + extended plan status | GitHub (public), Azure (audit copy) |
| **Lightspeed EVO** — DMS | BRP | Booking calendar, RO, deal, customer | Azure only; non-PII summary to GitHub |
| **BOSSWeb** — BRP dealer portal, warranty | BRP | Warranty claim entry, B.E.S.T. status | Azure only; non-PII summary to GitHub |
| **Assurant, Portfolio, EasyCare, Zurich** — wave-one VSC administrators | BRP | Contract lookup by VIN, claim status | Azure only; non-PII summary to GitHub |
| **Protective/ProGuard, GWC/CornerStone** — wave-two VSC administrators | BRP | Contract lookup by VIN, claim status | Azure only; non-PII summary to GitHub |
| **Bank/CU-branded VSC administrators** (Ally, GM Financial, Chase, TD Auto, Desjardins, RBC, and any surfaced at the counter) | BRP | Contract-holder resolution for on-the-spot claims | Azure only; non-PII summary to GitHub |
| **Selling-dealer outreach** (phone) | BRP | Contract resolution when the sovereign replica does not yet hold it | Azure only |

*Table 2: Twenty-one classes of source across two rooftops. Azure is the write destination for every one; the GitHub replica receives the non-PII derived summary. The AI surface holds none of this at rest.*

### 5.2 Compute in-session, on whichever AI surface

Once data is read, analysis happens entirely in the session on the AI surface the operator chose. Two engines cover the two kinds of question:

| Working engine | Best at | Lifespan | Where results land |
|----------------|---------|----------|--------------------|
| **Coverage-math kernel** (deterministic) | Anchor date + engine family → window remaining per bucket per VIN | Per session | Azure (audit) + GitHub (non-PII derived) |
| **Uplift scanner** (component-name matcher) | Work-order line item → coverage bucket + confidence tier | Per session | Azure (audit) + GitHub (non-PII derived) |
| **Cohort ranker** (score sort) | Batch of VINs → top-N by composite score | Per session | Azure (audit) + GitHub (non-PII derived) |

*Table 3: Analysis is built in the tab, written to Azure and GitHub, then discarded from the tab.*

**AI surface interchangeability.** The three engines are specified deterministically enough that the same VIN and the same coverage ledger yield the same answer whether the session runs on Perplexity Computer (today) or on the Peterbilt-Atlantic / Torque Motorsports Claude surfaces (tomorrow). The AI surface is a wireframe and an ad hoc reasoning lane; it is not the system of record and it is not the source of truth for any coverage or claim outcome.

---

## 6 · What it takes to point at Torque Motorsports

Configuration, not build. Reusing the v1 pattern (§6 of EgD-WGB-001) applied to the BRP side, and drawing every counterparty from [EgD-WGB-005](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-contacts/EgD-WGB-005-Luke-Contact-Table.pdf).

| Item | Who provisions | Cost | Blocker? |
|------|---------------|------|----------|
| Rooftop list and BRP-line map | Dealer operations | Free | No |
| Lightspeed EVO export path (or Client Portal API) | Dealer service manager | Contract-dependent | No — paste-in fallback |
| BRP VIN decode / public B.E.S.T. references | Public | Free | No |
| BOSSWeb dealer portal (BRP corporate) | Luke via BRP corporate | Free | **Yes — commercial** |
| Wave-one VSC administrators (Assurant, Portfolio, EasyCare, Zurich) | Luke | Free | **Yes — commercial** |
| Wave-two VSC administrators (Protective/ProGuard, GWC/CornerStone) | Luke | Free | **Yes — commercial** |
| Bank/CU-branded VSC administrators | Per-customer, on-the-spot | Free | No — on-the-spot workflow |
| Selling-dealer outreach protocol | Luke's service writer | Free | No — always available as fallback |
| Peter's authorization for both rooftops' subscriptions | Peter | Some subscriptions carry monthly fees | **Yes — internal** |

For Torque Motorsports, items 1–3 and 7–8 are ready today. Items 4–6 and 9 are the subject of [EgD-WGB-004](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-prep-brp/EgD-WGB-004-Luke-Access-Prep-BRP.pdf), sent all at once (not sequentially) per operator direction.

---

## 7 · The delivery surfaces

Three surfaces, same page, same flow, both rooftops:

| Surface | Who uses it | Question answered |
|---------|-------------|-------------------|
| **Single VIN wizard** | Service writer, warranty administrator, both rooftops | "Is this VIN still under warranty (OEM base, extended, CE033, B.E.S.T., or third-party VSC) for the work I'm about to invoice?" |
| **Work-order uplift** | Warranty administrator, fixed-ops director | "Which line items on today's ROs could shift from customer-pay to warranty, and which payer is first-position?" |
| **VIN batch scan** | Fixed-ops director, dealer principal | "Across the next four weeks of bookings, where are we not getting at the big warranty jobs?" |

Every surface produces the same three exports (PDF, CSV, JSON). Every surface writes its computation trail back to Azure and mirrors the non-PII derived row to GitHub — including which payer was chosen, which was rejected, and why. That last piece is what §9 compounds.

---

## 8 · How this scales beyond Hawkins

The Warranty GENE is a **sidecar** — integral to the Hawkins Twin, and a standalone subscription for every other dealership.

| Subscription tier | What the dealer gets | What EgD does |
|-------------------|---------------------|---------------|
| **Public ledger only** | Wireframe + NHTSA/BRP public references + paste-in + exports. Any dealer, any brand. | Zero-touch. Dealer signs up, uses the tool. |
| **Dealer-authorized** | Above + configured source adapter for the dealer's DMS (CDK Drive, Lightspeed EVO, Karmak, Procede Excede, SERTI, TCS365) + integration with the dealer's OEM and VSC portal sessions. Dealer's own Azure tenant holds the business data. | One configuration engagement per rooftop family. Reasoning engine reused unchanged. |
| **Twin-integrated (Hawkins tier)** | Above + full integration with the Hawkins Twin: territory relationship, telemetry lane, PM/compliance overlay, historical claim ledger, cross-rooftop customer twin (Peterbilt Atlantic + Torque Motorsports under one customer record when the same customer appears on both). | The tier Hawkins is running. Sidecar becomes an integral organ of the twin. |

**Custody rule is invariant across tiers.** Every subscriber owns their own Azure tenant and their own repository fork. EVE has no cross-tenant data access, ever. The reasoning engine is portable code; the schema is a public standard; the data always sits with the dealer.

---

## 9 · Strategic frame — the compounding decision dataset

The v1 blueprint framed the strategy as an industry-specific record repository. That is still correct, and this v2 tightens the frame to name the specific compounding asset the two-rooftop configuration creates.

Every VIN that flows through the engine leaves behind two things:

1. **A structured record** (customer twin + equipment twin — v1 §9.1, unchanged), written to Azure and mirrored to GitHub.
2. **A choice record** — the human decision made at the write-up bay: which coverage bucket was picked, which payer was written first, which was rejected, and why. This is new to v2.

### 9.1 The choice record

Every warranty write-up is a human decision under uncertainty. On the Peterbilt side, the writer picks between OEM base, extended, CE033, or customer-pay. On the BRP side, the writer picks between OEM base, B.E.S.T., a specific third-party VSC, a bank-branded VSC, or customer-pay. **Every one of those choices is a data point about which coverage recommendation was the right one for that job, that customer, and that VIN.**

The choice record is written alongside the twin record: `(VIN, work-order line, recommended payer, chosen payer, reason if different, outcome after claim, days-to-payment, dollars recovered)`. Non-PII. Mirrored to GitHub. Accumulates.

### 9.2 Why the choice record is the compounding asset

Three properties make it worth writing carefully from day one:

- **It grades the engine.** The gap between recommended payer and chosen payer is the engine's error rate. Small consistent gaps mean the engine is missing something the human sees; the fix is a new coverage rule or a better join. Large one-off gaps mean the human overrode the engine; the reason field explains why.
- **It compounds across rooftops.** A customer with both a Peterbilt truck and a BRP powersport (Hawkins has these) generates two choice records tied to one customer twin. Patterns across rooftops — "this customer always chooses to file B.E.S.T. before Assurant" — become recommendations for the next visit and the next customer of that shape.
- **It becomes a training signal, later.** Once the choice record has a season of history, a model that learns from it can propose the payer sequence directly instead of routing every write-up through the deterministic engine. That model would run on the same interchangeable AI surface described in §2. **The choice record is what turns the engine into an assistant that gets better every week without new engineering.**

### 9.3 The industry repository play, restated

The v1 §9.3 argument holds: as the Hawkins Twin accumulates records across two rooftops (and across peer dealers who subscribe on the tiers in §8), it becomes the first meaningful sample of the standard structure filled with real Class 8 truck and BRP powersports operator data. The **choice record is the second layer** — the first sample of real dealer-side warranty decision data, likewise vendor-neutral and provenance-stamped.

Warranty GENE is the first tenant. The record repository is the landlord. The choice record is what makes the landlord smarter every quarter. **Hawkins is building the landlord.**

---

## 10 · Integrations — the value added, articulated

Tobias will want each integration named against what it adds to Hawkins's dataset (not what it does for EVE — EVE has no dataset).

| Integration | Adds to Hawkins's dataset | Compounds because |
|-------------|--------------------------|-------------------|
| **CDK Drive (Peterbilt)** | Live booking calendar, RO history, current mileage — the substrate every truck-side answer joins against | Same substrate feeds recall recovery, resale valuation, PM planning tomorrow — one integration, many services |
| **Lightspeed EVO (BRP)** | Live booking calendar, RO history, deal + customer records — the substrate every powersports answer joins against | Same substrate feeds seasonality-aware bookings, cross-line customer profiles, third-party VSC reconciliation tomorrow |
| **PRWS + PACCAR Solutions + PSSM Decisiv** | Truck-side coverage windows, telemetry, point-of-service coverage — the fields the twin needs that CDK does not carry | Turns every service event on a Peterbilt VIN into a payer-first write-up instead of a customer-pay-by-default one |
| **Big-5 truck component portals** (Cummins, Eaton, Allison, Cummins-Meritor, Bendix, ZF, Dana) | Component-level coverage — Cummins engine block covered separately from the Peterbilt chassis, etc. | Answers component-level "who pays" questions the OEM portal cannot, and produces the choice records that grade component-level coverage recommendations |
| **BOSSWeb + BRP B.E.S.T.** | Powersports coverage windows and extended plan status — the analog of PRWS on the BRP side | Turns every service event on a BRP VIN into a payer-first write-up |
| **Wave-one + wave-two + bank-branded VSC administrators** | Third-party coverage on the powersports side — a denser layer than the truck side | Every third-party claim is a choice record; over a season, the engine learns which administrator pays which class of claim reliably |
| **Selling-dealer outreach** | Contract resolution for the long tail of unknown administrators | Every resolved case moves that VIN from tier-3 (unknown) to tier-1/2 (known) for every future visit — the sovereign replica grows without new subscriptions |
| **Interchangeable AI surface** (Perplexity Computer / Peterbilt-Atlantic Claude / BRP Claude) | A wireframe today, an ad hoc reasoning lane every day, a learned recommender tomorrow (§9.2) | The value is portable across surfaces because the schema and the replica are the durable layer; the surface is not |

*Table 4: Every integration is a feed into Hawkins's Azure + GitHub. None is a feed into EVE.*

---

## 11 · What is not in this blueprint

Called out so nothing is presumed:

- **Cross-brand support beyond Peterbilt and BRP.** Cummins-powered non-Peterbilt chassis, DTNA, Volvo, Kenworth on the truck side; Polaris, Yamaha, Honda on the powersports side. Not on the Hawkins critical path.
- **Write-back to PRWS or BOSSWeb.** Read-only in this design. A warranty administrator files the claim through the OEM portal the normal way, using the twin card as the write-up input.
- **Warranty claim submission automation.** Out of scope; regulated by each OEM and administrator.
- **Customer PII.** Full PII lives in Azure only; the GitHub replica carries non-PII derived rows. The rendering rule for owner names on the delivery surfaces is set by the dealer principal per rooftop.
- **EVE holding any data at rest.** Not in scope. Not in this design. Not in any future revision of this design.

---

## 12 · Review questions for Tobias

Called out so the review is efficient:

1. Is the three-lane custody model (§2) — Azure of record, GitHub replica, session-only compute — the right long-term architecture, or does Tobias want a variant?
2. Is the AI-surface interchangeability rule (§2, §5.2) — same schema, same replica, same answers whether Perplexity Computer or Claude runs the session — worth pinning as a design constraint, or is it an implementation detail?
3. Is the choice record (§9.1) worth writing from day one, or should it wait until the twin records themselves are stable? EgD's recommendation is day-one, because the compounding is what turns the engine into an assistant.
4. On the powersports side, does Torque Motorsports have a BRP district-manager relationship already? That fills the one gap left in [EgD-WGB-005 row 12](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-contacts/EgD-WGB-005-Luke-Contact-Table.pdf).
5. Any Tobias-specific integration requirements (identity, SSO, audit-log format) that should be added to §10 before the twin repository schema is frozen?

---

## 13 · Provenance

- [Warranty GENE wireframe](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/wireframe/)
- [Warranty GENE schema v1](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/schema/)
- [Warranty GENE field mappings](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/mappings/)
- [Warranty GENE registration inventory](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/registration/)
- [Warranty GENE blueprint v1 (EgD-WGB-001)](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/blueprint/EgD-WGB-001-Warranty-GENE-Blueprint.pdf)
- [Luke access prep — Peterbilt (EgD-WGB-003)](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-prep/EgD-WGB-003-Luke-Access-Prep.pdf)
- [Luke access prep — BRP (EgD-WGB-004)](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-prep-brp/EgD-WGB-004-Luke-Access-Prep-BRP.pdf)
- [Luke contact table (EgD-WGB-005)](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-contacts/EgD-WGB-005-Luke-Contact-Table.pdf)
- [Hawkins Twin Platform repository](https://github.com/EVEglyphDesign/hawkins-twin-platform)
- [NHTSA VIN decoder API](https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/1XPBSYN00N1000101?format=json)
- [NHTSA CE033 bulletin (federal emissions extension, EMY2023 MX-11/MX-13)](https://static.nhtsa.gov/odi/tsbs/2025/MC-11021404-0001.pdf)

Dealer-document provenance (not publicly URL-addressable): Warranty Procedure Manual v2026.7 §7 and §Contacts, Warranty Quick Reference Guide 2025.4, BRP B.E.S.T. component list (dealer-portal-held).

---

© 2026 EVEglyphDesign. All rights reserved. Controlled copy.
*Pour le bien-être du peuple.*
