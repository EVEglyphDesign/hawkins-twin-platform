# Briefing Note — Hawkins Truck Mart / Peterbilt Atlantic

## The EVE / DMZ Open opportunity: twinning the Murphy-Hoffman blueprint for Atlantic Canada

**Prepared for:** Tim Hawkins, CEO & Owner — Hawkins Truck Mart Ltd. / Peterbilt Atlantic (Hanwell, New Brunswick)
**Champion (New Brunswick):** Luke Weatherby
**Prepared by:** EVE Glyph Design
**Posture:** Surgical, not disruptive — and non-profit by default (*pour le bien-être du peuple*)
**Date:** July 1, 2026

---

## 1. Why we are writing

Tim, you were one of our original research-and-development partners, and you are a consequential beneficiary of what that work has produced. We have now completed a full, production-grade integration blueprint for the **Murphy-Hoffman Company (MHC) — the Kenworth/PACCAR dealer group in Kansas City** — and it is ready to be *twinned* for Hawkins Truck Mart.

This note gives you two things in plain terms:

1. **What we have to offer** — the technical twin of the MHC system, sized for Peterbilt Atlantic and its nine centres across Eastern Canada ([Peterbilt Atlantic — Dealership Information](https://www.peterbiltatlantic.com/about-us-heavy-trucks-trailers-dealership--info)).
2. **The ethos behind it** — a toned-down version of our founding principles, so you understand the kind of enterprise we are building and why it works the way it does.

---

## 2. Who we are — the ethos in one page

EVE Glyph Design is not a conventional software vendor. We are organized as a **charitable, non-commercial body** dedicated to the welfare of the people — closer in spirit to a stewardship order than a startup. Our work descends from a decision-intelligence framework we call **The Thériault Method** ("the glyph"), which traces to a New Brunswick family lineage in Paquetville and rests on a simple, recurring idea: **the original protection of the individual**.

Four principles are enough for this conversation:

- **Non-Disruption Posture.** We deliberately take the opposite position of incumbents *without trying to displace them*. PACCAR, BRP, SAP, Salesforce — they keep their operational role. We interoperate; we do not replace. Your existing investments stay intact and get *more* valuable.
- **The Yield Clause.** We build a new competitive surface and then **yield it for the benefit of others**, on purpose. We anchor prior art publicly so the surface cannot be captured or fenced off by anyone — including us. This is a protective act, not a monopolizing one.
- **Nonprofit default.** Our part of any engagement stays non-profit. That does not stop us from sharing in the profits of our commercialization partners — which is exactly the arrangement we would propose with you.
- ***Pour le bien-être du peuple.*** Our first-contact phrase and our test for every design decision: does this help people get outside and live their lives, rather than curl up in front of screens that aren't real? Better distribution tools and better equipment for real, physical life — that is the point.

That is the whole ethos in one breath: **research sovereignty, non-disruption, yield — surgical, not disruptive, and non-profit.**

---

## 3. What we built for Murphy-Hoffman (and what we would twin for you)

For MHC — a 130+ location Kenworth/Volvo/Isuzu group running on a **PACCAR SAP S/4HANA** dealer instance — we designed an end-to-end system that takes a roadside/service event from intelligent intake all the way through dispatch, billing, vendor payables, and analytics, with full financial control and audit trail.

The heart of it is a **governed three-tier pattern**:

| Tier | What it does | Components |
|---|---|---|
| **1 — Intelligent execution** | AI intake, triage, vendor matching, case management | Azure AI agent + Salesforce Service Cloud |
| **2 — ERP core** | Service orders, POs, billing, GL postings, approvals | **SAP S/4HANA** + governed CPI middleware |
| **3 — Analytics** | Operational + financial KPIs, margin analysis, reconciliation | Salesforce dashboards → SAP Datasphere / datalake |

The design principle that matters most to you: **the AI never writes to SAP directly.** Every financial posting flows through governed middleware with validation and human-in-the-loop approval gates, using SAP's *standard* open interfaces (OData APIs, BAPIs). That means **no custom code in the SAP core that breaks on patch day**, and **zero dependency on any single vendor's proprietary connector** — you never get locked in. This is the Non-Disruption Posture expressed in architecture.

For MHC, the outcomes we targeted were concrete: 25–35% faster create-to-dispatch, meaningful DSO reduction, automated incident-to-invoice, and a scalable foundation that grows without re-platforming.

---

## 4. Why this fits Hawkins Truck Mart specifically

You already sit at the intersection of two sizable SAP investments that we can plug into rather than compete with:

- **PACCAR** purchased **SAP S/4HANA** and runs a centralized Transportation Portal / Global Trade platform to harmonize its North American logistics with real-time shipment visibility ([SAP Innovation Awards — PACCAR logistics deck](https://www.sap.com/bin/sapdxc/proxy.inmsl.attachment.11352.pitch-deck.pdf); [Mainline — PACCAR + SAP HANA case study](https://mainline.com/wp-content/uploads/PDFs/CS_PACCAR-Power.pdf)).
- **BRP** operates its own **SAP S/4HANA Center of Expertise** for logistics — Extended Warehouse Management (EWM) and Transportation Management (TM) across a large, multi-business-unit landscape ([BRP — Senior SAP S/4HANA Logistics Analyst posting](https://www.jobillico.com/en/job-offer/brp-/senior-sap-s-4hana-logistics-analyst-ewm-tm-/16884591)).

Both are state-of-the-art SAP logistics platforms. Our system is designed to **interact directly with exactly this kind of state-of-the-art SAP environment** through standard, non-invasive interfaces. That is the whole point of twinning the MHC blueprint here: you get the same governed, upgrade-safe, AI-assisted incident-to-cash system, calibrated to Peterbilt Atlantic's footprint — nine centres serving five Eastern Canadian provinces from your Hanwell head office, built on 50+ years of family experience in the truck business ([Peterbilt Atlantic — Staff / CEO profile](https://www.peterbiltatlantic.com/view-our--xstaff)).

---

## 5. The proposed structure

Two parts, cleanly separated:

- **Our part (EVE)** remains **non-profit** — the governance, methodology, and decision-intelligence canon. This is the stewardship layer, and it does not change.
- **Your part** is the **commercialization partnership.** As one of our original R&D partners, you engage as a commercial beneficiary. We share in the profits of that commercialization; you get a system that makes your PACCAR/BRP-aligned SAP investments work harder without disrupting them.

Because we yield the surface publicly and anchor the prior art, neither of us has to worry about the platform being captured or enclosed down the road. That protection is built in.

---

## 6. The people — how the meeting works

This is a **champion-to-champion** meeting, then a managed hand-off:

- **Your champion:** **Luke Weatherby** — the rock star of the group, and the rock star from New Brunswick. In this meeting, Tim, you would put Luke into a **technology-application** role on your side.
- **Our side:** we bring Luke into the **AI team alongside Tobias**, so the New Brunswick champion sits inside the technology transition from day one.
- **The transition:** EVE manages the connection and the technology transfer end-to-end, with Luke as the bridge between both organizations.

The introduction, in short: **my champion and Tim's champion meet — and then I manage the connection and the transition of the technology.**

---

## 7. The ask

Consistent with our first-contact posture, the decision comes down to three questions:

1. **Do you want the twin?** — the MHC-proven governed system, calibrated for Peterbilt Atlantic.
2. **Do you accept the interoperate-don't-replace approach?** — plug into PACCAR and BRP's SAP platforms, no lock-in, upgrade-safe.
3. **Do you accept the two-part structure?** — EVE non-profit above, commercialization partnership below.

Three yeses opens the working surface and we schedule the champion-to-champion session with Luke. If the answer is no, it closes cleanly — by design.

---

*The pattern came first. The pipe came second. The governance came third. We build for people to get outside and live — pour le bien-être du peuple. That was just our way.*

---

### Sources
- Tim Hawkins, CEO — background, founding (1994), nine centres across Atlantic Canada: [Peterbilt Atlantic — Staff](https://www.peterbiltatlantic.com/view-our--xstaff)
- Peterbilt Atlantic dealership scope (five Eastern Canadian provinces, Hanwell): [Peterbilt Atlantic — Dealership Information](https://www.peterbiltatlantic.com/about-us-heavy-trucks-trailers-dealership--info)
- PACCAR SAP S/4HANA logistics / Transportation Portal: [SAP Innovation Awards 2021 deck](https://www.sap.com/bin/sapdxc/proxy.inmsl.attachment.11352.pitch-deck.pdf); [Mainline PACCAR + SAP HANA case study](https://mainline.com/wp-content/uploads/PDFs/CS_PACCAR-Power.pdf)
- BRP SAP S/4HANA Center of Expertise (EWM/TM logistics): [BRP — Senior SAP S/4HANA Logistics Analyst](https://www.jobillico.com/en/job-offer/brp-/senior-sap-s-4hana-logistics-analyst-ewm-tm-/16884591)
- MHC RoadAssist SAP integration blueprint — internal EVE reference document (three-tier pattern, governed CPI middleware, incident-to-cash design)
