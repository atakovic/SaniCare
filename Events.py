import streamlit as st
import pandas as pd


# Daten laden ohne Cache, damit immer aktuell
def lade_Events():
    df = pd.read_csv("Faker/Events.csv")
    df.columns = df.columns.str.strip()
    return df





# Daten in Session State speichern (oder laden, falls noch nicht vorhanden)
if "df_Events" not in st.session_state:
    st.session_state.df_Events = lade_Events()




def reload_data():
    st.session_state.df_Events = lade_Events()



# Session State für UI-Steuerung
if "ausgewählter_Events" not in st.session_state:
    st.session_state.ausgewählter_Events = None
if "seite" not in st.session_state:
    st.session_state.seite = 0
if "modus" not in st.session_state:
    st.session_state.modus = "liste"  # liste, detail, hinzufügen
if "popup_visible" not in st.session_state:
    st.session_state.popup_visible = True
if "pg" not in st.session_state:
        st.session_state.pg = None


# Popup für Warnungen


# Kopfzeile mit Suchfeld, Postfach, Abmelden
col_suche, col_postfach, col_abmelden = st.columns([3, 1, 1])
with col_suche:
    suche = st.text_input("", placeholder="Nach Titel suchen", label_visibility="collapsed")
with col_postfach:
    if st.button("Postfach", use_container_width=True):
        st.switch_page("Welcome.py")
with col_abmelden:
    if st.button("Abmelden", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.Name = None
        st.session_state.pg = None
        st.rerun()  # Zurück zur Login-Seite

# „Neuen Events hinzufügen“-Button oben, nur im Listenmodus
if st.session_state.modus == "liste":
    if st.button("Neue Events hinzufügen", use_container_width=True):
        st.session_state.modus = "hinzufügen"
        st.session_state.ausgewählter_Events = None
        st.rerun()

# Eventsliste anzeigen
if st.session_state.modus == "liste" and st.session_state.ausgewählter_Events is None:
    gefiltert = st.session_state.df_Events
    if suche:
        suchbegriff = suche.strip().lower()
        gefiltert = gefiltert[
            gefiltert['Veranstaltungsnummer'].astype(str).str.lower().str.contains(suchbegriff, na=False) |
            gefiltert['Art der Veranstaltung'].astype(str).str.lower().str.contains(suchbegriff, na=False) |
            gefiltert['Titel'].astype(str).str.lower().str.contains(suchbegriff, na=False) |
            gefiltert['Veranstalter'].astype(str).str.lower().str.contains(suchbegriff, na=False) |
            gefiltert['Ort der Veranstaltung'].astype(str).str.lower().str.contains(suchbegriff, na=False)

        ]

    pro_seite = 25
    seitenzahl = (len(gefiltert) - 1) // pro_seite + 1
    start_idx = st.session_state.seite * pro_seite
    end_idx = start_idx + pro_seite
    seite_df = gefiltert.iloc[start_idx:end_idx]

    st.markdown("### Liste aller Events")

    for _, row in seite_df.iterrows():
        if st.button(f"{row['Veranstaltungsnummer']}: {row['Art der Veranstaltung']} {row['Titel']}", use_container_width=True):
            st.session_state.ausgewählter_Events = row['Veranstaltungsnummer']
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

    cols = st.columns(len(seiten_liste))
    for i, val in enumerate(seiten_liste):
        if val == "...":
            cols[i].write("...")
        else:
            if cols[i].button(str(val + 1), use_container_width=True):
                st.session_state.seite = val
                st.rerun()

# Detailansicht eines Events
elif st.session_state.ausgewählter_Events is not None and st.session_state.modus == "detail":
    Events = st.session_state.df_Events[
        st.session_state.df_Events['Veranstaltungsnummer'] == st.session_state.ausgewählter_Events].iloc[0]

    st.markdown("### Eventsdaten")
    st.write(f"**Veranstaltungsnummer**: {Events['Veranstaltungsnummer']}")
    st.write(f"**Art der Veranstaltung**: {Events['Art der Veranstaltung']}")
    st.write(f"**Titel**: {Events['Titel']}")
    st.write(f"**Veranstalter**: {Events['Veranstalter']}")
    st.write(f"**zuständige Mitarbeiter**: {Events['zuständige Mitarbeiter']}")
    st.write(f"**Teilnehmer(Pat. ID / Ang. ID / Pfleger ID)**: {Events['Teilnehmer(Pat. ID / Ang. ID / Pfleger ID)']}")
    st.write(f"**Ort der Veranstaltung**: {Events['Ort der Veranstaltung']}")
    st.write(f"**Raum**: {Events['Raum']}")
    st.write(f"**Hinweise**: {Events['Hinweise']}")
    st.write(f"**Datum**: {Events['Datum']}")
    st.write(f"**Beginn**: {Events['Beginn']}")
    st.write(f"**Ende**: {Events['Ende']}")

    if st.button("Zurück zur Liste"):
        st.session_state.modus = "liste"
        st.session_state.ausgewählter_Events = None
        st.rerun()

    if st.button("Events löschen"):
        st.session_state.df_Events = st.session_state.df_Events[
            st.session_state.df_Events['Veranstaltungsnummer'] != st.session_state.ausgewählter_Events]
        st.session_state.df_Events.to_csv("scratches/Events.csv", index=False)
        reload_data()
        st.session_state.ausgewählter_Events = None
        st.session_state.modus = "liste"
        st.rerun()

# Neuen Events hinzufügen
elif st.session_state.modus == "hinzufügen":
    st.markdown("### Neue Events hinzufügen")

    with st.form("neuer_Events_formular"):
        neue_daten = {}
        neue_daten['Veranstaltungsnummer'] = st.text_input("Veranstaltungsnummer")
        neue_daten['Art der Veranstaltung'] = st.text_input("Art der Veranstaltung")
        neue_daten['Titel'] = st.text_input("Titel")
        neue_daten['Veranstalter'] = st.text_input("Veranstalter")
        neue_daten['zuständige Mitarbeiter'] = st.text_input("zuständige Mitarbeiter")
        neue_daten['Teilnehmer(Pat. ID / Ang. ID / Pfleger ID'] = st.text_input("Teilnehmer(Pat. ID / Ang. ID / Pfleger ID")
        neue_daten['Ort der Veranstaltung'] = st.text_input("Ort der Veranstaltung")
        neue_daten['Raum'] = st.text_input("Raum")
        neue_daten['Hinweise'] = st.text_input("Hinweise")
        neue_daten['Datum'] = st.text_input("Datum")
        neue_daten['Beginn'] = st.text_input("Beginn")
        neue_daten['Ende'] = st.text_input("Ende")




        submitted = st.form_submit_button("Speichern")
        zurück = st.form_submit_button("Zurück")

    if zurück:
        st.session_state.modus = "liste"
        st.rerun()

    if submitted:
        pflichtfelder = ["Veranstaltungsnummer", "Ort der Veranstaltung", "Titel", "Datum","Beginn","Ende"]
        fehlende = [feld for feld in pflichtfelder if not neue_daten[feld].strip()]


        if fehlende:
            st.error(f"Bitte fülle folgende Pflichtfelder aus: {', '.join(fehlende)}")


        else:
                neue_Events_df = pd.DataFrame([neue_daten])
                st.session_state.df_Events = pd.concat([st.session_state.df_Events, neue_Events_df],
                                                          ignore_index=True)
                st.session_state.df_Events.to_csv("scratches/Events.csv", index=False)
                reload_data()
                st.success("Events hinzugefügt!")
                st.session_state.modus = "liste"
                st.rerun()


