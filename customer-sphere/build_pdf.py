#!/usr/bin/env python3
"""
Build the EVEglyphDesign Hawkins Twin Customer Sphere Design PDF from
CUSTOMER-SPHERE-DESIGN.md, in EgD canon: cream and orange, Fraunces and Inter,
watermark, SHA-256 content hash, key ID, ISO-8601 UTC timestamp, page count in footer.

Two-pass build: pass one discovers the page count, pass two stamps it.

    python3 customer-sphere/build_pdf.py
"""
import hashlib
import pathlib
import re
import datetime

import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
FONTS = pathlib.Path("/home/user/workspace/fonts")
SRC = HERE / "CUSTOMER-SPHERE-DESIGN.md"
OUT = HERE / "EVEglyphDesign_Hawkins_Twin_Customer_Sphere_Design.pdf"

KEY_ID = "EgD-KEY-2026-07"
REPO = "https://github.com/EVEglyphDesign/hawkins-twin-platform"
DOC_URL = f"{REPO}/blob/main/customer-sphere/CUSTOMER-SPHERE-DESIGN.md"

raw = SRC.read_text(encoding="utf-8")
CONTENT_HASH = hashlib.sha256(raw.encode("utf-8")).hexdigest()
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ---------------------------------------------------------------- parse source
body = raw

# Strip the trailing copyright block; the PDF carries its own colophon.
body = body.split("\n---\n\n© 2026")[0]

# Title and the front-matter block that follows it.
lines = body.split("\n")
title = lines[0].lstrip("# ").strip()
rest = "\n".join(lines[1:])

front, _, after = rest.partition("\n---\n")

# Rewrite relative repo links to absolute GitHub links so every link is clickable.
def absolutise(m):
    text, href = m.group(1), m.group(2)
    if href.startswith(("http://", "https://", "#")):
        return m.group(0)
    target = (HERE / href).resolve().relative_to(ROOT)
    return f"[{text}]({REPO}/blob/main/{target})"

after = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", absolutise, after)
front = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", absolutise, front)

md = markdown.Markdown(extensions=["tables", "attr_list", "sane_lists"])
front_html = md.convert(front.strip())
md.reset()
body_html = md.convert(after.strip())

# Section headings open a new page from section 2 onward, keeping the cover and
# section 1 together on the opening spread.
_first = [True]


def _h2(m):
    if _first[0]:
        _first[0] = False
        return "<h2>"
    return '<h2 class="brk">'


body_html = re.sub(r"<h2>", _h2, body_html)

# ---------------------------------------------------------------------- styles
CSS_TMPL = """
@font-face {{ font-family: Fraunces; src: url("file://{fonts}/Fraunces.ttf"); }}
@font-face {{ font-family: Inter; src: url("file://{fonts}/Inter.ttf"); }}
@font-face {{ font-family: Inter; font-style: italic; src: url("file://{fonts}/Inter-Italic.ttf"); }}

:root {{
  --cream: #fdfaf4; --cream2: #f7f2e7; --ink: #1a1a1a;
  --line: #e7e1d3; --mute: #6b665c; --accent: #e87722;
}}

@page {{
  size: Letter;
  margin: 20mm 18mm 22mm 18mm;
  background: #fdfaf4;
  @bottom-left {{
    content: "EVEglyphDesign · Hawkins Twin · Customer Sphere Design";
    font-family: Inter; font-size: 7.5pt; color: #6b665c;
  }}
  @bottom-right {{
    content: "Page " counter(page) " of {pages}";
    font-family: Inter; font-size: 7.5pt; color: #6b665c;
  }}
}}
@page cover {{ margin: 0; @bottom-left {{ content: "" }} @bottom-right {{ content: "" }} }}

html {{ background: var(--cream); }}
body {{
  font-family: Inter, sans-serif; font-size: 9.6pt; line-height: 1.55;
  color: var(--ink); background: var(--cream); margin: 0;
}}

/* ------------------------------------------------------------------- cover */
.cover {{ page: cover; break-after: page; }}
.cover-band {{ background: var(--cream2); border-bottom: 3px solid var(--accent);
  padding: 34mm 18mm 14mm 18mm; }}
.mark {{ font-family: Inter; font-size: 8pt; letter-spacing: .22em;
  text-transform: uppercase; color: var(--accent); margin: 0 0 14mm; font-weight: 600; }}
.cover h1 {{ font-family: Fraunces, serif; font-size: 30pt; line-height: 1.14;
  margin: 0 0 6mm; font-weight: 600; letter-spacing: -.01em; }}
.cover .sub {{ font-family: Fraunces, serif; font-size: 13pt; color: var(--mute);
  margin: 0; font-style: italic; }}
.cover-body {{ padding: 14mm 18mm 0 18mm; }}
.for {{ font-family: Inter; font-size: 8pt; letter-spacing: .18em;
  text-transform: uppercase; color: var(--mute); margin: 0 0 3mm; font-weight: 600; }}
.recipients {{ font-family: Fraunces, serif; font-size: 15pt; margin: 0 0 12mm; }}
.abstract {{ font-size: 10pt; line-height: 1.6; max-width: 148mm; color: #2a2a2a;
  margin: 0 0 40mm; }}
.cover-meta {{ margin: 0 18mm; border-top: 1px solid var(--line); padding-top: 5mm;
  font-size: 7.6pt; color: var(--mute); }}
.cover-meta b {{ color: var(--ink); font-weight: 600; }}
.cover-meta .row {{ margin: 0 0 1.6mm; }}
.hash {{ font-family: "DejaVu Sans Mono", monospace; font-size: 6.6pt;
  word-break: break-all; }}

/* ---------------------------------------------------------------- headings */
h2 {{ font-family: Fraunces, serif; font-size: 16pt; font-weight: 600;
  margin: 9mm 0 3mm; padding-bottom: 2mm; border-bottom: 2px solid var(--accent);
  break-after: avoid; }}
h2.brk {{ break-before: page; margin-top: 0; }}
h2:first-of-type {{ margin-top: 0; }}
h3 {{ font-family: Fraunces, serif; font-size: 11.5pt; font-weight: 600;
  margin: 6mm 0 1.5mm; color: #2b2b2b; break-after: avoid; }}
p {{ margin: 0 0 3mm; }}
strong {{ font-weight: 600; }}
a {{ color: #b8590f; text-decoration: none; border-bottom: .4pt solid #e3c9ae; }}

ul, ol {{ margin: 0 0 3.5mm; padding-left: 5.5mm; }}
li {{ margin-bottom: 1.8mm; }}

/* ------------------------------------------------------------------ tables */
table {{ width: 100%; border-collapse: collapse; margin: 3mm 0 5mm;
  font-size: 8.6pt; break-inside: avoid; }}
th {{ background: var(--cream2); text-align: left; font-weight: 600;
  padding: 2.2mm 2.6mm; border-bottom: 1.4pt solid var(--accent);
  font-size: 8pt; letter-spacing: .04em; }}
td {{ padding: 2.2mm 2.6mm; border-bottom: .6pt solid var(--line);
  vertical-align: top; }}
tr:nth-child(even) td {{ background: #fbf7ee; }}

/* ------------------------------------------------------------- front block */
.front {{ background: var(--cream2); border-left: 3px solid var(--accent);
  padding: 4mm 5mm 2mm; margin: 0 0 7mm; font-size: 8.8pt; }}
.front p {{ margin: 0 0 1.6mm; }}

/* ---------------------------------------------------------------- colophon */
.colophon {{ break-before: page; border-top: 2px solid var(--accent);
  margin-top: 6mm; padding-top: 5mm; font-size: 8.4pt; color: var(--mute); }}
.colophon h2 {{ border: 0; margin: 0 0 3mm; padding: 0; font-size: 14pt;
  color: var(--ink); }}
.colophon dt {{ font-weight: 600; color: var(--ink); margin-top: 3mm; }}
.colophon dd {{ margin: .6mm 0 0; }}
.closing {{ font-family: Fraunces, serif; font-style: italic; font-size: 12pt;
  color: var(--accent); text-align: center; margin: 12mm 0 0; }}
"""

WATERMARK = """
<svg class="wm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="34" fill="none" stroke="#e87722" stroke-width="1.6"/>
  <circle cx="50" cy="50" r="12" fill="none" stroke="#e87722" stroke-width="1.6"/>
  <path d="M50 16 C72 34 72 66 50 84 C28 66 28 34 50 16 Z" fill="none"
        stroke="#e87722" stroke-width="1.2"/>
</svg>
"""

WM_CSS = """
.wm { position: fixed; bottom: 8mm; right: 12mm; width: 16mm; height: 16mm;
      opacity: .16; z-index: 0; }
"""

ABSTRACT = (
    "Hawkins Truck Mart's customer records live in a dealer management system, a call "
    "platform, and the systems Craig Allen runs day to day. This design resolves all of "
    "them onto one customer, in one combined schema, with one key. It is built as an index "
    "repository inside the wider enterprise reference model, extending the existing ACDOCA "
    "standard at the edges rather than replacing it, with every face of the customer "
    "carried as a vector against a declared target. The description of the model is "
    "published and portable. The data itself stays inside Peterbilt Atlantic's own Azure "
    "tenant and never leaves it. That split is the whole design, and it is what puts the "
    "dealership \u2014 not a vendor \u2014 in the reference-model position for its industry."
)

RECIPIENTS = "Tim Hawkins &nbsp;·&nbsp; Luke Weatherbie"


def render(pages_label: str, out_path: pathlib.Path) -> int:
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{title}</title></head><body>
{WATERMARK}
<section class="cover">
  <div class="cover-band">
    <p class="mark">EVEglyphDesign · Peterbilt Atlantic Digital Twin</p>
    <h1>Customer Sphere Design</h1>
    <p class="sub">HawkinsTwin Customer 360 — an indexed, ACDOCA-aligned sphere of vectored targets</p>
  </div>
  <div class="cover-body">
    <p class="for">Prepared for</p>
    <p class="recipients">{RECIPIENTS}</p>
    <p class="abstract">{ABSTRACT}</p>
  </div>
  <div class="cover-meta">
    <p class="row"><b>Status</b> — Draft for review. No dealership data has moved.</p>
    <p class="row"><b>Agreement holder</b> Tim Hawkins &nbsp;·&nbsp;
       <b>20 Group access</b> Luke Weatherbie &nbsp;·&nbsp;
       <b>Systems register</b> Craig Allen</p>
    <p class="row"><b>Source of record</b>
       <a href="{DOC_URL}">customer-sphere/CUSTOMER-SPHERE-DESIGN.md</a></p>
    <p class="row"><b>Issued</b> {STAMP} &nbsp;·&nbsp; <b>Key ID</b> {KEY_ID}
       &nbsp;·&nbsp; <b>Pages</b> {pages_label}</p>
    <p class="row hash"><b>SHA-256</b> {CONTENT_HASH}</p>
  </div>
</section>

<div class="front">{front_html}</div>
{body_html}

<section class="colophon">
  <h2>Provenance and control</h2>
  <dl>
    <dt>Document</dt>
    <dd>EVEglyphDesign — Hawkins Twin Customer Sphere Design, {pages_label} pages.</dd>
    <dt>Source of record</dt>
    <dd><a href="{DOC_URL}">customer-sphere/CUSTOMER-SPHERE-DESIGN.md</a> in the
        <a href="{REPO}">Hawkins Twin Platform repository</a>. The repository is
        authoritative; this PDF is a controlled copy of it at the timestamp below.</dd>
    <dt>Direction record</dt>
    <dd><a href="{REPO}/blob/main/interactions/2026-08-01-customer-360-and-reference-model.md">2026-08-01
        — Customer 360 and the reference-model position</a>, the dated exchange this
        design was written from.</dd>
    <dt>Content hash (SHA-256 of the source Markdown)</dt>
    <dd class="hash">{CONTENT_HASH}</dd>
    <dt>Key ID</dt><dd>{KEY_ID}</dd>
    <dt>Issued</dt><dd>{STAMP}</dd>
    <dt>Standing gates</dt>
    <dd>No dealership data moves before Tim Hawkins's executed agreement. Peer comparison
        waits on Luke Weatherbie's 20 Group access. The live CDK dealer management system
        is never written to. Every surface runs on synthetic or mock data until those clear.</dd>
    <dt>Rights</dt>
    <dd>© 2026 Dany Theriault. EVE “digital stem cell” glyph and glyph-based design
        principles — all rights reserved. Stewardship of rights of use and assignment for
        large public and institutional usage rests with the Pacific Utilities Design
        Council. Published as a time-stamped record of authorship and intent.</dd>
  </dl>
  <p class="closing">Pour le bien-être du peuple.</p>
</section>
</body></html>"""

    font_config = FontConfiguration()
    doc = HTML(string=html, base_url=str(HERE)).render(
        stylesheets=[
            CSS(string=CSS_TMPL.format(fonts=FONTS, pages=pages_label),
                font_config=font_config),
            CSS(string=WM_CSS, font_config=font_config),
        ],
        font_config=font_config,
    )
    doc.write_pdf(out_path)
    return len(doc.pages)


if __name__ == "__main__":
    n = render("—", OUT)          # pass one: discover page count
    n2 = render(str(n), OUT)      # pass two: stamp it
    if n2 != n:
        n2 = render(str(n2), OUT)
    print(f"{OUT.name}: {n2} pages, sha256={CONTENT_HASH[:16]}…, issued {STAMP}")
