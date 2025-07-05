import streamlit as st
import pandas as pd
from datetime import datetime

# --- Hilfsfunktionen ---
def lade_Postfach():
    df = pd.read_csv("Faker/Postfach.csv")
    df.columns = df.columns.str.strip()
    return df

def speichere_postfach(df):
    df.to_csv("Faker/Postfach.csv", index=False)

def reload_data():
    st.session_state.df_Postfach = lade_Postfach()

# --- Session State ---
if "df_Postfach" not in st.session_state:
    st.session_state.df_Postfach = lade_Postfach()

if "postfach_modus" not in st.session_state:
    st.session_state.postfach_modus = "empfangen"  # empfangen | gesendet | detail | neu

if "ausgewählte_nachricht" not in st.session_state:
    st.session_state.ausgewählte_nachricht = None

if "pg" not in st.session_state:
        st.session_state.pg = None


# --- Name aus Session extrahieren ---
vorname = st.session_state.Name.split()[0]
nachname = st.session_state.Name.split()[1]

# --- UI: Navigation ---
st.title(f"Welcome {vorname} {nachname}")
st.subheader("📨 Postfach")

# Kopfzeile mit Suchfeld, Postfach, Abmelden
col_suche, col_abmelden = st.columns([3, 1, ])
with col_suche:
    suche = st.text_input("", placeholder="Nach Titel suchen", label_visibility="collapsed")
    gefiltert = st.session_state.df_Postfach
    if suche:
        suchbegriff = suche.lower()
        gefiltert = gefiltert[
            gefiltert['Nachricht'].astype(str).str.lower().str.contains(suchbegriff, na=False) |
            gefiltert['Von_Vorname'].astype(str).str.lower().str.contains(suchbegriff, na=False) |
            gefiltert['Von_Nachname'].astype(str).str.lower().str.contains(suchbegriff, na=False)
            ]

with col_abmelden:
    if st.button("Abmelden", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.Name = None
        st.session_state.pg = None
        st.rerun()  # Zurück zur Login-Seite

nav1, nav2, nav3 = st.columns(3)
with nav1:
    if st.button("📥 Empfangen", use_container_width=True):
        st.session_state.postfach_modus = "empfangen"
        st.session_state.ausgewählte_nachricht = None
        st.rerun()
with nav2:
    if st.button("📤 Gesendet", use_container_width=True):
        st.session_state.postfach_modus = "gesendet"
        st.session_state.ausgewählte_nachricht = None
        st.rerun()
with nav3:
    if st.button("✍️ Neue Nachricht", use_container_width=True):
        st.session_state.postfach_modus = "neu"
        st.session_state.ausgewählte_nachricht = None
        st.rerun()

# --- Suche & Liste ---
if st.session_state.postfach_modus in ["empfangen", "gesendet"]:
    df = st.session_state.df_Postfach

    if st.session_state.postfach_modus == "empfangen":
        df = df[(df["An_Vorname"] == vorname) & (df["An_Nachname"] == nachname)]
    else:
        df = df[(df["Von_Vorname"] == vorname) & (df["Von_Nachname"] == nachname)]


    df = df.sort_values(by=["Datum", "Uhrzeit"], ascending=False)

    if df.empty:
        st.info("Keine Nachrichten gefunden.")
    else:
        for i, row in df.iterrows():
            if st.button(f"{row['Datum']} {row['Uhrzeit']} | Von: {row['Von_Vorname']} {row['Von_Nachname']} | An: {row['An_Vorname']} {row['An_Nachname']}", key=f"msg_{i}"):
                st.session_state.ausgewählte_nachricht = i
                st.session_state.postfach_modus = "detail"
                st.rerun()

# --- Detailansicht ---
elif st.session_state.postfach_modus == "detail":
    idx = st.session_state.ausgewählte_nachricht
    nachricht = st.session_state.df_Postfach.loc[idx]

    st.markdown(f"**Datum**: {nachricht['Datum']} {nachricht['Uhrzeit']}")
    st.markdown(f"**Von**: {nachricht['Von_Vorname']} {nachricht['Von_Nachname']}")
    st.markdown(f"**An**: {nachricht['An_Vorname']} {nachricht['An_Nachname']}")
    st.markdown("**Nachricht:**")
    st.info(nachricht['Nachricht'])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Löschen"):
            st.session_state.df_Postfach = st.session_state.df_Postfach.drop(idx)
            speichere_postfach(st.session_state.df_Postfach)
            st.success("Nachricht gelöscht.")
            st.session_state.postfach_modus = "empfangen"
            st.session_state.ausgewählte_nachricht = None
            reload_data()
            st.rerun()
    with col2:
        if st.button("Zurück"):
            st.session_state.postfach_modus = "empfangen"
            st.session_state.ausgewählte_nachricht = None
            st.rerun()

# --- Neue Nachricht ---
elif st.session_state.postfach_modus == "neu":
    df_mitarbeiter = pd.read_csv("Faker/Mitarbeiter.csv")
    empfänger_options = [
        f"{r['Vorname']} {r['Nachname']} ({r['Mitarbeiter-ID']})"
        for _, r in df_mitarbeiter.iterrows()
        if r['Vorname'] != vorname or r['Nachname'] != nachname
    ]

    with st.form("neue_nachricht"):
        empfänger = st.selectbox("Empfänger", empfänger_options)
        nachricht = st.text_area("Nachricht", height=150)
        senden = st.form_submit_button("Senden")

    if senden:
        # Empfänger extrahieren
        teile = empfänger.split()
        emp_vorname = teile[0]
        emp_nachname = teile[1]

        jetzt = datetime.now()
        neue_nachricht = {
            "Datum": jetzt.date().isoformat(),
            "Uhrzeit": jetzt.strftime("%H:%M:%S"),
            "Von_ID": "",  # optional
            "Von_Vorname": vorname,
            "Von_Nachname": nachname,
            "An_ID": "",  # optional
            "An_Vorname": emp_vorname,
            "An_Nachname": emp_nachname,
            "Nachricht": nachricht
        }

        st.session_state.df_Postfach = pd.concat([
            st.session_state.df_Postfach,
            pd.DataFrame([neue_nachricht])
        ], ignore_index=True)
        speichere_postfach(st.session_state.df_Postfach)
        st.success("Nachricht gesendet.")
        st.session_state.postfach_modus = "empfangen"
        st.rerun()
