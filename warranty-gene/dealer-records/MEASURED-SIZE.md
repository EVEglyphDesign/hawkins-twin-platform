# Warranty GENE — dealer-records size measurement

_As of 2026-08-25T00:25:31Z · from `scripts/measure_repo_size.py`._

## Current footprint

| Metric | Value |
| --- | --- |
| VIN records | **7** |
| Total bytes | **29,910** (29.2 KiB) |
| Average bytes per record | **4,273** |
| Median bytes per record | **4,457** |
| Largest record | **4,954** bytes |

## Projected footprint

| VIN count | Projected size | Share of Pages 1 GB cap |
| --- | --- | --- |
| 500 | **2.0 MB** | 0.2% |
| 5,000 | **20.4 MB** | 2.0% |
| 25,000 | **101.9 MB** | 9.9% |
| 50,000 | **203.7 MB** | 19.9% |

Peterbilt Atlantic five-year projection: **~25,000 VINs**.
At the current average record size, that lands at **101.9 MB** — comfortably inside the GitHub Pages 1 GB cap.
