# Start here — Hawkins Twin

**For Luke Weatherbie and his Claude.** This page is the front door to the whole Hawkins Twin
lane: the design and outreach work, the data build, and the Azure build. Read it once, then use
[`lane/LANE-MAP.json`](lane/LANE-MAP.json) as the machine-readable reference.

> **This repository is public.** It holds design, rules, names and states. Dealer figures,
> customer names and VINs live in private repositories and in Hawkins Azure, never here.

---

## 1. What the Hawkins Twin is, in three sentences

1. **Record.** Peterbilt Atlantic's customer, vehicle, service, warranty and interaction history
   is reassembled into one dealer-owned record in Hawkins Azure, joined on the VIN.
2. **Decide.** WarrantyGENE, the Owner Console and the Customer Sphere read only that record.
3. **Act.** One surface, one question panel, one human release point. People decide bookings;
   PACCAR systems decide claims.

Source: Integrated Blueprint 1.0 DRAFT `EgD-BP-HAWKINS-TWIN-001` (private, see §4).

## 2. The four workstreams

| Workstream | What it covers | Where to look | State |
|---|---|---|---|
| **Design** | How Tim and the team see the twin: Owner Console, Customer Sphere, WarrantyGENE surfaces | This repo: [`owner-console/`](owner-console/), [`customer-sphere/`](customer-sphere/), [`warranty-gene/`](warranty-gene/), [`demo/`](demo/). Real-data surfaces v1/v2: private SmartLINQ repo | Built (synthetic here; real aggregates private) |
| **Outreach** | How the work reached Peterbilt Atlantic, and how the twin reaches truck owners | [`tim-vip.html`](tim-vip.html), [`handoff/`](handoff/), [`interactions/`](interactions/); outreach workbook and Notify queues in the private repos | Built |
| **Data build** | Extracts → one VIN-keyed warehouse | [eve-hawkins-cdk-twin](https://github.com/EVEglyphDesign/eve-hawkins-cdk-twin) (public model), [eve-hawkins-paccar-smartlinq](https://github.com/EVEglyphDesign/eve-hawkins-paccar-smartlinq) (private) | Built on 17–18 Sep 2026 extracts |
| **Azure build** (Tobias) | The dealer-owned home for the record | [`lane/AZURE-WORKSTREAM.md`](lane/AZURE-WORKSTREAM.md) | Designed; build details **not yet recorded** |

## 3. Read in this order (about 45 minutes)

1. **This page.**
2. **[`lane/LANE-MAP.json`](lane/LANE-MAP.json)** — every repository, document, gate and open
   item with its state. Your Claude should load this first.
3. **[`lane/AZURE-WORKSTREAM.md`](lane/AZURE-WORKSTREAM.md)** — what Azure is for and what is
   still to be written down.
4. **[`warranty-gene/WARRANTY-GENE.md`](warranty-gene/WARRANTY-GENE.md)** — the VIN row contract
   and the two-step operating model.
5. **[`owner-console/`](owner-console/)** — the executive dashboard map (7 ATD tiles, 60 COVs).
6. **In the private SmartLINQ repo** (you have write access):
   `00-START-HERE.md`, then `BLUEPRINT.md`, then `surface/hawkins-twin/HANDOFF.md`.

## 4. Repositories in the lane

| Repository | Visibility | Role | Last activity |
|---|---|---|---|
| hawkins-twin-platform (this) | public | Program surface, design, lane map | 2026-10-05 |
| [eve-hawkins-paccar-smartlinq](https://github.com/EVEglyphDesign/eve-hawkins-paccar-smartlinq) | private | Telemetry build, blueprint draft, real-data surfaces | 2026-10-04 (draft PR #1) |
| [eve-hawkins-cdk-twin](https://github.com/EVEglyphDesign/eve-hawkins-cdk-twin) | public | CDK data model and warehouse (no dealer rows) | 2026-09-17 |
| [eve-dealer-parts-twin](https://github.com/EVEglyphDesign/eve-dealer-parts-twin) | public | Parts model (synthetic seed) | 2026-08-30 |
| [eve-hawkins-sovereign-enterprise](https://github.com/EVEglyphDesign/eve-hawkins-sovereign-enterprise) | public | Strategy paper | 2026-08-30 |
| eve-hawkins-truck-mart | private | Commercial note and contract economics | 2026-08-14 |
| hawkins-twin-compliance-vault | private | Agreements and sign-offs | 2026-07-29 |
| eve-hawkins-telus-twin (origin-labs-co) | private | Calls and mail | not visible from here |

## 5. Before technical work: Step 0

The compliance vault sets the rule: nobody moves into technical work until their agreements are
uploaded and a written sign-off from Dany and Tim names them and what they may commit. Ask Dany
where your sign-off stands before your Claude changes anything.

## 6. How we work (several people, several AI surfaces)

- The **repository is the shared memory** between Dany (Perplexity, Claude), Tobias (Claude) and you.
- **Branch, then pull request.** Never push to `main`.
- **Done = GitHub shows the commit.** Not when an AI says so.
- **Leave a trail.** Every commit and PR says what changed and why.
- **Public vs private.** Names, states and rules can be public. Figures, customers and VINs cannot.

### A first prompt for your Claude

```
Read 00-START-HERE.md and lane/LANE-MAP.json in EVEglyphDesign/hawkins-twin-platform,
then lane/AZURE-WORKSTREAM.md. Summarise: the four workstreams and their state, which
repositories hold what, the gates before technical work, and the open items with owners.
Read-only — don't change anything.
```

## 7. Open items

See `open_items` in [`lane/LANE-MAP.json`](lane/LANE-MAP.json). The ones that need you:
which DMS each site runs, and what you and Tim asked to see, in your own words.

---

*Added 2026-10-05 by Claude (chat), at Dany's request, so Luke's Claude has one front door to the lane.*

© 2026 EVEglyphDesign. Controlled copy.
