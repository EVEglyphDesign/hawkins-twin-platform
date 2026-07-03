import type { Express } from "express";
import { createServer } from "node:http";
import type { Server } from "node:http";
import { storage } from "./storage";
import { insertOfferSchema } from "@shared/schema";

export async function registerRoutes(httpServer: Server, app: Express): Promise<Server> {
  app.get("/api/fleet", (_req, res) => res.json(storage.getFleet()));
  app.get("/api/telemetry", (_req, res) => res.json(storage.getLatestTelemetry()));
  app.get("/api/sensor-map", (_req, res) => res.json(storage.getSensorMap()));
  app.get("/api/parts", (_req, res) => res.json(storage.getParts()));
  app.get("/api/alerts", (_req, res) => res.json(storage.getAlerts()));
  app.get("/api/offers", (_req, res) => res.json(storage.getOffers()));

  // canon meta — commit hash + footer for the tokenized-history panel
  app.get("/api/canon", (_req, res) =>
    res.json({
      footer:
        '© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.',
      repo: "EVEglyphDesign/hawkins-twin-platform",
      motto: "Pour le bien-être du peuple.",
      stage: "Wireframe",
      stageNote:
        "Built with EVE, an advanced R&D tool, to wireframe this repository on representative data that mirrors the real SmartLINQ, PACCAR Solutions, FleetRight, and SAP parts shapes. Optimization comes later, after the live systems are connected.",
    }),
  );

  // create an overnight "betterment" offer (draft + send stub)
  app.post("/api/offers", (req, res) => {
    const parsed = insertOfferSchema.safeParse(req.body);
    if (!parsed.success) return res.status(400).json({ error: parsed.error.flatten() });
    res.json(storage.createOffer(parsed.data));
  });

  // send / accept / decline stub — logs state, no real message leaves
  app.patch("/api/offers/:id", (req, res) => {
    const state = String(req.body?.state ?? "");
    if (!["draft", "sent", "accepted", "declined"].includes(state))
      return res.status(400).json({ error: "invalid state" });
    const updated = storage.updateOfferState(Number(req.params.id), state);
    if (!updated) return res.status(404).json({ error: "not found" });
    res.json(updated);
  });

  return httpServer;
}
