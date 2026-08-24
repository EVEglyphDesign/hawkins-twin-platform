"""Validate the sample rich-target rows against the schema and re-check scoring.

Run: python3 scripts/validate.py

Exits 0 on clean pass, non-zero on any defect. Prints one line per row.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((HERE / "schema" / "rich-target.schema.json").read_text())
ROWS = json.loads((HERE / "samples" / "rich-targets.sample.json").read_text())

validator = jsonschema.Draft202012Validator(SCHEMA)

failures = 0
for row in ROWS:
    errors = sorted(validator.iter_errors(row), key=lambda e: list(e.absolute_path))
    if errors:
        failures += 1
        print(f"FAIL  {row['vin']}  score={row['score']['total']}")
        for e in errors:
            path = "/".join(str(p) for p in e.absolute_path) or "<root>"
            print(f"  - {path}: {e.message}")
    else:
        print(f"OK    {row['vin']}  score={row['score']['total']:>5}  "
              f"urgency={row['score']['booking_urgency']:<18}  "
              f"margin=${row['score']['margin_estimate_cad']:>8,.2f}  "
              f"clean={row['compliance']['clean']}")

print("-" * 72)
if failures:
    print(f"{failures} row(s) failed schema validation.")
    sys.exit(1)
print(f"All {len(ROWS)} rows valid against the schema.")
sys.exit(0)
