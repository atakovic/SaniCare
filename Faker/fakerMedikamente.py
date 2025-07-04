import pandas as pd
from faker import Faker
import random

fake = Faker('de_DE')
Faker.seed(42)
random.seed(42)


# Listen für Darreichungsformen und Anwendungsgebiete
darreichungsformen = ['Tablette', 'Kapsel', 'Lösung', 'Injektion', 'Salbe', 'Tropfen']
anwendungsgebiete = [
    'Bluthochdruck', 'Diabetes', 'Schmerzen', 'Entzündungen', 'Demenz', 'Herz-Kreislauf',
    'Parkinson', 'Asthma', 'Infektionen', 'Schlafstörungen', 'Depression', 'Magenprobleme'
]

def generate_medikamente(n):
    medikamente = []
    for i in range(n):
        medikament_id = f"MED{str(i+1).zfill(4)}"
        name = fake.unique.lexify(text="Medika????")
        hersteller = fake.company()
        dosierung = random.choice([50, 100, 250, 500, 750, 1000])
        einheit = random.choice(['mg', 'ml'])
        darreichung = random.choice(darreichungsformen)
        anwendungsgebiet = random.choice(anwendungsgebiete)
        verordner = fake.name()
        beginn = fake.date_between(start_date='-2y', end_date='-1d')
        ende = fake.date_between(start_date=beginn, end_date='+6M')

        medikamente.append({
            "Medikament-ID": medikament_id,
            "Name": name,
            "Hersteller": hersteller,
            "Dosierung": dosierung,
            "Einheit": einheit,
            "Darreichungsform": darreichung,
            "Anwendungsgebiet": anwendungsgebiet,
            "Verordner": verordner,
            "Beginn Verordnung": beginn,
            "Ende Verordnung": ende
        })
    return medikamente

# Erzeuge 200 Medikamente
medikamente_df = pd.DataFrame(generate_medikamente(200))

# Speichern als CSV
medikamente_csv_path = "/streamlit/Medikamente.csv"
medikamente_df.to_csv(medikamente_csv_path, index=False)

