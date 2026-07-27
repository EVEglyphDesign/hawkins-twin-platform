#!/usr/bin/env python3
"""
EVEglyphDesign — Hawkins Twin sample-data generator.

Produces a fully SYNTHETIC parts and vehicle inventory dataset across nine
notional centres, for the sandbox demo. No Hawkins data, no live system access,
no customer records. Deterministic: seeded, so the demo is reproducible and
every number on the surface can be traced back to this script.

Output: sample_data.json
"""
import json, random, hashlib, datetime

SEED = 20260727
random.seed(SEED)

CENTRES = [
    {"code": "HNW", "name": "Hanwell",      "prov": "NB", "size": 1.00, "role": "Pilot centre · main parts hub"},
    {"code": "MNC", "name": "Moncton",      "prov": "NB", "size": 0.92, "role": "Regional hub"},
    {"code": "SJN", "name": "Saint John",   "prov": "NB", "size": 0.80, "role": "Port / heavy haul"},
    {"code": "EDM", "name": "Edmundston",   "prov": "NB", "size": 0.55, "role": "Forestry corridor"},
    {"code": "BAT", "name": "Bathurst",     "prov": "NB", "size": 0.48, "role": "North shore"},
    {"code": "TRU", "name": "Truro",        "prov": "NS", "size": 0.74, "role": "Crossroads / transfer node"},
    {"code": "DAR", "name": "Dartmouth",    "prov": "NS", "size": 0.86, "role": "Metro service"},
    {"code": "SYD", "name": "Sydney",       "prov": "NS", "size": 0.42, "role": "Cape Breton"},
    {"code": "CHA", "name": "Charlottetown","prov": "PE", "size": 0.50, "role": "Island / seasonal"},
]

PART_CLASSES = [
    # class, share of lines, unit-cost range, base monthly demand, criticality
    ("Filtration",        0.16, (18, 120),   9.0, "high"),
    ("Brake & air",       0.14, (45, 640),   6.5, "critical"),
    ("Engine & aftertreat",0.12,(180, 4200), 3.0, "critical"),
    ("Electrical",        0.12, (25, 900),   5.5, "high"),
    ("Driveline",         0.10, (120, 3100), 2.2, "medium"),
    ("Suspension & steer",0.09, (85, 1800),  2.8, "medium"),
    ("Cab & trim",        0.09, (30, 1400),  2.0, "low"),
    ("Cooling",           0.07, (60, 1500),  2.4, "high"),
    ("Fluids & chemical", 0.06, (12, 210),  11.0, "low"),
    ("Tooling & shop",    0.05, (22, 900),   1.2, "low"),
]

PART_NAMES = {
    "Filtration": ["Fuel filter element", "Oil filter, spin-on", "Air filter, primary", "Air filter, safety",
                   "Coolant filter", "Hydraulic filter", "DEF inlet filter", "Cabin air filter"],
    "Brake & air": ["Brake shoe kit", "Brake drum", "Air dryer cartridge", "Slack adjuster", "Relay valve",
                    "Air spring, drive", "Brake chamber 30/30", "S-cam kit"],
    "Engine & aftertreat": ["DPF assembly", "EGR cooler", "Turbo cartridge", "Injector, common rail",
                            "Water pump", "DEF dosing unit", "NOx sensor", "Fuel rail pressure sensor"],
    "Electrical": ["Alternator 160A", "Starter motor", "Battery, group 31", "Harness, chassis rear",
                   "Headlamp assembly, LH", "ABS wheel speed sensor", "Dash switch pod", "Ground stud kit"],
    "Driveline": ["Clutch kit, 15.5", "U-joint kit", "Differential carrier", "Driveshaft, centre",
                  "Transmission shift cyl.", "Axle shaft", "Wheel seal kit", "Yoke, slip"],
    "Suspension & steer": ["Leaf spring pack", "Shock absorber, steer", "Torque rod", "King pin kit",
                           "Tie rod end", "Steering gear", "Bushing kit, hanger", "Air ride levelling valve"],
    "Cab & trim": ["Mirror assembly, RH", "Door latch", "Seat cushion, air ride", "Windshield wiper motor",
                   "Grille surround", "Bumper end cap", "Step assembly", "HVAC blower"],
    "Cooling": ["Radiator assembly", "Charge air cooler", "Fan clutch", "Thermostat kit",
                "Coolant hose, upper", "Surge tank", "Fan blade", "Belt tensioner"],
    "Fluids & chemical": ["Engine oil 15W-40 pail", "DEF 9.5L jug", "Coolant, ELC concentrate",
                          "Gear lube 80W-90", "Grease cartridge", "Brake cleaner", "Windshield fluid", "Shop rags"],
    "Tooling & shop": ["Torque wrench, 3/4", "Air impact 1/2", "Wheel dolly", "Diagnostic cable kit",
                       "Pressure test kit", "Jack stand pair", "Bench grinder wheel", "Creeper seat"],
}

MODELS = [
    ("Peterbilt 579", "Highway tractor", 0.30, (168000, 232000)),
    ("Peterbilt 567", "Vocational / heavy", 0.22, (192000, 268000)),
    ("Peterbilt 589", "Highway tractor", 0.12, (205000, 285000)),
    ("Peterbilt 548", "Medium duty", 0.14, (128000, 176000)),
    ("Peterbilt 536", "Medium duty", 0.12, (112000, 158000)),
    ("Peterbilt 220", "Urban / refuse", 0.10, (138000, 186000)),
]

STATUSES = ["Available", "Available", "Available", "Allocated", "In prep", "Demo unit"]


def pick(weighted):
    r = random.random()
    acc = 0.0
    for row in weighted:
        acc += row[2] if len(row) > 3 else row[1]
        if r <= acc:
            return row
    return weighted[-1]


def gen_parts():
    parts = []
    pid = 1000
    for cls, share, (lo, hi), base_demand, crit in PART_CLASSES:
        n_lines = max(6, round(share * 180))
        for i in range(n_lines):
            pid += 1
            name = random.choice(PART_NAMES[cls])
            unit_cost = round(random.uniform(lo, hi), 2)
            part_no = f"{cls[:2].upper()}-{pid}-{random.randint(10,99)}"
            seasonal = round(random.uniform(0.75, 1.35), 2)
            for c in CENTRES:
                demand = base_demand * c["size"] * seasonal * random.uniform(0.55, 1.55)
                demand_m = round(max(0.2, demand), 1)
                lead_days = random.choice([3, 5, 7, 10, 14, 21, 28])
                # incumbent behaviour: a static reorder point that ignores lead time
                static_rop = max(1, round(demand_m * 0.9))
                # the twin's reorder point: lead-time aware, criticality weighted
                safety = 1.0 + (0.45 if crit in ("critical", "high") else 0.2)
                twin_rop = max(1, round(demand_m * (lead_days / 30.0) * safety + (2 if crit == "critical" else 0)))
                # months of supply on hand drives everything else
                mos = random.choice([
                    random.uniform(0.0, 0.4),   # thin
                    random.uniform(0.4, 1.5),   # tight
                    random.uniform(1.5, 3.5),   # healthy
                    random.uniform(1.5, 3.5),
                    random.uniform(3.5, 9.0),   # heavy
                ])
                onhand = round(demand_m * mos)
                if onhand == 0 and random.random() > 0.35:
                    onhand = 1
                turns = round(min(24.0, (demand_m * 12) / max(onhand, 0.8)), 1)
                last_move = random.randint(0, 420) if mos > 3.0 else random.randint(0, 120)
                aged = last_move > 270 and onhand > 0
                if onhand == 0:
                    risk = "Stockout"
                elif onhand < twin_rop:
                    risk = "At risk"
                elif onhand > twin_rop * 2.4 and turns < 3.2:
                    risk = "Overstock"
                else:
                    risk = "Healthy"
                parts.append({
                    "part_no": part_no, "name": name, "cls": cls, "crit": crit,
                    "centre": c["code"], "onhand": onhand, "unit_cost": unit_cost,
                    "demand_m": demand_m, "lead_days": lead_days,
                    "static_rop": static_rop, "twin_rop": twin_rop,
                    "mos": round(mos, 1),
                    "turns": turns, "days_since_move": last_move,
                    "aged": aged, "risk": risk,
                })
    return parts


def gen_vins():
    vins = []
    for c in CENTRES:
        n = max(6, round(26 * c["size"]))
        for _ in range(n):
            model, seg, _w, (lo, hi) = pick(MODELS)
            year = random.choice([2025, 2026, 2026, 2026, 2027])
            vin = "1XP" + "".join(random.choice("ABCDEFGHJKLMNPRSTUVWXYZ0123456789") for _ in range(14))
            age = random.randint(2, 340)
            price = round(random.uniform(lo, hi), -2)
            status = random.choice(STATUSES)
            vins.append({
                "vin": vin, "model": model, "segment": seg, "year": year,
                "centre": c["code"], "age_days": age, "floorplan": price,
                "status": status,
                "flag": "Aged floor plan" if age > 210 else ("Watch" if age > 140 else "Normal"),
            })
    return vins


def gen_transfers(parts):
    """Twin recommends inter-centre transfers: pair shortage centres with overstock centres."""
    by_part = {}
    for p in parts:
        by_part.setdefault(p["part_no"], []).append(p)
    recs = []
    rid = 0
    for part_no, rows in by_part.items():
        short = [r for r in rows if r["risk"] in ("Stockout", "At risk")]
        over = [r for r in rows if r["risk"] == "Overstock"]
        if not short or not over:
            continue
        for s in short[:2]:
            o = max(over, key=lambda r: r["onhand"] - r["twin_rop"])
            surplus = o["onhand"] - o["twin_rop"]
            qty = max(1, min(surplus // 2, max(1, s["twin_rop"] - s["onhand"])))
            if qty < 1 or surplus < 2:
                continue
            rid += 1
            avoided = round(qty * s["unit_cost"] * (1.18 if s["crit"] == "critical" else 1.06), 2)
            conf = min(0.97, 0.58 + (0.11 if s["crit"] == "critical" else 0) +
                       min(0.24, s["demand_m"] / 40.0) + random.uniform(0, 0.10))
            recs.append({
                "id": f"TR-{rid:04d}", "part_no": part_no, "name": s["name"], "cls": s["cls"],
                "from": o["centre"], "to": s["centre"], "qty": int(qty),
                "reason": ("Stockout at destination; surplus at source"
                           if s["risk"] == "Stockout" else
                           "Below twin reorder point; surplus at source"),
                "crit": s["crit"], "value": round(qty * s["unit_cost"], 2),
                "avoided": avoided, "confidence": round(conf, 2),
                "lead_days": s["lead_days"], "status": "Awaiting approval",
            })
    recs.sort(key=lambda r: (-r["confidence"], -r["avoided"]))
    return recs[:40]


def centre_rollup(parts, vins):
    out = []
    for c in CENTRES:
        cp = [p for p in parts if p["centre"] == c["code"]]
        cv = [v for v in vins if v["centre"] == c["code"]]
        lines = len(cp)
        value = sum(p["onhand"] * p["unit_cost"] for p in cp)
        stockouts = sum(1 for p in cp if p["risk"] == "Stockout")
        at_risk = sum(1 for p in cp if p["risk"] == "At risk")
        over = sum(1 for p in cp if p["risk"] == "Overstock")
        aged_val = sum(p["onhand"] * p["unit_cost"] for p in cp if p["aged"])
        fill = round(100 * (1 - (stockouts + 0.35 * at_risk) / max(lines, 1)), 1)
        turns = round(sum(p["turns"] for p in cp) / max(lines, 1), 1)
        out.append({
            "code": c["code"], "name": c["name"], "prov": c["prov"], "role": c["role"],
            "lines": lines, "value": round(value, 2), "stockouts": stockouts,
            "at_risk": at_risk, "overstock": over, "aged_value": round(aged_val, 2),
            "fill_rate": fill, "turns": turns,
            "units": len(cv), "floorplan": round(sum(v["floorplan"] for v in cv), 2),
            "aged_units": sum(1 for v in cv if v["flag"] == "Aged floor plan"),
        })
    return out


def main():
    parts = gen_parts()
    vins = gen_vins()
    recs = gen_transfers(parts)
    centres = centre_rollup(parts, vins)

    lines = len(parts)
    stockouts = sum(1 for p in parts if p["risk"] == "Stockout")
    at_risk = sum(1 for p in parts if p["risk"] == "At risk")
    fill_twin = round(100 * (1 - (stockouts + 0.35 * at_risk) / lines), 1)
    # incumbent static reorder point would have covered fewer lines
    # modelled incumbent behaviour: lines where a static, lead-time-blind reorder
    # point sits below the twin's reorder point would not have triggered in time
    static_gap = sum(1 for p in parts
                     if p["static_rop"] < p["twin_rop"] and p["risk"] != "Overstock")
    fill_static = round(100 * (1 - (stockouts + 0.35 * at_risk + 0.22 * static_gap) / lines), 1)

    data = {
        "meta": {
            "generator": "generate_sample_data.py",
            "seed": SEED,
            "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "notice": "100% SYNTHETIC DATA. Generated from a seeded random model. "
                      "No Hawkins Truck Mart, Peterbilt Atlantic, PACCAR, BRP or CDK data, "
                      "no live system access, no customer records.",
            "centres_note": "Nine notional centres. Place names are Atlantic-Canada plausible "
                            "but the inventory, VINs, values and demand are invented.",
        },
        "kpi": {
            "parts_lines": lines,
            "parts_value": round(sum(p["onhand"] * p["unit_cost"] for p in parts), 2),
            "units": len(vins),
            "floorplan": round(sum(v["floorplan"] for v in vins), 2),
            "fill_rate_twin": fill_twin,
            "fill_rate_static": fill_static,
            "turns": round(sum(p["turns"] for p in parts) / lines, 1),
            "stockouts": stockouts,
            "at_risk": at_risk,
            "overstock": sum(1 for p in parts if p["risk"] == "Overstock"),
            "aged_value": round(sum(p["onhand"] * p["unit_cost"] for p in parts if p["aged"]), 2),
            "aged_units": sum(1 for v in vins if v["flag"] == "Aged floor plan"),
            "recs": len(recs),
            "recs_value": round(sum(r["avoided"] for r in recs), 2),
        },
        "centres": centres,
        "parts": parts,
        "vins": vins,
        "recs": recs,
        "classes": [c[0] for c in PART_CLASSES],
    }
    blob = json.dumps(data, separators=(",", ":"), sort_keys=True)
    data["meta"]["content_hash"] = hashlib.sha256(blob.encode()).hexdigest()[:16]
    with open("sample_data.json", "w") as f:
        json.dump(data, f, separators=(",", ":"))
    print(f"parts={lines} vins={len(vins)} recs={len(recs)} hash={data['meta']['content_hash']}")


if __name__ == "__main__":
    main()
