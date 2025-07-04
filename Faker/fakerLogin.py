import pandas as pd
import random
from faker import Faker

fake = Faker("de_DE")

base_path = "/home/alen/PycharmProjects/PythonProject/streamlit/Faker/"

abteilungen = ["Pflege", "Verwaltung", "Therapie", "Reinigung", "Küche"]

def create_email(vorname, nachname):
    email = f"{vorname}.{nachname}@beispiel.com".lower()
    email = email.replace(" ", "").replace("ß", "ss")
    return email

def create_password(length=8):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(chars) for _ in range(length))

def process_angehoerige():
    df = pd.read_csv(base_path + "Angehoerige.csv")
    records = []
    for _, row in df.iterrows():
        vorname = row["Vorname"]
        nachname = row["Nachname"]
        user_id = row["Angehörige-ID"]
        email = create_email(vorname, nachname)
        pw = create_password()
        records.append({
            "ID": user_id,
            "Login-Email": email,
            "Login-Passwort": pw,
            "Rolle": "Angehöriger",
            "Abteilung": ""
        })
    return records

def process_patienten():
    df = pd.read_csv(base_path + "Patienten.csv")
    records = []
    for _, row in df.iterrows():
        vorname = row["Vorname"]
        nachname = row["Nachname"]
        user_id = row["Patienten-ID"]
        email = create_email(vorname, nachname)
        pw = create_password()
        records.append({
            "ID": user_id,
            "Login-Email": email,
            "Login-Passwort": pw,
            "Rolle": "Patient",
            "Abteilung": ""
        })
    return records

def process_mitarbeiter():
    df = pd.read_csv(base_path + "Mitarbeiter.csv")
    records = []
    for _, row in df.iterrows():
        vorname = row["Vorname"]
        nachname = row["Nachname"]
        user_id = row["Mitarbeiter-ID"]
        email = create_email(vorname, nachname)
        pw = create_password()
        abteilung = row.get("Abteilung", "")
        records.append({
            "ID": user_id,
            "Login-Email": email,
            "Login-Passwort": pw,
            "Rolle": "Mitarbeiter",
            "Abteilung": abteilung
        })
    return records

# Alle User zusammenführen
angehoerige = process_angehoerige()
patienten = process_patienten()
mitarbeiter = process_mitarbeiter()

alle_user = angehoerige + patienten + mitarbeiter

df_users = pd.DataFrame(alle_user)

# Speichern
df_users.to_csv(base_path + "Login.csv", index=False)

