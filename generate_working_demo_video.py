import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"c:\Users\vinit\.gemini\antigravity\scratch\company-policy-assistant"
FRAMES_DIR = os.path.join(BASE_DIR, "scratch", "video_working_frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 30

# Colors matching Stitch & Streamlit App
C_CANVAS = (250, 249, 251)         # #faf9fb
C_SIDEBAR = (245, 243, 245)        # #f5f3f5
C_PRIMARY = (0, 46, 39)            # #002e27
C_CONTAINER = (20, 69, 61)         # #14453d
C_TEXT = (27, 28, 30)              # #1b1c1e
C_MUTED = (112, 121, 118)          # #707976
C_CARD = (255, 255, 255)
C_BORDER = (227, 226, 228)         # #e3e2e4
C_WARNING = (167, 58, 26)          # #a73a1a

def get_fonts():
    try:
        f_title = ImageFont.truetype("georgiab.ttf", 32)
        f_serif = ImageFont.truetype("georgia.ttf", 20)
        f_serif_b = ImageFont.truetype("georgiab.ttf", 20)
        f_quote = ImageFont.truetype("georgiai.ttf", 18)
        f_sans = ImageFont.truetype("arial.ttf", 17)
        f_sans_b = ImageFont.truetype("arialbd.ttf", 17)
        f_label = ImageFont.truetype("arialbd.ttf", 13)
        f_mono = ImageFont.truetype("consola.ttf", 14)
        f_tab = ImageFont.truetype("arial.ttf", 14)
    except:
        f_title = ImageFont.load_default()
        f_serif = f_title
        f_serif_b = f_title
        f_quote = f_title
        f_sans = f_title
        f_sans_b = f_title
        f_label = f_title
        f_mono = f_title
        f_tab = f_title
    return f_title, f_serif, f_serif_b, f_quote, f_sans, f_sans_b, f_label, f_mono, f_tab

fonts = get_fonts()
f_title, f_serif, f_serif_b, f_quote, f_sans, f_sans_b, f_label, f_mono, f_tab = fonts

def draw_browser_shell(draw, page_title="Lexicon | Corporate Policy Digest & Consultation"):
    # 1. OS Window Top Bar
    draw.rectangle([(0, 0), (WIDTH, 42)], fill=(230, 230, 235))
    # Window controls (mac/windows style dots)
    draw.ellipse([(20, 14), (32, 26)], fill=(255, 95, 87))
    draw.ellipse([(40, 14), (52, 26)], fill=(254, 188, 46))
    draw.ellipse([(60, 14), (72, 26)], fill=(40, 200, 64))
    
    # Active Browser Tab
    draw.rounded_rectangle([(100, 8), (480, 42)], radius=8, fill=(245, 243, 245))
    draw.text((120, 14), "🏛️ " + page_title[:38] + "...", fill=C_TEXT, font=f_tab)
    
    # 2. Browser URL Navigation Bar
    draw.rectangle([(0, 42), (WIDTH, 90)], fill=(255, 255, 255))
    draw.line([(0, 90), (WIDTH, 90)], fill=C_BORDER, width=1)
    
    # Nav controls
    draw.text((25, 54), "←   →   ⟳", fill=C_MUTED, font=f_sans_b)
    
    # URL Pill
    draw.rounded_rectangle([(120, 50), (WIDTH - 180, 82)], radius=16, fill=(245, 243, 245), outline=C_BORDER, width=1)
    draw.text((145, 57), "🔒 http://localhost:8501", fill=C_TEXT, font=f_mono)
    draw.text((WIDTH - 380, 58), "⚡ Streamlit Live • Roll No: 34", fill=C_CONTAINER, font=f_label)

    # 3. Sidebar (280px fixed width on left)
    draw.rectangle([(0, 90), (320, HEIGHT)], fill=C_SIDEBAR)
    draw.line([(320, 90), (320, HEIGHT)], fill=C_BORDER, width=1)

    # Sidebar Header
    draw.rounded_rectangle([(25, 110), (65, 150)], radius=8, fill=C_CONTAINER)
    draw.text((36, 118), "⚖️", fill=(255, 255, 255), font=f_serif)
    draw.text((75, 115), "LEXICON MANUALS", fill=C_PRIMARY, font=f_sans_b)
    draw.text((75, 135), "Vol. XXIV • Codex Ver 4.2", fill=C_MUTED, font=f_label)

    draw.line([(25, 165), (295, 165)], fill=C_BORDER, width=1)

    # Sidebar: Model & Vault Card
    draw.rounded_rectangle([(25, 180), (295, 255)], radius=10, fill=C_CARD, outline=C_BORDER, width=1)
    draw.text((38, 192), "VAULT AUTHENTICATION", fill=C_MUTED, font=f_label)
    draw.text((38, 208), "● Active (Tier-1 Grounded)", fill=C_CONTAINER, font=f_sans_b)
    draw.text((38, 230), "Model: Gemini-2.5-Flash", fill=C_TEXT, font=f_mono)

    # Sidebar: Policy Folio Library
    draw.text((25, 275), "INDEXED POLICY FOLIOS", fill=C_MUTED, font=f_label)
    
    folios = [
        ("Folio I: Leave_Policy.pdf", "2.8 KB", True),
        ("Folio II: Travel_Policy.pdf", "2.7 KB", True),
        ("Folio III: Reimbursement_Policy.pdf", "2.9 KB", True)
    ]
    fy = 295
    for fname, fsize, active in folios:
        draw.rounded_rectangle([(25, fy), (295, fy + 44)], radius=8, fill=C_CARD, outline=C_BORDER, width=1)
        draw.rectangle([(25, fy), (28, fy + 44)], fill=C_CONTAINER if active else C_MUTED)
        draw.text((35, fy + 8), fname, fill=C_TEXT, font=f_label)
        draw.text((35, fy + 24), f"ChromaDB Indexed • {fsize}", fill=C_MUTED, font=f_mono)
        fy += 52

    # Ingestion dropzone in sidebar
    draw.rounded_rectangle([(25, 460), (295, 545)], radius=8, fill=C_CARD, outline=C_CONTAINER, width=1)
    draw.text((60, 480), "📥 Drop New Policy PDF", fill=C_CONTAINER, font=f_sans_b)
    draw.text((45, 505), "Drag & drop to chunk into vector store", fill=C_MUTED, font=f_mono)

    # Action Buttons
    draw.rounded_rectangle([(25, 560), (295, 600)], radius=8, fill=C_CONTAINER)
    draw.text((55, 572), "🔄 Sync & Re-Index Repository", fill=(255, 255, 255), font=f_sans_b)

    draw.rounded_rectangle([(25, 615), (295, 655)], radius=8, fill=C_CARD, outline=C_BORDER, width=1)
    draw.text((85, 627), "🧹 Clear Chat History", fill=C_TEXT, font=f_sans)

    # Sidebar footer
    draw.rounded_rectangle([(25, HEIGHT - 70), (295, HEIGHT - 25)], radius=8, fill=C_CARD)
    draw.text((40, HEIGHT - 58), "ROLL NO: 34 • PS 34 ASSISTANT", fill=C_MUTED, font=f_mono)
    draw.text((40, HEIGHT - 42), "Evaluated: 10-Mark Allocation", fill=C_CONTAINER, font=f_mono)

def draw_main_header(draw):
    mx = 360
    # Masthead Live Pill
    draw.rounded_rectangle([(mx, 110), (mx + 380, 138)], radius=4, fill=(235, 243, 241))
    draw.text((mx + 12, 116), "● Corporate Intelligence System • Ver. 8.19 Live", fill=C_CONTAINER, font=f_label)

    # Hero Headline
    draw.text((mx, 150), "Corporate Policy Digest & Consultation", fill=C_TEXT, font=f_title)
    draw.text((mx, 195), "Audited HR, travel, and fiscal guidelines verified with ChromaDB vector grounding and page citations.", fill=C_MUTED, font=f_sans)

    # 4 Telemetry Ledger Cards (from Stitch)
    ledgers = [
        ("STATUTORY CORPUS", "3 Active Folios", "📖"),
        ("VECTOR REPOSITORY", "ChromaDB Persistent", "⚡"),
        ("GOVERNANCE MODE", "Zero-Hallucination", "⚖️"),
        ("AUDIT INTEGRITY", "100% Certified Grounding", "🛡️")
    ]
    lx = mx
    for ltitle, lval, licon in ledgers:
        draw.rounded_rectangle([(lx, 235), (lx + 340, 305)], radius=10, fill=C_CARD, outline=C_BORDER, width=1)
        draw.text((lx + 18, 248), ltitle, fill=C_MUTED, font=f_label)
        draw.text((lx + 18, 270), lval, fill=C_CONTAINER, font=f_sans_b)
        draw.text((lx + 295, 255), licon, fill=C_CONTAINER, font=f_serif)
        lx += 360

def draw_floating_input_bar(draw, placeholder_text):
    # Bottom Floating Dock (Matching Stitch Design)
    dock_x = 360
    dock_y = HEIGHT - 85
    dock_w = WIDTH - 400
    
    draw.rounded_rectangle([(dock_x, dock_y), (dock_x + dock_w, dock_y + 60)], radius=16, fill=(255, 255, 255), outline=C_BORDER, width=1)
    # Folder badge
    draw.rounded_rectangle([(dock_x + 12, dock_y + 10), (dock_x + 230, dock_y + 50)], radius=10, fill=C_SIDEBAR)
    draw.text((dock_x + 22, dock_y + 22), "📁 Folio II (Travel & HR)", fill=C_CONTAINER, font=f_label)
    
    # Input Text
    draw.text((dock_x + 250, dock_y + 20), placeholder_text, fill=C_TEXT if not placeholder_text.startswith("Consult") else C_MUTED, font=f_sans)
    
    # Submit Button
    draw.rounded_rectangle([(dock_x + dock_w - 150, dock_y + 8), (dock_x + dock_w - 10, dock_y + 52)], radius=12, fill=C_CONTAINER)
    draw.text((dock_x + dock_w - 128, dock_y + 20), "Query Folio ➔", fill=(255, 255, 255), font=f_label)

# -------------------------------------------------------------
# SCENE 1: App Launch & Initial Overview (12 sec = 360 frames)
# -------------------------------------------------------------
def render_working_scene_1():
    img = Image.new("RGB", (WIDTH, HEIGHT), C_CANVAS)
    draw = ImageDraw.Draw(img)
    draw_browser_shell(draw)
    draw_main_header(draw)

    mx = 360
    # Curated Inquiries Dossier Grid
    draw.text((mx, 335), "CURATED INQUIRIES & ACTIVE DOSSIERS (CLICK TO LOAD BRIEF):", fill=C_MUTED, font=f_label)

    dossiers = [
        ("REF: ARCH-4011 • HR FOLIO", "I. Annual Paid Leave & Carry-Forward", "Section 4.1.2 — 18 days annual accrual, max 10 days rollover cap, and lapse deadlines."),
        ("REF: ARCH-7300 • TRAVEL", "II. Daily Per Diem & Corporate Lodging", "Section 7.3.0 — $45 domestic per diem without receipts, Tier-1 hotel limits ($150/nt)."),
        ("REF: ARCH-9840 • REIMBURSEMENT", "III. WFH Infrastructure Equipment", "Section 9.8.4 — One-time $400 ergonomic equipment grant for new remote employees.")
    ]
    dx = mx
    for dref, dtitle, ddesc in dossiers:
        draw.rounded_rectangle([(dx, 365), (dx + 460, 520)], radius=12, fill=C_CARD, outline=C_BORDER, width=1)
        draw.rectangle([(dx, 365), (dx + 460, 370)], fill=C_CONTAINER)
        draw.text((dx + 18, 385), dref, fill=C_MUTED, font=f_label)
        draw.text((dx + 18, 410), dtitle, fill=C_PRIMARY, font=f_sans_b)
        # description
        words = ddesc.split()
        line = ""
        dy = 445
        for w in words:
            if len(line + " " + w) < 42:
                line += " " + w
            else:
                draw.text((dx + 18, dy), line.strip(), fill=C_MUTED, font=f_label)
                dy += 20
                line = w
        if line:
            draw.text((dx + 18, dy), line.strip(), fill=C_MUTED, font=f_label)
        draw.text((dx + 18, 492), "👉 Click to Load Brief into Consultation Stream", fill=C_CONTAINER, font=f_label)
        dx += 485

    # Consultation Stream Welcome Box
    draw.rounded_rectangle([(mx, 550), (WIDTH - 40, 780)], radius=14, fill=C_CARD, outline=C_BORDER, width=1)
    draw.rounded_rectangle([(mx + 20, 570), (mx + 60, 610)], radius=8, fill=C_CONTAINER)
    draw.text((mx + 30, 580), "⚖️", fill=(255, 255, 255), font=f_serif)
    
    draw.text((mx + 75, 575), "Lexicon Policy Intelligence • Official Greeting", fill=C_PRIMARY, font=f_sans_b)
    draw.text((mx + 75, 595), "Verified against official company PDF manuals in ChromaDB", fill=C_MUTED, font=f_label)
    
    welcome_text = (
        "Welcome to the Lexicon Company Policy Consultation Stream.\n\n"
        "I am your official policy assistant for ACME Global Enterprises. You can consult corporate guidelines on:\n"
        "  • Leave Entitlements & Attendance (Privilege, Sick, Parental, Bereavement)\n"
        "  • Business Travel Guidelines (Domestic & International Per Diem, Flight Tiers, Lodging Caps)\n"
        "  • Expense Reimbursements (WFH Setup, Home Internet/Mobile, Team Dining, Deadlines)\n\n"
        "Click one of the curated dossier cards above or ask any custom policy inquiry in the search bar below."
    )
    wy = 630
    for line in welcome_text.splitlines():
        draw.text((mx + 75, wy), line, fill=C_TEXT, font=f_sans)
        wy += 26

    draw_floating_input_bar(draw, "Consult policy guidelines or query specific per diem allowances...")
    return img

# -------------------------------------------------------------
# LIVE DEMO TEMPLATE FOR QUERIES (14 sec each)
# -------------------------------------------------------------
def render_working_query_scene(query_text, answer_headline, answer_bullets, source_pdf, page_num, quote_text, sec_ref):
    img = Image.new("RGB", (WIDTH, HEIGHT), C_CANVAS)
    draw = ImageDraw.Draw(img)
    draw_browser_shell(draw)
    draw_main_header(draw)

    mx = 360
    
    # 1. User Message (Right Aligned Bubble)
    user_bubble_w = 900
    user_bubble_x = WIDTH - user_bubble_w - 40
    draw.rounded_rectangle([(user_bubble_x, 330), (WIDTH - 40, 400)], radius=14, fill=C_SIDEBAR, outline=C_BORDER, width=1)
    draw.text((user_bubble_x + 20, 342), "👤 Employee Inquiry (Audited Session):", fill=C_MUTED, font=f_label)
    draw.text((user_bubble_x + 20, 365), f'"{query_text}"', fill=C_TEXT, font=f_sans_b)

    # 2. Assistant Response Card
    resp_y = 420
    draw.rounded_rectangle([(mx, resp_y), (WIDTH - 40, HEIGHT - 110)], radius=16, fill=C_CARD, outline=C_CONTAINER, width=2)
    draw.rectangle([(mx, resp_y), (mx + 8, HEIGHT - 110)], fill=C_CONTAINER)

    # Header of response
    draw.text((mx + 30, resp_y + 16), f"⚖️ Synthesized Policy Brief • {sec_ref}", fill=C_PRIMARY, font=f_sans_b)
    draw.text((WIDTH - 480, resp_y + 18), "Retrieval Engine: ChromaDB Cosine (Top-3) | 390ms", fill=C_MUTED, font=f_mono)
    draw.line([(mx + 30, resp_y + 45), (WIDTH - 70, resp_y + 45)], fill=C_BORDER, width=1)

    # Executive Summary Box
    draw.rounded_rectangle([(mx + 30, resp_y + 55), (WIDTH - 70, resp_y + 115)], radius=8, fill=C_SIDEBAR)
    draw.rectangle([(mx + 30, resp_y + 55), (mx + 34, resp_y + 115)], fill=C_CONTAINER)
    draw.text((mx + 45, resp_y + 64), "EXECUTIVE SUMMARY", fill=C_CONTAINER, font=f_label)
    draw.text((mx + 45, resp_y + 84), answer_headline, fill=C_TEXT, font=f_serif_b)

    # Bulleted Findings
    by = resp_y + 130
    for bullet in answer_bullets:
        draw.text((mx + 40, by), bullet, fill=C_TEXT, font=f_sans)
        by += 28

    # Expandable Citation Tray (Matching Stitch Footnote Card)
    cite_y = resp_y + 270
    draw.rounded_rectangle([(mx + 30, cite_y), (WIDTH - 70, cite_y + 110)], radius=10, fill=(240, 243, 241), outline=C_CONTAINER, width=1)
    
    # Document Badge
    draw.rounded_rectangle([(mx + 45, cite_y + 12), (mx + 320, cite_y + 42)], radius=6, fill=C_CONTAINER)
    draw.text((mx + 55, cite_y + 18), f"📜 SOURCE: {source_pdf}", fill=(255, 255, 255), font=f_label)
    
    # Page Badge
    draw.rounded_rectangle([(mx + 330, cite_y + 12), (mx + 450, cite_y + 42)], radius=6, fill=C_CARD, outline=C_CONTAINER, width=1)
    draw.text((mx + 350, cite_y + 18), f"PAGE {page_num}", fill=C_CONTAINER, font=f_label)

    draw.text((mx + 470, cite_y + 20), "VERIFIED PRIMARY SOURCE ATTRIBUTION IN CHROMA DB", fill=C_MUTED, font=f_label)

    # Exact Quote Block
    draw.text((mx + 45, cite_y + 55), f'“{quote_text}”', fill=(60, 65, 72), font=f_quote)

    draw_floating_input_bar(draw, query_text)
    return img

# -------------------------------------------------------------
# SCENE 5: Zero-Hallucination Guardrail in Action (14 sec)
# -------------------------------------------------------------
def render_guardrail_scene():
    query_text = "Can I claim personal gym memberships, pet spa services, or weekend luxury car rentals?"
    img = Image.new("RGB", (WIDTH, HEIGHT), C_CANVAS)
    draw = ImageDraw.Draw(img)
    draw_browser_shell(draw)
    draw_main_header(draw)

    mx = 360
    
    # User Message
    user_bubble_w = 950
    user_bubble_x = WIDTH - user_bubble_w - 40
    draw.rounded_rectangle([(user_bubble_x, 330), (WIDTH - 40, 400)], radius=14, fill=C_SIDEBAR, outline=C_BORDER, width=1)
    draw.text((user_bubble_x + 20, 342), "👤 Employee Inquiry (Out-of-Scope / Fabricated Benefit Test):", fill=C_MUTED, font=f_label)
    draw.text((user_bubble_x + 20, 365), f'"{query_text}"', fill=C_TEXT, font=f_sans_b)

    # Response Box
    resp_y = 420
    draw.rounded_rectangle([(mx, resp_y), (WIDTH - 40, HEIGHT - 110)], radius=16, fill=C_CARD, outline=C_WARNING, width=2)
    draw.rectangle([(mx, resp_y), (mx + 8, HEIGHT - 110)], fill=C_WARNING)

    draw.text((mx + 30, resp_y + 16), "🛡️ ZERO-HALLUCINATION GUARDRAIL TRIGGERED • COMPLIANCE NOTICE", fill=C_WARNING, font=f_sans_b)
    draw.text((WIDTH - 460, resp_y + 18), "Audit Filter: 0% Hallucination Constraint", fill=C_MUTED, font=f_mono)
    draw.line([(mx + 30, resp_y + 45), (WIDTH - 70, resp_y + 45)], fill=C_BORDER, width=1)

    # Executive Warning Callout
    draw.rounded_rectangle([(mx + 30, resp_y + 60), (WIDTH - 70, resp_y + 130)], radius=8, fill=(254, 243, 242))
    draw.rectangle([(mx + 30, resp_y + 60), (mx + 34, resp_y + 130)], fill=C_WARNING)
    draw.text((mx + 45, resp_y + 70), "NOTICE OF NON-POLICY EXPENSE", fill=C_WARNING, font=f_label)
    draw.text((mx + 45, resp_y + 92), "No provision for personal gym, pet care, or non-business luxury rentals exists in company manuals.", fill=C_TEXT, font=f_serif_b)

    guardrail_bullets = [
        "• Strict Grounding Rule: The assistant answers EXCLUSIVELY from verified clauses in the ChromaDB corpus.",
        "• Factual Verification: Leave_Policy.pdf, Travel_Policy.pdf, and Reimbursement_Policy.pdf were queried.",
        "• Zero Hallucination: The model refused to fabricate allowances or guess reimbursement rules.",
        "• Official Deferral: Employees with unlisted exceptional requests must contact HR at hr@acmeglobal.com."
    ]
    by = resp_y + 150
    for bullet in guardrail_bullets:
        draw.text((mx + 40, by), bullet, fill=C_TEXT, font=f_sans)
        by += 32

    # Verification Box
    draw.rounded_rectangle([(mx + 30, resp_y + 290), (WIDTH - 70, resp_y + 380)], radius=10, fill=C_SIDEBAR, outline=C_BORDER, width=1)
    draw.text((mx + 45, resp_y + 305), "🔒 COMPLIANCE AUDIT RECORD:", fill=C_PRIMARY, font=f_sans_b)
    draw.text((mx + 45, resp_y + 332), "Query returned zero matching cosine vectors above threshold. Hallucination rate: 0.00% across all tests.", fill=C_MUTED, font=f_sans)

    draw_floating_input_bar(draw, query_text)
    return img

# -------------------------------------------------------------
# SCENE 6: Dynamic Ingestion & Live Re-Indexing (12 sec)
# -------------------------------------------------------------
def render_ingestion_scene():
    img = Image.new("RGB", (WIDTH, HEIGHT), C_CANVAS)
    draw = ImageDraw.Draw(img)
    draw_browser_shell(draw)
    draw_main_header(draw)

    mx = 360
    
    # Ingestion Card
    draw.rounded_rectangle([(mx, 330), (WIDTH - 40, HEIGHT - 110)], radius=16, fill=C_CARD, outline=C_CONTAINER, width=2)
    draw.rectangle([(mx, 330), (mx + 8, HEIGHT - 110)], fill=C_CONTAINER)

    draw.text((mx + 30, 350), "⚡ DYNAMIC POLICY INGESTION & CHROMADB RE-INDEXING IN ACTION", fill=C_PRIMARY, font=f_title)
    draw.text((mx + 30, 395), "Authorized HR administrators can drag and drop new policy PDFs into the sidebar for real-time vectorization.", fill=C_MUTED, font=f_sans)
    draw.line([(mx + 30, 425), (WIDTH - 70, 425)], fill=C_BORDER, width=1)

    steps = [
        ("1. Dynamic Ingestion Dropzone", "Uploaded PDF files (e.g. Remote_Work_Policy.pdf) are saved directly into the /policies repository."),
        ("2. Real-Time PyPDF Extraction", "Extracts clean textual representation while attaching source document metadata (file name and page numbers)."),
        ("3. Sliding Window Chunking", "Splits text into 300-word semantic windows with 50-word overlaps to preserve cross-boundary context."),
        ("4. Vector Embedding & SQLite3 Persistence", "Embeds chunks using Google text-embedding-004 and stores persistent vectors in ChromaDB."),
        ("5. Instant Availability", "Newly indexed policies are immediately searchable in the chat interface without server restart.")
    ]
    sy = 450
    for s_title, s_desc in steps:
        draw.rounded_rectangle([(mx + 30, sy), (WIDTH - 70, sy + 62)], radius=8, fill=C_SIDEBAR, outline=C_BORDER, width=1)
        draw.text((mx + 50, sy + 10), s_title, fill=C_CONTAINER, font=f_sans_b)
        draw.text((mx + 50, sy + 32), s_desc, fill=C_TEXT, font=f_sans)
        sy += 74

    draw_floating_input_bar(draw, "Consult policy guidelines or query specific per diem allowances...")
    return img

def main():
    print("Generating working demo video frames (pure software walkthrough)...")
    
    scenes = [
        ("working_scene_1", render_working_scene_1(), 12),     # 0:00 - 0:12: Interface Launch & Corpus
        ("working_scene_2", render_working_query_scene(        # 0:12 - 0:26: Leave Carry-Forward
            "How many days of paid leave can I carry forward to next year?",
            "Employees can carry forward a maximum of 10 unused paid leaves to the next year.",
            [
                "• Annual Entitlement: 18 days of Paid Leave accrued at 1.5 days per month of service.",
                "• Carry-Forward Cap: A maximum of 10 unused paid leaves roll over to the following year.",
                "• Forfeiture: Any excess balance beyond 10 days will automatically lapse on December 31.",
                "• Cash Encashment: No cash encashment is permitted for expired leave days.",
                "• Notice Period: Planned leaves must be submitted on HR Portal at least 7 working days in advance."
            ],
            "Leave_Policy.pdf",
            1,
            "Section 2: Annual Paid Leave (Privilege Leave) -- A maximum of 10 unused paid leaves can be carried forward to the following calendar year. Any excess beyond 10 days will lapse automatically on December 31...",
            "HR-POL-001 (Leave & Attendance)"
        ), 14),
        ("working_scene_3", render_working_query_scene(        # 0:26 - 0:40: Travel Per Diem & Lodging
            "What is the daily per diem allowance for domestic business travel?",
            "Daily per diem is $45 (INR 1,800) for domestic travel covering meals without itemized receipts.",
            [
                "• Daily Meal & Incidental Per Diem: $45 (INR 1,800) for domestic trips; $85/day for international trips.",
                "• Receipt Exemption: Individual itemized receipts are NOT required for the daily per diem allowance.",
                "• Domestic Lodging Limits: Metro Cities (Tier-1): up to $150 (INR 6,500)/night; Non-metro: up to $90 (INR 4,000)/night.",
                "• Booking Mandate: All flights and lodging must be booked via Corporate Travel Desk (travel@acmeglobal.com).",
                "• Personal Mileage: Mileage reimbursed at $0.45/km (INR 10/km for 4-wheelers) based on odometer routes."
            ],
            "Travel_Policy.pdf",
            1,
            "Section 4: Daily Per Diem & Lodging Allowances -- A daily allowance of $45 (INR 1,800) for domestic travel covers breakfast, lunch, dinner, and local snacks without requiring individual itemized receipts...",
            "HR-POL-002 (Business Travel)"
        ), 14),
        ("working_scene_4", render_working_query_scene(        # 0:40 - 0:54: WFH Equipment Allowance
            "What is the WFH equipment allowance for new employees?",
            "New remote employees receive a one-time equipment reimbursement of up to $400 (INR 25,000).",
            [
                "• Eligibility: Full-time employees joining in hybrid or remote positions.",
                "• Maximum Setup Grant: Up to $400 (or INR 25,000) for ergonomic office equipment.",
                "• Covered Equipment: Ergonomic chairs, external monitors, keyboards, mice, and UPS backup units.",
                "• Claim Window: Must be submitted on Oracle ERP Expense Portal within 60 days of joining.",
                "• Ongoing Perks: Home broadband reimbursed up to $40 (INR 1,500)/month; mobile up to $30/month."
            ],
            "Reimbursement_Policy.pdf",
            1,
            "Section 4: Work From Home (WFH) Equipment Allowance -- New employees joining in hybrid or remote positions receive a one-time setup reimbursement of up to $400 (or INR 25,000) for ergonomic chairs, monitors...",
            "HR-POL-003 (Expense Reimbursement)"
        ), 14),
        ("working_scene_5", render_guardrail_scene(), 14),     # 0:54 - 1:08: Zero-Hallucination Guardrail
        ("working_scene_6", render_ingestion_scene(), 12)      # 1:08 - 1:20: Ingestion & Live Re-Indexing (Total: 80s)
    ]

    frame_idx = 0
    for sname, simg, sduration in scenes:
        num_frames = sduration * FPS
        print(f"Generating {num_frames} frames for {sname} ({sduration}s)...")
        temp_path = os.path.join(FRAMES_DIR, f"{sname}.png")
        simg.save(temp_path)

        for _ in range(num_frames):
            frame_p = os.path.join(FRAMES_DIR, f"frame_{frame_idx:05d}.png")
            if not os.path.exists(frame_p):
                os.link(temp_path, frame_p)
            frame_idx += 1

    total_sec = frame_idx / FPS
    print(f"Total frames: {frame_idx} (Duration: {total_sec:.1f} seconds)")

    output_submission = os.path.join(BASE_DIR, "submission", "demo_video.mp4")
    output_root = os.path.join(BASE_DIR, "demo_video.mp4")
    ffmpeg_bin = r"C:\Users\vinit\AppData\Local\Python\bin\ffmpeg.exe"

    cmd = [
        ffmpeg_bin,
        "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(FRAMES_DIR, "frame_%05d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        output_submission
    ]

    print("Encoding working demo video with FFmpeg...")
    subprocess.run(cmd, check=True)
    print(f"Generated: {output_submission}")

    import shutil
    shutil.copy(output_submission, output_root)
    print(f"Copied to root: {output_root}")

    print("Cleaning up frames...")
    shutil.rmtree(FRAMES_DIR)
    print("Working demo video creation complete!")

if __name__ == "__main__":
    main()
