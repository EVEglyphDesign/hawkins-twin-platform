import { trucks, telemetry, sensorMap, parts, alerts } from "@shared/schema";

// Peterbilt Atlantic nine-centre topology (WERKS PA01..PA09)
const CENTERS: Record<string, [string, number, number]> = {
  PA01: ["Moncton, NB", 46.0878, -64.7782],
  PA02: ["Hanwell, NB", 45.9166, -66.7573],
  PA03: ["Dartmouth, NS", 44.6658, -63.5669],
  PA04: ["Truro, NS", 45.3669, -63.2799],
  PA05: ["Charlottetown, PE", 46.2382, -63.1311],
  PA06: ["St. John's, NL", 47.5615, -52.7126],
  PA07: ["Grand Falls, NB", 47.0472, -67.7411],
  PA08: ["Sydney, NS", 46.1368, -60.1942],
  PA09: ["Rimouski, QC", 48.4489, -68.5236],
};
const CK = Object.keys(CENTERS);

function pick<T>(a: T[], i: number): T { return a[i % a.length]; }
const now = new Date("2026-07-02T20:00:00-04:00");
const iso = (d: Date) => d.toISOString();

// ----- FLEET -----------------------------------------------------------------
const MODELS = [
  ["579", "PACCAR MX-13", "SmartLINQ"], ["579", "Cummins X15", "SmartLINQ"],
  ["589", "PACCAR MX-13", "SmartLINQ"], ["567", "PACCAR MX-11", "PACCAR Solutions"],
  ["548", "PACCAR PX-9", "FleetRight"], ["579EV", "PACCAR EV", "SmartLINQ"],
  ["520EV", "PACCAR EV", "SmartLINQ"], ["567", "Cummins X15", "PACCAR Solutions"],
];
const CUSTOMERS = [
  "Mutch Trucking Ltd.", "WCF Transport", "Fundy Express Transport", "Ocean Crisp Transport",
  "Leader by Litre", "Parker Trucking", "Robbins Trucking", "Belgo Transport",
  "Kingharv Inc.", "St. Mary's First Nation", "JE March", "Trent Hill Haulage",
  "Rose's Mobile 1", "Maritime Bulk Carriers", "Acadian Freight Lines", "Sable Logistics",
  "Gulf Shore Transport", "Northumberland Haul", "Cabot Trail Carriers", "Miramichi Freight",
];

export function seedAll(db: any) {
  const truckRows: any[] = [];
  for (let i = 0; i < 20; i++) {
    const [model, engine, tele] = pick(MODELS, i);
    const werks = pick(CK, i);
    const [cname, lat, lng] = CENTERS[werks];
    const isEV = model.includes("EV");
    const health = [98, 71, 44, 88, 63, 92, 55, 81, 34, 76, 95, 68, 49, 84, 90, 58, 73, 41, 86, 67][i];
    const status = health < 45 ? "in_service" : health < 60 ? "idle" : "active";
    truckRows.push({
      vin: `1XPBD49X${(7 + i).toString().padStart(2, "0")}D${782600 + i * 137}`,
      unitNo: `PA-${(101 + i)}`,
      model, engine, year: 2024 + (i % 3), customer: pick(CUSTOMERS, i),
      homeCenter: werks, centerName: cname, status,
      odometerKm: 40000 + i * 21350, engineHours: 1200 + i * 640,
      telematics: tele as string, healthScore: health,
      lat: lat + (Math.sin(i) * 0.4), lng: lng + (Math.cos(i) * 0.4),
    });
  }
  db.insert(trucks).values(truckRows).run();
  const saved = db.select().from(trucks).all();

  // ----- TELEMETRY (latest snapshot per truck) -------------------------------
  const telRows = saved.map((t: any, i: number) => {
    const isEV = t.model.includes("EV");
    const low = t.healthScore < 55;
    return {
      truckId: t.id, capturedAt: iso(new Date(now.getTime() - (i % 5) * 15000)),
      speedKph: t.status === "active" ? 82 + (i % 20) : 0,
      rpm: t.status === "active" ? 1350 + (i % 6) * 40 : isEV ? 0 : 620,
      coolantC: isEV ? 38 + (i % 6) : low ? 104 + (i % 6) : 88 + (i % 5),
      oilPsi: isEV ? 0 : low ? 24 + (i % 4) : 41 + (i % 6),
      fuelPct: isEV ? 0 : 30 + ((i * 7) % 65),
      defPct: isEV ? 0 : low ? 8 + (i % 5) : 45 + ((i * 5) % 50),
      batteryV: low ? 12.1 + (i % 3) * 0.1 : 13.6 + (i % 4) * 0.1,
      socPct: isEV ? 40 + ((i * 9) % 55) : null,
      brakeWearPct: low ? 78 + (i % 12) : 22 + ((i * 6) % 40),
      tirePsiAvg: 108 - (i % 7) - (low ? 12 : 0),
      faultCount: low ? 2 + (i % 3) : i % 2,
      regenPct: isEV ? 0 : low ? 92 + (i % 6) : (i * 13) % 60,
      ambientC: 18 + (i % 10),
    };
  });
  db.insert(telemetry).values(telRows).run();

  // ----- SENSOR MAP (physical channel → digital-model node) ------------------
  const smRows = [
    ["ECU-100", "PACCAR Solutions", "Engine Oil Pressure Sensor", "SPN 100", "twin.powertrain.engine.oil.pressure", "oilPsi", "psi", 5, "live"],
    ["ECU-110", "PACCAR Solutions", "Engine Coolant Temp Sensor", "SPN 110", "twin.powertrain.cooling.coolant.temp", "coolantC", "°C", 5, "live"],
    ["ECU-190", "PACCAR Solutions", "Engine Speed (Crank)", "SPN 190", "twin.powertrain.engine.speed", "rpm", "rpm", 20, "live"],
    ["ATS-3226", "SmartLINQ", "SCR Outlet NOx / DEF Level", "SPN 3226/1761", "twin.aftertreatment.def.level", "defPct", "%", 1, "live"],
    ["ATS-3701", "SmartLINQ", "DPF Soot Load / Regen State", "SPN 3701", "twin.aftertreatment.dpf.regen", "regenPct", "%", 1, "live"],
    ["BRK-070", "SmartLINQ", "Brake Lining Wear Sensor", "SPN 070", "twin.chassis.brakes.lining.wear", "brakeWearPct", "%", 0.5, "live"],
    ["TPMS-2586", "FleetRight", "Tire Pressure Monitor (avg)", "SPN 2586", "twin.chassis.tires.pressure.avg", "tirePsiAvg", "psi", 0.2, "live"],
    ["ELE-168", "PACCAR Solutions", "Battery Potential / Voltage", "SPN 168", "twin.electrical.battery.voltage", "batteryV", "V", 1, "live"],
    ["FUE-96", "FleetRight", "Fuel Level Sensor", "SPN 96", "twin.powertrain.fuel.level", "fuelPct", "%", 0.5, "live"],
    ["GPS-NMEA", "SmartLINQ", "GNSS Position / Speed", "NMEA RMC", "twin.telemetry.position", "speedKph", "kph", 1, "live"],
    ["EV-SOC-8092", "SmartLINQ", "HV Battery State of Charge", "SPN 8092", "twin.ev.hvbattery.soc", "socPct", "%", 1, "stale"],
    ["AMB-171", "PACCAR Solutions", "Ambient Air Temperature", "SPN 171", "twin.environment.ambient.temp", "ambientC", "°C", 0.2, "live"],
    ["DTC-1213", "SmartLINQ", "Active Fault Code Count (MIL)", "SPN 1213", "twin.diagnostics.active.faults", "faultCount", "count", 1, "live"],
  ].map((r) => ({
    channel: r[0] as string, sourceSystem: r[1] as string, physicalSensor: r[2] as string,
    j1939Spn: r[3] as string, twinNode: r[4] as string, twinField: r[5] as string,
    unit: r[6] as string, hz: r[7] as number, status: r[8] as string,
  }));
  db.insert(sensorMap).values(smRows).run();

  // ----- PARTS (SAP MARA/MARC/MARD mirror) -----------------------------------
  const PART_DEFS = [
    ["S64-1002", "DPF Filter Assembly, MX-13", "Filtre à particules DPF, MX-13", "PACCAR", "2600344PE", "AFTRTMT", "V", "S", 3820.0, 21],
    ["S64-1188", "DEF Dosing Injector", "Injecteur de dosage DEF", "PACCAR", "1877854", "AFTRTMT", "E", "F", 612.5, 7],
    ["A45-6620", "Brake Pad Set, Bendix ADB22X", "Jeu de plaquettes de frein ADB22X", "Bendix", "K068867", "BRAKES", "V", "F", 289.9, 5],
    ["N28-9004", "Coolant Thermostat, 82°C", "Thermostat de refroidissement 82°C", "PACCAR", "1657959", "COOLING", "E", "S", 96.4, 10],
    ["E11-3300", "AGM Group 31 Battery", "Batterie AGM Groupe 31", "Peterbilt OE", "16-09873", "ELECTRIC", "E", "F", 348.0, 4],
    ["T90-2586", "TPMS Wheel Sensor", "Capteur TPMS de roue", "TRP", "TP-2586", "TIRES", "D", "N", 74.2, 14],
    ["S64-1002R", "DPF Filter, Reman (core)", "Filtre DPF reconditionné (carcasse)", "PACCAR", "2600344R", "AFTRTMT", "V", "S", 2410.0, 30],
    ["O12-4407", "Oil Pressure Sensor", "Capteur de pression d'huile", "Cummins", "4921517", "ENGINE", "E", "F", 133.7, 6],
  ];
  const partRows: any[] = [];
  PART_DEFS.forEach((p, pi) => {
    // stock this part at 3 of the 9 centres
    for (let k = 0; k < 3; k++) {
      const werks = pick(CK, pi * 3 + k);
      const [cname] = CENTERS[werks];
      const onHand = [pi === 0 ? 1 : 6, 3, 0][k] + (pi % 2);
      const reorder = 2 + (pi % 3);
      partRows.push({
        matnr: p[0], maktx: p[1], maktxFr: p[2], manufacturer: p[3], mfrPartNumber: p[4],
        matkl: p[5], vedClass: p[6], fsnClass: p[7], werks, centerName: cname,
        labst: onHand, umlme: k === 2 ? 2 : 0, minbe: reorder, eisbe: 1,
        plifz: p[9] as number, bin: `${werks}-${String.fromCharCode(65 + k)}${12 + pi}`,
        unitPrice: p[8] as number, daysOfSupply: onHand === 0 ? 0 : 5 + onHand * 3,
      });
    }
  });
  db.insert(parts).values(partRows).run();

  // ----- PREDICTIVE ALERTS (linked to parts) ---------------------------------
  const critical = saved.filter((t: any) => t.healthScore < 60);
  const alertRows: any[] = [];
  const ALERT_TEMPLATES = [
    { severity: "critical", system: "Aftertreatment", title: "DPF soot load trending to derate", detail: "Regen efficiency down 34% over 14 days. Soot load approaching forced-derate threshold.", spn: "SPN 3701", days: 6, conf: 91, matnr: "S64-1002", part: "DPF Filter Assembly, MX-13" },
    { severity: "critical", system: "Brakes", title: "Brake lining below service limit", detail: "Steer-axle lining wear at 88%; predicted metal-to-metal within one duty cycle.", spn: "SPN 070", days: 4, conf: 87, matnr: "A45-6620", part: "Brake Pad Set, Bendix ADB22X" },
    { severity: "warning", system: "Cooling", title: "Coolant temp excursions rising", detail: "Peak coolant 106°C under load; thermostat response degrading.", spn: "SPN 110", days: 12, conf: 74, matnr: "N28-9004", part: "Coolant Thermostat, 82°C" },
    { severity: "warning", system: "Emissions", title: "DEF dosing fault intermittent", detail: "SCR NOx conversion dropping; dosing injector likely fouling.", spn: "SPN 3226", days: 9, conf: 69, matnr: "S64-1188", part: "DEF Dosing Injector" },
    { severity: "watch", system: "Electrical", title: "Battery voltage sag at start", detail: "Cranking voltage 12.1V cold; AGM capacity fading.", spn: "SPN 168", days: 18, conf: 58, matnr: "E11-3300", part: "AGM Group 31 Battery" },
  ];
  critical.forEach((t: any, i: number) => {
    const tpl = pick(ALERT_TEMPLATES, i);
    // resolve parts availability at truck's home center + network
    const homeStock = partRows.filter((p) => p.matnr === tpl.matnr && p.werks === t.homeCenter)
      .reduce((s, p) => s + p.labst, 0);
    const hubStock = partRows.filter((p) => p.matnr === tpl.matnr).reduce((s, p) => s + p.labst, 0);
    alertRows.push({
      truckId: t.id, raisedAt: iso(new Date(now.getTime() - i * 3600000)),
      severity: tpl.severity, system: tpl.system, title: tpl.title, detail: tpl.detail,
      j1939Spn: tpl.spn, predictedFailureDays: tpl.days, confidencePct: tpl.conf,
      matnr: tpl.matnr, partName: tpl.part, partsInStock: homeStock, partsHubStock: hubStock,
      status: "open",
    });
  });
  db.insert(alerts).values(alertRows).run();
}
