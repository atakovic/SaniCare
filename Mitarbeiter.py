import streamlit as st
import pandas as pd

@st.cache_data
def lade_Mitarbeiter():
    df = pd.read_csv("Faker/Mitarbeiter.csv")
    df.columns = df.columns.str.strip()
    return df

@st.cache_data
def lade_Patienten():
    df_p = pd.read_csv("Faker/Patienten.csv")
    df_p.columns = df_p.columns.str.strip()
    return df_p

df = lade_Mitarbeiter()
if "df_Mitarbeiter" not in st.session_state:
    st.session_state.df_Mitarbeiter = None
st.session_state.df_Mitarbeiter = df
df_patienten = lade_Patienten()

# Initialisierung des States
if "ausgewahlt_mitarbeiter" not in st.session_state:
    st.session_state.ausgewahlt_mitarbeiter = None
if "seite" not in st.session_state:
    st.session_state.seite = 0
if "modus" not in st.session_state:
    st.session_state.modus = "liste"

col_suche, col_postfach, col_abmelden = st.columns([3,1,1])
with col_suche:
    if st.session_state.modus == "liste" and st.session_state.ausgewahlt_mitarbeiter is None:
        suche = st.text_input("", placeholder="Nach Name suchen", label_visibility="collapsed")
    else:
        suche = ""

with col_postfach:
    if st.button("Postfach", use_container_width=True):
        st.warning("Du hast auf den Postfach gedrückt!")
with col_abmelden:
    if st.button("Abmelden", use_container_width=True):
        st.warning("Du wurdest abgemeldet.")

if st.session_state.modus == "liste" and st.session_state.ausgewahlt_mitarbeiter is None:
    if st.button("Neuen Mitarbeiter hinzufügen", use_container_width=True):
        st.session_state.modus = "hinzufügen"
        st.rerun()

# Mitarbeiterliste anzeigen
if st.session_state.modus == "liste" and st.session_state.ausgewahlt_mitarbeiter is None:
    gefiltert = st.session_state.df_Mitarbeiter
    if suche:
        suchbegriff = suche.strip().lower()
        gefiltert = gefiltert[
            gefiltert['Vorname'].astype(str).str.lower().str.contains(suchbegriff, na=False) |
            gefiltert['Nachname'].astype(str).str.lower().str.contains(suchbegriff, na=False) |
            gefiltert['Mitarbeiter-ID'].astype(str).str.lower().str.contains(suchbegriff, na=False)
            ]

    pro_seite = 25
    seitenzahl = max(1, (len(gefiltert) - 1) // pro_seite + 1)
    start_idx = st.session_state.seite * pro_seite
    end_idx = start_idx + pro_seite
    seite_df = gefiltert.iloc[start_idx:end_idx]

    seite_df = gefiltert.iloc[start_idx:end_idx]

    if gefiltert.empty:
        st.info("🔍 Keine Treffer gefunden.")
    else:
        st.markdown("Liste aller Mitarbeiter")
        for _, row in seite_df.iterrows():
            if st.button(f"{row['Mitarbeiter-ID']}: {row['Nachname']} {row['Vorname']}", use_container_width=True):
                st.session_state.ausgewahlt_mitarbeiter = row['Mitarbeiter-ID']
                st.rerun()

    # Paginierung
    def Seitenliste(aktuelle, gesamt):
        if gesamt <= 7:
            return list(range(gesamt))
        if aktuelle < 4:
            return list(range(5)) + ["...", gesamt - 1]
        if aktuelle > gesamt - 5:
            return [0, "..."] + list(range(gesamt - 5, gesamt))
        return [0, "..."] + list(range(aktuelle - 1, aktuelle + 2)) + ["...", gesamt - 1]

    seiten_liste = Seitenliste(st.session_state.seite, seitenzahl)
    nav_cols = st.columns(len(seiten_liste))
    for i, item in enumerate(seiten_liste):
        with nav_cols[i]:
            if item == "...":
                st.markdown("⋯")
            elif item == st.session_state.seite:
                st.markdown(f"**{item + 1}**")
            else:
                if st.button(str(item + 1), key=f"seite_{item}"):
                    st.session_state.seite = item
                    st.rerun()

# Detailansicht eines Mitarbeiters
elif st.session_state.ausgewahlt_mitarbeiter is not None:
    Mitarbeiter = df[df['Mitarbeiter-ID'] == st.session_state.ausgewahlt_mitarbeiter].iloc[0]

    if st.session_state.modus == "bearbeiten":
        st.markdown("Bearbeiten")
        with st.form("bearbeiten_form"):
            nachname = st.text_input("Nachname", value=Mitarbeiter['Nachname'])
            vorname = st.text_input("Vorname", value=Mitarbeiter['Vorname'])
            abteilung = st.text_input("Abteilung", value=Mitarbeiter.get('Abteilung',""))
            strasse = st.text_input("Straße + Hnr", value=Mitarbeiter['Straße + Hnr'])
            plz = st.text_input("PLZ", value=Mitarbeiter['PLZ'])
            wohnort = st.text_input("Wohnort", value=Mitarbeiter['Wohnort'])
            telefon = st.text_input("Telefon", value=Mitarbeiter['Telefon'])
            email = st.text_input("E-Mail", value=Mitarbeiter['E-Mail'])
            rolle = st.text_input("Rolle", value=Mitarbeiter.get('Rolle',""))

            speichern = st.form_submit_button("Speichern")
            abbrechen = st.form_submit_button("Abbrechen")

        if speichern:
            idx = df.index[df['Mitarbeiter-ID'] == st.session_state.ausgewahlt_mitarbeiter][0]
            df.at[idx, 'Nachname'] = nachname
            df.at[idx, 'Vorname'] = vorname
            if 'Abteilung' in df.columns:
                df.at[idx, 'Abteilung'] = abteilung
            df.at[idx, 'Straße + Hnr'] = strasse
            df.at[idx, 'PLZ'] = plz
            df.at[idx, 'Wohnort'] = wohnort
            df.at[idx, 'Telefon'] = telefon
            df.at[idx, 'E-Mail'] = email
            if 'Rolle' in df.columns:
                df.at[idx, 'Rolle'] = rolle
            df.to_csv("Faker/Mitarbeiter.csv", index=False)
            lade_Mitarbeiter.clear()
            df = lade_Mitarbeiter()
            st.success("Mitarbeiterdaten wurden aktualisiert.")
            st.session_state.modus = "liste"
            st.session_state.ausgewahlt_mitarbeiter = None
            st.rerun()

        if abbrechen:
            st.session_state.modus = "liste"
            st.rerun()

    elif st.session_state.modus == "direktnachricht":
        empfanger = Mitarbeiter
        with st.form("nachricht_form"):
            st.markdown(f"Nachricht an {empfanger['Vorname']} {empfanger['Nachname']}")
            nachricht = st.text_area("Ihre Nachricht", height=150)
            col_senden, col_zurück = st.columns(2)
            with col_senden:
                if st.form_submit_button("Nachrichten senden"):
                    st.success(f"Nachricht an {empfanger['Vorname']} {empfanger['Nachname']} gesendet.")
                    st.session_state.modus = "liste"
                    st.rerun()
            with col_zurück:
                if st.form_submit_button("Zurück"):
                    st.session_state.modus = "liste"
                    st.rerun()

    else:
        # Normale Detailanzeige
        st.markdown("Mitarbeiterdetails")
        st.write(f"**Mitarbeiter-ID**: {Mitarbeiter['Mitarbeiter-ID']}")
        st.write(f"**Name**: {Mitarbeiter['Nachname']} {Mitarbeiter['Vorname']}")
        st.write(f"**Abteilung**: {Mitarbeiter.get('Abteilung','')}")
        st.write(f"**Adresse**: {Mitarbeiter['Straße + Hnr']}, {Mitarbeiter['PLZ']} {Mitarbeiter['Wohnort']}")
        st.write(f"**Telefon**: {Mitarbeiter['Telefon']}")
        st.write(f"**E-Mail**: {Mitarbeiter['E-Mail']}")
        st.write(f"**Rolle**: {Mitarbeiter.get('Rolle','')}")

        st.markdown("Liste alle betreuenden Personen")
        betreute = df_patienten[df_patienten['Mitarbeiter-ID'] == Mitarbeiter['Mitarbeiter-ID']]
        if not betreute.empty:
            for _, pat in betreute.iterrows():
                st.write(f"- {pat['Patienten-ID']}: {pat['Nachname']} {pat['Vorname']}")
                #st.write(f"- {pat['Patienten-ID']}: {pat['Name']}")
        else:
            st.info("Keine betreuten Patienten gefunden.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Direktnachricht"):
                st.session_state.modus = "direktnachricht"
                st.rerun()
        with col2:
            if st.button("Bearbeiten"):
                st.session_state.modus = "bearbeiten"
                st.rerun()

        col3, col4 = st.columns(2)
        with col3:
            if st.button("Mitarbeiter löschen"):
                df = df[df['Mitarbeiter-ID'] != st.session_state.ausgewahlt_mitarbeiter]
                df.to_csv("Faker/Mitarbeiter.csv", index=False)
                lade_Mitarbeiter.clear()
                df = lade_Mitarbeiter()
                st.success("Mitarbeiter wurde gelöscht.")
                st.session_state.ausgewahlt_mitarbeiter = None
                st.rerun()
        with col4:
            if st.button("Zurück zur Liste"):
                st.session_state.ausgewahlt_mitarbeiter = None
                st.rerun()

# Formular neue Mitarbeiter
elif st.session_state.modus == "hinzufügen":
    st.markdown("Neue Mitarbeiter")
    with st.form("neuer_Mitarbeiter_formular"):
        neue_daten = {}
        neue_daten['Mitarbeiter-ID'] = st.text_input("Mitarbeiter-ID")
        neue_daten['Nachname'] = st.text_input("Nachname")
        neue_daten['Vorname'] = st.text_input("Vorname")
        neue_daten['Straße + Hnr'] = st.text_input("Straße + Hnr")
        neue_daten['PLZ'] = st.text_input("PLZ")
        neue_daten['Wohnort'] = st.text_input("Wohnort")
        neue_daten['Telefon'] = st.text_input("Telefon")
        neue_daten['E-Mail'] = st.text_input("E-Mail")
        submitted = st.form_submit_button("Speichern")
    if submitted:
        pflicht = ["Mitarbeiter-ID","Nachname","Vorname"]
        fehl = [f for f in pflicht if not neue_daten[f].strip()]
        if fehl:
            st.error(f"Bitte fülle folgende Pflichtfelder aus: {', '.join(fehl)}")
        else:
            df = pd.concat([df, pd.DataFrame([neue_daten])], ignore_index=True)
            df.to_csv("Faker/Mitarbeiter.csv", index=False)
            lade_Mitarbeiter.clear()
            df = lade_Mitarbeiter()
            st.success("Mitarbeiter hinzugefügt!")
            st.session_state.modus = "liste"
            st.rerun()
    if st.button("↩️ Zurück zur Liste"):
        st.session_state.modus = "liste"
        st.rerun()



