/* HawkinsTwin Customer Sphere — demonstration surface.
   100% synthetic data. No dealership record has moved. Nothing here touches CDK.
   Every customer, VIN, phone number, amount and timestamp below is invented. */

const META = {
  asOf: "07:40 AST",
  nextRefresh: "13:40 AST",
  agreement: "Not executed — the sphere is running on synthetic and mock composite data (§10)."
};

const SOURCES = [
  { short: "CDK", name: "Dealer management system", landed: "07:40", state: "current", route: "Restored backup + export lane" },
  { short: "TELUS", name: "Call platform", landed: "07:36", state: "current", route: "Service identity, company owned" },
  { short: "ePortal", name: "Inventory and ePortal surface", landed: "06:55", state: "current", route: "Export" },
  { short: "Marketing", name: "Lead and marketing platform", landed: "yesterday", state: "stale", route: "Manual" },
  { short: "Scheduling", name: "Service scheduling", landed: "—", state: "unreachable", route: "No access route stated" }
];

/* Names stand alone. Titles are deliberately not shown — canon/naming-people.md. */
const VIEWS = [
  { id: "tim",   who: "Tim Hawkins",                view: "accounts" },
  { id: "luke",  who: "Luke Weatherbie [Skywalker]", view: "targets and peer variance" },
  { id: "craig", who: "Craig Allen [Mr. Marketing]", view: "sources and the index" }
];

const FACES = [
  { id: "commercial",   label: "Commercial",   journal: "ACDOCA" },
  { id: "service",      label: "Service",      journal: "ACDOCA" },
  { id: "parts",        label: "Parts",        journal: "ACDOCA" },
  { id: "finance",      label: "Finance",      journal: "ACDOCA" },
  { id: "warranty",     label: "Warranty",     journal: "ACDOCA" },
  { id: "relationship", label: "Relationship", journal: "ACDOCI" },
  { id: "marketing",    label: "Marketing",    journal: "—" }
];

/* ---------------- accounts ---------------- */
const ACCOUNTS = [
  {
    id: "CS-0001", key: "cs_8f31a0c2", name: "Miramichi Forest Haulage Ltd", short: "Miramichi", kind: "Organisation",
    value: "CAD 1.24M trailing 12 months", units: 14, since: "2011",
    people: ["R. Savoie — dispatch", "M. Doucet — maintenance", "P. Arsenault — accounts"],
    keys: ["CDK 104882", "TELUS +1 506 555 0142", "ePortal MFH-4471", "Marketing acct 88213"],
    identity: "Resolved deterministically on CDK customer number and normalised phone. Two candidate links held.",
    cohort: "Voicemail not returned within two hours",
    headline: "Bought nothing for nine months and four of its calls were never returned",
    vectors: {
      commercial:   { cur: "CAD 0 units sold, 9 months", tgt: "2 units / year", gap: 92, unit: "",
                      note: "Last unit delivered 27 Oct 2025. Two prior years averaged 2.5 units." },
      service:      { cur: "31 repair orders, CAD 214,000", tgt: "CAD 240,000", gap: 11,
                      note: "Service is holding. It is the only face that is." },
      parts:        { cur: "CAD 88,400", tgt: "CAD 130,000", gap: 32,
                      note: "Counter purchases fell after the second unreturned call in March." },
      finance:      { cur: "CAD 41,200 open, 12 days average", tgt: "under 30 days", gap: 0,
                      note: "Pays early. There is no finance problem here." },
      warranty:     { cur: "2 open claims, 61 days oldest", tgt: "under 30 days", gap: 51,
                      note: "One claim has been open since 2 June with no dealer-side action recorded." },
      relationship: { cur: "9 unreturned contacts, 4 voicemails", tgt: "0 unreturned over 2 hours", gap: 100,
                      note: "Nine events across four contacts compose into one account-level vector (§6)." },
      marketing:    { cur: "Present, spelled differently", tgt: "One resolved identity", gap: 40,
                      note: "Marketing platform holds 'Miramichi Forestry Haulage' — a candidate link, not a merge." }
    },
    disagreement: {
      field: "Primary phone",
      a: { src: "CDK", val: "+1 506 555 0142", ts: "07:40", conf: "high" },
      b: { src: "Marketing platform", val: "+1 506 555 0199", ts: "yesterday", conf: "low" },
      ruling: "Both vectors are held. Neither is averaged away. The divergence is reported and the stewardship queue decides (§6.2)."
    },
    action: {
      title: "Dispatch a callback and a warranty chase",
      to: "the service desk",
      body: [
        "Return four voicemails on the account, oldest first — 12 Mar, 4 Apr, 19 Jun, 28 Jul.",
        "Chase warranty claim WC-2026-0331, open 61 days.",
        "Confirm the primary phone number against CDK, not the marketing record."
      ],
      envelope: {
        customer_sphere_id: "cs_8f31a0c2",
        cdk_customer_number: "104882",
        dispatch: "callback_and_warranty_chase",
        journal: "ACDOCI",
        target_window_hours: 2,
        write_to_dms: false
      }
    }
  },
  {
    id: "CS-0002", key: "cs_23d90fb7", name: "Restigouche Aggregate Co", short: "Restigouche", kind: "Organisation",
    value: "CAD 2.61M trailing 12 months", units: 22, since: "2004",
    people: ["J. Lévesque — owner", "A. Chiasson — shop"],
    keys: ["CDK 100214", "TELUS +1 506 555 0771", "ePortal RAC-1102"],
    identity: "Resolved deterministically. No candidate links outstanding.",
    cohort: "Repeat caller without callback",
    headline: "Called three times in five days about the same unit and has not been called back",
    vectors: {
      commercial:   { cur: "4 units, CAD 1.42M", tgt: "4 units / year", gap: 0,
                      note: "On target. The commercial face is not the problem." },
      service:      { cur: "CAD 388,000, 3 units awaiting parts", tgt: "CAD 420,000", gap: 8,
                      note: "Three units down and waiting is the reason for the calls." },
      parts:        { cur: "CAD 240,100", tgt: "CAD 280,000", gap: 14,
                      note: "Two back-ordered lines are blocking the three units above." },
      finance:      { cur: "CAD 188,000 open, 44 days average", tgt: "under 30 days", gap: 47,
                      note: "Ageing has moved with the service dispute, not independently of it." },
      warranty:     { cur: "0 open claims", tgt: "under 30 days", gap: 0, note: "Clean." },
      relationship: { cur: "3 inbound in 5 days, 0 callbacks", tgt: "0 repeat callers uncalled", gap: 100,
                      note: "Repeat caller without callback — the second standing cohort (§7b)." },
      marketing:    { cur: "Resolved, single identity", tgt: "One resolved identity", gap: 0, note: "Clean." }
    },
    disagreement: {
      field: "Units in operation",
      a: { src: "CDK", val: "22", ts: "07:40", conf: "high" },
      b: { src: "ePortal", val: "19", ts: "06:55", conf: "medium" },
      ruling: "Three units sold through another dealer are in CDK as owned and absent from ePortal. Both held, divergence reported."
    },
    action: {
      title: "Dispatch a callback on the parts back-order",
      to: "the parts desk",
      body: [
        "Call J. Lévesque today. Three inbound calls in five days, none returned.",
        "State a date for the two back-ordered lines blocking three units.",
        "Note that CAD 188,000 of ageing sits behind the same dispute."
      ],
      envelope: {
        customer_sphere_id: "cs_23d90fb7",
        cdk_customer_number: "100214",
        dispatch: "callback_parts_backorder",
        journal: "ACDOCI",
        target_window_hours: 4,
        write_to_dms: false
      }
    }
  },
  {
    id: "CS-0003", key: "cs_5b7e14aa", name: "Fundy Bay Seafood Transport Inc", short: "Fundy Bay", kind: "Organisation",
    value: "CAD 640,000 trailing 12 months", units: 6, since: "2019",
    people: ["S. Comeau — owner"],
    keys: ["CDK 112907", "TELUS +1 902 555 0330"],
    identity: "Resolved on phone only. CDK customer number matched at medium confidence.",
    cohort: "Never reached",
    headline: "Six attempts outbound, never reached, and the unit warranty window closes in 21 days",
    vectors: {
      commercial:   { cur: "1 unit, CAD 198,000", tgt: "2 units / year", gap: 50,
                      note: "Bought one. The second was quoted in January and never followed up." },
      service:      { cur: "CAD 61,000", tgt: "CAD 96,000", gap: 36,
                      note: "Reefer work is going somewhere else. It is not clear where." },
      parts:        { cur: "CAD 22,300", tgt: "CAD 40,000", gap: 44, note: "Counter only. No account activity." },
      finance:      { cur: "CAD 0 open", tgt: "under 30 days", gap: 0, note: "Nothing outstanding." },
      warranty:     { cur: "Window closes in 21 days, 0 claims made", tgt: "Reviewed before close", gap: 78,
                      note: "A warranty window closing unreviewed is money the customer loses and blames the dealer for." },
      relationship: { cur: "6 outbound, 0 connected, 0 inbound", tgt: "Contact made", gap: 100,
                      note: "Never reached — the third standing cohort. Six attempts is not a relationship." },
      marketing:    { cur: "Not present in any marketing system", tgt: "One resolved identity", gap: 100,
                      note: "Known to CDK and to the phone system and to nothing else." }
    },
    disagreement: {
      field: "Account status",
      a: { src: "CDK", val: "Active", ts: "07:40", conf: "high" },
      b: { src: "Call platform", val: "No connected call in 14 months", ts: "07:36", conf: "high" },
      ruling: "Two high-confidence sources, no contradiction in the data and a contradiction in the business. Held as a divergence, surfaced, not resolved by rule."
    },
    action: {
      title: "Dispatch a warranty review before the window closes",
      to: "the service desk",
      body: [
        "Review the warranty position on VIN 1XPBD49X6MD" + "774201 before 23 August.",
        "Six outbound attempts have not connected. Try the shop line, not the mobile.",
        "If unreachable again, record it and escalate rather than attempting a seventh time."
      ],
      envelope: {
        customer_sphere_id: "cs_5b7e14aa",
        cdk_customer_number: "112907",
        dispatch: "warranty_window_review",
        journal: "ACDOCI",
        target_window_hours: 24,
        write_to_dms: false
      }
    }
  },
  {
    id: "CS-0004", key: "cs_c04182de", name: "Chaleur Regional Freight", short: "Chaleur", kind: "Organisation",
    value: "CAD 910,000 trailing 12 months", units: 9, since: "2016",
    people: ["Y. Roy — dispatch", "L. Basque — accounts"],
    keys: ["CDK 108330", "TELUS +1 506 555 0288", "Marketing acct 90114"],
    identity: "Resolved. One candidate link to a person record held at 0.62.",
    cohort: "Voicemail not returned within two hours",
    headline: "Two voicemails past the two-hour window and a finance file drifting",
    vectors: {
      commercial:   { cur: "2 units, CAD 402,000", tgt: "2 units / year", gap: 0, note: "On target." },
      service:      { cur: "CAD 141,000", tgt: "CAD 160,000", gap: 12, note: "Slightly light." },
      parts:        { cur: "CAD 96,700", tgt: "CAD 110,000", gap: 12, note: "Steady." },
      finance:      { cur: "CAD 74,000 open, 51 days average", tgt: "under 30 days", gap: 58,
                      note: "Ageing has doubled since March with no dispute recorded against it." },
      warranty:     { cur: "1 open claim, 12 days", tgt: "under 30 days", gap: 0, note: "Within window." },
      relationship: { cur: "2 voicemails past 2 hours", tgt: "0 unreturned over 2 hours", gap: 70,
                      note: "Both from L. Basque, both about the finance file above." },
      marketing:    { cur: "Resolved, single identity", tgt: "One resolved identity", gap: 0, note: "Clean." }
    },
    disagreement: {
      field: "Billing address",
      a: { src: "CDK", val: "1120 Rue Principale, Bathurst NB", ts: "07:40", conf: "high" },
      b: { src: "Marketing platform", val: "PO Box 41, Petit-Rocher NB", ts: "yesterday", conf: "low" },
      ruling: "A post-office box and a street address are not a contradiction. Both held; neither overwrites the other."
    },
    action: {
      title: "Dispatch a callback on the finance file",
      to: "the business office",
      body: [
        "Return two voicemails from L. Basque, both past the two-hour window.",
        "Ageing has moved from 24 to 51 days since March with no dispute on file.",
        "Establish whether there is a dispute nobody recorded."
      ],
      envelope: {
        customer_sphere_id: "cs_c04182de",
        cdk_customer_number: "108330",
        dispatch: "callback_finance_ageing",
        journal: "ACDOCI",
        target_window_hours: 2,
        write_to_dms: false
      }
    }
  }
];

/* --------------- structural items : the digest that never empties --------------- */
const STRUCTURAL = [
  {
    id: "ST-1", views: ["craig", "tim"],
    title: "Five of the sixteen registered systems have no stated access route",
    scale: "16 systems registered · 11 reachable · 5 not",
    ref: "Design §7c, open item",
    trend: "Unchanged since the register was catalogued",
    cols: ["System", "Contributes", "Access route", "State"],
    rows: [
      ["Service scheduling", "Appointment events", "None stated", "Known, unreachable"],
      ["Reputation platform", "Review and response history", "None stated", "Known, unreachable"],
      ["Tyre programme portal", "Parts and fitment", "None stated", "Known, unreachable"],
      ["Finance submission portal", "F&I outcomes", "None stated", "Known, unreachable"],
      ["Legacy lead capture", "Historic leads", "None stated", "Known, unreachable"]
    ],
    more: "The remaining eleven each have an owner, a route and a confidence tag.",
    method: [
      "The register is the authority on what exists. This surface only records whether each entry has a landing, an owner, an access path and a confidence tag.",
      "A system with no access route is recorded as known-but-unreachable. It is never quietly dropped, because a dropped source becomes an invisible gap in every number downstream.",
      "The source inventory is not closed until the register is confirmed complete and current.",
      "Least defensible assumption named first: that the five have no route rather than a route nobody has written down yet."
    ],
    actions: ["Request the access route", "Mark as deferred", "Park"]
  },
  {
    id: "ST-2", views: ["tim", "craig"],
    title: "118 candidate identity links are waiting on stewardship",
    scale: "3,904 resolved entities · 118 candidates · 0 auto-merged",
    ref: "Design §8",
    trend: "Rising with each marketing extract",
    cols: ["Rule that produced it", "Candidates", "Median score", "Auto-merged"],
    rows: [
      ["Fuzzy business name + city", "61", "0.71", "0"],
      ["Fuzzy person name + phone stem", "34", "0.66", "0"],
      ["Address normalisation collision", "15", "0.58", "0"],
      ["VIN-to-owner, historical", "8", "0.81", "0"]
    ],
    more: "Every link carries the score and the rule that produced it. None was thresholded away.",
    method: [
      "Deterministic matching runs first — CDK customer number, normalised phone, VIN-to-owner. Only the remainder reaches fuzzy matching.",
      "Least defensible assumption named first: that a 0.81 VIN-to-owner link is safer than a 0.71 name-and-city link. It is not obviously so, which is why neither is auto-merged.",
      "Merges are appended, timestamped and attributed events. An unmerge restores both sides.",
      "A destructive merge is a defect, not a design choice."
    ],
    actions: ["Open the stewardship queue", "Export the candidates", "Park"]
  },
  {
    id: "ST-3", views: ["luke", "tim"],
    title: "Peer variance is blank because the 20 Group figures are not yet accessible",
    scale: "11 declared targets · 6 internal · 5 peer-derived · 5 blank",
    ref: "Design §10",
    trend: "Blocked, not degrading",
    cols: ["Target", "Source of the figure", "Current", "Target", "Variance"],
    rows: [
      ["Absorption", "20 Group guide", "—", "—", "blank pending access"],
      ["Parts gross per RO", "20 Group guide", "—", "—", "blank pending access"],
      ["Service labour rate", "20 Group guide", "—", "—", "blank pending access"],
      ["Units per salesperson", "20 Group guide", "—", "—", "blank pending access"],
      ["Warranty claim age", "Internal", "31 days", "under 30 days", "+1 day"]
    ],
    more: "Blank variance fields stay blank. They are not estimated, interpolated or filled with a plausible figure.",
    method: [
      "A guessed peer figure is worse than an absent one, because it will be quoted back as though it were measured.",
      "Least defensible assumption named first: that the guide figures will be comparable to this dealership's definitions when they do arrive. They may not be, and the definitions will need reconciling before the variance column means anything.",
      "The five internal targets are populated because their definitions are held in the index and their derivation is inspectable.",
      "Nothing on this row is a criticism of anybody. It is an access dependency with a name on it."
    ],
    actions: ["Record the dependency", "Send the definition list ahead", "Park"]
  },
  {
    id: "ST-4", views: ["luke", "craig"],
    title: "Three of the eleven targets have no declared owner or version",
    scale: "11 targets · 8 versioned in the index · 3 undeclared",
    ref: "Design §6 and §12 question 7",
    trend: "Undeclared since the model was first drafted",
    cols: ["Target", "Declared by", "Version", "Last changed"],
    rows: [
      ["Voicemail returned within two hours", "Index, versioned", "v1.2", "2026-07-14"],
      ["Warranty claim under 30 days", "Index, versioned", "v1.0", "2026-06-02"],
      ["Units per year, per account", "Undeclared", "—", "—"],
      ["Parts revenue per account", "Undeclared", "—", "—"],
      ["Marketing identity resolution", "Undeclared", "—", "—"]
    ],
    more: "An undeclared target still produces a gap on the sphere. It just produces one nobody has agreed to.",
    method: [
      "Targets are declared in the index repository, versioned there, and never hard-coded into a model.",
      "Changing what the dealership is aiming at is a committed decision with a date and an author on it, not a silent edit to a query.",
      "Least defensible assumption named first: that the three undeclared targets are currently being derived from last year's actuals. If so, the sphere is measuring the dealership against its own past rather than against an intention.",
      "This card exists because declaring a target costs one commit and leaving it undeclared costs every number that depends on it."
    ],
    actions: ["Draft the three declarations", "Take to the agreement holder", "Park"]
  }
];

/* --------------- index repository : pointers, never payload --------------- */
const INDEX_CARDS = {
  "customer.legal_name": {
    canonical: "customer.legal_name",
    names: [
      ["CDK", "NAME1 / CUSTNAME"],
      ["Call platform", "account_label"],
      ["Marketing platform", "Company"],
      ["Canonical", "customer.legal_name"],
      ["SAP-side alignment", "BUT000-NAME_ORG1"]
    ],
    pointer: "azure-postgres · sphere · customer · legal_name",
    width: "Source width wins — CDK carries 60 characters against the SAP default of 40. The widening is recorded.",
    governance: ["Personal data: organisation name, low sensitivity", "Retention: per source, unsigned", "Gate: never committed to GitHub", "Decision record: design §5"]
  },
  "contact.phone_primary": {
    canonical: "contact.phone_primary",
    names: [
      ["CDK", "PHONE1"],
      ["Call platform", "ani_normalized"],
      ["Marketing platform", "Phone"],
      ["Canonical", "contact.phone_primary"],
      ["SAP-side alignment", "ADRC-TEL_NUMBER"]
    ],
    pointer: "azure-postgres · conformed · contact · phone_e164",
    width: "Normalised to E.164 in the conformed layer. The source-native string is retained in landing, unmodified.",
    governance: ["Personal data: yes", "Retention: per source, unsigned", "Erasure: resolves through the identity layer", "Gate: never committed to GitHub"]
  },
  "vehicle.vin": {
    canonical: "vehicle.vin",
    names: [
      ["CDK", "VIN"],
      ["ePortal", "vin17"],
      ["Canonical", "vehicle.vin"],
      ["SAP-side alignment", "EQUI-SERGE"]
    ],
    pointer: "azure-postgres · sphere · vehicle · vin",
    width: "17 characters, fixed. Service and warranty history hang from the vehicle, not from the person who booked the appointment.",
    governance: ["Personal data: indirect identifier", "Retention: per source, unsigned", "Gate: never committed to GitHub", "Decision record: design §8"]
  },
  "interaction.voicemail_return_delta": {
    canonical: "interaction.voicemail_return_delta",
    names: [
      ["Call platform", "vm_return_delta"],
      ["CDK", "no equivalent"],
      ["Canonical", "interaction.voicemail_return_delta"],
      ["SAP-side alignment", "extension journal ACDOCI"]
    ],
    pointer: "azure-postgres · sphere · interaction · voicemail_return_delta",
    width: "Interval. Null where call direction or extension identity is missing — such records contribute to cohort counts but never score an individual.",
    governance: ["Personal data: employee-attributable, restricted", "Journal: ACDOCI, never ACDOCA", "Gate: never committed to GitHub", "Decision record: design §5 and §7b"]
  },
  "finance.open_ar_balance": {
    canonical: "finance.open_ar_balance",
    names: [
      ["CDK", "ARBAL"],
      ["Canonical", "finance.open_ar_balance"],
      ["SAP-side alignment", "ACDOCA, universal journal"]
    ],
    pointer: "azure-postgres · sphere · finance · open_ar_balance",
    width: "Currency, CAD. Ties out to the general ledger through the reconciliation contract rather than being recomputed.",
    governance: ["Personal data: no", "Journal: ACDOCA, unmodified", "Gate: never committed to GitHub", "Decision record: design §5"]
  }
};

/* which index card a face row points at */
const FACE_FIELDS = {
  commercial:   ["customer.legal_name", "finance.open_ar_balance"],
  service:      ["vehicle.vin"],
  parts:        ["customer.legal_name"],
  finance:      ["finance.open_ar_balance"],
  warranty:     ["vehicle.vin"],
  relationship: ["interaction.voicemail_return_delta", "contact.phone_primary"],
  marketing:    ["customer.legal_name", "contact.phone_primary"]
};

/* --------------- stewardship queue --------------- */
const CANDIDATES = [
  { id: "L-1", a: "Miramichi Forest Haulage Ltd (CDK 104882)", b: "Miramichi Forestry Haulage (Marketing 88213)",
    score: "0.74", rule: "Fuzzy business name + city", why: "One word differs. Same city, same phone stem, different phone tail." },
  { id: "L-2", a: "Miramichi Forest Haulage Ltd (CDK 104882)", b: "R. Savoie (Marketing 88907)",
    score: "0.62", rule: "Fuzzy person name + phone stem", why: "A person at the organisation, not the organisation. Affiliation edge, not a merge (§8)." },
  { id: "L-3", a: "Chaleur Regional Freight (CDK 108330)", b: "L. Basque (Marketing 90114)",
    score: "0.62", rule: "Fuzzy person name + phone stem", why: "Same shape as L-2. Person to organisation." },
  { id: "L-4", a: "Fundy Bay Seafood Transport Inc (CDK 112907)", b: "Fundy Bay Transport (Legacy lead capture)",
    score: "0.58", rule: "Address normalisation collision", why: "Legacy lead capture has no stated access route, so the right side cannot be re-read to confirm." }
];
