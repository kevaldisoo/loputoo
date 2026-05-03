# Bakalaureusetöö programmid suuremahuliseks hindamiseks

Käesolev projekt on osa Karl Erik Valdsioo bakalaureusetööst "Õppeainete "Operatsioonisüsteemid" ja "Andmeturve" praktikumide hindamine tehisaru abil".
Bakalaureusetööd on võimalik lugeda Tartu Ülikooli lõputööde registrist pärast selle avaldamist, kuid enne seda on see repositoorium mõeldud juhendajale ja restsenseerijatele.
Projekt automatiseerib üliõpilaste eksamitööde hindamise, kasutades mitut tehisintellekti mudelit, ning sisestab tulemused automaatselt Moodle'i õpikeskkonda.

---

## Kaustade struktuur

```
loputoo/
├── hindamine/               # PDF-ide töötlemine ja AI-põhine hindamine
├── hinnete_sisestamine/     # Hinnete ettevalmistamine ja Moodle'i integratsioon
├── submissions/             # Üliõpilaste originaalülesanded Moodle'ist (PDF, CDOC, ASICE)
├── opilaste_tood/           # Eraldatud PDF-failid (organiseeritud esituse ID järgi)
├── tulemused/               # Hindamistulemused (JSON ja Excel)
├── requirements.txt         # Pythoni sõltuvused
└── .env                     # Keskkonnamuutujad (API võtmed)
```

---

## Kaustade kirjeldus

### `hindamine/`
Sisaldab üliõpilaste PDF-tööde tekstiks teisendamise ja AI-hindamise skripte.

| Fail              | Kirjeldus                                                                                                        |
|-------------------|------------------------------------------------------------------------------------------------------------------|
| `pdf_json.py`     | Eraldab PDF-failidest üliõpilaste vastused ja salvestab need `tulemused/test.json` faili                         |
| `api_requests.py` | Saadab vastused mitmele AI mudelile (GPT, Gemini, Claude) hindamiseks ja salvestab tulemused `tulemused/` kausta |
| `json_excel.py`   | Koondab kõigi mudelite tulemused ühtsesse Exceli faili (`tulemused/koondtabel.xlsx`)                             |

### `hinnete_sisestamine/`
Sisaldab hinnete võrdlemise, teisendamise ja Moodle'i sisestamise abiskripte.

| Fail                   | Kirjeldus                                                                                |
|------------------------|------------------------------------------------------------------------------------------|
| `compare_results.py`   | Võrdleb eri mudelite hindeid ja valib parima tulemuse (`tulemused/tulemused_parim.json`) |
| `userid_get_map.py`    | Hangib Moodle'i API kaudu esituste ID-de ja kasutaja ID-de vastenduse                    |
| `changing_id.py`       | Asendab tulemuste failides esituste ID-d Moodle'i kasutaja ID-dega                       |
| `pre_flight_checks.py` | Kontrollib enne hinnete sisestamist, et Moodle'i API oleks õigesti seadistatud           |

### `submissions/`
Moodle'ist allalaaditud üliõpilaste originaalsed ülesandefailid (143+ alamkausta, üks iga üliõpilase kohta).

### `opilaste_tood/`
`pdf_json.py` poolt eraldatud ja organiseeritud PDF-failid — üks fail üliõpilase kohta.

### `tulemused/`
Kõik hindamistulemused:

| Fail                       | Kirjeldus                                                      |
|----------------------------|----------------------------------------------------------------|
| `test.json`                | Üliõpilaste vastused (sisend AI hindamisele)                   |
| `tulemused_gpt52.json`     | GPT-5.2 hindamistulemused                                      |
| `tulemused_gpt51.json`     | GPT-5.1 hindamistulemused                                      |
| `tulemused_gemini.json`    | Gemini 3.1 Pro hindamistulemused                               |
| `tulemused_sonnet.json`    | Claude Sonnet hindamistulemused                                |
| `tulemused_parim.json`     | Parimad koondtulemused kõigist mudelitest                      |
| `koondtabel.xlsx`          | Kõigi mudelite tulemuste võrdlustabel Excelis (ainult puntkid) |
| `koondtabel_pohjalik.xlsx` | Kõigi mudelite tulemuste võrdlustabel Excelis                  |


---

## Eeltingimused

### 1. Pythoni paigaldamine
Veendu, et arvutis on paigaldatud Python 3.9 või uuem versioon.

### 2. Sõltuvuste paigaldamine
Ava terminal projekti kaustas ja käivita:

```bash
pip install -r requirements.txt
```

### 3. Keskkonna seadistamine
Loo projekti juurkausta `.env` fail järgmise sisuga:

```env
MOODLE_WS_TOKEN=sinu_moodle_api_token
OPENROUTER_API_KEY=sinu_openrouter_api_võti
```

## Tööpõhimõte (samm-sammult)

```
1. PDF-ide eraldamine  →  2. AI hindamine  →  3. Tulemuste võrdlus
       ↓                        ↓                      ↓
  pdf_json.py            api_requests.py         compare_results.py
                                                        ↓
6. Hinnete sisestamine  ←  5. ID-de teisendamine  ←  4. ID-de hankimine
   hinnete_sisestamine.py    changing_id.py          userid_get_map.py
```

---

## Programmide käivitamine

Kõiki skripte tuleb käivitada **projekti juurkaustas** (`loputoo/`).

### Samm 1 — PDF-idest vastuste eraldamine

Eraldab küsimuse 9.4 vastused kõigist PDF-failidest ja loob `tulemused/test.json`.

```bash
python hindamine/pdf_json.py
```

### Samm 2 — AI-põhine hindamine

Hindab üliõpilaste vastused nelja erineva AI mudeliga ja salvestab tulemused `tulemused/` kausta.

```bash
python hindamine/api_requests.py
```

### Samm 3 — Exceli koondtabeli loomine

Koondab kõigi mudelite tulemused ühte Exceli faili (`tulemused/koondtabel.xlsx`).

```bash
python hindamine/json_excel.py
```

### Samm 4 — Parimate tulemuste valimine

Võrdleb mudelite tulemusi ja salvestab parima hinde iga üliõpilase kohta.

```bash
python hinnete_sisestamine/compare_results.py
```

### Samm 5 — Moodle'i kasutaja ID-de hankimine

Hangib Moodle'i API kaudu esituste ja kasutajate ID-de vastenduse.

```bash
python hinnete_sisestamine/userid_get_map.py
```

### Samm 6 — ID-de teisendamine

Asendab tulemuste failis esituste ID-d Moodle'i kasutaja ID-dega.

```bash
python hinnete_sisestamine/changing_id.py
```

### Samm 7 — Moodle'i API kontrollimine (valikuline)

Kontrollitakse, et kõik vajalikud Moodle'i API funktsioonid on lubatud.

```bash
python hinnete_sisestamine/pre_flight_checks.py
```

### Samm 8 — Hinnete automaatne sisestamine Moodle'i

DRY_RUN muutuja maha võtmisel sisestatakse tulemused_by_userid.json failis olevad tulemused valitud Moodle kursusele.

```bash
python hinnete_sisestamine/hinnete_sisestamine.py
```

---

## Hindamissüsteem

Iga üliõpilase töö hinnatakse **4 alamküsimuse** alusel, igaüks on väärt **0,25 punkti** (kokku **1,0 punkti**).

Tulemuse JSON-formaat:

```json
{
  "opilane": "üliõpilase_id",
  "punktid": 1.0,
  "alamylesanded": {
    "kysimus_1": { "punktid": 0.25, "pohjendus": "põhjendus" },
    "kysimus_2": { "punktid": 0.25, "pohjendus": "põhjendus" },
    "kysimus_3": { "punktid": 0.25, "pohjendus": "põhjendus" },
    "kysimus_4": { "punktid": 0.25,  "pohjendus": "põhjendus" }
  },
  "tagasiside": "Üldine tagasiside eesti keeles.",
  "ai_toenaosus_protsent": 0,
  "ai_pohjendus": "Põhjendus AI tõenäosuse hindele"
}
```

---

## Kasutatavad AI mudelid

| Mudel | Faili nimi |
|-------|-----------|
| GPT-5.2 | `tulemused_gpt52.json` |
| GPT-5.1 | `tulemused_gpt51.json` |
| Gemini 3.1 Pro | `tulemused_gemini.json` |
| Claude Sonnet | `tulemused_sonnet.json` |

Mudelitele pääseb ligi [OpenRouter](https://openrouter.ai) API kaudu.
