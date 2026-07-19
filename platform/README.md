# platform/ — Single-Stack Reasoning Layer

This folder holds the **baseline technology** for the Hawkins twin: a proven, production AI stack that we retarget per engagement rather than rebuild. It is the single stack we apply to everything — heavy lifting for the custom models.

## What's here

| File | What it is |
|---|---|
| [`REASONING-LAYER.md`](./REASONING-LAYER.md) | The distilled, reusable canon — architecture, reasoning path, ephemeral compute, models, security, and the retarget sequence. **Start here.** |
| `2026-07-17_Discovery_Architecture_Extract.pdf` | Source of record — full architecture extract (SC-DISC-EXTRACT-2026-07). |
| `2026-07-17_Discovery_Business_Brief.pdf` | Source of record — business case / Revenue Leakage brief (SC-DISC-BRIEF-2026-07). |

## The idea in one line

**One engine, one stack — retarget the *source*, not the build.** The bounded LangGraph agent (plan → retrieve → narrate), Microsoft Teams delivery, Langfuse audit trail, and closed-network security posture are reused unchanged. Only the source adapter, ephemeral DuckDB/graph compute, and the in-tenant model deployment are configured per engagement. Roughly three-quarters of any new rollout is reuse.

## How this maps to the Hawkins twin

The Hawkins/Peterbilt twin is one retarget of this stack:

1. **Source adapter** → point at the chosen Hawkins/Peterbilt live system's edit history (dealer systems, parts inventory, orders — reusing the dealer-parts-twin SAP-shaped schema rather than inventing a new model).
2. **Ephemeral DuckDB layer** → ranking/leakage/inventory summaries per session; add the graph only for relationship questions.
3. **Model + boundary** → confirm the in-tenant Azure Foundry deployment.
4. **Validate + open in Teams** → validate against a known period, then hand to Tim / Luke.

Same engine, audit trail, Teams experience, and security posture as the finance workstream that is already live — the twin funds a retargeting, not another platform.

## Provenance

Steel Cloud Solutions — *Reasoning Layer for Discovery* (SC-DISC-EXTRACT-2026-07) and *Revenue Leakage for Discovery* (SC-DISC-BRIEF-2026-07). Author: Tobias Polly, polly consulting e.U., 17 July 2026. Confidential.
