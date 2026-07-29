# Work-list Dispatch Spec

**Programme:** EVEglyphDesign — Peterbilt Atlantic Digital Twin, Phase 1
**Dealer:** Hawkins / Peterbilt Atlantic, New Brunswick — 9 sites, plant codes PA01–PA09
**Currency:** CAD
**Languages:** English / French (Atlantic Canada)
**System of record:** CDK Drive (dealer management system) — the twin is READ-ONLY and never writes to CDK
**Decision support:** Azure-hosted open-source model
**People:** Tim Hawkins (dealer principal), Luke Weatherbie (20 Group access), Craig Allen (16-system register)

**Terminology rule:** the person using the system is the **operator**, never "the user". This rule is used consistently throughout this document and must be preserved in all derived materials.

---

## 0. The design, in the operator's own words

The following is preserved verbatim because the intent — including the humour — should not be paraphrased away by implementers:

> "We execute the work list, but those are just input manually, just like they are today in CDK. So those work lists, we can just send them out as emails — we'll create draft emails for each one, but only if you click them. The operator receives a prioritised work list: one by urgency, and one by strategy. If they want to click and create an email, it takes the contact information and creates a draft email for them. But they have to hit send. And they have to do something else in order for that email to change, because you don't want to make it too easy for people to start firing off emails that the AI tells them. There has to be a little bit of friction in that process — a skill-testing question or something stupid. Or they have to delete the alien from the bottom of it. We just put the alien GIF on the bottom, so they have to at least read the whole thing, delete the alien, and then hit send. Otherwise people know that someone just hit send without deleting the alien. Something like that would be funny to start with anyway. Let Tim maybe take it off."

Everything below is the implementable consequence of this statement. The humour is reported, not performed: no jokes have been added beyond what is quoted above.

---

## 1. Purpose and the non-negotiable boundary

Phase 1 of the digital twin changes what the operator **knows** before acting. It does not change how the dealership **transacts**.

The boundary is non-negotiable and applies without exception across all 9 sites (PA01–PA09):

- The twin **proposes**; the operator **disposes**.
- Nothing is dispatched automatically. No email, message, or notification leaves the system without a human deliberately sending it.
- Nothing is written back to CDK Drive, at any point, under any workflow. The twin reads from CDK-sourced marts; it never writes to CDK.
- Work continues to be entered into CDK manually, exactly as it is today. The work list is a prioritisation and communication aid, not a new channel of record.

If a future phase proposes write-back to CDK or automatic dispatch, that is a distinct decision requiring its own sign-off — it is explicitly out of scope for Phase 1 and is not assumed by anything in this document.

---

## 2. Two lists, two questions

The operator is presented with two separate work lists, each answering a different question:

- **URGENCY list** — "What will hurt if I do nothing today?"
- **STRATEGY list** — "What compounds if I start it this week?"

### Ranking inputs

Both lists are ranked from the conformed data marts. Indicative inputs, drawn per plant code (PA01–PA09):

| List | Primary ranking inputs (from marts) |
|---|---|
| Urgency | Parts inventory and movement (stock-outs, ageing, backorders); service repair orders and labour (open ROs, aged WIP, stalled jobs); work in process; near-term financial exposure |
| Strategy | Unit sales trends; financial performance and absorption; parts movement trends over a longer window; service capacity and utilisation patterns |

### Where the numbers come from

Ranking is computed in SQL from the conformed marts. The model's role is to **explain and order** the results it is given — it does not originate any numeric value that appears on a work-list item. Every figure the operator sees traces to a mart query, not to model inference.

### Why the lists are kept apart

The urgency and strategy lists are deliberately not merged into one. If they were combined, urgency would eat strategy every single day: whatever is on fire today would always outrank whatever compounds this week, and the strategic list would never surface. Keeping them separate is what allows strategic work to be seen and worked at all.

---

## 3. Anatomy of a work-list item

Every item on either list carries the same field set, regardless of which list it appears on.

| Field | Description |
|---|---|
| Item ID | Unique identifier for the work-list item |
| List | Urgency or Strategy |
| Rank | Position within its list, as computed in SQL from the marts |
| Site | Plant code, PA01–PA09 |
| Object reference | The underlying record the item concerns (e.g. repair order, part, unit, account) |
| Observation | The plain-language statement of what was found |
| Figure (as-of marker, lane provenance) | The supporting number, tagged with the date/time it was computed and the data lane it was drawn from |
| Why it ranked here | The ranking rationale, as explained by the model from the SQL-computed rank — not a re-derivation of the number |
| Suggested action | What the twin proposes the operator consider doing |
| Contact | The person to be contacted, resolved from master data |
| Estimated value or exposure (CAD) | The financial figure attached to the item, in Canadian dollars |
| State | Current status of the item (e.g. shown, opened, actioned, aged out) |
| Age | How long the item has been outstanding on its list |

**Provenance flagging:** an item carrying a figure sourced from an unreconciled lane, or one with an open exception recorded against it, is marked as such on the face of the item itself. This flag is not buried in a detail view — it appears wherever the item is displayed, so the operator sees data-quality caveats at the same moment they see the figure.

---

## 4. Draft-only dispatch

The click path is fixed and does not vary by list, site, or item type:

1. Operator selects an item.
2. Operator opens the draft (an explicit click — nothing is pre-opened or pre-sent).
3. The draft is composed from a template, with contact details resolved from master data (not typed by the operator, not guessed by the model).
4. The draft opens in the **operator's own mail client**, unsent.

Nothing leaves the building without a human pressing send. Nothing is auto-populated into CDK — draft creation is a twin-side, mail-client-side action only, with no CDK write of any kind.

**Logging:** every draft creation is logged. The twin records that a draft was created. It does not, and cannot, know whether that draft was subsequently sent — send happens inside the operator's own mail client, outside the twin's visibility. This limitation is by design, not an omission to be fixed later.

---

## 5. The friction gate

### Principle

The cost of sending must stay above zero. The failure mode of AI-assisted outreach is **volume**, not error — a send that costs nothing will be spent carelessly. Ease of dispatch is not a feature to be maximised; in this workflow, some friction is the feature.

### Mechanism

An alien graphic is appended at the foot of every generated draft. The operator must delete it before sending. A recipient who receives an email with the alien still attached can see immediately that it was fired off unread.

The joke is load-bearing. It is a public, self-enforcing signal that:

- costs nothing to implement,
- cannot be gamed without actually reading the message (deleting it requires opening and scrolling the draft),
- and makes lapses visible to the recipient, not just to an internal log.

### Configuration notes

- The graphic must be removable in configuration.
- Tim Hawkins may switch it off.
- It is the kind of thing that stops being funny on the two-hundredth send. Whether it should **rotate** (varying graphic or message) or **expire** (revert to a different gate after a set period or send volume) is recorded as an open question in Section 10, not decided here.

---

## 6. Alternative gates

| Gate | Friction cost to the operator | What it actually prevents | Gameable? | Recommendation |
|---|---|---|---|---|
| Alien deletion | Low — a few seconds, requires scrolling to the foot of the draft | Sending without opening/scrolling the draft at all; makes un-read sends visible to the recipient | Hard to game without reading the message; trivial to game if the operator learns to delete on sight without reading the body | Adopt for Phase 1 launch, per the operator's design |
| Skill-testing question | Low to moderate — depends on question design | Sending on true autopilot (no interaction at all) | Easily gamed once the answer pattern is memorised | Acceptable as a fallback if the alien is switched off, but weaker as a signal to the recipient |
| Mandatory free-text line ("why this contact and not another") | Moderate — requires a written justification each time | Contacting the wrong person, or contacting someone reflexively rather than deliberately | Gameable by boilerplate text, but boilerplate is itself visible on review | Useful for audit trail; adds real friction but also real logging value — consider pairing with the alien rather than replacing it |
| Timed hold before send | Low effort, but costs real elapsed time | Impulsive same-second sends; gives a cooling-off window | Not gameable in the sense of skipping it, but operators can simply wait it out without re-reading | Useful for high-value items; poor fit as a universal gate since it slows every item equally regardless of stakes |
| Daily send cap | None per-send, but constrains total volume | Runaway volume across a day, not carelessness on any single send | Not gameable per item, but can be worked around by spreading sends across days | Complements a per-item gate; does not replace one, since it does nothing to stop a careless individual send |

A gate the operator learns to click through has become theatre. Any gate adopted should be reviewed periodically against this test, including the alien.

---

## 7. Bilingual drafts

- Drafts are produced in English or French, reflecting Atlantic Canada's bilingual dealer environment.
- Language is selected from the **contact's own preference field**, where held in master data.
- Language is **never guessed from surname** or any other proxy.
- Every draft states clearly which language was used and why (i.e., that it reflects the contact's recorded preference), so the operator is not left to infer the reasoning.
- Where no preference is held, this is itself a data-quality gap to be resolved with master data owners rather than defaulted to a guess (see open questions, Section 10).

---

## 8. What is logged

The dispatch ledger records, for every item and every draft:

- Item shown (to which operator, when)
- Item opened
- Draft created
- Draft template version
- Model version (the specific version of the Azure-hosted model that produced the explanation/ranking narrative shown)
- The figures as presented, together with their as-of markers
- Gate satisfied (which friction gate was completed, and confirmation it was completed — not merely offered)

**Why this matters:** this record lets anyone, later, ask what the operator was told at the moment they acted — which figures they saw, how current those figures were, which lane they came from, and what version of the model and template produced the wording in front of them. This is the audit trail that makes the "twin proposes, operator disposes" boundary defensible after the fact, not just at design time.

---

## 9. Measures of whether this is working

Deliberately **not** "emails sent". Suggested measures:

- Items acted on as a proportion of items shown (uptake, not output)
- Items ageing out unactioned (what the operator saw but never worked)
- Exposure closed, in CAD (the financial outcome, not the activity)
- Repeat items recurring after being marked done (whether "done" actually resolved the underlying issue)

A rising send count with a flat outcome is a failure signal, not a success one — it indicates volume without effect, which is precisely the failure mode the friction gate in Section 5 exists to guard against.

---

## 10. Open questions

| # | Question | Best placed to answer |
|---|---|---|
| 1 | Should the alien graphic stay on by default at go-live, or does Tim Hawkins want it off from day one? | Tim Hawkins |
| 2 | If the alien is kept, should it rotate (different graphic/message per draft) or expire (switch to another gate after a set time or send volume)? | Tim Hawkins |
| 3 | Where a contact's language preference is not held in master data, what should the default be, and who owns correcting the gap? | CDK administrator |
| 4 | Should the mandatory free-text justification (Section 6) be added alongside the alien for high-value items, or kept out of Phase 1 entirely? | Luke Weatherbie |
| 5 | What CAD exposure threshold, if any, should trigger a stronger gate (e.g. timed hold) rather than the standard alien gate? | Craig Allen |
| 6 | Who reviews the dispatch ledger, and how often, to check whether gates are becoming theatre (Section 6)? | Luke Weatherbie |
| 7 | Should a daily send cap be introduced per operator, and if so, what should the cap be? | Tim Hawkins |
| 8 | Which master-data source is authoritative for contact resolution across all 9 sites, and who maintains it (register ownership)? | Craig Allen |

---

© 2026 EVEglyphDesign. Controlled copy. Key ID EgD-KEY-2026-07.

*Pour le bien-être du peuple.*
