# Hawkins Twin Platform — Peterbilt Digital Twin

A digital-twin dashboard for a nine-centre Peterbilt Atlantic fleet. It visualizes
real-time telemetry, health/performance metrics, and predictive-maintenance alerts in a
sortable, interactive interface — then flows each predicted fault straight into the SAP
parts inventory and an **overnight betterment** outreach layer that turns idle off-hours
bay capacity into recovered value.

> **Stage · Wireframe.** Built with EVE, an advanced R&D tool, to wireframe this repository
> on representative data that mirrors the real SmartLINQ, PACCAR Solutions, FleetRight, and
> SAP parts shapes. Optimization comes later, after the live systems are connected.

## The canon-faithful flow

```
Physical asset → Sensor map → Live telemetry → Predictive alert → Linked SAP part → Overnight betterment offer
```

## Sections

| Section | What it shows |
| --- | --- |
| **Fleet Overview** | KPIs (units twinned, active, composite health, critical alerts, downtime saved) + per-unit health chart. |
| **Live Telemetry** | Sortable, searchable snapshot per unit — speed, coolant, oil, DEF, brake wear, alerts. |
| **Predictive Alerts** | Faults predicted from telemetry, each linked to the exact SAP part and network stock, with a one-click *Draft overnight repair offer*. |
| **Sensor → Digital Model Mapping** | How each physical sensor channel (SmartLINQ / PACCAR Solutions / FleetRight, J1939 SPN) binds to a node in the digital twin. |
| **Parts Inventory · SAP Twin** | Dealer-owned MARA/MARC/MARD mirror across the nine centres (PA01–PA09), with V/E/D + F/S/N classes, stock, reorder, lead time, price. |
| **Overnight Betterment** | Off-hours repair offers: draft + one-click send stub (simulated, no message leaves the twin), with uptime and bay-utilization gains. |
| **Fork · Host · Fund** | Governance and handover under EVE Glyph Design canon. |

## Fork · Host · Fund

- **Fork** — Tim receives a full, MIT-forkable copy of this twin to commercialize and operate; ARK footer preserved.
- **Host** — Self-hostable with a documented escape path. No vendor lock-in; runs without EVE, PACCAR-cloud, or any single vendor as a hard dependency. Inheritor-operable.
- **Fund** — Putting the physical sites to work in off-hours turns idle overnight capacity into betterment revenue — the commercial engine that funds EVE Glyph Design R&D.

**Operations:** Luke serves as technical observer and understands how to manage every
component (access provisioning, maintenance windows, system health). The team runs 24/7, so
operational support is never far away during and after handover.

## Canon principles this twin obeys

1. **Public stays public** — the twin is a lens over data already coming off the trucks, not a vault.
2. **Tokenized history is canonical** — every commit is a time-stamped, tamper-evident record in the GitHub Merkle ledger.
3. **Cryptographic notarization under the copyright umbrella** — the ARK footer is the only visible watermark.
4. **No vendor lock-in / inheritor-operable** — portable JSON via `/api/*`, open Markdown + TypeScript source, runbooks in the repo.
5. **Operator is Apex** — Dany Theriault defines the canon; Tim hosts and commercializes; the Pacific Utilities Design Council stewards institutional rights.

*Pour le bien-être du peuple.*

## Stack

Express + Vite + React + Tailwind CSS + shadcn/ui + Drizzle ORM (SQLite), Recharts.

```bash
npm install
npm run dev      # dev server (Express + Vite) on port 5000
npm run build    # production build → dist/
```

### API (portable JSON — the escape path)

`GET /api/fleet` · `/telemetry` · `/sensor-map` · `/parts` · `/alerts` · `/offers` · `/canon`
`POST /api/offers` (draft) · `PATCH /api/offers/:id` (state: draft | sent | accepted | declined)

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all
rights reserved. Stewardship of rights of use and assignment for large public and
institutional usage rests with the Pacific Utilities Design Council. Published as a
time-stamped record of authorship and intent.
