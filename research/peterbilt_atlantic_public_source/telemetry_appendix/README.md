# Telemetry Appendix — Peterbilt Atlantic

> This appendix is deliberately placed at the end of the repository, not the front. The first thing Tim, Craig, and Luke should see when they open this repo is themselves — accurately, respectfully, and in their own words. Telemetry is the bridge, not the pitch.

## Why this appendix exists

Peterbilt Atlantic already runs one of the most telemetry-forward product stacks in Atlantic Canada. Every truck on the lot ships with the plumbing:

- **SmartLINQ Remote Diagnostics** — factory-standard on Peterbilt Model 579, 589, 567, 548, and the full EV line (579EV / 520EV / 220EV). Real-time fault-code streaming, remote parameter updates, and predictive maintenance flags are already coming off the trucks Craig markets and Luke's Extreme Torque team services (see [company/inventory_overview.md](../company/inventory_overview.md)).
- **FleetRight** — Peterbilt's fleet-side data console, already offered by Peterbilt Atlantic through the parts and service channel.
- **PACCAR Solutions** — engine, drivetrain, and duty-cycle telemetry piped back to the PACCAR cloud.

The trucks are already talking. The question is who owns the conversation.

## The data-sovereignty framing

The canon we're carrying forward (see the DSC / ARK / EVE / SpaceX unification work in the parent knowledge base):

1. **Data is the new oil.** Every SmartLINQ event, every PACCAR Solutions telemetry burst, every dealer-side service record is an economic asset. Today most of that value pools upstream — at PACCAR, at OEM cloud vendors, at whichever telematics broker gets between the truck and the fleet.
2. **The dealer is the natural sovereign.** Peterbilt Atlantic is the only party in the chain that touches the customer, the truck, the technician, and the financing simultaneously. That is the unlock position.
3. **Telemetry-first ownership** means the dealer group operates its own indexed, permissioned record of every truck it has ever sold or serviced — cross-referenced against the OEM feed, not dependent on it. When the customer asks "what happened to my truck," the dealer answers first, with better data, faster.

This is the same unlock-protocol pattern we're applying elsewhere in the canon — commoditize the stack, remove lock-in, hand the keys to the operator.

## What that would look like at Peterbilt Atlantic

Not a proposal. A sketch — for Tim, Craig, and Luke to react to.

- **A private, dealer-owned truck registry.** Every unit sold across the nine centres, indexed by VIN, with a lifetime record: spec, delivery photos (Craig already publishes many of these on the blog — see [company/website_sweep.md](../company/website_sweep.md)), service history, SmartLINQ event stream, warranty status, ownership chain.
- **Craig's marketing surface, upgraded.** Every "Built in Canada — Driven by You" story ([source](https://fr.peterbiltatlantic.com/blog/built-in-canada---driven-by-you--101690)) already lives on the blog. Attach each story to its VIN in the registry and the marketing content compounds — every new customer story strengthens the record for the next one.
- **Luke's technology mandate, made concrete.** If Luke is the chosen technologist meant to scale this globally (as we understand from the framing), the registry is the artifact. It is scalable, licensable to sister dealer groups, and demonstrable in a demo.
- **Global scaling path.** Peterbilt has ~400 dealer locations across North America and international affiliates. The pattern that works for 9 centres in Atlantic Canada works for 400. That is the "convert and scale globally" objective in operational terms.

## What we are NOT saying

- We are not saying Peterbilt Atlantic's current stack is deficient. It is not.
- We are not saying PACCAR / Peterbilt corporate is adversarial. They are not.
- We are not proposing anything that requires Peterbilt Atlantic to break franchise obligations, share customer data improperly, or violate any OEM agreement.
- We are not asking anyone to sign anything.

The point of this appendix is simply: **you already own the sovereign position. Here is what it looks like when you operate from it.**

## Next steps (only if the reader wants them)

1. A 30-minute walk-through with Craig on how the registry would attach to the existing blog / marketing surface.
2. A separate technical scoping conversation with Luke on where the SmartLINQ / FleetRight / PACCAR Solutions feeds terminate today and what a dealer-owned mirror would require.
3. A one-page summary for Tim on the economics — what it costs to stand up, what it returns, and what it protects.

None of these happen unless Tim, Craig, and Luke want them to.

---

*This appendix is part of the Peterbilt Atlantic public-source repository. All company facts referenced here are cited to public sources documented elsewhere in this repository. The telemetry framing is our contribution and is offered for discussion, not asserted as fact about Peterbilt Atlantic's current operations or intentions.*
