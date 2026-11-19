import os
import zipfile
import shutil

BASE_DIR = r"c:\Users\vinit\.gemini\antigravity\scratch\company-policy-assistant"
SUBMISSION_DIR = os.path.join(BASE_DIR, "submission")
os.makedirs(SUBMISSION_DIR, exist_ok=True)

# 1. Package Code.zip
zip_path = os.path.join(SUBMISSION_DIR, "Code.zip")
files_to_include = [
    "app.py",
    "rag_pipeline.py",
    "generate_policies.py",
    "create_screenshots.py",
    "create_report_pdf.py",
    "requirements.txt",
    "README.md",
    "github_link.txt"
]

folders_to_include = [
    ".streamlit",
    "policies",
    "screenshots",
    "stitch_design"
]

print("Packaging Code.zip...")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    # Add root files
    for f in files_to_include:
        fpath = os.path.join(BASE_DIR, f)
        if os.path.exists(fpath):
            zipf.write(fpath, arcname=f)
            print(f"  + Added: {f}")

    # Add folders
    for folder in folders_to_include:
        folder_path = os.path.join(BASE_DIR, folder)
        if os.path.exists(folder_path):
            for root, dirs, files in os.walk(folder_path):
                # Filter out cache
                dirs[:] = [d for d in dirs if d not in ["__pycache__", ".git"]]
                for file in files:
                    if file.endswith((".pyc", ".pyo")):
                        continue
                    full_p = os.path.join(root, file)
                    rel_p = os.path.relpath(full_p, BASE_DIR)
                    zipf.write(full_p, arcname=rel_p)
                    print(f"  + Added: {rel_p}")

print(f"Code.zip created at {zip_path} (Size: {round(os.path.getsize(zip_path)/1024, 1)} KB)")

# Also copy Code.zip to root workspace
shutil.copy(zip_path, os.path.join(BASE_DIR, "Code.zip"))

# 2. Copy Report.pdf to submission folder
report_src = os.path.join(BASE_DIR, "Report.pdf")
if os.path.exists(report_src):
    shutil.copy(report_src, os.path.join(SUBMISSION_DIR, "Report.pdf"))
    print("Copied Report.pdf to submission directory.")

# 3. Copy github_link.txt to submission folder
gh_src = os.path.join(BASE_DIR, "github_link.txt")
if os.path.exists(gh_src):
    shutil.copy(gh_src, os.path.join(SUBMISSION_DIR, "github_link.txt"))
    print("Copied github_link.txt to submission directory.")

# 4. Copy screenshots folder to submission folder
sub_screenshots = os.path.join(SUBMISSION_DIR, "screenshots")
if os.path.exists(sub_screenshots):
    shutil.rmtree(sub_screenshots)
shutil.copytree(os.path.join(BASE_DIR, "screenshots"), sub_screenshots)
print("Copied screenshots/ folder to submission directory.")

print("\n--- SUBMISSION FOLDER SUMMARY ---")
for item in os.listdir(SUBMISSION_DIR):
    item_p = os.path.join(SUBMISSION_DIR, item)
    if os.path.isdir(item_p):
        print(f"📁 {item}/ ({len(os.listdir(item_p))} items)")
    else:
        print(f"📄 {item} ({round(os.path.getsize(item_p)/1024, 1)} KB)")
