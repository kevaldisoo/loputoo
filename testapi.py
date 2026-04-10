import time

from openrouter import OpenRouter
from dotenv import load_dotenv
load_dotenv()
import os
import json

with open("test.json", "r", encoding="utf-8") as f:
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

opilased_json = json.dumps(opilased, ensure_ascii=False, separators=(",", ":"))
total = len(opilased)

prompt = f"""Sa pead hindama õpilaste töid e-valimiste kohta. Õpilane peab vastama nendele neljale küsimusele:
            1. Kirjeldage võimalikult detailselt ja tehniliselt kuidas on tagatud hääle salajasus (kelle poolt sa hääletasid). 2. Oma antud häält on võimalik kontrollida nutiseadmes. Kuidas on tagatud, et nutiseadmega oma hääle kontrollimine ei avalikusta sinu häält?
            3. 2025 aasta KOV valimised on esimesed, kus hääletamiseks saab kasutada lisaks ID-kaartile ja Mobiili ID-le ka Smart-ID tarkvara isiku tuvastamiseks ja hääle valiku kinnitamiseks. Millised muudatused seadusandluses ja Smart-ID turvalisuses võimaldavad nüüd ka Smart-ID abil e-hääletada? Vastake võimalikult konkreetselt ja tehniliselt.
            4. Pärast e-valimiste tehnilise seletusega tutvumist milline on teie arvamus Kas e-hääletamine on ebaturvalisem, sama turvaline või turvalisem võrreldes valimiskasti juures paberhääletamisega? Palun põhjendage enda vastust ning tooge välja võimalikud ründekohad (probleemid turvalisusega), miks teie arvates üks või teine valimise vorm on turvalisem/ebaturvalisem.
            Vastus võiks sisaldada mõisteid ümbrik, valimiskast, krüpteerimine, räsi, avalik võti, salajane võti, valimiste server, hääletaja arvuti, nutiseade, Smart-ID jne. Eeldatav maht iga küsimuse kohta on ~1 lõik teksti ja koguvastus umbes üks A4 lehekülg pikkune arutelu e-valimiste turvalisuse teemal (võib olla rohkem).
            Arvesta, et tegu on 1. aasta üliõpilastega ning peamine on veenduda, kas õpilane on teemast aru saanud.
            Seal on üldiselt välja toodud küsimuse number, millele on konkreetne õpilane vastanud, kuid on ka mõningaid erandeid. Kui õpilase juures on teksti, mis pole küsimustega seotud, siis ignoreeri seda. Juhul, kui vastust pole, anna õpilasele 0 punkti. Arvesta igat json faili pealkirja kui eraldi õpilast ning hinda neid eraldi. 
            Anna hinnang, mitu punkti peaks õpilane oma vastuse eest saama, kui maksimaalselt on võimalik õpilasel saada 1 punkt ning iga alampunkti vastuse väärtus on võrdne (maksimaalselt 0,25 punkti). Hindamine pole binaarne. Põhjenda oma vastust ühe lausega (too välja puudusi, kui on). 
            Samuti lisa lõpus AI teksti tõenäosuse protsent ning põhjenda lausega, miks sa sellise protsendi andisid.
            Õpilaste vastused: {opilased_json}
            Vasta AINULT JSON formaadis, ilma lisatekstita. Hinda KÕIKI õpilasi. Formaat: {vastuse_formaat} """

with OpenRouter(
    api_key=os.getenv("OPENROUTER_API_KEY")
) as client:
    for model, filename in models.items():
        print(f"\n{'=' * 50}")
        print(f"Mudel: {model}")
        print(f"{'=' * 50}")
        print(f"Saadan {total} õpilast korraga hindamisele...")
        for attempt in range(5):
            try:
                response = client.chat.send(
                    model=model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                vastus_text = response.choices[0].message.content.strip()
                if vastus_text.startswith("```"):
                    vastus_text = vastus_text.split("\n", 1)[1]
                    vastus_text = vastus_text.rsplit("```", 1)[0]

                output = json.loads(vastus_text)

                if isinstance(output, list):
                    output = {"hindamine": output}

                hinnatud = len(output.get("hindamine", []))
                print(f"Valmis! Hinnatud {hinnatud}/{total} õpilast")

                if hinnatud < total:
                    print(f"HOIATUS: {total - hinnatud} õpilast jäi hindamata!")

                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(output, f, ensure_ascii=False, indent=2)
                print(f"Salvestatud: {filename}")

                if "hindamine" in output:
                    max_pts = sum(1 for t in output["hindamine"] if t.get("punktid") == 1)
                    print(f"Maksimum punktid: {max_pts}/{hinnatud}")
                break
            except json.JSONDecodeError:
                print(f"JSON parse error, saving raw response")
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump({"mudel": model, "raw": vastus_text}, f, ensure_ascii=False, indent=2)
                print(f"Salvestatud (raw): {filename}")
                break
            except Exception as e:
                wait = 30 * (attempt + 1)
                print(f"Error: {e}. Waiting {wait}s... (attempt {attempt + 1})")
                time.sleep(wait)

        time.sleep(5)

print(f"\n{'='*50}")
print("Kõik mudelid valmis!")
print(f"Failid: {', '.join(models.values())}")
