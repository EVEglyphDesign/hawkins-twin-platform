#!/usr/bin/env python3
"""Rebuild the five indexes from the primary VIN records.

Indexes emitted under warranty-gene/dealer-records/indexes/ :

  by-model.json              — Peterbilt model (579, 567, 220EV, ...)      -> [vin]
  by-engine-series.json      — chassis.series entries (MX-Equipped, ...)   -> [vin]
  by-coverage-expiry.json    — bucket -> tier (expired / critical / soon /
                                healthy / n_a) -> [vin]
  by-in-service-month.json   — YYYY-MM                                     -> [vin]
  open-jobs.json             — coverage_bucket                             -> [{vin, job_id, ata_code, customer_pay_at_risk_cad}]

Every value is either a list of VINs or a list of objects whose primary key is `vin`.
Never a DMS record number, never a dealer-internal serial. This is canon rule EgD-WGB-002.
"""
import json
import pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[3]
BASE = ROOT / "warranty-gene/dealer-records"
IDX = BASE / "indexes"
IDX.mkdir(parents=True, exist_ok=True)


def coverage_tier(bucket_data):
    """Bucketise a coverage entry into expired / critical / soon / healthy / n_a."""
    if not bucket_data.get("applies"):
        return "n_a"
    m = bucket_data.get("months_remaining")
    if m is None:
        return "unknown"
    if m <= 0:
        return "expired"
    if m <= 3:
        return "critical"
    if m <= 12:
        return "soon"
    return "healthy"


by_model = defaultdict(list)
by_engine_series = defaultdict(list)
by_coverage_expiry = defaultdict(lambda: defaultdict(list))
by_in_service_month = defaultdict(list)
open_jobs = defaultdict(list)

record_count = 0
for f in sorted((BASE / "peterbilt-atlantic").glob("*/vins/*.json")):
    r = json.loads(f.read_text())
    vin = r["vin"]
    record_count += 1

    chassis = r.get("chassis", {}) or {}
    if chassis.get("model"):
        by_model[chassis["model"]].append(vin)
    for series in chassis.get("series", []) or []:
        by_engine_series[series].append(vin)

    in_service = (chassis.get("in_service_date") or "")[:7]
    if in_service:
        by_in_service_month[in_service].append(vin)

    coverage = r.get("coverage", {}) or {}
    for bucket, data in coverage.items():
        tier = coverage_tier(data)
        by_coverage_expiry[bucket][tier].append(vin)

    for job in r.get("open_jobs", []) or []:
        bucket = job.get("coverage_bucket", "unassigned")
        open_jobs[bucket].append({
            "vin": vin,
            "job_id": job.get("job_id"),
            "type": job.get("type"),
            "ata_code": job.get("ata_code"),
            "customer_pay_at_risk_cad": job.get("customer_pay_at_risk_cad"),
            "status": job.get("status"),
        })


def dump(name, data):
    # sort every value list for determinism (dicts sort by vin, plain by string)
    if isinstance(data, dict):
        for k, v in list(data.items()):
            if isinstance(v, list):
                if v and isinstance(v[0], dict):
                    data[k] = sorted(v, key=lambda d: d.get("vin", ""))
                else:
                    data[k] = sorted(v)
            elif isinstance(v, dict):
                for kk, vv in v.items():
                    v[kk] = sorted(vv)
    (IDX / name).write_text(json.dumps(data, indent=2, sort_keys=True))
    top_keys = len(data)
    print(f"wrote {name} — {top_keys} top-level keys")


dump("by-model.json", dict(by_model))
dump("by-engine-series.json", dict(by_engine_series))
dump("by-coverage-expiry.json", {k: dict(v) for k, v in by_coverage_expiry.items()})
dump("by-in-service-month.json", dict(by_in_service_month))
dump("open-jobs.json", dict(open_jobs))

print(f"\nindexed {record_count} record{'s' if record_count != 1 else ''}")
