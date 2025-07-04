import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("de_DE")

# Pfad zum Ordner mit deinen CSVs
base_path = "/home/alen/PycharmProjects/PythonProject/streamlit/Faker/"

# CSV-Dateien laden
mitarbeiter_df = pd.read_csv(base_path + "Mitarbeiter.csv")
patienten_df = pd.read_csv(base_path + "Patienten.csv")
angehoerige_df = pd.read_csv(base_path + "Angehoerige.csv")
heime_df = pd.read_csv(base_path + "Heime.csv")

# IDs extrahieren
pfleger_ids = mitarbeiter_df["Mitarbeiter-ID"].tolist()
patienten_ids = patienten_df["Patienten-ID"].tolist()
angehoerige_ids = angehoerige_df["Angehörige-ID"].tolist()

# Heim-Namen als Veranstalter
heim_veranstalter = heime_df["Ort"].tolist()

veranstaltungsarten = ["Musiknachmittag", "Yoga-Gruppe", "Arztvortrag", "Kochkurs", "Gedächtnistraining"]
orte = ["Gemeinschaftsraum", "Außenanlage", "Mehrzweckraum", "Therapieraum", "Cafeteria"]

def generate_events(n):
    events = []
    for i in range(1, n+1):
        event_id = f"E{str(i).zfill(4)}"
        art = random.choice(veranstaltungsarten)
        titel = f"{art} mit {fake.first_name()}"
        veranstalter = random.choice(heim_veranstalter)
        mitarbeiter = random.choice(pfleger_ids)
        teilnehmer = ', '.join(random.sample(patienten_ids, 2) +
                              random.sample(angehoerige_ids, 1) +
                              random.sample(pfleger_ids, 1))
        ort = random.choice(orte)
        raum = f"Raum {random.randint(1,5)}"
        hinweise = fake.sentence(nb_words=6)
        datum = fake.date_between(start_date='today', end_date='+30d')
        beginn = fake.time(pattern="%H:%M")
        beginn_dt = datetime.strptime(f"{datum} {beginn}", "%Y-%m-%d %H:%M")
        ende_dt = beginn_dt + timedelta(hours=random.randint(1, 3))
        ende = ende_dt.strftime("%H:%M")

        events.append({
            "Veranstaltungsnummer": event_id,
            "Art der Veranstaltung": art,
            "Titel": titel,
            "Veranstalter": veranstalter,
            "zuständige Mitarbeiter": mitarbeiter,
            "Teilnehmer(Pat. ID / Ang. ID / Pfleger ID)": teilnehmer,
            "Ort der Veranstaltung": ort,
            "Raum": raum,
            "Hinweise": hinweise,
            "Datum": datum.strftime("%Y-%m-%d"),
            "Beginn": beginn,
            "Ende": ende
        })
    return events

# 5 Events erzeugen
events_df = pd.DataFrame(generate_events(5))

# CSV speichern
events_df.to_csv(base_path + "Events.csv", index=False)

