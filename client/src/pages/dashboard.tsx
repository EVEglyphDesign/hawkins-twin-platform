import { useMemo, useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { apiRequest, queryClient } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";
import { useTheme, formatKm, timeAgo } from "@/lib/theme";
import { TwinMark, SeverityBadge, StatusDot, HealthBar } from "@/components/brand";
import type { FleetRow, SensorMap, Part, Alert, Offer, Canon } from "@/lib/types";
import {
  Activity, AlertTriangle, Truck, Gauge, PackageSearch, MoonStar, ShieldCheck,
  Sun, Moon, ArrowUpDown, Github, GitFork, Zap, Radio, ChevronRight,
} from "lucide-react";
import {
  ResponsiveContainer, AreaChart, Area, BarChart, Bar, XAxis, YAxis, Tooltip, Cell,
} from "recharts";

const NAV = [
  { id: "overview", label: "Fleet Overview", icon: Gauge },
  { id: "telemetry", label: "Live Telemetry", icon: Activity },
  { id: "alerts", label: "Predictive Alerts", icon: AlertTriangle },
  { id: "sensors", label: "Sensor → Twin Map", icon: Radio },
  { id: "parts", label: "Parts Inventory", icon: PackageSearch },
  { id: "offers", label: "Overnight Betterment", icon: MoonStar },
  { id: "sovereignty", label: "Fork · Host · Fund", icon: ShieldCheck },
];

function scrollTo(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
}

export default function Dashboard() {
  const { theme, toggle } = useTheme();
  const { data: fleet = [] } = useQuery<FleetRow[]>({ queryKey: ["/api/fleet"] });
  const { data: sensors = [] } = useQuery<SensorMap[]>({ queryKey: ["/api/sensor-map"] });
  const { data: parts = [] } = useQuery<Part[]>({ queryKey: ["/api/parts"] });
  const { data: alerts = [] } = useQuery<Alert[]>({ queryKey: ["/api/alerts"] });
  const { data: offers = [] } = useQuery<Offer[]>({ queryKey: ["/api/offers"] });
  const { data: canon } = useQuery<Canon>({ queryKey: ["/api/canon"] });

  return (
    <div className="flex h-[100dvh] overflow-hidden bg-background text-foreground">
      {/* Sidebar */}
      <aside className="hidden w-60 shrink-0 flex-col border-r border-sidebar-border bg-sidebar text-sidebar-foreground md:flex">
        <div className="flex items-center gap-2.5 border-b border-sidebar-border px-5 py-4">
          <TwinMark size={30} />
          <div className="leading-tight">
            <div className="text-sm font-bold text-white">Hawkins Twin</div>
            <div className="text-xs text-sidebar-foreground/70">Peterbilt · Atlantic</div>
          </div>
        </div>
        <nav className="flex-1 space-y-1 p-3">
          {NAV.map((n) => (
            <button
              key={n.id}
              data-testid={`nav-${n.id}`}
              onClick={() => scrollTo(n.id)}
              className="flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-sidebar-foreground/80 hover-elevate"
            >
              <n.icon className="h-4 w-4 shrink-0" />
              {n.label}
            </button>
          ))}
        </nav>
        <div className="border-t border-sidebar-border p-3">
          <a
            href={`https://github.com/${canon?.repo ?? "EVEglyphDesign/hawkins-twin-platform"}`}
            target="_blank" rel="noreferrer"
            data-testid="link-repo"
            className="flex items-center gap-2 rounded-md px-3 py-2 text-xs text-sidebar-foreground/70 hover-elevate"
          >
            <Github className="h-3.5 w-3.5" /> View repository
          </a>
          <p className="px-3 pt-2 text-xs italic text-sidebar-foreground/50">{canon?.motto}</p>
        </div>
      </aside>

      {/* Main scroll region */}
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header theme={theme} toggle={toggle} canon={canon} />
        <main className="flex-1 overflow-y-auto overscroll-contain">
          <div className="mx-auto max-w-[1400px] space-y-12 px-5 py-6 md:px-8">
            <StageBanner canon={canon} />
            <Overview fleet={fleet} alerts={alerts} offers={offers} />
            <Telemetry fleet={fleet} />
            <Alerts alerts={alerts} fleet={fleet} parts={parts} offers={offers} />
            <Sensors sensors={sensors} />
            <Parts parts={parts} />
            <Offers offers={offers} />
            <Sovereignty canon={canon} offers={offers} />
            <Footer canon={canon} />
          </div>
        </main>
      </div>
    </div>
  );
}

function Header({ theme, toggle, canon }: { theme: string; toggle: () => void; canon?: Canon }) {
  return (
    <header className="sticky top-0 z-20 flex items-center justify-between border-b border-border bg-background/85 px-5 py-3 backdrop-blur md:px-8">
      <div className="flex items-center gap-3">
        <div className="md:hidden"><TwinMark size={26} /></div>
        <div>
          <h1 className="text-lg font-bold tracking-tight">Peterbilt Digital Twin</h1>
          <p className="hidden text-xs text-muted-foreground sm:block">
            Sovereign fleet mirror · live telemetry → predictive → parts → betterment
          </p>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <span className="hidden items-center gap-1.5 rounded-full border border-[hsl(142_62%_45%/0.4)] bg-[hsl(142_62%_45%/0.12)] px-2.5 py-1 text-xs font-semibold text-[hsl(142_62%_38%)] dark:text-[hsl(142_62%_55%)] sm:inline-flex">
          <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-[hsl(142_62%_50%)]" /> Feed live
        </span>
        <button data-testid="button-theme" onClick={toggle} aria-label="Toggle theme"
          className="rounded-md border border-border p-2 hover-elevate">
          {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </button>
      </div>
    </header>
  );
}

function StageBanner({ canon }: { canon?: Canon }) {
  if (!canon) return null;
  return (
    <div className="flex flex-col gap-2 rounded-lg border border-[hsl(38_92%_48%/0.4)] bg-[hsl(38_92%_48%/0.08)] px-4 py-3 sm:flex-row sm:items-center sm:gap-4">
      <span className="inline-flex w-fit items-center gap-1.5 rounded-full bg-[hsl(38_92%_48%)] px-2.5 py-1 text-xs font-bold uppercase tracking-wide text-black">
        <Zap className="h-3.5 w-3.5" /> Stage · {canon.stage}
      </span>
      <p className="text-sm text-foreground/80">{canon.stageNote}</p>
    </div>
  );
}

function Section({ id, icon: Icon, title, desc, children }: any) {
  return (
    <section id={id} className="scroll-mt-20">
      <div className="mb-4 flex items-start gap-3">
        <div className="mt-0.5 rounded-md bg-primary/10 p-2 text-primary"><Icon className="h-4.5 w-4.5" /></div>
        <div>
          <h2 className="text-base font-bold tracking-tight sm:text-lg">{title}</h2>
          {desc && <p className="text-sm text-muted-foreground">{desc}</p>}
        </div>
      </div>
      {children}
    </section>
  );
}

// ---------- OVERVIEW ----------
function Kpi({ label, value, sub, accent }: any) {
  return (
    <div className="rounded-lg border border-card-border bg-card p-4">
      <div className="text-xs font-medium uppercase tracking-wide text-muted-foreground">{label}</div>
      <div className="tnum mt-1 text-xl font-bold" style={accent ? { color: accent } : undefined}>{value}</div>
      {sub && <div className="mt-0.5 text-xs text-muted-foreground">{sub}</div>}
    </div>
  );
}
function Overview({ fleet, alerts, offers }: { fleet: FleetRow[]; alerts: Alert[]; offers: Offer[] }) {
  const active = fleet.filter((f) => f.status === "active").length;
  const avgHealth = fleet.length ? Math.round(fleet.reduce((s, f) => s + f.healthScore, 0) / fleet.length) : 0;
  const critical = alerts.filter((a) => a.severity === "critical" && a.status !== "cleared").length;
  const savedHrs = offers.reduce((s, o) => s + o.downtimeSavedHrs, 0);
  const health = fleet.map((f) => ({ name: f.unitNo, v: f.healthScore }));
  return (
    <Section id="overview" icon={Gauge} title="Fleet Overview"
      desc="Are we on track? Nine-centre Peterbilt Atlantic fleet at a glance.">
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-5">
        <Kpi label="Units twinned" value={fleet.length} sub="across 9 centres" />
        <Kpi label="Active now" value={active} sub={`${fleet.length - active} idle / off shift`} accent="hsl(142 62% 45%)" />
        <Kpi label="Fleet health" value={`${avgHealth}%`} sub="composite score" accent={avgHealth >= 70 ? "hsl(142 62% 45%)" : "hsl(38 92% 50%)"} />
        <Kpi label="Critical alerts" value={critical} sub="need review" accent={critical ? "hsl(4 78% 55%)" : undefined} />
        <Kpi label="Downtime saved" value={`${savedHrs.toFixed(0)}h`} sub="via betterment offers" accent="hsl(199 89% 50%)" />
      </div>
      <div className="mt-4 rounded-lg border border-card-border bg-card p-4">
        <div className="mb-3 text-sm font-semibold">Health score by unit</div>
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={health} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
            <XAxis dataKey="name" tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))" }} interval={0} angle={-40} textAnchor="end" height={44} />
            <YAxis domain={[0, 100]} tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))" }} />
            <Tooltip contentStyle={tooltip} cursor={{ fill: "hsl(var(--muted)/0.4)" }} />
            <Bar dataKey="v" radius={[3, 3, 0, 0]}>
              {health.map((h, i) => (
                <Cell key={i} fill={h.v >= 75 ? "hsl(142 62% 45%)" : h.v >= 55 ? "hsl(38 92% 50%)" : "hsl(4 78% 55%)"} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Section>
  );
}

const tooltip = {
  background: "hsl(var(--popover))", border: "1px solid hsl(var(--border))",
  borderRadius: 8, fontSize: 12, color: "hsl(var(--popover-foreground))",
};

// ---------- TELEMETRY (sortable) ----------
type SortKey = "unitNo" | "model" | "healthScore" | "speedKph" | "coolantC" | "oilPsi" | "defPct" | "brakeWearPct" | "openAlerts";
function Telemetry({ fleet }: { fleet: FleetRow[] }) {
  const [sort, setSort] = useState<{ k: SortKey; dir: 1 | -1 }>({ k: "healthScore", dir: 1 });
  const [q, setQ] = useState("");
  const rows = useMemo(() => {
    const val = (f: FleetRow, k: SortKey): number | string => {
      if (k === "unitNo" || k === "model") return f[k];
      if (k === "healthScore" || k === "openAlerts") return f[k];
      return (f.latest as any)?.[k] ?? -1;
    };
    return [...fleet]
      .filter((f) => `${f.unitNo} ${f.model} ${f.customer} ${f.vin}`.toLowerCase().includes(q.toLowerCase()))
      .sort((a, b) => {
        const va = val(a, sort.k), vb = val(b, sort.k);
        if (typeof va === "string") return va.localeCompare(vb as string) * sort.dir;
        return ((va as number) - (vb as number)) * sort.dir;
      });
  }, [fleet, sort, q]);
  const th = (k: SortKey, label: string, right = false) => (
    <th className="whitespace-nowrap px-3 py-2 font-semibold">
      <button data-testid={`sort-${k}`} onClick={() => setSort((s) => ({ k, dir: s.k === k ? (s.dir * -1) as 1 | -1 : 1 }))}
        className={`inline-flex w-full items-center gap-1 hover:text-foreground ${right ? "justify-end" : "justify-start"} ${sort.k === k ? "text-foreground" : "text-muted-foreground"}`}>
        {label} <ArrowUpDown className="h-3 w-3" />
      </button>
    </th>
  );
  return (
    <Section id="telemetry" icon={Activity} title="Live Telemetry"
      desc="Latest sensor snapshot per unit. Click any column to sort.">
      <div className="mb-3">
        <input data-testid="input-search" value={q} onChange={(e) => setQ(e.target.value)}
          placeholder="Search unit, model, customer, VIN…" type="search"
          className="w-full max-w-sm rounded-md border border-input bg-card px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-ring" />
      </div>
      <div className="overflow-x-auto rounded-lg border border-card-border bg-card">
        <table className="min-w-[880px] text-sm">
          <thead className="border-b border-border bg-muted/40 text-xs">
            <tr>
              {th("unitNo", "Unit")}{th("model", "Model")}{th("healthScore", "Health")}
              {th("speedKph", "Speed", true)}{th("coolantC", "Coolant", true)}
              {th("oilPsi", "Oil", true)}{th("defPct", "DEF", true)}
              {th("brakeWearPct", "Brake wear", true)}{th("openAlerts", "Alerts", true)}
              <th className="px-3 py-2 text-right font-semibold text-muted-foreground">Updated</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((f) => (
              <tr key={f.id} data-testid={`row-truck-${f.id}`} className="border-b border-border/60 last:border-0 hover-elevate">
                <td className="px-3 py-2">
                  <div className="flex items-center gap-2"><StatusDot status={f.status} />
                    <div><div className="font-semibold">{f.unitNo}</div>
                      <div className="text-xs text-muted-foreground">{f.customer}</div></div></div>
                </td>
                <td className="px-3 py-2"><div className="font-medium">{f.model}</div>
                  <div className="text-xs text-muted-foreground">{f.engine}</div></td>
                <td className="px-3 py-2"><HealthBar score={f.healthScore} /></td>
                <td className="tnum px-3 py-2 text-right">{f.latest ? `${f.latest.speedKph.toFixed(0)}` : "—"}</td>
                <td className="tnum px-3 py-2 text-right" style={colorC(f.latest?.coolantC, 100)}>{f.latest ? `${f.latest.coolantC.toFixed(0)}°` : "—"}</td>
                <td className="tnum px-3 py-2 text-right">{f.latest && f.latest.oilPsi > 0 ? `${f.latest.oilPsi.toFixed(0)}` : "—"}</td>
                <td className="tnum px-3 py-2 text-right" style={colorLow(f.latest?.defPct, 15)}>{f.latest && f.latest.defPct > 0 ? `${f.latest.defPct.toFixed(0)}%` : "EV"}</td>
                <td className="tnum px-3 py-2 text-right" style={colorC(f.latest?.brakeWearPct, 70)}>{f.latest ? `${f.latest.brakeWearPct.toFixed(0)}%` : "—"}</td>
                <td className="tnum px-3 py-2 text-right">{f.openAlerts > 0
                  ? <span className="font-semibold text-primary">{f.openAlerts}</span> : "0"}</td>
                <td className="whitespace-nowrap px-3 py-2 text-right text-xs text-muted-foreground">{f.latest ? timeAgo(f.latest.capturedAt) : "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Section>
  );
}
const colorC = (v: number | undefined, hi: number) => v != null && v >= hi ? { color: "hsl(4 78% 55%)", fontWeight: 600 } : undefined;
const colorLow = (v: number | undefined, lo: number) => v != null && v > 0 && v <= lo ? { color: "hsl(4 78% 55%)", fontWeight: 600 } : undefined;

// ---------- ALERTS + offer generation ----------
function Alerts({ alerts, fleet, parts, offers }: { alerts: Alert[]; fleet: FleetRow[]; parts: Part[]; offers: Offer[] }) {
  const { toast } = useToast();
  const byId = (id: number) => fleet.find((f) => f.id === id);
  const order: Record<string, number> = { critical: 0, warning: 1, watch: 2 };
  const sorted = [...alerts].sort((a, b) => order[a.severity] - order[b.severity] || a.predictedFailureDays - b.predictedFailureDays);

  const create = useMutation({
    mutationFn: async (a: Alert) => {
      const t = byId(a.truckId)!;
      const start = new Date(); start.setHours(23, 0, 0, 0);
      const end = new Date(start); end.setHours(start.getHours() + 4);
      const body = {
        alertId: a.id, truckId: a.truckId, createdAt: new Date().toISOString(),
        customer: t.customer, contactName: "Fleet contact", channel: "Prokeep",
        bayCenter: t.centerName, slotStart: start.toISOString(), slotEnd: end.toISOString(),
        downtimeSavedHrs: 8 + a.predictedFailureDays * 0.5,
        bayUtilGainPct: 6 + (a.confidencePct % 10),
        message: draftOffer(a, t),
        state: "draft",
      };
      return (await apiRequest("POST", "/api/offers", body)).json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/offers"] });
      queryClient.invalidateQueries({ queryKey: ["/api/alerts"] });
      toast({ title: "Overnight offer drafted", description: "Queued in Overnight Betterment for review." });
      setTimeout(() => scrollTo("offers"), 350);
    },
  });
  const hasOffer = (id: number) => offers.some((o) => o.alertId === id);

  return (
    <Section id="alerts" icon={AlertTriangle} title="Predictive Maintenance Alerts"
      desc="Faults predicted from telemetry, each linked to the exact SAP part and network stock.">
      <div className="grid gap-3 lg:grid-cols-2">
        {sorted.map((a) => {
          const t = byId(a.truckId);
          const inStock = (a.partsInStock ?? 0) > 0;
          return (
            <div key={a.id} data-testid={`alert-${a.id}`} className="rounded-lg border border-card-border bg-card p-4">
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2"><SeverityBadge level={a.severity} />
                  <span className="text-xs font-medium text-muted-foreground">{a.system}</span></div>
                <span className="tnum text-xs text-muted-foreground">{a.j1939Spn}</span>
              </div>
              <div className="mt-2 font-semibold">{a.title}</div>
              <div className="mt-0.5 text-sm text-muted-foreground">{a.detail}</div>
              <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs">
                <span className="text-muted-foreground">Unit <b className="text-foreground">{t?.unitNo}</b> · {t?.centerName}</span>
                <span className="text-muted-foreground">Predicted fail <b className="tnum text-primary">{a.predictedFailureDays}d</b></span>
                <span className="text-muted-foreground">Confidence <b className="tnum text-foreground">{a.confidencePct}%</b></span>
              </div>
              {a.matnr && (
                <div className="mt-3 flex flex-wrap items-center justify-between gap-2 rounded-md border border-border bg-muted/40 p-2.5">
                  <div className="text-xs">
                    <div className="font-mono font-semibold text-foreground">{a.matnr}</div>
                    <div className="text-muted-foreground">{a.partName}</div>
                  </div>
                  <div className="text-right text-xs">
                    <div className={inStock ? "font-semibold text-[hsl(142_62%_38%)] dark:text-[hsl(142_62%_55%)]" : "font-semibold text-primary"}>
                      {inStock ? `${a.partsInStock} at home centre` : "0 at home centre"}
                    </div>
                    <div className="tnum text-muted-foreground">{a.partsHubStock} in network</div>
                  </div>
                </div>
              )}
              <button data-testid={`button-offer-${a.id}`} disabled={hasOffer(a.id) || create.isPending}
                onClick={() => create.mutate(a)}
                className="mt-3 inline-flex w-full items-center justify-center gap-2 rounded-md bg-primary px-3 py-2 text-sm font-semibold text-primary-foreground hover-elevate disabled:opacity-50">
                <MoonStar className="h-4 w-4" />
                {hasOffer(a.id) ? "Overnight offer queued" : "Draft overnight repair offer"}
              </button>
            </div>
          );
        })}
      </div>
    </Section>
  );
}

function draftOffer(a: Alert, t: FleetRow) {
  return `Bonjour / Hi ${t.customer},

Our Peterbilt Atlantic twin flagged your unit ${t.unitNo} (${t.model}, VIN …${t.vin.slice(-6)}): ${a.title.toLowerCase()} — predicted within ~${a.predictedFailureDays} days (${a.confidencePct}% confidence, ${a.j1939Spn}).

We can fix it overnight without pulling the truck from a revenue shift. The ${t.centerName} bay is open off-hours and the part (${a.matnr} — ${a.partName}) is staged. Proposed window: tonight 23:00–03:00.

You keep your daytime miles; we recover value from an idle bay. Reply to confirm and we'll hold the slot.

— Peterbilt Atlantic Service · Hawkins Twin Platform`;
}

// ---------- SENSOR MAP ----------
function Sensors({ sensors }: { sensors: SensorMap[] }) {
  const groups = ["SmartLINQ", "PACCAR Solutions", "FleetRight"];
  return (
    <Section id="sensors" icon={Radio} title="Sensor → Digital Model Mapping"
      desc="How each physical sensor channel on the Peterbilt asset binds to a node in the digital twin.">
      <div className="mb-4 flex flex-wrap gap-2">
        {groups.map((g) => (
          <span key={g} className="rounded-full border border-border bg-card px-3 py-1 text-xs font-medium">
            {g} · {sensors.filter((s) => s.sourceSystem === g).length} channels
          </span>
        ))}
      </div>
      <div className="overflow-x-auto rounded-lg border border-card-border bg-card">
        <table className="min-w-[900px] text-sm">
          <thead className="border-b border-border bg-muted/40 text-xs text-muted-foreground">
            <tr>
              <th className="px-3 py-2 text-left font-semibold">Physical sensor</th>
              <th className="px-3 py-2 text-left font-semibold">Source</th>
              <th className="px-3 py-2 text-left font-semibold">J1939 / channel</th>
              <th className="px-3 py-2 text-left font-semibold">Digital-model node</th>
              <th className="px-3 py-2 text-right font-semibold">Rate</th>
              <th className="px-3 py-2 text-left font-semibold">Status</th>
            </tr>
          </thead>
          <tbody>
            {sensors.map((s) => (
              <tr key={s.id} data-testid={`sensor-${s.id}`} className="border-b border-border/60 last:border-0 hover-elevate">
                <td className="px-3 py-2 font-medium">{s.physicalSensor}<div className="text-xs text-muted-foreground">{s.unit}</div></td>
                <td className="px-3 py-2"><span className="rounded border border-border px-1.5 py-0.5 text-xs">{s.sourceSystem}</span></td>
                <td className="tnum px-3 py-2 font-mono text-xs">{s.j1939Spn}<div className="text-muted-foreground">{s.channel}</div></td>
                <td className="px-3 py-2">
                  <div className="flex items-center gap-1.5 font-mono text-xs text-primary">
                    <ChevronRight className="h-3 w-3" />{s.twinNode}
                  </div>
                  <div className="text-xs text-muted-foreground">→ telemetry.{s.twinField}</div>
                </td>
                <td className="tnum px-3 py-2 text-right text-xs">{s.hz} Hz</td>
                <td className="px-3 py-2">
                  <span className={`inline-flex items-center gap-1.5 text-xs font-medium ${s.status === "live" ? "text-[hsl(142_62%_38%)] dark:text-[hsl(142_62%_55%)]" : "text-[hsl(38_92%_45%)]"}`}>
                    <span className={`h-1.5 w-1.5 rounded-full ${s.status === "live" ? "bg-[hsl(142_62%_50%)] animate-pulse" : "bg-[hsl(38_92%_50%)]"}`} />
                    {s.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Section>
  );
}

// ---------- PARTS ----------
function Parts({ parts }: { parts: Part[] }) {
  const [center, setCenter] = useState("all");
  const centers = Array.from(new Set(parts.map((p) => `${p.werks}|${p.centerName}`)));
  const rows = parts.filter((p) => center === "all" || p.werks === center);
  return (
    <Section id="parts" icon={PackageSearch} title="Parts Inventory · SAP Twin"
      desc="Dealer-owned MARA/MARC/MARD mirror across the nine centres. Predicted faults pull straight from here.">
      <div className="mb-3 flex flex-wrap items-center gap-2">
        <button data-testid="center-all" onClick={() => setCenter("all")}
          className={`rounded-full border px-3 py-1 text-xs font-medium hover-elevate ${center === "all" ? "border-primary bg-primary/10 text-primary" : "border-border"}`}>
          All centres
        </button>
        {centers.map((c) => {
          const [w, name] = c.split("|");
          return (
            <button key={w} data-testid={`center-${w}`} onClick={() => setCenter(w)}
              className={`rounded-full border px-3 py-1 text-xs font-medium hover-elevate ${center === w ? "border-primary bg-primary/10 text-primary" : "border-border"}`}>
              {w} · {name.split(",")[0]}
            </button>
          );
        })}
      </div>
      <div className="overflow-x-auto rounded-lg border border-card-border bg-card">
        <table className="min-w-[900px] text-sm">
          <thead className="border-b border-border bg-muted/40 text-xs text-muted-foreground">
            <tr>
              <th className="px-3 py-2 text-left font-semibold">Material (MATNR)</th>
              <th className="px-3 py-2 text-left font-semibold">Centre · bin</th>
              <th className="px-3 py-2 text-left font-semibold">Class</th>
              <th className="px-3 py-2 text-right font-semibold">On hand</th>
              <th className="px-3 py-2 text-right font-semibold">Reorder</th>
              <th className="px-3 py-2 text-right font-semibold">Lead</th>
              <th className="px-3 py-2 text-right font-semibold">Unit price</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((p) => {
              const low = p.labst <= p.minbe;
              return (
                <tr key={p.id} data-testid={`part-${p.id}`} className="border-b border-border/60 last:border-0 hover-elevate">
                  <td className="px-3 py-2">
                    <div className="font-mono text-xs font-semibold">{p.matnr}</div>
                    <div className="text-xs text-muted-foreground">{p.maktx}</div>
                    <div className="text-xs italic text-muted-foreground/70">{p.manufacturer} · {p.mfrPartNumber}</div>
                  </td>
                  <td className="px-3 py-2 text-xs">{p.werks}<div className="text-muted-foreground">{p.centerName.split(",")[0]} · {p.bin}</div></td>
                  <td className="px-3 py-2">
                    <span className="rounded border border-border px-1.5 py-0.5 font-mono text-xs" title="V/E/D criticality · F/S/N velocity">{p.vedClass}/{p.fsnClass}</span>
                  </td>
                  <td className="tnum px-3 py-2 text-right">
                    <span className={low ? "font-bold text-primary" : "font-semibold"}>{p.labst}</span>
                    {p.umlme > 0 && <span className="text-xs text-[hsl(199_89%_50%)]"> +{p.umlme}⇄</span>}
                  </td>
                  <td className="tnum px-3 py-2 text-right text-muted-foreground">{p.minbe}</td>
                  <td className="tnum px-3 py-2 text-right text-muted-foreground">{p.plifz}d</td>
                  <td className="tnum px-3 py-2 text-right">${p.unitPrice.toLocaleString()}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <p className="mt-2 text-xs text-muted-foreground">
        Legend: on-hand in red = at/below reorder point · <span className="text-[hsl(199_89%_50%)]">⇄</span> = stock in transit ·
        V/E/D = criticality, F/S/N = movement velocity (SAP spare-parts classes).
      </p>
    </Section>
  );
}

// ---------- OFFERS ----------
function Offers({ offers }: { offers: Offer[] }) {
  const { toast } = useToast();
  const send = useMutation({
    mutationFn: async ({ id, state }: { id: number; state: string }) =>
      (await apiRequest("PATCH", `/api/offers/${id}`, { state })).json(),
    onSuccess: (_d, v) => {
      queryClient.invalidateQueries({ queryKey: ["/api/offers"] });
      toast({ title: v.state === "sent" ? "Offer sent (logged)" : `Marked ${v.state}`, description: "Simulated — no message left the twin." });
    },
  });
  const totalSaved = offers.reduce((s, o) => s + o.downtimeSavedHrs, 0);
  const avgUtil = offers.length ? Math.round(offers.reduce((s, o) => s + o.bayUtilGainPct, 0) / offers.length) : 0;
  return (
    <Section id="offers" icon={MoonStar} title="Overnight Betterment — Off-Hours Repair Offers"
      desc="Idle bays overnight are dormant capital. Booking predicted repairs into off-hours recovers that value — betterment.">
      <div className="mb-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <Kpi label="Offers drafted" value={offers.length} />
        <Kpi label="Sent" value={offers.filter((o) => o.state !== "draft").length} accent="hsl(199 89% 50%)" />
        <Kpi label="Downtime recovered" value={`${totalSaved.toFixed(0)}h`} sub="customer uptime" accent="hsl(142 62% 45%)" />
        <Kpi label="Avg bay-util gain" value={`${avgUtil}%`} sub="off-hours utilization" accent="hsl(38 92% 50%)" />
      </div>
      {offers.length === 0 ? (
        <div className="rounded-lg border border-dashed border-border bg-card p-8 text-center">
          <MoonStar className="mx-auto h-8 w-8 text-muted-foreground/50" />
          <p className="mt-2 text-sm font-medium">No offers yet</p>
          <p className="text-xs text-muted-foreground">Draft one from a predictive alert above to populate the queue.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {offers.map((o) => (
            <div key={o.id} data-testid={`offer-${o.id}`} className="rounded-lg border border-card-border bg-card p-4">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold">{o.customer}</span>
                    <span className={`rounded-full border px-2 py-0.5 text-xs font-semibold capitalize ${stateColor(o.state)}`}>{o.state}</span>
                  </div>
                  <div className="mt-0.5 text-xs text-muted-foreground">
                    {o.bayCenter} · {new Date(o.slotStart).toLocaleTimeString("en-CA", { hour: "2-digit", minute: "2-digit" })}–
                    {new Date(o.slotEnd).toLocaleTimeString("en-CA", { hour: "2-digit", minute: "2-digit" })} · via {o.channel}
                  </div>
                </div>
                <div className="flex gap-4 text-right text-xs">
                  <div><div className="tnum text-sm font-bold text-[hsl(142_62%_38%)] dark:text-[hsl(142_62%_55%)]">{o.downtimeSavedHrs.toFixed(1)}h</div><div className="text-muted-foreground">uptime kept</div></div>
                  <div><div className="tnum text-sm font-bold text-[hsl(38_92%_45%)]">+{o.bayUtilGainPct}%</div><div className="text-muted-foreground">bay util</div></div>
                </div>
              </div>
              <pre className="mt-3 whitespace-pre-wrap rounded-md border border-border bg-muted/40 p-3 font-sans text-xs text-foreground/85">{o.message}</pre>
              <div className="mt-3 flex flex-wrap gap-2">
                <button data-testid={`send-${o.id}`} disabled={o.state !== "draft" || send.isPending}
                  onClick={() => send.mutate({ id: o.id, state: "sent" })}
                  className="inline-flex items-center gap-1.5 rounded-md bg-primary px-3 py-1.5 text-xs font-semibold text-primary-foreground hover-elevate disabled:opacity-50">
                  Send offer
                </button>
                <button data-testid={`accept-${o.id}`} disabled={o.state === "accepted"}
                  onClick={() => send.mutate({ id: o.id, state: "accepted" })}
                  className="rounded-md border border-border px-3 py-1.5 text-xs font-medium hover-elevate disabled:opacity-40">Mark accepted</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </Section>
  );
}
const stateColor = (s: string) =>
  s === "draft" ? "border-border text-muted-foreground"
  : s === "sent" ? "border-[hsl(199_89%_42%/0.4)] bg-[hsl(199_89%_42%/0.12)] text-[hsl(199_89%_42%)]"
  : s === "accepted" ? "border-[hsl(142_62%_45%/0.4)] bg-[hsl(142_62%_45%/0.12)] text-[hsl(142_62%_38%)] dark:text-[hsl(142_62%_55%)]"
  : "border-primary/40 bg-primary/10 text-primary";

// ---------- SOVEREIGNTY / FORK-HOST-FUND ----------
function Sovereignty({ canon, offers }: { canon?: Canon; offers: Offer[] }) {
  const items = [
    { icon: GitFork, title: "Fork", body: "Tim receives a full fork of this twin to commercialize and operate. Public source, MIT-forkable, ARK footer preserved." },
    { icon: Zap, title: "Host", body: "Self-hostable with a documented escape path — no vendor lock-in, inheritor-operable. Runs without EVE, PACCAR-cloud, or any single vendor as a hard dependency." },
    { icon: MoonStar, title: "Fund", body: "Putting the physical sites to work in off-hours turns idle overnight capacity into betterment revenue — the commercial engine that, one way or another, funds EVE Glyph Design R&D." },
  ];
  const operations = [
    { role: "Technical observer", who: "Luke", body: "Understands how to manage every component — access provisioning, maintenance windows, and system health across the twin." },
    { role: "24/7 support", who: "EVE team", body: "The team runs around the clock, so operational support is never far away during and after handover." },
  ];
  const canonPrinciples = [
    "Public stays public — the twin is a lens over data already coming off the trucks, not a vault.",
    "Tokenized history — every commit is a time-stamped, tamper-evident record in the GitHub Merkle ledger.",
    "Cryptographic notarization under the copyright umbrella — the ARK footer is the only visible watermark.",
    "Operator is Apex — Dany Theriault defines the canon; Tim hosts and commercializes; PUDC stewards institutional rights.",
  ];
  return (
    <Section id="sovereignty" icon={ShieldCheck} title="Fork · Host · Fund — Canon & Handover"
      desc="How this twin is governed and handed over, in line with EVE Glyph Design doctrine.">
      <div className="grid gap-3 md:grid-cols-3">
        {items.map((it) => (
          <div key={it.title} className="rounded-lg border border-card-border bg-card p-4">
            <div className="flex items-center gap-2 text-primary"><it.icon className="h-4 w-4" />
              <span className="text-sm font-bold text-foreground">{it.title}</span></div>
            <p className="mt-2 text-sm text-muted-foreground">{it.body}</p>
          </div>
        ))}
      </div>
      <div className="mt-3 grid gap-3 md:grid-cols-2">
        {operations.map((op) => (
          <div key={op.role} className="rounded-lg border border-card-border bg-card p-4" data-testid={`card-ops-${op.role.replace(/\s+/g, "-").toLowerCase()}`}>
            <div className="flex items-center gap-2">
              <span className="rounded-md border border-primary/40 bg-primary/10 px-2 py-0.5 text-[11px] font-semibold uppercase tracking-wide text-primary">{op.role}</span>
              <span className="text-sm font-bold text-foreground">{op.who}</span>
            </div>
            <p className="mt-2 text-sm text-muted-foreground">{op.body}</p>
          </div>
        ))}
      </div>
      <div className="mt-4 grid gap-3 lg:grid-cols-2">
        <div className="rounded-lg border border-card-border bg-card p-4">
          <div className="text-sm font-bold">Canon principles this twin obeys</div>
          <ul className="mt-2 space-y-2">
            {canonPrinciples.map((p, i) => (
              <li key={i} className="flex gap-2 text-sm text-muted-foreground">
                <ShieldCheck className="mt-0.5 h-4 w-4 shrink-0 text-primary" />{p}
              </li>
            ))}
          </ul>
        </div>
        <div className="rounded-lg border border-card-border bg-card p-4">
          <div className="text-sm font-bold">EVE is an R&D tool — read this as a wireframe</div>
          <p className="mt-2 text-sm text-muted-foreground">{canon?.stageNote}</p>
          <div className="mt-3 rounded-md border border-border bg-muted/40 p-3 text-xs text-muted-foreground">
            Escape path: all data is portable JSON via <code className="font-mono text-foreground">/api/*</code> ·
            source is open Markdown + TypeScript · runbooks live in the repo. Migrate the fork to any host without
            losing fidelity.
          </div>
          <a href={`https://github.com/${canon?.repo ?? "EVEglyphDesign/hawkins-twin-platform"}`}
            target="_blank" rel="noreferrer" data-testid="link-sovereignty-repo"
            className="mt-3 inline-flex items-center gap-2 rounded-md border border-border px-3 py-2 text-sm font-medium hover-elevate">
            <Github className="h-4 w-4" /> {canon?.repo}
          </a>
        </div>
      </div>
    </Section>
  );
}

function Footer({ canon }: { canon?: Canon }) {
  return (
    <footer className="border-t border-border pt-5 text-xs leading-relaxed text-muted-foreground">
      <p className="italic">{canon?.motto}</p>
      <p className="mt-2 max-w-4xl">{canon?.footer}</p>
    </footer>
  );
}
