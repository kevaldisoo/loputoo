import json

with open("../tulemused/tulemused_gemini.json", "r", encoding="utf-8") as f:
    gemini_data = json.load(f)

with open("../tulemused/tulemused_gpt51.json", "r", encoding="utf-8") as f:
    gpt_data = json.load(f)

gemini_map = {entry["opilane"]: entry for entry in gemini_data["hindamine"]}
gpt_map = {entry["opilane"]: entry for entry in gpt_data["hindamine"]}

all_students = set(gemini_map) | set(gpt_map)

result = []
for opilane in sorted(all_students):
    gemini_entry = gemini_map.get(opilane)
    gpt_entry = gpt_map.get(opilane)

    if gemini_entry and gpt_entry:
        if gpt_entry["punktid"] > gemini_entry["punktid"]:
            chosen = gpt_entry
        else:
            chosen = gemini_entry
    elif gemini_entry:
        chosen = gemini_entry
    else:
        chosen = gpt_entry

    result.append(chosen)

output = {"hindamine": result}

with open("../tulemused/tulemused_parim.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Valmis. {len(result)} tudengit lisatud faili tulemused_parim.json")
