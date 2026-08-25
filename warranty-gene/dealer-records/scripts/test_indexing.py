#!/usr/bin/env python3
"""Round-trip test: every primary VIN appears in every index it should.

For every VIN record on disk:
  - It appears in by-model.json under its chassis.model
  - It appears in by-engine-series.json under each of its chassis.series
  - It appears in by-in-service-month.json under its in-service YYYY-MM
  - For every open_job it has, the {vin, job_id} pair appears in
    open-jobs.json under the correct coverage_bucket
  - For every coverage bucket, it appears under the correct expiry tier in
    by-coverage-expiry.json

Red exit on any missing link. This is the guarantee the indexes are not lying.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
BASE = ROOT / "warranty-gene/dealer-records"
IDX = BASE / "indexes"

indexes = {p.name: json.loads(p.read_text()) for p in IDX.glob("*.json")}


def coverage_tier(bucket_data):
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


def has_vin_in(index_name, key_path, vin):
    node = indexes[index_name]
    for k in key_path:
        if not isinstance(node, dict) or k not in node:
            return False
        node = node[k]
    if not isinstance(node, list):
        return False
    return any(
        (e == vin) or (isinstance(e, dict) and e.get("vin") == vin)
        for e in node
    )


errors = 0
checked = 0
for f in sorted((BASE / "peterbilt-atlantic").glob("*/vins/*.json")):
    r = json.loads(f.read_text())
    vin = r["vin"]
    checked += 1
    chassis = r.get("chassis", {}) or {}

    if chassis.get("model") and not has_vin_in("by-model.json", [chassis["model"]], vin):
        errors += 1
        print(f"FAIL {vin} missing from by-model[{chassis['model']}]")

    for series in chassis.get("series", []) or []:
        if not has_vin_in("by-engine-series.json", [series], vin):
            errors += 1
            print(f"FAIL {vin} missing from by-engine-series[{series}]")

    in_service = (chassis.get("in_service_date") or "")[:7]
    if in_service and not has_vin_in("by-in-service-month.json", [in_service], vin):
        errors += 1
        print(f"FAIL {vin} missing from by-in-service-month[{in_service}]")

    for bucket, data in (r.get("coverage") or {}).items():
        tier = coverage_tier(data)
        if not has_vin_in("by-coverage-expiry.json", [bucket, tier], vin):
            errors += 1
            print(f"FAIL {vin} missing from by-coverage-expiry[{bucket}][{tier}]")

    for job in r.get("open_jobs", []) or []:
        bucket = job.get("coverage_bucket", "unassigned")
        entries = indexes.get("open-jobs.json", {}).get(bucket, [])
        if not any(
            e.get("vin") == vin and e.get("job_id") == job.get("job_id")
            for e in entries
        ):
            errors += 1
            print(f"FAIL {vin} job {job.get('job_id')} missing from open-jobs[{bucket}]")

print(f"\nchecked {checked} records against {len(indexes)} indexes, "
      f"{errors} error{'s' if errors != 1 else ''}")
sys.exit(1 if errors else 0)
