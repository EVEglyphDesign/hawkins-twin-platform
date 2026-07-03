import {
  trucks, telemetry, sensorMap, parts, alerts, offers,
} from "@shared/schema";
import type {
  Truck, Telemetry, SensorMap, Part, Alert, Offer, InsertOffer, FleetRow,
} from "@shared/schema";
import { drizzle } from "drizzle-orm/better-sqlite3";
import Database from "better-sqlite3";
import { eq, desc } from "drizzle-orm";
import { seedAll } from "./seed";

const sqlite = new Database("data.db");
sqlite.pragma("journal_mode = WAL");
export const db = drizzle(sqlite);

// create tables (idempotent) — SQLite DDL mirrored from shared/schema.ts
sqlite.exec(`
CREATE TABLE IF NOT EXISTS trucks (
  id INTEGER PRIMARY KEY AUTOINCREMENT, vin TEXT NOT NULL UNIQUE, unit_no TEXT NOT NULL,
  model TEXT NOT NULL, engine TEXT NOT NULL, year INTEGER NOT NULL, customer TEXT NOT NULL,
  home_center TEXT NOT NULL, center_name TEXT NOT NULL, status TEXT NOT NULL,
  odometer_km INTEGER NOT NULL, engine_hours INTEGER NOT NULL, telematics TEXT NOT NULL,
  health_score INTEGER NOT NULL, lat REAL NOT NULL, lng REAL NOT NULL);
CREATE TABLE IF NOT EXISTS telemetry (
  id INTEGER PRIMARY KEY AUTOINCREMENT, truck_id INTEGER NOT NULL, captured_at TEXT NOT NULL,
  speed_kph REAL NOT NULL, rpm INTEGER NOT NULL, coolant_c REAL NOT NULL, oil_psi REAL NOT NULL,
  fuel_pct REAL NOT NULL, def_pct REAL NOT NULL, battery_v REAL NOT NULL, soc_pct REAL,
  brake_wear_pct REAL NOT NULL, tire_psi_avg REAL NOT NULL, fault_count INTEGER NOT NULL,
  regen_pct REAL NOT NULL, ambient_c REAL NOT NULL);
CREATE TABLE IF NOT EXISTS sensor_map (
  id INTEGER PRIMARY KEY AUTOINCREMENT, channel TEXT NOT NULL, source_system TEXT NOT NULL,
  physical_sensor TEXT NOT NULL, j1939_spn TEXT NOT NULL, twin_node TEXT NOT NULL,
  twin_field TEXT NOT NULL, unit TEXT NOT NULL, hz REAL NOT NULL, status TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS parts (
  id INTEGER PRIMARY KEY AUTOINCREMENT, matnr TEXT NOT NULL, maktx TEXT NOT NULL, maktx_fr TEXT NOT NULL,
  manufacturer TEXT NOT NULL, mfr_part_number TEXT NOT NULL, matkl TEXT NOT NULL, ved_class TEXT NOT NULL,
  fsn_class TEXT NOT NULL, werks TEXT NOT NULL, center_name TEXT NOT NULL, labst INTEGER NOT NULL,
  umlme INTEGER NOT NULL, minbe INTEGER NOT NULL, eisbe INTEGER NOT NULL, plifz INTEGER NOT NULL,
  bin TEXT NOT NULL, unit_price REAL NOT NULL, days_of_supply INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS alerts (
  id INTEGER PRIMARY KEY AUTOINCREMENT, truck_id INTEGER NOT NULL, raised_at TEXT NOT NULL,
  severity TEXT NOT NULL, system TEXT NOT NULL, title TEXT NOT NULL, detail TEXT NOT NULL,
  j1939_spn TEXT NOT NULL, predicted_failure_days INTEGER NOT NULL, confidence_pct INTEGER NOT NULL,
  matnr TEXT, part_name TEXT, parts_in_stock INTEGER, parts_hub_stock INTEGER, status TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS offers (
  id INTEGER PRIMARY KEY AUTOINCREMENT, alert_id INTEGER NOT NULL, truck_id INTEGER NOT NULL,
  created_at TEXT NOT NULL, customer TEXT NOT NULL, contact_name TEXT NOT NULL, channel TEXT NOT NULL,
  bay_center TEXT NOT NULL, slot_start TEXT NOT NULL, slot_end TEXT NOT NULL,
  downtime_saved_hrs REAL NOT NULL, bay_util_gain_pct INTEGER NOT NULL, message TEXT NOT NULL,
  state TEXT NOT NULL);
`);

export const storage = {
  getTrucks: (): Truck[] => db.select().from(trucks).all(),
  getLatestTelemetry: (): Telemetry[] => db.select().from(telemetry).all(),
  getSensorMap: (): SensorMap[] => db.select().from(sensorMap).all(),
  getParts: (): Part[] => db.select().from(parts).all(),
  getAlerts: (): Alert[] => db.select().from(alerts).orderBy(desc(alerts.severity)).all(),
  getOffers: (): Offer[] => db.select().from(offers).orderBy(desc(offers.id)).all(),

  getFleet(): FleetRow[] {
    const tks = this.getTrucks();
    const tel = this.getLatestTelemetry();
    const als = this.getAlerts();
    return tks.map((t) => ({
      ...t,
      latest: tel.find((x) => x.truckId === t.id) ?? null,
      openAlerts: als.filter((a) => a.truckId === t.id && a.status !== "cleared").length,
    }));
  },

  createOffer(o: InsertOffer): Offer {
    const row = db.insert(offers).values(o).returning().get();
    db.update(alerts).set({ status: "offered" }).where(eq(alerts.id, o.alertId)).run();
    return row;
  },

  updateOfferState(id: number, state: string): Offer | undefined {
    return db.update(offers).set({ state }).where(eq(offers.id, id)).returning().get();
  },
};

// seed once on cold start
if (db.select().from(trucks).all().length === 0) {
  seedAll(db);
}
