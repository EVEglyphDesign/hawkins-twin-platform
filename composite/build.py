import json, datetime, sys
sys.path.insert(0, '/home/user/workspace/hawkins/composite')
from data import DEPTS, ACTIONS

def fmt(v, f):
    if v is None: return "\u2014"
    if f == "pct": return f"{v:,.1f}%"
    if f == "x":   return f"{v:,.1f}\u00d7"
    if f == "mo":  return f"{v:,.2f} mo"
    if f == "days":return f"{v:,.1f} days" if v % 1 else f"{v:,.0f} days"
    if f == "usd":
        if abs(v) >= 1_000_000: return f"${v/1_000_000:,.2f}M"
        if abs(v) >= 1000: return f"${v/1000:,.1f}k"
        return f"${v:,.0f}"
    if f == "ratio": return f"{v:,.2f}:1"
    return f"{v:,.1f}"

rows_by_dept = {}
kpi_pool = {}
below = 0
total = 0
for key, label, items in DEPTS:
    out = []
    for name, formula, f, d, guide, act, avg, best, twin, src in items:
        gap = (act - guide) * d
        ok = gap >= -0.0001
        total += 1
        if not ok: below += 1
        # variance text
        if f == "usd":
            vt = ("" if gap >= 0 else "\u2212") + fmt(abs(gap), "usd")
        elif f in ("pct",):
            vt = f"{gap:+.1f} pts"
        elif f in ("x",):
            vt = f"{gap:+.1f}\u00d7"
        elif f in ("mo", "ratio"):
            vt = f"{gap:+.2f}"
        elif f == "days":
            vt = f"{gap:+.1f} days"
        else:
            vt = f"{gap:+.1f}"
        out.append({
            "name": name, "formula": formula,
            "act": fmt(act, f), "twin": fmt(twin, f) if twin is not None else "",
            "avg": fmt(avg, f), "best": fmt(best, f), "guide": fmt(guide, f),
            "var": vt, "ok": ok, "live": src == "twin",
            "_raw": (f, d, guide, act, twin),
        })
    rows_by_dept[key] = out
    kpi_pool[key] = (label, out)

KPI = [
    ("Total absorption", "dealership", 0),
    ("Fixed absorption", "dealership", 1),
    ("Net profit return on sales", "dealership", 2),
    ("Parts fill rate \u2014 first time", "parts", 2),
    ("Parts inventory turnover", "parts", 1),
    ("Technician proficiency", "service", 0),
    ("Open repair orders", "service", 8),
    ("Used-truck days' supply", "variable", 3),
]
kpis = []
for label, dept, idx in KPI:
    r = rows_by_dept[dept][idx]
    f, d, guide, act, twin = r["_raw"]
    shown = twin if twin is not None else act
    gap = (shown - guide) * d
    if f == "pct": vt = f"{gap:+.1f} pts"
    elif f == "x": vt = f"{gap:+.1f}\u00d7"
    elif f == "days": vt = f"{gap:+.1f} days"
    elif f in ("mo", "ratio"): vt = f"{gap:+.2f}"
    elif f == "usd": vt = ("" if gap >= 0 else "\u2212") + fmt(abs(gap), "usd")
    else: vt = f"{gap:+.1f}"
    kpis.append({"label": r["name"], "value": r["twin"] or r["act"], "guide": r["guide"],
                 "var": vt, "ok": gap >= -0.0001, "live": r["live"]})

for k in rows_by_dept:
    for r in rows_by_dept[k]: r.pop("_raw")

payload = {
    "tabs": [{"key": k, "label": l, "rows": rows_by_dept[k]} for k, l, _ in DEPTS],
    "kpis": kpis,
    "actions": [{"what": a[0], "lines": a[1], "src": a[2], "effect": a[3], "status": a[4]} for a in ACTIONS],
    "below": below, "total": total,
    "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
}

HTML = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Hawkins composite mock &middot; EVEglyphDesign</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{--cream:#fdfaf4;--cream2:#f7f2e7;--ink:#1a1a1a;--line:#e7e1d3;--mute:#6b665c;--acc:#e87722;--acc2:#b8560f;--good:#2f6b2f}
*{box-sizing:border-box}
body{margin:0;background:var(--cream);color:var(--ink);font-family:Inter,system-ui,sans-serif;font-size:15px;line-height:1.5}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px 70px}
header{border-bottom:1px solid var(--line);background:var(--cream2)}
header .wrap{padding-top:26px;padding-bottom:22px}
.eyebrow{font-size:12px;letter-spacing:.09em;text-transform:uppercase;color:var(--mute);margin:0 0 8px}
h1{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:34px;line-height:1.12;margin:0 0 6px}
h1 span{display:block;font-size:18px;font-weight:500;color:var(--mute);margin-top:6px}
.rule{height:3px;width:64px;background:var(--acc);margin:14px 0 0}
.banner{background:var(--acc);color:var(--cream);padding:11px 22px;font-size:13.5px;font-weight:500}
.banner b{font-weight:600}
h2{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:22px;margin:34px 0 4px}
h3{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:16px;margin:22px 0 6px}
p{margin:8px 0}
.lede{color:var(--mute);max-width:76ch;font-size:14.5px}
a{color:var(--acc2);text-decoration:none;border-bottom:1px solid rgba(184,86,15,.3)}
a:hover{border-bottom-color:var(--acc2)}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0 6px}
.kpi{background:#fff;border:1px solid var(--line);border-radius:6px;padding:13px 14px;min-width:0}
.kpi .k{font-size:11.5px;color:var(--mute);letter-spacing:.02em;min-height:30px}
.kpi .v{font-family:Fraunces,Georgia,serif;font-size:25px;font-weight:600;margin:5px 0 3px;letter-spacing:-.01em}
.kpi .g{font-size:11.5px;color:var(--mute)}
.kpi .d{font-size:12px;font-weight:600;margin-top:5px}
.d.ok{color:var(--good)} .d.no{color:var(--acc2)}
.live{display:inline-block;font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;background:var(--acc);color:var(--cream);border-radius:2px;padding:1px 5px;margin-left:5px;vertical-align:2px}
.tabs{display:flex;flex-wrap:wrap;gap:6px;margin:22px 0 0;border-bottom:1px solid var(--line)}
.tab{appearance:none;border:1px solid var(--line);border-bottom:none;background:var(--cream2);color:var(--mute);font-family:Inter;font-size:13.5px;font-weight:500;padding:9px 15px;border-radius:5px 5px 0 0;cursor:pointer}
.tab[aria-selected="true"]{background:#fff;color:var(--ink);box-shadow:inset 0 3px 0 var(--acc)}
table{width:100%;border-collapse:collapse;margin:0;font-size:13px;background:#fff}
th{background:var(--cream2);text-align:left;font-weight:600;font-size:11.5px;letter-spacing:.03em;text-transform:uppercase;color:var(--mute);padding:9px 10px;border-bottom:1px solid var(--line);white-space:nowrap}
td{padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr:last-child td{border-bottom:none}
.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.nm{font-weight:500}
.fx{display:block;color:var(--mute);font-size:11.5px;margin-top:2px;font-weight:400}
.pill{display:inline-block;font-size:11px;font-weight:600;padding:2px 8px;border-radius:11px;white-space:nowrap}
.pill.ok{background:rgba(47,107,47,.1);color:var(--good)}
.pill.no{background:rgba(232,119,34,.14);color:var(--acc2)}
.tblwrap{border:1px solid var(--line);border-top:none;border-radius:0 0 6px 6px;overflow-x:auto;background:#fff}
.note{background:var(--cream2);border-left:3px solid var(--acc);padding:12px 15px;margin:16px 0;font-size:13.5px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:26px}
ul{margin:8px 0;padding-left:19px}li{margin-bottom:5px}
footer{border-top:1px solid var(--line);margin-top:44px;padding-top:16px;font-size:12px;color:var(--mute)}
@media(max-width:900px){.tblwrap table{min-width:860px}.kpis{grid-template-columns:repeat(2,1fr)}.two{grid-template-columns:1fr}h1{font-size:27px}}
</style></head><body>
<div class="banner"><b>Mock composite \u2014 illustrative only.</b> Line names, formulas and guide values are public ATD figures. Every Hawkins number, group average and best-in-class figure on this page is invented to show the shape of the instrument. Nothing here is Hawkins data.</div>
<header><div class="wrap">
<p class="eyebrow">EVEglyphDesign &middot; Hawkins Twin &middot; Peterbilt Atlantic</p>
<h1>The composite, as the twin would render it<span>A mock 20 Group composite built on public ATD line items, pending Luke's export</span></h1>
<div class="rule"></div>
</div></header>
<div class="wrap">

<p class="lede">This is the shape of the instrument, not the numbers. It is built against the line items and published guides that <a href="https://slideguide.nada.org/ATDSlideGuide.pdf">American Truck Dealers publishes openly in its 2026 Formulas, Definitions and Guides</a>, alongside the <a href="https://www.nada.org/atd/research/atd-data">ATD Data annual financial profile</a> and the <a href="https://www.nada.org/nada/nada-20-group">NADA/ATD 20 Group composite description</a>. When the real ADA composite export lands (HT-01), the same frame is re-cut against its actual line names and Hawkins' actual figures, and this mock is retired.</p>

<div class="note">__BELOW__ of __TOTAL__ mocked line items sit below the published ATD guide. Items carrying a <span class="live">live</span> mark are ones the twin can compute continuously rather than once a month \u2014 that is the whole difference between a composite and a position.</div>

<h2>At a glance</h2>
<div class="kpis" id="kpis"></div>

<h2>Line items</h2>
<p class="lede">Hawkins column reads as the monthly composite would report it. Twin column is the same line recomputed live where the twin has a source. Variance is measured against the ATD guide.</p>
<div class="tabs" id="tabs" role="tablist"></div>
<div class="tblwrap"><table>
<thead><tr>
<th style="width:34%">Line item</th>
<th class="num">Hawkins</th><th class="num">Twin (live)</th>
<th class="num">20 Group avg</th><th class="num">Best in class</th>
<th class="num">ATD guide</th><th class="num">vs guide</th><th></th>
</tr></thead><tbody id="rows"></tbody></table></div>

<h2>Gap, cause and the action queue</h2>
<p class="lede">The composite tells Tim where he is behind. It does not tell him why, and it does not hand anyone a job. That layer is what the twin adds, and every item below is tied to a numbered next step from the 27 July working session.</p>
<div class="tblwrap" style="border-top:1px solid var(--line);border-radius:6px;margin-top:12px"><table>
<thead><tr><th style="width:26%">Move</th><th style="width:24%">Composite lines it touches</th><th style="width:16%">Source</th><th style="width:18%">Projected effect</th><th>Status</th></tr></thead>
<tbody id="acts"></tbody></table></div>

<div class="two">
<div><h3>What this proves</h3><ul>
<li>The twin can speak entirely in Tim's existing vocabulary \u2014 no new metric, no translation in front of peers.</li>
<li>Monthly rear-view becomes a running position on every line the twin has a source for.</li>
<li>Each gap carries a named cause, an owner, and a projected effect rather than a colour.</li>
<li>The same frame drops onto any dealer in the 20 Group, because the line items are the association's, not ours.</li>
</ul></div>
<div><h3>What it does not prove</h3><ul>
<li>No Hawkins data has been touched. Nothing here is measured.</li>
<li>The real composite's line names, groupings and period conventions are unknown until HT-01 lands.</li>
<li>Group average and best-in-class columns are invented; the real ones come from the 20 Group itself.</li>
<li>Projected effects are illustrative arithmetic on synthetic figures, not forecasts.</li>
</ul></div>
</div>

<footer>
<p>Sources for line items, formulas and guides: <a href="https://slideguide.nada.org/ATDSlideGuide.pdf">ATD 2026 Formulas, Definitions and Guides</a> &middot; <a href="https://www.nada.org/atd/research/atd-data">ATD Data annual financial profile</a> &middot; <a href="https://www.nada.org/nada/nada-20-group">NADA 20 Group composite</a>. Companion surfaces: <a href="../demo/">sandbox inventory twin</a> &middot; <a href="../next-steps/EVEglyphDesign_Hawkins_Twin_Next_Steps_Executive_Dashboard.pdf">next-steps register and dashboard specification</a> &middot; <a href="https://github.com/EVEglyphDesign/hawkins-twin-platform">repository</a>.</p>
<p>&copy; 2026 EVEglyphDesign. All rights reserved. Controlled copy. Key ID EgD-KEY-2026-07 &middot; generated __TS__. EVE \u201cdigital stem cell\u201d glyph and glyph-based design principles \u2014 all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council.</p>
<p><i>Pour le bien-\u00eatre du peuple.</i></p>
</footer>
</div>
<script>
const D = __DATA__;
const kw = document.getElementById('kpis');
kw.innerHTML = D.kpis.map(k => `<div class="kpi"><div class="k">${k.label}${k.live?'<span class="live">live</span>':''}</div><div class="v">${k.value}</div><div class="g">guide ${k.guide}</div><div class="d ${k.ok?'ok':'no'}">${k.var} vs guide</div></div>`).join('');
const tw = document.getElementById('tabs'), rw = document.getElementById('rows');
function draw(i){
  [...tw.children].forEach((b,j)=>b.setAttribute('aria-selected', j===i));
  rw.innerHTML = D.tabs[i].rows.map(r => `<tr>
    <td><span class="nm">${r.name}</span><span class="fx">${r.formula}</span></td>
    <td class="num">${r.act}</td>
    <td class="num">${r.twin ? r.twin + '<span class="live">live</span>' : '<span style="color:var(--mute)">\u2014</span>'}</td>
    <td class="num">${r.avg}</td><td class="num">${r.best}</td><td class="num">${r.guide}</td>
    <td class="num" style="color:${r.ok?'var(--good)':'var(--acc2)'};font-weight:600">${r.var}</td>
    <td><span class="pill ${r.ok?'ok':'no'}">${r.ok?'at guide':'below guide'}</span></td></tr>`).join('');
}
tw.innerHTML = D.tabs.map((t,i)=>`<button class="tab" role="tab" aria-selected="${i===0}">${t.label}</button>`).join('');
[...tw.children].forEach((b,i)=>b.addEventListener('click',()=>draw(i)));
draw(0);
document.getElementById('acts').innerHTML = D.actions.map(a=>`<tr>
  <td><span class="nm">${a.what}</span></td><td>${a.lines}</td><td>${a.src}</td><td>${a.effect}</td><td>${a.status}</td></tr>`).join('');
</script></body></html>
"""

html = (HTML.replace("__DATA__", json.dumps(payload))
            .replace("__BELOW__", str(below))
            .replace("__TOTAL__", str(total))
            .replace("__TS__", payload["generated"]))
open('/home/user/workspace/hawkins/composite/index.html', 'w').write(html)
print("wrote", below, "below guide of", total)
