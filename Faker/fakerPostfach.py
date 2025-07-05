import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Faker für Nachrichtentexte und Zeitstempel
fake = Faker("de_DE")

# 1. Mitarbeiter laden
df_mitarbeiter = pd.read_csv("/home/alen/PycharmProjects/PythonProject/streamlit/Faker/Mitarbeiter.csv")

# 2. Nachrichtendaten generieren
nachrichten = []

# Jeder MA soll 3 Nachrichten bekommen
for _, empfänger in df_mitarbeiter.iterrows():
    empfänger_id = empfänger['Mitarbeiter-ID']
    empfänger_vorname = empfänger['Vorname']
    empfänger_nachname = empfänger['Nachname']

    for _ in range(3):
        # Zufälligen Absender auswählen, aber nicht sich selbst
        absender = empfänger
        while absender['Mitarbeiter-ID'] == empfänger_id:
            absender = df_mitarbeiter.sample(1).iloc[0]

        # Zufälliges Datum & Uhrzeit in den letzten 30 Tagen
        datum_uhrzeit = fake.date_time_between(start_date="-30d", end_date="now")

        # Nachricht generieren
        nachricht_text = fake.sentence(nb_words=random.randint(5, 12))

        nachrichten.append({
            "Datum": datum_uhrzeit.date(),
            "Uhrzeit": datum_uhrzeit.time().strftime("%H:%M:%S"),
            "Von_ID": absender['Mitarbeiter-ID'],
            "Von_Vorname": absender['Vorname'],
            "Von_Nachname": absender['Nachname'],
            "An_ID": empfänger_id,
            "An_Vorname": empfänger_vorname,
            "An_Nachname": empfänger_nachname,
            "Nachricht": nachricht_text
        })

# 3. Als CSV speichern
df_postfach = pd.DataFrame(nachrichten)
df_postfach.to_csv("/home/alen/PycharmProjects/PythonProject/streamlit/Faker/Postfach.csv", index=False, encoding="utf-8")

print("✅ Nachrichten erfolgreich generiert und in Postfach.csv gespeichert.")
