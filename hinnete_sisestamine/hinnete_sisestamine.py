import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# --- Config ---
TOKEN = os.getenv("MOODLE_WS_TOKEN")
ASSIGNMENT_ID = 94922
GRADING_FILE = "tulemused_by_userid.json"
COMMON_MESSAGE = """
<p>Tegu on tehisaru poolt hinnatud ülesande 9-4 tulemused.</p> 
<p>Juhul, kui soovid hinnet vaidlustada, võta ühendust aine korraldajatega.</p>
<p>Kui Sinu esitust on enne siia hinde ilmumist hinnatud, jääb jõusse inimese antud hinne.</p>
"""

MAX_GRADE = 1.0

DRY_RUN = True  # ← set to False to actually push grades


def call(function, **params):
    params.update({
        "wstoken": TOKEN,
        "wsfunction": function,
        "moodlewsrestformat": "json",
    })
    r = requests.post(f"https://moodle.ut.ee/webservice/rest/server.php", data=params)
    return r.json()


def build_feedback_html(entry):
    parts = []

    # Overall feedback
    if entry.get("tagasiside"):
        parts.append(f"<p>{entry['tagasiside']}</p>")

    parts.append(COMMON_MESSAGE)

    return "\n".join(parts)


def grade_one(userid, grade, feedback_html):
    return call(
        "mod_assign_save_grade",
        assignmentid=ASSIGNMENT_ID,
        userid=userid,
        grade=grade,
        attemptnumber=-1,
        addattempt=0,
        workflowstate="",
        applytoall=0,
        **{
            "plugindata[assignfeedbackcomments_editor][text]": feedback_html,
            "plugindata[assignfeedbackcomments_editor][format]": 1,  # 1 = HTML
        },
    )


# --- Load grading data ---
with open(GRADING_FILE, encoding="utf-8") as f:
    data = json.load(f)

entries = data["hindamine"]
print(f"Leidsin {len(entries)} esitust hindamiseks")

# --- Sanity check: try ONE student first when DRY_RUN is False ---
if not DRY_RUN:
    confirm = input(f"⚠ DRY_RUN on välja lülitatud. LAEN ÜLES {len(entries)} HINNET MOODLESSE. NEID HINDEID TAGASI VÕTTA EI SAA. Kirjuta 'JAH' jätkamiseks: ")
    if confirm != "JAH":
        print("Hindamist ei toimu.")
        exit(0)


# --- Loop ---
successes = 0
failures = []

for i, entry in enumerate(entries, 1):
    userid = entry["opilane"]
    score = entry["punktid"] * MAX_GRADE  # scale if needed
    feedback = build_feedback_html(entry)

    if DRY_RUN:
        print(f"[{i}/{len(entries)}] DRY: userid={userid}, score={score}")
        print(f"    Tagasiside preview: {feedback[:120]}...")
        continue

    try:
        result = grade_one(userid, score, feedback)
        # mod_assign_save_grade returns null on success, error dict on failure
        if result is None or result == [] or result == "":
            successes += 1
            print(f"[{i}/{len(entries)}] ✓ userid={userid} graded")
        else:
            failures.append((userid, result))
            print(f"[{i}/{len(entries)}] ✗ userid={userid}: {result}")
    except Exception as e:
        failures.append((userid, str(e)))
        print(f"[{i}/{len(entries)}] ✗ userid={userid}: {e}")

# --- Summary ---
print(f"\n=== Valmis ===")
print(f"Õnnestumisi: {successes}")
print(f"Vigu: {len(failures)}")
if failures:
    with open("grading_failures.json", "w", encoding="utf-8") as f:
        json.dump(failures, f, ensure_ascii=False, indent=2)
    print("Vead kirjutatud faili grading_failures.json")