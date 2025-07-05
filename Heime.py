import streamlit as st
import pandas as pd


# Daten laden ohne Cache, damit immer aktuell
def lade_Heime():
    df = pd.read_csv("Faker/Heime.csv")
    df.columns = df.columns.str.strip()
    return df





# Daten in Session State speichern (oder laden, falls noch nicht vorhanden)
if "df_Heime" not in st.session_state:
    st.session_state.df_Heime = lade_Heime()




def reload_data():
    st.session_state.df_Heime = lade_Heime()



# Session State für UI-Steuerung
if "ausgewählter_Heime" not in st.session_state:
    st.session_state.ausgewählter_Heime = None
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
    suche = st.text_input("", placeholder="Nach Heim suchen", label_visibility="collapsed")
with col_postfach:
    if st.button("Postfach", use_container_width=True):
        st.switch_page("Welcome.py")
with col_abmelden:
    if st.button("Abmelden", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.Name = None
        st.session_state.pg = None
        st.rerun()  # Zurück zur Login-Seite

# „Neuen Heime hinzufügen“-Button oben, nur im Listenmodus
#if st.session_state.modus == "liste":
   # if st.button("Neue Heime hinzufügen", use_container_width=True):
        #st.session_state.modus = "hinzufügen"
        #st.session_state.ausgewählter_Heime = None
        #st.rerun()

# Heimeliste anzeigen
if st.session_state.modus == "liste" and st.session_state.ausgewählter_Heime is None:
    gefiltert = st.session_state.df_Heime
    if suche:
        suchbegriff = suche.strip().lower()
        gefiltert = gefiltert[
            gefiltert['Straße + Hnr'].astype(str).str.lower().str.contains(suchbegriff, na=False) |
            gefiltert['Heim-ID'].astype(str).str.lower().str.contains(suchbegriff, na=False) |
            gefiltert['Zuständiger Heimleiter:in'].astype(str).str.lower().str.contains(suchbegriff, na=False)
            ]
    pro_seite = 25
    seitenzahl = (len(gefiltert) - 1) // pro_seite + 1
    start_idx = st.session_state.seite * pro_seite
    end_idx = start_idx + pro_seite
    seite_df = gefiltert.iloc[start_idx:end_idx]

    st.markdown("### Liste aller Heime")

    for _, row in seite_df.iterrows():
        if st.button(f"{row['Heim-ID']}: {row['Straße + Hnr']} {row['E-Mail-Adresse']}", use_container_width=True):
            st.session_state.ausgewählter_Heime = row['Heim-ID']
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

# Detailansicht eines Heime
elif st.session_state.ausgewählter_Heime is not None and st.session_state.modus == "detail":
    Heime = st.session_state.df_Heime[
        st.session_state.df_Heime['Heim-ID'] == st.session_state.ausgewählter_Heime].iloc[0]

    st.markdown("### Heim-daten")
    st.write(f"**Heim-ID**: {Heime['Heim-ID']}")
    st.write(f"**Zimmernummer**: {Heime['Zimmernummer']}")
    st.write(f"**Straße + Hnr**: {Heime['Straße + Hnr']}")
    st.write(f"**PLZ**: {Heime['PLZ']}")
    st.write(f"**Ort**: {Heime['Ort']}")
    st.write(f"**Zuständiger Heimleiter:in**: {Heime['Zuständiger Heimleiter:in']}")
    st.write(f"**Telefonnummer**: {Heime['Telefonnummer']}")
    st.write(f"**E-Mail-Adresse**: {Heime['E-Mail-Adresse']}")

    if st.button("Zurück zur Liste"):
        st.session_state.modus = "liste"
        st.session_state.ausgewählter_Heime = None
        st.rerun()

    #if st.button("Heime löschen"):
       # st.session_state.df_Heime = st.session_state.df_Heime[
           # st.session_state.df_Heime['Heim-ID'] != st.session_state.ausgewählter_Heime]
       # st.session_state.df_Heime.to_csv("scratches/Heime.csv", index=False)
      #  reload_data()
     #   st.session_state.ausgewählter_Heime = None
      #  st.session_state.modus = "liste"
       # st.rerun()

# Neuen Heime hinzufügen
#elif st.session_state.modus == "hinzufügen":
    #st.markdown("### Neuen Heime hinzufügen")

    #with st.form("neuer_Heime_formular"):
        #neue_daten = {}
       # neue_daten['Heim-ID'] = st.text_input("Heim-ID")
        #neue_daten['Uhrzeit'] = st.text_input("Uhrzeit")
       # neue_daten['Titel'] = st.text_input("Titel")
       # neue_daten['Text'] = st.text_input("Text")


        #submitted = st.form_submit_button("Speichern")
       # zurück = st.form_submit_button("Zurück")

   # if zurück:
       # st.session_state.modus = "liste"
        #st.rerun()

    #if submitted:
        #pflichtfelder = ["Heim-ID", "Uhrzeit", "Titel", "Text"]
       # fehlende = [feld for feld in pflichtfelder if not neue_daten[feld].strip()]


       # if fehlende:
           # st.error(f"Bitte fülle folgende Pflichtfelder aus: {', '.join(fehlende)}")


      #  else:
             #   neue_Heime_df = pd.DataFrame([neue_daten])
             #   st.session_state.df_Heime = pd.concat([st.session_state.df_Heime, neue_Heime_df],
                   #                                       ignore_index=True)
              #  st.session_state.df_Heime.to_csv("scratches/Heime.csv", index=False)
               # reload_data()
              #  st.success("Heime hinzugefügt!")
               # st.session_state.modus = "liste"
                #st.rerun()


