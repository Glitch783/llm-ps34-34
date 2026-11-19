"""
Script to generate sample HR Policy PDFs for Company Policy Assistant (PS 34)
Generates 3 realistic PDF files:
1. Leave_Policy.pdf
2. Travel_Policy.pdf
3. Reimbursement_Policy.pdf
"""
from fpdf import FPDF
import os

class PolicyPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, 'ACME Global Enterprises - Corporate HR Policy Manual', border=False, align='C')
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}} - Internal & Confidential HR Document', align='C')

def create_leave_policy(filepath):
    pdf = PolicyPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'POLICY DOC: HR-POL-001 - LEAVE & ATTENDANCE POLICY', ln=True)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.cell(0, 8, 'Effective Date: January 1, 2026 | Department: Human Resources', ln=True)
    pdf.ln(5)

    sections = [
        ("1. Purpose & Scope", 
         "This policy governs leave entitlements, applications, and approvals for all permanent and probationary full-time employees across all domestic and international branches of ACME Global."),
        
        ("2. Annual Paid Leave (Privilege Leave)",
         "Employees are credited with 18 days of Paid Leave per calendar year, accrued at 1.5 days per completed month of service. A maximum of 10 unused paid leaves can be carried forward to the following calendar year. Any excess beyond 10 days will lapse automatically on December 31 without cash encashment. Employees must apply for planned leave at least 7 working days in advance via the HR Portal."),
        
        ("3. Sick and Medical Leave",
         "All employees are allocated 12 days of paid Sick Leave each year. Sick leave is meant solely for personal illness, medical emergencies, or consultations. For any consecutive sick leave exceeding 3 continuous working days, a signed medical fitness certificate from a registered medical practitioner (MBBS or equivalent) must be uploaded to the HR portal upon resumption of duties."),
        
        ("4. Parental Leave (Maternity & Paternity)",
         "Maternity Leave: Female employees who have completed at least 80 days of continuous service are entitled to 26 consecutive weeks of fully paid maternity leave for up to two surviving children. Paternity Leave: Male employees are entitled to 10 consecutive working days of paid paternity leave, which must be availed within 6 months of child delivery or legal adoption."),
        
        ("5. Bereavement & Casual Leave",
         "Bereavement Leave: 5 consecutive days of paid leave are granted in the unfortunate event of the death of an immediate family member (spouse, child, parent, sibling). Casual Leave: 6 days per calendar year for unforeseen personal matters, with a maximum of 2 consecutive days at a time."),
        
        ("6. Compensatory Off (Comp-Off)",
         "Employees who work on officially declared company holidays or weekends under prior written approval from their Department Head are eligible for 1 Comp-Off day. Comp-Offs must be redeemed within 60 days of accrual, after which they expire.")
    ]

    for title, body in sections:
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(24, 43, 73)
        pdf.cell(0, 8, title, ln=True)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 6, body)
        pdf.ln(3)

    pdf.output(filepath)
    print(f"Created: {filepath}")

def create_travel_policy(filepath):
    pdf = PolicyPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'POLICY DOC: HR-POL-002 - BUSINESS TRAVEL POLICY', ln=True)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.cell(0, 8, 'Effective Date: January 1, 2026 | Department: Finance & Operations', ln=True)
    pdf.ln(5)

    sections = [
        ("1. Purpose & Scope",
         "This document defines the guidelines and financial boundaries for business travel undertaken by employees on behalf of ACME Global Enterprises."),
        
        ("2. Travel Authorization & Booking Process",
         "All domestic trips must be approved by the Department Head at least 5 business days in advance. International business travel requires prior approval from the Vice President / Business Unit Head at least 14 days in advance. All flight tickets and hotel bookings must be reserved exclusively through the corporate travel desk (travel@acmeglobal.com). Self-booked flights without prior travel desk exception approval will not be reimbursed."),
        
        ("3. Flight & Train Travel Tiers",
         "Tiers 1-3 (Associates to Senior Leads): Economy Class flight booking for flight journeys exceeding 4 hours, or AC 2-Tier train for journeys under 500 km. Tiers 4+ (Directors, VPs, Executives): Premium Economy or Business Class allowed for international flights exceeding 6 hours non-stop."),
        
        ("4. Daily Per Diem & Lodging Allowances",
         "Lodging Limits: Metro Cities (Tier 1): Up to $150 (or INR 6,500) per night inclusive of taxes. Non-Metro Cities (Tier 2/3): Up to $90 (or INR 4,000) per night. Daily Per Diem (Meals & Incidentals): A daily allowance of $45 (INR 1,800) for domestic travel covers breakfast, lunch, dinner, and local snacks without requiring individual itemized receipts. For international travel, the per diem is $85 per day."),
        
        ("5. Local Ground Conveyance & Mileage",
         "Employees are encouraged to utilize ride-sharing services (Uber/Ola Corporate) or prepaid airport taxis. If using personal vehicles for approved business visits, mileage reimbursement is paid at $0.45 per kilometer (or INR 10/km for 4-wheelers and INR 5/km for 2-wheelers), verified via odometer readings and Google Maps routes.")
    ]

    for title, body in sections:
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(24, 43, 73)
        pdf.cell(0, 8, title, ln=True)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 6, body)
        pdf.ln(3)

    pdf.output(filepath)
    print(f"Created: {filepath}")

def create_reimbursement_policy(filepath):
    pdf = PolicyPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'POLICY DOC: HR-POL-003 - EXPENSE REIMBURSEMENT POLICY', ln=True)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.cell(0, 8, 'Effective Date: January 1, 2026 | Department: Finance & Accounts', ln=True)
    pdf.ln(5)

    sections = [
        ("1. Purpose & General Principles",
         "ACME Global reimburses employees for fair, reasonable, and actual expenses incurred directly in the discharge of official duties. All claims must be accompanied by valid GST/tax invoices displaying the vendor name, date, description, and tax identification number."),
        
        ("2. Submission Deadlines & Window",
         "All expense claims must be submitted on the Oracle ERP Expense Portal within 30 days of incurring the expense. Claims submitted beyond 45 days will be summarily rejected unless an explicit written waiver is granted by the Chief Financial Officer (CFO). Approved claims are credited directly to the employee payroll bank account within two payroll cycles."),
        
        ("3. Home Internet & Mobile Phone Reimbursement",
         "Full-time remote and hybrid employees are eligible for home broadband internet reimbursement up to $40 (or INR 1,500) per month. For client-facing roles (Sales, Support, Consulting), mobile phone bills are reimbursed up to $30 (or INR 1,200) monthly. Bills must reflect the employee's residential address or name."),
        
        ("4. Work From Home (WFH) Equipment Allowance",
         "New employees joining in hybrid or remote positions receive a one-time setup reimbursement of up to $400 (or INR 25,000) for ergonomic chairs, external monitors, keyboards, mice, and UPS devices. Claims must be submitted within the first 60 days of joining."),
        
        ("5. Client Entertainment & Team Dining",
         "Business meals with prospective clients or partners require pre-approval if the estimated cost exceeds $100 per person. Itemized receipts with attendee names and business agenda must be attached. Alcohol expenses are capped at a maximum of 25% of the total food bill. Team bonding lunches are capped at $25 (INR 1,000) per employee once per quarter."),
        
        ("6. Professional Certifications & Learning Stipend",
         "Every permanent employee with at least 6 months tenure can claim up to $500 (INR 40,000) annually for approved technical certifications (AWS, GCP, PMP, Scrum) or conference passes. Reimbursement is disbursed upon submitting proof of passing/completion certificate.")
    ]

    for title, body in sections:
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(24, 43, 73)
        pdf.cell(0, 8, title, ln=True)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 6, body)
        pdf.ln(3)

    pdf.output(filepath)
    print(f"Created: {filepath}")

if __name__ == "__main__":
    out_dir = r"C:\Users\vinit\.gemini\antigravity\scratch\company-policy-assistant\policies"
    os.makedirs(out_dir, exist_ok=True)
    create_leave_policy(os.path.join(out_dir, "Leave_Policy.pdf"))
    create_travel_policy(os.path.join(out_dir, "Travel_Policy.pdf"))
    create_reimbursement_policy(os.path.join(out_dir, "Reimbursement_Policy.pdf"))
    print("All 3 policy documents successfully generated!")
