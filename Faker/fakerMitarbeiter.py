import pandas as pd
from faker import Faker
import random

fake = Faker('de_DE')
Faker.seed(42)
random.seed(42)

# Listen für Abteilungen und Schichten
abteilungen = ['Pflege', 'Verwaltung', 'Medizinischer Dienst', 'Hauswirtschaft']

def generate_mitarbeiter(n):
    mitarbeiter = []
    for i in range(n):
        mitarbeiter_id = f"M{str(i+1).zfill(4)}"
        abteilung = random.choice(abteilungen)
        vorname = fake.first_name()
        nachname = fake.last_name()
        strasse = fake.street_name() + ' ' + str(random.randint(1, 100))
        plz = fake.postcode()
        ort = fake.city()
        telefon = fake.phone_number()
        email = fake.email()
        rolle = "Mitarbeiter"

        mitarbeiter.append({
            "Mitarbeiter-ID": mitarbeiter_id,
            "Abteilung": abteilung,
            "Nachname": nachname,
            "Vorname": vorname,
            "Straße + Hnr": strasse,
            "PLZ": plz,
            "Wohnort": ort,
            "Telefon": telefon,
            "E-Mail": email,
            "Rolle": rolle
        })
    return mitarbeiter

# Erzeuge 100 Mitarbeiterdatensätze
mitarbeiter_df = pd.DataFrame(generate_mitarbeiter(100))

# Speichern als CSV
mitarbeiter_csv_path = "/streamlit/Faker/Mitarbeiter.csv"
mitarbeiter_df.to_csv(mitarbeiter_csv_path, index=False)


