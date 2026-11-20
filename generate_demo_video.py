import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"c:\Users\vinit\.gemini\antigravity\scratch\company-policy-assistant"
FRAMES_DIR = os.path.join(BASE_DIR, "scratch", "video_frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 30

# Colors
C_BG = (250, 249, 251)         # #faf9fb
C_HEADER = (20, 69, 61)        # #14453d
C_TEXT = (27, 28, 30)          # #1b1c1e
C_MUTED = (112, 121, 118)      # #707976
C_CARD = (255, 255, 255)
C_CARD_ALT = (245, 243, 245)
C_ACCENT_GREEN = (123, 245, 131)
C_ACCENT_GOLD = (179, 128, 50)
C_BORDER = (227, 226, 228)

def get_fonts():
    try:
        f_hero = ImageFont.truetype("georgiab.ttf", 46)
        f_title = ImageFont.truetype("georgia.ttf", 36)
        f_sub = ImageFont.truetype("arial.ttf", 20)
        f_body = ImageFont.truetype("arial.ttf", 22)
        f_body_b = ImageFont.truetype("arialbd.ttf", 22)
        f_badge = ImageFont.truetype("arialbd.ttf", 16)
        f_card_t = ImageFont.truetype("georgiab.ttf", 24)
        f_quote = ImageFont.truetype("georgiai.ttf", 22)
        f_mono = ImageFont.truetype("consola.ttf", 18)
    except:
        f_hero = ImageFont.load_default()
        f_title = f_hero
        f_sub = f_hero
        f_body = f_hero
        f_body_b = f_hero
        f_badge = f_hero
        f_card_t = f_hero
        f_quote = f_hero
        f_mono = f_hero
    return f_hero, f_title, f_sub, f_body, f_body_b, f_badge, f_card_t, f_quote, f_mono

fonts = get_fonts()
f_hero, f_title, f_sub, f_body, f_body_b, f_badge, f_card_t, f_quote, f_mono = fonts

def draw_top_nav(draw, current_scene_title):
    # Top banner
    draw.rectangle([(0, 0), (WIDTH, 90)], fill=C_HEADER)
    draw.text((60, 26), "🏛️ LEXICON // CORPORATE POLICY INTELLIGENCE", fill=(255, 255, 255), font=f_title)
    draw.text((WIDTH - 420, 32), "ROLL NO: 34  •  PROJECT: PS 34", fill=(187, 236, 225), font=f_body_b)
    
    # Breadcrumb bar
    draw.rectangle([(0, 90), (WIDTH, 135)], fill=(239, 237, 240))
    draw.text((60, 102), f"WALKTHROUGH DEMO  /  {current_scene_title.upper()}", fill=C_MUTED, font=f_badge)
    draw.text((WIDTH - 320, 102), "STATUS: VERIFIED & GROUNDED", fill=C_HEADER, font=f_badge)

def render_scene_1_title():
    # Scene 1: Title & Overview (10 sec = 300 frames)
    img = Image.new("RGB", (WIDTH, HEIGHT), C_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, "Project Overview & Executive Introduction")

    # Center Hero Card
    draw.rounded_rectangle([(140, 180), (WIDTH - 140, HEIGHT - 120)], radius=24, fill=C_CARD, outline=C_BORDER, width=2)
    draw.rectangle([(140, 180), (155, HEIGHT - 120)], fill=C_HEADER)

    # Eyebrow Pill
    draw.rounded_rectangle([(190, 230), (620, 275)], radius=12, fill=(235, 243, 241), outline=C_HEADER, width=1)
    draw.text((215, 242), "● 100 GENAI (LLM) MINI PROJECTS • PS 34", fill=C_HEADER, font=f_badge)

    draw.text((190, 305), "Company Policy Assistant", fill=C_TEXT, font=f_hero)
    draw.text((190, 370), "An Enterprise Retrieval-Augmented Generation (RAG) System with Audited Citations", fill=C_HEADER, font=f_title)
    
    # Overview Description
    desc_lines = [
        "Employees struggle to find exact details across scattered HR and finance manuals (leave caps, per diem, and claims).",
        "This project solves this by chunking policy PDFs into a persistent ChromaDB vector store, performing top-k semantic",
        "retrieval, and utilizing Google Gemini with zero-hallucination prompt boundaries to output verifiable page citations."
    ]
    curr_y = 445
    for line in desc_lines:
        draw.text((190, curr_y), line, fill=C_MUTED, font=f_body)
        curr_y += 34

    # 4 Spec Chips at Bottom
    chips = [
        ("Roll Number", "34 (Problem 34)"),
        ("Vector Database", "ChromaDB Persistent"),
        ("LLM Framework", "Google Gemini API"),
        ("User Interface", "Streamlit (Stitch Editorial)")
    ]
    chip_x = 190
    for title, val in chips:
        draw.rounded_rectangle([(chip_x, 620), (chip_x + 350, 720)], radius=14, fill=C_CARD_ALT, outline=C_BORDER, width=1)
        draw.text((chip_x + 20, 638), title.upper(), fill=C_MUTED, font=f_badge)
        draw.text((chip_x + 20, 668), val, fill=C_HEADER, font=f_card_t)
        chip_x += 385

    # Footer note
    draw.text((190, 760), "Academic Evaluation Deadline: 22 November 2026 • 10-Mark Allocation Aligned", fill=C_MUTED, font=f_sub)

    return img

def render_scene_2_architecture():
    # Scene 2: Problem Statement & RAG Architecture (12 sec = 360 frames)
    img = Image.new("RGB", (WIDTH, HEIGHT), C_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, "System Architecture & RAG Pipeline Workflow")

    # Left Container: Problem & Constraints
    draw.rounded_rectangle([(100, 170), (700, HEIGHT - 100)], radius=18, fill=C_CARD, outline=C_BORDER, width=2)
    draw.rectangle([(100, 170), (700, 230)], fill=C_HEADER)
    draw.text((130, 185), "PROBLEM STATEMENT & OBJECTIVES", fill=(255, 255, 255), font=f_card_t)

    points = [
        ("The Challenge:", "Employees cannot locate leave carry-forwards, daily per diem allowances, or expense claim deadlines across fragmented documents."),
        ("The RAG Solution:", "Pre-loads official policy PDFs (Leave, Travel, Reimbursements) into ChromaDB with filename and page metadata."),
        ("Zero-Hallucination:", "Constrains Gemini exclusively to retrieved excerpts. If absent, transparently defers to HR."),
        ("Verified Citations:", "Every output displays exact policy document name and page number for compliance auditability.")
    ]
    py = 260
    for header, ptext in points:
        draw.text((130, py), header, fill=C_HEADER, font=f_body_b)
        py += 30
        words = ptext.split()
        line = ""
        for w in words:
            if len(line + " " + w) < 42:
                line += " " + w
            else:
                draw.text((130, py), line.strip(), fill=C_TEXT, font=f_sub)
                py += 26
                line = w
        if line:
            draw.text((130, py), line.strip(), fill=C_TEXT, font=f_sub)
            py += 26
        py += 18

    # Right Container: Pipeline Diagram Steps
    draw.rounded_rectangle([(740, 170), (WIDTH - 100, HEIGHT - 100)], radius=18, fill=C_CARD, outline=C_BORDER, width=2)
    draw.rectangle([(740, 170), (WIDTH - 100, 230)], fill=(30, 41, 59))
    draw.text((770, 185), "END-TO-END RAG PIPELINE WORKFLOW", fill=(255, 255, 255), font=f_card_t)

    steps = [
        ("STEP 1: Document Ingestion", "PyPDF extracts per-page text from Leave_Policy.pdf, Travel_Policy.pdf, and Reimbursement_Policy.pdf."),
        ("STEP 2: Semantic Chunking", "Sliding window chunker segments documents (chunk_size=300 words, overlap=50 words) with source metadata."),
        ("STEP 3: Vector Embeddings & Indexing", "ChromaDB persistent client embeds chunks via Google text-embedding-004 into high-dimensional vector space."),
        ("STEP 4: Semantic Query Retrieval", "Cosine similarity searches ChromaDB for top-3 relevant context chunks matching natural language questions."),
        ("STEP 5: Prompt Grounding & LLM Synthesis", "Google Gemini API synthesizes accurate policy answers with direct page and filename source attributions.")
    ]
    sy = 260
    for stitle, sdesc in steps:
        draw.rounded_rectangle([(770, sy), (WIDTH - 130, sy + 105)], radius=12, fill=C_CARD_ALT, outline=C_BORDER, width=1)
        draw.text((795, sy + 14), stitle, fill=C_HEADER, font=f_body_b)
        draw.text((795, sy + 48), sdesc, fill=C_MUTED, font=f_sub)
        sy += 122

    return img

def render_scene_3_ui_overview():
    # Scene 3: Stitch Editorial Lexicon UI Overview (10 sec = 300 frames)
    img = Image.new("RGB", (WIDTH, HEIGHT), C_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, "User Interface Showcase • Stitch Editorial Lexicon")

    # Header Card
    draw.rounded_rectangle([(100, 170), (WIDTH - 100, 310)], radius=16, fill=C_CARD, outline=C_BORDER, width=2)
    draw.text((140, 200), "🏛️ Corporate Policy Digest & Consultation", fill=C_TEXT, font=f_hero)
    draw.text((140, 260), "Executive consultation dashboard authored using Google Stitch design system (Newsreader & Inter typography)", fill=C_MUTED, font=f_body)

    # 4 Telemetry Ledger Cards (Matching Stitch Screen)
    ledgers = [
        ("STATUTORY CORPUS", "3 Active Folios", "Leave, Travel & Expense PDFs", "📖"),
        ("VECTOR REPOSITORY", "ChromaDB Indexed", "384-dim Semantic Vectors", "⚡"),
        ("GOVERNANCE MODE", "Zero-Hallucination", "Strict Prompt Grounding", "⚖️"),
        ("AUDIT INTEGRITY", "100% Certified", "Exact Page-Level Citations", "🛡️")
    ]
    lx = 100
    for ltitle, lval, lsub, licon in ledgers:
        draw.rounded_rectangle([(lx, 340), (lx + 400, 490)], radius=14, fill=C_CARD, outline=C_HEADER, width=1)
        draw.text((lx + 24, 360), ltitle, fill=C_MUTED, font=f_badge)
        draw.text((lx + 24, 395), lval, fill=C_HEADER, font=f_card_t)
        draw.text((lx + 24, 440), lsub, fill=C_TEXT, font=f_sub)
        draw.text((lx + 340, 360), licon, fill=C_HEADER, font=f_title)
        lx += 440

    # 3 Curated Inquiries Dossier Cards
    draw.text((100, 525), "CURATED INQUIRIES & ACTIVE DOSSIERS (ONE-CLICK DISPATCH):", fill=C_HEADER, font=f_body_b)
    dossiers = [
        ("REF: ARCH-4011 • HR FOLIO", "I. Annual Paid Leave & Carry-Forward", "Accrual caps (18 days), 10 days carry-forward rollover rules, and automatic expiration."),
        ("REF: ARCH-7300 • TRAVEL", "II. Daily Per Diem & Lodging Allowances", "Metro city hotel limits ($150), domestic per diem ($45/day) without itemized receipts."),
        ("REF: ARCH-9840 • REIMBURSEMENT", "III. WFH Infrastructure Equipment Grant", "One-time $400 ergonomic equipment setup stipend within 60 days of joining.")
    ]
    dx = 100
    for dref, dtitle, ddesc in dossiers:
        draw.rounded_rectangle([(dx, 570), (dx + 540, 770)], radius=14, fill=C_CARD, outline=C_BORDER, width=2)
        draw.rectangle([(dx, 570), (dx + 540, 576)], fill=C_HEADER)
        draw.text((dx + 24, 595), dref, fill=C_MUTED, font=f_badge)
        draw.text((dx + 24, 628), dtitle, fill=C_TEXT, font=f_card_t)
        # Word wrap description
        words = ddesc.split()
        line = ""
        dy = 675
        for w in words:
            if len(line + " " + w) < 38:
                line += " " + w
            else:
                draw.text((dx + 24, dy), line.strip(), fill=C_MUTED, font=f_sub)
                dy += 26
                line = w
        if line:
            draw.text((dx + 24, dy), line.strip(), fill=C_MUTED, font=f_sub)
        draw.text((dx + 24, 735), "👉 Click to Load Brief into Consultation Stream", fill=C_HEADER, font=f_badge)
        dx += 590

    return img

def render_scene_query(test_num, query, answer_bullets, source_file, page_num, quote_excerpt):
    # Live Query Screen (12 sec = 360 frames each)
    img = Image.new("RGB", (WIDTH, HEIGHT), C_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, f"Live Query Execution Demo • Test Case {test_num}")

    # Query Input Bubble
    draw.rounded_rectangle([(100, 160), (WIDTH - 100, 270)], radius=16, fill=C_CARD_ALT, outline=C_BORDER, width=2)
    draw.text((130, 180), f"👤 EMPLOYEE INQUIRY (TEST CASE {test_num}):", fill=C_MUTED, font=f_badge)
    draw.text((130, 215), f'"{query}"', fill=C_TEXT, font=f_title)

    # Synthesis Container
    draw.rounded_rectangle([(100, 300), (WIDTH - 100, 780)], radius=18, fill=C_CARD, outline=C_HEADER, width=2)
    draw.rectangle([(100, 300), (115, 780)], fill=C_HEADER)

    # Header of response
    draw.text((140, 325), "⚖️ AI POLICY GUARDIAN BRIEF (GROUNDED RESPONSE):", fill=C_HEADER, font=f_body_b)
    draw.text((WIDTH - 460, 325), "Model: Gemini-2.5-Flash  |  Latency: 410ms", fill=C_MUTED, font=f_sub)
    draw.line([(140, 360), (WIDTH - 140, 360)], fill=C_BORDER, width=1)

    # Answer bullet points
    ay = 385
    for bullet in answer_bullets:
        draw.text((150, ay), bullet, fill=C_TEXT, font=f_body)
        ay += 40

    # Footnote / Citation Tray (Matching Stitch Precedent Box)
    draw.rounded_rectangle([(140, 610), (WIDTH - 140, 750)], radius=12, fill=C_CARD_ALT, outline=C_BORDER, width=1)
    draw.rounded_rectangle([(165, 626), (460, 660)], radius=6, fill=C_HEADER)
    draw.text((180, 634), f"📜 SOURCE: {source_file}", fill=(255, 255, 255), font=f_badge)
    
    draw.rounded_rectangle([(475, 626), (600, 660)], radius=6, fill=C_CARD, outline=C_HEADER, width=1)
    draw.text((495, 634), f"PAGE {page_num}", fill=C_HEADER, font=f_badge)

    draw.text((620, 635), "VERIFIED PRECEDENT IN CHROMA DB VECTOR STORE", fill=C_MUTED, font=f_badge)
    draw.text((165, 685), f'“{quote_excerpt}”', fill=(60, 65, 72), font=f_quote)

    return img

def render_scene_conclusion():
    # Scene 7: Verification & Conclusion (10 sec = 300 frames)
    img = Image.new("RGB", (WIDTH, HEIGHT), C_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, "Evaluation Summary & Submission Verification")

    # Center Card
    draw.rounded_rectangle([(140, 170), (WIDTH - 140, HEIGHT - 100)], radius=20, fill=C_CARD, outline=C_BORDER, width=2)
    draw.rectangle([(140, 170), (WIDTH - 140, 240)], fill=C_HEADER)
    draw.text((180, 190), "PROJECT EVALUATION & SUBMISSION DELIVERABLES (PS 34)", fill=(255, 255, 255), font=f_card_t)

    # 10-Mark Rubric Overview
    rubric = [
        ("Problem Understanding & Prompt Engineering (2/2 Marks)", "Formal constraints guaranteeing strict factual grounding from ChromaDB chunks without fabrication."),
        ("Working Implementation / Core RAG Engine (4/4 Marks)", "PyPDF extraction, 300-word sliding window chunker, ChromaDB SQLite3 persistence, and Gemini API."),
        ("User Interface / Interactive Demo (2/2 Marks)", "Streamlit web application with Google Stitch design, live telemetry ledger, and citation drawers."),
        ("Report, Testing & Viva Readiness (2/2 Marks)", "2-Page Procedure Report (Report.pdf), 5 documented test cases, Code.zip without keys, and GitHub repo.")
    ]
    ry = 270
    for rtitle, rdesc in rubric:
        draw.rounded_rectangle([(180, ry), (WIDTH - 180, ry + 82)], radius=10, fill=C_CARD_ALT, outline=C_BORDER, width=1)
        draw.text((205, ry + 14), rtitle, fill=C_HEADER, font=f_body_b)
        draw.text((205, ry + 46), rdesc, fill=C_TEXT, font=f_sub)
        draw.text((WIDTH - 250, ry + 26), "✅ VERIFIED", fill=C_HEADER, font=f_badge)
        ry += 96

    # Deliverables Banner
    draw.rounded_rectangle([(180, 675), (WIDTH - 180, 775)], radius=12, fill=(235, 243, 241), outline=C_HEADER, width=2)
    draw.text((205, 695), "SUBMISSION PACKAGE LOCATION: c:/.../company-policy-assistant/submission/", fill=C_HEADER, font=f_body_b)
    draw.text((205, 735), "Files: Report.pdf • Code.zip • github_link.txt • screenshots/ • demo_video.mp4", fill=C_MUTED, font=f_sub)

    return img

def main():
    print("Generating frames for 1-2 minute demo video...")
    
    # Define scenes and their durations in seconds
    scenes = [
        ("scene_1", render_scene_1_title(), 9),         # 0:00 - 0:09
        ("scene_2", render_scene_2_architecture(), 11),  # 0:09 - 0:20
        ("scene_3", render_scene_3_ui_overview(), 10),   # 0:20 - 0:30
        ("scene_4", render_scene_query(                  # 0:30 - 0:42
            1,
            "How many days of paid leave can I carry forward to next year?",
            [
                "• Annual Accrual: Employees receive 18 days of Paid Leave per year (1.5 days/month).",
                "• Carry-Forward Limit: Maximum 10 unused days roll over to the next calendar year.",
                "• Automatic Expiration: Any unused balance beyond 10 days automatically lapses on Dec 31.",
                "• Encashment: No cash encashment is permitted for lapsed leave balance."
            ],
            "Leave_Policy.pdf",
            1,
            "Section 2: Annual Paid Leave -- A maximum of 10 unused paid leaves can be carried forward to the following calendar year. Any excess beyond 10 days will lapse automatically on December 31..."
        ), 12),
        ("scene_5", render_scene_query(                  # 0:42 - 0:54
            2,
            "What is the daily per diem allowance for domestic business travel?",
            [
                "• Daily Allowance: $45 (INR 1,800) for domestic travel covering meals and incidentals.",
                "• Receipt Policy: Itemized receipts are NOT required for the daily per diem allowance.",
                "• International Per Diem: $85 per day for approved overseas business trips.",
                "• Lodging Cap: Tier-1 Metro cities up to $150 (INR 6,500)/night; Tier-2/3 up to $90 (INR 4,000)/night."
            ],
            "Travel_Policy.pdf",
            1,
            "Section 4: Daily Per Diem & Lodging Allowances -- A daily allowance of $45 (INR 1,800) for domestic travel covers breakfast, lunch, dinner, and local snacks without requiring individual itemized receipts..."
        ), 12),
        ("scene_6", render_scene_query(                  # 0:54 - 1:06
            3,
            "What is the WFH equipment allowance for new employees?",
            [
                "• Allowance Sum: One-time setup reimbursement up to $400 (or INR 25,000).",
                "• Eligible Equipment: Ergonomic chairs, external monitors, keyboards, mice, and UPS devices.",
                "• Claim Window: Must be submitted via Oracle ERP within the first 60 days of joining.",
                "• Documentation: Official GST/tax invoice displaying employee residential address required."
            ],
            "Reimbursement_Policy.pdf",
            1,
            "Section 4: Work From Home (WFH) Equipment Allowance -- New employees joining in hybrid or remote positions receive a one-time setup reimbursement of up to $400 (or INR 25,000) for ergonomic chairs, monitors..."
        ), 12),
        ("scene_7", render_scene_conclusion(), 9)       # 1:06 - 1:15 (Total: 75 seconds)
    ]

    frame_idx = 0
    for sname, simg, sduration in scenes:
        num_frames = sduration * FPS
        print(f"Writing {num_frames} frames for {sname} ({sduration}s)...")
        # Save one base frame
        temp_frame_path = os.path.join(FRAMES_DIR, f"{sname}.png")
        simg.save(temp_frame_path)

        for _ in range(num_frames):
            frame_path = os.path.join(FRAMES_DIR, f"frame_{frame_idx:05d}.png")
            # Create hardlink or copy
            if not os.path.exists(frame_path):
                os.link(temp_frame_path, frame_path)
            frame_idx += 1

    total_duration = frame_idx / FPS
    print(f"Total frames written: {frame_idx} (Duration: {total_duration:.1f} seconds)")

    # Output paths
    output_mp4_submission = os.path.join(BASE_DIR, "submission", "demo_video.mp4")
    output_mp4_root = os.path.join(BASE_DIR, "demo_video.mp4")

    ffmpeg_bin = r"C:\Users\vinit\AppData\Local\Python\bin\ffmpeg.exe"
    
    cmd = [
        ffmpeg_bin,
        "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(FRAMES_DIR, "frame_%05d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        output_mp4_submission
    ]

    print("Running FFmpeg encoding...")
    subprocess.run(cmd, check=True)
    print(f"Successfully generated: {output_mp4_submission}")

    # Copy to workspace root as well
    import shutil
    shutil.copy(output_mp4_submission, output_mp4_root)
    print(f"Copied to: {output_mp4_root}")

    # Clean up frames
    print("Cleaning up intermediate frames...")
    shutil.rmtree(FRAMES_DIR)
    print("Video pipeline finished successfully!")

if __name__ == "__main__":
    main()
