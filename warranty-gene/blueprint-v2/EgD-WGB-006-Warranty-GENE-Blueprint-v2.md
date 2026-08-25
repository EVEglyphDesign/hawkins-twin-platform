# Warranty GENE — Blueprint v2 (Two-rooftop, Azure-custody)

**Programme:** EVEglyphDesign — Warranty GENE
**Document ID:** EgD-WGB-006 · **Key ID:** EgD-KEY-2026-07
**Status:** For Tobias review, v0.2
**Posture:** Modular sidecar to the Hawkins Twin. Business data lives in the client-owned Azure server. Public replica of record lives in the [Hawkins Twin GitHub repository](https://github.com/EVEglyphDesign/hawkins-twin-platform). **EVE holds custody of nothing at rest.**
**Operating model:** Warranty GENE runs as a **two-step process on every VIN, every visit** — step 1 is an automated OEM coverage check from the DMS record, step 2 is a human-driven third-party check by the customer and the Hawkins service writer. Integrations tighten step 2 over time; they do not gate it.
**Supersedes:** [EgD-WGB-001](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/blueprint/EgD-WGB-001-Warranty-GENE-Blueprint.pdf) — same architectural spine, retargeted to two rooftops (Peterbilt Atlantic + Torque Motorsports), custody split made explicit, AI surface made interchangeable, **two-step operating model made primary**.
**Companions:** [Wireframe v0](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/wireframe/) · [Schema v1](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/schema/) · [Luke access prep (Peterbilt)](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-prep/EgD-WGB-003-Luke-Access-Prep.pdf) · [Luke access prep (BRP)](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-prep-brp/EgD-WGB-004-Luke-Access-Prep-BRP.pdf) · [Luke contact table](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-contacts/EgD-WGB-005-Luke-Contact-Table.pdf)

---

## 1 · Operating model — two steps on every VIN, every visit

**Warranty GENE operates as a two-step check on every VIN with an active work order, at both rooftops, every visit.** The two steps are the primary operating model, not a POC scaffold. Integrations tighten step 2 over time; they do not gate it and they do not replace it. The customer's own knowledge stays in the loop even after every third-party portal is wired up, because the customer is the highest-confidence source of what they actually hold.

### 1.1 The two steps

**Step 1 — automated OEM coverage check.** For every VIN with an active work order at either rooftop, the engine reads what CDK Drive already carries on the Peterbilt Atlantic side and what Lightspeed EVO already carries on the Torque Motorsports side, joins it against the public OEM coverage references, and returns which OEM warranty buckets are still active on that VIN. On the Peterbilt side that is PACCAR base and extended warranty windows and the CE033 federal emissions extension. On the Torque Motorsports side that is BRP base warranty and any B.E.S.T. extended coverage the DMS record already reflects. **This step touches no third party, requires no new credential, and needs no integration built.** It uses the DMS logins Luke has today and the public references already committed to the repository. It runs on every VIN, every visit, forever — not just during the POC.

**Step 2 — human-driven third-party check.** Everything the DMS record does not know about is surfaced by the humans in the loop. The service writer asks the customer whether they hold any extended warranty, service contract, or VSC on the unit — the customer knows what they bought, they usually have the paperwork with them, and if they do not know we can rely on them to check. Hawkins staff then verify against whichever administrator the customer names, using whatever channel is fastest at that moment (customer-provided paperwork, a phone call to the administrator, a portal login if Hawkins already has one). The engine records what the customer surfaced, what Hawkins verified, and against which administrator, so the sovereign replica grows one VIN at a time — tier-3 (unknown) moves to tier-1/2 (known) for that VIN's next visit. **Step 2 runs on every VIN, every visit, forever — even after every third-party integration is wired up, because the customer's knowledge is upstream of every portal.**

### 1.2 Why two steps, not one

The automation and the human are good at different things and the operating model has to reflect that.

- **Step 1** is where the automation earns its keep. The engine is faster than the service writer at seeing which OEM bucket is still open on a VIN, and it is doing that already-visible check on every VIN on the book rather than only the ones the writer thought to check. It also does not tire, does not forget CE033 exists on EMY2023 MX engines, and does not miss a B.E.S.T. plan the DMS record already reflects.
- **Step 2** is where the humans earn theirs. Customers know their own coverage — they signed the contract, they hold the booklet, they remember what the finance manager sold them. Hawkins staff can verify a named administrator in a minute or two. And when the DMS record and the customer disagree, the human is the tiebreaker, not the machine.

Every third-party portal integration in [EgD-WGB-005](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-contacts/EgD-WGB-005-Luke-Contact-Table.pdf) makes step 2 faster and more precise — same call, done from a screen instead of a phone — but none of them replaces step 2. The customer's own knowledge is upstream of every portal.

### 1.3 What each step writes back

Every run of the two-step check writes back to the sovereign replica exactly what it saw, so the next visit for the same VIN starts closer to complete than the last one did.

- **Step 1 writes back:** the OEM buckets still active for this VIN, the anchor date, the window remaining, the coverage row cited, and the DMS record that fed it.
- **Step 2 writes back:** the third-party administrator the customer named, the contract identifier if produced, the coverage the administrator confirmed, the human who verified it, the channel used (paperwork / phone / portal), and the time it took. Every negative answer ("customer holds no third-party coverage on this VIN") is written back with the same rigour, because a confirmed negative is what keeps step 2 from re-asking on the next visit.

### 1.4 The POC — first four weeks of the operating model

The POC is not a different mode of operation. It is the first four weeks of the two-step model running on the current booking calendar at both rooftops, measured. The economic formula the POC tests is the formula the operating model runs on forever:

```
  additional_margin =
    Σ (line items where step 1 flagged an active OEM warranty bucket
       AND the current write-up path is billing customer-pay)
    + Σ (line items where step 2 surfaced a third-party or extended
         contract AND the current write-up path is billing customer-pay)
    × (labour + parts recovered at the coverage payer's rate)
    − (time cost of the automated step + the human second step)
```

The POC exists to make the number legible so Peter can set the bar for how much margin justifies the ongoing operation. If the first four weeks clear that bar, the two-step model keeps running as-is. Integrations named in §10 are added over time to compress the time cost of step 2, one counterparty at a time, with each addition paid for by the margin it reduces the friction of collecting.

**Inputs required today — all in hand.**

- Luke's existing **CDK Drive** login (Peterbilt Atlantic).
- Luke's existing **Lightspeed EVO** login (Torque Motorsports).
- The **public NHTSA VIN decoder and recalls API**.
- The **public PACCAR coverage references** already committed to the [Hawkins Twin GitHub repository](https://github.com/EVEglyphDesign/hawkins-twin-platform/tree/main/warranty-gene) — base warranty windows, MX extended, CE033 federal emissions extension, WPM v2026.7 §7.
- The **public BRP base-warranty and B.E.S.T. component references**.
- The **customer's own knowledge and paperwork** for anything the DMS record does not carry — read by Hawkins staff, verified manually.

**What proof looks like at the end of the first four weeks.** A one-page rollup Tobias and Peter can read in one sitting:

- Ranked list of VINs seen in the window with at least one flagged line, split into two columns: what step 1 caught automatically, what step 2 caught with a human in the loop.
- For each flagged VIN, the delta: what the current write-up bills customer-pay versus what the two-step check believes should file against a coverage bucket, cited to the coverage row.
- A warranty-administrator review column: confirm, override with reason, or reject — recorded in the choice record (§9.1).
- One rolled-up dollar figure: additional margin surfaced over the window that the previous process was not catching.
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

## 3 · The architecture, stripped to four parts (unchanged from v1, run in two steps)

*VIN · booking calendar · work-order table · public coverage ledger · dealer credentials · third-party VSC feeds*

```
  1. Source adapter       2. Reasoning              3. Delivery
  VIN + WO in         →   step 1: OEM      →        Browser wizard
  (CDK Drive /            coverage join              (three modes,
   Lightspeed EVO /       step 2: capture             each shows
   Excel drop)            of human-verified           step-1 and
                          third-party coverage        step-2 rows
                                ⋮                     side by side)
                        4. Observability — every join, decision, and
                        provenance stamp recorded; every answer replayable
                        against the Azure record and the GitHub replica

           (compute in-session; state in Azure + GitHub)
```

Four parts, each replaceable on its own — identical to the v1 spine, wired through the two-step operating model (§1).

- **Source adapter** — crosses the boundary from CDK Drive (Peterbilt side), Lightspeed EVO (BRP side), OEM portals, and third-party administrator portals into a uniform "VIN + coverage + work-order + owner + contract" shape. Public references feed step 1; third-party portal integrations (when they exist) accelerate step 2 without replacing the human check.
- **Reasoning** — a bounded set of joins and scored answers. Deterministic pipeline; no open-ended language-model loop. Same on both sides. Runs step 1 automatically on every VIN; consumes the step-2 record the humans produce and re-scores the VIN once it lands.
- **Delivery** — the browser wizard (single VIN / work-order uplift / cohort scan). Same page, same flow, both rooftops. **Every surface renders step 1 (automated) and step 2 (human-verified) as adjacent, equally-weighted rows** so the write-up decision sees both.
- **Observability** — provenance stamps on every field. Every answer replayable against the Azure record and the GitHub replica. Step 1 provenance is `(coverage row, DMS record, timestamp)`; step 2 provenance is `(administrator named by customer, channel used, human verifier, timestamp)`.

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

Fixed path, same on both sides, threaded through the two-step operating model.

```
  Decode VIN  →  Step 1: OEM check  →  Anchor date  →  Step 2: human
  (NHTSA on      (DMS record +           (retail-sale     third-party
   truck;         public PACCAR /         date or         check
   BRP VIN        BRP ledger;             contract)       (customer +
   decode on      automated,                              Hawkins staff,
   powersports)   seconds/VIN)                            minutes/VIN)

                                                              ↓

              Rank + narrate  ←  Uplift scan  ←  Job scoring
              (per VIN or        (work-order      (sums step-1
               cohort)            mode)            + step-2 buckets)
```

Step 1 runs unattended and completes in seconds per VIN. Step 2 runs when the customer is at the counter, or asynchronously against paperwork already on file, and completes in minutes per VIN. The engine does not wait for step 2 to render step-1 answers, and it does not overwrite step-1 answers when step 2 lands; both steps write into the same VIN record and the score is the sum.

Two worked examples — one per side, both steps shown.

```
  PETERBILT ATLANTIC — SERVICE WRITER
  Anything on today's book that should be warranty instead of customer-pay?

  STEP 1 (automated, OEM)
  Three of today's twelve booked VINs have jobs under an active OEM bucket.
  VIN 1XPBSYN00…202 is booked for a DEF dosing valve — the CE033 federal
  emissions extension covers this until 2033-09-05 and it has not been claimed.

  STEP 2 (human, third-party)
  Ask the customer for VIN …202 whether they hold any extended service
  contract on the truck. If yes, verify against the administrator and record
  the coverage row. If no, record the confirmed negative so we don't re-ask
  next visit.

  RECOVERY-AT-RISK on today's book: $4,180 customer-pay that could be filed
  as warranty if the write-ups are corrected before close (step 1 only;
  step 2 may add).
```

```
  TORQUE MOTORSPORTS — SERVICE WRITER
  Sea-Doo in the bay for a supercharger rebuild. Anything on the coverage side
  I should know before I write this up customer-pay?

  STEP 1 (automated, OEM)
  This VIN has an active BRP B.E.S.T. plan that runs through 2027-05-14 in the
  DMS record; the supercharger clutch and drive shaft are in the B.E.S.T.
  component list. Base warranty is expired.

  STEP 2 (human, third-party)
  The sovereign replica already holds an Assurant contract number for this
  customer from a prior visit — confirm with the customer it is still
  active, or capture any new contract they surface. B.E.S.T. is the first-
  position payer for this component; file B.E.S.T. before Assurant.

  RECOVERY-AT-RISK if written customer-pay: $2,340 (B.E.S.T. + Assurant
  stack, step-2 confirmation pending).
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

## 7 · The delivery surfaces — every one runs the two-step model

Three surfaces, same page, same flow, both rooftops. Every surface renders step 1 and step 2 as adjacent rows so the write-up decision sees both.

| Surface | Who uses it | Step 1 (automated) shows | Step 2 (human) shows |
|---------|-------------|--------------------------|----------------------|
| **Single VIN wizard** | Service writer, warranty administrator, both rooftops | OEM buckets still active on this VIN and the covered line items on the current work order | Prompt to ask the customer about third-party coverage; capture form with administrator, contract number, coverage confirmed, channel used |
| **Work-order uplift** | Warranty administrator, fixed-ops director | Every OEM-covered line across today's ROs, ranked by recovery-at-risk | Every VIN on today's ROs that still needs a step-2 conversation, sorted by time-since-last-asked |
| **VIN batch scan** | Fixed-ops director, dealer principal | Cohort-level OEM coverage opportunity across the next four weeks of bookings | Cohort-level step-2 backlog: which upcoming VINs have never had a third-party check completed |

Every surface produces the same three exports (PDF, CSV, JSON). Every surface writes both step-1 and step-2 computation trails back to Azure and mirrors the non-PII derived row to GitHub — including which payer was chosen, which was rejected, and why. That last piece is what §9 compounds.

---

## 8 · How this scales beyond Hawkins

The Warranty GENE is a **sidecar** — integral to the Hawkins Twin, and a standalone subscription for every other dealership.

| Subscription tier | What the dealer gets | What EgD does |
|-------------------|---------------------|---------------|
| **Public ledger only** | Wireframe + NHTSA/BRP public references + paste-in + exports. Any dealer, any brand. | Zero-touch. Dealer signs up, uses the tool. |
| **Dealer-authorized** | Above + configured source adapter for the dealer's DMS (CDK Drive, Lightspeed EVO, Karmak, Procede Excede, SERTI, TCS365) + integration with the dealer's OEM and VSC portal sessions. Dealer's own Azure tenant holds the business data. | One configuration engagement per rooftop family. Reasoning engine reused unchanged. |
| **Twin-integrated (Hawkins tier)** | Above + full integration with the Hawkins Twin: territory relationship, telemetry lane, PM/compliance overlay, historical claim ledger, cross-rooftop customer twin (Peterbilt Atlantic + Torque Motorsports under one customer record when the same customer appears on both). | The tier Hawkins is running. Sidecar becomes an integral organ of the twin. |

**Custody rule is invariant across tiers.** Every subscriber owns their own Azure tenant and their own repository fork. EVE has no cross-tenant data access, ever. The reasoning engine is portable code; the schema is a public standard; the data always sits with the dealer.

**Operating model is invariant across tiers.** Every subscriber, every tier, runs the same two-step model on every VIN. The public-ledger tier runs it against public references and paste-in inputs; the dealer-authorized tier runs it against integrated DMS and portal feeds; the twin-integrated tier runs it against the full Hawkins Twin. The steps are the same; the friction on step 2 is what higher tiers reduce.

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

## 10 · Integrations — what each one does for the two-step model

Every integration is named against which step it feeds and what it adds to Hawkins's dataset (not what it does for EVE — EVE has no dataset). Nothing here gates the operating model; step 1 and step 2 already run today with the inputs listed in §1. Integrations compress the time cost of step 2 (or add depth to step 1) one counterparty at a time.

| Integration | Feeds which step | Adds to Hawkins's dataset | Compounds because |
|-------------|------------------|--------------------------|-------------------|
| **CDK Drive (Peterbilt)** | Step 1 (already in hand) | Live booking calendar, RO history, current mileage — the substrate step 1 joins against | Same substrate feeds recall recovery, resale valuation, PM planning tomorrow — one integration, many services |
| **Lightspeed EVO (BRP)** | Step 1 (already in hand) | Live booking calendar, RO history, deal + customer records — the substrate step 1 joins against | Same substrate feeds seasonality-aware bookings, cross-line customer profiles, third-party VSC reconciliation tomorrow |
| **PRWS + PACCAR Solutions + PSSM Decisiv** | Step 1 (adds depth) | Truck-side coverage windows, telemetry, point-of-service coverage — fields step 1 needs that CDK does not carry | Turns every service event on a Peterbilt VIN into a payer-first write-up instead of a customer-pay-by-default one |
| **Big-5 truck component portals** (Cummins, Eaton, Allison, Cummins-Meritor, Bendix, ZF, Dana) | Step 1 (adds depth) | Component-level coverage — Cummins engine block covered separately from the Peterbilt chassis, etc. | Answers component-level "who pays" questions the OEM portal cannot; produces the choice records that grade component-level coverage recommendations |
| **BOSSWeb + BRP B.E.S.T.** | Step 1 (adds depth) | Powersports coverage windows and extended plan status — the analog of PRWS on the BRP side | Turns every service event on a BRP VIN into a payer-first write-up |
| **Wave-one + wave-two + bank-branded VSC administrators** | Step 2 (compresses friction) | Third-party coverage on the powersports side — same coverage that step 2 collects by phone today, collected from a portal tomorrow | Every third-party claim is a choice record; over a season, the engine learns which administrator pays which class of claim reliably. Does **not** remove the customer conversation — verifies faster what the customer already surfaced |
| **Selling-dealer outreach** | Step 2 (long tail) | Contract resolution for the long tail of unknown administrators | Every resolved case moves that VIN from tier-3 (unknown) to tier-1/2 (known) for every future visit — the sovereign replica grows without new subscriptions |
| **Interchangeable AI surface** (Perplexity Computer / Peterbilt-Atlantic Claude / BRP Claude) | Both steps (compute lane) | A wireframe today, an ad hoc reasoning lane every day, a learned recommender tomorrow (§9.2) | The value is portable across surfaces because the schema and the replica are the durable layer; the surface is not |

*Table 4: Every integration is a feed into Hawkins's Azure + GitHub. None is a feed into EVE. Step-1 integrations deepen automation; step-2 integrations reduce human friction; neither replaces the customer conversation.*

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

1. Is the **two-step operating model** (§1) — automated OEM check plus human-driven third-party check, on every VIN every visit — the right shape for how Hawkins wants warranty determination to run in service? EgD's recommendation is yes: it works with what is on hand today, and integrations layer on top without changing the shape.
2. Is the three-lane custody model (§2) — Azure of record, GitHub replica, session-only compute — the right long-term architecture, or does Tobias want a variant?
3. Is the AI-surface interchangeability rule (§2, §5.2) — same schema, same replica, same answers whether Perplexity Computer or Claude runs the session — worth pinning as a design constraint, or is it an implementation detail?
4. Is the choice record (§9.1) worth writing from day one, or should it wait until the twin records themselves are stable? EgD's recommendation is day-one, because the compounding is what turns the engine into an assistant.
5. On the powersports side, does Torque Motorsports have a BRP district-manager relationship already? That fills the one gap left in [EgD-WGB-005 row 12](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/luke-contacts/EgD-WGB-005-Luke-Contact-Table.pdf).
6. Any Tobias-specific integration requirements (identity, SSO, audit-log format) that should be added to §10 before the twin repository schema is frozen?

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
