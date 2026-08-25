#!/usr/bin/env python3
"""Validate every VIN record under dealer-records/ against the canon schema.

Rules:
  1. Every *.json file under peterbilt-atlantic/*/vins/ must parse.
  2. Filename stem must exactly equal the record's `vin` field (VIN is the
     equipment record base code — this is canon rule EgD-WGB-002).
  3. Every record must validate against warranty-gene/schema/rich-target.schema.json
     if the schema imposes constraints; if the schema is permissive (empty),
     we still enforce that the top-level `vin`, `as_of`, `chassis`, and
     `coverage` keys are present.

Red exit on any failure.
"""
import json
import sys
import pathlib

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.stderr.write("install jsonschema first: pip install jsonschema\n")
    sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parents[3]
SCHEMA_PATH = ROOT / "warranty-gene/schema/rich-target.schema.json"
BASE = ROOT / "warranty-gene/dealer-records/peterbilt-atlantic"
REQUIRED_TOP = {"vin", "as_of", "chassis", "coverage"}

schema = json.loads(SCHEMA_PATH.read_text())
validator = Draft202012Validator(schema)

records = sorted(BASE.glob("*/vins/*.json"))
errors = 0

for f in records:
    rel = f.relative_to(ROOT)
    try:
        rec = json.loads(f.read_text())
    except json.JSONDecodeError as e:
        errors += 1
        print(f"FAIL {rel}: not valid JSON — {e}")
        continue

    # Rule 2: filename is the VIN
    vin = rec.get("vin")
    if not vin:
        errors += 1
        print(f"FAIL {rel}: record has no top-level 'vin' field")
    elif f.stem != vin:
        errors += 1
        print(f"FAIL {rel}: filename '{f.stem}' does not match record vin '{vin}'")

    # Rule 3a: required top-level keys
    missing = REQUIRED_TOP - set(rec.keys())
    if missing:
        errors += 1
        print(f"FAIL {rel}: missing top-level keys: {sorted(missing)}")

    # Rule 3b: JSON Schema (only reports if schema actually constrains)
    for e in validator.iter_errors(rec):
        errors += 1
        loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
        print(f"FAIL {rel}: schema violation at {loc} — {e.message}")

print(f"\nchecked {len(records)} records, {errors} error{'s' if errors != 1 else ''}")
sys.exit(1 if errors else 0)
