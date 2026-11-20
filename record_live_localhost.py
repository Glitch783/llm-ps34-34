import os
import sys
import time
import glob
import subprocess
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUBMISSION_DIR = os.path.join(BASE_DIR, "submission")
SCREENSHOTS_DIR = os.path.join(SUBMISSION_DIR, "screenshots")
RECORDINGS_DIR = os.path.join(BASE_DIR, "scratch", "live_recordings")

os.makedirs(SUBMISSION_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(RECORDINGS_DIR, exist_ok=True)

from playwright.sync_api import sync_playwright

def record_localhost():
    print("=" * 60)
    print("STARTING LIVE RECORDING FROM http://localhost:8501")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True,
            args=["--start-maximized", "--no-sandbox", "--disable-gpu"]
        )
        
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=RECORDINGS_DIR,
            record_video_size={"width": 1920, "height": 1080}
        )
        
        page = context.new_page()
        
        print("Navigating to http://localhost:8501...")
        page.goto("http://localhost:8501", wait_until="networkidle", timeout=60000)
        time.sleep(3)

        # Wait for Streamlit to be fully rendered
        page.wait_for_selector('[data-testid="stAppViewContainer"]', timeout=30000)
        time.sleep(2)

        # 1. Capture Overview Screenshot of the Live Application
        print("Capturing Overview Screenshot (Screen 1)...")
        overview_path = os.path.join(SCREENSHOTS_DIR, "corporate_policy_digest_stitch.png")
        page.screenshot(path=overview_path)
        # Also copy to root screenshots
        root_sc_dir = os.path.join(BASE_DIR, "screenshots")
        os.makedirs(root_sc_dir, exist_ok=True)
        page.screenshot(path=os.path.join(root_sc_dir, "corporate_policy_digest_stitch.png"))
        print(f"  Saved live screenshot: {overview_path}")
        time.sleep(3)

        # 2. Configure API Key in sidebar if present in .env
        api_key = os.getenv("GEMINI_API_KEY", "")
        if api_key:
            print("Configuring Gemini API key into sidebar...")
            try:
                pw_input = page.locator('input[type="password"]').first
                if pw_input.is_visible():
                    pw_input.fill(api_key)
                    pw_input.press("Enter")
                    time.sleep(3)
            except Exception as e:
                print(f"  API key entry notice: {e}")

        # Helper to submit query via chat input
        def submit_query(query_text):
            chat_area = page.locator('textarea[data-testid="stChatInputTextArea"]').first
            chat_area.click()
            chat_area.fill(query_text)
            time.sleep(1)
            chat_area.press("Enter")
            print(f"  Submitted query: '{query_text}'")

        def wait_for_stream():
            time.sleep(2)
            try:
                spinners = page.locator('[data-testid="stSpinner"]')
                if spinners.count() > 0:
                    spinners.first.wait_for(state="detached", timeout=45000)
            except Exception:
                pass
            time.sleep(3)

        # 3. Query 1: Paid Leave Carry-Forward Limits
        print("\n--- Query 1: Annual Paid Leave & Carry-Forward ---")
        submit_query("How many days of paid leave can I carry forward to next year?")
        wait_for_stream()

        # Scroll to show response and expand citations if available
        page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        time.sleep(2)
        try:
            exp = page.locator('details[data-testid="stExpander"]').last
            if exp.is_visible() and not exp.get_attribute("open"):
                exp.locator('summary').click()
                time.sleep(2)
        except Exception:
            pass

        s1_path = os.path.join(SCREENSHOTS_DIR, "screenshot_1_leave_carryforward.png")
        page.screenshot(path=s1_path)
        page.screenshot(path=os.path.join(root_sc_dir, "screenshot_1_leave_carryforward.png"))
        print(f"  Saved Query 1 screenshot: {s1_path}")
        time.sleep(5)

        # 4. Query 2: Daily Per Diem & Travel Lodging
        print("\n--- Query 2: Daily Per Diem & Lodging Allowance ---")
        submit_query("What is the daily per diem allowance for domestic business travel?")
        wait_for_stream()

        page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        time.sleep(2)
        try:
            exp = page.locator('details[data-testid="stExpander"]').last
            if exp.is_visible() and not exp.get_attribute("open"):
                exp.locator('summary').click()
                time.sleep(2)
        except Exception:
            pass

        s2_path = os.path.join(SCREENSHOTS_DIR, "screenshot_2_travel_perdiem.png")
        page.screenshot(path=s2_path)
        page.screenshot(path=os.path.join(root_sc_dir, "screenshot_2_travel_perdiem.png"))
        print(f"  Saved Query 2 screenshot: {s2_path}")
        time.sleep(5)

        # 5. Query 3: WFH Equipment Allowance
        print("\n--- Query 3: Home Office / WFH Equipment Allowance ---")
        submit_query("What is the WFH equipment allowance for new employees?")
        wait_for_stream()

        page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        time.sleep(2)
        try:
            exp = page.locator('details[data-testid="stExpander"]').last
            if exp.is_visible() and not exp.get_attribute("open"):
                exp.locator('summary').click()
                time.sleep(2)
        except Exception:
            pass

        s3_path = os.path.join(SCREENSHOTS_DIR, "screenshot_3_wfh_reimbursement.png")
        page.screenshot(path=s3_path)
        page.screenshot(path=os.path.join(root_sc_dir, "screenshot_3_wfh_reimbursement.png"))
        print(f"  Saved Query 3 screenshot: {s3_path}")
        time.sleep(5)

        # 6. Query 4: Maternity / Paternity Leave
        print("\n--- Query 4: Maternity & Paternity Provisions ---")
        submit_query("What are the provisions for maternity and paternity leave?")
        wait_for_stream()

        page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        time.sleep(2)
        try:
            exp = page.locator('details[data-testid="stExpander"]').last
            if exp.is_visible() and not exp.get_attribute("open"):
                exp.locator('summary').click()
                time.sleep(2)
        except Exception:
            pass

        s4_path = os.path.join(SCREENSHOTS_DIR, "screenshot_4_maternity_paternity.png")
        page.screenshot(path=s4_path)
        page.screenshot(path=os.path.join(root_sc_dir, "screenshot_4_maternity_paternity.png"))
        print(f"  Saved Query 4 screenshot: {s4_path}")
        time.sleep(5)

        # 7. Query 5: Expense Submission Deadlines
        print("\n--- Query 5: Expense Submission Deadlines ---")
        submit_query("What is the deadline for submitting business travel expense claims?")
        wait_for_stream()

        page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        time.sleep(2)
        try:
            exp = page.locator('details[data-testid="stExpander"]').last
            if exp.is_visible() and not exp.get_attribute("open"):
                exp.locator('summary').click()
                time.sleep(2)
        except Exception:
            pass

        s5_path = os.path.join(SCREENSHOTS_DIR, "screenshot_5_expense_deadlines.png")
        page.screenshot(path=s5_path)
        page.screenshot(path=os.path.join(root_sc_dir, "screenshot_5_expense_deadlines.png"))
        print(f"  Saved Query 5 screenshot: {s5_path}")
        time.sleep(5)

        # 8. Query 6: Zero-Hallucination Guardrail Refusal Check
        print("\n--- Query 6: Guardrail Refusal Check ---")
        submit_query("Can I get reimbursement for my personal gym membership or pet food?")
        wait_for_stream()

        page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        time.sleep(5)

        # Showcase full consultation record by scrolling through
        print("Showcasing full consultation record...")
        page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'});")
        time.sleep(3)
        page.evaluate("window.scrollTo({top: 600, behavior: 'smooth'});")
        time.sleep(3)
        page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        time.sleep(4)

        print("Finalizing video capture...")
        page.close()
        context.close()
        browser.close()

    print("Browser closed. Finding recorded webm file...")
    recorded_videos = glob.glob(os.path.join(RECORDINGS_DIR, "*.webm"))
    if not recorded_videos:
        print("ERROR: No .webm video found in recordings directory!")
        return

    latest_video = max(recorded_videos, key=os.path.getctime)
    print(f"Original webm recording: {latest_video} ({os.path.getsize(latest_video) / 1024:.1f} KB)")

    ffmpeg_bin = r"C:\Users\vinit\AppData\Local\Python\bin\ffmpeg.exe"
    output_submission_mp4 = os.path.join(SUBMISSION_DIR, "demo_video.mp4")
    output_root_mp4 = os.path.join(BASE_DIR, "demo_video.mp4")

    # Transcode to standard H.264 mp4
    cmd = [
        ffmpeg_bin,
        "-y",
        "-i", latest_video,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        output_submission_mp4
    ]

    print(f"Transcoding video to {output_submission_mp4}...")
    subprocess.run(cmd, check=True)
    print(f"Transcoded successfully! Size: {os.path.getsize(output_submission_mp4) / 1024:.1f} KB")

    import shutil
    shutil.copy(output_submission_mp4, output_root_mp4)
    print(f"Copied demo_video.mp4 to root.")

    # Recreate Code.zip with the latest real assets
    print("Refreshing Code.zip package...")
    subprocess.run([sys.executable, os.path.join(BASE_DIR, "create_submission_zip.py")], check=True)
    print("=" * 60)
    print("LIVE RECORDING AND SCREENSHOT EXTRACTION COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    record_localhost()
