# Reconciliation Contract

**Programme:** EVEglyphDesign — Peterbilt Atlantic Digital Twin, Phase 1
**Parties:** Hawkins / Peterbilt Atlantic (New Brunswick) and PACCAR
**Agreement holder:** Tim Hawkins
**20 Group access:** Luke Weatherbie
**16-system register:** Craig Allen
**Constraint:** the live CDK dealer management system is never written to.

---

## 1. Purpose, and why two lanes

The twin's advanced analytics and decision support layer is fed by two lanes that land in the same Postgres database. They are deliberately different in character, and the difference is the point.

- **Lane A, the backup lane**, is built from a full restore of the CDK backup set, followed by delta-only refreshes. It feeds a model running straight from the backup to the 20 Group performance set. This lane is complete and trusted — it is a faithful copy of what CDK actually held — but it lags, because it is only ever as current as the last backup and the delta refreshes applied against it.
- **Lane B, the API lane**, is pulled from the CDK API and structured by a data mart library built from harvested application metadata, reusing as much of the SAP model as possible. This lane is current — it reflects what is happening in the system today — but it is partial and entitlement-bound, since the API only exposes what Peterbilt Atlantic's entitlements permit, and only the objects CDK chooses to surface through that interface.

Each lane checks the other. The backup lane's completeness catches what the API cannot see; the API lane's currency catches what the backup has not yet absorbed. Neither lane is asked to be everything, which is why reconciliation between them, rather than a single unified feed, is the design.

A divergence between the lanes does not mean the twin is broken. It means one of a small number of concrete things: the API lane knows about a change the backup has not yet caught up to (lag), the backup lane holds an object the API cannot see (an entitlement gap), the two sides disagree about a value that both claim to hold (a genuine variance), or the shape of the data itself has drifted between the two structures (schema drift). Reconciliation exists to say which of these it is, not to silently decide who is correct.

---

## 2. Reconcile as a function

Reconciliation is an **executable function**, called on demand — never a background process. As the operator put it, "we don't need to reconcile them unless we want them executable." It must be cheap to run on a narrow scope, precisely so that calling it is never a decision anyone has to think twice about.

**Signature**

```
reconcile(
  scope: object_set | metric_set,     -- which objects or 20 Group metrics to compare
  window: time_range,                  -- the period under comparison
  lane_versions: {
    backup_set_id: string,             -- identifies the exact backup restore + deltas
    api_pull_id:   string              -- identifies the exact API pull / cursor
  },
  tolerance_profile: string             -- reference to a versioned tolerance configuration (see §6)
) -> {
  run_record:      RunRecord,          -- who/when/what-scope/what-versions
  matched_counts:  MatchSummary,       -- counts matched within tolerance, by object/metric
  variance_rows:   VarianceRow[],      -- rows/metrics that differ beyond tolerance
  exception_set:   Exception[]         -- classified exceptions raised by this run (see §5)
}
```

**Guarantees**

- **Read-only** against both lanes: reconciliation never mutates Lane A or Lane B source data, and never touches the live CDK system.
- **Deterministic**: given the same scope, window, lane versions and tolerance profile, the function returns the same result every time.
- **Re-runnable**: it may be called repeatedly against the same or overlapping scope without side effects accumulating incorrectly.
- **No side effects beyond its own run record and exceptions**: the only things written are the run record itself and any exceptions raised. It does not update conformed values, does not resolve variances, and does not decide precedence — that is a separate, explicit act (see §4).
- **Not scheduled by default**: there is no timer. It is invoked when someone — an operator, a scheduled report generation step, or an analyst — actually needs a reconciled answer for a given scope and window.

---

## 3. Grain of comparison

Reconciliation can compare at three grains, and choosing the right one is mostly a question of cost versus what question is being asked.

| Grain | What it compares | When appropriate | Relative cost |
|---|---|---|---|
| **Row-level key-and-hash** | Each row's business key, with a content hash of its comparable fields, across both lanes | Investigating a specific object, or narrowing down which records within a flagged aggregate actually differ | Highest — requires reading and hashing full row sets on both sides |
| **Aggregate control totals** | Sums, counts, or checksums per object and period (e.g. total invoice count and value for a dealership-month) | Routine confirmation that a given object and period agree overall, before spending effort on row-level detail | Moderate — one pass over each side, no row matching |
| **Metric-level comparison** | The 20 Group figures each lane independently produces (e.g. gross profit per department) | Confirming the actual deliverable — the 20 Group performance set — agrees between the backup-fed model and the API-fed mart, which is the figure that ultimately matters to Luke Weatherbie's audience | Lowest per check, but only as trustworthy as the row and aggregate layers beneath it |

The cheapest first pass is aggregate control totals: if totals agree, there is no need to descend further. Row-level key-and-hash is reserved for narrowing down a control-total mismatch to the specific rows responsible. Metric-level comparison is the outward-facing check — it is what tells Tim Hawkins and PACCAR whether the number on the 20 Group report can be trusted — but it is only as reliable as the row and aggregate reconciliation underneath it, so it should never be run as the sole check.

---

## 4. Precedence and overwrite

The precedence rule, in the operator's own terms: **the API can overwrite what is in the backup-and-recovery lane; but if a subsequent change arrives and there is a variance, it is logged as an exception.**

This is narrower than it sounds, and the narrowness is deliberate:

- The API overwrites backup values **only within entitled scope** — it cannot overwrite what it cannot see, and it must not be treated as authoritative for objects outside its entitlement.
- It overwrites **only for objects the API is authoritative for**. Where the backup lane is the sole complete record of an object, the API's silence is not licence to overwrite; it simply means that object stays sourced from the backup.
- It **never overwrites silently**. Every overwrite in the conformed layer records: the backup value, the API value, which source won, and the timestamp of the overwrite.

The precedence rule has a second half that matters as much as the first: if a **later** change arrives and shows a variance against something that has already been reconciled, that later change does not quietly win by virtue of arriving after. It raises an exception instead. Precedence at the point of first reconciliation is not a standing licence for every future API value to overwrite forever without scrutiny — a subsequent disagreement against an already-reconciled position is exactly the kind of event the exception mechanism exists to catch.

---

## 5. Exception taxonomy

| Code | Class | Trigger | Default severity | Response |
|---|---|---|---|---|
| EX-01 | Variance within tolerance | Values differ but the difference is within the declared tolerance for that field class | Informational | Logged, no action required; visible in run record for audit |
| EX-02 | Variance beyond tolerance | Values differ by more than the declared tolerance | Warning | Surfaced for review; conformed value held pending resolution |
| EX-03 | Row in one lane only | A key exists in Lane A or Lane B but not the other, with no known reason | Warning | Investigate whether it is lag, an entitlement gap, or a genuine data issue |
| EX-04 | Row missing from both after a known change | A row expected to exist (per a known change event) is absent from both lanes | High | Escalate immediately; suggests an upstream failure, not a reconciliation timing issue |
| EX-05 | Late-arriving change | A change appears in one lane materially after the window it logically belongs to | Informational to Warning | Re-run reconciliation for the affected window once both lanes have caught up |
| EX-06 | Lane lag beyond threshold | The backup set's as-of point is older than the agreed maximum lag relative to the API pull | Warning | Flag lane currency on the surface; consider triggering a fresh backup restore or delta refresh |
| EX-07 | Entitlement gap | The API cannot see an object that exists in the backup lane | Informational | Confirm entitlement scope is as expected; not treated as a data fault |
| EX-08 | Schema or field drift | The structure or field definition differs between the harvested API mart and the backup-derived model | High | Data mart library and mapping reviewed before further reconciliation on the affected object |
| EX-09 | Repeated variance on the same key | The same key produces a variance exception across consecutive reconciliation runs | High | Escalated beyond routine review; treated as a candidate systemic issue, not a one-off (see §9) |

---

## 6. Tolerances

Exact-match comparison is the wrong default for almost every field class, because it manufactures noise rather than signal: a monetary value differing by a rounding fraction, or a timestamp differing by the seconds between an API pull and a backup checkpoint, is not a meaningful disagreement between the lanes.

| Field class | Tolerance approach | Rationale |
|---|---|---|
| Monetary | Small absolute and/or percentage tolerance (declared, not assumed) | Rounding and currency-handling differences between the backup-derived model and the SAP-reused mart should not register as variances |
| Count | Zero or near-zero tolerance, but windowed for lag | Counts should generally match exactly once both lanes are caught up to the same window; a mismatch during lag is expected and should not alarm |
| Timestamp | Tolerance expressed as a duration (e.g. within the known lag window) | The two lanes are captured at different moments by design; comparing timestamps exactly would flag the lane design itself as an exception |
| Free text | Normalised comparison (case, whitespace) rather than byte-exact | Free text fields carry no material business meaning in small formatting differences |
| Coded value | Exact match, but against a shared code mapping | Coded values must resolve to the same meaning even where the two systems use different underlying codes; the tolerance is really a mapping correctness question |

Tolerances are declared in **versioned configuration**, never hard-coded into the model or the reconciliation function itself. This means a tolerance change is a reviewable, dated, attributable event — not a silent code change — and different tolerance profiles can be applied to different scopes or windows without altering the function's logic.

---

## 7. Lag and the daily picture

The backup lane is only ever as current as its backup set: it is as-of the point the backup was taken, plus whatever delta refreshes have since been applied. The API lane is as-of the pull time of its most recent call against the CDK API. These are two different clocks, and the surface presenting the twin's output must always show both as-of markers alongside any figure drawn from either lane.

This is not a cosmetic requirement. Without both markers visible, someone reading the 20 Group performance set has no way of knowing whether they are looking at a figure that is hours old (backup-derived) or minutes old (API-derived), and no way of knowing whether an apparent change in the number reflects a real change in the dealership or simply the two lanes catching up to each other. The as-of markers are what prevent a stale figure from being read as live.

---

## 8. What the model may and may not do

Numeric values in the twin come from SQL — from the reconciled Postgres tables and the run records the reconciliation function produces — never from the model. The model's role is strictly downstream of the arithmetic:

- It **classifies** exceptions against the taxonomy in §5.
- It **explains** an exception in plain terms, drawing on the two source values and the run record.
- It **ranks** exceptions by likely importance or urgency, to help a human decide what to look at first.

The model does **not adjudicate which lane is right**. That is a precedence and business-authority question (§4), decided by rule and by the humans who own the objects in question, not inferred by the model from the data. Every exception the model surfaces must carry a traceable reason and both source values, so that a reviewer can verify the model's classification against the actual numbers rather than taking its word for it.

---

## 9. Exception ledger

Each exception is stored with:

- The exception code and class (per §5).
- The scope (object or metric), key, and window it relates to.
- Both source values (Lane A and Lane B) and their respective as-of markers.
- The tolerance profile version in force at the time.
- The run record ID of the reconciliation run that raised it.
- Timestamp raised, and current status (open, under review, closed).
- Who closed it and when, and the closure reason.

**Ageing and closure**: an exception remains open until a named person actively closes it with a recorded reason (e.g. resolved as lag, resolved as entitlement gap, corrected in source, accepted as tolerance-adjacent). Closure is not automatic and does not happen simply because a subsequent reconciliation run no longer reproduces the variance — the ledger entry stands as a historical record regardless.

**Recurrence**: if a previously closed exception recurs on the same key, it is not treated as a fresh, unrelated event. It is linked to its prior occurrence(s) and its severity is escalated by default (see EX-09), on the basis that a repeat on the same key suggests a systemic cause rather than an isolated incident, and warrants attention beyond the routine review a first occurrence would receive.

---

## 10. Open questions

1. What is the maximum acceptable lag between a backup set and the API pull before Lane A is considered stale for 20 Group reporting purposes? — best answered by **Tim Hawkins**, as agreement holder for what the performance set is expected to reflect.
2. Which specific objects fall inside the API's entitlement scope today, and is that scope expected to change? — best answered by **the CDK administrator**, who controls entitlement configuration.
3. Of the 16 systems on the register, which are in scope for Lane B's data mart library in Phase 1, and which remain backup-only? — best answered by **Craig Allen**, who holds the 16-system register.
4. Who is authorised to close an exception, and does that authority differ by exception class or severity? — best answered by **Tim Hawkins**, as the party accountable for the agreement.
5. Which 20 Group metrics does Luke Weatherbie actually consume, and should metric-level reconciliation be scoped to only those, at least initially? — best answered by **Luke Weatherbie**, given his 20 Group access.
6. Are there objects where the SAP-derived data mart model does not map cleanly onto CDK's structures, and how should schema drift there be handled ahead of time rather than discovered as an exception? — best answered by **Craig Allen**, given his familiarity with the system register.
7. What is the expected cadence of full backup restores versus delta-only refreshes, and does that cadence set a practical floor on Lane A's lag? — best answered by **the CDK administrator**.
8. Should reconciliation be triggered automatically around known events (such as month-end close), even though it is not run on a timer by default? — best answered by **Tim Hawkins**, as the decision affects how the performance set is presented under the agreement.

---

© 2026 EVEglyphDesign. Controlled copy. Key ID EgD-KEY-2026-07.

*Pour le bien-être du peuple.*
