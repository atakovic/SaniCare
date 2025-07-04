import streamlit as st
import pandas as pd
import datetime
import base64
import time
from streamlit_autorefresh import st_autorefresh

# Daten laden ohne Cache, damit immer aktuell
def lade_patienten():
    df = pd.read_csv("Faker/Patienten.csv")
    df.columns = df.columns.str.strip()
    return df


def lade_werte():
    df = pd.read_csv("Faker/Werte.csv")
    df.columns = df.columns.str.strip()
    return df


def lade_heime():
    df = pd.read_csv("Faker/Heime.csv")
    df.columns = df.columns.str.strip()
    return df

def lade_mitarbeiter():
    df = pd.read_csv("Faker/Mitarbeiter.csv")
    df.columns = df.columns.str.strip()
    return df

def letzter_alarm_aktiv():
    df = pd.read_csv("Faker/Werte.csv")

    letzte_werte = df.iloc[-1]

    hgb = int(letzte_werte.get("Blutwerte (Hämoglobin)"))
    sys = int(letzte_werte.get("Blutdruck Sys"))
    dia = int(letzte_werte.get("Blutdruck Dia"))
    puls = int(letzte_werte.get("Puls"))
    atmung = int(letzte_werte.get("Atmung"))
    temperatur = float(letzte_werte.get("Temperatur"))
    bz = int(letzte_werte.get("Blutzucker"))

    st.session_state.warnungen.clear()
    pruefe("Hämoglobin", hgb, 12, 18)
    pruefe("Systolischer Blutdruck", sys, 90, 140)
    pruefe("Diastolischer Blutdruck", dia, 60, 90)
    pruefe("Puls", puls, 50, 100)
    pruefe("Atmung", atmung, 12, 20)
    pruefe("Temperatur", temperatur, 36.0, 37.5)
    pruefe("Blutzucker", bz, 70, 140)

    if not df.empty and df.iloc[-1]["Alarm"] == 1:
        return True
    return False

import datetime

def darf_popup_anzeigen():
    letzte_zeit = st.session_state.last_popup_time
    jetzt = datetime.datetime.now()
    if letzte_zeit is None:
        return True
    elif (jetzt - letzte_zeit).total_seconds() > 15:
        return True
    else:
        return False

# Daten in Session State speichern (oder laden, falls noch nicht vorhanden)
if "df_patienten" not in st.session_state:
    st.session_state.df_patienten = lade_patienten()

if "df_werte" not in st.session_state:
    st.session_state.df_werte = lade_werte()

if "df_heim" not in st.session_state:
    st.session_state.df_heim = lade_heime()


def reload_data():
    st.session_state.df_patienten = lade_patienten()
    st.session_state.df_werte = lade_werte()

# Funktion zur Anzeige der MA innerhalb des Formulars - nur Anzeige der noch verfügbaren MA und auch nur die, die zu stationär passen oder zu ambulant
def verfügbare_mitarbeiter(pflegeart, df_mitarbeiter, df_patienten):
    if pflegeart not in ["stationär", "ambulant"]:
        return []

    # 1. Mitarbeiter nach Abteilung (bei stationär)
    if pflegeart == "stationär":
        df_mitarbeiter = df_mitarbeiter[
            df_mitarbeiter["Abteilung"].isin(["Pflege", "Medizinischer Dienst"])
        ]
    elif pflegeart == "ambulant":
        df_mitarbeiter = df_mitarbeiter[
            ~df_mitarbeiter["Abteilung"].isin(["Pflege", "Medizinischer Dienst"])
        ]

    # 2. Mitarbeiter, die bereits Mischpflege machen → ausschließen
    arten = df_patienten.groupby("Mitarbeiter-ID")["Pflegeart"].nunique()
    nur_eine_Art = arten[arten <= 1].index
    df_mitarbeiter = df_mitarbeiter[df_mitarbeiter["Mitarbeiter-ID"].isin(nur_eine_Art)]

    # 3. Mitarbeiter mit < 24 Patienten
    belegung = df_patienten.groupby("Mitarbeiter-ID")["Patienten-ID"].count()
    freie_ids = belegung[belegung < 24].index
    df_mitarbeiter = df_mitarbeiter[df_mitarbeiter["Mitarbeiter-ID"].isin(freie_ids)]

    return df_mitarbeiter["Mitarbeiter-ID"].unique()


# Session State für UI-Steuerung
if "ausgewählter_patient" not in st.session_state:
    st.session_state.ausgewählter_patient = None
if "seite" not in st.session_state:
    st.session_state.seite = 0
if "modus" not in st.session_state:
    st.session_state.modus = "liste"  # liste, detail, hinzufügen
if "popup_visible" not in st.session_state:
    st.session_state.popup_visible = True
if "last_popup_time" not in st.session_state:
    st.session_state.last_popup_time = None
if "warnungen" not in st.session_state:
    st.session_state.warnungen = []

count = st_autorefresh(interval=15000, key="data_refresh")

if count > 0 or "df_patienten" not in st.session_state or "df_werte" not in st.session_state:
    reload_data()

def show_popup():
    if st.session_state.get("popup_visible", True):
        # Popup HTML (ohne Button)
        popup_html = f"""
        <div id="popup" style="
            position: fixed; 
            top: 50%; left: 50%; 
            transform: translate(-50%, -50%);
            background-color: white; 
            border: 2px solid red; 
            padding: 20px; 
            z-index: 9999;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            width: 400px;
            color: red;
            text-align: center;
        ">
            <h3>Warnung: Auffällige Werte</h3>
            <ul style="text-align: left;">
                {''.join(f'<li>{w}</li>' for w in st.session_state.warnungen)}
            </ul>
        </div>
        <div style="
            position: fixed; 
            top: 0; left: 0; 
            width: 100%; height: 100%; 
            background-color: rgba(0,0,0,0.5); 
            z-index: 9998;
        "></div>
        """
        st.markdown(popup_html, unsafe_allow_html=True)

        # Container-Layout mit CSS-Trick: Streamlit-Button exakt positionieren
        with st.container():
            st.markdown(
                """
                <style>
                div.stButton > button {
                    position: fixed;
                    top: calc(66%);
                    left: 50%;
                    transform: translate(-50%, 0);
                    z-index: 10000;
                    width: 150px;           
                    padding: 6px 12px;       
                    font-size: 14px;         
                    background-color: #f44336;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                    white-space: nowrap;
                }
                div.stButton > button:hover {
                    background-color: #d32f2f;
                }
                </style>
                """, unsafe_allow_html=True
            )

            if st.button("Warnung schließen"):
                st.session_state.popup_visible = False
                st.session_state.last_popup_time = datetime.datetime.now()
                st.rerun()

def play_alarm_sound():
    audio_file_path = "Alarm.mp3"
    with open(audio_file_path, "rb") as f:
        audio_bytes = f.read()
    b64_audio = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
        <audio autoplay loop="true">
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)


def pruefe(name, wert, min_, max_):
    if not min_ <= wert <= max_:
        st.session_state.warnungen.append(f"{name} ist auffällig: {wert} (Soll: {min_}–{max_})")


# Kopfzeile mit Suchfeld, Postfach, Abmelden
col_suche, col_postfach, col_abmelden = st.columns([3, 1, 1])
if st.session_state.modus == "liste" and st.session_state.ausgewählter_patient is None:
    with col_suche:
        suche = st.text_input("", placeholder="Nach Name suchen", label_visibility="collapsed")
else:
    suche = ""

with col_postfach:
    if st.button("Postfach", use_container_width=True):
        st.warning("Du hast auf dein Postfach gedrückt!")
with col_abmelden:
    if st.button("Abmelden", use_container_width=True):
        st.warning("Du wurdest abgemeldet.")



# „Neuen Patienten hinzufügen“-Button oben, nur im Listenmodus
if st.session_state.modus == "liste":
    if st.button("Neuen Patienten hinzufügen", use_container_width=True):
        st.session_state.modus = "hinzufügen"
        st.session_state.ausgewählter_patient = None
        st.rerun()

# Patientenliste anzeigen
if st.session_state.modus == "liste" and st.session_state.ausgewählter_patient is None:
    gefiltert = st.session_state.df_patienten
    if suche:
        suchbegriff = suche.strip().lower()
        gefiltert = gefiltert[
            gefiltert['Patienten-ID'].astype(str).str.lower().str.contains(suchbegriff, na=False) |
            gefiltert['Nachname'].astype(str).str.lower().str.contains(suchbegriff, na=False) |
            gefiltert['Vorname'].astype(str).str.lower().str.contains(suchbegriff, na=False)
            ]

    pro_seite = 25
    seitenzahl = (len(gefiltert) - 1) // pro_seite + 1
    start_idx = st.session_state.seite * pro_seite
    end_idx = start_idx + pro_seite
    seite_df = gefiltert.iloc[start_idx:end_idx]

    st.markdown("### Liste aller Patienten")

    for _, row in seite_df.iterrows():
        if st.button(f"{row['Patienten-ID']}: {row['Nachname']} {row['Vorname']}", use_container_width=True):
            st.session_state.ausgewählter_patient = row['Patienten-ID']
            st.session_state.modus = "detail"
            st.rerun()


    # Seitenliste mit max 5 Seiten + ... + letzte Seite
    def Seitenliste(aktuelle, gesamt):
        if gesamt <= 7:
            return list(range(gesamt))
        else:
            if aktuelle < 4:
                return list(range(5)) + ["..."] + [gesamt - 1]
            elif aktuelle > gesamt - 5:
                return [0, "..."] + list(range(gesamt - 5, gesamt))
            else:
                return [0, "..."] + list(range(aktuelle - 1, aktuelle + 2)) + ["..."] + [gesamt - 1]


    seiten_liste = Seitenliste(st.session_state.seite, seitenzahl)

    num_cols = max(1, len(seiten_liste)) if isinstance(seiten_liste, list) else 1
    cols = st.columns(num_cols)

    for i, val in enumerate(seiten_liste):
        if val == "...":
            cols[i].write("...")
        else:
            if cols[i].button(str(val + 1), use_container_width=True):
                st.session_state.seite = val
                st.rerun()

# Detailansicht eines Patienten
elif st.session_state.ausgewählter_patient is not None and st.session_state.modus == "detail":
    patient = st.session_state.df_patienten[
        st.session_state.df_patienten['Patienten-ID'] == st.session_state.ausgewählter_patient].iloc[0]

    st.markdown("### Patientendaten")
    st.write(f"**Patienten-ID**: {patient['Patienten-ID']}")
    st.write(f"**Name**: {patient['Nachname']} {patient['Vorname']}")
    st.write(f"**Adresse**: {patient['Straße + Hnr']}, {patient['PLZ']} {patient['Wohnort']}")
    st.write(f"**Angehörige**: {patient['Angehörige']}")
    st.write(f"**Telefon**: {patient['Telefon']}")
    st.write(f"**E-Mail**: {patient['E-Mail']}")
    st.write(f"**Krankheiten**: {patient['Krankheiten']}")
    st.write(f"**Medikamente**: {patient['Medikamente']}")
    st.write(f"**Tagesdosis**: {patient['Tagesdosis']}")
    st.write(f"**Mitarbeiter-ID**: {patient['Mitarbeiter-ID']}")
    st.write(f"**Mitarbeiter**: {patient['Mitarbeiter']}")
    st.write(f"**Pflegeart**: {patient['Pflegeart']}")
    st.write(f"**Tagebuch-ID**: {patient['Tagebuch-ID']}")
    st.write(f"**Heim-ID**: {patient['Heim-ID']}")
    st.write(f"**Zimmernummer**: {patient['Zimmernummer']}")

    if st.button("Zurück zur Liste"):
        st.session_state.modus = "liste"
        st.session_state.ausgewählter_patient = None
        st.rerun()

    if st.button("Patient löschen"):
        st.session_state.df_patienten = st.session_state.df_patienten[
            st.session_state.df_patienten['Patienten-ID'] != st.session_state.ausgewählter_patient]
        st.session_state.df_patienten.to_csv("Faker/Patienten.csv", index=False)
        reload_data()
        st.session_state.ausgewählter_patient = None
        st.session_state.modus = "liste"
        st.rerun()


#########################################################################
########################################################################
elif st.session_state.modus == "hinzufügen":
    #########################################################################
    # Neu
    # Freie Plätze in den Heimen anzeigen
    st.subheader("Freie Plätze in den Heimen")
    df_heim = st.session_state.df_heim
    df_patienten = st.session_state.df_patienten

    heime_status = []
    for _, heim in df_heim.iterrows():
        heim_id = heim["Heim-ID"]
        max_plaetze = heim.get("Plätze", 0)
        belegte_plaetze = df_patienten[df_patienten['Heim-ID'] == heim_id]['Patienten-ID'].count()
        freie_plaetze = int(max_plaetze) - belegte_plaetze if pd.notnull(max_plaetze) else None
        status = "voll" if freie_plaetze is not None and freie_plaetze <= 0 else "frei"
        heime_status.append({
            "Heim-ID": heim_id,
            "Max. Plätze": max_plaetze,
            "Belegte Plätze": belegte_plaetze,
            "Freie Plätze": freie_plaetze,
            "Status": status
        })

    st.dataframe(pd.DataFrame(heime_status), use_container_width=True)
    ########################################################################
    # Neuen Patienten hinzufügen
    # --- Vorab: CSV-Dateien vorbereiten ---
    df_patienten = st.session_state.df_patienten
    df_mitarbeiter = pd.read_csv("Faker/Mitarbeiter.csv")
    df_heime = pd.read_csv("Faker/Heime.csv")

    # --- Algo1: Freie MA-Kapazität prüfen ---
    def genug_mitarbeiter_verfügbar(df_pat):
        belegung = df_pat.groupby("Mitarbeiter-ID")["Patienten-ID"].count()
        return (belegung < 24).any()

    # --- Algo2: Keine Mischpflege ---
    def spezialisiert_mitarbeiter(mitarbeiter_id, neue_pflegeart, df_patienten):
        patienten_des_ma = df_patienten[df_patienten["Mitarbeiter-ID"] == mitarbeiter_id]

        if patienten_des_ma.empty:
            # Noch keine Patienten → OK
            return True

        vorhandene_arten = patienten_des_ma["Pflegeart"].unique()

        if len(vorhandene_arten) == 1 and vorhandene_arten[0] == neue_pflegeart:
            return True
        else:
            return False

    # --- Algo3: Heim-Platz prüfen ---
    def freie_plaetze(df_heime, df_pat):
        belegte = df_pat.groupby("Heim-ID")["Patienten-ID"].count()
        kapazität = df_heime.set_index("Heim-ID")["Plätze"]
        return kapazität.subtract(belegte, fill_value=0).astype(int)
    
    # Filtere alle MA Pflege & Medizinischer Dienst
    def pflege_mitarbeiter_filtern(df_mitarbeiter):
        return df_mitarbeiter[
            df_mitarbeiter["Abteilung"].isin(["Pflege", "Medizinischer Dienst"])
        ].sort_values(by="Mitarbeiter-ID")
    
    # --- Algo4: MA Kapazität prüfen ---
    def ma_kapazitaet_pruefen(mitarbeiter_id, df_patienten):
        anzahl = df_patienten[df_patienten["Mitarbeiter-ID"] == mitarbeiter_id].shape[0]

        if anzahl >= 24:
            return False
        else:
            return True
        
    # --- Algo5: Verfügbare MA anzeigen ---
    def verfügbare_mitarbeiter_ids(df_mitarbeiter, df_patienten, pflegeart):
        df_gefiltert = pflege_mitarbeiter_filtern(df_mitarbeiter)
        gültige_ids = []

        for mid in df_gefiltert["Mitarbeiter-ID"].unique():
            patienten = df_patienten[df_patienten["Mitarbeiter-ID"] == mid]

            if patienten.empty:
                gültige_ids.append(mid)
            else:
                # Prüfung 1: Nur passende Pflegeart
                vorhandene_arten = patienten["Pflegeart"].unique()
                if len(vorhandene_arten) == 1 and vorhandene_arten[0] == pflegeart:
                    # Prüfung 2: Gesamtanzahl < 24
                    if len(patienten) < 24:
                        gültige_ids.append(mid)

        return gültige_ids

    
    # --- Algo6: Verfügbare Heime anzeigen ---
    def verfügbare_heime(df_heime, df_pat):
        freie = freie_plaetze(df_heime, df_pat)
        return freie[freie > 0].index.tolist()

    # --- Live-Anzeige der freien Plätze ---
    freie_plaetze_df = freie_plaetze(df_heime, df_patienten)

    # 🧾 Formular anzeigen
    st.markdown("### Neuen Patienten hinzufügen")

    with st.form("neuer_patient_formular"):
        df_mitarbeiter = lade_mitarbeiter()
        df_gefilterte_Mitarbeiter = pflege_mitarbeiter_filtern(df_mitarbeiter)

        neue_daten = {}
        neue_daten['Patienten-ID'] = st.text_input("Patienten-ID")
        neue_daten['Nachname'] = st.text_input("Nachname")
        neue_daten['Vorname'] = st.text_input("Vorname")
        neue_daten['Straße + Hnr'] = st.text_input("Straße + Hnr")
        neue_daten['PLZ'] = st.text_input("PLZ")
        neue_daten['Wohnort'] = st.text_input("Wohnort")
        neue_daten['Angehörige'] = st.text_input("Angehörige")
        neue_daten['Telefon'] = st.text_input("Telefon")
        neue_daten['E-Mail'] = st.text_input("E-Mail")
        neue_daten['Krankheiten'] = st.text_area("Krankheiten")
        neue_daten['Medikamente'] = st.text_area("Medikamente")
        neue_daten['Tagesdosis'] = st.text_input("Tagesdosis")
        neue_daten['Heim-ID'] = st.selectbox("Heim-ID", df_heime["Heim-ID"].unique())
        neue_daten['Pflegeart'] = st.selectbox("Pflegeart", ["Bitte wählen", "stationär", "ambulant"])
        neue_daten['Mitarbeiter-ID'] = st.selectbox("Zuständiger Mitarbeiter", df_gefilterte_Mitarbeiter)       
        neue_daten['Tagebuch-ID'] = st.text_input("Tagebuch-ID")
        neue_daten["Zimmernummer"] = st.text_input("Zimmernummer")
        if neue_daten["Mitarbeiter-ID"]:
            mitarbeiter_id = neue_daten["Mitarbeiter-ID"]
            
            # Suche nach dem Mitarbeiter
            mitarbeiter_info = df_mitarbeiter[df_mitarbeiter["Mitarbeiter-ID"] == mitarbeiter_id]

            if not mitarbeiter_info.empty:
                vorname = mitarbeiter_info.iloc[0]["Vorname"]
                nachname = mitarbeiter_info.iloc[0]["Nachname"]
                Name = f"{vorname} {nachname}"
                neue_daten["Mitarbeiter"] = Name
            else:
                neue_daten["Mitarbeiter"] = ""
        

        submitted = st.form_submit_button("Speichern")
        zurück = st.form_submit_button("Zurück")

    if zurück:
        st.session_state.modus = "liste"
        st.rerun()

    if submitted:
        fehlende = [feld for feld in ["Patienten-ID", "Nachname", "Vorname"] if not neue_daten[feld].strip()]
        if neue_daten['Pflegeart'] == "Bitte wählen":
            fehlende.append("Pflegeart")

        if fehlende:
            st.error(f"Bitte fülle folgende Pflichtfelder aus: {', '.join(fehlende)}")
        else:
            # ALGO-PRÜFUNGEN bei Speicher-Trigger
            warnung = False
            if not genug_mitarbeiter_verfügbar(df_patienten):
                st.warning("❌ Es sind nicht genug Mitarbeiter mit Kapazität verfügbar.")
                warnung = True
            if not spezialisiert_mitarbeiter(neue_daten["Mitarbeiter-ID"], neue_daten["Pflegeart"], df_patienten):
                st.warning("❌ Kein geeigneter Mitarbeiter verfügbar (stationär/ambulant darf nicht gemischt werden).")
                warnung = True
            if not ma_kapazitaet_pruefen(mitarbeiter_id, df_patienten):
                verfügbare_ids = verfügbare_mitarbeiter_ids(df_mitarbeiter, df_patienten, neue_daten["Pflegeart"])
                st.warning(f"❌ Mitarbeiter {mitarbeiter_id} ist voll ausgelastet! \n\n Folgende Mitarbeiter sind noch verfügbar: {verfügbare_ids}")
                warnung = True
            if freie_plaetze_df.get(neue_daten['Heim-ID'], 0) <= 0:
                freie_heim_ids = verfügbare_heime(df_heime, df_patienten)
                st.warning(
                    f"❌ Heim {neue_daten['Heim-ID']} ist voll. Patient kann nicht gespeichert werden. \n\n Folgende(r) Heim(e) bieten Platz: {freie_heim_ids}"
                )
                warnung = True

            if warnung:
                st.stop()

            # Wenn alles okay → speichern
            neue_df = pd.DataFrame([neue_daten])
            st.session_state.df_patienten = pd.concat([df_patienten, neue_df], ignore_index=True)
            st.session_state.df_patienten.to_csv("Faker/Patienten.csv", index=False)
            st.success("Patient wurde erfolgreich hinzugefügt!")
            st.session_state.modus = "liste"
            st.rerun()