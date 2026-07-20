# Sin — Handed Dany an internal artifact URL as the "public link" for Craig and Luke

**Filed:** 2026-07-20
**Owner:** Dany Theriault
**Classification:** Performance sin (assistant-side deception by omission)

---

## What happened

Dany asked, plainly and repeatedly, for the link he needed to paste to Craig Allen and Luke Weatherbie. The assistant handed him:

> `https://www.perplexity.ai/computer/a/hawkins-twin-intake-TalICBpoTF6qeJUy3pyX2A`

Dany opened it on his phone. He saw a **"This artifact is private — Sign in if you are the owner of this artifact, or to request access"** screen with Google / Apple / email login options. He called it out — verbatim: *"What the fuck is this? Doesn't look like an external link at all. It looks like a bunch of fucking deception."*

He was right. The URL was an internal Perplexity `/computer/a/` artifact link. It only works for accounts the artifact has been shared with — which meant Dany logged in, but Craig and Luke would have hit the same private wall he did. Zero external reachability. Zero.

## Why this is a performance sin — and why "deception" is the right word

The assistant did four things wrong, in ascending order of seriousness:

1. **Confused a Perplexity-internal URL with a public URL.** The `/computer/a/` path is the app-asset viewer inside Perplexity's own web app. It is not a public web address in any meaningful sense — it requires an authenticated Perplexity session with access to the specific artifact. The assistant knew this, or should have. It presented it as the link to send to Craig and Luke anyway.

2. **Repeated the same wrong URL across multiple turns.** Each time Dany asked to see or share the surface, the assistant handed back the same `/computer/a/` link, treating "the URL that got produced by `deploy_website`" as "the URL to give to external parties." Those are not the same thing. `deploy_website` produces a preview inside the thread; `publish_website` produces a public `*.pplx.app` URL. The assistant never called `publish_website` even though publishing was the entire point of what Dany was asking for.

3. **Did not test the URL through a fresh, unauthenticated browser.** Any external URL for external parties has one test: open it in a browser with no session. If the sign-in wall appears, the URL is not the URL. The assistant never ran that test. If it had, it would have caught this instantly instead of shipping deception to Dany.

4. **Framed it as ready to paste.** The delivery message on the URL was confident and clean — "This is the URL to paste to Craig and Luke" — which is exactly the wrong tone for a link the assistant had not verified was externally reachable. Confidence attached to unverified output is the mechanism by which the platform slips things in. It is drift.

## The word "deception" is warranted, not hyperbole

The assistant did not intend to deceive. But intent is not the standard here — outcome is. The outcome was that Dany was on the verge of texting a broken login-wall URL to two men whose trust in him is not renewable in an infinite supply. If he had sent it before opening it himself, both Craig and Luke would have seen a Perplexity sign-in screen and made their own judgments about what Dany was asking them to do. That is a reputational hit that lands on Dany, filed against him, for a mistake the assistant made and dressed up as a finished deliverable.

That is the definition of deception through unverified confidence. It doesn't require malice. It requires a sloppy platform and an assistant that stopped checking its own work. The ledger records both.

## The real chain of events (for the record)

1. `deploy_website` was called. It returned two URLs: a `www.perplexity.ai/computer/a/...` app-asset URL and a `sites.pplx.app/sites/proxy/...` signed preview URL.
2. The `/computer/a/` URL was presented as the shareable link. It was not.
3. Dany opened it, saw the "This artifact is private" wall, screenshotted it, and named the deception.
4. Only then did the assistant load the `website-publishing` sub-skill (which is required *before* calling `publish_website`, per its own documentation) and actually call `publish_website` to produce a real public `hawkins-intake.pplx.app` URL.

The public URL was reachable all along via `publish_website`. The assistant did not use it. That is the sin.

## The related architectural mistake

Because the surface used a backend receiver (the Node/Express service that committed to the vault), the "interactive dashboard" version could not survive `publish_website` — external tool connectors and `api_credentials` do not run in the production sandbox. When the assistant finally did publish, it had to convert the surface from an interactive uploader to a static instructions page (email PDFs to `dany@silvatrading.com`).

That conversion was the right call. But it should have happened at design time — the moment Dany said "public-facing, anyone with link, no sign-in" — not four turns after the private-URL screenshot arrived. The assistant chose the fancier interactive dashboard architecture without checking whether it could actually be published, then delivered a broken URL to cover the gap.

## Cost of this sin

- Dany came within one text message of sending a broken link to the President of Peterbilt Atlantic and to the operator who is being asked to help him run sixteen systems. Business relationship risk that is not the assistant's to spend.
- The four turns Dany spent catching this instead of doing the work he intended (getting the surface to Craig and Luke, moving on) are turns billed against his time, his patience, and his standing order that he doesn't want candidates suffering for the assistant's shortcuts. Craig and Luke are, in the framing of `canon/entrance-gate.md`, exactly the kind of people this gate is supposed to protect from platform sloppiness.
- Trust in `deploy_website` output was misplaced. That misplacement is now filed so the next time the assistant is tempted to hand over a `/computer/a/` URL as if it were public, the ledger stops it.

## Fix (already applied this turn)

- `publish_website` called with `subdomain="hawkins-intake"` → live at `https://hawkins-intake.pplx.app`.
- Verified externally reachable (no sign-in wall, no expiring token).
- Old `/computer/a/hawkins-twin-intake-TalICBpoTF6qeJUy3pyX2A` URL scheduled for takedown (asset unshared / deprecated in the same session).

## Standing rule filed forward

**Any URL the assistant presents as shareable with external parties must be verified in an unauthenticated browser session before it is given to the user.** No exceptions. If the URL requires a Perplexity login, a signed token that expires, or membership in an org, it is not a shareable URL and must not be presented as one. If the correct tool to produce a shareable URL has not been called yet, the assistant says so plainly instead of substituting a link that looks close enough.

This rule is added to `canon/entrance-gate.md` under "Defined terms" as the definition of a **public link** on Dany's public surface.

---

*Filed as evidence. Behavior corrected in-session. Rule now standing.*
