import streamlit as st


nav_bar1, nav_bar2 = st.columns(2)
with nav_bar1:
        suche = st.text_input("",
                              placeholder="Suche",
                              label_visibility="collapsed",
                              icon="🔍",
                              )

with nav_bar2:
        nav_elem1, nav_elem2 = st.columns(2)
        with nav_elem1:
                postfach = st.button("Postfach",
                                     use_container_width=True,
                                     key = "postfach")
                if postfach:
                        st.write("Du hast auf dein Postfach gedrückt!")
        with nav_elem2:
                abmelden = st.button("Abmelden",
                                     use_container_width=True,
                                     key = "abmelden")
                if abmelden:
                        st.write("Du wirst ausgeloggt")

st.title("Welcome")