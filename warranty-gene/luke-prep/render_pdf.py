"""Render EgD-WGB-001 blueprint markdown to canon PDF via WeasyPrint.

EgD canon: cream #fdfaf4 / cream-2 #f7f2e7 / ink #1a1a1a / line #e7e1d3 /
mute #6b665c / accent orange #e87722; Fraunces display, Inter body.
"""
from __future__ import annotations
import hashlib, os, re, datetime
from pathlib import Path
from weasyprint import HTML, CSS

HERE = Path(__file__).parent
MD = HERE / "EgD-WGB-003-Luke-Access-Prep.md"
OUT = HERE / "EgD-WGB-003-Luke-Access-Prep.pdf"

md = MD.read_text(encoding="utf-8")
sha = hashlib.sha256(md.encode("utf-8")).hexdigest()
ts  = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
KEY = "EgD-KEY-2026-07"

# --- Minimal markdown -> HTML (same subset the other renderer uses) ---
def _inline(s: str) -> str:
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s

def md_to_html(md_text: str) -> str:
    out: list[str] = []
    lines = md_text.splitlines()
    i = 0
    in_ul = False
    in_ol = False
    in_table = False
    in_code = False
    tbl_rows: list[list[str]] = []
    code_buf: list[str] = []

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>"); in_ul = False
        if in_ol:
            out.append("</ol>"); in_ol = False

    def flush_table():
        nonlocal in_table, tbl_rows
        if not tbl_rows:
            in_table = False; return
        header, *body = tbl_rows
        out.append('<table class="data"><thead><tr>')
        for c in header: out.append(f"<th>{_inline(c)}</th>")
        out.append("</tr></thead><tbody>")
        for r in body:
            while len(r) < len(header): r.append("")
            out.append("<tr>")
            for c in r: out.append(f"<td>{_inline(c)}</td>")
            out.append("</tr>")
        out.append("</tbody></table>")
        in_table = False; tbl_rows = []

    while i < len(lines):
        ln = lines[i]

        # Fenced code block toggle
        if ln.strip().startswith("```"):
            if in_code:
                # close
                escaped = "\n".join(code_buf).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                out.append(f"<pre><code>{escaped}</code></pre>")
                code_buf = []
                in_code = False
            else:
                close_lists()
                if in_table: flush_table()
                in_code = True
            i += 1; continue
        if in_code:
            code_buf.append(ln); i += 1; continue

        # Table
        if "|" in ln and ln.strip().startswith("|"):
            close_lists()
            if not in_table:
                in_table = True; tbl_rows = []
            if re.match(r"^\s*\|?\s*[:\- ]+\|", ln):
                i += 1; continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            tbl_rows.append(cells)
            i += 1; continue
        else:
            if in_table: flush_table()

        # HR
        if re.match(r"^\s*---+\s*$", ln):
            close_lists(); out.append("<hr>"); i += 1; continue

        # Headings
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            close_lists()
            level = len(m.group(1))
            out.append(f"<h{level}>{_inline(m.group(2).strip())}</h{level}>")
            i += 1; continue

        # Blockquote
        if ln.startswith("> "):
            close_lists()
            out.append(f"<blockquote>{_inline(ln[2:].strip())}</blockquote>")
            i += 1; continue

        # Bullet (with indented continuation lines merged)
        m = re.match(r"^\s*[-*]\s+(.*)$", ln)
        if m:
            if in_ol: out.append("</ol>"); in_ol = False
            if not in_ul: out.append("<ul>"); in_ul = True
            item = [m.group(1)]
            j = i + 1
            while j < len(lines) and re.match(r"^\s{2,}\S", lines[j]) \
                    and not re.match(r"^\s*[-*]\s+", lines[j]) \
                    and not re.match(r"^\s*\d+\.\s+", lines[j]):
                item.append(lines[j].strip())
                j += 1
            out.append(f"<li>{_inline(' '.join(item))}</li>")
            i = j; continue

        # Numbered (with indented continuation lines merged)
        m = re.match(r"^\s*\d+\.\s+(.*)$", ln)
        if m:
            if in_ul: out.append("</ul>"); in_ul = False
            if not in_ol: out.append("<ol>"); in_ol = True
            item = [m.group(1)]
            j = i + 1
            while j < len(lines) and re.match(r"^\s{3,}\S", lines[j]) \
                    and not re.match(r"^\s*[-*]\s+", lines[j]) \
                    and not re.match(r"^\s*\d+\.\s+", lines[j]):
                item.append(lines[j].strip())
                j += 1
            out.append(f"<li>{_inline(' '.join(item))}</li>")
            i = j; continue

        # Blank
        if not ln.strip():
            close_lists()
            i += 1; continue

        # Paragraph
        para = [ln]
        j = i + 1
        while j < len(lines) and lines[j].strip() and not re.match(
            r"^(#|>\s|\s*[-*]\s|\s*\d+\.\s|\||```)", lines[j]):
            para.append(lines[j]); j += 1
        close_lists()
        out.append(f"<p>{_inline(' '.join(para))}</p>")
        i = j

    close_lists()
    if in_table: flush_table()
    return "\n".join(out)

html_body = md_to_html(md)

CSS_STR = f"""
@page {{
  size: Letter;
  margin: 22mm 20mm 22mm 20mm;
  background: #fdfaf4;

  @top-left {{
    content: "EVEglyphDesign — Warranty GENE Luke Access Prep (EgD-WGB-003)";
    color: #e87722;
    font-family: Inter, sans-serif;
    font-weight: 600;
    font-size: 8.5pt;
    padding-bottom: 4mm;
    border-bottom: 0.6pt solid #e87722;
  }}
  @top-right {{
    content: "{KEY}  ·  {ts}";
    color: #6b665c;
    font-family: Inter, sans-serif;
    font-size: 8pt;
    padding-bottom: 4mm;
    border-bottom: 0.6pt solid #e87722;
    white-space: nowrap;
  }}
  @bottom-left {{
    content: "© 2026 EVEglyphDesign  ·  SHA-256 {sha[:10]}…";
    color: #6b665c;
    font-family: Inter, sans-serif;
    font-size: 7.5pt;
    padding-top: 3mm;
    border-top: 0.4pt solid #e7e1d3;
    white-space: nowrap;
  }}
  @bottom-right {{
    content: "Page " counter(page) " of " counter(pages) "  ·  Pour le bien-être du peuple";
    color: #6b665c;
    font-family: Inter, sans-serif;
    font-size: 7.5pt;
    padding-top: 3mm;
    border-top: 0.4pt solid #e7e1d3;
    white-space: nowrap;
  }}
}}

html, body {{
  background: #fdfaf4;
  color: #1a1a1a;
  font-family: Inter, "Helvetica Neue", Arial, sans-serif;
  font-size: 10.5pt;
  line-height: 1.55;
  hyphens: auto;
}}

body::before {{
  content: "";
  position: fixed;
  top: 40%; left: 15%;
  transform: rotate(-24deg);
  color: #f2ebd8;
  font-family: "Fraunces", "Times New Roman", serif;
  font-size: 96pt;
  font-weight: 400;
  letter-spacing: -1pt;
  z-index: -1;
  opacity: 1;
}}

h1, h2, h3, h4 {{
  font-family: "Fraunces", "Times New Roman", serif;
  color: #1a1a1a;
  page-break-after: avoid;
}}
h1 {{ font-size: 26pt; line-height: 1.15; margin: 0 0 4pt; }}
h2 {{ font-size: 18pt; line-height: 1.2; margin: 20pt 0 6pt; }}
h3 {{ font-size: 13.5pt; line-height: 1.25; margin: 14pt 0 4pt; }}
h4 {{ font-family: Inter, sans-serif; font-size: 10.5pt; text-transform: uppercase;
      letter-spacing: 0.5pt; color: #e87722; margin: 12pt 0 3pt; }}

p {{ margin: 0 0 8pt; text-align: justify; }}
ul, ol {{ margin: 0 0 8pt 20pt; padding: 0; }}
li {{ margin: 0 0 3pt; }}

blockquote {{
  margin: 8pt 0 12pt 8pt;
  padding: 4pt 12pt;
  border-left: 2pt solid #e87722;
  color: #6b665c;
  font-style: italic;
}}

a {{ color: #e87722; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
code {{ font-family: "JetBrains Mono", Menlo, Consolas, monospace;
        font-size: 9.5pt; background: #f7f2e7; padding: 0 3pt; border-radius: 2pt; }}
pre {{ background: #f7f2e7; border: 0.4pt solid #e7e1d3; border-radius: 3pt;
       padding: 8pt 10pt; font-size: 8.8pt; line-height: 1.4;
       white-space: pre-wrap; word-wrap: break-word;
       page-break-inside: avoid; margin: 6pt 0 12pt; }}
pre code {{ background: transparent; padding: 0; font-size: 8.8pt; }}

hr {{ border: 0; border-top: 0.5pt solid #e7e1d3; margin: 14pt 0; }}

table.data {{
  width: 100%; border-collapse: collapse; margin: 6pt 0 14pt;
  font-size: 9pt;
}}
table.data th {{
  text-align: left;
  background: #f7f2e7;
  border-bottom: 0.8pt solid #e87722;
  padding: 5pt 7pt;
  font-family: Inter, sans-serif;
  font-weight: 700;
  color: #1a1a1a;
}}
table.data td {{
  border-bottom: 0.3pt solid #e7e1d3;
  padding: 4pt 7pt;
  vertical-align: top;
}}
table.data tr {{ page-break-inside: avoid; }}

.title-block {{ margin-bottom: 20pt; }}
.title-block .kicker {{
  font-family: Inter, sans-serif;
  font-size: 9pt;
  text-transform: uppercase;
  letter-spacing: 2pt;
  color: #e87722;
  margin-bottom: 4pt;
}}
.title-block h1 {{ font-size: 36pt; line-height: 1.05; margin: 0; }}
.title-block .subtitle {{
  font-family: "Fraunces", serif;
  font-size: 15pt; color: #6b665c;
  margin: 4pt 0 10pt;
  font-style: italic;
}}

.closing {{ text-align: center; color: #6b665c; font-style: italic;
            margin-top: 20pt; font-size: 9pt; }}
"""

# Replace the H1 into a title block; grab the first paragraph as subtitle text
html_body = re.sub(
    r"^<h1>Warranty GENE — Luke access prep</h1>\s*<p>(.+?)</p>",
    lambda m: (
        '<div class="title-block">'
        '<div class="kicker">EVEglyphDesign · Hawkins Twin Platform</div>'
        '<h1>Warranty GENE — Luke access prep</h1>'
        '<div class="subtitle">EgD-WGB-003 · Five counterparties, one sweep · Credentials scoped to every VIN Hawkins services, not just the sample</div>'
        f'<p>{m.group(1)}</p>'
        '</div>'
    ),
    html_body, count=1, flags=re.DOTALL,
)

# Convert the italic closing tagline into the .closing block
html_body = re.sub(
    r"<p><em>Pour le bien-être du peuple\.</em></p>\s*$",
    '<p class="closing">© 2026 EVEglyphDesign. All rights reserved. Controlled copy.<br>'
    'Key ID <code>EgD-KEY-2026-07</code>.<br>'
    '<em>Pour le bien-être du peuple.</em></p>',
    html_body,
)

HTML_DOC = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Warranty GENE — Luke Access Prep (EgD-WGB-003)</title></head>
<body>{html_body}</body></html>"""

(HERE / "EgD-WGB-003-Luke-Access-Prep.html").write_text(HTML_DOC, encoding="utf-8")

HTML(string=HTML_DOC, base_url=str(HERE)).write_pdf(
    str(OUT),
    stylesheets=[CSS(string=CSS_STR)],
)

import pypdf
n = len(pypdf.PdfReader(str(OUT)).pages)
print(f"wrote {OUT} pages={n} sha256={sha}")
