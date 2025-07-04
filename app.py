import streamlit as st


pg = st.navigation([st.Page("Welcome.py"), st.Page("Heime.py"), st.Page("News.py"),
                    st.Page("Mitarbeiter.py"), st.Page("Patienten_neu.py"), st.Page("Events.py"),
                    ])
pg.run()
