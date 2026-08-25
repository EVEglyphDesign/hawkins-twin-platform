# Warranty GENE — DMS pull (wireframe)

Proves that Luke's own CDK Drive and Lightspeed EVO logins pull real warranty
data when driven headlessly. Everything runs on GitHub Actions in this repo.
No Fortellis subscription. No Lightspeed Client Portal API subscription.
No Azure yet — this is the wireframe Tobias will move to Azure.

## What's here

- `intake/index.html` — the credential-intake page Luke opens in a browser.
  Live at [Warranty GENE — Credential intake](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/dms-pull/intake/).
- `readers/run.py` — Playwright entry point, called by the workflow.
- `readers/cdk.py` — CDK Drive login + VIN lookup.
- `readers/lightspeed.py` — Lightspeed EVO login + VIN lookup.
- `pulls/` — output lands here as `{side}-{vin}-{timestamp}.json`.
- `credentials.age` — written by the `store-credentials` workflow.
  age-encrypted with the repo's public key. Decrypted only inside
  the `pull-vin` workflow at read time.

## One-time setup (10 minutes)

Do this once, before Luke arrives.

1. **Generate an `age` key pair locally**:
   ```
   age-keygen -o warranty-gene-age.key
   ```
   This prints one line to stderr — the public key, starting with `age1...`.
   The file contains the private key, starting with `AGE-SECRET-KEY-...`.

2. **Add two GitHub repo secrets** in
   [repo Settings → Secrets and variables → Actions](https://github.com/EVEglyphDesign/hawkins-twin-platform/settings/secrets/actions):
   - `AGE_PUBLIC_KEY` — the `age1...` public key
   - `AGE_PRIVATE_KEY` — the full contents of `warranty-gene-age.key`
     (the private key line beginning `AGE-SECRET-KEY-...`)

3. **Set the public key in the intake page**. Edit
   `warranty-gene/dms-pull/intake/index.html` and replace
   `REPLACE_WITH_AGE_RECIPIENT_PUBLIC_KEY` with the `age1...` public key.
   Commit and push. (The wireframe intake page emits base64 that the
   workflow re-encrypts to age server-side, so this is defence-in-depth,
   not the primary encryption.)

4. **Delete the local `warranty-gene-age.key` file** — you don't need it,
   GitHub Actions has both halves.

## When Luke arrives

1. **Send Luke the intake page**:
   [https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/dms-pull/intake/](https://eveglyphdesign.github.io/hawkins-twin-platform/warranty-gene/dms-pull/intake/)
2. Luke fills in:
   - Exact login URL for CDK Drive (his dealer's URL, not the marketing site)
   - CDK username, password
   - CDK MFA method (**preferred: TOTP** — if it's SMS or push, we need
     to switch it to TOTP for automation to work, or Luke has to approve
     each pull)
   - If TOTP: the base32 seed from the authenticator setup screen
   - Same for Lightspeed EVO
3. Luke clicks **Encrypt in browser**, copies the blob.
4. Luke (or you) opens the [Store credentials workflow](https://github.com/EVEglyphDesign/hawkins-twin-platform/actions/workflows/store-credentials.yml),
   clicks **Run workflow**, pastes the blob into the `payload` input, and runs.
   That writes `credentials.age` to the repo.
5. Get one test VIN for the Peterbilt side and one test VIN for the BRP side
   from Luke — VINs he has in his DMS today, ideally where he already knows
   the warranty answer so we can eyeball whether the pull is right.
6. Open the [Pull VIN workflow](https://github.com/EVEglyphDesign/hawkins-twin-platform/actions/workflows/pull-vin.yml):
   - `side = cdk`, `vin = <the Peterbilt VIN>`, run
   - `side = lightspeed`, `vin = <the BRP VIN>`, run
7. When the workflow finishes, look in `warranty-gene/dms-pull/pulls/` —
   there will be a JSON file per run with:
   - `success: true` and an `extracted.raw.main_text` field containing
     whatever CDK/Lightspeed showed for that VIN, OR
   - `success: false` with an `error` and a Playwright trace attached to
     the workflow run as an artifact.

## First-run reality

The selectors in `cdk.py` and `lightspeed.py` are best-effort. There is a
real chance the first pull fails because the login page or the VIN-search
control is shaped differently than the reader expects. When that happens:

- The workflow uploads a Playwright trace as an artifact
- The trace file lets us step through what the reader actually saw
- We adjust the selectors in `readers/cdk.py` or `readers/lightspeed.py`,
  commit, and re-dispatch the workflow
- Luke does not re-enter anything — the credentials stay encrypted in the repo

Expected: one to three iterations before both sides pull cleanly. Every
iteration is a code change, not a Luke change.

## What comes out of a successful pull (v0.1)

A raw text dump of the VIN detail screen. That is deliberately dumb — we
capture everything CDK/Lightspeed shows for the VIN into a single field so
we can read the JSON, see what's actually in Luke's DMS record, and then
write targeted selectors (`base warranty start`, `base warranty end`,
`extended plans`, `open ROs`, etc.) in a second pass.

Once the targeted selectors exist, `extracted.warranty` fills in for real
and this becomes the step-1 input the blueprint's engine consumes.

## Moving to Azure (Tobias)

Everything above runs today from GitHub Actions using GitHub's ephemeral
Ubuntu runners and the encrypted credential file in the repo. To move it
into Hawkins's Azure tenant, Tobias:

1. Creates an Azure Container App or Function running the same
   `readers/run.py` script.
2. Replaces the `credentials.age` file read with an Azure Key Vault
   `Get Secret` call — one code change in `run.py`, ~4 lines.
3. Replaces the `git commit` write with an Azure Blob write, mirroring
   the same non-PII summary to the repo.
4. Schedules the container on the cadence Hawkins wants (nightly, hourly,
   or on-demand per VIN).

The reader modules (`cdk.py`, `lightspeed.py`) do not change.

---

© 2026 EVEglyphDesign · *Pour le bien-être du peuple*
