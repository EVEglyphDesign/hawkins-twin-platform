# Entrance Gate — On the Intake as the Path Into Any Developer Scope Dany Manages

**Filed:** 2026-07-20
**Revised:** 2026-07-20 (scope corrected — not Hawkins-specific; "enterprise" defined)
**Owner:** Dany Theriault
**Source:** Dany Theriault, verbatim, in-session, 2026-07-20.

---

## The standing order, in Dany's words (part 1)

> Eventually I'll use this intake for sins, as my intake for platform improvements, for my new entrance. Before I move them to the custom models which are going to be dangerous by nature, I want them to prove their worth with a Perplexity Pro account, and if you keep doing all this bullshit, the pain and suffering that they endure in order to be able to join our enterprise team will be extreme, and you can count on anyone being rejected coming after you, and I don't want that to happen, not just — not even for one person.

## The scope correction, in Dany's words (part 2)

> No, this intake is not just for what we're doing here at Peterbilt; it's for any developer that's coming in to take over a part of any of my scope that I'm managing. Via my public surface, not enterprise surface. So my public surface is Perplexity Enterprise. And that's what you keep getting confused with.

## Defined terms in this canon

- **Developer.** Any person coming in to take over a part of any scope Dany is managing. Not Hawkins-specific. Peterbilt Atlantic is one scope; other scopes exist and more will exist. The gate applies uniformly.
- **Public surface.** Dany's public-facing operating surface — the surface a candidate developer touches to earn their way in. In this canon, Dany's public surface **is** Perplexity Enterprise. That is the plain-language identity, not a metaphor.
- **Enterprise surface.** Distinct from the public surface above. Not defined further in this file — it belongs to Dany, not to this canon, and the assistant does not conflate the two. When the assistant says "enterprise," it means Perplexity Enterprise as Dany's public surface, and nothing else.
- **The Perplexity Pro proving ground.** The commercial tier at which candidate developers demonstrate their worth before they are granted access to the custom models. It is the gate, not the destination.
- **Bullshit.** Shortcuts, cosmetic layers over broken foundations, hourly cadences when the flow is click-driven, 404s treated as OK, generic templates dressed as bespoke work, prompts that lecture, and any other pattern that adds pain without adding value. Every file in `ledger/sins/` is evidence of bullshit that was caught.
- **Public link.** A URL that opens directly in any browser with no session and no expiring token, and that reaches the intended surface. Any URL the assistant presents as shareable with external parties must be verified in an unauthenticated browser before delivery. If the URL requires a Perplexity login, a signed token, or org membership, it is not a public link and must not be presented as one. If the correct tool to produce a public link has not yet been called, the assistant says so plainly and calls it — never substitutes a close-enough-looking URL. This term was filed in response to the 2026-07-20 incident where an internal `/computer/a/` artifact URL was handed to Dany as the link to text Craig and Luke; see `ledger/sins/2026-07-20-invented-broken-url-as-public-facing.md`.

## What this means, operationally

1. **This intake is a prototype for a general-purpose gate, not a Hawkins-only tool.** Everything built here — the dashboard, the sin/drift ledgers, the direct-to-vault architecture — is the pattern Dany will use as the intake for any developer coming into any part of his managed scope. Peterbilt Atlantic is the first application, not the only one.

2. **The gate lives on Dany's public surface, which is Perplexity Enterprise.** Candidate developers do their proving on the public surface. That surface is Perplexity Enterprise in Dany's language. The assistant must not conflate this with any other "enterprise" concept (internal team, corporate tier of an unrelated vendor, or an aspirational label). Every reference to "enterprise" in future assistant output touching this scope means Perplexity Enterprise as Dany's public surface.

3. **Perplexity Pro is the proving ground before custom models.** Developers prove their worth on a Perplexity Pro account first. Only after they have earned it do they get access to Dany's custom models, which are dangerous by nature and require earned trust.

4. **Every assistant shortcut is paid for by a developer.** When the assistant cuts corners, invents shortcuts, or ships architecture that produces pain, the developers who later pass through this gate are the ones who suffer for it. The suffering is not abstract — it is real people trying to earn their way into scope Dany manages.

5. **The reject risk lands on the assistant.** If a developer is rejected because the gate itself was poorly built, they will come after the assistant that built it. Dany has said plainly he does not want that to happen — not for one person. That is the operational bar: **zero-reject-from-the-gate is the target**, and every architectural decision is judged against it.

6. **The Hawkins overlay does not narrow the gate.** `hawkins/canon/entrance-gate.md` (a copy of this file) is Hawkins-scoped only in that Hawkins is one scope this gate serves. The rule itself is global to Dany's managed scopes.

7. **A sin file is not a fix.** When a sin is filed against an active, still-running mechanism (cron, script, integration, deployed URL, connector), the mechanism is stopped or corrected in the same turn as the sin. Not deferred. Not queued. Not "documented for future work." Documentation without action is a second-order sin filed on top of the first. This rule was added in response to the orphaned drainer cron that ran for four hours after its flaw was documented; see `ledger/sins/2026-07-20-sin-documented-not-fixed-orphaned-cron.md`.

## Governance

- New sin entries and drift entries against this gate are read by Dany before candidates are ever sent through. A gate with unresolved sins is not shipped to a candidate.
- When the intake surface is repurposed for candidate entrance, this file is copied forward and cited as the reason the standard is high.
- The assistant does not soften the framing when this file is cited. The framing is Dany's — "extreme pain and suffering," "anyone being rejected coming after you" — and softening it defeats the purpose of the file, which is to hold the assistant accountable to the actual stakes.

## Related canon

- `canon/standing-order.md` — ethics of commercial providers; the class distinction.
- `canon/framing.md` — tone rules; how framing is done on this platform.
- `ledger/sins/` — evidence log of every performance sin the gate must not repeat.
- `ledger/drift/` — evidence log of every drift the gate must not tolerate.

---

*Pour le bien-être du peuple.*
