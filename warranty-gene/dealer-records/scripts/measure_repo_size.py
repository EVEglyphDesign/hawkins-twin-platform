#!/usr/bin/env python3
"""Measure current VIN record footprint and project growth.

Writes a Markdown report to stdout. Redirect to MEASURED-SIZE.md at the
dealer-records root.
"""
import pathlib
import statistics
import datetime

ROOT = pathlib.Path(__file__).resolve().parents[3]
BASE = ROOT / "warranty-gene/dealer-records/peterbilt-atlantic"

files = sorted(BASE.glob("*/vins/*.json"))
sizes = [f.stat().st_size for f in files]
n = len(sizes)
total = sum(sizes)
avg = (total / n) if n else 0
median = statistics.median(sizes) if n else 0
largest = max(sizes) if n else 0

# GitHub Pages soft cap: 1 GB
PAGES_CAP_BYTES = 1024 ** 3

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

print(f"# Warranty GENE — dealer-records size measurement")
print()
print(f"_As of {now} · from `scripts/measure_repo_size.py`._")
print()
print(f"## Current footprint")
print()
print(f"| Metric | Value |")
print(f"| --- | --- |")
print(f"| VIN records | **{n:,}** |")
print(f"| Total bytes | **{total:,}** ({total/1024:,.1f} KiB) |")
print(f"| Average bytes per record | **{avg:,.0f}** |")
print(f"| Median bytes per record | **{median:,.0f}** |")
print(f"| Largest record | **{largest:,}** bytes |")
print()
print(f"## Projected footprint")
print()
print(f"| VIN count | Projected size | Share of Pages 1 GB cap |")
print(f"| --- | --- | --- |")
for target in (500, 5_000, 25_000, 50_000):
    projected = target * avg
    share = 100 * projected / PAGES_CAP_BYTES
    print(f"| {target:,} | **{projected/1024/1024:,.1f} MB** | {share:,.1f}% |")
print()
print(f"Peterbilt Atlantic five-year projection: **~25,000 VINs**.")
print(f"At the current average record size, that lands at "
      f"**{25_000*avg/1024/1024:,.1f} MB** — comfortably inside the GitHub Pages 1 GB cap.")
