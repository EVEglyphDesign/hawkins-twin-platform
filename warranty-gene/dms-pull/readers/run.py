#!/usr/bin/env python3
"""
Warranty GENE — DMS pull entry point.

Reads Luke's DMS credentials from an age-decrypted JSON file, drives a
headless Chromium session as Luke against CDK Drive or Lightspeed EVO,
extracts what is visible for the requested VIN, writes a provenance-stamped
JSON to warranty-gene/dms-pull/pulls/.

This is a WIREFRAME. The reader modules (cdk.py, lightspeed.py) contain
best-effort selectors based on public documentation of the login flows,
but the exact click paths are only knowable once Luke authenticates once
and we see what he sees. Every reader captures screenshots on the way
through so we can iterate on the selectors without another authentication.

Usage:
  python run.py --side cdk --vin 1XPBSYN00... --creds /tmp/credentials.json --out ./pulls/
"""

import argparse
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

# Reader dispatch
import cdk
import brp
import lightspeed

READERS = {
    "cdk": cdk.pull,
    "brp": brp.pull,
    "lightspeed": lightspeed.pull,
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--side", required=True, choices=list(READERS))
    ap.add_argument("--vin", required=True)
    ap.add_argument("--creds", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--headed", action="store_true")
    args = ap.parse_args()

    creds = json.loads(args.creds.read_text())
    creds_for_side = creds[args.side]

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    args.out.mkdir(parents=True, exist_ok=True)
    out_json = args.out / f"{args.side}-{args.vin}-{ts}.json"
    trace_dir = Path(__file__).parent / "trace"
    trace_dir.mkdir(exist_ok=True)

    result = {
        "schema": "warranty-gene/dms-pull/v1",
        "pulled_at": datetime.now(timezone.utc).isoformat(),
        "side": args.side,
        "vin": args.vin,
        "reader_version": "0.1-wireframe",
        "success": False,
        "screens": [],
        "extracted": {},
        "error": None,
    }

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not args.headed)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/128.0 Safari/537.36",
        )
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()

        try:
            reader = READERS[args.side]
            extracted, screens = reader(page, creds_for_side, args.vin, trace_dir)
            result["extracted"] = extracted
            result["screens"] = screens
            result["success"] = True
        except Exception as e:
            result["error"] = {
                "type": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc(),
            }
            # Save a final screenshot for debugging.
            try:
                shot = trace_dir / f"error-{args.side}-{ts}.png"
                page.screenshot(path=str(shot), full_page=True)
                result["screens"].append(str(shot.relative_to(Path.cwd())))
            except Exception:
                pass
        finally:
            trace_path = trace_dir / f"{args.side}-{args.vin}-{ts}.zip"
            try:
                context.tracing.stop(path=str(trace_path))
                result["trace"] = str(trace_path.relative_to(Path.cwd()))
            except Exception:
                pass
            browser.close()

    out_json.write_text(json.dumps(result, indent=2, default=str))
    print(f"Wrote {out_json}")
    print(f"Success: {result['success']}")
    if not result["success"]:
        print(f"Error: {result['error']['type']}: {result['error']['message']}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
