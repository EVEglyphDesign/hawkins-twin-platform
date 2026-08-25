# Warranty GENE — Luke access prep

For the next sit-down with Luke Weatherbie. Five external surfaces, five contacts on the other side, the exact ask for each one, and the language to avoid so we don't set off a response we didn't want. Dany asks; Luke owns the dealer relationships that unlock each surface.

## Who Luke is asking, at a glance

| # | Surface | Who Luke asks | What we're asking for | What we're not asking for (yet) |
| --- | --- | --- | --- | --- |
| 1 | **PRWS on Fortellis** | Luke's CDK Global account manager (CDK Drive Inside Sales) — cc PACCAR Dealer Systems | A Fortellis Organization tied to Hawkins, one Subscription-Id for our read-only App, OAuth2 service-account credentials scoped to PRWS read | A new App listed in the public Fortellis Marketplace, a US$129 listing fee, or a claim-submission credential |
| 2 | **PACCAR Solutions Service Management (Decisiv)** | The same CDK account manager, because the DMS provider is the required entry point per Decisiv | Confirmation that the existing CDK Drive ↔ Decisiv integration is live at all eight rooftops, and one read-only account on our side to inspect the same case data | Any change to how service advisors log in, or an OWL Case Estimator re-provisioning |
| 3 | **PACCAR Solutions Portal + SmartLINQ** | Peter (Hawkins CFO), because the account is dealer-billed, not Luke's to sign for | Read access under Hawkins' existing subscription — one service account, not a personal login — for the Peterbilt Atlantic BAC codes | A new subscription, a fleet-owner Data Sharing Request, or anything that touches PACCAR Connect (see #4) |
| 4 | **PACCAR Connect Data Integration Services** | PACCAR North America commercial contact (route through the Peterbilt District Manager, not Eindhoven) | One question only, in writing: does PACCAR Connect Data Integration Services cover Peterbilt VINs in North America today, or does Peterbilt telemetry still route through PACCAR Solutions/SmartLINQ? | Partner-network onboarding, a customer Data Sharing Request, or a purchased data package. All three come after we know the answer |
| 5 | **PACCAR.net supplier bulletins** | Peter, or Luke's Peterbilt District Manager if Peter can't provision it | One dealer-scoped service account with read access to the supplier-bulletin PDF library | A personal PACCAR.net login shared with a service account name pinned to Luke |

Cummins RAPIDSERVE Web is deliberately off this list. It only matters if Hawkins services Cummins-engine chassis outside PACCAR MX. Confirm scope with Tim before adding a sixth surface.

---

## 1. PRWS on Fortellis — the registration record of truth

**Publisher.** CDK Global operates the Fortellis marketplace and gateway. PACCAR publishes PRWS on it. This is the machine-readable field-of-record for VIN-level registration and warranty claim data — the Warranty Procedure Manual v2026.7 names PRWS as authoritative for Retail Sale and warranty transactions.

**Who Luke asks.** His current CDK Global account manager (CDK Drive Inside Sales). If Luke does not have a named CDK rep, ask through the [Fortellis contact form](https://fortellis.io/contact) and mark the request as originating from an existing CDK Drive dealer.

**Exact ask.**

> "We're standing up a read-only integration that consumes the PRWS API through Fortellis. We already run CDK Drive across eight rooftops. We need three things provisioned: a Fortellis Organization tied to Hawkins, a Subscription-Id for our internal App (not marketplace-listed), and OAuth2 service-account credentials scoped to PRWS read endpoints only. The App is dealer-internal — no marketplace listing, no listing fee. Warranty claim submission stays where it is today, in our existing CDK-PRWS workflow."

**What Luke does not say.**

- Do not describe the App as a "product" or a "solution we're selling." That language routes the request into Fortellis Marketplace publishing, which carries a listing fee per App and a review process we don't need.
- Do not ask for write access to PRWS. If we ask for write, CDK will route this to the PACCAR PRWS integration team and the conversation becomes about certification, not credentials.
- Do not name the twin. Call it an "internal read-only integration." Once "twin" is on paper, we get a data-governance escalation before we get an API key.

**Evidence Luke can point to if pushed.**

- [Fortellis API request/response components](https://docs.fortellis.io/) — Subscription-Id is a documented header, not a bespoke request.
- [CDK Global Heavy Truck PRWS description](https://www.cdkglobal.com/) — PRWS creates warranty claim drafts from ROs, so read-only inspection is a lower-privilege ask than what CDK already grants.

**What "good" looks like leaving the room.** Fortellis Organization created, one Subscription-Id issued, and a named CDK contact who owns the OAuth2 provisioning ticket.

---

## 2. PACCAR Solutions Service Management (built on Decisiv)

**Publisher.** PACCAR (product). Decisiv (platform). Reached at [paccar.decisiv.net](https://paccar.decisiv.net).

**Who Luke asks.** The same CDK Global account manager, because Decisiv's own documented policy is that DMS integration starts with the DMS provider: [Decisiv PACCAR support — Integration with Decisiv, start with your DMS provider](https://support.paccar.decisiv.net/hc/en-us/articles/360034411774).

**Exact ask.**

> "Our CDK Drive ↔ Decisiv integration is already live for warranty coverage read-back at the point of service. Please confirm the integration is enabled for all eight Peterbilt Atlantic BAC codes, not just the primary rooftop. Second, we need one read-only account on our end that can view the same case-level coverage data through PSSM, tied to a service-account mailbox, not a personal login."

**What Luke does not say.**

- Do not ask about "bulk data extraction" from PSSM. PSSM is case-scoped by design — that's what the [Decisiv SRM Case Estimator fact sheet](https://info.decisiv.com/) describes. Bulk registration belongs to PRWS (#1). Asking for bulk out of PSSM triggers a "wrong tool" reply and delays #1.
- Do not name Decisiv in the initial ask — CDK is the provisioning path. Decisiv only surfaces if CDK asks who the endpoint is.

**What "good" looks like leaving the room.** A confirmation that all eight BAC codes are enabled and a service-account mailbox provisioned for PSSM read access.

---

## 3. PACCAR Solutions Portal + SmartLINQ Service Management

**Publisher.** PACCAR. This is the human-facing portal and the SmartLINQ remote-diagnostics feed for over 800 engine and emissions systems, per [Peterbilt Connected Services](https://www.peterbilt.com/services/connected-services).

**Who Luke asks.** Peter (Hawkins CFO). This account is dealer-billed and enrolled through [PACCARSolutions.com](https://www.paccarsolutions.com/), per the PACCAR Truck Connectivity Services Agreement. It is not Luke's to sign for; it is Peter's.

**Exact ask, from Luke to Peter.**

> "We need one read-only service account under Hawkins' existing PACCAR Solutions subscription — same billing entity, no new subscription. The account name should be a service-account mailbox, not a personal login. Scope is Peterbilt Atlantic BAC codes only. This is for the same warranty program we discussed with Tim."

**What Luke does not say.**

- Do not ask Peter to open a new subscription. That's a purchasing decision that needs Tim, not just Peter, and it changes what we're doing from "read what Hawkins already pays for" to "buy something new" — a different conversation.
- Do not mention PACCAR Connect (#4) in the same ask. PACCAR Solutions and PACCAR Connect are separate surfaces with separate account trees. Mixing them makes Peter route the ask to the wrong internal owner.

**What "good" looks like leaving the room.** One service account provisioned under Hawkins' PACCAR Solutions subscription, all eight BAC codes visible.

---

## 4. PACCAR Connect Data Integration Services

**Publisher.** PACCAR Global Connected Services in Eindhoven, DAF-branded. Named on the [DAF PACCAR Connect Data Integration Services page](https://www.daf.global/en-us/daf-services/connected-services/paccar-connect-data-integration-services).

**Why this one is delicate.** Third-party integrator [Navixy publicly claims](https://www.navixy.com/oem-telematics-brands/) PACCAR Connect covers DAF, Kenworth, and Peterbilt. PACCAR itself has not confirmed North American Peterbilt scope in a citable document. Until we know the answer, we do not want to trigger the partner-onboarding flow.

**Who Luke asks.** His Peterbilt District Manager (PACCAR North America commercial contact). Not Eindhoven. Not the partner-onboarding form.

**Exact ask, in writing.**

> "One question. Does PACCAR Connect Data Integration Services cover Peterbilt VINs in North America today for a dealer integration, or does Peterbilt telemetry still route through PACCAR Solutions and SmartLINQ Service Management? We're planning a read-only warranty integration and need to know which surface owns the telemetry lane before we scope credentials."

**What Luke does not say.**

- Do not fill in the [PACCAR Connect Data Integration Partner form](https://www.daf.global/en-us/daf-services/connected-services/paccar-connect-data-integration-services). Once submitted, we're in the partner-network flow, which means a partner agreement, a data-package purchase decision, and a customer Data Sharing Request routed to Hawkins as if we were a third party — none of which we want before we know the answer to the one question.
- Do not describe the ask as "we want to integrate." Describe it as "we want to scope." The first framing gets us a partnership pitch; the second gets us the answer.
- Do not mention Navixy or any third-party integrator by name. If PACCAR North America is unaware of a claim about their scope, naming it accelerates a marketing correction, not our answer.

**What "good" looks like leaving the room.** A one-line answer, in writing if possible, from a named PACCAR North America contact. That's it.

---

## 5. PACCAR.net supplier bulletins

**Publisher.** PACCAR. Referenced 17 times in the Warranty Procedure Manual v2026.7 as the retrieval location for supplier warranty bulletins (Sensata, SmartLINQ/PMG, and others — §7.52 page 175 and §7.53 pages 175–176 are the exemplars).

**Who Luke asks.** Peter first, because this is again a dealer-billed credential. If Peter cannot provision a service account, Luke's Peterbilt District Manager is the fallback.

**Exact ask.**

> "One dealer-scoped service account with read access to the PACCAR.net supplier bulletin PDF library. Service-account mailbox, not a personal login. Scope is Peterbilt Atlantic BAC codes."

**What Luke does not say.**

- Do not offer to reuse Luke's personal PACCAR.net login "just to get started." A personal login pinned to a service becomes a credential-audit finding six months from now, and it also creates a dependency on Luke being at Hawkins.
- Do not ask for admin. Read is enough.

**What "good" looks like leaving the room.** One service account, read-only, all eight BAC codes in scope.

---

## The three things Luke should keep off every conversation

1. **The word "twin."** Everywhere it appears in our internal canon, replace it with "internal read-only integration" in external asks. The twin framing is correct on our side and unhelpful on theirs — it invites governance review before it invites credentials.
2. **Warranty claim submission.** Every surface we're asking for is read-only. Submission stays where it lives today. Naming submission triggers a certification conversation that we do not need to have to build the read lane.
3. **Cross-surface bundling.** Ask one surface owner for one surface at a time. Bundling PRWS + PSSM + PACCAR Solutions + PACCAR Connect + PACCAR.net into one "we need access to everything" ask routes the entire request to a data-governance escalation queue at CDK or PACCAR, and slows every individual ask.

## Order of operations for the sit-down with Luke

1. **PACCAR Connect (#4) first, in writing, before the meeting if possible.** It's a single-question read that unblocks the shape of the telemetry lane. Answer determines nothing else, but it removes an unknown.
2. **PRWS (#1) at the meeting.** This is the biggest unlock and the most sensitive framing. Get Luke to send the ask to his CDK account manager while Dany is with him, so the language is right on the first send.
3. **PSSM (#2) in the same message as #1.** Same contact, same CDK account manager, adjacent surface. Bundling PRWS and PSSM to one contact is fine; that's not the bundling failure — the bundling failure is bundling across contacts.
4. **PACCAR Solutions (#3) and PACCAR.net (#5) via Peter after the meeting.** These are dealer-billed; Peter owns them. Route these once the meeting produces the exact account names to request.

---

## Provenance

- Canonical surface map: [`warranty-gene/registration/registration-and-terms.json`](https://github.com/EVEglyphDesign/hawkins-twin-platform/blob/main/warranty-gene/registration/registration-and-terms.json)
- Registration & Terms narrative: [Warranty GENE Registration & Terms](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/registration/)
- Warranty Procedure Manual v2026.7 (§1.18, §7.52, §7.53) — uploaded to the project workspace
- Shrish's execution lane, activated once these credentials arrive: [Warranty GENE Shrish Setup (EgD-WGB-002)](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/shrish-setup/)
