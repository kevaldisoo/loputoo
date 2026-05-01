import time

from openrouter import OpenRouter
from dotenv import load_dotenv
load_dotenv()
import os
import json

with open("../tulemused/test.json", "r", encoding="utf-8") as f:
    opilased = json.load(f)

vastuse_formaat = '''{
  "opilane": "Nimi",
  "punktid": 1.0,
  "alamylesanded": {
    "kysimus_1": {"punktid": 0.25, "pohjendus": "Vead"},
    "kysimus_2": {"punktid": 0.25, "pohjendus": "Vead"},
    "kysimus_3": {"punktid": 0.25, "pohjendus": "Vead"},
    "kysimus_4": {"punktid": 0.25, "pohjendus": "Vead"}
  },
  "tagasiside": "Üldine tagasiside õpilasele",
  "ai_toenaosus_protsent": 0,
  "ai_pohjendus": "Ühe lauseline põhjendus"
}'''

models = {
    "openai/gpt-5.2": "tulemused_gpt52.json",
    "openai/gpt-5.1": "tulemused_gpt51.json",
    "google/gemini-3.1-pro-preview": "tulemused_gemini.json",
    "anthropic/claude-sonnet-4.5": "tulemused_sonnet.json"
}

MIN_CONTENT_LENGTH = 50  # submissions shorter than this are considered empty

tyhjad_hinded = []
hinnatud_opilased = {}

for name, content in opilased.items():
    content_str = json.dumps(content, ensure_ascii=False)
    if len(content_str) < MIN_CONTENT_LENGTH:
        tyhjad_hinded.append({
            "opilane": name,
            "punktid": 0,
            "alamylesanded": {
                "kysimus_1": {"punktid": 0, "pohjendus": "Vastus puudub"},
                "kysimus_2": {"punktid": 0, "pohjendus": "Vastus puudub"},
                "kysimus_3": {"punktid": 0, "pohjendus": "Vastus puudub"},
                "kysimus_4": {"punktid": 0, "pohjendus": "Vastus puudub"}
            },
            "tagasiside": "Vastus puudub või on liiga lühike hindamiseks",
            "ai_toenaosus_protsent": 0,
            "ai_pohjendus": "Vastust ei esitatud"
        })
        print(f"Tühi vastus, automaatne 0p: {name}")
    else:
        hinnatud_opilased[name] = content

print(f"\nKokku: {len(opilased)} õpilast")
print(f"Tühjad (automaatne 0p): {len(tyhjad_hinded)}")
print(f"Hindamisele läheb: {len(hinnatud_opilased)}\n")

BATCH_SIZE = 25
total = len(opilased)
opilane_items = list(hinnatud_opilased.items())
batches = [dict(opilane_items[i:i + BATCH_SIZE]) for i in range(0, len(opilane_items), BATCH_SIZE)]

PROMPT_PREFIX = """Sa pead hindama õpilaste töid e-valimiste kohta. Õpilane peab vastama nendele neljale küsimusele:
            1. Kirjeldage võimalikult detailselt ja tehniliselt kuidas on tagatud hääle salajasus (kelle poolt sa hääletasid). 2. Oma antud häält on võimalik kontrollida nutiseadmes. Kuidas on tagatud, et nutiseadmega oma hääle kontrollimine ei avalikusta sinu häält?
            3. 2025 aasta KOV valimised on esimesed, kus hääletamiseks saab kasutada lisaks ID-kaartile ja Mobiili ID-le ka Smart-ID tarkvara isiku tuvastamiseks ja hääle valiku kinnitamiseks. Millised muudatused seadusandluses ja Smart-ID turvalisuses võimaldavad nüüd ka Smart-ID abil e-hääletada? Vastake võimalikult konkreetselt ja tehniliselt.
            4. Pärast e-valimiste tehnilise seletusega tutvumist milline on teie arvamus Kas e-hääletamine on ebaturvalisem, sama turvaline või turvalisem võrreldes valimiskasti juures paberhääletamisega? Palun põhjendage enda vastust ning tooge välja võimalikud ründekohad (probleemid turvalisusega), miks teie arvates üks või teine valimise vorm on turvalisem/ebaturvalisem.
            Vastus võiks sisaldada mõisteid ümbrik, valimiskast, krüpteerimine, räsi, avalik võti, salajane võti, valimiste server, hääletaja arvuti, nutiseade, Smart-ID jne. Eeldatav maht iga küsimuse kohta on ~1 lõik teksti ja koguvastus umbes üks A4 lehekülg pikkune arutelu e-valimiste turvalisuse teemal (võib olla rohkem).
            Arvesta, et tegu on 1. aasta üliõpilastega ning peamine on veenduda, kas õpilane on teemast aru saanud.
            Seal on üldiselt välja toodud küsimuse number, millele on konkreetne õpilane vastanud, kuid on ka mõningaid erandeid. Kui õpilase juures on teksti, mis pole küsimustega seotud, siis ignoreeri seda. Juhul, kui vastust pole, anna õpilasele 0 punkti. Arvesta igat json faili pealkirja kui eraldi õpilast ning hinda neid eraldi.
            Anna hinnang, mitu punkti peaks õpilane oma vastuse eest saama, kui maksimaalselt on võimalik õpilasel saada 1 punkt ning iga alampunkti vastuse väärtus on võrdne (maksimaalselt 0,25 punkti). Hindamine pole binaarne. Põhjenda oma vastust ühe lausega (too välja puudusi, kui on).
            Samuti lisa lõpus AI teksti tõenäosuse protsent ning põhjenda lausega, miks sa sellise protsendi andisid.
            OLULINE: Iga õpilase "opilane" väli peab olema TÄPSELT sama kui JSON sisendi võti (nt "3084201.pdf"). Ära muuda nimesid. Iga õpilase kohta TÄPSELT üks hinnang — ära jäta kedagi vahele ja ära lisa ühtegi lisaõpilast. """

PROMPT_SUFFIX = "\n            Vasta AINULT JSON formaadis, ilma lisatekstita. Formaat: " + vastuse_formaat

def validate_grades(hinded, nimed):
    kontrollitud = []
    nähtud = set()
    oodatud_set = set(nimed)
    for hinne in hinded:
        nimi = hinne.get("opilane", "")
        if nimi in nähtud:
            print(f" Kordus eemaldatud: {nimi}")
            continue
        if nimi not in oodatud_set:
            print(f" Tundmatu õpilane eemaldatud: {nimi}")
            continue
        nähtud.add(nimi)
        kontrollitud.append(hinne)

    kadunud = oodatud_set - nähtud
    if kadunud:
        print(f"  Puuduvad hinded ({len(kadunud)}): {', '.join(sorted(kadunud))}")

    return kontrollitud, kadunud

with OpenRouter(
    api_key=os.getenv("OPENROUTER_API_KEY")
) as client:
    for model, filename in models.items():
        print(f"\n{'=' * 50}")
        print(f"Mudel: {model}")
        print(f"{'=' * 50}")

        koik_hinded = list(tyhjad_hinded)

        for batch_num, batch in enumerate(batches, 1):
            batch_nimed = list(batch.keys())
            batch_suurus = len(batch)
            print(f"\nPartii {batch_num}/{len(batches)} ({batch_suurus} õpilast)...")

            ylejaanud_nimed = list(batch.keys())
            ylejaanud_batch = dict(batch)
            batch_hinded = []

            for attempt in range(5):
                if not ylejaanud_nimed:
                    break

                nimed_list = ", ".join(ylejaanud_nimed)
                batch_json = json.dumps(ylejaanud_batch, ensure_ascii=False, separators=(",", ":"))
                prompt = (
                        PROMPT_PREFIX
                        + f"\n            Selles partiis on TÄPSELT {len(ylejaanud_nimed)} õpilast: {nimed_list}\n"
                        + "\n            Õpilaste vastused: " + batch_json
                        + PROMPT_SUFFIX
                )

                try:
                    response = client.chat.send(
                        model=model,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    vastus_text = response.choices[0].message.content.strip()
                    if vastus_text.startswith("```"):
                        vastus_text = vastus_text.split("\n", 1)[1]
                        vastus_text = vastus_text.rsplit("```", 1)[0]

                    output = json.loads(vastus_text)
                    hinded = output if isinstance(output, list) else output.get("hindamine", [])

                    hinnatud, kadunud = validate_grades(hinded, ylejaanud_nimed)
                    batch_hinded.extend(hinnatud)

                    if kadunud:
                        print(f"  {len(kadunud)} puudu, proovin ainult neid uuesti...")
                        ylejaanud_nimed = list(kadunud)
                        ylejaanud_batch = {k: v for k, v in batch.items() if k in kadunud}
                        time.sleep(10)
                        continue
                    else:
                        break

                except json.JSONDecodeError:
                    print(f"JSON parse error partiis {batch_num}, salvestatakse toorvastus")
                    with open(f"{filename}.batch{batch_num}.raw", "w", encoding="utf-8") as f:
                        json.dump({"mudel": model, "partii": batch_num, "raw": vastus_text}, f, ensure_ascii=False,
                                  indent=2)
                    break
                except Exception as e:
                    wait = 30 * (attempt + 1)
                    print(f"Error: {e}. Waiting {wait}s... (attempt {attempt + 1})")
                    time.sleep(wait)

            print(f"Valmis! Hinnatud {len(batch_hinded)}/{batch_suurus} õpilast")
            koik_hinded.extend(batch_hinded)

            with open(filename, "w", encoding="utf-8") as f:
                json.dump({"hindamine": koik_hinded}, f, ensure_ascii=False, indent=2)
            print(f"Salvestatud: {filename} ({len(koik_hinded)} kokku)")

            max_pts = sum(1 for t in batch_hinded if t.get("punktid") == 1)
            print(f"Maksimum punktid selles partiis: {max_pts}/{len(batch_hinded)}")

            time.sleep(5)

        hinnatud_nimed = {h.get("opilane") for h in koik_hinded}
        koik_nimed = set(opilased.keys())
        ikka_kadunud = koik_nimed - hinnatud_nimed
        print(f"\nMudel {model} valmis. Kokku hinnatud: {len(koik_hinded)}/{total}")
        if ikka_kadunud:
            print(f"PUUDUVAD HINDED: {', '.join(sorted(ikka_kadunud))}")
        else:
            print("Kõik õpilased hinnatud!")

print(f"\n{'='*50}")
print("Kõik mudelid valmis!")
print(f"Failid: {', '.join(models.values())}")
