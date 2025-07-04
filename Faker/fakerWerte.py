import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("de_DE")

# Lade Patienten-IDs
patienten_df = pd.read_csv("/home/alen/PycharmProjects/PythonProject/streamlit/Faker/Patienten.csv")
patienten_ids = patienten_df["Patienten-ID"].tolist()


def generate_vitalwerte(patienten_ids, min_vals=5, max_vals=10):
    daten = []
    for pid in patienten_ids:
        anzahl = random.randint(min_vals, max_vals)
        tod = 0
        for i in range(anzahl):
            zeitpunkt = fake.date_time_between(start_date='-30d', end_date='now')

            # Normale Werte mit etwas Streuung
            blutwerte = round(random.uniform(12, 18), 1)  # Hämoglobin g/dl
            blutdruck_sys = random.randint(90, 140)
            blutdruck_dia = random.randint(60, 90)
            puls = random.randint(60, 100)
            atmung = random.randint(12, 20)
            temperatur = round(random.uniform(36.0, 37.5), 1)
            blutzucker = random.randint(70, 140)
            sturzsensor = random.choices([0, 1], weights=[0.95, 0.05])[0]  # 5% Sturz

            # Kritische Werte definieren
            alarm = 0
            if blutdruck_sys > 180 or blutdruck_dia > 110:
                alarm = 1
            if puls < 40 or puls > 130:
                alarm = 1
            if temperatur < 35.5 or temperatur > 39:
                alarm = 1
            if blutzucker < 50 or blutzucker > 300:
                alarm = 1
            if sturzsensor == 1:
                alarm = 1

            # Simuliere Tod zufällig beim letzten Messwert (z.B. 1% aller Patienten)
            if i == anzahl - 1 and random.random() < 0.01:
                tod = 1
                alarm = 1  # Tod = Notfall

            daten.append({
                "Patienten-ID": pid,
                "Zeitpunkt": zeitpunkt.strftime("%Y-%m-%d %H:%M:%S"),
                "Blutwerte (Hämoglobin)": blutwerte,
                "Blutdruck Sys": blutdruck_sys,
                "Blutdruck Dia": blutdruck_dia,
                "Puls": puls,
                "Atmung": atmung,
                "Temperatur": temperatur,
                "Blutzucker": blutzucker,
                "Sturzsensor": sturzsensor,
                "Alarm": alarm,
                "Tod": tod
            })

            if tod == 1:
                # Nach Tod keine weiteren Messungen für diesen Patienten
                break
    return daten


# Generiere Daten
vitalwerte = generate_vitalwerte(patienten_ids)

# DataFrame & speichern
vitalwerte_df = pd.DataFrame(vitalwerte)
vitalwerte_df.to_csv("/home/alen/PycharmProjects/PythonProject/streamlit/Faker/Werte.csv", index=False)

