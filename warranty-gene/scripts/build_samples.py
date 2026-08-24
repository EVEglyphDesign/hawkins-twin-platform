"""Generate a deterministic set of Warranty GENE rich-target sample rows.

Every VIN in this file is a synthetic construct. Real dealer data does not move
until Tim's agreement is executed and Luke receives 20-Group access; these rows
exist only to exercise the schema, the scoring formula, and the executive
control surface (fourth cohort). The Peterbilt-owned service account, not any
personal credential, remains the identity for real ingestion.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone, date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SAMPLES = HERE / "samples"
SAMPLES.mkdir(exist_ok=True)

AS_OF = datetime(2026, 8, 24, 12, 0, 0, tzinfo=timezone.utc)
AS_OF_DATE = AS_OF.date()
AS_OF_ISO = AS_OF.isoformat()

# Synthetic VINs — WMI 1XPB reserved to Peterbilt but the remaining digits are
# arbitrary and do not correspond to any real production truck.
SYNTHETIC = [
    # (vin, model, klass, series, in_service, vocational, odo_km, hours, rooftop, cust_type, fleet_id, telemetry)
    ("1XPBSYN00N1000101", "579", "Class 8", ["Diesel", "MX-Equipped"],
     "2023-04-12", "Line Haul", 412_000, 4_800, "PA-MONCTON", "Small Fleet", None,
     dict(in_region=True, projected="Hawkins-NB", confidence=0.92)),

    ("1XPBSYN00P1000202", "579", "Class 8", ["Diesel", "MX-Equipped"],
     "2024-11-02", "Regional Haul", 118_000, 1_450, "PA-FREDERICTON", "Owner-Operator", None,
     dict(in_region=False, projected="Hawkins-NB", confidence=0.71)),

    ("1XPBSYN00M1000303", "567", "Class 8", ["Diesel", "Severe Service"],
     "2022-06-18", "Logger", 258_000, 3_600, "PA-BATHURST", "DSFW Fleet", "FLEET-ATLANTIC-LOG-002",
     dict(in_region=True, projected="Adjacent-QC", confidence=0.55)),

    ("1XPBSYN00L1000404", "579", "Class 8", ["Diesel", "MX-Equipped"],
     "2021-03-08", "Line Haul", 705_000, 8_100, "PA-SAINT-JOHN", "Direct Fleet", "FLEET-DIRECT-088",
     dict(in_region=False, projected="Out-of-region", confidence=0.88)),

    ("1XPBSYN00R1000505", "537", "Class 6/7", ["Diesel"],
     "2025-01-22", "Pickup Delivery", 42_000, 620, "PA-DIEPPE", "Owner-Operator", None,
     dict(in_region=True, projected="Hawkins-NB", confidence=0.94)),

    ("1XPBSYN00P1000606", "220EV", "Class 6/7", ["Battery Electric"],
     "2024-09-14", "Pickup Delivery", 27_500, None, "PA-MONCTON", "Small Fleet", None,
     dict(in_region=True, projected="Hawkins-NB", confidence=0.90)),

    ("1XPBSYN00N1000707", "579", "Class 8", ["Diesel", "MX-Equipped"],
     "2023-08-30", "Regional Haul", 385_000, 4_200, "PA-EDMUNDSTON", "Small Fleet", None,
     dict(in_region=False, projected="Unknown", confidence=0.10)),
]


# ---------- Coverage math ----------
# Source: 2025.4 Warranty Quick Reference Guide, Coverage Time & Exclusions table.
# Miles converted at the published km values in the source table.
BUCKETS_CLASS_8 = {
    "base_emissions_carb":       dict(months=60, km=None,       hours=None, unlimited_dist=False),
    "base_emissions_epa_eccc":   dict(months=60, km=160_000,    hours=None),
    "standard_vehicle":          dict(months=12, km=160_000,    hours=None),
    "standard_mx_engine":        dict(months=24, km=400_000,    hours=6_250),
    "engine_major_components":   dict(months=60, km=800_000,    hours=12_500),
    "vehicle_major_components":  dict(months=36, km=480_000,    hours=None),
    "severe_service":            dict(months=12, km=80_000,     hours=None),
    "paccar_alternator_starter": dict(months=36, km=560_000,    hours=None),
    "paccar_front_axles":        dict(months=60, km=1_200_000,  hours=None),
    "non_paccar_front_axles":    dict(months=36, km=480_000,    hours=None),
}
BUCKETS_CLASS_67 = {
    "base_emissions_carb":       dict(months=60, km=None,      hours=None),
    "base_emissions_epa_eccc":   dict(months=60, km=160_000,   hours=None),
    "standard_vehicle":          dict(months=12, km=None,      hours=None),  # Unlimited km
    "vehicle_major_components":  dict(months=24, km=None,      hours=None),  # Unlimited km
    "severe_service":            dict(months=12, km=80_000,    hours=None),
    "paccar_front_axles":        dict(months=60, km=1_200_000, hours=None),
    "non_paccar_front_axles":    dict(months=48, km=None,      hours=None),
}
BUCKETS_BEV_MEDIUM = {
    "standard_vehicle":         dict(months=12, km=None,      hours=None),
    "vehicle_major_components": dict(months=24, km=None,      hours=None),
    "bev_ess":                  dict(months=72, km=200_000,   hours=None),  # or 80% charge floor
}


def months_between(a: date, b: date) -> int:
    return (b.year - a.year) * 12 + (b.month - a.month)


def bucket_remaining(spec: dict, in_service: date, odo_km: int, hours: int | None) -> dict:
    used_months = months_between(in_service, AS_OF_DATE)
    months_rem: int | None
    if spec["months"] is None:
        months_rem = None
    else:
        months_rem = max(0, spec["months"] - used_months)

    dist_rem: int | None
    if spec.get("km") is None:
        dist_rem = None
    else:
        dist_rem = max(0, spec["km"] - odo_km)

    hours_rem: int | None
    if spec.get("hours") is None or hours is None:
        hours_rem = None
    else:
        hours_rem = max(0, spec["hours"] - hours)

    # Which limit binds?
    candidates: list[tuple[int, str]] = []
    if months_rem is not None:
        candidates.append((months_rem * 30, "months"))
    if dist_rem is not None:
        # Assume 500 km/day average for the binding comparison
        candidates.append((dist_rem // 500, "distance"))
    if hours_rem is not None:
        # Assume 10 hr/day of engine time
        candidates.append((hours_rem // 10, "hours"))
    if not candidates:
        reason = "unlimited"
    else:
        reason = min(candidates, key=lambda x: x[0])[1]

    return dict(
        applies=True,
        months_remaining=months_rem,
        distance_remaining_km=dist_rem,
        hours_remaining=hours_rem,
        expiry_reason=reason,
    )


def build_coverage(klass: str, series: list[str], model: str,
                   in_service: date, odo_km: int, hours: int | None) -> dict:
    """Emit only the buckets that apply to this chassis."""
    if "Battery Electric" in series:
        applicable = BUCKETS_BEV_MEDIUM
    elif klass == "Class 8":
        applicable = dict(BUCKETS_CLASS_8)
        if "MX-Equipped" not in series:
            applicable.pop("standard_mx_engine", None)
            applicable.pop("engine_major_components", None)
        if "Severe Service" not in series:
            # Severe service still applies but distance cap ties to it — keep it
            pass
    else:  # Class 6/7 diesel
        applicable = BUCKETS_CLASS_67

    return {k: bucket_remaining(v, in_service, odo_km, hours) for k, v in applicable.items()}


# ---------- Open jobs (deterministic per VIN) ----------
OPEN_JOBS_BY_VIN = {
    "1XPBSYN00N1000101": [
        dict(
            job_id="E312-2025",
            authority="Field Repair Campaign",
            type="Aftertreatment",
            component="Diesel Exhaust Fluid (DEF) Dosing Valve [Injector]",
            ata_code="SPN-4334",
            coverage_bucket="base_emissions_epa_eccc",
            estimated_srt_hours=1.6,
            parts_on_hand=True,
            customer_pay_at_risk_cad=1_450.00,
            status="Open",
            source_bulletin_url="https://paccar.example/bulletins/E312-2025",
        ),
        dict(
            job_id="PROG-EGR-COOLER-018",
            authority="Prognostic",
            type="Powertrain",
            component="EGR Cooler Coolant Return Tube O-Ring Seals",
            ata_code=None,
            coverage_bucket="standard_mx_engine",
            estimated_srt_hours=3.2,
            parts_on_hand=False,
            customer_pay_at_risk_cad=2_180.00,
            status="Open",
            source_bulletin_url="https://paccar.example/prognostics/EGR-018",
        ),
    ],
    "1XPBSYN00P1000202": [
        dict(
            job_id="R2026-014",
            authority="Federal Safety Recall",
            type="Safety",
            component="Brake Pedal Position Switch",
            ata_code="SPN-91",
            coverage_bucket="standard_vehicle",
            estimated_srt_hours=0.9,
            parts_on_hand=True,
            customer_pay_at_risk_cad=0.00,
            status="Open",
            source_bulletin_url="https://paccar.example/recalls/R2026-014",
        ),
    ],
    "1XPBSYN00M1000303": [
        dict(
            job_id="FLT-1569C",
            authority="Live Fault Code",
            type="Powertrain",
            component="Turbocharger — Variable Geometry (VGT) Assembly",
            ata_code="1569.C",
            coverage_bucket="standard_mx_engine",
            estimated_srt_hours=4.8,
            parts_on_hand=False,
            customer_pay_at_risk_cad=6_400.00,
            status="Open",
            source_bulletin_url=None,
        ),
        dict(
            job_id="ESA-9485634-CORE",
            authority="Extended Service Agreement",
            type="Powertrain",
            component="MX-13 Major Component Coverage — 7/700 ESA",
            ata_code=None,
            coverage_bucket="engine_major_components",
            estimated_srt_hours=0.0,
            parts_on_hand=True,
            customer_pay_at_risk_cad=0.00,
            status="Open",
            source_bulletin_url="https://paccar.example/esa/9485634",
        ),
    ],
    "1XPBSYN00L1000404": [
        # Out-of-window powertrain — the row should route to review lane, not booking
        dict(
            job_id="FLT-3251E",
            authority="Live Fault Code",
            type="Aftertreatment",
            component="Diesel Particulate Filter (DPF) Differential Pressure Sensor",
            ata_code="3251.E",
            coverage_bucket="base_emissions_epa_eccc",
            estimated_srt_hours=1.2,
            parts_on_hand=True,
            customer_pay_at_risk_cad=780.00,
            status="Open",
            source_bulletin_url=None,
        ),
    ],
    "1XPBSYN00R1000505": [
        dict(
            job_id="R2026-021",
            authority="Federal Safety Recall",
            type="Electrical",
            component="Accelerator Pedal (Lever Position) Sensor",
            ata_code="SPN-91",
            coverage_bucket="standard_vehicle",
            estimated_srt_hours=0.8,
            parts_on_hand=True,
            customer_pay_at_risk_cad=0.00,
            status="Open",
            source_bulletin_url="https://paccar.example/recalls/R2026-021",
        ),
    ],
    "1XPBSYN00P1000606": [
        dict(
            job_id="BEV-CAMP-2026-04",
            authority="Field Repair Campaign",
            type="BEV Powertrain",
            component="High Voltage Battery Junction Box (S-Box)",
            ata_code=None,
            coverage_bucket="bev_ess",
            estimated_srt_hours=3.5,
            parts_on_hand=False,
            customer_pay_at_risk_cad=8_900.00,
            status="Open",
            source_bulletin_url="https://paccar.example/bev/CAMP-2026-04",
        ),
    ],
    "1XPBSYN00N1000707": [
        dict(
            job_id="INFO-SW-2026-11",
            authority="Information Only",
            type="Powertrain",
            component="Engine Control Module (ECM) Software",
            ata_code=None,
            coverage_bucket="none",
            estimated_srt_hours=0.6,
            parts_on_hand=True,
            customer_pay_at_risk_cad=0.00,
            status="Open",
            source_bulletin_url="https://paccar.example/info/SW-2026-11",
        ),
    ],
}

COMPLIANCE_BY_VIN = {
    # All clean except the out-of-window one (repeat/ineffective flagged after two prior claims)
    "1XPBSYN00L1000404": dict(
        missing_technician_id=False,
        rmi_undocumented=False,
        labor_time_unsupported=False,
        repeat_ineffective_repair=True,
        prior_approval_required_and_missing=False,
    ),
    "1XPBSYN00M1000303": dict(
        missing_technician_id=False,
        rmi_undocumented=False,
        labor_time_unsupported=False,
        repeat_ineffective_repair=False,
        # VGT replacement over the MX threshold requires Prior Approval
        prior_approval_required_and_missing=True,
    ),
}


def compliance_for(vin: str) -> dict:
    default = dict(
        missing_technician_id=False,
        rmi_undocumented=False,
        labor_time_unsupported=False,
        repeat_ineffective_repair=False,
        prior_approval_required_and_missing=False,
    )
    flags = COMPLIANCE_BY_VIN.get(vin, default)
    return dict(clean=not any(flags.values()), flags=flags)


# ---------- Scoring ----------
HAWKINS_LABOR_RATE_CAD = 168.00   # placeholder; real rate lives in dealer CDK
PARTS_MARKUP_MULTIPLIER = 1.30

def score_row(open_jobs: list[dict], coverage: dict, telemetry_in_region: bool,
              projected: str, chassis_class: str) -> dict:
    # Margin: only jobs with a covering bucket count. Zero-hour jobs (ESA
    # coverage confirmation) do not book margin. Cap SRT at the published table.
    labor_cad = sum(j["estimated_srt_hours"] * HAWKINS_LABOR_RATE_CAD
                    for j in open_jobs if j["coverage_bucket"] != "none")
    # Parts assumed at 0.6x labor for warranty-covered work; markup counted only
    # on jobs whose parts were flagged not on hand (ordered fresh, higher margin
    # capture) — this is a heuristic, not a claim number.
    parts_cad = sum(j["estimated_srt_hours"] * HAWKINS_LABOR_RATE_CAD * 0.6
                    * (PARTS_MARKUP_MULTIPLIER if not j.get("parts_on_hand", True) else 1.0)
                    for j in open_jobs if j["coverage_bucket"] != "none")
    margin = round(labor_cad + parts_cad, 2)

    # Time to expiry — min across covering buckets used by open jobs
    days_candidates: list[int] = []
    for j in open_jobs:
        b = j["coverage_bucket"]
        if b == "none":
            continue
        bucket = coverage.get(b)
        if not bucket:
            continue
        m = bucket.get("months_remaining")
        d = bucket.get("distance_remaining_km")
        if m is not None:
            days_candidates.append(m * 30)
        if d is not None:
            days_candidates.append(d // 500)
    tte = min(days_candidates) if days_candidates else 9999

    # Booking urgency
    if telemetry_in_region and projected == "Hawkins-NB":
        urgency = "inbound-tonight"
    elif projected == "Hawkins-NB":
        urgency = "inbound-this-week"
    elif telemetry_in_region:
        urgency = "in-region"
    else:
        urgency = "out-of-region"

    # Composite: 0-100, deterministic
    #   margin_component     0-50   (saturates at $10k)
    #   urgency_component    0-30   (inbound-tonight=30, this-week=22, in-region=15, out=0)
    #   expiry_component     0-20   (≤90d=20, ≤180d=14, ≤365d=8, else 3)
    margin_c = min(50.0, (margin / 10_000.0) * 50.0)
    urgency_c = {"inbound-tonight": 30, "inbound-this-week": 22,
                 "in-region": 15, "out-of-region": 0}[urgency]
    if tte <= 90:      expiry_c = 20
    elif tte <= 180:   expiry_c = 14
    elif tte <= 365:   expiry_c = 8
    else:              expiry_c = 3
    total = round(margin_c + urgency_c + expiry_c, 1)

    return dict(
        margin_estimate_cad=margin,
        time_to_expiry_days=tte,
        booking_urgency=urgency,
        total=total,
    )


# ---------- Assembly ----------
def record_id(vin: str) -> str:
    return hashlib.sha1(f"{vin}|{AS_OF_DATE.isoformat()}".encode()).hexdigest()


rows: list[dict] = []
for (vin, model, klass, series, in_service, vocational, odo_km, hours,
     rooftop, cust_type, fleet_id, tele) in SYNTHETIC:
    in_service_date = date.fromisoformat(in_service)
    coverage = build_coverage(klass, series, model, in_service_date, odo_km, hours)
    open_jobs = OPEN_JOBS_BY_VIN[vin]
    compliance = compliance_for(vin)
    score = score_row(
        open_jobs, coverage,
        telemetry_in_region=tele["in_region"],
        projected=tele["projected"],
        chassis_class=klass,
    )

    row = dict(
        record_id=record_id(vin),
        vin=vin,
        as_of=AS_OF_ISO,
        chassis=dict(
            model=model,
            **{"class": klass},
            series=series,
            in_service_date=in_service,
            vocational_use=vocational,
        ),
        usage=dict(
            odometer_km=odo_km,
            **({"engine_hours": hours} if hours is not None else {}),
            as_of=AS_OF_ISO,
            source="SmartLINQ",
        ),
        owner=dict(
            customer_id=f"CDK-CUST-{vin[-6:]}",
            customer_type=cust_type,
            fleet_id=fleet_id,
            home_rooftop=rooftop,
        ),
        coverage=coverage,
        open_jobs=open_jobs,
        score=score,
        compliance=compliance,
        telemetry=dict(
            last_ping=AS_OF_ISO,
            in_hawkins_region=tele["in_region"],
            projected_overnight_region=tele["projected"],
            geofence_confidence=tele["confidence"],
        ),
        source_provenance=[
            dict(source="SIR",                                       captured_at=AS_OF_ISO),
            dict(source="SmartLINQ Service Management",              captured_at=AS_OF_ISO),
            dict(source="PACCAR Solutions Telematics",               captured_at=AS_OF_ISO),
            dict(source="Warranty Quick Reference Guide 2025.4",     captured_at=AS_OF_ISO,
                 note="Coverage buckets, months, and distance caps."),
            dict(source="CARB/EPA/ECCC Emission Component Coverage", captured_at=AS_OF_ISO,
                 note="Emissions-family tagging for aftertreatment jobs."),
            dict(source="Warranty Procedure Manual v2026.7",         captured_at=AS_OF_ISO,
                 note="Authority hierarchy, Prior Approval and audit rules."),
        ],
    )
    rows.append(row)


# Sort by score descending — the executive control surface's row order
rows.sort(key=lambda r: r["score"]["total"], reverse=True)

out = SAMPLES / "rich-targets.sample.json"
out.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
print(f"wrote {out}  rows={len(rows)}")

# Also emit a compact worklist view for the fourth cohort tile
worklist = [
    dict(
        vin=r["vin"],
        rooftop=r["owner"]["home_rooftop"],
        customer_type=r["owner"]["customer_type"],
        top_job=(r["open_jobs"][0]["component"] if r["open_jobs"] else None),
        authority=(r["open_jobs"][0]["authority"] if r["open_jobs"] else None),
        margin_estimate_cad=r["score"]["margin_estimate_cad"],
        time_to_expiry_days=r["score"]["time_to_expiry_days"],
        booking_urgency=r["score"]["booking_urgency"],
        score=r["score"]["total"],
        lane="review" if not r["compliance"]["clean"] else "booking",
    )
    for r in rows
]
worklist_out = SAMPLES / "rich-targets.worklist.json"
worklist_out.write_text(json.dumps(worklist, indent=2) + "\n", encoding="utf-8")
print(f"wrote {worklist_out}  rows={len(worklist)}")
