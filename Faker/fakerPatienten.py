import pandas as pd
from faker import Faker
import random

fake = Faker('de_DE')
Faker.seed(42)
random.seed(42)

# Beispielhafte Listen für Krankheiten und Medikamente
krankheiten = ['Diabetes Typ 2', 'Bluthochdruck', 'Demenz', 'Arthrose', 'Herzinsuffizienz', 'Parkinson', 'Asthma']
medikamente = ['Metformin', 'Ramipril', 'Aspirin', 'Ibuprofen', 'Insulin', 'Donepezil', 'Furosemid']

pflegearten = ['stationär', 'zu Hause']
heime = ['H001', 'H002', 'H003']

def generate_patienten(n):
    patienten = []
    for i in range(n):
        patient_id = f"P{str(i+1).zfill(4)}"
        vorname = fake.first_name()
        nachname = fake.last_name()
        strasse = fake.street_name() + ' ' + str(random.randint(1, 100))
        plz = fake.postcode()
        ort = fake.city()
        angehoerige = fake.name()
        telefon = fake.phone_number()
        email = fake.email()
        krankheit = ', '.join(random.sample(krankheiten, random.randint(1, 3)))
        medikamentenliste = random.sample(medikamente, random.randint(1, 3))
        medikamente_str = ', '.join(medikamentenliste)
        tagesdosis = ', '.join([f"{med} ({random.randint(1,3)}x täglich)" for med in medikamentenliste])
        aktueller_pfleger = fake.name()
        pflegeart = random.choice(pflegearten)
        tagebuch_id = f"T{str(i+1).zfill(4)}"
        heim_id = random.choice(heime)
        zimmernummer = str(random.randint(100, 500))
        hinweise = fake.sentence(nb_words=6)
        rolle = "Patient"

        patienten.append({
            "Patienten-ID": patient_id,
            "Nachname": nachname,
            "Vorname": vorname,
            "Straße + Hnr": strasse,
            "PLZ": plz,
            "Wohnort": ort,
            "Angehörige": angehoerige,
            "Telefon": telefon,
            "E-Mail": email,
            "Krankheiten": krankheit,
            "Medikamente": medikamente_str,
            "Tagesdosis": tagesdosis,
            "aktueller Pfleger": aktueller_pfleger,
            "Pflegeart": pflegeart,
            "Tagebuch-ID": tagebuch_id,
            "Heim-ID": heim_id,
            "Zimmernummer": zimmernummer,
            "Hinweise": hinweise,
            "Rolle": rolle
        })
    return patienten

# Erzeuge 1000 Patientendatensätze
patienten_df = pd.DataFrame(generate_patienten(1000))

# Speichern als CSV
csv_path = "/home/alen/PycharmProjects/PythonProject/streamlit/Faker/Patienten.csv"
patienten_df.to_csv(csv_path, index=False)