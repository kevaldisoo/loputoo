import pdfplumber
import json
import glob
import re
import os
import shutil

# Directory containing student submission subdirectories
SUBMISSIONS_DIR = "submissions"
OUTPUT_DIR = "opilaste_tood"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Subdirectory name format: "firstname lastname_studentid_assignsubmission_file"
for subdir in os.scandir(SUBMISSIONS_DIR):
    if not subdir.is_dir():
        continue
    parts = subdir.name.split("_")
    if len(parts) < 2:
        continue
    student_id = parts[1]
    for pdf_file in glob.glob(os.path.join(subdir.path, "*.pdf")):
        dest = os.path.join(OUTPUT_DIR, f"{student_id}.pdf")
        shutil.copy2(pdf_file, dest)

result = {}

# Matches "9.4", "9-4", or "4." (standalone, not part of 9.1/9.2/9.3 etc.)
PATTERN = re.compile(r'(?:9[-.]4\b|(?<!\d)4\.(?!\d))')

for pdf_path in glob.glob(os.path.join(OUTPUT_DIR, "*.pdf")):
    pages_text = []
    found = False
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text or not text.strip():
                continue
            pages_text.append(text)
            #if not found:
            #     match = PATTERN.search(text)
            #     if match:
            #         found = True
            #         pages_text.append(text[match.start():])
            #else:
            #     pages_text.append(text)
    result[os.path.basename(pdf_path)] = pages_text

with open("test.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)