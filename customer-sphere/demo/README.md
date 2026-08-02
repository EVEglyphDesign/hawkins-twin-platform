# customer-sphere/demo/ — Customer Sphere demonstration surface

Live surface: [Customer Sphere demo](https://eveglyphdesign.github.io/hawkins-twin-platform/customer-sphere/demo/)

The [Customer Sphere design](../CUSTOMER-SPHERE-DESIGN.md) made clickable, on **100% synthetic
data**. No dealership data has moved, nothing on this surface is a measurement of the business,
and the live dealer management system is never written to.

## What it demonstrates

| Screen | Design section | What it shows |
|---|---|---|
| **Worklist** | §6.3 | Accounts ranked by the widest gap between current and target, weighted by account value. Ranking falls out of the geometry rather than being a rule somebody maintains. Split urgency above, structural digest below. |
| **The sphere** | §6 | One customer at the centre, seven faces drawn as vectors. Length is the gap. Commercial, service, parts, finance, warranty, relationship, marketing. |
| **A face** | §5, §6 | The vector's direction, magnitude, origin and target; which journal it aligns to — ACDOCA unmodified, ACDOCI for interactions — and the sources that contributed. |
| **Disagreement** | §6.2 | Where two sources disagree, both vectors are held with their origins and confidences intact. Nothing is averaged away. |
| **Stewardship queue** | §8 | Candidate identity links with the score and the rule that produced each one. Nothing auto-merges. Merges are reversible. A person at an organisation is an affiliation edge, never a merge. |
| **Index card** | §2, §3 | The GitHub half of the two-body split. One field, every vocabulary it has, a pointer into the tenant Postgres, and what governs it — and never a value. |
| **The gate** | §10 | The exact dispatch envelope, carrying `write_to_dms: false` as a property rather than a setting. Nothing leaves without a human approving it. |
| **The record** | §9 | The closure trail, walkable back to the extraction that produced every number, and evidence that CDK was not touched. |

Three list recipients are selectable. Names appear without titles, per
[the naming canon](../../canon/naming-people.md).

## Navigation

Every screen has an address, so the browser back and forward buttons work and any screen
can be linked to directly — `#/a/CS-0002/f/finance` is the finance face of Restigouche
Aggregate Co, and it will still be there tomorrow. Three things are always on the page:

- a **section bar** of five items with the current one marked, following the
  [GOV.UK service navigation pattern](https://design-system.service.gov.uk/components/service-navigation/);
- a **breadcrumb** whose every earlier segment is a link;
- an **account strip**, so moving sideways from one account to another never requires
  going back to the worklist first. A dispatched account keeps its tick.

Changing the list recipient keeps you on the screen you are reading rather than
returning you to the worklist.

## What it is not

It is not a measurement of the dealership. Every customer, vehicle, phone number, amount and
timestamp is invented for this demonstration. Real figures are unknowable until the sphere reads
real data, and that is gated on the executed agreement (§10).

## Files

| File | Role |
|---|---|
| `index.html` | Page shell and font loading |
| `app.css` | EVEglyphDesign palette and type canon |
| `data.js` | All synthetic data, in one file, readable end to end |
| `app.js` | Routing, screen rendering and state. No framework, no build step, no network calls |

© 2026 EVEglyphDesign. *Pour le bien-être du peuple.*
