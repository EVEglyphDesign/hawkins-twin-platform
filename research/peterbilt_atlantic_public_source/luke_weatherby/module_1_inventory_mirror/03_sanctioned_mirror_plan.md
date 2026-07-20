# Step 2 — Sanctioned Mirror Plan

**Status: BLOCKED pending Step 1 sign-off.**

This page will remain a draft until [`02_what_luke_may_do.md`](./02_what_luke_may_do.md) contains a green list from Dany Theriault and Tim Hawkins.

## Draft shape (not authorized yet)

When authorized, the mirror plan will follow the same three-input pattern the SAP twin uses:

### Input A — Public developer documentation and APIs

- **CDK Fortellis** ([developer.fortellis.io](https://developer.fortellis.io/)) for the CDK-side data model, subject to Fortellis developer terms
- **PACCAR / Peterbilt** publicly documented dealer and parts endpoints (subject to what is actually published and permitted)
- **BRP** publicly documented parts and dealer resources (subject to what is published and permitted)

These are the sanctioned mirror path. They are documented for developers precisely so integrators do not have to reverse-engineer the systems.

### Input B — Luke's own sanctioned exports

Reports and exports Luke is entitled to run and archive as part of his role, per the sign-off in Step 1. Committed with any customer / employee / financial data redacted per the sign-off's guidance.

### Input C — Luke's personal notes

Luke's own words describing what he has learned. Always Luke's to commit.

### Target — EVE Glyph Postgres schema, SAP-shaped

The three inputs land in the same Postgres schema pattern used by the SAP twin, so downstream twins can join across BRP and PACCAR inventory without further translation work.

---

*This is a placeholder describing the shape of the plan. It is not authorization to perform any of the activities above. Authorization comes only from the sign-off in Step 1.*
