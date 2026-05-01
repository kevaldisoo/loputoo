import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("MOODLE_WS_TOKEN")
ASSIGNMENT_ID = 94922
COURSE_ID = 11380  # ← put your actual course ID here
MOODLE = "https://moodle.ut.ee"


def call(function, **params):
    params.update({
        "wstoken": TOKEN,
        "wsfunction": function,
        "moodlewsrestformat": "json",
    })
    r = requests.post(f"{MOODLE}/webservice/rest/server.php", data=params)
    return r.json()


# --- Check 1: Is save_grade enabled on the service? ---
print("=== Check 1: Required functions ===")
info = call("core_webservice_get_site_info")
function_names = {f["name"] for f in info["functions"]}

required = [
    "mod_assign_save_grade",
    "mod_assign_get_assignments",
    "mod_assign_get_submissions",
    "mod_assign_get_user_mappings",
]

for fn in required:
    status = "✓" if fn in function_names else "✗ MISSING"
    print(f"  {status}  {fn}")

# --- Check 2: What feedback plugin does the assignment use? ---
print("\n=== Check 2: Feedback plugin config ===")
result = call("mod_assign_get_assignments", **{"courseids[0]": COURSE_ID})

found = False
for course in result.get("courses", []):
    for assignment in course.get("assignments", []):
        if assignment["id"] == ASSIGNMENT_ID:
            found = True
            print(f"Assignment: {assignment['name']}")
            print(f"  Max grade: {assignment.get('grade')}")
            print(f"  Blind marking: {assignment.get('blindmarking')}")
            print(f"\n  Active feedback plugins:")
            for cfg in assignment.get("configs", []):
                if cfg["plugin"].startswith("assignfeedback") and cfg["name"] == "enabled" and cfg["value"] == "1":
                    print(f"    ✓ {cfg['plugin']}")

if not found:
    print(f"⚠ Assignment {ASSIGNMENT_ID} not found in course {COURSE_ID}")
    print("  Available assignments:")
    for course in result.get("courses", []):
        for a in course.get("assignments", []):
            print(f"    id={a['id']}: {a['name']}")