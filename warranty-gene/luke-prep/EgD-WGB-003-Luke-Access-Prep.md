# Warranty GENE — Luke access prep

For the next sit-down with Luke Weatherbie. Five counterparties, one sweep. The goal is that from each counterparty we ask for **everything Hawkins is legitimately entitled to** as a dealer of its tenure that touches a VIN's service history — repair orders, work orders, historical service records, warranty claims, telematics feeds, campaign lookups, supplier bulletins, engine-manufacturer records, chassis-supplier records. All of it, in one message per counterparty, so we don't have to go back multiple times.

**Why one sweep.** Owner-operators are our customers. The more of a VIN's service history we can pull together in one place, the better job we can do for them. Every time we go back to the same counterparty a second time with a new ask, we raise the question "why now, why again, what changed" — which triggers governance review before it triggers credentials. Ask for everything in scope on the first pass, framed as due diligence, and the second pass is only for what wasn't granted.

**Where this is going.** The proof-of-concept is a representative sample. The target is complete warranty coverage for every VIN in Hawkins' book of service — every active vehicle, every historical vehicle we've touched, every claim eligible on any warranty lane through any counterparty. This sweep is designed so that once the credentials arrive, the same read pattern scales from the sample VINs to the full VIN population without renegotiating access. That's the point of asking each counterparty for everything Hawkins is entitled to as a dealer of its tenure, in one message: the credential granted here is the credential that covers every VIN we service, not just the ones in the first sample.

**Adaptive frame.** This document is a revision of an earlier five-surface sweep. Warranty GENE is designed to be redirected as we learn. When the counterparty conversations run and something new surfaces, this document is reissued at the same canon URL with a new revision line in the provenance block. Do not treat any single revision as the final word.

---

## Who Luke is asking, at a glance

| # | Counterparty | Who Luke asks | One-message ask covers |
| --- | --- | --- | --- |
| 1 | **CDK Global** | Luke's CDK Global account manager (CDK Drive Inside Sales) | CDK Drive read-only service account (ROs, work orders, labor ops, parts on ticket, 3C narratives, customer records, historical invoices); PRWS on Fortellis (Organization, Subscription-Id, OAuth2 read credentials); PACCAR Solutions Service Management (PSSM/Decisiv) integration confirmation and PSSM read account |
| 2 | **PACCAR — Peterbilt District Manager** | Luke's Peterbilt District Manager (PACCAR North America, not Eindhoven) | PACCAR.net service account (TSBs, campaigns, supplier bulletins, warranty policy circulars); PACCAR Solutions Portal + SmartLINQ scoping; PACCAR Connect Data Integration Services scoping question; MX engine warranty lane confirmation; PartsPRO warranty transaction read; CARB/EPA emissions-warranty scope inside PRWS |
| 3 | **Peter (Hawkins CFO)** | Peter, internally | Authorization for a Hawkins service-account mailbox to be attached to every dealer-billed subscription (PACCAR Solutions, PACCAR.net, PartsPRO); business-side sign-off to expose historical DMS customer/invoice records to a service-account read; PacLease/PACCAR Financial lease-return files if Hawkins runs them |
| 4 | **Powertrain manufacturers** | One rep per manufacturer, framed as dealer-side due diligence | Cummins (RAPIDSERVE Web API, QuickServe warranty history, INSITE session logs, campaign lookups); Eaton (ServiceRanger data, Roadranger warranty history); Allison (Allison DOC session logs, Allison warranty portal read) |
| 5 | **Chassis & air-system suppliers** | One rep per manufacturer, same due-diligence framing | Meritor (MTIS / OnTrac warranty portal, axle warranty history); Bendix (ACom Pro session logs, Bendix warranty portal); Wabco / ZF (Toolbox session logs, Wabco warranty portal); Dana (Dana Expert System, Spicer warranty portal) |

---

## 1. CDK Global — one message, three lanes

**Who Luke asks.** His current CDK Global account manager (CDK Drive Inside Sales). If Luke does not have a named CDK rep, the request originates through the [Fortellis contact form](https://fortellis.io/contact) tagged as an existing CDK Drive dealer.

**Why one message.** CDK owns the DMS Hawkins already runs, publishes PRWS on Fortellis, and is Decisiv's documented entry point for PSSM integration per the [Decisiv PACCAR support article](https://support.paccar.decisiv.net/hc/en-us/articles/360034411774). Splitting the ask across three tickets fragments the account manager's context and produces three governance reviews. One message, three lanes, one governance review.

**Exact ask, one message to the CDK account manager.**

> Hawkins runs CDK Drive across eight Peterbilt Atlantic rooftops. We're standing up an internal warranty due-diligence workflow — read-only — that reconciles our warranty claim submissions against the engine-manufacturer record before submission, so we're not filing claims that get denied and cost our owner-operator customers downtime while we appeal. To do that, we need three things provisioned under our existing CDK relationship.

**Lane 1 — CDK Drive read-only service-account access.** Repair orders, work orders, labor operations, parts-on-ticket detail, 3C narratives, customer master records, and historical service invoices, scoped to our eight BAC codes. Service-account mailbox, not a personal login.

**Lane 2 — PRWS on Fortellis.** A Fortellis Organization tied to Hawkins, a Subscription-Id for our internal App (not marketplace-listed), and OAuth2 service-account credentials scoped to PRWS read endpoints only. The App is dealer-internal — no marketplace listing, no listing fee. Warranty claim submission stays in our existing CDK-PRWS workflow.

**Lane 3 — PACCAR Solutions Service Management.** Please confirm the CDK Drive ↔ Decisiv integration is enabled for all eight BAC codes, and provision one read-only service-account for PSSM case data on our side.

**What Luke does not say.**

- Do not describe the workflow as a "product," a "solution we're selling," or a "twin." Product framing routes Fortellis into marketplace publishing (US$129 listing fee and a review process we don't need). Twin framing routes the entire ask into data-governance review before it reaches provisioning.
- Do not ask for write access anywhere. Write access to PRWS routes to the PACCAR PRWS integration team and the conversation becomes about certification, not credentials. Write access to CDK Drive is not a service-account grant, it's a user seat, and it triggers a different conversation about license count.
- Do not ask about bulk data extraction from PSSM. PSSM is case-scoped by design per the [Decisiv SRM Case Estimator fact sheet](https://info.decisiv.com/). Bulk registration data belongs to PRWS. Naming bulk out of PSSM triggers a "wrong tool" reply and delays PRWS.
- Do not name Decisiv in the initial ask. CDK is the provisioning path. Decisiv only surfaces if CDK asks who the endpoint is.

**Evidence Luke can point to if pushed.**

- [Fortellis API request/response components](https://docs.fortellis.io/) — Subscription-Id is a documented header, not a bespoke request.
- [CDK Global Heavy Truck PRWS description](https://www.cdkglobal.com/) — PRWS creates warranty claim drafts from ROs, so read-only inspection is a lower-privilege ask than what CDK already grants Hawkins today.

**What "good" looks like leaving the room.** Three ticket IDs (or one ticket with three sub-items) opened under Luke's CDK account manager, with named CDK owners for each: DMS read service-account, Fortellis provisioning, PSSM integration confirmation.

---

## 2. PACCAR — one message to the Peterbilt District Manager

**Who Luke asks.** Luke's Peterbilt District Manager (PACCAR North America commercial contact). Not Eindhoven. Not the partner-onboarding form on the DAF site.

**Why one message.** The PDM owns Hawkins' dealer relationship across every PACCAR-brand surface: PACCAR.net, PACCAR Solutions, PACCAR Connect scoping, MX engine warranty policy, PartsPRO parts warranty, and the emissions-warranty policy overlay. Splitting these across separate emails invites the PDM to route each to a different internal group, which delays every one of them. One message, framed as a dealer due-diligence review, produces one PDM-owned response.

**Exact ask, one message to the PDM.**

> Peterbilt Atlantic is standing up an internal warranty due-diligence workflow across our eight rooftops. Read-only. Purpose is to reconcile our warranty claims and campaign eligibility against the manufacturer record before submission, so we deny fewer claims to the owner-operator and appeal fewer to PACCAR. As dealer principals we'd like to sweep, in one review, everything Hawkins is already entitled to under our current PACCAR agreements that would feed this workflow.

**Item 1 — PACCAR.net service account.** Read access to the full document library: technical service bulletins, warranty policy circulars, campaign notices, and supplier warranty bulletins (§7.52 and §7.53 exemplars in Warranty Procedure Manual v2026.7). Service-account mailbox tied to Hawkins, not a personal login. All eight BAC codes.

**Item 2 — PACCAR Solutions Portal and SmartLINQ Service Management.** Confirmation of Hawkins' current subscription scope, and one read-only service account under the existing subscription for the same BAC codes. Not a new subscription, not a fleet-owner Data Sharing Request.

**Item 3 — PACCAR Connect Data Integration Services.** One scoping question, in writing: does PACCAR Connect Data Integration Services cover Peterbilt VINs in North America today for a dealer-side read integration, or does Peterbilt telemetry still route through PACCAR Solutions and SmartLINQ Service Management? If it does cover Peterbilt NA, we'd like to know the entitlement path for a dealer of our tenure. If it doesn't, no further ask.

**Item 4 — PACCAR MX engine warranty lane.** Confirmation that the PRWS credentials CDK is provisioning cover MX engine warranty transactions (MX-11 and MX-13) alongside chassis warranty. If MX warranty is a separate credential lane, the path to that credential.

**Item 5 — PartsPRO warranty transactions.** Read-only service-account access to parts warranty transaction history, warranty parts return authorizations, and parts campaign lookups, tied to our BAC codes.

**Item 6 — CARB/EPA emissions warranty scope.** Confirmation that the emissions-warranty claim types described in the CARB/EPA Emission Component Coverage matrix are in scope of the PRWS read credential CDK is provisioning. If separate, the path to that credential.

**What Luke does not say.**

- Do not describe this as "an integration" or "a partnership." Describe it as "a due-diligence review" and "an internal read-only workflow." Integration framing routes PACCAR Connect into the partner-onboarding flow (partner agreement, data-package purchase, customer Data Sharing Request routed to Hawkins as if it were a third party). Due-diligence framing routes it to the PDM's dealer-services desk.
- Do not fill in the [PACCAR Connect Data Integration Partner form](https://www.daf.global/en-us/daf-services/connected-services/paccar-connect-data-integration-services). The form is the partner flow. The email to the PDM is the dealer flow.
- Do not name Navixy or any third-party integrator. If PACCAR North America is unaware of a public third-party claim about their scope, naming it accelerates a marketing correction, not our answer.
- Do not name the twin. "Internal warranty due-diligence workflow" is the phrase.
- Do not bundle the CDK ask (Counterparty 1) into this message. PACCAR does not provision Fortellis; CDK does. Naming CDK's provisioning inside PACCAR's ask makes the PDM think we're asking PACCAR to intervene on our behalf with CDK, which slows everything.

**What "good" looks like leaving the room.** One PDM-owned response covering all six items — some as confirmations of existing scope, some as new service-account provisions, one as a scoping answer.

---

## 3. Peter — one internal conversation

**Who Luke asks.** Peter, Hawkins CFO. Not by email. In person, or a scheduled call. This is internal authorization for the two external counterparties above to succeed.

**Why one conversation.** Everything CDK and PACCAR would provision under Counterparties 1 and 2 is dealer-billed or requires a Hawkins business-side signatory. Without Peter's authorization staged before Luke sends the two external asks, the external asks will bounce back to Hawkins for a signature and stall.

**Exact ask, from Luke to Peter.**

> Peter, on the warranty workflow Dany and I are standing up: I'm going to send our CDK account manager and our PACCAR PDM two messages this week. They'll both come back to you for authorization on a few items, and I want you to know what's coming so you're not surprised.

**Item 1 — Hawkins service-account mailbox.** One address like `warranty-integration@hawkinstruck.com` or similar, attached to every dealer-billed subscription for read-only access: PACCAR Solutions, PACCAR.net, PartsPRO, CDK Drive read, PSSM read, Fortellis. This replaces pinning service accounts to individual employee logins, which is a credential-audit finding waiting to happen.

**Item 2 — business-side sign-off** on exposing our historical DMS customer master and service-invoice records to that service account, on a read-only basis. Same data our service advisors see today; the read scope changes, not the data.

**Item 3 — PacLease.** If Hawkins runs any PacLease returns, we'll want the lease-return warranty files in the same workflow. If we don't, no action needed.

> Nothing in this changes what Hawkins pays. Every subscription named already exists under our BAC codes. We're asking for read seats under existing entitlements, not new purchases.

**What Luke does not say.**

- Do not present this as "Dany's project." Present it as "our warranty workflow." Peter authorizes Hawkins-owned work, not vendor-owned work.
- Do not ask for a new subscription. If any of the external counterparties comes back with "we can grant this, but it requires an upgraded subscription," that's a separate conversation with Peter *and* Tim, not the first conversation.
- Do not name the twin. "Warranty workflow" is the phrase.

**What "good" looks like leaving the room.** Peter's verbal go-ahead on the service-account mailbox, the read-only DMS record exposure, and clarity on whether PacLease is in scope.

---

## 4. Powertrain manufacturers — three parallel due-diligence asks

**Who Luke asks.** One rep per manufacturer. Cummins district service manager (or Hawkins' authorized-dealer service rep). Eaton warranty rep (Roadranger territory manager). Allison warranty rep (Allison Authorized Distributor territory manager). Each is a separate message. Do not bundle across manufacturers — each has its own warranty group, its own governance review, and no cross-visibility to what we asked another.

**Why in this sweep.** Powertrain is where warranty dollars concentrate. Engine, transmission, and torque-converter/automatic-transmission claims produce the biggest single-line warranty amounts and the longest owner-operator downtime. Reconciling our claim against the manufacturer's warranty record *before* submission is the single largest per-claim reduction in denial-and-appeal cycle time we can deliver to an owner-operator. The chassis and air-system suppliers in Counterparty 5 are the second-largest bucket by claim frequency — axles, brakes, air-system — and both counterparties are needed together for a representative sample.

**Framing across all three manufacturers.** Same opening, adjusted per manufacturer's own terminology.

> Hawkins is an authorized service dealer for [manufacturer] equipment on our Peterbilt platform. We're standing up an internal warranty due-diligence workflow that reconciles our warranty claim submissions against the [manufacturer] warranty record before submission. Goal is to reduce the denial rate of our claims and the appeal workload on your warranty group. Read-only. As an authorized service dealer of our tenure, we'd like to sweep — in one review — everything we're entitled to that would feed this reconciliation.

**Per-manufacturer specifics below.**

### 4a. Cummins

**Who.** Cummins district service manager assigned to Hawkins' authorized-dealer coverage. If Luke doesn't have a named DSM, the entry is through [QuickServe Online](https://quickserve.cummins.com/) dealer support, tagged as an authorized-dealer request.

**Exact ask to Cummins.**

> As an authorized Cummins service dealer, we'd like read-only access under our existing dealer authorization.

**Cummins Item 1 — RAPIDSERVE Web API.** Read credentials for warranty coverage lookup by ESN, campaign eligibility lookup, and warranty history by ESN.

**Cummins Item 2 — QuickServe Online warranty history.** Service-account access to warranty transaction history for Cummins engines we service, tied to Hawkins' authorized-dealer ID.

**Cummins Item 3 — INSITE session log archive.** The ability to submit and retrieve INSITE session logs against warranty claims we're preparing, so we can attach the same session data your warranty group would ask us to attach on appeal, before submission rather than after.

**Cummins Item 4 — authorized-dealer campaign document library**, if Cummins publishes campaign notices to authorized dealers separately from QuickServe. Service-account read access.

**Language to avoid.**

- Do not describe Hawkins as "building an integration with Cummins." Cummins integration goes through Cummins Digital, which is a partner track, not a dealer track.
- Do not ask for CustomerLink or CumminsLink write access. Read is enough.

### 4b. Eaton (Roadranger)

**Who.** Eaton Roadranger warranty rep for the Atlantic Canada territory, or Luke's Roadranger contact if Hawkins has a named one.

**Exact ask to Eaton.**

> As an authorized Eaton service dealer under our Peterbilt platform, we'd like read-only access under our existing dealer authorization.

**Eaton Item 1 — ServiceRanger data.** Read credentials for transmission diagnostic data, warranty coverage lookup by serial number, and campaign eligibility.

**Eaton Item 2 — Roadranger warranty history.** Service-account access to warranty transaction history for Eaton transmissions and clutches we service, tied to Hawkins' authorized-dealer ID.

**Eaton Item 3 — Roadranger dealer bulletin library.** Service-account read to warranty policy and campaign notices.

**Language to avoid.**

- Do not ask about Cummins-Eaton Endurant partnership scope until Cummins confirms 4a. If Endurant is in play, it will surface in the Cummins conversation first and simplify the Eaton ask.

### 4c. Allison

**Who.** Allison Authorized Distributor territory manager, or Allison warranty rep if Hawkins deals direct.

**Exact ask to Allison.**

> As an authorized Allison service dealer on our Peterbilt platform, we'd like read-only access under our existing dealer authorization.

**Allison Item 1 — Allison DOC session logs.** The ability to submit and retrieve DOC session data against warranty claims we're preparing.

**Allison Item 2 — Allison warranty portal.** Service-account read access to warranty transaction history for Allison transmissions we service, tied to Hawkins' authorized-dealer ID, plus campaign eligibility lookup.

**Allison Item 3 — Allison dealer bulletin library.** Service-account read to warranty policy and campaign notices.

**Language to avoid.**

- Do not ask for Allison DOC Premium features. Read against the warranty portal and standard DOC session logs is the scope.

**What "good" looks like leaving the room, across all three powertrain manufacturers.** Three separate warranty-rep-owned responses, each covering the read credentials and the warranty history/portal access for that manufacturer.

---

## 5. Chassis and air-system suppliers — four parallel due-diligence asks

**Who Luke asks.** One rep per manufacturer. Meritor (now Cummins Meritor) warranty rep or Hawkins' authorized-dealer contact. Bendix warranty rep for the Atlantic Canada territory. Wabco / ZF Commercial Vehicle Solutions warranty rep. Dana (Spicer) warranty rep. Each is a separate message. Same no-bundling rule as Counterparty 4 — each has its own warranty group and no cross-visibility.

**Why in this sweep.** These four suppliers own the axle, brake, air-system, and driveline component warranty lanes on every Peterbilt Atlantic chassis. A representative warranty sample cannot be proved out without at least one recovered claim per major component family, and these are where the second tier of warranty dollars lives after powertrain. Adding them now, in the same sweep as Counterparty 4, gets a full component-level picture on one pass and lets us prove the concept end-to-end.

**Framing across all four.** Same opening as Counterparty 4, adjusted per manufacturer's own terminology.

> Hawkins is an authorized service dealer for [manufacturer] equipment on our Peterbilt platform. We're standing up an internal warranty due-diligence workflow that reconciles our warranty claim submissions against the [manufacturer] warranty record before submission. Goal is to reduce the denial rate of our claims and the appeal workload on your warranty group. Read-only. As an authorized service dealer of our tenure, we'd like to sweep — in one review — everything we're entitled to that would feed this reconciliation.

### 5a. Meritor (Cummins Meritor)

**Who.** Meritor warranty rep, or Hawkins' authorized-dealer service contact through the Meritor dealer channel.

**Exact ask to Meritor.**

> As an authorized Meritor service dealer under our Peterbilt platform, we'd like read-only access under our existing dealer authorization.

**Meritor Item 1 — MTIS / OnTrac warranty portal.** Service-account read access to warranty transaction history for Meritor axles, driveline components, and tire-inflation systems (MTIS) we service, tied to Hawkins' authorized-dealer ID, plus campaign eligibility lookup.

**Meritor Item 2 — Meritor dealer bulletin library.** Service-account read to warranty policy circulars, campaign notices, and TSBs.

**Meritor Item 3 — axle serial-number warranty coverage lookup.** Read credentials for coverage lookup by axle serial, so we can confirm coverage before submission.

### 5b. Bendix

**Who.** Bendix warranty rep for the Atlantic Canada territory (Bendix is now part of Knorr-Bremse North America), or Hawkins' authorized-dealer contact.

**Exact ask to Bendix.**

> As an authorized Bendix service dealer under our Peterbilt platform, we'd like read-only access under our existing dealer authorization.

**Bendix Item 1 — ACom Pro session log archive.** The ability to submit and retrieve ACom Pro session data against warranty claims we're preparing, so the same session data your warranty group would ask us to attach on appeal is attached before submission.

**Bendix Item 2 — Bendix warranty portal.** Service-account read access to warranty transaction history for Bendix air-brake components (compressors, valves, ABS/ESP modules) we service, tied to Hawkins' authorized-dealer ID, plus campaign eligibility.

**Bendix Item 3 — Bendix dealer bulletin library.** Service-account read to warranty policy circulars, campaign notices, and TSBs.

### 5c. Wabco / ZF

**Who.** ZF Commercial Vehicle Solutions warranty rep (Wabco was acquired by ZF in 2020; warranty is administered under ZF CVS now), or Hawkins' authorized-dealer contact.

**Exact ask to ZF.**

> As an authorized ZF / Wabco service dealer under our Peterbilt platform, we'd like read-only access under our existing dealer authorization.

**ZF Item 1 — Wabco Toolbox session log archive.** The ability to submit and retrieve Toolbox session data against warranty claims we're preparing.

**ZF Item 2 — ZF / Wabco warranty portal.** Service-account read access to warranty transaction history for Wabco air-system components we service, tied to Hawkins' authorized-dealer ID, plus campaign eligibility.

**ZF Item 3 — ZF / Wabco dealer bulletin library.** Service-account read to warranty policy circulars, campaign notices, and TSBs.

### 5d. Dana (Spicer)

**Who.** Dana warranty rep for the Atlantic Canada territory, or Hawkins' authorized-dealer contact through the Spicer dealer channel.

**Exact ask to Dana.**

> As an authorized Dana service dealer under our Peterbilt platform, we'd like read-only access under our existing dealer authorization.

**Dana Item 1 — Dana Expert System / SpicerParts warranty lookup.** Read credentials for driveline coverage lookup by component serial number, and campaign eligibility.

**Dana Item 2 — Dana warranty portal.** Service-account read access to warranty transaction history for Dana driveline components (driveshafts, universal joints, PTOs) we service, tied to Hawkins' authorized-dealer ID.

**Dana Item 3 — Dana dealer bulletin library.** Service-account read to warranty policy circulars, campaign notices, and TSBs.

**Language to avoid across Counterparty 5.**

- Do not describe Hawkins as "building an integration" with any of these suppliers. Same reason as Counterparty 4 — supplier integration goes through their partner-network track, not their dealer-service track.
- Do not name a competing supplier inside another supplier's ask. If Meritor sees us naming Dana, or Bendix sees us naming ZF, we get a marketing conversation instead of a warranty conversation.

**What "good" looks like leaving the room, across all four chassis suppliers.** Four separate warranty-rep-owned responses, each covering read credentials for the warranty portal, session-log archive access where applicable, and bulletin-library read.

---

## The three things Luke keeps off every conversation

1. **The word "twin."** Everywhere it appears in our internal canon, replace with "internal read-only warranty due-diligence workflow" in external asks. The twin framing is correct on our side and unhelpful on theirs — it invites governance review before it invites credentials.
2. **Warranty claim submission.** Every credential we're asking for is read-only. Submission stays where it lives today. Naming submission triggers a certification conversation that we do not need to have to build the read lane.
3. **Cross-counterparty bundling.** Ask one counterparty for their full scope at a time. Naming CDK's provisioning inside PACCAR's message, or naming Cummins inside Eaton's, routes the conversation to a governance escalation because it looks like we're building something that spans everyone's data.

---

## Order of operations

1. **Peter first (Counterparty 3), in person.** Before either external message goes out, Luke and Peter agree on the service-account mailbox name and the DMS-record read-exposure authorization. This is the internal prerequisite for the external asks to succeed.
2. **CDK message (Counterparty 1) same day as the Luke-and-Dany sit-down.** Get Luke to send it to his CDK account manager while Dany is with him, so the language is right on the first send. Three ticket IDs come back over the next several days.
3. **PACCAR PDM message (Counterparty 2), 24 hours after CDK.** Not the same day. CDK and PACCAR should each see a message that is clearly theirs alone, not one that arrives in tandem with the other's — which would make both counterparties assume this is a coordinated procurement event rather than a dealer due-diligence review.
4. **Powertrain manufacturers (Counterparty 4a, 4b, 4c) in parallel, one week after Counterparties 1 and 2.** By that point, CDK has confirmed PRWS provisioning and PACCAR has confirmed MX engine warranty scope, which gives Luke the "as an authorized service dealer of our tenure" credibility line on the manufacturer asks.
5. **Chassis and air-system suppliers (Counterparty 5a, 5b, 5c, 5d) in parallel, same week as Counterparty 4.** Same framing, same tenure line. These four move in parallel with the powertrain asks because they're independent counterparties — no one waits on another. The staggered send day-to-day is fine; the requirement is that all eight supplier messages (three powertrain plus four chassis) are out within the same week.

---

## Provenance

- **Revision.** This is EgD-WGB-003 revision 3. Revision 1 (five surfaces) is superseded. Revision 2 (four counterparties, three powertrain suppliers) is superseded by this revision, which restores the full chassis-supplier sweep so the proof-of-concept has a representative sample across every major warranty-data repository a Peterbilt Atlantic VIN touches. The trimmed revision-2 scope is preserved in git history at commit `bd2240d` on the source repository for the record.
- Canonical surface map: [`warranty-gene/registration/registration-and-terms.json`](https://github.com/EVEglyphDesign/hawkins-twin-platform/blob/main/warranty-gene/registration/registration-and-terms.json)
- Registration & Terms narrative: [Warranty GENE Registration & Terms](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/registration/)
- Warranty Procedure Manual v2026.7 (§1.18, §7.52, §7.53) — uploaded to the project workspace
- CARB/EPA Emission Component Coverage matrix — uploaded to the project workspace
- Shrish's execution lane, activated once these credentials arrive: [Warranty GENE Shrish Setup (EgD-WGB-002)](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/shrish-setup/)
