import streamlit as st
import pandas as pd



# Daten laden ohne Cache, damit immer aktuell
def lade_News():
    df = pd.read_csv("Faker/News.csv")
    df.columns = df.columns.str.strip()
    return df





# Daten in Session State speichern (oder laden, falls noch nicht vorhanden)
if "df_News" not in st.session_state:
    st.session_state.df_News = lade_News()




def reload_data():
    st.session_state.df_News = lade_News()



# Session State für UI-Steuerung
if "ausgewählter_News" not in st.session_state:
    st.session_state.ausgewählter_News = None
if "seite" not in st.session_state:
    st.session_state.seite = 0
if "modus" not in st.session_state:
    st.session_state.modus = "liste"  # liste, detail, hinzufügen
if "popup_visible" not in st.session_state:
    st.session_state.popup_visible = True


# Popup für Warnungen


# Kopfzeile mit Suchfeld, Postfach, Abmelden
col_suche, col_postfach, col_abmelden = st.columns([3, 1, 1])
with col_suche:
    suche = st.text_input("", placeholder="Nach Titel suchen", label_visibility="collapsed")
with col_postfach:
    if st.button("Postfach", use_container_width=True):
        st.warning("Du hast auf dein Postfach gedrückt!")
with col_abmelden:
    if st.button("Abmelden", use_container_width=True):
        st.warning("Du wurdest abgemeldet.")

# „Neuen News hinzufügen“-Button oben, nur im Listenmodus
if st.session_state.modus == "liste":
    if st.button("Neue News hinzufügen", use_container_width=True):
        st.session_state.modus = "hinzufügen"
        st.session_state.ausgewählter_News = None
        st.rerun()

# Newsliste anzeigen
if st.session_state.modus == "liste" and st.session_state.ausgewählter_News is None:
    gefiltert = st.session_state.df_News
    if suche:
        suchbegriff = suche.strip().lower()
        gefiltert = gefiltert[
            gefiltert['Titel'].astype(str).str.lower().str.contains(suchbegriff, na=False) |
            gefiltert['Text'].astype(str).str.lower().str.contains(suchbegriff, na=False) |
            gefiltert['Datum'].astype(str).str.lower().str.contains(suchbegriff, na=False)
            ]


    pro_seite = 25
    seitenzahl = (len(gefiltert) - 1) // pro_seite + 1
    start_idx = st.session_state.seite * pro_seite
    end_idx = start_idx + pro_seite
    seite_df = gefiltert.iloc[start_idx:end_idx]

    st.markdown("### Liste aller News")

    for _, row in seite_df.iterrows():
        if st.button(f"{row['Datum']}: {row['Uhrzeit']} {row['Titel']}", use_container_width=True):
            st.session_state.ausgewählter_News = row['Datum']
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

# Detailansicht eines News
elif st.session_state.ausgewählter_News is not None and st.session_state.modus == "detail":
    News = st.session_state.df_News[
        st.session_state.df_News['Datum'] == st.session_state.ausgewählter_News].iloc[0]

    st.markdown("### Newsdaten")
    st.write(f"**Datum**: {News['Datum']}")
    st.write(f"**Uhrzeit**: {News['Uhrzeit']}")
    st.write(f"**Titel**: {News['Titel']}")
    st.write(f"**Text**: {News['Text']}")

    if st.button("Zurück zur Liste"):
        st.session_state.modus = "liste"
        st.session_state.ausgewählter_News = None
        st.rerun()

    if st.button("News löschen"):
        st.session_state.df_News = st.session_state.df_News[
            st.session_state.df_News['Datum'] != st.session_state.ausgewählter_News]
        st.session_state.df_News.to_csv("scratches/News.csv", index=False)
        reload_data()
        st.session_state.ausgewählter_News = None
        st.session_state.modus = "liste"
        st.rerun()

# Neuen News hinzufügen
elif st.session_state.modus == "hinzufügen":
    st.markdown("### Neuen News hinzufügen")

    with st.form("neuer_News_formular"):
        neue_daten = {}
        neue_daten['Datum'] = st.text_input("Datum")
        neue_daten['Uhrzeit'] = st.text_input("Uhrzeit")
        neue_daten['Titel'] = st.text_input("Titel")
        neue_daten['Text'] = st.text_input("Text")


        submitted = st.form_submit_button("Speichern")
        zurück = st.form_submit_button("Zurück")

    if zurück:
        st.session_state.modus = "liste"
        st.rerun()

    if submitted:
        pflichtfelder = ["Datum", "Uhrzeit", "Titel", "Text"]
        fehlende = [feld for feld in pflichtfelder if not neue_daten[feld].strip()]


        if fehlende:
            st.error(f"Bitte fülle folgende Pflichtfelder aus: {', '.join(fehlende)}")


        else:
                neue_News_df = pd.DataFrame([neue_daten])
                st.session_state.df_News = pd.concat([st.session_state.df_News, neue_News_df],
                                                          ignore_index=True)
                st.session_state.df_News.to_csv("scratches/News.csv", index=False)
                reload_data()
                st.success("News hinzugefügt!")
                st.session_state.modus = "liste"
                st.rerun()


