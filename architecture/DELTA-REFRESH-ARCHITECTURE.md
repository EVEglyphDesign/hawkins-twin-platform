# Delta Refresh Architecture

**Programme:** EVEglyphDesign — Peterbilt Atlantic Digital Twin, Phase 1
**Sites:** Hawkins / Peterbilt Atlantic (New Brunswick), PACCAR
**Status:** Working architecture, for review
**Prepared for:** Tim Hawkins, Luke Weatherbie, Craig Allen

---

## 0. Ground rules

The live CDK dealer management system is never touched, queried, or connected to directly. All data is acquired from the CDK **BACKUP** system, restored into an environment we control, and landed in Postgres. A second, independent lane pulls from the CDK API where available. This document concerns what happens after the first full restore: how we keep the twin current without repeating the cost of that first restore on every refresh.

---

## 1. Purpose and the scalability rule

The operating requirement, stated plainly: one full backup and restore to seed the environment, and every refresh thereafter by delta only. A delta request must be specific enough that a CDK administrator can answer it directly — vague requests produce full-volume jobs in practice, whatever they are called.

We state this as a hard design rule, with a named guard that enforces it mechanically rather than by good intention:

> **Rule (the Proportionality Rule):** the cost of a refresh job — time, I/O, rows read, restore operations — must be proportional to the volume of *change* since the last successful watermark, never to the size of the database.
>
> **Guard: PROPORTIONALITY-GUARD.** Every refresh run declares, in advance, an expected change volume as a proportion of the object's last known row count. If a run's actual rows-scanned exceeds a declared multiple of that proportion, the run halts and raises rather than completing silently. See §4 for the mechanics and §6 for failure handling.

This rule is the test every strategy below must pass. A strategy that requires reading a whole table to find a small number of changed rows fails the rule even if it is fast today, because cost then scales with database size, not change size, and that is precisely what is not scalable and what "nobody will accept."

---

## 2. What we must ask CDK for, precisely

This is a quotable, yes/no list for the CDK administrator. Each answer unlocks or rules out a strategy in §3–§4. We ask these before designing anything further, because the honest answer may change which strategy is buildable at all.

1. **Do you offer incremental or differential backup sets, or is every backup a full backup?**
   *(Unlocks: if incremental/differential exists, Strategy A becomes viable outright.)*
2. **Is there a transaction log backup chain (log shipping), and if so, is a log position or LSN (log sequence number) exposed to us as consumers of the restore?**
   *(Unlocks: Strategy A via log-chain replay, the strongest form of native delta.)*
3. **For each core object (table), is there a per-row change marker — a last-modified timestamp, a row version number, a monotonic sequence, or equivalent audit column?**
   *(Unlocks: Tier 1 watermark pulls in Strategy B, object by object.)*
4. **Is that change marker populated on every write, including updates that touch only a subset of columns, and — separately — on deletes?**
   *(This is the single most consequential question. A marker that is not maintained on every write is worse than no marker, because it produces silent gaps. See Failure Mode 2, §6.)*
5. **Are deletes hard (row physically removed) or soft (row flagged, e.g. a status or `deleted_at` column)?**
   *(Hard deletes are invisible to any watermark-only pull; see §4 and Failure Mode 3.)*
6. **Do you run change data capture (CDC) or maintain change-tracking tables on any of these objects?**
   *(Unlocks: the strongest form of Strategy B, replacing Tier 2/3 diffing with a native change feed.)*
7. **What is the backup schedule and retention window, and how is a specific backup set identified (a backup set ID, timestamp, label, or similar)?**
   *(Required regardless of strategy — this is the identity half of every watermark. See §3 and §4.)*
8. **What are the row counts and on-disk size of the largest objects (parts inventory and movements, repair order and labour line history, ledger tables in particular)?**
   *(Needed to set the proportionality thresholds in the cost guard, §4, and to size Tier 3 sweep windows.)*
9. **Can a restore be taken more than once a day, and if so, at what practical cadence and cost?**
   *(Bounds refresh cadence regardless of which strategy applies — a delta strategy is only as fresh as the restore it is built on, unless the API lane in §0 supplements it.)*

**Which answers unlock which strategy, summarised:**

| Answer | Effect |
|---|---|
| Incremental/differential sets exist (Q1) | Strategy A viable directly |
| Log chain with exposed position (Q2) | Strategy A, strongest form |
| Change marker exists and is complete (Q3–Q4) | Strategy B, Tier 1, per object |
| Deletes are hard with no marker (Q5) | Tier 1 alone insufficient; Tier 2 or CDC required for that object |
| CDC or change-tracking present (Q6) | Strategy B upgraded — replaces Tier 2/3 |
| Backup identity and retention known (Q7) | Required baseline for either strategy's watermark |
| Sizes and counts known (Q8) | Required to calibrate the cost guard and Tier 3 sweep sizing |
| Restore cadence confirmed (Q9) | Sets the ceiling on refresh frequency |

If Q1, Q2 and Q6 are all "no" for a given object, that object runs under Strategy B in full (Tiers 1–3, per §4), and we build and own the delta logic ourselves.

---

## 3. Strategy A — native delta available

Applies where CDK exposes incremental/differential backup sets, or a log backup chain with an addressable position, per §2 Q1–Q2.

**Seeding:** one full restore, taken once, into the controlled environment and landed in Postgres. Every object's row count and a checksum (see §4) are recorded at this point regardless of strategy, so that Strategy A and Strategy B objects are auditable against a common baseline.

**Ongoing refresh:** each subsequent cycle applies either the next incremental/differential backup set, or replays the log chain from the last-applied log position forward. No full restore is repeated.

**The watermark** is a compound value: **(backup set identity, log position)**. Backup set identity alone is not sufficient, because two different administrators or environments could otherwise apply the same label to different underlying content; log position alone is not sufficient without knowing which base set it applies against. Both are stored together as a single watermark record per object (or per backup set, where the chain is not object-scoped).

**The run loop:**

1. Read the last successfully committed watermark for the object/chain.
2. Request the next backup set or log segment(s) after that watermark from CDK.
3. Restore/apply into the controlled environment.
4. Load the resulting change set into Postgres, stamped with source backup ID and load timestamp (per §4).
5. Verify the applied segment's ending position matches what was requested (no gap, no overlap).
6. Commit the new watermark only after verification succeeds.

**What is recorded** each cycle: backup set ID or log segment range applied, starting and ending position, row counts affected, duration, and outcome (success, gap-detected, failed). This is the same ledger discipline as §4's delta ledger, applied to the native case.

**Detecting a broken chain:** the chain is broken when the next available segment's starting position does not equal the last committed watermark's ending position — i.e., a gap. This is checked mechanically at step 5 above, before commit, never inferred after the fact.

**Healing a broken chain:** a broken chain cannot be repaired by "skipping ahead" — that silently loses changes and violates the same principle that makes Failure Mode 3 (§6) dangerous. The only sound repair is:

- Request the missing segment(s) from CDK if retention still holds them, and apply in order; or
- If the gap is unrecoverable (segment expired, chain broken at source), fall back to a reseed for the affected object per the Reseed Policy (§7), never a silent resume.

---

## 4. Strategy B — build our own delta utility

Applies where CDK cannot supply native incremental/differential sets or an addressable log chain (§2 Q1–Q2 both "no"), and no CDC/change-tracking exists (Q6 "no"). This is the default assumption for planning purposes until CDK administrator answers say otherwise, and it is the strategy we control end-to-end, so it carries the most detail.

### Seed

One full restore. For every object in scope: row count and a **checksum** are computed and stored — not a checksum of the whole table as a blob, but a per-row hash of business columns (same hash function used in Tier 2 below) rolled up into a stored hash index, plus an aggregate row count and aggregate checksum for fast whole-object sanity checks. This seed state is the baseline every later tier compares against.

### Tier 1 — watermark pull

Where a change marker exists and is populated on every write (§2 Q3–Q4 both "yes" for that object):

- Extract rows `WHERE change_column > last_watermark`, bounded to a specific range, not an open-ended scan.
- Apply a **small overlap window** behind the last watermark (re-pulling a short trailing slice, e.g. rows just before the prior cutoff) to absorb clock skew between the source system's clock and ours, and to catch writes that were mid-transaction (not yet visible) at the moment the previous pull's cutoff was taken. Rows re-pulled in the overlap are reconciled by key against what was already loaded — they are idempotent upserts, not duplicate inserts (see chunking/idempotency below).
- This is the cheapest tier and the default wherever the change marker is trustworthy.

### Tier 2 — key-plus-hash diff

Where no reliable change marker exists, or where Tier 1 cannot see deletes (§2 Q5), or as a periodic integrity check even on Tier 1 objects:

- Pull **only the primary key and a hash of the business columns** for every row — a narrow projection, never the full row.
- Compare the pulled key+hash set against the stored hash index from the seed (or from the last Tier 2 run).
- Three outcomes fall out of simple set and value comparison: a key present now but not in the stored index is an **insert**; a key present in both but with a changed hash is an **update**; a key present in the stored index but absent from the current pull is a **delete** (subject to the soft-delete caveat below).
- Only rows flagged by this comparison as new or changed are then fetched in full, and the local hash index is updated to match.

**Why the narrow projection keeps this affordable:** the expensive part of a diff — moving data — is proportional to row width times row count if full rows are pulled every time. A key and a fixed-width hash are a small, constant-size payload per row regardless of how wide or complex the underlying record is (labour lines, ledger schedules, parts records with many columns). Reading and comparing that narrow projection over the whole object is still cheaper than reading and moving the object itself, and it is the *comparison*, not a second full data pull, that identifies what actually changed. Only the genuinely changed rows incur the cost of a full-row transfer. This is what allows Tier 2 to stand in for a missing change marker without breaching the Proportionality Rule.

### Tier 3 — key-range sweep

For large objects where even a full key+hash pass is too costly to run in a single cycle (e.g. very large parts movement or transaction history tables):

- Partition the object's key space into fixed ranges (by primary key or a suitable partitioning column).
- Rotate through ranges across successive runs — one or a few ranges per cycle — so that no single run scans the entire object, while the full object is eventually covered on a rolling basis.
- Each range sweep uses the same Tier 2 key+hash comparison logic, scoped to that range only.
- This tier exists specifically so that "we build our own delta utility" does not quietly become "we read the whole table every night" for the largest objects.

### Deletes

- **Tier 1** cannot see hard deletes at all — a row that has been physically removed leaves no trace for a `WHERE change_column > watermark` pull to find. Tier 1 alone is only safe for delete detection where deletes are soft (a flag or `deleted_at` column that itself updates the change marker).
- **Tier 2/3** detect deletes correctly by construction, because a key missing from the current pull but present in the stored index is a delete, independent of whether the source system marks it in any special way.
- **Soft-delete caveat:** where deletes are soft, confirm during the CDK administrator conversation (§2 Q5) that the soft-delete flag itself updates the change marker on the same write. If it does not, a soft delete is indistinguishable from "no change" to Tier 1, and Tier 2/3 must be relied on for that object regardless of an otherwise-good change marker.

### Chunking, batch caps, resumability, idempotency

- Every extraction — Tier 1, 2, or 3 — runs in bounded chunks with a fixed batch cap (a maximum row count per request/transaction), never as one unbounded pull.
- Each chunk is independently committed and its progress recorded, so a run interrupted partway can resume from the last completed chunk rather than restarting from the beginning.
- All writes into Postgres are idempotent upserts keyed on the object's primary key: re-applying the same chunk twice (as happens deliberately in the Tier 1 overlap window, or accidentally on a retried failure) produces the same end state, not duplicates.
- Every loaded row is stamped with the **source backup ID** it was extracted from and a **load timestamp**, so provenance is traceable per row, not just per run.

### Cost guard

Direct enforcement of the Proportionality Rule (§1) inside Strategy B specifically:

- Before a run executes, it declares an expected change volume as a proportion of the object's last known row count (informed by history and, initially, by CDK administrator answers to §2 Q8).
- If the actual rows scanned during the run exceeds a declared multiple of that proportion, the run **halts and raises** — it does not proceed silently to completion. This applies per object, per tier.
- **Full-table reads are permitted only at seed time, or under an explicit, logged reseed** (§7). A Tier 2/3 run that finds itself effectively re-reading an entire large object without having been declared a reseed is exactly the condition this guard exists to catch — see Failure Mode 6, §6.

### Delta ledger

A structured record kept for every refresh run, Strategy A or B, forming the audit trail for the whole mechanism:

- Backup set ID used as the source for the run.
- Window covered (watermark range, or key range for Tier 3).
- Objects touched.
- Rows scanned versus rows changed (the figures the cost guard evaluates).
- Checksums (aggregate, before and after) for the objects touched.
- Duration.
- Outcome: success, halted (cost guard), gap-detected, or failed.

This ledger is the primary evidence, on request, that a given refresh cost what it should have cost — and the primary diagnostic when it did not.

---

## 5. Choosing a tier per object

Generic dealership/DMS object classes, pending confirmation of actual CDK schema detail from the administrator conversation in §2.

| Object class | Change marker available | Tier | Refresh cadence | Notes |
|---|---|---|---|---|
| Parts inventory and movements | Likely (quantity/last-updated fields common) | Tier 1, with periodic Tier 2 reconciliation | Frequent (intraday, restore cadence permitting) | High volume of small movements; good Tier 1 candidate if marker confirmed complete on every write |
| Service repair orders and labour lines | Likely on header, uncertain on lines | Tier 1 for headers; Tier 2 for labour lines until confirmed | Daily | Labour lines may update without a corresponding header timestamp change — confirm with CDK administrator |
| Work in process | Uncertain | Tier 2 initially | Daily or intraday | Transient, fast-changing state; hard deletes plausible when work closes out — treat cautiously until Q5 answered |
| Ledger and accounting schedules | **Unverified** | Tier 2, possibly Tier 3 for large history tables | Daily, conservative | Financial data — do not assume soft deletes or complete audit columns without explicit confirmation; treat as unverified until CDK administrator confirms Q3–Q6 |
| Customer and contact master | Plausible (audit columns common on master data) | Tier 1, with Tier 2 reconciliation | Daily | Master data typically smaller in volume; low risk if Tier 2 reconciliation run periodically |
| Unit inventory and sales | Plausible | Tier 1, with Tier 2 reconciliation | Daily | Moderate volume; status changes (sold, in-transit) are good Tier 1 candidates if marker confirmed |
| Vendor and purchase orders | Uncertain | Tier 2 initially | Daily | Confirm change marker completeness before promoting to Tier 1 |

Any row marked "Unverified" or "Uncertain" here is a placeholder pending the administrator's answers in §2 and must not be treated as confirmed for design purposes.

---

## 6. Failure modes

| # | Failure mode | Detection signal | Response |
|---|---|---|---|
| 1 | Broken log chain (Strategy A) | Next available segment's starting position does not match last committed watermark's ending position (§3, step 5) | Halt; attempt to source the missing segment from CDK if retention allows; otherwise reseed the affected object per §7 — never skip ahead |
| 2 | Change column not populated on updates | Tier 2 reconciliation run finds hash-changed rows whose change-marker value did not advance since the last Tier 1 pull | Demote the object from Tier 1 to Tier 2/3 until CDK administrator confirms marker completeness (§2 Q4); treat all prior Tier 1-only history for that object as suspect and reconcile via Tier 2 |
| 3 | Hard deletes invisible to a watermark pull | Tier 2/3 key-set comparison finds keys present in the stored index but absent from a fresh full or ranged pull, with no corresponding Tier 1 signal | Confirm delete semantics with CDK administrator (§2 Q5); for objects with hard deletes and no CDC, require periodic Tier 2/3 coverage rather than relying on Tier 1 alone |
| 4 | Hash collisions | A key+hash match masks an actual business-column change (theoretically possible with any hash function) | Negligible in practice: a well-distributed hash over business columns at DMS-scale row counts per object has a vanishingly small collision probability, and periodic full-row reconciliation on a sampled basis (not a full re-read) provides a backstop without breaching the Proportionality Rule |
| 5 | Restore unavailable on schedule | Expected restore window passes with no new backup set available, or CDK administrator confirms restore cadence cap is tighter than assumed (§2 Q9) | Refresh cadence for affected objects steps down to match actual restore availability; the API lane (§0) is evaluated as a supplementary source for objects it covers, rather than forcing an off-schedule restore |
| 6 | Delta run scanning far more than it changes | Cost guard trips: rows scanned exceeds the declared multiple of expected change proportion for that run (§4, cost guard) | Run halts and raises rather than completing; investigate whether the object's change marker has degraded (Failure Mode 2), whether a reseed is masking as a routine run, or whether the declared proportion needs recalibrating against updated CDK administrator figures (§2 Q8) |

---

## 7. Reseed policy

A reseed — a fresh full restore and re-seeding of an object or the whole environment, per §4's seed step — is justified only when:

- A broken chain (Failure Mode 1) cannot be healed by sourcing the missing segment(s); or
- An object has been demoted (Failure Mode 2 or 3) and its accumulated delta history is no longer trustworthy; or
- The delta ledger (§4) shows sustained cost-guard trips for an object that recalibration cannot resolve, indicating the delta approach itself has broken down for that object; or
- A scheduled integrity audit finds material drift between the stored hash index and a sampled reconciliation that cannot be explained by pending changes.

**Authorisation:** a reseed is not a routine operational action and is not triggered automatically by any tier or guard in this document — it is an explicit, logged decision. Given the agreement structure on this programme, authorisation rests with Tim Hawkins as agreement holder, informed by the delta ledger evidence assembled by the operating team; Craig Allen, as holder of the 16-system register, should confirm the reseed's system-of-record implications before it proceeds.

**Cost in time versus a delta run:** a reseed repeats the cost of the original full restore and seed — proportional to the size of the database, by definition — against a delta run's cost, which is proportional only to change volume. This is precisely the asymmetry the Proportionality Rule (§1) exists to avoid paying repeatedly; a reseed is the deliberate, occasional exception, not a fallback to be reached for casually.

---

## 8. Open questions

1. Does CDK offer incremental/differential backup sets for this dealership's environment, or is every backup full-only? — **CDK administrator**
2. Is a transaction log backup chain available, and is a log position or LSN exposed to us as consumers? — **CDK administrator**
3. Which core objects have a change marker populated on every write, including deletes, and which do not? — **CDK administrator**
4. Are deletes hard or soft across the ledger and accounting schedule tables specifically, given they are marked unverified in §5? — **CDK administrator**
5. What is the actual restore cadence PACCAR's/CDK's infrastructure supports — can a restore be taken more than once a day? — **CDK administrator**
6. Given Luke Weatherbie's 20 Group access, is there comparative or benchmark data from other dealerships that would validate our assumed object-class change rates in §5 before we calibrate the cost guard? — **Luke Weatherbie**
7. Does the 16-system register Craig Allen holds already document which of these object classes exist as distinct systems or modules within this dealership's CDK configuration, which would sharpen §5's table before the administrator conversation? — **Craig Allen**
8. Under the agreement Tim Hawkins holds, what access or introduction is available to reach the actual CDK administrator directly, rather than routing questions through intermediaries? — **Tim Hawkins**

---

© 2026 EVEglyphDesign. Controlled copy. Key ID EgD-KEY-2026-07.

*Pour le bien-être du peuple.*
