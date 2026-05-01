import os
import json
import shutil

# --- Config ---
SOURCE_SCORES = r"C:\Users\karle\PycharmProjects\loputoo\tulemused\tulemused_parim.json"
LOCAL_SCORES = "tulemused_parim.json"
MAPPINGS_FILE = "user_mappings.json"
ASSIGNMENT_ID = 79364

# --- Step 1: Copy scoring file locally ---
if not os.path.exists(LOCAL_SCORES):
    shutil.copy(SOURCE_SCORES, LOCAL_SCORES)
    print(f"Copied {SOURCE_SCORES} → {LOCAL_SCORES}")
else:
    print(f"{LOCAL_SCORES} already exists, skipping copy")

# --- Step 2: Load saved user mappings ---
with open(MAPPINGS_FILE, encoding="utf-8") as f:
    all_mappings = json.load(f)

# Handle both possible JSON shapes
if str(ASSIGNMENT_ID) in all_mappings:
    raw = all_mappings[str(ASSIGNMENT_ID)]
else:
    raw = all_mappings

participant_to_userid = {}
for participant_id, value in raw.items():
    if isinstance(value, dict):
        participant_to_userid[str(participant_id)] = value["userid"]
    else:
        participant_to_userid[str(participant_id)] = value

print(f"Loaded {len(participant_to_userid)} participant→userid mappings")

# --- Step 3: Load scoring data and replace participant IDs with userids ---
with open(LOCAL_SCORES, encoding="utf-8") as f:
    scores_data = json.load(f)

translated = []
unmapped = []
for entry in scores_data["hindamine"]:
    participant_id = str(entry["opilane"])
    if participant_id in participant_to_userid:
        new_entry = dict(entry)  # shallow copy
        new_entry["opilane"] = participant_to_userid[participant_id]
        translated.append(new_entry)
    else:
        unmapped.append(participant_id)

if unmapped:
    print(f"⚠ {len(unmapped)} participant IDs had no mapping: {unmapped}")

# --- Step 4: Save translated scoring file ---
output = {"hindamine": translated}
with open("tulemused_by_userid.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Translated {len(translated)} entries → tulemused_by_userid.json")