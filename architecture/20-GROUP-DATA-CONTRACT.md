# 20 Group Data Contract — Peterbilt Atlantic Digital Twin

Phase 1 of the Peterbilt Atlantic Digital Twin, "Side Car Twin & Historical Archive," establishes a
side-car data pathway from Hawkins / Peterbilt Atlantic's (New Brunswick) CDK dealer management system
through to a governed 20 Group performance surface, without ever touching, querying, or writing to the
live DMS. This document is the data contract for that pathway: it fixes what the restore must guarantee,
what the landing schema must enforce, which metrics the 20 Group performance set covers, how the model
layer is bound to reproducibility, and the gates that must clear before any real dealership data is
permitted to move. It covers the parties named in this phase of work: Hawkins / Peterbilt Atlantic and
PACCAR as the manufacturer context for the dealership's operations.

**Status: draft, Phase 1.**

## Source of truth

The entry point to this pipeline is the nightly backup set of the CDK dealer management system, restored
into an environment EVEglyphDesign controls — not the live DMS itself. This is a deliberate, non-negotiable
choice rather than a convenience.

Working from a restored replica rather than the production system rules out:

- **No production risk.** No read or write path touches the live DMS at any point in this pipeline. The
  dealership's day-to-day operations, transaction throughput, and system availability are unaffected by
  anything done in Phase 1.
- **No integration window.** There is no requirement to negotiate API access, connection quotas, batch
  windows, or vendor integration approval with CDK as a live system. The dependency surface with the
  production vendor relationship is eliminated for this phase of work.
- **Repeatable and disposable restore.** Because the working copy is a restore artefact, it can be
  discarded and rebuilt from a fresh backup set at will. Mistakes in schema design, extraction logic, or
  metric derivation cost a re-restore, not a production incident.

This posture holds for the whole of Phase 1. Any future write-back into CDK is out of scope here and is
addressed under Gates, below.

## Restore contract

The replica job — the process that takes a CDK backup set and produces a queryable restore in an
environment we control — must guarantee the following before its output is considered usable by any
downstream step:

- **Backup set identity and timestamp recorded.** Every restore is traceable to a specific backup set,
  identified and timestamped at the point of restore, not inferred after the fact.
- **Restore reproducible from scratch.** The restore procedure must be capable of being run again from the
  same backup set and produce an equivalent result. Nothing in the restore path may depend on manual,
  undocumented, or one-off steps.
- **Checksum / row-count reconciliation against the backup manifest.** The restored environment is
  reconciled against the backup manifest by checksum and row count before being accepted as faithful. A
  restore that cannot be reconciled is not a valid source for landing.
- **No network path from the replica back to production.** The replica environment is isolated such that
  it cannot reach, query, or otherwise affect the live DMS. This is an architectural property of the
  environment, not a policy statement.
- **Retention and disposal.** Restored replicas are retained only as long as needed for the current
  extraction cycle and are disposed of on a defined schedule, rather than accumulating indefinitely.

## Landing contract

The restored replica is landed into Postgres under an ASCII-safe schema of 21 objects and 443
confidence-tagged fields, with generated Postgres and Snowflake DDL and a preflight validator. The
following rules govern that landing:

- **ASCII-safe field handling.** All field and object names are normalised to an ASCII-safe form at
  landing time. Source system encoding quirks (extended characters, non-standard delimiters) are handled
  at the boundary and do not propagate into the landing schema.
- **Confidence tags carried through as column metadata.** Each of the 443 fields carries a confidence tag
  (reflecting how well its meaning, type, and provenance are understood) as column-level metadata in the
  landing schema — not as a separate, disconnected document. Confidence is queryable alongside the data
  it describes.
- **Preflight validator must pass before load.** No load proceeds unless the preflight validator has
  confirmed the incoming restore matches the expected 21-object, 443-field shape and passes its structural
  checks. A failed preflight blocks the load; it is not a warning to be overridden.
- **Load is idempotent and re-runnable.** Loading the same restore twice produces the same landed state.
  The load process may be re-run without manual clean-up as a precondition.
- **Every table stamped with source backup ID and load timestamp.** Every landed table carries the
  identity of the backup set it was sourced from and the timestamp at which it was loaded, so that any
  downstream figure can be traced back to a specific backup and load event.

Of the 21 landed objects, the ledger-side objects are not yet documented against known CDK schema
references. Verifying admin-level access to these ledger-side objects is the first verification target
for this pipeline, because several financial and absorption-related metrics in the 20 Group performance
set depend on them (see Notes column below).

## 20 Group performance metric set

Three full months of data are extracted for each cycle. Financial reporting is keyed to the middle month
of the three, so that boundary effects at the start or end of the extraction window cannot distort
month-over-month or trend figures.

| Metric | Domain | Source objects | Period basis | Notes |
|---|---|---|---|---|
| Parts inventory turns | Parts | Parts inventory, parts sales history | Rolling 3-month, keyed to middle month | Peer benchmark comparison BLANK pending Luke Weatherbie's 20 Group figures. |
| Parts fill rate | Parts | Parts orders, parts inventory | Middle month | Standard dealer metric; source objects expected in landed schema, not ledger-dependent. |
| Parts obsolescence | Parts | Parts inventory, aging buckets | Middle month snapshot | Peer benchmark BLANK pending Luke Weatherbie. |
| Stock order vs emergency order mix | Parts | Parts orders | Rolling 3-month | No ledger dependency; confirmable once parts order objects are validated. |
| Technician productivity | Service | Service repair orders, labour time records | Rolling 3-month, keyed to middle month | Depends on labour ledger objects not yet verified for admin access. |
| Technician efficiency | Service | Service repair orders, labour time records, flat-rate standards | Rolling 3-month, keyed to middle month | Depends on labour ledger objects not yet verified for admin access. |
| Effective labour rate | Service | Service repair orders, labour billing | Middle month | Ledger-side billing objects not yet verified; figure is provisional until confirmed. |
| Comeback rate | Service | Service repair orders, warranty/comeback flags | Rolling 3-month | Peer benchmark BLANK pending Luke Weatherbie. |
| Work-in-process ageing | Service | Open repair orders | Middle month snapshot | No ledger dependency; depends only on service repair order objects. |
| Truck sales unit gross | Truck sales (where applicable) | Sales deals, unit cost records | Middle month | Ledger-side deal-cost objects not yet verified for admin access. |
| Truck sales days in stock | Truck sales (where applicable) | Vehicle inventory, sales deals | Middle month snapshot | No ledger dependency; inventory-only calculation. |
| Absorption rate | Dealership | Parts, service, and truck sales gross; fixed operating expense | Rolling 3-month, keyed to middle month | Depends on ledger-side expense objects not yet verified for admin access; peer benchmark BLANK pending Luke Weatherbie. |
| Expense-to-gross | Dealership | Departmental expense, departmental gross | Rolling 3-month, keyed to middle month | Depends on ledger-side expense objects not yet verified for admin access; peer benchmark BLANK pending Luke Weatherbie. |

Peer benchmark fields and any Hawkins historical benchmark fields not yet extracted stay blank in the
performance surface rather than being estimated or guessed. Luke Weatherbie is the sole source for 20
Group peer benchmark numbers; until those are supplied, this document and the surface it describes treat
those cells as blank by design, not as a gap to be filled with an assumption.

## Model layer contract

The 20 Group performance surface is produced with the help of an Azure-hosted open-source model, run with
pinned weights and a versioned prompt set. This combination was chosen specifically for its absence of
drift and its predictable cost and performance profile, as opposed to a hosted commercial model whose
weights and behaviour can change outside our control.

The contract for this layer is:

- **Pinned model version and prompt version recorded with every output.** Every generated output —
  ranking, narrative, or work list — carries a record of the exact model version and prompt version that
  produced it.
- **Identical input must produce identical output.** Given the same landed data and the same pinned
  model/prompt combination, re-running the model layer must yield the same result. This is what "no
  drift" means operationally, and it is verifiable, not aspirational.
- **The model ranks and explains; it does not invent metric values.** The model's role is to prioritise,
  contextualise, and narrate findings that already exist in the data. It is not a source of any numeric
  metric value.
- **All numeric values come from SQL, never from the model.** Every number appearing on the performance
  surface is computed by SQL against the landed schema. The model consumes those numbers; it does not
  compute or restate them independently.
- **Every ranked item carries a traceable reason.** Where the model produces a prioritised work list, each
  ranked item is accompanied by a stated reason traceable to the underlying metric(s) and source objects,
  not a bare ranking.

## Gates

The following gates apply to Phase 1 and must clear before this pipeline is permitted to operate on real
dealership data:

- **Real dealership data does not move until Tim Hawkins's agreement is executed.** Until that agreement
  is in place, no real Hawkins / Peterbilt Atlantic data is extracted, landed, or processed by this
  pipeline.
- **Luke Weatherbie must have 20 Group access** before peer benchmark figures can be supplied into the
  performance surface; this is a precondition for the benchmark columns described above, independent of
  the Tim Hawkins agreement.
- **Synthetic and mock data stand in until both of the above clear**, and the pipeline shape — restore,
  landing schema, metric set, model layer — does not change when real data arrives. The purpose of
  building against synthetic/mock data now is precisely so that the transition to real data is a data
  swap, not a redesign.
- **Call-history ingestion uses a Peterbilt-owned TELUS service account, never personal credentials.** Any
  ingestion of call-history data for this or related phases is bound to a Peterbilt-owned service account
  with TELUS; personal credentials are not an acceptable substitute under any circumstance.
- **Craig Allen's 16-system register is the substrate** for this and adjacent digital twin work; signed
  user agreements and public access URLs are the first intake against that register, ahead of any deeper
  system-by-system integration.
- **Client-facing material stays separate from the protected internal origin thesis.** Anything prepared
  for client or dealership-facing consumption is kept structurally separate from the internal thesis and
  reasoning that underpins this programme of work.

## Open questions

- What is the actual field-level schema of the ledger-side objects in the CDK backup, and who at Hawkins /
  Peterbilt Atlantic or CDK can confirm it? (Best placed to answer: Tim Hawkins, via CDK's data dictionary
  or a CDK technical contact.)
- When will Luke Weatherbie's 20 Group peer benchmark data be available, and in what format? (Best placed
  to answer: Luke Weatherbie.)
- Does admin-level access to the ledger-side objects in the backup set already exist, or does it need to
  be separately requested and provisioned? (Best placed to answer: Tim Hawkins, as the party controlling
  DMS administrative access.)
- What is the expected cadence of the nightly backup set — is it genuinely nightly without gaps, and how
  far back does retention on the CDK side extend? (Best placed to answer: Tim Hawkins or the Hawkins IT
  contact responsible for CDK backup administration.)
- What is the target timeline for executing Tim Hawkins's agreement, and does it gate only real-data
  ingestion or also earlier pipeline build-out steps? (Best placed to answer: Tim Hawkins.)
- Which of the 16 systems in Craig Allen's register, beyond CDK, are expected to feed Phase 2 or later
  phases of the Digital Twin, and in what order? (Best placed to answer: Craig Allen.)
- What are the specific terms of the Peterbilt-owned TELUS service account for call-history ingestion —
  who provisions and owns it operationally once ingestion begins? (Best placed to answer: Craig Allen, in
  coordination with Peterbilt Atlantic's TELUS account contact.)
- What separation mechanism (technical or procedural) will be used to keep client-facing material apart
  from the protected internal origin thesis, and who owns enforcing that boundary on an ongoing basis?
  (Best placed to answer: the EVEglyphDesign programme lead for this engagement.)

---

© 2026 EVEglyphDesign. Controlled copy. Key ID EgD-KEY-2026-07.

*Pour le bien-être du peuple.*
