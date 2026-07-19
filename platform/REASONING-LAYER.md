# Reasoning Layer — Single-Stack Baseline

**Source:** Steel Cloud Solutions — *Reasoning Layer for Discovery* (SC-DISC-EXTRACT-2026-07) and *Revenue Leakage for Discovery* (SC-DISC-BRIEF-2026-07), Tobias Polly / polly consulting e.U., 17 July 2026.
**Status:** Baseline canon for the Hawkins twin and every downstream retarget.
**One line:** One engine, one stack — retarget the *source*, not the build.

This is the load-bearing baseline. It captures the proven AI stack stripped of any single source system, so the same engine can be pointed at the Hawkins/Peterbilt twin and everything after it. The two source PDFs live alongside this file; this is the distilled, reusable version.

---

## The core claim

The engine was commissioned in November 2025 under a single narrow mandate (RFQ 125): a **zero-data-leakage AI agent** that reads the *edit history* of enterprise transactions, tells a person in plain language which records changed and by whom, and delivers it inside Microsoft Teams — all inside a locked-down network boundary. It is live in production today on a finance workstream (the Revenue Leakage Model).

Pointing it at a new data source is a **configuration change, not a new build.** Roughly three-quarters of every new rollout is reuse — only the source, the measures, and the delivery cards change. The agent does not change between use cases; only the source in front of it and the questions asked of it do.

**This is the baseline technology for the custom models — the single stack we apply to everything, retargeted per engagement.**

---

## Architecture — four parts, each replaceable

```
1. Source adapter  →  2. Reasoning        →  3. Delivery
   edit history in     LangGraph agent        Microsoft Teams
   (SAP · custom ·     plan → retrieve →      answer + cards
    data lake)         narrate
                            ↑
                4. Observability — Langfuse records every step;
                   any answer can be replayed end-to-end

        (all inside a secure network boundary)
```

| Part | Role | Reuse |
|---|---|---|
| **Source adapter** | Crosses the boundary from the customer's system, presents edit history in one uniform shape. Source is interchangeable. | Configured per source |
| **Reasoning** | Bounded agent: plans what to fetch, fetches it, writes the plain-language answer. | Reused unchanged |
| **Delivery** | Microsoft Teams. Plain English in, written answer + structured card out. No SQL, no dashboard. | Reused unchanged |
| **Observability** | Langfuse under everything; every step recorded so any answer can be reconstructed and defended. | Reused unchanged |

**Reused as-is:** reasoning agent, Teams delivery, Langfuse audit trail, security boundary.
**Configured per engagement:** source adapter, ephemeral compute layer, model deployment. **None is a new build.**

---

## How it reasons — bounded, three steps, auditable

```
Router  →  Executor  →  Synthesizer
reads the   fetches the   turns results into
question,   data the       a plain-language
plans steps plan calls for answer
```

Three steps, three model calls, one answer — bounded every time. A fixed path (not open-ended improvisation) is deliberate: cheaper to run, easier to budget, and fully auditable for regulated data.

**Worked example (Revenue Leakage):**
> **Q:** Where are we leaking the most revenue on last quarter's orders?
> **A:** Order 4500012345 was edited 12 times after booking — the most this quarter. Eight of those changes reduced the net price, all by two editors. Across the quarter, discount and net-price fields account for 71% of post-booking edits, concentrated in three accounts. Those three are where booked revenue is leaking fastest.

Two properties make it safe over sensitive data:
- **Bounded and auditable** — the plan and every data lookup are stored with the answer. No open-ended tool-call loop, so cost and behaviour are predictable and reviewable.
- **Zero data leakage, fully replayable** — runs inside a closed network boundary; Langfuse records each step end-to-end. "How do I know the AI didn't make it up?" → replay it and see.

---

## Where the data lives — query live, compute ephemerally

No standing copy of the customer's data. The engine queries the live system on demand, pulls back only what a question needs, and builds the analysis in an ephemeral working layer that exists for the session and then disappears. There is no second database of sensitive records to secure, reconcile, or destroy — because there is no second database.

### Source adapters (uniform "edit history" interface)

| Live source | Typical use | Status |
|---|---|---|
| SAP S/4 & DataSphere | Finance and order edit history | Live today |
| Custom / in-house systems | Own matter and billing systems | Ready to point |
| Staffing & HR platforms | Bullhorn, Workday record changes | Planned |
| Data lake / warehouse | Consolidated cross-system history | Planned |

SAP is one supported source, not a requirement.

### Ephemeral compute engines

| Working engine | Best at | Lifespan |
|---|---|---|
| **DuckDB** (tabular) | Ranking, counting, trend/leakage summaries over large volumes; cross-source joins; fast follow-up slicing | Per session |
| **Ephemeral graph** | "How is this connected to that?" — tracing edits, people, matters across many hops | Per session |
| Persistent store (optional) | A standing pre-computed view only when a customer specifically wants one retained | Retained (exception) |

DuckDB is the general-purpose workhorse — same engine, pointed at different data. The graph is added only when the value is in the relationships rather than the totals.

---

## The models — swappable behind one interface

Reasoning runs on models hosted in **Azure AI Foundry**, inside the same network boundary — prompts and data never leave the customer's Azure tenant. The model is a configuration value, not a hard-wired dependency.

| Option | Notes | Residency |
|---|---|---|
| Foundry — GPT-5.6 Sol | Current default; strongest structured reasoning | In-tenant |
| Foundry — Kimi K3 | Alternate hosted model, same interface | In-tenant |
| Self-hosted (open model) | For a fully on-premises requirement | On-premises |

---

## Security posture — built to pass a review

- Registration to reach into a customer system **lives in the customer's own tenant**; Steel Cloud holds only the operating secret and rotates it. Customer keeps the power to revoke at any time.
- Data handled during a run is **destroyed on a fixed schedule**; the network **defaults to deny**.
- Every answer is logged for replay.
- **Human-approval gate** on anything that leaves the building: the AI proposes, a person disposes.

Access is scoped, revocable, and observable end-to-end. Nothing here requires trusting a black box.

---

## Paid-for lessons (inherit the hardened version, not the first draft)

- **Bounded beats clever** — predictable cost, answers in seconds, an auditable plan. Clears a compliance review where an open-ended agent would not.
- **Swapping the data source is configuration, not a rebuild** — the whole basis of the retargeting claim.
- **Business-language layer over the tools** — users ask in their own words; changing a tool never means rewriting prompts.
- **Full replay (Langfuse)** — the honest answer to "did the AI invent this?" is to replay it step by step.
- **Human-approval gate** — what makes automation acceptable in regulated work.
- **One engine across engagements** — ~¾ reuse; only source, measures, delivery cards change.
- **Known limit, fixed up front** — the first build kept session memory in-process (single instance); the production path swaps in a shared store to scale to many users. Named up front rather than discovered late.

---

## Pointing the engine at a new twin (e.g. Hawkins)

A short, low-risk sequence rather than a fresh build:

1. Point the source adapter at the chosen live system's edit history.
2. Stand up the ephemeral DuckDB layer; add the graph only if relationship questions demand it.
3. Confirm the model deployment and network boundary in the customer's tenant.
4. Validate answers against a known period, then open it in Teams.

**The position:** the engine, audit trail, Teams experience, and security posture are already built and running. A new twin does not fund another platform — it funds a retargeting. The fastest way to move the P&L is to reuse what already works.

---

*Distilled from the two Steel Cloud Discovery briefings (SC-DISC-EXTRACT-2026-07, SC-DISC-BRIEF-2026-07) archived in this folder. This markdown is the reusable canon; the PDFs are the source of record.*
