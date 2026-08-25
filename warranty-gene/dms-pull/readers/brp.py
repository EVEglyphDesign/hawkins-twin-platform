"""
BRP dealer portal reader — Torque Motorsports.

WIREFRAME. Same shape as cdk.py / lightspeed.py. BRP's dealer portal
(BRP Dealer Central / BOSSweb variants) presents warranty history,
unit master, campaigns/recalls, and claim status for the units the
dealer has sold or services.

First-run reality: BRP portals often front with Cloudflare or Akamai
bot management. Headless Chromium may be blocked before we get to the
login form. If that happens, the reader dies with a "detected as bot"
type page and we switch to playwright-stealth + a persistent context.
"""

from pathlib import Path
from datetime import datetime, timezone

import pyotp


def _stamp(page, trace_dir: Path, label: str, screens: list) -> None:
    ts = datetime.now(timezone.utc).strftime("%H%M%S")
    p = trace_dir / f"brp-{label}-{ts}.png"
    page.screenshot(path=str(p), full_page=True)
    screens.append(str(p.relative_to(Path.cwd())))


def _handle_mfa(page, creds: dict, trace_dir: Path, screens: list) -> None:
    method = (creds.get("mfa") or "none").lower()
    if method == "none":
        return
    if method == "totp":
        seed = creds.get("totp_seed")
        if not seed:
            raise RuntimeError("MFA=totp but no totp_seed in credentials")
        code = pyotp.TOTP(seed).now()
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
        raise RuntimeError("MFA=totp but no TOTP input field found")
    if method in ("sms", "push"):
        raise RuntimeError(
            f"MFA={method} requires interactive step. Switch to TOTP."
        )
    if method == "sso":
        raise RuntimeError(
            "MFA=sso — BRP is federated. IdP credentials needed, not portal."
        )


def pull(page, creds: dict, vin: str, trace_dir: Path):
    screens: list[str] = []

    page.goto(creds["url"], wait_until="domcontentloaded", timeout=60000)
    _stamp(page, trace_dir, "login-loaded", screens)

    # Detect bot-block page early.
    body_text = page.locator("body").inner_text().lower()
    if any(sig in body_text for sig in [
        "attention required", "cloudflare", "checking your browser",
        "access denied", "just a moment"
    ]):
        html_path = trace_dir / f"brp-bot-block-{datetime.now(timezone.utc).strftime('%H%M%S')}.html"
        html_path.write_text(page.content())
        raise RuntimeError(
            f"BRP: bot-management page detected on first hit. "
            f"HTML saved to {html_path.relative_to(Path.cwd())}. "
            f"Recovery: switch reader to playwright-stealth + persistent context."
        )

    # Fill username + password.
    for sel in ['input[name="username"]', 'input[type="email"]',
                'input[id*="user" i]', 'input[name="user"]',
                'input[id*="email" i]']:
        if page.locator(sel).count() > 0:
            page.fill(sel, creds["username"])
            break
    else:
        raise RuntimeError("Could not find a username field on the BRP login page")

    for sel in ['input[type="password"]', 'input[name="password"]']:
        if page.locator(sel).count() > 0:
            page.fill(sel, creds["password"])
            break
    else:
        raise RuntimeError("Could not find a password field on the BRP login page")

    for sel in ['button:has-text("Sign in")', 'button:has-text("Log in")',
                'button:has-text("Login")', 'button:has-text("Submit")',
                'button[type="submit"]', 'input[type="submit"]']:
        if page.locator(sel).count() > 0:
            page.click(sel)
            break
    page.wait_for_load_state("networkidle", timeout=60000)
    _stamp(page, trace_dir, "login-after-password", screens)

    _handle_mfa(page, creds, trace_dir, screens)
    _stamp(page, trace_dir, "post-mfa", screens)

    # BRP dealer portal — VIN/unit lookup. Common patterns:
    #   - top-nav "Warranty" > "Unit Inquiry" > VIN
    #   - global search box accepting VIN
    #   - a "Serial Number" field on the warranty page
    search_selectors = [
        'input[placeholder*="VIN" i]',
        'input[placeholder*="Serial" i]',
        'input[placeholder*="Unit" i]',
        'input[placeholder*="Search" i]',
        'input[type="search"]',
        'input[name*="vin" i]',
        'input[name*="serial" i]',
    ]
    searched = False
    for sel in search_selectors:
        if page.locator(sel).count() > 0:
            page.fill(sel, vin)
            page.keyboard.press("Enter")
            page.wait_for_load_state("networkidle", timeout=45000)
            _stamp(page, trace_dir, "after-search", screens)
            searched = True
            break

    if not searched:
        html_path = trace_dir / f"brp-landing-{datetime.now(timezone.utc).strftime('%H%M%S')}.html"
        html_path.write_text(page.content())
        raise RuntimeError(
            f"BRP: no VIN/serial search field on post-login landing. "
            f"HTML saved to {html_path.relative_to(Path.cwd())}."
        )

    body_text_full = page.locator("body").inner_text()
    main = page.locator("main, [role=main], #main, .main").first
    main_text = main.inner_text() if main.count() > 0 else body_text_full

    extracted = {
        "vin": vin,
        "identity": {
            "source": "BRP Dealer Portal",
            "portal_url": creds["url"],
            "pulled_at": datetime.now(timezone.utc).isoformat(),
        },
        "raw": {
            "url_after_search": page.url,
            "page_title": page.title(),
            "main_text": main_text[:20000],
            "body_length": len(body_text_full),
        },
        "warranty": {
            "base": None,
            "extended": [],
            "campaigns": [],
            "claims_history": [],
            "note": "WIREFRAME: raw-text dump. Targeted extractors added after first successful run.",
        },
        "unit_master": {},
    }

    return extracted, screens
