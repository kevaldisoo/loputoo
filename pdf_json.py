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

# Matches "9.4", "9-4", "9_4", "Ülesanne 4", "4." or "1." (standalone)
PATTERN = re.compile(r'(?:9[-._]4\b|Ülesanne\s+4\b|(?<!\d)[14]\.(?!\d))')

FALLBACK_SENTENCE = "Kirjeldage võimalikult detailselt"

for pdf_path in glob.glob(os.path.join(OUTPUT_DIR, "*.pdf")):
    with pdfplumber.open(pdf_path) as pdf:
        all_pages = [page.extract_text() or "" for page in pdf.pages]

    # Try primary pattern first
    matched_pages = []
    for i, text in enumerate(all_pages):
        match = PATTERN.search(text)
        if match:
            matched_pages = [text[match.start():]] + [
                t for t in all_pages[i + 1: i + 4] if t.strip()
            ]
            break

    # Fall back to sentence containing FALLBACK_SENTENCE if pattern not found.
    # The sentence may be preceded by "1." so look back for that prefix.
    if not matched_pages:
        for i, text in enumerate(all_pages):
            idx = text.find(FALLBACK_SENTENCE)
            if idx != -1:
                prefix = re.search(r'1\.\s*$', text[:idx])
                start = prefix.start() if prefix else idx
                matched_pages = [text[start:]] + [
                    t for t in all_pages[i + 1: i + 4] if t.strip()
                ]
                break

    student_id = os.path.splitext(os.path.basename(pdf_path))[0]
    result[int(student_id)] = matched_pages

with open("test.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)