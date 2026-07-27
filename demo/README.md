# demo/ — Hawkins Twin Sample-Data Sandbox

Live surface: [Sample-Data Sandbox](https://eveglyphdesign.github.io/hawkins-twin-platform/demo/)

This is the answer to Luke Weatherbie's second question — *"Can we see a demo using
sample/test data, not our live systems?"* — with a public, zero-login, zero-credential
surface.

## What it is

A working demonstration of the inventory twin's mechanism running on **100% synthetic
data** across nine notional Atlantic-Canada centres:

- **KPI roll-up** — parts value on hand, fill rate (twin vs. a modelled lead-time-blind
  static reorder point), inventory turns, stockouts, overstock and aged stock, unit floor
  plan, transfers proposed and avoidable cost.
- **Nine centre cards** — click one to scope every table to it. Hanwell is marked as the
  pilot centre, matching `inventory-twin-spec.md` §6.
- **Transfer recommendations** — each row pairs a genuine shortage at one centre with
  genuine surplus at another for the same part number, with a confidence bar and a
  modelled avoided cost. Approve or decline individually, or approve all critical lines.
- **Parts inventory twin** — one row per part number per centre, showing `static_rop`
  beside `twin_rop` so the divergence is visible.
- **Vehicle / VIN inventory twin** — VIN-level model with aging and floor-plan visibility.
- **Governed path and audit trail** — the write-back flow, a drafted posting envelope on
  every approval, and an append-only audit trail with reconciliation state. The envelope
  is displayed, never sent. Direct database writes are denied by design.
- **Method** — what the demo proves, what it does not, how the data was made, and the
  three research questions the sandbox sets up.

## What it is not

It is not a measurement of Hawkins' business. Real fill rate, turns, and aged stock are
unknowable until the twin reads real data from one centre. This demonstrates **mechanism**,
not outcome.

## Provenance

| File | Role |
|---|---|
| [`generate_sample_data.py`](./generate_sample_data.py) | Seeded generator (seed `20260727`). Re-run it and you get exactly this dataset. |
| `sample_data.json` | The generated dataset consumed by the page. |
| `index.html` | The demo surface. No build step, no dependencies, no backend. |

No Hawkins Truck Mart, Peterbilt Atlantic, PACCAR, BRP, or CDK Global data was used.
No live system was accessed. No customer records exist in this dataset. Part
descriptions are generic heavy-truck parts nomenclature; VINs are random 17-character
strings that decode to nothing; place names are Atlantic-Canada plausible but the
inventory, values, and demand behind them are invented.

## Model notes

- Static ROP = `demand × 0.9`, ignoring lead time — the incumbent behaviour.
- Twin ROP = `demand × (lead_days ÷ 30) × safety factor`, plus a floor for critical lines.
- Months of supply on hand is drawn from a mixed distribution (thin / tight / healthy /
  heavy); risk state is derived from it, never assigned directly.
- The static-vs-twin fill-rate gap is **modelled**, and labelled as such on the surface.

## See also

- [Outline, functional map, and next steps (PDF)](../outline/EVEglyphDesign_Hawkins_Twin_Outline_Functional_Map.pdf)
- [`platform/REASONING-LAYER.md`](../platform/REASONING-LAYER.md) — the single stack this retargets
- `eve-hawkins-truck-mart` → `commercial/inventory-twin-spec.md` (private lane) — the spec this implements

---

© 2026 EVEglyphDesign. All rights reserved. Controlled copy.
*Pour le bien-être du peuple.*
