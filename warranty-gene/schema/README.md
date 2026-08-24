# Warranty GENE — VIN Rich-Target Schema (v1)

The row that answers, per VIN, per day, whether the truck belongs on Tim's
booking calendar this week.

## What this schema is

A single JSON row per VIN, produced daily by the twin, consumed by two surfaces:

- **The executive control surface** — the fourth cohort tile beside the three existing TELUS-style tiles, ordered by `score.total` descending.
- **The outbound-booking worklist** — filtered to `compliance.clean == true` and `booking_urgency ∈ {inbound-tonight, inbound-this-week, in-region}`, handed to the counter for outreach.

Any row failing `compliance.clean` routes to the **review lane** instead of
the booking lane. A human decides what to do with it.

## What this schema is not

- Not a claim submission payload. PRWS remains authoritative; the GENE flags
  candidates, humans file claims.
- Not a copy of customer data. `owner.customer_id` is the CDK master id only;
  the payload — names, phones, VIN histories — stays in Hawkins-owned Azure
  Postgres.
- Not a source of coverage truth. SIR and SmartLINQ Service Management remain
  the eligibility source of record; the GENE reads them and encodes what it
  reads with `source_provenance` intact.

## Files

- `rich-target.schema.json` — JSON Schema Draft 2020-12
- `../samples/rich-targets.sample.json` — 7 synthetic VINs across Class 8
  diesel, Class 8 MX, Class 6/7, and battery electric
- `../samples/rich-targets.worklist.json` — compact projection for the
  fourth-cohort tile
- `../scoring.md` — deterministic 0–100 score formula
- `../scripts/build_samples.py` — reproduces the samples deterministically
- `../scripts/validate.py` — validates every sample against the schema

## The row at a glance

```
record_id           sha1(vin + as_of_date)          idempotent per day
vin                 17-char PACCAR-validated
as_of               ISO-8601 UTC

chassis             { model, class, series[], in_service_date, vocational_use }
usage               { odometer_km, engine_hours?, as_of, source }
owner               { customer_id, customer_type, fleet_id?, home_rooftop }

coverage            { <ten buckets> } — only applicable ones present
                     each: applies, months_remaining, distance_remaining_km,
                           hours_remaining?, expiry_reason

open_jobs[]         { job_id, authority, type, component, ata_code?,
                      coverage_bucket, estimated_srt_hours, parts_on_hand?,
                      customer_pay_at_risk_cad?, status, source_bulletin_url? }

score               { margin_estimate_cad, time_to_expiry_days,
                      booking_urgency, total }

compliance          { clean, flags{5 booleans} }

telemetry?          { last_ping, in_hawkins_region,
                      projected_overnight_region, geofence_confidence }

source_provenance[] { source, captured_at, note? }
```

## Coverage buckets

Modelled directly against the 2025.4 Warranty Quick Reference Guide,
Coverage Time & Exclusions table:

| Key                            | Applies to                                    |
| ------------------------------ | --------------------------------------------- |
| `base_emissions_carb`          | CARB-registered chassis                       |
| `base_emissions_epa_eccc`      | EPA/ECCC-registered chassis                   |
| `standard_vehicle`             | All chassis                                   |
| `standard_mx_engine`           | MX-equipped Class 8                           |
| `engine_major_components`      | MX-equipped Class 8                           |
| `vehicle_major_components`     | All chassis (definition varies by class)      |
| `severe_service`               | Chassis in a defined severe-service vocation  |
| `paccar_alternator_starter`    | Chassis with PACCAR-branded charging set      |
| `paccar_front_axles`           | Chassis with PACCAR-branded front axle        |
| `non_paccar_front_axles`       | Chassis with non-PACCAR front axle            |
| `bev_ess`                      | Battery-electric chassis (energy storage)     |

Buckets that do not apply to a given chassis are simply omitted from the row.

## Authority hierarchy for open jobs

Ordered from highest authority to lowest, matching the Warranty Procedure
Manual v2026.7:

1. `Federal Safety Recall`
2. `Field Repair Campaign`
3. `MX Component Emissions`
4. `Government Agency Mandated`
5. `Retrofit`
6. `Prognostic`
7. `Fix-as-Fail`
8. `Information Only`
9. `Live Fault Code`
10. `Extended Service Agreement`

A `Live Fault Code` becomes an open job only when the ATA component it names
maps to a warrantable component. Every other authority is emitted directly
from the SIR / SmartLINQ Service Management surface.

## Sample fixture — what each VIN demonstrates

| VIN suffix | Chassis                     | Demonstrates                                                     |
| ---------- | --------------------------- | ---------------------------------------------------------------- |
| `…0101`    | 579 MX, line haul           | Campaign + prognostic stacking, inbound-tonight                  |
| `…0202`    | 579 MX, regional haul       | Federal Safety Recall alone, inbound-this-week                   |
| `…0303`    | 567 severe service (logger) | MX VGT job routes to **review lane** on missing Prior Approval   |
| `…0404`    | 579 MX, line haul, aged     | Ineffective-repeat flag routes to **review lane**, out-of-region |
| `…0505`    | 537 Class 6/7               | Class 6/7 recall path, inbound-tonight                           |
| `…0606`    | 220EV battery electric      | BEV ESS campaign, `bev_ess` bucket                               |
| `…0707`    | 579 MX, regional            | Info-only bulletin scores 3.0 — no false urgency manufactured    |

## Validating a row

```bash
cd warranty-gene
python3 scripts/validate.py
```

Expected output: one line per row, all `OK`, all valid.

## Rebuilding the samples

```bash
cd warranty-gene
python3 scripts/build_samples.py
```

Deterministic. The same VIN + `as_of` date always produces the same row id.

## Landing

- Public: `warranty-gene/schema/` under the Hawkins Twin Platform.
- Private: rich-target worklists remain in Hawkins-owned Azure Postgres.

*Pour le bien-être du peuple.*
