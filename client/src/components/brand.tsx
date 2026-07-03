// EVE Glyph twin mark — geometric "digital stem cell" node linking physical (filled)
// to digital (ring) across a signal axis. Works at 24px and 200px.
export function TwinMark({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" fill="none" aria-label="Hawkins Twin Platform">
      <rect x="1" y="1" width="30" height="30" rx="7" className="stroke-primary" strokeWidth="1.5" />
      <circle cx="11" cy="16" r="4.2" className="fill-primary" />
      <circle cx="21" cy="16" r="4.2" fill="none" className="stroke-foreground" strokeWidth="1.6" />
      <path d="M11 16 H21" className="stroke-foreground" strokeWidth="1.6" strokeDasharray="1.5 1.8" />
    </svg>
  );
}

const sev: Record<string, string> = {
  critical: "bg-primary/15 text-primary border-primary/30",
  warning: "bg-[hsl(38_92%_48%/0.15)] text-[hsl(38_92%_38%)] dark:text-[hsl(38_95%_62%)] border-[hsl(38_92%_48%/0.3)]",
  watch: "bg-[hsl(199_89%_42%/0.15)] text-[hsl(199_89%_36%)] dark:text-[hsl(199_90%_62%)] border-[hsl(199_89%_42%/0.3)]",
};
export function SeverityBadge({ level }: { level: string }) {
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full border px-2 py-0.5 text-xs font-semibold capitalize ${sev[level] ?? sev.watch}`}>
      <span className="h-1.5 w-1.5 rounded-full bg-current" />
      {level}
    </span>
  );
}

export function StatusDot({ status }: { status: string }) {
  const c =
    status === "active" ? "bg-[hsl(142_62%_45%)]"
    : status === "idle" ? "bg-[hsl(38_92%_50%)]"
    : status === "in_service" ? "bg-primary"
    : "bg-muted-foreground";
  return <span className={`inline-block h-2 w-2 rounded-full ${c}`} title={status} />;
}

export function HealthBar({ score }: { score: number }) {
  const c = score >= 75 ? "hsl(142 62% 45%)" : score >= 55 ? "hsl(38 92% 50%)" : "hsl(4 78% 55%)";
  return (
    <div className="flex items-center gap-2">
      <div className="h-1.5 w-14 overflow-hidden rounded-full bg-muted">
        <div className="h-full rounded-full" style={{ width: `${score}%`, background: c }} />
      </div>
      <span className="tnum text-xs font-semibold" style={{ color: c }}>{score}</span>
    </div>
  );
}
