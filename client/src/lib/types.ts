export interface Telemetry {
  id: number; truckId: number; capturedAt: string; speedKph: number; rpm: number;
  coolantC: number; oilPsi: number; fuelPct: number; defPct: number; batteryV: number;
  socPct: number | null; brakeWearPct: number; tirePsiAvg: number; faultCount: number;
  regenPct: number; ambientC: number;
}
export interface FleetRow {
  id: number; vin: string; unitNo: string; model: string; engine: string; year: number;
  customer: string; homeCenter: string; centerName: string; status: string;
  odometerKm: number; engineHours: number; telematics: string; healthScore: number;
  lat: number; lng: number; latest: Telemetry | null; openAlerts: number;
}
export interface SensorMap {
  id: number; channel: string; sourceSystem: string; physicalSensor: string; j1939Spn: string;
  twinNode: string; twinField: string; unit: string; hz: number; status: string;
}
export interface Part {
  id: number; matnr: string; maktx: string; maktxFr: string; manufacturer: string;
  mfrPartNumber: string; matkl: string; vedClass: string; fsnClass: string; werks: string;
  centerName: string; labst: number; umlme: number; minbe: number; eisbe: number;
  plifz: number; bin: string; unitPrice: number; daysOfSupply: number;
}
export interface Alert {
  id: number; truckId: number; raisedAt: string; severity: string; system: string;
  title: string; detail: string; j1939Spn: string; predictedFailureDays: number;
  confidencePct: number; matnr: string | null; partName: string | null;
  partsInStock: number | null; partsHubStock: number | null; status: string;
}
export interface Offer {
  id: number; alertId: number; truckId: number; createdAt: string; customer: string;
  contactName: string; channel: string; bayCenter: string; slotStart: string; slotEnd: string;
  downtimeSavedHrs: number; bayUtilGainPct: number; message: string; state: string;
}
export interface Canon { footer: string; repo: string; motto: string; stage: string; stageNote: string; }
