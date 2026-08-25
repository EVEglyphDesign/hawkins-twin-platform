"""
CDK Drive reader — Peterbilt Atlantic.

WIREFRAME state. Login selectors and warranty-screen navigation are
best-effort based on the general shape of CDK Drive's web login. The FIRST
run against Luke's actual dealer login will tell us exactly what the login
page and warranty screens look like — that first run will fail on the
navigation step and we adjust the selectors in-place. The Playwright trace
captured on failure lets us walk through what the reader saw without
another authentication.

Contract:
  pull(page, creds, vin, trace_dir) -> (extracted: dict, screens: [str])

  extracted must include (when successful):
    { "vin": str,
      "identity": {...},          # decoded VIN facts from the DMS
      "warranty": {
        "base": {"start": ISO, "end": ISO, "months": int, "miles": int},
        "extended": [...],        # PACCAR extended, CE033, aftertreatment, etc.
        "claims_open": [...],
        "raw_screens": [...],     # screenshot paths for provenance
      },
      "work_orders_open": [...],  # active ROs against this VIN
    }
"""

from pathlib import Path
from datetime import datetime, timezone

import pyotp


def _stamp(page, trace_dir: Path, label: str, screens: list) -> None:
    ts = datetime.now(timezone.utc).strftime("%H%M%S")
    p = trace_dir / f"cdk-{label}-{ts}.png"
    page.screenshot(path=str(p), full_page=True)
    screens.append(str(p.relative_to(Path.cwd())))


def _handle_mfa(page, creds: dict, trace_dir: Path, screens: list) -> None:
    method = creds.get("mfa", "none")
    if method == "none":
        return
    if method == "totp":
        seed = creds.get("totp_seed")
        if not seed:
            raise RuntimeError("MFA=totp but no totp_seed in credentials")
        code = pyotp.TOTP(seed).now()
        # CDK's TOTP prompt typically has a 6-digit input; we try common names.
        for sel in [
            'input[name="code"]',
            'input[name="otp"]',
            'input[id*="otp" i]',
            'input[id*="code" i]',
            'input[autocomplete="one-time-code"]',
        ]:
            if page.locator(sel).count() > 0:
                page.fill(sel, code)
                _stamp(page, trace_dir, "mfa-filled", screens)
                page.keyboard.press("Enter")
                page.wait_for_load_state("networkidle", timeout=30000)
                return
        raise RuntimeError("MFA=totp but no TOTP input field found on page")
    if method in ("sms", "push"):
        # We cannot bypass — the workflow will fail and Luke needs to change
        # to TOTP or approve manually.
        raise RuntimeError(
            f"MFA={method} requires an interactive step Luke has to take. "
            f"Ask Luke to switch to authenticator-app (TOTP) MFA on this account, "
            f"or run the pull headed (locally) so Luke can approve."
        )
    if method == "sso":
        raise RuntimeError(
            "MFA=sso — CDK is federated through Peterbilt/PACCAR identity. "
            "Requires the SSO IdP credentials, not the CDK ones. Capture those "
            "in the intake form as a separate account."
        )


def pull(page, creds: dict, vin: str, trace_dir: Path):
    """Log into CDK Drive as Luke and pull everything visible for `vin`."""
    screens: list[str] = []

    # 1. Login page.
    login_url = creds["url"]
    page.goto(login_url, wait_until="domcontentloaded", timeout=45000)
    _stamp(page, trace_dir, "login-loaded", screens)

    # CDK Drive login: username first, then Next, then password on the next screen
    # in most tenants. We handle both single-page and split-page shapes.
    if page.locator('input[type="password"]').count() == 0:
        # Split-page login — fill username, click Next.
        for sel in ['input[name="username"]', 'input[type="email"]', 'input[id*="user" i]']:
            if page.locator(sel).count() > 0:
                page.fill(sel, creds["username"])
                break
        else:
            raise RuntimeError("Could not find a username field on the CDK login page")
        for sel in ['button:has-text("Next")', 'button[type="submit"]', 'input[type="submit"]']:
            if page.locator(sel).count() > 0:
                page.click(sel)
                break
        page.wait_for_load_state("networkidle", timeout=30000)
        _stamp(page, trace_dir, "login-after-next", screens)

    # Password.
    for sel in ['input[type="password"]', 'input[name="password"]']:
        if page.locator(sel).count() > 0:
            page.fill(sel, creds["password"])
            break
    else:
        raise RuntimeError("Could not find a password field on the CDK login page")

    # If it was a single-page form, username might still be needed.
    if page.locator('input[name="username"]').count() > 0 and \
       not page.locator('input[name="username"]').input_value():
        page.fill('input[name="username"]', creds["username"])

    for sel in ['button:has-text("Sign in")', 'button:has-text("Log in")',
                'button:has-text("Login")', 'button[type="submit"]']:
        if page.locator(sel).count() > 0:
            page.click(sel)
            break
    page.wait_for_load_state("networkidle", timeout=45000)
    _stamp(page, trace_dir, "login-after-password", screens)

    # 2. MFA if any.
    _handle_mfa(page, creds, trace_dir, screens)
    _stamp(page, trace_dir, "post-mfa", screens)

    # 3. Navigate to VIN lookup / warranty screen.
    # WIREFRAME: the exact path here is dealership-configured in CDK Drive.
    # Common patterns:
    #   - a top-nav "Service" -> "Vehicle Inquiry" -> VIN
    #   - a global search box that accepts VIN
    # First-run behaviour: capture the post-login landing screen, look for
    # a search input by placeholder, and try that. If nothing matches,
    # save the DOM and let Luke tell us where to click.
    _stamp(page, trace_dir, "post-login-landing", screens)

    search_selectors = [
        'input[placeholder*="VIN" i]',
        'input[placeholder*="Search" i]',
        'input[aria-label*="search" i]',
        'input[type="search"]',
    ]
    searched = False
    for sel in search_selectors:
        if page.locator(sel).count() > 0:
            page.fill(sel, vin)
            page.keyboard.press("Enter")
            page.wait_for_load_state("networkidle", timeout=30000)
            _stamp(page, trace_dir, "after-search", screens)
            searched = True
            break

    if not searched:
        # Save the landing page HTML for offline inspection.
        html_path = trace_dir / f"cdk-landing-{datetime.now(timezone.utc).strftime('%H%M%S')}.html"
        html_path.write_text(page.content())
        raise RuntimeError(
            f"CDK: could not find a VIN search field on the post-login page. "
            f"Landing HTML saved to {html_path.relative_to(Path.cwd())} — "
            f"send it to the reader author and we adjust the selector for run #2."
        )

    # 4. Extract whatever the search returned.
    # WIREFRAME: dump the visible text of the main content area. This is
    # deliberately dumb — it captures everything CDK shows for the VIN so we
    # can look at the JSON and see what's actually in the DMS record for Luke's
    # account. Once we know the layout, we replace this with targeted selectors.
    body_text = page.locator("body").inner_text()
    main = page.locator("main, [role=main], #main, .main").first
    main_text = main.inner_text() if main.count() > 0 else body_text

    extracted = {
        "vin": vin,
        "identity": {
            "source": "CDK Drive",
            "dealer_url": creds["url"],
            "pulled_at": datetime.now(timezone.utc).isoformat(),
        },
        "raw": {
            "url_after_search": page.url,
            "page_title": page.title(),
            "main_text": main_text[:20000],  # cap to 20KB
            "body_length": len(body_text),
        },
        "warranty": {
            "base": None,
            "extended": [],
            "claims_open": [],
            "note": "WIREFRAME: raw-text dump. Targeted extractors added after first successful run.",
        },
        "work_orders_open": [],
    }

    return extracted, screens
