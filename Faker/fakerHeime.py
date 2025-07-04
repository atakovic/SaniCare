import pandas as pd
from faker import Faker
import random

fake = Faker('de_DE')
Faker.seed(42)
random.seed(42)

# Erzeuge 3 Heime mit zugehörigen Informationen

def generate_heime():
    heime = []
    for i in range(1, 4):
        heim_id = f"H00{i}"
        zimmernummern = [str(z) for z in range(100 + i*100, 100 + i*100 + 50)]  # z. B. 200–249
        strasse = fake.street_name() + ' ' + str(random.randint(1, 20))
        plz = fake.postcode()
        ort = fake.city()
        heimleiter = fake.name()
        telefon = fake.phone_number()
        email = fake.email()


        heime.append({
            "Heim-ID": heim_id,
            "Zimmernummer": ', '.join(zimmernummern[:300]),  # nur 10 exemplarisch
            "Straße + Hnr": strasse,
            "PLZ": plz,
            "Ort": ort,
            "Zuständiger Heimleiter:in": heimleiter,
            "Telefonnummer": telefon,
            "E-Mail-Adresse": email,
        })
    return heime

# Erzeuge Heimdaten
heime_df = pd.DataFrame(generate_heime())

# Speichern als CSV
heime_csv_path = "/streamlit/Heime.csv"
heime_df.to_csv(heime_csv_path, index=False)

