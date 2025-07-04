import pandas as pd
from faker import Faker
import random

fake = Faker('de_DE')
Faker.seed(42)
random.seed(42)


# Beispielhafte Beziehungen und Kontaktarten
# Lade Patientendaten
patienten_df = pd.read_csv("/home/alen/PycharmProjects/PythonProject/streamlit/Faker/Patienten.csv")
patient_ids = patienten_df["Patienten-ID"].tolist()
patient_namen = patienten_df[["Patienten-ID", "Nachname", "Vorname"]]

beziehungen = ['Ehepartner', 'Kind', 'Enkel', 'Freund', 'Nachbar', 'Geschwister']
kontaktarten = ['Telefon', 'Besuch', 'Brief', 'Videocall', 'E-Mail']

# Angehörige generieren
def generate_angehoerige(n):
    angehoerige = []
    for i in range(1, n + 1):
        angehoerige_id = f"A{str(i).zfill(4)}"
        vorname = fake.first_name()
        nachname = fake.last_name()
        strasse = fake.street_name() + ' ' + str(random.randint(1, 100))
        plz = fake.postcode()
        ort = fake.city()
        patient = random.choice(patient_namen.values.tolist())
        patienten_id = patient[0]
        patient_name = f"{patient[1]} {patient[2]}"
        telefon = fake.phone_number()
        email = fake.email()
        beziehung = random.choice(beziehungen)
        letzter_kontakt = fake.date_between(start_date='-6M', end_date='today').strftime("%Y-%m-%d")
        kontaktart = random.choice(kontaktarten)
        notizen = fake.sentence(nb_words=6)
        rolle = "Angehöriger"

        angehoerige.append({
            "Angehörige-ID": angehoerige_id,
            "Nachname": nachname,
            "Vorname": vorname,
            "Straße + Hnr": strasse,
            "PLZ": plz,
            "Wohnort": ort,
            "zugehöriger Patient": patient_name,
            "Patienten-Nr": patienten_id,
            "Telefon": telefon,
            "E-Mail": email,
            "Beziehung zum Patienten": beziehung,
            "letzter Kontakt": letzter_kontakt,
            "Art des Kontaktes": kontaktart,
            "Notizen": notizen,
            "Rolle": rolle
        })
    return angehoerige


# Erzeuge 300 Angehörige
angehoerige_df = pd.DataFrame(generate_angehoerige(300))

# Speichern als CSV
angehoerige_csv_path = "/streamlit/Angehoerige.csv"
angehoerige_df.to_csv(angehoerige_csv_path, index=False)

