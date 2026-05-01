import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("MOODLE_WS_TOKEN")
ASSIGNMENT_ID = 79364

def call(function, **params):
    params.update({
        "wstoken": TOKEN,
        "wsfunction": function,
        "moodlewsrestformat": "json",
    })
    r = requests.post(f"https://moodle.ut.ee/webservice/rest/server.php", data=params)
    return r.json()

# Fetch participant_id → userid mapping
result = call("mod_assign_get_user_mappings",
              **{"assignmentids[0]": ASSIGNMENT_ID})

print(json.dumps(result, indent=2, ensure_ascii=False))

participant_to_userid = {}
for assignment in result["assignments"]:
    for m in assignment["mappings"]:
        participant_to_userid[m["id"]] = m["userid"]

with open("user_mappings.json", "w", encoding="utf-8") as f:
    json.dump(participant_to_userid, f, ensure_ascii=False, indent=2)

print(f"Saved {len(participant_to_userid)} mappings to user_mappings.json")