import json
import openpyxl

files = {
    "GPT-5.2": "tulemused_gpt52.json",
    "GPT-5.1": "tulemused_gpt51.json",
    "Gemini 3.1 Pro": "tulemused_gemini.json",
    "Sonnet 4.5": "tulemused_sonnet.json",
}

# Load all data into a dict: {student_name: {model: {punktid, tagasiside, ai_protsent}}}
all_data = {}
for model, filename in files.items():
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    for entry in data["hindamine"]:
        name = entry["opilane"]
        if name not in all_data:
            all_data[name] = {}
        all_data[name][model] = {
            "punktid": entry.get("punktid", ""),
            # "tagasiside": entry.get("tagasiside", ""),
            # "ai_protsent": entry.get("ai_toenaosus_protsent", ""),
        }

# Create Excel
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Hinded"

# Header row
models = list(files.keys())
header = ["Õpilane"]
for m in models:
    header += [f"{m} - Punktid"]  # , f"{m} - Tagasiside", f"{m} - AI %"]
header += ["Keskmine punktid"]  # , "Keskmine AI %"]
ws.append(header)

# Data rows
for student in sorted(all_data.keys()):
    row = [student]
    scores = []
    # ai_pcts = []
    for m in models:
        d = all_data[student].get(m, {})
        punktid = d.get("punktid", "")
        # tagasiside = d.get("tagasiside", "")
        # ai_protsent = d.get("ai_protsent", "")
        row += [punktid]  # , tagasiside, ai_protsent]
        if isinstance(punktid, (int, float)):
            scores.append(punktid)
        # if isinstance(ai_protsent, (int, float)):
        #     ai_pcts.append(ai_protsent)

    avg_score = round(sum(scores) / len(scores), 2) if scores else ""
    # avg_ai = round(sum(ai_pcts) / len(ai_pcts), 1) if ai_pcts else ""
    row += [avg_score]  # , avg_ai]
    ws.append(row)

# Auto-adjust column widths
for col in ws.columns:
    max_len = max(len(str(cell.value or "")) for cell in col)
    ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 50)

wb.save("koondtabel.xlsx")
print(f"Valmis! {len(all_data)} õpilast, salvestatud koondtabel.xlsx")