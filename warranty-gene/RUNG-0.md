# Warranty GENE — Rung 0 for the API and data-custody expansion

**EVEglyphDesign · Hawkins Twin Platform · Warranty GENE**
**Frame:** [`EgD-BOOT-001` §1a](https://eveglyphdesign.github.io/eve-glyph-boot-contract/#1a-rung-0-outcome-and-custody-frame-added-2026-08-24) · **Prepared:** 2026-08-24
**Companion to:** [`WARRANTY-GENE.md`](./WARRANTY-GENE.md)

---

## Outcome

Peterbilt Atlantic recovers the warranty dollars it is entitled to but is not currently
billing, by turning every VIN broadcasting into Tim Hawkins's region into a scheduled,
parts-staged booking before someone else claims the truck.

## Owner participation points

1. **Tim Hawkins and Luke Weatherbie** authorize which OEM and telematics contracts to
   pursue — the module cannot enter another party's system without their signature above
   it.
2. **The dealer principal** signs the data-sharing terms with PACCAR, Fortellis, and any
   third-party telematics provider the fleet uses. No signature, no feed.
3. **Peterbilt Atlantic IT** names the system of record for the VIN plus its usage
   metrics (odometer, engine hours, in-service date, coverage-window state). The GENE
   reads from that system; it does not create a second one.
4. **The warranty admin** owns the PRWS submission boundary. The GENE identifies rich
   targets; PRWS remains authoritative for claim filing. This boundary is fixed and does
   not move.

## Data custody map — named parties, not systems

| Participation point | Before | During | After |
|---|---|---|---|
| 1 · Contract authorization | Tim and Luke | Tim and Luke | Tim and Luke |
| 2 · Data-sharing terms | PACCAR (telemetry), the fleet (fault stream), the dealer (RO and labor) | PACCAR and the dealer, jointly under the signed terms | The dealer, for the retention window PACCAR's terms allow |
| 3 · System of record (VIN + metrics) | The dealer (Procede Excede is dealer-owned) | The dealer | The dealer; the GENE reads a view, never owns the row |
| 4 · PRWS submission | PACCAR | PACCAR | PACCAR |

EVEglyphDesign is custodian of none of the above. The Warranty GENE is a lens over
data other parties hold; it produces a booking recommendation and lands it beside the
dealer's own calendar. Fortellis, where used, is a broker of API access, not a
custodian of the data that passes through it.

## Boundary of this turn

This document names the outcome and custody posture only. It does **not** name API
endpoints, authentication models, developer-portal URLs, request-access forms, field
mappings, or auth scopes. Those are §1b custody-gated specifics — they appear only after
participation points 1 and 2 are decided, and only for the sources that decision
selects.

The prior turn's 18-row ranked API table is retracted from the working canon and is
logged as defect **F-2026-08-24-01** in the SIN register. It may re-enter as a working
document once §1b's three-question gate can be answered for each row: whose data does
it touch, which participation point does it serve, which custody boundary does it
cross.

---

© 2026 EVEglyphDesign. All rights reserved. Controlled copy.
*Pour le bien-être du peuple.*
