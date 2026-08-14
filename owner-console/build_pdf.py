"""
Build the Hawkins Owner Console conceptual map PDF.
Canon: cream/orange, Fraunces/Inter, watermark, SHA-256, EgD-KEY-2026-07.
Two-pass: first build to discover page count, then stamp footer with total.
"""
from __future__ import annotations

import hashlib
import io
import os
from datetime import datetime, timezone
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

HERE = Path(__file__).parent
OUT = HERE / "EVEglyphDesign_Hawkins_Owner_Console_Conceptual_Map.pdf"

CREAM = colors.HexColor("#fdfaf4")
CREAM2 = colors.HexColor("#f7f2e7")
INK = colors.HexColor("#1a1a1a")
LINE = colors.HexColor("#e7e1d3")
MUTE = colors.HexColor("#6b665c")
ACCENT = colors.HexColor("#e87722")

KEY_ID = "EgD-KEY-2026-07"
DOC_ID = "EgD-HAWKINS-CONSOLE-001"
TIMESTAMP = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def register_fonts():
    LOCAL = HERE / "fonts"
    candidates = {
        "Fraunces": str(LOCAL / "Fraunces-Regular.ttf"),
        "Fraunces-Bold": str(LOCAL / "Fraunces-Bold.ttf"),
        "Inter": str(LOCAL / "Inter-Regular.ttf"),
        "Inter-Bold": str(LOCAL / "Inter-Bold.ttf"),
    }
    got = {}
    for name, path in candidates.items():
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont(name, path))
                got[name] = name
            except Exception:
                pass
    return got


fonts = register_fonts()
DISP = fonts.get("Fraunces", "Helvetica-Bold")
DISP_B = fonts.get("Fraunces-Bold", "Helvetica-Bold")
BODY = fonts.get("Inter", "Helvetica")
BODY_B = fonts.get("Inter-Bold", "Helvetica-Bold")


class Painter:
    def __init__(self):
        self.total_pages = None
        self.sha_short = "pending"

    def draw(self, canv, doc):
        canv.saveState()
        canv.setFillColor(CREAM)
        canv.rect(0, 0, LETTER[0], LETTER[1], stroke=0, fill=1)

        # Watermark
        canv.saveState()
        canv.translate(LETTER[0] / 2, LETTER[1] / 2)
        canv.rotate(35)
        canv.setFillColor(colors.HexColor("#f0e9d6"))
        canv.setFont(DISP_B, 84)
        canv.drawCentredString(0, 0, "EVEglyphDesign")
        canv.restoreState()

        # Top rule + brand
        canv.setStrokeColor(LINE)
        canv.setLineWidth(0.75)
        canv.line(0.6 * inch, LETTER[1] - 0.55 * inch, LETTER[0] - 0.6 * inch, LETTER[1] - 0.55 * inch)
        canv.setFillColor(INK)
        canv.setFont(BODY_B, 8)
        canv.drawString(0.6 * inch, LETTER[1] - 0.4 * inch, "EVEglyphDesign")
        canv.setFillColor(MUTE)
        canv.setFont(BODY, 8)
        canv.drawRightString(LETTER[0] - 0.6 * inch, LETTER[1] - 0.4 * inch,
                             f"{DOC_ID}  ·  {KEY_ID}")

        # Accent bar
        canv.setFillColor(ACCENT)
        canv.rect(0.4 * inch, 0.8 * inch, 0.06 * inch, LETTER[1] - 1.6 * inch, stroke=0, fill=1)

        # Footer
        canv.setStrokeColor(LINE)
        canv.line(0.6 * inch, 0.72 * inch, LETTER[0] - 0.6 * inch, 0.72 * inch)
        canv.setFillColor(MUTE)
        canv.setFont(BODY, 7.5)
        page_no = canv.getPageNumber()
        total = self.total_pages or "?"
        # Line 1: copyright + timestamp | page number
        canv.drawString(0.6 * inch, 0.56 * inch,
                        f"© 2026 EVEglyphDesign · Controlled copy · {TIMESTAMP}")
        canv.drawRightString(LETTER[0] - 0.6 * inch, 0.56 * inch,
                             f"Page {page_no} of {total}")
        # Line 2: SHA + tagline
        canv.setFont(BODY, 7)
        canv.drawString(0.6 * inch, 0.42 * inch, f"SHA-256 {self.sha_short}")
        canv.setFont(DISP, 8)
        canv.setFillColor(ACCENT)
        canv.drawRightString(LETTER[0] - 0.6 * inch, 0.42 * inch, "Pour le bien-être du peuple")
        canv.restoreState()


painter = Painter()

H1 = ParagraphStyle("H1", fontName=DISP_B, fontSize=26, leading=30, textColor=INK, spaceBefore=6, spaceAfter=10)
SUB = ParagraphStyle("Sub", fontName=DISP, fontSize=13, leading=16, textColor=MUTE, spaceAfter=14)
H2 = ParagraphStyle("H2", fontName=DISP_B, fontSize=16, leading=20, textColor=ACCENT, spaceBefore=14, spaceAfter=6)
H3 = ParagraphStyle("H3", fontName=BODY_B, fontSize=11, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3)
BODY_P = ParagraphStyle("Body", fontName=BODY, fontSize=9.5, leading=13.5, textColor=INK, spaceAfter=5)
LEAD_P = ParagraphStyle("Lead", fontName=BODY, fontSize=10.5, leading=15, textColor=INK, spaceAfter=8)
CAP = ParagraphStyle("Cap", fontName=BODY, fontSize=8, leading=10.5, textColor=MUTE, spaceAfter=4)
CLOSE = ParagraphStyle("Close", fontName=BODY, fontSize=9.5, leading=13.5, textColor=MUTE, spaceAfter=5)
COV_P = ParagraphStyle("Cov", fontName=BODY_B, fontSize=9.5, leading=13, textColor=ACCENT, spaceAfter=3)
TBL_H = ParagraphStyle("TblH", fontName=BODY_B, fontSize=8.5, leading=11, textColor=colors.white)
TBL_C = ParagraphStyle("TblC", fontName=BODY, fontSize=8.5, leading=11, textColor=INK)
TBL_A = ParagraphStyle("TblA", fontName=BODY_B, fontSize=8.5, leading=11, textColor=ACCENT)


def link(href, text=None):
    text = text or href
    return f'<link href="{href}" color="#e87722"><u>{text}</u></link>'


def table_of(rows, col_widths, header=True):
    data = []
    for i, row in enumerate(rows):
        style = TBL_H if (header and i == 0) else TBL_C
        data.append([Paragraph(c, style) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    styles = [
        ("ROWBACKGROUNDS", (0, 1 if header else 0), (-1, -1), [CREAM, CREAM2]),
        ("LINEBELOW", (0, 1 if header else 0), (-1, -1), 0.25, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        styles.append(("BACKGROUND", (0, 0), (-1, 0), ACCENT))
        styles.append(("LINEBELOW", (0, 0), (-1, 0), 0.6, INK))
    t.setStyle(TableStyle(styles))
    return t


def stack_row(label, txt, col):
    hex_color = col.hexval() if hasattr(col, 'hexval') else "#1a1a1a"
    para = Paragraph(f'<font color="{hex_color}"><b>{label}</b></font><br/>{txt}', BODY_P)
    cell = Table([[para]], colWidths=[6.5 * inch])
    cell.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM2),
        ("LINEBEFORE", (0, 0), (0, -1), 3, col),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return cell


def drill_box(q, cov, txt):
    box = Table(
        [
            [Paragraph(f"<b>{q}</b>", H3)],
            [Paragraph(cov, COV_P)],
            [Paragraph(txt, BODY_P)],
        ],
        colWidths=[6.5 * inch],
    )
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM2),
        ("LINEBEFORE", (0, 0), (0, -1), 3, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return KeepTogether(box)


def build_story():
    s = []
    s.append(Spacer(1, 0.4 * inch))
    s.append(Paragraph("The Owner Console", H1))
    s.append(Paragraph(
        "Conceptual Map — ATD Performance Measurement 2026 driving the Hawkins Twin",
        SUB,
    ))
    s.append(Paragraph(
        "The 60 Critical Operating Variables published by ATD in the "
        "NADA Management Series <i>Driven</i> are the owner's ledger of truth. "
        "The Hawkins Twin translates those variables into a drill-downable console whose "
        "first question is not <i>how are we doing</i> but <i>where is the next dollar</i> — "
        "which customers to accelerate, which vendors to press, which trucks to move.",
        LEAD_P,
    ))
    s.append(Paragraph(
        "Anchor guide: " + link(
            "https://www.nada.org/media/6116/download?inline",
            "ATD Performance Measurement 2026 (TD08, publication TD08260519)",
        ),
        CAP,
    ))

    # 1
    s.append(Paragraph("1 · Why the ATD guide is the anchor", H2))
    s.append(Paragraph(
        "ATD's 60 COVs are the shared vocabulary of the medium- and heavy-duty truck "
        "dealer network. They are already the numbers Tim Hawkins reads at his 20-Group. "
        "Building the console <i>backwards</i> from those variables gives four things at once.",
        BODY_P,
    ))
    for h, b in [
        ("Peer-comparability by construction",
         "every tile has a <b>Total-Dealer Average</b> and <b>Best-of-Class Average</b> line "
         "for 2023, 2024, and 2025 — no invented benchmark."),
        ("Portable across the network",
         "the same tile deploys to any Peterbilt dealer and, with a bookkeeping map, to any "
         "Kenworth, Mack, Volvo, or International dealer using the same NADA framework."),
        ("Owner-native language",
         "return on assets, cash months' supply, service absorption, past-due receivables — "
         "these are the words owners already use with their bankers."),
        ("Regulator-safe",
         "the guide's own disclaimer — no price coordination, informational only — sets the tone "
         "for how the twin displays peer values."),
    ]:
        s.append(Paragraph(f"<b>{h}.</b> {b}", BODY_P))

    # 2
    s.append(Paragraph("2 · Seven owner categories, one console", H2))
    s.append(Paragraph(
        "ATD groups the 60 COVs into seven shaded bands. The console mirrors those groups "
        "as top-level tiles.",
        BODY_P,
    ))
    s.append(table_of(
        [
            ["#", "Category (top-level tile)", "COVs", "Owner question the tile answers"],
            ["I", "Dealership financial health", "1–13",
             "Am I making money, is it turning into cash, and who owes it to me?"],
            ["II", "New truck", "14–22",
             "Is every unit in the yard earning its keep, and does F&amp;I add or subtract?"],
            ["III", "Used truck", "23–31",
             "Am I an appraiser or a hoarder — and are my used units returning capital?"],
            ["IV", "Service (mechanical)", "32–38",
             "Are the bays absorbing the store, and is warranty carrying its share?"],
            ["V", "Parts", "39–51",
             "Is inventory turning, are the right customers on account, and where is the leak?"],
            ["VI", "Body shop", "52–58",
             "Is the body shop paying for itself or leaking gross into overhead?"],
            ["VII", "Absorption composite", "59–60",
             "Could fixed operations alone cover the whole store this month?"],
        ],
        [0.35 * inch, 2.05 * inch, 0.6 * inch, 3.5 * inch],
    ))
    s.append(Paragraph(
        "The composite tiles (VII, COVs 59–60) are the owner's north star. Total dealership "
        "absorption of <b>117.09%</b> is the 2025 Best-of-Class value: the store's fixed "
        "departments cover 117% of dealership expense before a single truck is sold. The "
        "total-dealer average is 91.11%.",
        BODY_P,
    ))

    # 3
    s.append(Paragraph("3 · The eleven operating guides — the alarm line", H2))
    s.append(Paragraph(
        "ATD publishes eleven operating guides for the key COVs. These become the console's "
        "alarm thresholds — tiles turn amber below the guide and red on breach.",
        BODY_P,
    ))
    guides_data = [
        ("Guide", "Target", "Bound COV"),
        ("Return on assets", "17–25%", "COV 2"),
        ("Cash months' supply", "3 months", "COV 10"),
        ("P&amp;S receivables &gt;30 days / month sales", "≤15%", "COV 12"),
        ("Warranty receivables / current month P&amp;L", "≤100%", "COV 13"),
        ("Used-truck inventory turns", "≥6 / yr", "COV 28"),
        ("Service total labor gross % labor sales", "73% (75% net of unapplied)", "COV 32"),
        ("Parts sales per parts employee", "$70,000", "COV 49"),
        ("Parts inventory turns", "6–8 / yr", "COV 46"),
        ("Parts inventory performance", "≥180%", "COV 48"),
        ("Fixed absorption", "≥115%", "COV 59"),
        ("Total absorption", "≥130%", "COV 60"),
    ]
    # Custom render so 'Target' column shows in accent
    rows = [[Paragraph(c, TBL_H) for c in guides_data[0]]]
    for g, t, c in guides_data[1:]:
        rows.append([Paragraph(g, TBL_C), Paragraph(t, TBL_A), Paragraph(c, TBL_C)])
    gtbl = Table(rows, colWidths=[3.4 * inch, 2.2 * inch, 0.9 * inch], repeatRows=1)
    gtbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CREAM, CREAM2]),
        ("LINEBELOW", (0, 1), (-1, -1), 0.25, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    s.append(gtbl)

    # 4
    s.append(Paragraph("4 · How the twin produces every tile — the layer stack", H2))
    s.append(Paragraph(
        "Held work already draws the plumbing. The console is the last layer on a stack the "
        "Hawkins repositories have been building for months.",
        BODY_P,
    ))
    for label, txt, col in [
        ("L5 · Owner Console",
         "The dashboard itself. Seven category tiles, eleven guide-bound alarms, three "
         "composite tiles. Each tile drills into a ranked worklist of customers, vendors, "
         "or units — never into a chart with no next action.", ACCENT),
        ("L4 · Semantic model (ACDOCA + ACDOCI)",
         "The customer sphere preserves ACDOCA as the transaction journal and adds ACDOCI "
         "for customer interactions. COV formulas are expressed in this vocabulary once, "
         "then compile to whichever underlying system a dealer runs.", INK),
        ("L3 · Twin ingestion lanes",
         "CDK Data Export Tool over SFTP/PGP plus Dealer Data Exchange for the DMS side; "
         "TELUS Business Connect for voice and voicemail; Exchange Server archive for "
         "correspondence; Fortellis and restored-backup as parallel lanes when API coverage "
         "is thin.", INK),
        ("L2 · Repository ledger",
         "GitHub is the index of what exists, where it lives, and what governs it. Customer "
         "data stays in Hawkins-controlled Azure Postgres; the repository holds schema, DDL, "
         "tie-out logic, confidence tags, and the widening register.", INK),
        ("L1 · Boot contract",
         "Cheapest-source-first retrieval, symmetric processing, durable landing, canon "
         "output. Every console tile is a rung-2 or rung-3 answer on a pre-computed metric — "
         "never a rung-6 recompute.", MUTE),
    ]:
        s.append(stack_row(label, txt, col))
        s.append(Spacer(1, 4))

    # 5
    s.append(Paragraph("5 · Where each category's numbers come from", H2))
    s.append(Paragraph(
        "Every tile is bound to a source of record. Nothing on the console is invented — it "
        "is extracted, computed from extracted values, or explicitly labelled synthetic while "
        "access is being executed.",
        BODY_P,
    ))
    s.append(table_of(
        [
            ["Category", "Primary source", "Secondary / cross-check", "Refresh"],
            ["I · Financial health",
             "CDK General Ledger (COAs, monthly close, receivables aging)",
             "PACCAR ePortal warranty summary; bank feed for cash",
             "Monthly close + daily A/R"],
            ["II · New truck",
             "CDK Inventory + F&amp;I; PACCAR order-to-delivery",
             "OEM incentives export; used-appraisal DB",
             "Daily inventory, per-deal"],
            ["III · Used truck",
             "CDK Used Inventory + F&amp;I",
             "Wholesale block guides; internal appraiser log",
             "Daily inventory, per-deal"],
            ["IV · Service",
             "CDK Service RO detail (customer / warranty / internal)",
             "PACCAR warranty adjudication; time-clock",
             "Per RO close"],
            ["V · Parts",
             "CDK Parts (counter, wholesale, internal, RO)",
             "PACCAR parts availability; TELUS call log (parts inbound)",
             "Per invoice"],
            ["VI · Body shop",
             "CDK Body Shop RO detail",
             "Estimating package; insurer feeds where applicable",
             "Per RO close"],
            ["VII · Absorption composite",
             "Computed L4 (fixed depts ÷ dealership expense)",
             "Monthly financial statement tie-out",
             "Monthly + rolling"],
        ],
        [1.35 * inch, 2.05 * inch, 1.95 * inch, 1.15 * inch],
    ))

    # 6
    s.append(Paragraph("6 · The drill — how a tile becomes a next dollar", H2))
    s.append(Paragraph(
        "The owner does not want a chart. The owner wants a list of names, in priority "
        "order, with the amount at stake and the action to take. Every tile therefore "
        "drills through the same five-question sequence.",
        BODY_P,
    ))
    for q, cov, txt in [
        ("Who should pay us quicker?",
         "COVs 11–13 · Parts &amp; Service Receivables % Past Due",
         "Sort customer master by (invoice age × outstanding balance × 12-month gross margin). "
         "The console names the top 20 accounts, the CSR who owns them, the last-touch date "
         "from the TELUS call log, and the recommended action (call, statement, hold, COD). "
         "Amber at 15% past-due, red at 20%."),
        ("Who deserves more love?",
         "COVs 5–6, 33, 41 · Gross per Employee &amp; Customer RO Gross % Sales",
         "Sort customer master by trailing-12 gross contribution × repeat rate × mix "
         "(parts + service + body + truck). The tile surfaces the top 20 A-customers whose "
         "purchase cadence just slipped — a saved visit, a reserved bay, a fleet check-in "
         "call from the parts manager."),
        ("Which vendors should we press?",
         "COVs 39–48 · Parts Gross % / Inventory Turns / Inventory Performance",
         "Sort vendor master by (line-item margin gap vs Best-of-Class × dollars purchased × "
         "turn shortfall). The tile lists suppliers whose margin trails ATD Best-of-Class "
         "27.96% or whose SKUs drag inventory turns below the 6–8 guide — with the specific "
         "part numbers and last invoice."),
        ("Which trucks should we move?",
         "COVs 18–20, 27–29 · Inventory per Unit / Turns / Net Return",
         "Sort inventory by (days-on-lot × carrying cost × price-to-market gap). The tile "
         "flags every unit past its class-median age, with the appraiser's floor, the "
         "current wholesale bid, and the recommended action (retail push, wholesale, "
         "re-appraise, trade-out). 2025 Best-of-Class used-inventory turns is 3.0 against "
         "the ATD guide of 6."),
        ("Which bays are earning?",
         "COVs 32–38, 59 · Service Absorption &amp; Labor Gross",
         "Sort technicians by proficiency × posted vs actual hours × warranty labor gross. "
         "The tile shows which bays cover overhead and which do not, and where warranty is "
         "under-recovering at 72.46% average vs 77.28% Best-of-Class in 2025."),
    ]:
        s.append(drill_box(q, cov, txt))
        s.append(Spacer(1, 6))

    # 7
    s.append(Paragraph("7 · The Best-of-Class targets the tiles are set against", H2))
    s.append(Paragraph(
        "The console renders every metric alongside its ATD peer values so the owner sees "
        "Hawkins, Total-Dealer Average, and Best-of-Class on the same axis.",
        BODY_P,
    ))
    peer_rows = [
        ["Key COV", "2023 TDA", "2023 BoC", "2024 TDA", "2024 BoC", "2025 TDA", "2025 BoC"],
        ["Net profit % sales (1)", "4.98%", "10.54%", "3.27%", "7.50%", "3.15%", "7.19%"],
        ["Return on assets (2)", "8.82%", "16.85%", "5.31%", "6.44%", "4.74%", "8.54%"],
        ["Return on net worth (3)", "33.56%", "43.71%", "23.63%", "36.14%", "19.22%", "25.72%"],
        ["Cash months' supply (10)", "3.76", "4.00", "2.43", "3.72", "3.11", "5.44"],
        ["P&amp;S recv. past-due (12)", "20.54%", "11.00%", "18.06%", "20.77%", "19.15%", "13.88%"],
        ["Warranty receivables (13)", "120.79%", "109.95%", "111.53%", "106.47%", "122.62%", "104.32%"],
        ["New truck inv. turns (19)", "3.8", "5.0", "2.7", "3.3", "2.9", "3.8"],
        ["Net return on used (29)", "-13.83%", "17.53%", "-19.23%", "19.38%", "-11.67%", "18.13%"],
        ["Service absorption (38)", "38.02%", "46.02%", "36.40%", "43.41%", "37.24%", "47.25%"],
        ["Parts gross % sales (39)", "28.20%", "28.48%", "27.29%", "26.87%", "27.27%", "27.96%"],
        ["Parts inv. turns (46)", "5.0", "5.8", "5.0", "5.6", "5.0", "5.2"],
        ["Parts absorption (51)", "52.02%", "58.54%", "48.37%", "57.68%", "48.81%", "59.34%"],
        ["P&amp;S absorption (59)", "92.17%", "122.32%", "86.82%", "120.69%", "88.17%", "111.54%"],
        ["Total absorption (60)", "95.68%", "126.31%", "89.31%", "121.86%", "91.11%", "117.09%"],
    ]
    prow = [[Paragraph(c, TBL_H) for c in peer_rows[0]]]
    for r in peer_rows[1:]:
        prow.append([Paragraph(r[0], TBL_C)] + [Paragraph(v, TBL_A) for v in r[1:]])
    ptbl = Table(prow, colWidths=[1.95 * inch] + [0.72 * inch] * 6, repeatRows=1)
    ptbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CREAM, CREAM2]),
        ("LINEBELOW", (0, 1), (-1, -1), 0.25, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    s.append(ptbl)
    s.append(Paragraph(
        "Source: ATD Performance Measurement 2026 (TD08260519), page 3. TDA = Total-Dealer "
        "Average, BoC = Best-of-Class (top-performing 20%).",
        CAP,
    ))

    # 8
    s.append(Paragraph("8 · Scaling across the peer network — beyond Peterbilt", H2))
    s.append(Paragraph(
        "The 60 COVs are OEM-agnostic. The console is designed so that a new dealer onboards "
        "by mapping their DMS to the ACDOCA/ACDOCI vocabulary once — the tiles and peer "
        "values do not move.",
        BODY_P,
    ))
    s.append(table_of(
        [
            ["Dealer type", "Same tiles?", "What changes"],
            ["Peterbilt (PACCAR)", "Yes — reference implementation", "Nothing"],
            ["Kenworth (PACCAR)", "Yes", "ePortal is shared; DMS mapping is identical"],
            ["Mack / Volvo / Freightliner / International", "Yes",
             "Swap PACCAR warranty and parts sources for the OEM equivalent; ATD COVs are unchanged"],
            ["Non-CDK dealer (Karmak, Procede Excede, Lightspeed)", "Yes",
             "Replace L3 ingestion adapter only; L4 semantic model, L5 tiles and peer values are shared"],
            ["Automotive (NADA rather than ATD)", "Shape only",
             "The 60 COVs are truck-specific; the same layer stack applies with NADA's automotive COVs"],
        ],
        [2.0 * inch, 1.4 * inch, 3.1 * inch],
    ))

    # 9
    s.append(Paragraph("9 · What is already in place, and what plugs in next", H2))
    s.append(Paragraph("<b>In place</b>", H3))
    for item in [
        "<b>TELUS Business Connect twin</b> — authenticated MCP with per-tenant HNSW vector "
        "index, three-tile decision surface (voicemail-not-returned-in-two-hours, "
        "repeat-caller-without-callback, never-reached), hourly transcription pipeline. Feeds "
        "the customer-touch signals inside Categories I, IV, V, and VI.",
        "<b>Exchange Server archive</b> — historical Hawkins correspondence loaded into "
        "Postgres. Provides the non-voice customer-touch signal that pairs with TELUS for the "
        "<i>who deserves more love</i> drill.",
        "<b>CDK export lane</b> — Data Export Tool over SFTP/PGP plus Dealer Data Exchange, "
        "PGP key custody with Hawkins, encrypted-original + raw-CSV preservation, seven-day "
        "monitored purge. The 21-object, 443-field dictionary and Postgres/Snowflake DDL are "
        "generated. This is the primary source of record for every ATD COV.",
        "<b>SAP-shaped analytics reuse</b> — the advanced-analytics layer reuses the SAP "
        "model rather than a Hawkins-only structure, so the same L4 vocabulary supports the "
        "Hawkins console and the eve-vendor-sphere procurement side.",
    ]:
        s.append(Paragraph("· " + item, BODY_P))
    s.append(Paragraph("<b>Next to plug in</b>", H3))
    for item in [
        "<b>CDK Phase-1 load</b> — three full months, financial tie-out on the middle month, "
        "field-widening register live.",
        "<b>L4 formula pack</b> — the 60 COVs expressed once in the ACDOCA/ACDOCI vocabulary, "
        "with tests that reconcile to the Hawkins financial statement.",
        "<b>L5 tile pack</b> — seven category tiles, eleven alarm bindings, three composite "
        "tiles, each with its ranked worklist drill.",
        "<b>Owner walk-through</b> — Tim-facing surface (renamed Tim VIP), read-only, with "
        "the existing GitHub Pages intake path as fallback if pplx.app auth is unavailable.",
    ]:
        s.append(Paragraph("· " + item, BODY_P))

    # 10
    s.append(Paragraph("10 · Where this lands", H2))
    s.append(Paragraph(
        "Per canon, this map lands in the Hawkins repository and on a public surface. It "
        "supersedes any earlier tile sketch by adding the ATD anchor and the seven-category "
        "structure.",
        BODY_P,
    ))
    for label, name, url in [
        ("Anchor guide",
         "ATD Performance Measurement 2026 (TD08260519)",
         "https://www.nada.org/media/6116/download?inline"),
        ("Reference implementation",
         "eve-hawkins-truck-mart",
         "https://github.com/EVEglyphDesign/eve-hawkins-truck-mart"),
        ("Twin platform",
         "hawkins-twin-platform",
         "https://github.com/EVEglyphDesign/hawkins-twin-platform"),
        ("Customer sphere design",
         "CUSTOMER-SPHERE-DESIGN.md",
         "https://github.com/EVEglyphDesign/hawkins-twin-platform/blob/main/customer-sphere/CUSTOMER-SPHERE-DESIGN.md"),
        ("TELUS twin",
         "eve-hawkins-telus-twin",
         "https://github.com/EVEglyphDesign/eve-hawkins-telus-twin"),
        ("CDK twin",
         "eve-hawkins-cdk-twin",
         "https://github.com/EVEglyphDesign/eve-hawkins-cdk-twin"),
        ("Boot contract",
         "eve-glyph-boot-contract",
         "https://github.com/EVEglyphDesign/eve-glyph-boot-contract"),
    ]:
        s.append(Paragraph(f"<b>{label}</b> — {link(url, name)}", BODY_P))

    s.append(Spacer(1, 0.15 * inch))
    s.append(Paragraph(
        "This document is doctrine, not code. The next artifact is the L4 formula pack — "
        "60 formulas expressed in the shared vocabulary — followed by the L5 tile pack that "
        "renders them.",
        CLOSE,
    ))
    return s


def build(painter_instance):
    buf = io.BytesIO()
    doc = BaseDocTemplate(
        buf,
        pagesize=LETTER,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
        title="EVEglyphDesign — Hawkins Owner Console Conceptual Map",
        author="EVEglyphDesign",
        subject="ATD-anchored Owner Console conceptual map for the Hawkins Twin",
        creator="EVEglyphDesign",
    )
    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height,
        leftPadding=0.1 * inch, rightPadding=0,
        topPadding=0, bottomPadding=0,
        id="body",
    )
    tmpl = PageTemplate(id="main", frames=[frame], onPage=painter_instance.draw)
    doc.addPageTemplates([tmpl])
    doc.build(build_story())
    return buf.getvalue()


pass1 = build(painter)
pages_count = pass1.count(b"/Type /Page ") + pass1.count(b"/Type /Page\n") + pass1.count(b"/Type /Page/")
if pages_count == 0:
    pages_count = pass1.count(b"/Type/Page")
print(f"Pass 1 pages: {pages_count}")

# Compute a stable SHA from a page-count-stamped-but-SHA-blank pass
painter.total_pages = pages_count
pass2 = build(painter)
sha_pre = hashlib.sha256(pass2).hexdigest()
painter.sha_short = sha_pre[:16]
final = build(painter)

sha = hashlib.sha256(final).hexdigest()
OUT.write_bytes(final)
(HERE / "EVEglyphDesign_Hawkins_Owner_Console_Conceptual_Map.pdf.sha256").write_text(
    f"{sha}  EVEglyphDesign_Hawkins_Owner_Console_Conceptual_Map.pdf\n"
)
print(f"Wrote {OUT} ({len(final):,} bytes)")
print(f"SHA-256: {sha}")
print(f"Fonts: {list(fonts)}")
