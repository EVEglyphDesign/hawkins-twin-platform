# Warranty GENE — Luke access prep (BRP)

For the next sit-down with Luke on the BRP side. The BRP-brand rooftops run under **Torque Motorsports**, not Hawkins. Same customer service initiative as the Peterbilt document (EgD-WGB-003) — Tim wants his team to give owner-operators clearer answers at the counter on their own vehicle. Different feeds, different rooftop name on every outbound message. Same backend. The BRP aftermarket warranty ecosystem is denser than the heavy-truck side, which means there is more per-VIN coverage to surface and more per-VIN money to keep from leaking. Every ask reads as customer service. Nothing else.

**Internally, the picture is the same as the Peterbilt side.** Torque Motorsports is turning on feeds into the same sovereign data replica — the record already owned under agreements already signed. The seed layer for every BRP VIN is what already lives in GitHub: the original bill of sale, factory options as delivered, and the customer profile at the time of sale. When Lightspeed opens as a feed the replica gains everything Torque Motorsports has ever done to the VIN. When each administrator opens as a feed the replica gains the coverage picture beyond BRP's factory warranty. Automation compounds on top: WarrantyGENE reads across every open feed and returns a single coverage line at the counter. No single counterparty is a gate.

**Least questions is the goal.** Same discipline as the Peterbilt document. Each ask short, each ask standalone, no cross-references between counterparties in writing. What sits behind the initiative on our side — the replica, the automation, the compounding value — is not part of any outbound message. It is understood internally and stays internal until there is a result worth showing.

**One rooftop name per conversation.** Every outbound BRP-side quote in this document names **Torque Motorsports**. Every outbound Peterbilt-side quote in EgD-WGB-003 names **Peterbilt Atlantic**. Luke never mixes the two names in one message. Neither BRP nor its administrators nor Lightspeed hear the Peterbilt Atlantic name; neither PACCAR nor CDK nor the truck-side suppliers hear the Torque Motorsports name. Same operator behind both, different faces at the counter.

**Working assumptions to correct on first read.** These are the anchors Luke will say out loud. If any are wrong, correct them and this document is reissued at the same canon URL.

- The BRP rooftops trade as Torque Motorsports.
- Full BRP line coverage — Ski-Doo, Sea-Doo, Can-Am On-Road (Spyder / Ryker), Can-Am Off-Road (SxS, ATV), Lynx, Rotax.
- DMS is Lightspeed EVO.
- Peter is the internal authorizer for Torque Motorsports subscriptions the same way he is for Peterbilt Atlantic.
- Same eight-to-ten-week external spacing, adjusted around the powersports pre-season crunch (August through October for snowmobile, March through May for watercraft) — Luke drops asks outside those windows if he can help it.

---

## Contact map

| # | Party | Who Luke asks | What we're asking for |
| --- | --- | --- | --- |
| 1 | Lightspeed | Luke's Lightspeed account manager | Read-only service-account access to Torque Motorsports' own DMS records under existing Lightspeed subscription |
| 2 | BRP corporate | Luke's BRP district manager | Read-only service-account access to the BRP dealer portal and B.E.S.T. lookup under existing dealer agreements |
| 3 | Peter (internal) | Peter, in conversation | Authorization to attach a Torque Motorsports service-account mailbox to BRP-side subscriptions |
| 4 | Third-party administrators, wave one | One rep per administrator | Read-only service-account access under existing authorized-dealer relationship |
| 5 | Third-party administrators, wave two | One rep per administrator | Read-only service-account access, or phone-in coverage-lookup protocol |
| 6 | Selling-dealer outreach (internal) | Torque Motorsports advisors | Counter workflow for resolving unknown-administrator cases on first visit |

---

## 1. Lightspeed

**Who Luke asks.** His current Lightspeed account manager.

**What Luke says.**

> Torque Motorsports is rolling out a customer service initiative for our customers — giving them a clearer picture of their vehicle history when they come in. To do that on our side we need a read-only service-account attached to our existing Lightspeed subscription, covering the same records our advisors already see. Service-account mailbox, not a personal login.

**What Luke does not say.**

- Nothing about a workflow, an integration, a project, a due-diligence review, or a proof of concept.
- Nothing about API scope, ETL, or exports in this message. Each named surface is a question the account manager will ask.
- Nothing about scope beyond the Torque Motorsports rooftops and "the same records our advisors already see."
- Nothing about Peterbilt Atlantic. Lightspeed does not need to know Luke also runs a heavy-truck DMS conversation elsewhere.

**What good looks like.** A service-account login is provisioned. Nothing else changes.

---

## 2. BRP corporate — Luke's district manager

**Who Luke asks.** Luke's BRP district manager, one message covering both the dealer portal and B.E.S.T.

**What Luke says.**

> Torque Motorsports is rolling out a customer service initiative for our customers — helping them get better answers on coverage and history at the counter. On our side, that means a Torque Motorsports service-account with read access to the same BRP dealer portal material our team already uses, and B.E.S.T. contract lookup by VIN under our existing dealer agreements.

**What Luke does not say.**

- Nothing about BOSSWeb versioning, DTC access, campaign feeds, or telematics scope in this message. Same reason as the PACCAR ask on the truck side — every named surface is a question.
- Nothing about which BRP lines are in scope beyond "the material our team already uses." Line-specific coverage sorts itself out from the dealer authorization once the login is provisioned.
- No reference to Peterbilt Atlantic. BRP corporate does not need to know Luke also runs heavy-truck conversations elsewhere.

**What good looks like.** A service-account login is provisioned covering the dealer portal and B.E.S.T. lookup by VIN. Nothing else changes.

---

## 3. Peter — internal, BRP extension

**Who Luke asks.** Peter, in a private conversation. Not by email. Same conversation as the Peterbilt-side authorization if the timing works; a separate one if not.

**What Luke says.**

> Tim's customer service initiative — same one we talked about for the Peterbilt Atlantic side, now for Torque Motorsports too. Housekeeping on my side: I want a Torque Motorsports service-account mailbox attached to the Lightspeed and BRP subscriptions and to the third-party warranty administrators we work with on the BRP side, so it's not tied to any one person's login. Same data, service-account login instead of personal.

**What Luke does not say.**

- Nothing about the replica, the automation, or WarrantyGENE. Peter knows enough of the picture already; anything more said out loud is a detail he doesn't need to carry and a detail that could travel.
- Nothing about the BRP economics being potentially larger than the Peterbilt economics. That's an internal insight, not an outbound one.
- No numbers, no administrators named yet at first pass.

**What good looks like.** Peter says yes — which he will, because it's Tim's initiative and it's for customers — and the Torque Motorsports service-account mailbox is authorized for the BRP-side subscriptions within the week.

---

## 4. Third-party administrators — wave one

**Who Luke asks.** One rep per administrator, four separate conversations. These are the four largest administrators in the powersports F&I channel and are most likely to have a dealer portal or an API on file.

- **Assurant / American Bankers** — dealer relations desk for powersports.
- **Portfolio Group (Portfolio Protection)** — dealer relations desk for powersports and RV.
- **EasyCare (APCO Holdings)** — dealer relations desk for powersports.
- **Zurich (Universal Underwriters)** — dealer F&I services for powersports.

**What Luke says, per administrator.**

> As an authorized service dealer for BRP product covered under [administrator] contracts, Torque Motorsports is rolling out a customer service initiative for our customers — clearer answers on coverage and history at the counter. Under our existing dealer relationship, please provision a Torque Motorsports service-account with read access to coverage lookup by VIN and by contract number for contracts we service.

**What Luke does not say.**

- Nothing about API access, bulk export, or session logs.
- Nothing about claim-denial rates, reconciliation, or pre-submission checks.
- Nothing about the other three administrators.
- Nothing about BRP corporate.
- Nothing about Peterbilt Atlantic. Administrators are cross-industry in F&I; there is no reason for them to hear the truck-side name.

**What good looks like.** Four service-account logins, one per administrator, each covering coverage lookup by VIN plus by contract number for contracts Torque Motorsports services. The counter conversation stops being "let me call them and get back to you" and becomes "here's what you have."

---

## 5. Third-party administrators — wave two

**Who Luke asks.** One rep per administrator, spaced. This wave is the smaller powersports F&I administrators and the bank- or credit-union-branded programs. Some have portals, some don't. The ask is the same; the fallback is different.

- **ProGuard (Protective Asset Protection)** — dealer relations.
- **CornerStone / GWC** — dealer relations.
- **Bank- and credit-union-branded programs** — resolved individually as they appear on contracts, usually white-labeled on top of one of the wave-one administrators.
- **Any powersports administrator surfaced at the counter that we do not yet have a relationship with** — added to this wave on the fly, one at a time, as they appear.

**What Luke says, per administrator (portal path).**

> As an authorized service dealer for BRP product covered under [administrator] contracts, Torque Motorsports is rolling out a customer service initiative for our customers — clearer answers on coverage and history at the counter. Under our existing dealer relationship, please provision a Torque Motorsports service-account with read access to coverage lookup by VIN and by contract number for contracts we service.

**Phone-in fallback.** If the administrator has no dealer portal, the ask converts into a workflow rather than a login: Luke confirms the authorized dealer-lookup phone line, the required verification (usually VIN plus customer last name), and the internal contact so Torque Motorsports advisors can make the call before quoting. The result of every phone call is written into the replica against the VIN, dated, so the next visit does not repeat the call.

**What Luke does not say.**

- Nothing that would suggest Torque Motorsports is grading administrators against each other. F&I channel administrators talk to each other.
- Nothing about wave one — waves are internal spacing, not something the administrators see.

**What good looks like.** Each wave-two administrator ends up in one of three buckets: portal login provisioned (best), phone-in workflow documented with contacts (workable), or "administrator declined; we call the claims desk cold and cache the result" (slowest, still fine).

---

## 6. Selling-dealer outreach — internal counter workflow

**Not an outbound ask.** This is an internal Torque Motorsports workflow for the case where a customer arrives with a BRP unit under some third-party warranty and does not know who the administrator is. Common on used BRP product, especially watercraft and older snowmobile.

**What Torque Motorsports advisors do at the counter.**

1. **Ask the customer for the contract paperwork.** If they have their finance folder from delivery, the administrator's name is on page one of the service contract.
2. **If the customer doesn't have the paperwork, read the selling dealer off the bill of sale.** The bill of sale is in the replica for every VIN Torque Motorsports has ever sold; for VINs Torque Motorsports did not sell, ask the customer for it or pull it from the BRP dealer portal record.
3. **Dealer-to-dealer phone call to the selling dealer's F&I office.** One question: "what administrator were you writing through in model year X?" F&I offices are used to this call and answer it in minutes.
4. **Write the resolution into the replica against the VIN.** The next visit against the same VIN starts at wave-one or wave-two coverage lookup, not at unknown-administrator.

**Why this belongs in the Luke prep.** It closes the last coverage-picture gap without needing another counterparty. The replica converts the tier-3 unknown into a tier-1 or tier-2 known on the first visit. Every VIN becomes cheaper to serve on every subsequent visit.

---

## Three things off every conversation

1. **The workflow.** Never named. No "reconciliation," no "due diligence," no "proof of concept," no "twin." The frame is customer service, full stop.
2. **The scope.** Never described as broader than "the same material our team already uses" or "the same records our advisors already see." Any language that suggests we want more than what personal logins already give us invites a governance review.
3. **The other counterparties.** Never named inside another counterparty's message. Each ask stands alone. Powersports administrators in particular talk to each other in the F&I channel — do not give them a reason to compare notes.

---

## Order of operations

Spaced, not stacked. Adjusted around the powersports pre-season crunch.

1. **Peter first.** Same conversation as the Peterbilt-side authorization if the timing works; a separate one if not.
2. **Lightspeed, standalone.** After Peter confirms.
3. **BRP corporate, standalone, a week later.** Not the same week as Lightspeed.
4. **Wave-one administrators, one per week.** Assurant first (largest book on powersports), then Portfolio, then EasyCare, then Zurich.
5. **Wave-two administrators, one per week.** ProGuard, CornerStone/GWC, plus any bank- or credit-union-branded program surfaced at the counter, resolved on the fly.
6. **Selling-dealer outreach** — internal, live from day one. Does not wait for external provisioning.

Total elapsed time to have Lightspeed, BRP corporate, and the wave-one administrators provisioned: six to seven weeks. Wave two runs concurrently and finishes when it finishes. Avoid August through October and March through May for external asks if the calendar allows — those are the powersports pre-season windows and the counterparties' warranty desks are busiest then.

---

## Where this fits with the Peterbilt document

- Same customer service initiative on the outbound.
- Same sovereign data replica on the internal.
- Same standalone-ask pattern.
- Same eight-to-ten-week spacing discipline, adjusted for powersports seasonality.
- Same Peter, same Luke.
- Different rooftop name on every outbound message: **Torque Motorsports** here, **Peterbilt Atlantic** on the truck side. Never mixed.
- Different feeds. That is the only real difference on the backend.

The two documents run in parallel on independent calendars. Nothing in one gates anything in the other. WarrantyGENE reads across both replicas as one at the counter, but each side's counterparties see only their own conversation, under their own rooftop name.

---

## Provenance

- **Revision.** This is EgD-WGB-004 revision 1. Sibling to EgD-WGB-003 (Peterbilt) rev-5. Same tone, same discipline, different feeds.
- **Working assumptions block on page one** is designed to be corrected on first read. Once Luke confirms or corrects, this document is reissued at the same canon URL with revision 2.
- **BRP-side seed layer for every VIN** — bill of sale plus factory options plus customer profile at delivery, all under Torque Motorsports — lives in the sovereign replica in GitHub from day one. Lightspeed and BRP corporate feeds layer on top of that seed as they open. Third-party administrator coverage lookups layer on top of both. WarrantyGENE reads across all layers at the counter.
- **BRP economics.** Not on any outbound page. Internal understanding only: the aftermarket administrator ecosystem on BRP is denser than on heavy trucks, which likely makes the per-VIN warranty coverage picture larger and the per-VIN money-left-on-the-table risk higher. This is a reason to run the BRP sweep with the same discipline as the Peterbilt sweep, not a reason to run it faster or louder.
