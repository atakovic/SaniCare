import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import position

if "sidebar_anzeigen" not in st.session_state:
    st.session_state.sidebar_anzeigen = "hidden"


# --- Funktion: Login prüfen ---
def check_login(username, password, login_df):
    user = login_df[(login_df["Login-Email"] == username) & (login_df["Login-Passwort"] == password)]
    return not user.empty

# --- Login-Daten aus CSV laden ---
@st.cache_data
def load_login_data():
    return pd.read_csv("Faker/Login.csv")

# --- Session State initialisieren ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Hauptlogik: Login oder App anzeigen ---
def login_page():
    st.title("🔐 Login")

    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    if st.button("Anmelden"):
        login_df = load_login_data()
        if check_login(username, password, login_df):
            st.success("Login erfolgreich!")
            st.session_state.logged_in = True
        else:
            st.error("Ungültige Anmeldedaten!")

# --- Wenn eingeloggt, restliche App zeigen ---
pg = st.navigation([st.Page("Welcome.py"), st.Page("Heime.py"), st.Page("News.py"),
                    st.Page("Mitarbeiter.py"), st.Page("Patienten_neu.py"), st.Page("Events.py"),
                    ],
                   position=st.session_state.sidebar_anzeigen,
)


# --- Ausführung ---
def main():
    if st.session_state.logged_in:
        st.session_state.sidebar_anzeigen = "sidebar"
        pg.run()
    else:
        login_page()
        st.session_state.sidebar_anzeigen = "hidden"


if __name__ == "__main__":
    main()
    st.write(st.session_state)