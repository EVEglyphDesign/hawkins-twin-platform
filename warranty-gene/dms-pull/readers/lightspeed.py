"""
Lightspeed EVO reader — Torque Motorsports.

WIREFRAME. Same shape as cdk.py: log in as Luke, find the VIN, dump what
Lightspeed shows for it. Lightspeed EVO's login flow is generally simpler
than CDK's — single-page username/password with optional TOTP — but the
in-app navigation to a unit's warranty screen is dealer-configured.
"""

from pathlib import Path
from datetime import datetime, timezone

import pyotp


def _stamp(page, trace_dir: Path, label: str, screens: list) -> None:
    ts = datetime.now(timezone.utc).strftime("%H%M%S")
    p = trace_dir / f"lightspeed-{label}-{ts}.png"
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
            f"MFA={method} requires interactive step. Switch to TOTP on this account."
        )


def pull(page, creds: dict, vin: str, trace_dir: Path):
    screens: list[str] = []

    page.goto(creds["url"], wait_until="domcontentloaded", timeout=45000)
    _stamp(page, trace_dir, "login-loaded", screens)

    # Fill username + password.
    for sel in ['input[name="username"]', 'input[type="email"]',
                'input[id*="user" i]', 'input[name="user"]']:
        if page.locator(sel).count() > 0:
            page.fill(sel, creds["username"])
            break
    else:
        raise RuntimeError("Could not find a username field on the Lightspeed login page")

    for sel in ['input[type="password"]', 'input[name="password"]']:
        if page.locator(sel).count() > 0:
            page.fill(sel, creds["password"])
            break
    else:
        raise RuntimeError("Could not find a password field on the Lightspeed login page")

    for sel in ['button:has-text("Sign in")', 'button:has-text("Log in")',
                'button:has-text("Login")', 'button[type="submit"]',
                'input[type="submit"]']:
        if page.locator(sel).count() > 0:
            page.click(sel)
            break
    page.wait_for_load_state("networkidle", timeout=45000)
    _stamp(page, trace_dir, "login-after-password", screens)

    _handle_mfa(page, creds, trace_dir, screens)
    _stamp(page, trace_dir, "post-mfa", screens)

    # Lightspeed EVO — VIN search is typically a top-bar search or a
    # Service > Unit lookup. Try search inputs first.
    search_selectors = [
        'input[placeholder*="VIN" i]',
        'input[placeholder*="Unit" i]',
        'input[placeholder*="Search" i]',
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
        html_path = trace_dir / f"lightspeed-landing-{datetime.now(timezone.utc).strftime('%H%M%S')}.html"
        html_path.write_text(page.content())
        raise RuntimeError(
            f"Lightspeed: no VIN search field on post-login landing. "
            f"HTML saved to {html_path.relative_to(Path.cwd())}."
        )

    body_text = page.locator("body").inner_text()
    main = page.locator("main, [role=main], #main, .main").first
    main_text = main.inner_text() if main.count() > 0 else body_text

    extracted = {
        "vin": vin,
        "identity": {
            "source": "Lightspeed EVO",
            "dealer_url": creds["url"],
            "pulled_at": datetime.now(timezone.utc).isoformat(),
        },
        "raw": {
            "url_after_search": page.url,
            "page_title": page.title(),
            "main_text": main_text[:20000],
            "body_length": len(body_text),
        },
        "warranty": {
            "base": None,
            "best_plan": None,
            "claims_open": [],
            "note": "WIREFRAME: raw-text dump. Targeted extractors added after first successful run.",
        },
        "work_orders_open": [],
    }

    return extracted, screens
