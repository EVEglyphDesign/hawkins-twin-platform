import { sqliteTable, text, integer, real } from "drizzle-orm/sqlite-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

// ---------------------------------------------------------------------------
// TRUCKS — physical Peterbilt assets in the dealer-owned registry
// ---------------------------------------------------------------------------
export const trucks = sqliteTable("trucks", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  vin: text("vin").notNull().unique(),
  unitNo: text("unit_no").notNull(),
  model: text("model").notNull(),          // 579, 589, 567, 548, 579EV ...
  engine: text("engine").notNull(),        // PACCAR MX-13, Cummins X15, EV
  year: integer("year").notNull(),
  customer: text("customer").notNull(),
  homeCenter: text("home_center").notNull(),   // WERKS site code PA01..PA09
  centerName: text("center_name").notNull(),
  status: text("status").notNull(),        // active | idle | in_service | offline
  odometerKm: integer("odometer_km").notNull(),
  engineHours: integer("engine_hours").notNull(),
  telematics: text("telematics").notNull(),    // SmartLINQ | FleetRight | PACCAR Solutions
  healthScore: integer("health_score").notNull(), // 0-100 composite
  lat: real("lat").notNull(),
  lng: real("lng").notNull(),
});

// ---------------------------------------------------------------------------
// TELEMETRY — latest live sensor snapshot per truck (real-time feed)
// ---------------------------------------------------------------------------
export const telemetry = sqliteTable("telemetry", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  truckId: integer("truck_id").notNull(),
  capturedAt: text("captured_at").notNull(),
  speedKph: real("speed_kph").notNull(),
  rpm: integer("rpm").notNull(),
  coolantC: real("coolant_c").notNull(),
  oilPsi: real("oil_psi").notNull(),
  fuelPct: real("fuel_pct").notNull(),
  defPct: real("def_pct").notNull(),           // diesel exhaust fluid
  batteryV: real("battery_v").notNull(),
  socPct: real("soc_pct"),                     // EV state of charge (nullable)
  brakeWearPct: real("brake_wear_pct").notNull(),
  tirePsiAvg: real("tire_psi_avg").notNull(),
  faultCount: integer("fault_count").notNull(),
  regenPct: real("regen_pct").notNull(),       // DPF regeneration progress
  ambientC: real("ambient_c").notNull(),
});

// ---------------------------------------------------------------------------
// SENSOR MAP — maps a physical sensor channel to the digital-model node
// ---------------------------------------------------------------------------
export const sensorMap = sqliteTable("sensor_map", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  channel: text("channel").notNull(),          // SPN/PID-style source channel
  sourceSystem: text("source_system").notNull(),   // SmartLINQ | PACCAR Solutions | FleetRight
  physicalSensor: text("physical_sensor").notNull(),  // on-truck sensor name
  j1939Spn: text("j1939_spn").notNull(),       // SAE J1939 SPN reference
  twinNode: text("twin_node").notNull(),       // digital-model node path
  twinField: text("twin_field").notNull(),     // telemetry column it feeds
  unit: text("unit").notNull(),
  hz: real("hz").notNull(),                    // sample rate
  status: text("status").notNull(),            // live | stale | dropped
});

// ---------------------------------------------------------------------------
// PARTS — SAP-shape material master mirror (MARA + MARC + MARD flattened)
// ---------------------------------------------------------------------------
export const parts = sqliteTable("parts", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  matnr: text("matnr").notNull(),              // MARA.MATNR material number
  maktx: text("maktx").notNull(),              // description EN
  maktxFr: text("maktx_fr").notNull(),         // description FR (AC market)
  manufacturer: text("manufacturer").notNull(),
  mfrPartNumber: text("mfr_part_number").notNull(),
  matkl: text("matkl").notNull(),              // material group
  vedClass: text("ved_class").notNull(),       // V/E/D criticality
  fsnClass: text("fsn_class").notNull(),       // F/S/N velocity
  werks: text("werks").notNull(),              // MARC plant PA01..PA09
  centerName: text("center_name").notNull(),
  labst: integer("labst").notNull(),           // MARD unrestricted on-hand
  umlme: integer("umlme").notNull(),           // MARD in transit
  minbe: integer("minbe").notNull(),           // MARC reorder point
  eisbe: integer("eisbe").notNull(),           // MARC safety stock
  plifz: integer("plifz").notNull(),           // MARC planned delivery days
  bin: text("bin").notNull(),                  // MARD physical bin
  unitPrice: real("unit_price").notNull(),
  daysOfSupply: integer("days_of_supply").notNull(),
});

// ---------------------------------------------------------------------------
// ALERTS — predictive maintenance alerts derived from telemetry
// ---------------------------------------------------------------------------
export const alerts = sqliteTable("alerts", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  truckId: integer("truck_id").notNull(),
  raisedAt: text("raised_at").notNull(),
  severity: text("severity").notNull(),        // critical | warning | watch
  system: text("system").notNull(),            // Aftertreatment | Cooling | Brakes ...
  title: text("title").notNull(),
  detail: text("detail").notNull(),
  j1939Spn: text("j1939_spn").notNull(),
  predictedFailureDays: integer("predicted_failure_days").notNull(),
  confidencePct: integer("confidence_pct").notNull(),
  matnr: text("matnr"),                        // linked part (nullable)
  partName: text("part_name"),
  partsInStock: integer("parts_in_stock"),     // on-hand at home center
  partsHubStock: integer("parts_hub_stock"),   // available across network
  status: text("status").notNull(),            // open | offered | scheduled | cleared
});

// ---------------------------------------------------------------------------
// OFFERS — overnight (off-hours) repair "betterment" outreach offers
// ---------------------------------------------------------------------------
export const offers = sqliteTable("offers", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  alertId: integer("alert_id").notNull(),
  truckId: integer("truck_id").notNull(),
  createdAt: text("created_at").notNull(),
  customer: text("customer").notNull(),
  contactName: text("contact_name").notNull(),
  channel: text("channel").notNull(),          // SMS | Email | Prokeep
  bayCenter: text("bay_center").notNull(),
  slotStart: text("slot_start").notNull(),     // overnight window start
  slotEnd: text("slot_end").notNull(),
  downtimeSavedHrs: real("downtime_saved_hrs").notNull(),
  bayUtilGainPct: integer("bay_util_gain_pct").notNull(),
  message: text("message").notNull(),          // drafted outreach copy
  state: text("state").notNull(),              // draft | sent | accepted | declined
});

// ---- insert schemas + types -------------------------------------------------
export const insertTruckSchema = createInsertSchema(trucks).omit({ id: true });
export const insertTelemetrySchema = createInsertSchema(telemetry).omit({ id: true });
export const insertSensorMapSchema = createInsertSchema(sensorMap).omit({ id: true });
export const insertPartSchema = createInsertSchema(parts).omit({ id: true });
export const insertAlertSchema = createInsertSchema(alerts).omit({ id: true });
export const insertOfferSchema = createInsertSchema(offers).omit({ id: true });

export type Truck = typeof trucks.$inferSelect;
export type Telemetry = typeof telemetry.$inferSelect;
export type SensorMap = typeof sensorMap.$inferSelect;
export type Part = typeof parts.$inferSelect;
export type Alert = typeof alerts.$inferSelect;
export type Offer = typeof offers.$inferSelect;

export type InsertTruck = z.infer<typeof insertTruckSchema>;
export type InsertOffer = z.infer<typeof insertOfferSchema>;

// Composite row the fleet table renders (truck + latest telemetry)
export type FleetRow = Truck & { latest: Telemetry | null; openAlerts: number };
