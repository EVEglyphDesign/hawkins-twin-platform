# Azure workstream — Hawkins Twin

**Owner:** Tobias Polly · **Status as of 2026-10-05:** design recorded; build status **not recorded in GitHub**.

This page is where the Azure side of the Hawkins Twin is written down, so Luke's Claude (and
anyone else's) can see what exists in Hawkins Azure without a phone call. Sections 1–2 are what
the repositories already say. Section 3 is for Tobias to fill in.

> **This repository is public.** Record names, states and counts of *objects* only.
> No hostnames, IP addresses, connection strings, subscription or tenant IDs, keys, row data,
> dealer figures or customer names. Anything more detailed goes in the private
> [eve-hawkins-paccar-smartlinq](https://github.com/EVEglyphDesign/eve-hawkins-paccar-smartlinq)
> repository, with a one-line pointer here.

---

## 1. Why Azure is in the design

The blueprint (`EgD-BP-HAWKINS-TWIN-001`, §2 and §6) puts **custody** in Hawkins-owned Azure:

- Dealer rows live in **Hawkins Azure PostgreSQL**. Public repositories hold schema, rules and
  aggregates only.
- WarrantyGENE, the Owner Console and the Customer Sphere read **only** that record, through
  marts. Nothing reads source extracts directly.
- Nothing is promoted into it until the **data-use authorisation** and the **compliance sign-off**
  exist, and the **six promotion gates** pass
  ([DATA-QUALITY.md](https://github.com/EVEglyphDesign/eve-hawkins-cdk-twin/blob/main/warehouse/DATA-QUALITY.md)).

## 2. What is designed (blueprint §7)

| Step | What | Acceptance | State |
|---|---|---|---|
| B1 | Azure delivery in Hawkins' tenant: PostgreSQL, Key Vault, GitHub Actions with OIDC, no stored secrets | Deploys from the Hawkins GitHub organisation | Designed |
| B2 | Loaders for CDK, registration, SmartLINQ and the PACCAR API pull, each writing a SHA-256 manifest | Re-runnable; manifests committed | Designed |
| B3 | Warehouse and marts from one schema definition | The six promotion gates pass on loaded data | Designed (schema built in the CDK twin) |
| B4 | Surface wired to the marts instead of `aggregates.json` | Every number traces to a mart | Designed |
| B5 | Ask over the twin MCP, read only, explicit `peterbilt` / `torque` scope | Every answer shows its source rows | Mock only |
| B6 | Tie-out against full CDK history and ten historical warranty claims | Counts equal, breaks logged with an owner | Designed |

Schema already in GitHub that targets this database:
[`schema/ddl/smartlinq.sql`](https://github.com/EVEglyphDesign/eve-hawkins-paccar-smartlinq/blob/main/schema/ddl/smartlinq.sql)
(private repo) and the CDK twin warehouse DDL.

## 3. What exists today — for Tobias to complete

*Fill each row with names and states only. Replace "not recorded" when known. Add a baton-log
line at the bottom when you edit.*

| Item | Answer |
|---|---|
| Azure tenant owner (Hawkins / other) | not recorded |
| PostgreSQL server provisioned? (yes / no / planned) | not recorded |
| Databases and schemas created (names) | not recorded |
| Tables loaded (names, and which extract date) | not recorded |
| Loaders built (names, language, where the code lives) | not recorded |
| PACCAR API pull: field list (names only, no values) | not recorded |
| PACCAR API pull: refresh cadence | not recorded |
| Twin MCP server: name | not recorded |
| Twin MCP server: tools exposed (names) | not recorded |
| Twin MCP server: scope rule enforced (`peterbilt` / `torque`) | not recorded |
| Key Vault in use? Secrets managed how? (no values) | not recorded |
| CI/CD: GitHub Actions with OIDC? Which repository deploys? | not recorded |
| Which of B1–B6 are done | not recorded |
| Where the detailed runbook lives (repo + path) | not recorded |

## 4. Open questions that touch Azure

1. Which DMS each site runs (CDK Drive, Procede Excede, Karmak) decides which loader is real.
2. Whether the August session-based DMS readers (Luke's login) ever write into Azure, given the
   vendor contract clauses recorded in the truck-mart repository.
3. Who in Peterbilt Atlantic owns the Azure subscription after handover.

## Baton log

| Date | Who | Did |
|---|---|---|
| 2026-10-05 | Claude (chat), for Dany | Created this page from the Integrated Blueprint draft. Section 3 left for Tobias; his work is not visible from EVEglyphDesign's GitHub connection. |

---

© 2026 EVEglyphDesign. Controlled copy.
