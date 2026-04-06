import pdfplumber
import json
import glob
import re

result = {}

# Matches "14.4", "14-4", or "4." (standalone, not part of 14.1/14.2/14.3 etc.)
PATTERN = re.compile(r'(?:14[-.]4\b|(?<!\d)4\.(?!\d))')

for pdf_path in glob.glob("*.pdf"):
    pages_text = []
    found = False
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text or not text.strip():
                continue
            if not found:
                match = PATTERN.search(text)
                if match:
                    found = True
                    pages_text.append(text[match.start():])
            else:
                pages_text.append(text)
    result[pdf_path] = pages_text

with open("test.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)