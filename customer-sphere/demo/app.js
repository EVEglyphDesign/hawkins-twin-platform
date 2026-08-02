/* HawkinsTwin Customer Sphere — demonstration surface.
   Screens: worklist, sphere, face, index card, stewardship, structural card, gate, record.
   All state is in memory; reloading resets it. Nothing here writes anywhere. */

const S = {
  view: "tim",
  screen: "home",
  acct: null,
  face: null,
  card: null,
  struct: null,
  dispatched: {},  // acctId -> {at, ref, to}
  parked: {},      // structural id -> true
  merged: {},      // candidate id -> "merged" | "affiliation" | "rejected"
  notes: {}
};

const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const acct = id => ACCOUNTS.find(a => a.id === id);
const struc = id => STRUCTURAL.find(x => x.id === id);
const viewObj = () => VIEWS.find(v => v.id === S.view);
/* account value expressed in millions, from strings like "CAD 1.24M ..." or "CAD 640,000 ..." */
const valNum = a => {
  const m = a.value.match(/([\d,]+(?:\.\d+)?)\s*(M)?/);
  if (!m) return 0;
  const n = parseFloat(m[1].replace(/,/g, ""));
  return m[2] ? n : n / 1e6;
};
const topGap = a => Math.max(...Object.values(a.vectors).map(v => v.gap));
const weight = a => (topGap(a) / 100) * valNum(a);

function driverFace(a) {
  let best = null;
  for (const f of FACES) { const v = a.vectors[f.id]; if (!best || v.gap > a.vectors[best].gap) best = f.id; }
  return best;
}

function queueFor(v) {
  let list;
  if (v === "tim") list = ACCOUNTS.slice();
  else if (v === "craig") list = ACCOUNTS.filter(a => ["marketing", "relationship"].includes(driverFace(a)) && a.vectors.marketing.gap > 0);
  else list = ACCOUNTS.filter(a => a.vectors.warranty.gap > 0);
  return list.filter(a => !S.dispatched[a.id]).sort((x, y) => weight(y) - weight(x));
}

const SCOPE = {
  tim: "This list is scoped to every account with an open gap.",
  luke: "This list is scoped to accounts breaching a target that is declared and versioned in the index — currently the thirty-day warranty claim age.",
  craig: "This list is scoped to accounts whose widest gap is a marketing or relationship face, which is where the systems register and identity resolution decide the answer."
};

function go(screen, opts) { S.screen = screen; Object.assign(S, opts || {}); render(); window.scrollTo(0, 0); }

/* ---------------- chrome ---------------- */
function chrome() {
  return `
  <header class="app">
    <div>
      <h1>Customer Sphere</h1>
      <div style="font-size:12.5px;color:var(--mute);margin-top:2px">
        HawkinsTwin Customer 360 &middot; one customer, all faces &middot; demonstration surface
      </div>
    </div>
    <div class="who">
      <label class="sw" for="sw">Lists prepared for</label>
      <select id="sw">
        ${VIEWS.map(v => `<option value="${v.id}"${v.id === S.view ? " selected" : ""}>${esc(v.who)} — ${esc(v.view)}</option>`).join("")}
      </select>
    </div>
  </header>
  <div class="clock">
    <span><span class="dot"></span>Data as of ${META.asOf}</span><span>·</span>
    <span>next refresh ${META.nextRefresh}</span><span>·</span>
    <span>${SOURCES.filter(s => s.state === "current").length} of ${SOURCES.length} sources current</span>
    ${SOURCES.map(s => `<span class="src"${s.state !== "current" ? ' style="border-color:#e0b48a"' : ""}>${esc(s.short)} ${esc(s.landed)}</span>`).join("")}
  </div>
  <div class="note warn" style="margin-top:12px">
    <strong>No dealership data has moved.</strong> ${esc(META.agreement)}
    Every customer, VIN, phone number and amount on this surface is invented,
    and the live dealer management system is never written to.
  </div>`;
}

function foot() {
  return `<footer class="app">
    <p><strong>Demonstration surface, synthetic data.</strong> Names of people are shown without titles,
       per the platform naming canon. Customers, vehicles and figures are fabricated for this demonstration.</p>
    <p>Screens follow <a href="../CUSTOMER-SPHERE-DESIGN.md">the Customer Sphere design</a> —
       the two-body split (&sect;2), vectored targets (&sect;6), identity (&sect;8) and the gates (&sect;10).
       <a href="../EVEglyphDesign_Hawkins_Twin_Customer_Sphere_Design.pdf">Controlled PDF</a>.</p>
    <p>&copy; 2026 EVEglyphDesign. <em>Pour le bien-&ecirc;tre du peuple.</em></p>
  </footer>`;
}

/* ---------------- the sphere diagram ---------------- */
function sphereSVG(a) {
  const cx = 260, cy = 152, R = 108, LR = 126;
  const n = FACES.length;
  let spokes = "", labels = "";
  FACES.forEach((f, i) => {
    const ang = (-Math.PI / 2) + (i * 2 * Math.PI / n);
    const v = a.vectors[f.id];
    const len = 20 + (v.gap / 100) * (R - 20);
    const x = cx + Math.cos(ang) * len, y = cy + Math.sin(ang) * len;
    const ex = cx + Math.cos(ang) * R, ey = cy + Math.sin(ang) * R;
    const lx = cx + Math.cos(ang) * LR, ly = cy + Math.sin(ang) * LR;
    const hot = v.gap >= 70, warm = v.gap >= 30 && v.gap < 70;
    const col = hot ? "#e87722" : warm ? "#1a1a1a" : "#b9b2a3";
    spokes += `<g style="cursor:pointer" onclick="go('face',{face:'${f.id}'})" role="button" tabindex="0" aria-label="Open the ${esc(f.label)} face">`;
    spokes += `<line x1="${cx}" y1="${cy}" x2="${ex.toFixed(1)}" y2="${ey.toFixed(1)}" stroke="transparent" stroke-width="26"/>`;
    spokes += `<line x1="${cx}" y1="${cy}" x2="${ex.toFixed(1)}" y2="${ey.toFixed(1)}" stroke="#e7e1d3" stroke-width="1"/>`;
    spokes += `<line x1="${cx}" y1="${cy}" x2="${x.toFixed(1)}" y2="${y.toFixed(1)}" stroke="${col}" stroke-width="${hot ? 3.5 : 2.5}"/>`;
    spokes += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${hot ? 5 : 4}" fill="${col}"/>`;
    spokes += `</g>`;
    const c = Math.cos(ang);
    const anchor = c > 0.25 ? "start" : c < -0.25 ? "end" : "middle";
    const dy = Math.sin(ang) > 0.7 ? 12 : Math.sin(ang) < -0.7 ? -6 : 4;
    labels += `<g style="cursor:pointer" onclick="go('face',{face:'${f.id}'})"><rect x="${(lx - (anchor === "start" ? 2 : anchor === "end" ? 86 : 44)).toFixed(1)}" y="${(ly + dy - 12).toFixed(1)}" width="88" height="30" fill="transparent"/>`;
    labels += `<text x="${lx.toFixed(1)}" y="${(ly + dy).toFixed(1)}" text-anchor="${anchor}" font-family="Inter,sans-serif" font-size="11" font-weight="600" fill="#1a1a1a">${esc(f.label)}</text>`;
    labels += `<text x="${lx.toFixed(1)}" y="${(ly + dy + 13).toFixed(1)}" text-anchor="${anchor}" font-family="IBM Plex Mono,monospace" font-size="10" fill="${col}">gap ${v.gap}</text></g>`;
  });
  return `<svg viewBox="0 0 520 320" width="100%" style="max-width:520px;display:block;margin:0 auto" role="img"
      aria-label="Seven face vectors, each clickable from the customer at the centre, drawn at a length proportional to the gap between current and target.">
    <circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="#e7e1d3" stroke-width="1" stroke-dasharray="3 4"/>
    <circle cx="${cx}" cy="${cy}" r="${R * 0.5}" fill="none" stroke="#f0ebdd" stroke-width="1"/>
    ${spokes}
    <circle cx="${cx}" cy="${cy}" r="6" fill="#1a1a1a"/>
    ${labels}
    <text x="${cx}" y="${cy + 26}" text-anchor="middle" font-family="Inter,sans-serif" font-size="10" fill="#6b665c">the customer</text>
    <text x="${cx}" y="308" text-anchor="middle" font-family="Inter,sans-serif" font-size="10" fill="#6b665c">dashed ring = the declared target on every face &middot; click a spoke to open that face</text>
  </svg>`;
}

/* ---------------- home : the split worklist ---------------- */
function home() {
  const q = queueFor(S.view);
  const done = Object.keys(S.dispatched).length;
  const cards = STRUCTURAL.filter(c => c.views.includes(S.view) && !S.parked[c.id]);

  const queue = q.length ? q.map((a, i) => {
    const f = driverFace(a);
    return `
    <div class="item">
      <div class="top">
        <span class="idx">${i + 1}</span>
        <span class="kind">${esc(a.name)}</span>
        <span class="vend">${esc(a.cohort)}</span>
        <span class="amt">${esc(a.value.replace(" trailing 12 months", ""))}</span>
      </div>
      <div class="line2">${esc(a.headline)}.</div>
      <div class="why"><b>Widest gap:</b> ${esc(FACES.find(x => x.id === f).label)} — ${a.vectors[f].gap} of 100 against a declared target.</div>
      <div class="foot">
        <span class="ev">${a.units} units &middot; customer since ${esc(a.since)} &middot; ${a.keys.length} source keys held</span>
        <button class="pri" onclick="go('sphere',{acct:'${a.id}'})">Open the sphere</button>
        <button onclick="go('gate',{acct:'${a.id}'})">Dispatch</button>
      </div>
    </div>`;
  }).join("") : `
    <div class="empty">
      <b>The queue is empty.</b>
      Urgency is a queue and it is meant to reach zero. The structural digest below never does.
      ${done ? `<div style="margin-top:10px"><button class="ghost" onclick="reset()">Reset the demonstration</button></div>` : ""}
    </div>`;

  return `${chrome()}
  <div class="block">
    <div class="blockhead">
      <h2>Needs a person today</h2>
      <span class="count">${q.length} account${q.length === 1 ? "" : "s"}${done ? ` &middot; ${done} dispatched` : ""}</span>
    </div>
    <p class="blocknote">Ranked by the widest gap between current and target, weighted by account value.
       Prioritisation is not a rule somebody maintains — it falls out of the geometry (&sect;6.3).
       ${esc(SCOPE[S.view])}</p>
    ${queue}
  </div>

  <div class="block">
    <div class="blockhead">
      <h2>Worth fixing at the root</h2>
      <span class="count">structural &middot; no deadline, no owner</span>
    </div>
    <p class="blocknote">A digest. These are properties of the model and the sources, not of any one customer,
       and none of them is urgent on any particular morning.</p>
    ${cards.length ? cards.map((c, i) => `
      <div class="item strategy">
        <div class="top">
          <span class="idx">${String.fromCharCode(65 + i)}</span>
          <span class="kind">${esc(c.title)}</span>
          <span class="amt" style="font-size:12px">${esc(c.ref)}</span>
        </div>
        <div class="line2">${esc(c.scale)}</div>
        <div class="why">${esc(c.trend)}</div>
        <div class="foot">
          <span class="ev">${c.rows.length} rows shown</span>
          <button onclick="go('structural',{struct:'${c.id}'})">See the analysis</button>
        </div>
      </div>`).join("") : `<div class="empty"><b>Everything structural is parked.</b>
        That is not the same as fixed. <button class="ghost" onclick="reset()">Reset</button></div>`}
  </div>

  <div class="block">
    <div class="blockhead"><h2>The two-body split</h2><span class="count">&sect;2</span></div>
    <p class="blocknote">Two places, and only one of them ever holds a customer record.</p>
    <div class="panel"><div class="body">
      <table><thead><tr><th>&nbsp;</th><th>Index repository</th><th>Business data store</th></tr></thead><tbody>
        <tr><td><strong>What</strong></td><td>Pointers, field dictionary, identity rules, declared targets, lineage</td><td>Actual customer, sales, service, parts, finance and call records</td></tr>
        <tr><td><strong>Where</strong></td><td>GitHub — public, forkable</td><td>Postgres, inside the dealership's own Azure tenant</td></tr>
        <tr><td><strong>Holds a customer record?</strong></td><td><strong>Never</strong></td><td>Yes, all of them</td></tr>
      </tbody></table>
      <p class="hint" style="margin-top:10px">Open any field on any face below and you reach the index card, not the value.
         That is the split working, and it is the answer to <em>who ends up holding my data</em>.</p>
      <div style="margin-top:11px;display:flex;gap:8px;flex-wrap:wrap">
        ${Object.keys(INDEX_CARDS).map(k => `<button onclick="go('indexcard',{card:'${k}'})"><code>${esc(k)}</code></button>`).join("")}
      </div>
    </div></div>
  </div>
  ${foot()}`;
}

/* ---------------- the sphere, one account ---------------- */
function sphereScreen() {
  const a = acct(S.acct);
  const rows = FACES.map(f => {
    const v = a.vectors[f.id];
    const col = v.gap >= 70 ? "var(--accent)" : v.gap >= 30 ? "var(--ink)" : "#b9b2a3";
    return `<tr>
      <td><strong>${esc(f.label)}</strong><div class="hint">${esc(f.journal === "—" ? "no journal" : f.journal)}</div></td>
      <td>${esc(v.cur)}</td>
      <td>${esc(v.tgt)}</td>
      <td style="width:140px">
        <div style="background:var(--cream2);border:1px solid var(--line);height:10px;position:relative">
          <div style="background:${col};height:100%;width:${v.gap}%"></div>
        </div>
        <div class="hint" style="margin-top:2px">gap ${v.gap}</div>
      </td>
      <td class="num"><button onclick="go('face',{acct:'${a.id}',face:'${f.id}'})">Open</button></td>
    </tr>`;
  }).join("");

  return `${chrome()}
  <div class="back"><button class="ghost" onclick="go('home')">&larr; Back to the worklist</button></div>
  <div class="titlebar">
    <h2>${esc(a.name)}</h2>
    <span class="r">${esc(a.value)}</span>
  </div>

  <div class="panel"><h3>One customer, all faces</h3><div class="body">
    ${sphereSVG(a)}
    <p class="hint" style="margin-top:8px;text-align:center">Each spoke is a vector: a direction, a magnitude,
      an origin and a declared target. Length is the gap between where the face is and where it is aimed.</p>
  </div></div>

  <div class="panel"><h3>The faces</h3><div class="body">
    <table><thead><tr><th>Face</th><th>Current</th><th>Target</th><th>Gap</th><th class="num">&nbsp;</th></tr></thead>
      <tbody>${rows}</tbody></table>
  </div></div>

  <div class="panel"><h3>Identity — how this became one customer</h3><div class="body">
    <dl class="kv">
      <dt>Sphere key</dt><dd><code>${esc(a.key)}</code> — minted inside the sphere. No source key is promoted to master.</dd>
      <dt>Source keys</dt><dd class="idlist">${a.keys.map(esc).join(" &nbsp;·&nbsp; ")}</dd>
      <dt>Resolution</dt><dd>${esc(a.identity)}</dd>
      <dt>Kind</dt><dd>${esc(a.kind)} — ${a.people.length} affiliated ${a.people.length === 1 ? "person" : "people"}: ${a.people.map(esc).join("; ")}</dd>
      <dt>Vehicles</dt><dd>${a.units} — service and warranty history hangs from the vehicle, not from whoever booked the appointment.</dd>
    </dl>
    <div style="margin-top:12px"><button onclick="go('identity')">Open the stewardship queue</button></div>
  </div></div>

  <div class="panel"><h3>Where the sources disagree</h3><div class="body">
    <table><thead><tr><th>Field</th><th>Source</th><th>Value</th><th>Extracted</th><th class="num">Confidence</th></tr></thead><tbody>
      <tr><td rowspan="2"><strong>${esc(a.disagreement.field)}</strong></td>
          <td>${esc(a.disagreement.a.src)}</td><td>${esc(a.disagreement.a.val)}</td>
          <td>${esc(a.disagreement.a.ts)}</td><td class="num">${esc(a.disagreement.a.conf)}</td></tr>
      <tr><td>${esc(a.disagreement.b.src)}</td><td>${esc(a.disagreement.b.val)}</td>
          <td>${esc(a.disagreement.b.ts)}</td><td class="num">${esc(a.disagreement.b.conf)}</td></tr>
    </tbody></table>
    <div class="note">${esc(a.disagreement.ruling)}</div>
  </div></div>

  <div style="margin-top:18px;display:flex;gap:8px;flex-wrap:wrap">
    <button class="pri" onclick="go('gate',{acct:'${a.id}'})">Dispatch to a person &rarr;</button>
    <button class="ghost" onclick="go('home')">Back to the worklist</button>
  </div>
  ${foot()}`;
}

/* ---------------- a single face ---------------- */
function faceScreen() {
  const a = acct(S.acct), f = FACES.find(x => x.id === S.face), v = a.vectors[S.face];
  const fields = FACE_FIELDS[S.face] || [];
  return `${chrome()}
  <div class="back"><button class="ghost" onclick="go('sphere',{acct:'${a.id}'})">&larr; Back to the sphere</button></div>
  <div class="titlebar">
    <h2>${esc(f.label)} — ${esc(a.name)}</h2>
    <span class="r">gap ${v.gap}</span>
  </div>

  <div class="panel"><h3>The vector</h3><div class="body">
    <dl class="kv">
      <dt>Direction</dt><dd>${esc(f.label)} — one of seven faces on this customer</dd>
      <dt>Magnitude</dt><dd>${esc(v.cur)}</dd>
      <dt>Target</dt><dd>${esc(v.tgt)}</dd>
      <dt>Gap</dt><dd>${v.gap} of 100, weighted against account value when the worklist is ranked</dd>
      <dt>Journal</dt><dd>${esc(f.journal === "—" ? "None — this face is not financially meaningful" : f.journal + (f.journal === "ACDOCI" ? " — the interaction journal, never ACDOCA" : " — the universal journal, unmodified"))}</dd>
    </dl>
    <div class="note">${esc(v.note)}</div>
  </div></div>

  <div class="panel"><h3>Origin — every fact carries one</h3><div class="body">
    <table><thead><tr><th>Contributing source</th><th>Route</th><th>Extracted</th><th class="num">State</th></tr></thead><tbody>
      ${SOURCES.map(s => `<tr><td>${esc(s.name)} <span class="hint">(${esc(s.short)})</span></td><td>${esc(s.route)}</td><td>${esc(s.landed)}</td><td class="num">${esc(s.state)}</td></tr>`).join("")}
    </tbody></table>
    <p class="hint" style="margin-top:9px">A vector with no traceable origin is not admitted to the sphere.
      A number that reaches this screen can be walked back to the record and the extraction that produced it.</p>
  </div></div>

  <div class="panel"><h3>The fields behind this face</h3><div class="body">
    <p>These open the <strong>index</strong>, not the data. The index holds pointers, never payload.</p>
    <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">
      ${fields.map(k => `<button onclick="go('indexcard',{card:'${k}'})"><code>${esc(k)}</code></button>`).join("")}
    </div>
  </div></div>

  <div style="margin-top:18px;display:flex;gap:8px;flex-wrap:wrap">
    <button class="pri" onclick="go('gate',{acct:'${a.id}'})">Dispatch to a person &rarr;</button>
    <button class="ghost" onclick="go('sphere',{acct:'${a.id}'})">Back to the sphere</button>
  </div>
  ${foot()}`;
}

/* ---------------- index card ---------------- */
function indexCardScreen() {
  const c = INDEX_CARDS[S.card];
  return `${chrome()}
  <div class="back"><button class="ghost" onclick="back()">&larr; Back</button></div>
  <div class="titlebar">
    <h2>Index card</h2>
    <span class="r">${esc(c.canonical)}</span>
  </div>

  <div class="note warn">This is the index repository, the GitHub half of the two-body split.
    It tells you what exists, what it is called in every vocabulary, where the real thing lives, and what
    governs it. <strong>It never shows you a value.</strong></div>

  <div class="panel"><h3>What it is called, in every vocabulary it has</h3><div class="body">
    <table><thead><tr><th>Vocabulary</th><th>Name there</th></tr></thead><tbody>
      ${c.names.map(n => `<tr><td>${esc(n[0])}</td><td><code>${esc(n[1])}</code></td></tr>`).join("")}
    </tbody></table>
  </div></div>

  <div class="panel"><h3>Where the real thing lives</h3><div class="body">
    <p><code>${esc(c.pointer)}</code></p>
    <p class="hint">A pointer into the tenant Postgres — schema, table, column. Never the value itself.</p>
  </div></div>

  <div class="panel"><h3>Width and coercion</h3><div class="body">
    <p>${esc(c.width)}</p>
  </div></div>

  <div class="panel"><h3>What governs it</h3><div class="body">
    <ul>${c.governance.map(g => `<li>${esc(g)}</li>`).join("")}</ul>
  </div></div>
  ${foot()}`;
}

/* ---------------- stewardship queue ---------------- */
function identityScreen() {
  return `${chrome()}
  <div class="back"><button class="ghost" onclick="back()">&larr; Back</button></div>
  <div class="titlebar">
    <h2>Stewardship queue</h2>
    <span class="r">${CANDIDATES.filter(c => !S.merged[c.id]).length} of ${CANDIDATES.length} outstanding</span>
  </div>

  <div class="note">Deterministic matching ran first. What reached this queue is what fuzzy matching proposed
    and nothing auto-merged. Every link carries its score and the rule that produced it, and every merge is
    an appended, timestamped, attributed event that an unmerge reverses (&sect;8).</div>

  ${CANDIDATES.map(c => {
    const st = S.merged[c.id];
    return `<div class="panel"><h3>${esc(c.id)} — ${esc(c.rule)} — score ${esc(c.score)}</h3><div class="body">
      <dl class="kv">
        <dt>Left</dt><dd>${esc(c.a)}</dd>
        <dt>Right</dt><dd>${esc(c.b)}</dd>
        <dt>Why proposed</dt><dd>${esc(c.why)}</dd>
      </dl>
      ${st
        ? `<div class="note"><strong>${esc({ merged: "Merged", affiliation: "Recorded as an affiliation edge", rejected: "Rejected" }[st])}</strong>
             — appended as a timestamped, attributed event.
             <button class="link" style="margin-left:8px" onclick="unmerge('${c.id}')">Reverse it</button></div>`
        : `<div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">
             <button class="pri" onclick="decide('${c.id}','merged')">Merge — same entity</button>
             <button onclick="decide('${c.id}','affiliation')">Not a merge — affiliation edge</button>
             <button class="ghost" onclick="decide('${c.id}','rejected')">Reject</button>
           </div>`}
    </div></div>`;
  }).join("")}

  <div class="note warn">A person is not an organisation. A fleet is not a driver. Where the right side is a
    person at the organisation on the left, the correct answer is an affiliation edge and never a merge.</div>
  ${foot()}`;
}

/* ---------------- structural card ---------------- */
function structuralScreen() {
  const c = struc(S.struct);
  return `${chrome()}
  <div class="back"><button class="ghost" onclick="go('home')">&larr; Back to the worklist</button></div>
  <div class="titlebar">
    <h2>${esc(c.title)}</h2>
    <span class="r">${esc(c.ref)}</span>
  </div>

  <div class="panel"><h3>Scale</h3><div class="body">
    <dl class="kv"><dt>Population</dt><dd>${esc(c.scale)}</dd><dt>Trend</dt><dd>${esc(c.trend)}</dd></dl>
  </div></div>

  <div class="panel"><h3>The population</h3><div class="body">
    <table><thead><tr>${c.cols.map((h, i) => `<th${i >= c.cols.length - 1 ? ' class="num"' : ""}>${esc(h)}</th>`).join("")}</tr></thead><tbody>
      ${c.rows.map(r => `<tr>${r.map((v, i) => `<td${i >= c.cols.length - 1 ? ' class="num"' : ""}>${esc(v)}</td>`).join("")}</tr>`).join("")}
    </tbody></table>
    <p class="hint" style="margin-top:10px">${esc(c.more)}</p>
  </div></div>

  <div class="panel"><h3>How to read it</h3><div class="body">
    <ol>${c.method.map(m => `<li>${esc(m)}</li>`).join("")}</ol>
  </div></div>

  <div class="panel"><h3>What would change it</h3><div class="body">
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      ${c.actions.map((a, i) => `<button class="${i === 0 ? "pri" : i === 1 ? "" : "ghost"}" onclick="structAct('${c.id}','${esc(a)}')">${esc(a)}</button>`).join("")}
    </div>
    <p class="hint" style="margin-top:11px">No deadline and no owner by design. A structural card asks whether
      this is worth changing, never what to do today.</p>
  </div></div>
  ${foot()}`;
}

/* ---------------- the gate ---------------- */
function gateScreen() {
  const a = acct(S.acct);
  return `${chrome()}
  <div class="back"><button class="ghost" onclick="go('sphere',{acct:'${a.id}'})">&larr; Back to the sphere</button></div>
  <div class="titlebar">
    <h2>Approval required</h2>
    <span class="r">${esc(a.name)}</span>
  </div>

  <div class="note warn"><strong>The live dealer management system is never written to.</strong> Unchanged, in
    every phase. What leaves this gate is a dispatch to a named desk and an appended interaction record —
    never an update to CDK.</div>

  <div class="panel"><h3>What will be dispatched</h3><div class="body">
    <dl class="kv">
      <dt>Action</dt><dd>${esc(a.action.title)}</dd>
      <dt>To</dt><dd>${esc(a.action.to)}</dd>
      <dt>Origin</dt><dd>Composed from the sphere at ${esc(META.asOf)} across ${SOURCES.filter(s => s.state === "current").length} current sources</dd>
    </dl>
    <ol style="margin-top:10px">${a.action.body.map(b => `<li>${esc(b)}</li>`).join("")}</ol>
  </div></div>

  <div class="panel"><h3>Exact envelope</h3><div class="body">
    <pre class="payload">${esc(JSON.stringify(a.action.envelope, null, 2))}</pre>
    <p class="hint" style="margin-top:9px">The envelope, not a summary of it. Note
      <code>"write_to_dms": false</code> — it is a property of the envelope, not a setting somebody could
      forget to tick.</p>
  </div></div>

  <div class="panel"><h3>Alternative</h3><div class="body">
    <p>Prepare a file and hand it to the desk instead. Format: whichever the receiving system accepts today.</p>
    <button onclick="loadFile()">Prepare a file</button>
  </div></div>

  <div class="panel"><h3>Approving as ${esc(viewObj().who)}</h3><div class="body">
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <button class="pri" onclick="dispatch()">Approve and dispatch</button>
      <button onclick="go('sphere',{acct:'${a.id}'})">Edit</button>
      <button class="ghost" onclick="rejectDispatch()">Reject — reason required</button>
    </div>
    <div class="note">Nothing leaves the sphere without this click. After it, the interaction is appended to
      ACDOCI automatically and the account re-reads at the next refresh.</div>
  </div></div>
  ${foot()}`;
}

/* ---------------- the record ---------------- */
function recordScreen() {
  const a = acct(S.acct), d = S.dispatched[a.id];
  const rows = d.rejected ? [
    ["07:40", "Composed", "Widest gap ranked against account value"],
    ["07:52", "Reviewed", `${viewObj().who}`],
    ["07:52", "Rejected", d.reason],
    ["07:52", "Returned", "Back on the worklist. The rejection is the ranking's own error rate."]
  ] : [
    ["07:40", "Composed", "Widest gap ranked against account value"],
    ["07:52", "Approved", `${viewObj().who} — envelope shown at the gate`],
    ["07:52", "Dispatched", `${a.action.to} — reference ${d.ref}`],
    ["07:52", "Appended", "ACDOCI interaction record. ACDOCA untouched."],
    ["07:52", "Not written", "CDK. By design, in every phase."],
    ["13:40", "Re-read", "Account re-composed from source at the next refresh"],
    ["13:40", "Measured", "Gap on the driving face recalculated from the new position"]
  ];

  return `${chrome()}
  <div class="titlebar">
    <h2>${d.rejected ? "Returned" : "Dispatched"} — ${esc(a.name)}</h2>
    <span class="r">${esc(d.ref)}</span>
  </div>

  <div class="panel"><h3>The record</h3><div class="body">
    <ul class="tl">
      ${rows.map(r => `<li><span class="t">${esc(r[0])}</span><span class="e">${esc(r[1])}</span><span>${esc(r[2])}</span></li>`).join("")}
    </ul>
  </div></div>

  <div class="note">One record, exportable, and walkable back to the extraction that produced every number in
    it. This is the screen a sceptical auditor asks for, and it is also the screen that proves the dealer
    management system was not touched.</div>

  <div style="margin-top:18px;display:flex;gap:8px;flex-wrap:wrap">
    <button class="pri" onclick="go('home')">Back to the worklist</button>
    <button class="ghost" onclick="alert('Demonstration surface. Export is described in the design, §9 — every field at every layer carries source, extraction timestamp and confidence.')">Export the record</button>
  </div>
  ${foot()}`;
}

/* ---------------- actions ---------------- */
function back() { if (S.acct && S.face) go("face"); else if (S.acct) go("sphere"); else go("home"); }

function dispatch() {
  const a = acct(S.acct);
  S.dispatched[a.id] = { at: "07:52", ref: "DSP-" + a.id.replace("CS-", ""), to: a.action.to };
  go("record");
}

function rejectDispatch() {
  const r = prompt("Reject — reason required.\n\nThe rejection rate is the ranking's own error rate. A ranking nobody rejects is a ranking nobody is reading.");
  if (!r || !r.trim()) { alert("A reason is required. Nothing was rejected."); return; }
  const a = acct(S.acct);
  S.dispatched[a.id] = { at: "07:52", ref: "REJ-" + a.id.replace("CS-", ""), rejected: true, reason: r.trim() };
  go("record");
}

function decide(id, what) { S.merged[id] = what; render(); }
function unmerge(id) { delete S.merged[id]; render(); }

function structAct(id, label) {
  if (label === "Park") { S.parked[id] = true; go("home"); return; }
  alert(`"${label}" — a structural action does not write to an operational system. It raises a request, records a dependency, or parks the card.`);
}

function loadFile() {
  const a = acct(S.acct);
  const e = a.action.envelope;
  const csv = Object.keys(e).join(",") + "\n" + Object.values(e).map(v => `"${v}"`).join(",") + "\n";
  const url = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
  const link = document.createElement("a");
  link.href = url; link.download = `${a.id}-dispatch.csv`; link.click();
  URL.revokeObjectURL(url);
}

function reset() { S.dispatched = {}; S.parked = {}; S.merged = {}; go("home"); }

/* ---------------- render ---------------- */
function render() {
  const v = {
    home, sphere: sphereScreen, face: faceScreen, indexcard: indexCardScreen,
    identity: identityScreen, structural: structuralScreen, gate: gateScreen, record: recordScreen
  };
  $("#app").innerHTML = v[S.screen]();
  const sw = $("#sw");
  if (sw) sw.onchange = e => { S.view = e.target.value; go("home"); };
}

render();
