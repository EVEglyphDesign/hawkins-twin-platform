# Synthetic composite data for the Hawkins mock ADA/ATD 20 Group dashboard.
# Every "Hawkins" figure below is INVENTED. Line names, formulas and guide values
# are taken from the public ATD 2026 Formulas / Definitions / Guides slide guide.
# Group average and best-in-class columns are notional and do not represent any
# real 20 Group's published composite.
#
# tuple = (name, formula, format, direction, guide, hawkins, group_avg, best_in_class, twin_live, src)
# format: pct | x | days | mo | usd | ratio | num      direction: 1 higher better, -1 lower better

DEPTS = [
  ("dealership", "Dealership", [
    ("Total absorption", "Used-truck, service, parts and body shop gross \u00f7 total dealership expense, ex. lease & rental", "pct", 1, 130, 126.4, 124.8, 141.2, 128.9, "twin"),
    ("Fixed absorption", "Service, parts and body shop gross \u00f7 total dealership expense, ex. lease & rental", "pct", 1, 115, 111.8, 110.6, 124.8, 113.2, "twin"),
    ("Net profit return on sales", "Total dealership net profit \u00f7 total dealership sales", "pct", 1, 4.0, 4.3, 3.6, 5.2, None, ""),
    ("Net profit return on gross", "Total dealership net profit \u00f7 total dealership gross profit", "pct", 1, 22.5, 23.8, 20.9, 27.4, None, ""),
    ("Net profit return on assets", "Annual profits \u00f7 total assets", "pct", 1, 21.0, 22.6, 19.2, 26.1, None, ""),
    ("Return on equity", "Annualised net profit before tax \u00f7 net worth", "pct", 1, 31.5, 33.4, 29.6, 38.0, None, ""),
    ("Asset utilization", "Annualised total dealership sales \u00f7 total assets", "x", 1, 6.5, 6.9, 6.6, 7.8, None, ""),
  ]),
  ("parts", "Parts", [
    ("Parts inventory months' supply", "Reconciled inventory \u00f7 average month cost of sales", "mo", -1, 1.5, 1.26, 1.62, 1.31, 1.26, "twin"),
    ("Parts inventory turnover", "Annual cost of sales \u00f7 average inventory", "x", 1, 7.0, 9.5, 6.8, 8.4, 9.5, "twin"),
    ("Parts fill rate \u2014 first time", "Lines filled from stock on first request \u00f7 lines requested", "pct", 1, 90.0, 86.7, 88.9, 93.1, 91.3, "twin"),
    ("Parts obsolescence (>12 months no-sale)", "Parts inventory aged over 12 months no-sale \u00f7 total inventory", "pct", -1, 3.0, 4.1, 3.4, 1.9, 4.1, "twin"),
    ("Parts gross % sales", "Parts gross profit \u00f7 parts sales", "pct", 1, 29.0, 29.6, 28.6, 31.8, None, ""),
    ("Parts sales per parts employee", "Monthly parts sales \u00f7 parts employees", "usd", 1, 70000, 72400, 69800, 81400, None, ""),
    ("Parts gross per parts employee", "Monthly parts gross \u00f7 parts employees", "usd", 1, 21000, 20100, 20400, 25100, None, ""),
    ("Customer RO parts-to-labor ratio", "Customer parts sales \u00f7 customer labor sales", "ratio", 1, 1.0, 0.86, 0.97, 1.12, None, ""),
  ]),
  ("service", "Service", [
    ("Technician proficiency", "Hours produced \u00f7 hours available", "pct", 1, 100.0, 94.6, 96.2, 103.5, None, ""),
    ("Technician productivity", "Hours worked \u00f7 hours available", "pct", 1, 88.0, 89.2, 86.9, 92.4, None, ""),
    ("Technician efficiency", "Hours sold \u00f7 hours worked", "pct", 1, 115.0, 117.4, 113.2, 122.7, None, ""),
    ("Hours per repair order", "Retail hours sold \u00f7 customer repair orders", "num", 1, 6.0, 5.2, 5.9, 7.1, None, ""),
    ("Gross per tech per month", "At a $100 door rate, 88% proficiency, 22 days", "usd", 1, 11400, 11740, 11150, 13420, None, ""),
    ("Stall utilization (one shift)", "Stall hours used \u00f7 stall hours available", "pct", 1, 80.0, 74.8, 78.4, 86.9, None, ""),
    ("Customer labor gross retention", "Customer labor gross \u00f7 customer labor sales", "pct", 1, 76.0, 76.9, 75.4, 79.2, None, ""),
    ("Warranty labor gross retention", "Warranty labor gross \u00f7 warranty labor sales", "pct", 1, 76.0, 71.2, 74.8, 78.6, None, ""),
    ("Open repair orders", "Mechanical or body ROs not yet invoiced, days after last time punch", "days", -1, 2.0, 4.3, 2.8, 1.4, 4.3, "twin"),
    ("Work in process", "Days of average technician labor cost held in WIP", "days", -1, 2.0, 3.6, 2.5, 1.6, 3.6, "twin"),
    ("Policy and goodwill % of gross", "Goodwill granted \u00f7 service department gross profit", "pct", -1, 2.0, 1.6, 2.1, 1.2, None, ""),
    ("Technician-to-support ratio", "Technicians \u00f7 service support personnel", "ratio", 1, 3.0, 3.2, 2.9, 3.4, None, ""),
  ]),
  ("variable", "New and used trucks", [
    ("New-truck days' supply", "New-truck inventory \u00f7 average daily cost of sales", "days", -1, 60, 74, 63, 51, 74, "twin"),
    ("New-truck turn rate", "Annual cost of sales \u00f7 average inventory", "x", 1, 6.0, 4.9, 5.8, 7.2, 4.9, "twin"),
    ("New-truck gross % sales", "New-truck gross profit \u00f7 new-truck sales", "pct", 1, 8.0, 8.4, 7.6, 9.4, None, ""),
    ("Used-truck days' supply", "Used-truck inventory \u00f7 average daily cost of sales", "days", -1, 60, 88, 66, 47, 88, "twin"),
    ("Used-truck turn rate", "Annual cost of sales \u00f7 average inventory", "x", 1, 6.0, 4.1, 5.6, 7.8, 4.1, "twin"),
    ("Used-truck gross % sales", "Used-truck gross profit \u00f7 used-truck sales", "pct", 1, 12.0, 12.7, 11.7, 14.6, None, ""),
    ("Units per salesperson \u2014 new", "New units delivered \u00f7 non-fleet salespeople per month", "num", 1, 7.0, 7.3, 6.6, 8.3, None, ""),
    ("Units per salesperson \u2014 used", "Used units delivered \u00f7 non-fleet salespeople per month", "num", 1, 5.5, 5.1, 5.2, 6.9, None, ""),
  ]),
  ("capital", "Capital and liquidity", [
    ("Current ratio", "Total current assets \u00f7 total current liabilities", "ratio", 1, 2.25, 2.31, 2.18, 2.61, None, ""),
    ("Debt to equity", "Total liabilities \u00f7 equity", "ratio", -1, 3.0, 2.7, 2.9, 2.1, None, ""),
    ("Cash days' supply", "Cash and near-cash \u00f7 average month expense \u00d7 30", "days", 1, 30, 38, 34, 61, None, ""),
    ("Inventory trust position", "New-truck inventory + holdback receivables \u2212 notes payable on new trucks", "usd", 1, 0, 640000, 310000, 1240000, 640000, "twin"),
    ("Frozen capital", "Cash tied up in aged or excess receivables and inventory", "usd", -1, 0, 412000, 168000, 0, 412000, "twin"),
    ("Warranty receivables over 30 days", "Warranty claims outstanding beyond 30 days", "usd", -1, 0, 186400, 74000, 12000, 186400, "twin"),
  ]),
]

ACTIONS = [
  ("Rebalance 40 slow lines across the nine centres",
   "Parts fill rate \u00b7 parts obsolescence \u00b7 frozen capital",
   "HT-16 / inventory twin",
   "+4.6 pts fill rate, \u2212$77k avoidable cost",
   "Ready \u2014 running on synthetic data today"),
  ("Close the 4.3-day open-RO tail",
   "Open repair orders \u00b7 work in process \u00b7 fixed absorption",
   "HT-04 / phone and DMS ingest",
   "Frees roughly two days of labour value in WIP",
   "Blocked on Telus and CDK access"),
  ("Chase warranty receivables past 30 days",
   "Warranty receivables \u00b7 cash days' supply",
   "HT-10 / PACCAR portal",
   "$186k of cash currently parked",
   "Blocked on the PACCAR agreement read"),
  ("Answer the missed-call queue",
   "Stall utilization \u00b7 hours per RO \u00b7 absorption",
   "HT-04 / phone system",
   "Unquantified until the call data lands",
   "First live proof \u2014 next to build"),
  ("Drop the removable subscriptions",
   "Net profit return on sales \u00b7 expense ratios",
   "HT-15 / Bulletproof invoice",
   "Target $1,000/month, repays the engagement",
   "Blocked on the invoice"),
  ("Age out the 88-day used-truck position",
   "Used-truck days' supply \u00b7 used-truck turn \u00b7 frozen capital",
   "HT-16 / inventory twin",
   "28 days of supply above guide",
   "Ready once VIN structure is mirrored"),
]
