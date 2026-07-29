# What PACCAR Wants, and Why the Ask Should Happen Now

**Prepared for:** Tim Hawkins, Dealer Principal, Hawkins / Peterbilt Atlantic (New Brunswick)
**Intended second reader:** a PACCAR representative, once named
**Author posture:** enterprise systems architect, SAP background, speaking to the design choices behind Peterbilt Atlantic's Phase 1 build

---

## 1. Why this question now

Phase 1 of the dealer twin is being built on two deliberate constraints: it is read-only, and its canonical core is modelled directly on SAP MM/FI/CO/SD table and column shapes (MARA, MARC, MARD, MBEW, MATDOC, MVKE, MARM, MFRPN and the FI/CO analogues) rather than on CDK's own schema. Neither choice is free. Read-only discipline means we forgo some convenience today. SAP-shaping the core means the model was built to a standard we don't currently have any external counterpart for. Both bets only pay off if PACCAR is eventually in the room, looking at a payload that already speaks its language.

That is the case for asking now rather than later. Naming a PACCAR counterpart costs us nothing at this stage — we are not requesting system access, funding, or a commitment. We are asking who to talk to, and about what. But it forecloses nothing either: every architectural decision taken from here forward can be shaped, in small ways, by an early conversation instead of guessed at in isolation and possibly redone. The alternative — building for two or three phases in the dark and then approaching PACCAR with a finished thing — is the more expensive path, not the cautious one.

## 2. What PACCAR plausibly wants from its dealers

This section is inference, not confirmed PACCAR strategy. We have no statement of PACCAR's dealer-network objectives. What we have is a list of systems PACCAR has actually built and funded, and systems reveal intent: an organisation does not build and maintain Managed Dealer Inventory, Syncron Returns SmartBlox, PRWS, OPC, and SmartLINQ/PACCAR Solutions by accident. Each implies something PACCAR is trying to control or capture across its dealer network. The right-hand column below is our proposal for what a dealer-side twin, built the way ours is being built, could hand back toward each of those inferred objectives — this is not something PACCAR has asked for.

| PACCAR system (confirmed) | What building it implies PACCAR wants (inference) | What a dealer twin could give PACCAR toward it (proposal) |
|---|---|---|
| Managed Dealer Inventory (MDI) — daily automated stock-order recommendation engine, order types Stock, Emergency, MKT, COF | Control over stocking quality across the dealer network; PACCAR does not want stock decisions left purely to individual dealer judgement | Closed-loop feedback: what MDI recommended versus what actually sold or sat, at the plant/store level (PA01..PA09), fed back in a structured, SAP-shaped form |
| Syncron Service Lifecycle Management with Returns SmartBlox (dealer-to-OEM returns, adopted 2022) | Returns friction is a cost PACCAR wants out of the channel — restocking, credit cycle time, core tracking | A dealer-side returns record clean enough at source that the Syncron submission requires no manual reconciliation before it leaves the dealer |
| PRWS (PACCAR Registration and Warranty System) | Clean warranty data captured at the point of repair, not reconstructed afterward; PRWS drafts are already generated from repair-order data via CDK | A repair-order-to-warranty-draft pipeline with fewer data-quality gaps, because the underlying repair-order and parts-consumption data is held in an SAP-shaped model rather than a DMS-proprietary one |
| Online Parts Counter (OPC) — eCommerce parts ordering, 545,000+ parts | PACCAR wants order capture inside its own channel, not diverted elsewhere | Not directly addressed by Phase 1; noted here for completeness of the inference, not as a current proposal |
| SmartLINQ (Decisiv) and PACCAR Solutions/PSSM (Decisiv) | PACCAR wants the service event to start from the truck's own telemetry, not from a phone call | Not addressed by Phase 1; the twin deliberately does not touch bulk telematics (see Section 6) |

## 3. The win-wins, concretely

Each of the following is framed around using assets the dealer group has already paid for more effectively — not around either party buying anything new.

**(a) Network stock visibility and inter-dealer transfer.**
PACCAR does not offer an inter-dealer parts transfer service; this is a gap the twin is built to fill outside ePortal. Peterbilt Atlantic operates nine sites (PA01–PA09). Parts sitting on a shelf at one site and needed at another today rely on informal knowledge or a phone call. What the dealer gets: visibility into its own network stock it may not currently have in one place, and fewer emergency orders where a transfer would have done. What PACCAR gets: a lower rate of emergency/expedited order types against MDI, and evidence that existing inventory bought into the network is being used before more is ordered. What it takes: nothing from PACCAR to start — this is a dealer-side capability — but a conversation about whether PACCAR wants visibility into transfer activity, and whether it changes how MDI should weight a site's on-hand position.

**(b) Stocking-quality feedback to MDI.**
MDI issues stock recommendations; today we do not know, in a structured way, how those recommendations performed — what sold, what sat, what was overridden and why. What the dealer gets: a factual basis to challenge or confirm MDI's recommendations rather than acting on faith. What PACCAR gets: a feedback loop it does not currently have, closing the gap between "recommended" and "outcome" — data that could improve MDI's own model over time. What it takes: PACCAR's agreement on what feedback format is useful, and whether it wants it at all; we cannot assume MDI is instrumented to receive it.

**(c) Warranty data quality at source.**
CDK already creates PRWS drafts from repair-order data, and PRWS is reachable via Fortellis — the one PACCAR system with a confirmed API path. What the dealer gets: less rework correcting warranty claims after the fact. What PACCAR gets: cleaner claims arriving with fewer downstream corrections, because the source repair-order and parts data sits in a well-modelled system rather than being reconstructed loosely. What it takes: nothing structurally new from PACCAR — this rides the existing PRWS/Fortellis/CDK path — but confirmation that a service-account-driven, unattended read/write pattern against Fortellis for PRWS is acceptable practice.

**(d) Returns friction reduction against Syncron.**
Syncron Returns SmartBlox governs the dealer-to-OEM returns process PACCAR adopted in 2022. What the dealer gets: fewer rejected or delayed returns because the submission is built from clean, reconciled source data. What PACCAR gets: less friction and administrative cost on its side of the returns channel. What it takes: understanding Syncron's data expectations well enough to align the dealer's internal record to them before submission — a question for a PACCAR or Syncron-side counterpart, not something we can infer from outside.

None of these four requires either party to purchase new infrastructure. All four are about making fuller use of stock, data, and process capability that already exist.

## 4. The SAP argument — the part only an architect can make

PACCAR runs an SAP-shaped enterprise stack: SAP ECC moving to S/4HANA, plus SAP TM, SAP GTS, SAP IBP, SAP BFC, and SAP Concur. Peterbilt Atlantic's dealer twin has been built, from the outset, with its canonical core modelled directly on SAP MM/FI/CO/SD table and column names — MARA, MARC, MARD, MBEW, MATDOC, MVKE, MARM, MFRPN, and the FI/CO analogues. This was not done for elegance. It was done so that a PACCAR SAP payload maps onto the dealer's data model without an interpretive layer in between, and so that the dealer's own data model does not live or die with whichever DMS vendor happens to hold the contract in a given decade.

The practical consequence: when a dealer-side extract eventually needs to speak to PACCAR's SAP-based systems — whether over EDI trading-partner transaction sets (810, 850, 852, 855, 856, 861, 862) or some other route PACCAR specifies — the translation work is smaller, because the dealer-side object is already shaped like the target rather than like a proprietary DMS export that must first be reverse-engineered into SAP's vocabulary. This is the ordinary cost of every OEM-dealer integration: someone has to build the mapping layer, and it is almost always the OEM or a middleware vendor doing it on the dealer's behalf, working from a schema the dealer does not control and did not choose.

It is unusual — we believe uncommon — for a dealer to arrive at that conversation already holding a model in the OEM's own idiom. That is the credibility opener with a PACCAR representative: not "we would like to integrate," but "here is a payload already shaped the way your own systems expect it," with the specific ask being where to send it and under what authentication and transport terms.

## 5. What we are asking PACCAR for

Each item below is deliberately small enough to be answered without a project being spun up on PACCAR's side.

1. A named counterpart in PACCAR dealer systems or PACCAR Parts, to whom the above can be put directly.
2. Clarification of an open question we are carrying internally and cannot resolve from outside: whether Peterbilt/PACCAR heavy-truck dealers report into NADA's ATD 20 Group composite specifically, or into a PACCAR-proprietary equivalent.
3. EDI trading-partner setup (AS2/SFTP) for the dealer group, covering the transaction sets relevant to parts and service — invoice (810), purchase order (850), product activity (852), PO acknowledgement (855), ASN (856), receipt (861), schedule (862) — to the extent PACCAR supports each.
4. Guidance on whether any PACCAR system — PRWS via Fortellis in particular — supports service-account authentication for unattended, scheduled reads, as opposed to interactive user sessions.
5. A conversation about telematics access, on terms PACCAR sets, with no presumption on our part of what those terms should be.

None of these require PACCAR to build anything new. All five can, in principle, be answered by pointing us to an existing contact, an existing document, or an existing policy.

## 6. The boundary we are keeping

Phase 1 is read-only against the live CDK Drive system without exception: nothing is written back to it. Data is acquired two ways — from the CDK backup set, restored into an environment the dealer controls, and from the Fortellis API — landing in Postgres, with reconciliation between the two lanes run as an on-demand executable function rather than assumed. Notably, the ledger itself cannot be pulled by API at all: every GL-side object is unreachable on Fortellis and must come from the backup or a file export, which is itself a reason the read-only, dual-lane design exists.

On telematics specifically: PACCAR's Truck Connectivity Services Terms state that PACCAR collects, uses, and retains vehicle and telematics data, and do not frame dealer or customer access as ownership. The twin does not attempt to bulk-export raw telematics data. That boundary is being respected deliberately, not because of a technical limitation, and anything beyond it requires PACCAR's agreement, not our initiative.

This discipline is the point, not an obstacle to be managed around. A dealer that can point to a system with no live writes, no bulk telematics extraction, and explicit respect for PACCAR's stated terms is a dealer that can credibly ask for a named counterpart without that ask sounding like a request for unrestricted access. Trust is the asset being built here, and it is built by what we chose not to do as much as by what we did.

## 7. The longer arc — R&D on the truck itself

This is a stated direction, not a promise, and it depends entirely on PACCAR's appetite — realistically Phase 3 or later, well past the read-only side-car described here.

Once the dealer-side record is clean, complete, and SAP-shaped across all nine sites, Peterbilt Atlantic is positioned to be more than a sales and service point for PACCAR's product — it becomes a legitimate feedback surface into product engineering itself. Real duty cycles, real failure patterns, and real parts consumption in Atlantic Canadian operating conditions, drawn from a properly modelled record rather than reconstructed after the fact, is not something PACCAR can readily buy. It has to be built by an operator who has already done the unglamorous work of modelling its own data honestly.

We are not proposing a specific programme here, and we are conscious that this depends on interest we do not yet know PACCAR has. What we are noting is that the same architectural choices that make Phase 1 low-risk to ask about also make a much larger, later conversation possible — one about the truck itself, not just the dealership's systems.

## 8. Why it matters, and the truck as an object

Two things are true at once, and neither cancels the other out. Some of this work reduces real difficulty in real people's days: the driver whose truck is easier to keep on the road, the technician whose diagnostic path is shorter and whose back is spared another unnecessary teardown, the small operator whose entire income stops the moment the truck is down. None of that is abstract. It is the actual point of getting the data right.

The other thing that is true: a Peterbilt is a designed object, and people respond to it the way they respond to a well-made car on the road — the same instinct that makes someone notice a Porsche and simply respect it, without needing to know anything about its engineering. That instinct is not decoration on top of the engineering. It is evidence the engineering succeeded at something beyond specification.

We don't think this needs arguing to the people who build these trucks — they already know it. It is worth saying plainly here because it is the reason this work is worth doing carefully rather than quickly, and it is background, not a pitch, for the more immediate and modest ask in Section 5.

## 9. Open questions for PACCAR

1. Who, in dealer systems or PACCAR Parts, should be the standing point of contact for a dealer-led systems initiative like this one?
2. Do Peterbilt dealers report into NADA's ATD 20 Group composite, or into a PACCAR-specific equivalent we should be using instead?
3. Is EDI trading-partner onboarding (AS2 or SFTP) something a dealer group can request directly, and if so, through whom?
4. Does Fortellis, or PRWS specifically, support service-account or unattended authentication for scheduled reads, rather than only interactive sessions?
5. What would PACCAR need to see from us before it would consider a conversation about telematics access, given the terms it has already set out?
6. Does MDI have any existing channel for dealer feedback on recommendation-versus-outcome data, or would that be new to PACCAR as well?
7. Is there an existing data specification for Syncron Returns SmartBlox submissions that we should be aligning to now, ahead of any formal request?
8. Is there an appetite, even in principle, for a future conversation about dealer-sourced field data feeding back into product engineering — and if so, who owns that conversation inside PACCAR?

---

© 2026 EVEglyphDesign. Controlled copy. Key ID EgD-KEY-2026-07.

*Pour le bien-être du peuple.*
