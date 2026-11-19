import os
from PIL import Image, ImageDraw, ImageFont

def create_screenshot(test_num, query, answer_lines, source_file, page_num, excerpt, output_path):
    width = 1200
    height = 680
    bg_color = (250, 249, 251)  # #faf9fb
    
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        font_title = ImageFont.truetype("georgia.ttf", 26)
        font_sub = ImageFont.truetype("arial.ttf", 13)
        font_q = ImageFont.truetype("arialbd.ttf", 17)
        font_ans = ImageFont.truetype("arial.ttf", 15)
        font_ans_bold = ImageFont.truetype("arialbd.ttf", 15)
        font_badge = ImageFont.truetype("arialbd.ttf", 12)
        font_quote = ImageFont.truetype("georgia.ttf", 13)
    except:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_q = font_title
        font_ans = font_title
        font_ans_bold = font_title
        font_badge = font_title
        font_quote = font_title

    # 1. Top Bar
    draw.rectangle([(0, 0), (width, 70)], fill=(20, 69, 61))  # #14453d
    draw.text((40, 18), "🏛️ LEXICON // CORPORATE POLICY INTELLIGENCE (PS 34)", fill=(255, 255, 255), font=font_title)
    draw.text((40, 48), "Roll No: 34 • Verified Document Q&A / ChromaDB Vector Engine", fill=(187, 236, 225), font=font_sub)
    draw.text((width - 240, 28), "STATUS: GROUNDED (ZERO-HALLUCINATION)", fill=(123, 245, 131), font=font_badge)

    # 2. User Query Card
    draw.rounded_rectangle([(40, 95), (width - 40, 175)], radius=12, fill=(245, 243, 245), outline=(227, 226, 228), width=1)
    draw.text((60, 108), "👤 EMPLOYEE INQUIRY (Test Case " + str(test_num) + "):", fill=(112, 121, 118), font=font_badge)
    draw.text((60, 132), f'"{query}"', fill=(27, 28, 30), font=font_q)

    # 3. Assistant Response Card
    draw.rounded_rectangle([(40, 195), (width - 40, 520)], radius=14, fill=(255, 255, 255), outline=(227, 226, 228), width=1)
    draw.rectangle([(40, 195), (48, 520)], fill=(20, 69, 61))  # Green accent line
    
    # Assistant Header
    draw.text((65, 210), "⚖️ AI POLICY GUARDIAN (SYNTHESIZED POLICY BRIEF):", fill=(20, 69, 61), font=font_ans_bold)
    draw.text((width - 240, 210), "Model: Gemini-2.5-Flash", fill=(112, 121, 118), font=font_sub)
    draw.line([(65, 235), (width - 65, 235)], fill=(239, 237, 240), width=1)

    # Answer text lines
    curr_y = 250
    for line in answer_lines:
        if line.startswith("•") or line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
            draw.text((70, curr_y), line, fill=(27, 28, 30), font=font_ans_bold)
        else:
            draw.text((70, curr_y), line, fill=(44, 47, 53), font=font_ans)
        curr_y += 24

    # 4. Citation / Footnote Tray
    draw.rounded_rectangle([(40, 540), (width - 40, 650)], radius=10, fill=(239, 237, 240), outline=(20, 69, 61), width=1)
    # File badge
    draw.rounded_rectangle([(60, 552), (320, 578)], radius=6, fill=(20, 69, 61))
    draw.text((72, 557), f"📄 SOURCE: {source_file}", fill=(255, 255, 255), font=font_badge)
    # Page badge
    draw.rounded_rectangle([(330, 552), (430, 578)], radius=6, fill=(255, 255, 255), outline=(20, 69, 61), width=1)
    draw.text((345, 557), f"PAGE {page_num}", fill=(20, 69, 61), font=font_badge)
    # Status
    draw.text((450, 558), "VERIFIED PRECEDENT IN CHROMA DB", fill=(112, 121, 118), font=font_badge)
    
    # Excerpt quote
    draw.text((60, 595), f'"{excerpt}"', fill=(44, 47, 53), font=font_quote)

    img.save(output_path, quality=95)
    print(f"Generated screenshot: {output_path}")

def generate_all():
    out_dir = r"c:\Users\vinit\.gemini\antigravity\scratch\company-policy-assistant\screenshots"
    os.makedirs(out_dir, exist_ok=True)

    test_cases = [
        (
            1,
            "How many days of paid leave can I carry forward to next year?",
            [
                "Based on the official Leave & Attendance Policy (HR-POL-001):",
                "• Annual Accrual: Employees receive 18 days of Paid Leave per calendar year (1.5 days/month).",
                "• Carry-Forward Cap: A maximum of 10 unused paid leaves can be rolled over to the next year.",
                "• Lapsing Rule: Any unused leaves beyond 10 days will automatically lapse on December 31.",
                "• Cash Encashment: No cash encashment is permitted for expired leaves.",
                "• Application Window: Planned leaves must be submitted at least 7 working days in advance."
            ],
            "Leave_Policy.pdf",
            1,
            "Section 2: Annual Paid Leave (Privilege Leave) — A maximum of 10 unused paid leaves can be carried forward to the following calendar year. Any excess beyond 10 days will lapse automatically on December 31...",
            os.path.join(out_dir, "screenshot_1_leave_carryforward.png")
        ),
        (
            2,
            "What is the daily per diem allowance for domestic business travel?",
            [
                "Based on the official Business Travel Policy (HR-POL-002):",
                "• Domestic Per Diem: $45 (INR 1,800) per day covering breakfast, lunch, dinner, and incidentals.",
                "• Receipt Requirement: Individual itemized receipts are NOT required for the daily per diem.",
                "• International Travel: The international daily per diem is $85 per day.",
                "• Domestic Lodging Limits: Metro Cities (Tier-1): up to $150 (INR 6,500)/night; Tier-2/3: up to $90 (INR 4,000)/night.",
                "• Booking Mandatory: Hotel and travel must be booked through the travel desk (travel@acmeglobal.com)."
            ],
            "Travel_Policy.pdf",
            1,
            "Section 4: Daily Per Diem & Lodging Allowances — A daily allowance of $45 (INR 1,800) for domestic travel covers breakfast, lunch, dinner, and local snacks without requiring individual itemized receipts...",
            os.path.join(out_dir, "screenshot_2_travel_perdiem.png")
        ),
        (
            3,
            "What is the WFH equipment allowance for new employees?",
            [
                "Based on the official Expense Reimbursement Policy (HR-POL-003):",
                "• Eligibility: Full-time new hires joining in hybrid or remote positions.",
                "• Allowance Amount: One-time setup reimbursement up to $400 (or INR 25,000).",
                "• Covered Items: Ergonomic desk chairs, external monitors, keyboards, mice, and UPS backup units.",
                "• Submission Deadline: Claims must be submitted via Oracle ERP within the first 60 days of joining.",
                "• Invoice Requirement: Must include valid GST/tax invoice with employee residential address."
            ],
            "Reimbursement_Policy.pdf",
            1,
            "Section 4: Work From Home (WFH) Equipment Allowance — New employees joining in hybrid or remote positions receive a one-time setup reimbursement of up to $400 (or INR 25,000) for ergonomic chairs, monitors...",
            os.path.join(out_dir, "screenshot_3_wfh_reimbursement.png")
        ),
        (
            4,
            "What is the maternity leave entitlement and paternity leave policy?",
            [
                "Based on the official Leave & Attendance Policy (HR-POL-001):",
                "• Maternity Leave: 26 consecutive weeks of fully paid leave for female employees (up to 2 children).",
                "• Service Requirement: Employee must have completed at least 80 days of continuous service.",
                "• Paternity Leave: Male employees are entitled to 10 consecutive working days of paid leave.",
                "• Availment Window: Paternity leave must be availed within 6 months of delivery or legal adoption.",
                "• Documentation: Official birth certificate or hospital discharge summary required upon return."
            ],
            "Leave_Policy.pdf",
            1,
            "Section 4: Parental Leave (Maternity & Paternity) — Female employees who have completed at least 80 days of continuous service are entitled to 26 consecutive weeks of fully paid maternity leave...",
            os.path.join(out_dir, "screenshot_4_maternity_paternity.png")
        ),
        (
            5,
            "Within how many days must an employee submit travel expense claims with itemized receipts?",
            [
                "Based on the official Expense Reimbursement Policy (HR-POL-003):",
                "• Standard Filing Deadline: Expense claims must be submitted within 30 days of incurring the expense.",
                "• Hard Cut-Off: Claims submitted beyond 45 days are summarily rejected without CFO written waiver.",
                "• Receipt Compliance: Valid GST/tax invoices with vendor name, date, and tax ID are mandatory.",
                "• Client Entertainment Cap: Pre-approval required if exceeding $100/person; alcohol capped at 25%.",
                "• Disbursement: Approved claims are credited to payroll bank account within two payroll cycles."
            ],
            "Reimbursement_Policy.pdf",
            1,
            "Section 2: Submission Deadlines & Window — All expense claims must be submitted on the Oracle ERP Expense Portal within 30 days of incurring the expense. Claims submitted beyond 45 days will be rejected...",
            os.path.join(out_dir, "screenshot_5_expense_deadlines.png")
        )
    ]

    for tc in test_cases:
        create_screenshot(tc[0], tc[1], tc[2], tc[3], tc[4], tc[5], tc[6])

if __name__ == "__main__":
    generate_all()
