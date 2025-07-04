import datetime
import streamlit as st
import importlib.util
import pandas as pd
import numpy as np

from sqlalchemy import engine, create_engine, text

#--------------------------------------------------------------------------------------------
class Seite:
  def __init__(self, user, daten, postfach, page, login):
    self.user = user            #ID
    self.daten = daten          #Datenbank
    self.postfach = postfach
    self.page = page
    self.login = login          #boolean
  def showToolbar(self):
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
                             key="postfach")
        if postfach:
          st.write("Du hast auf dein Postfach gedrückt!")
      with nav_elem2:
        abmelden = st.button("Abmelden",
                             use_container_width=True,
                             key="abmelden")
        if abmelden:
          st.write("Du wirst ausgeloggt")
    st.title(f"{self.page}")


  def suche(self):
    print("Hello my name is " + self.name)
  def deleteData(self):
    print("Hello my name is " + self.name)

class Login(Seite):
  def __init__(self, user, daten, postfach, page, login, benutzer, passwort):
    Seite.__init__(self, user, daten, postfach, page, login)
    self.page = "Login"
    #user = ID
    #daten = CSV Daten
    #postfach = Postfach Klasse
    #page = Name der Page "Login"
    #login = true / false - also angemeldet ja oder nein?
    self.benutzer = benutzer      #E-Mail
    self.passwort = passwort      #Passwort

  def anmelden(self):
    super().anmelden()
  def abmelden(self):
    super().abmelden()
  def setLogin(self, login):
    self.login = login
  def setBenutzer(self, benutzer, passwort):
    self.benutzer = benutzer
    self.passwort = passwort

  def getLogin(self):
    try:
        csv_path = f"{self.page}.csv"
        benutzer = self.benutzer
        passwort = self.passwort
        df = self.daten

        # Suche nach passendem Benutzer + Passwort
        match = df[
            (df["Login-Email"] == benutzer) &
            (df["Login-Passwort"] == passwort)
        ]

        return not match.empty  # True wenn Treffer gefunden
    except FileNotFoundError:
        st.warning(f"Datei nicht gefunden: {csv_path}")
        return False
    except Exception as e:
        st.warning(f"Fehler beim Lesen der CSV: {e}")
        return False

  def get_name_from_email(self):
    try:
        temp = self.benutzer
        temp = temp.split("@")[0]
        Vorname = temp.split(".")[0]
        Nachname = temp.split(".")[1]
        return Vorname.capitalize(), Nachname.capitalize()
    except IndexError:
        return None, None  # Falls das Format nicht passt

  def get_user_id(self):
    try:
        csv_path = f"{self.page}.csv"
        email = self.benutzer
        passwort = self.passwort
        df = pd.read_csv(csv_path)

        # Suche nach passender Kombination aus E-Mail und Passwort
        match = df[(df["Login-Email"] == email) & (df["Login-Passwort"] == passwort)]

        if not match.empty:
            return match.iloc[0]["ID"]  # gib erste gefundene ID zurück
        else:
            return None
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {csv_path}")
        return None
    except Exception as e:
        print(f"Fehler beim Lesen: {e}")
        return None

class Welcome(Seite):
  def __init__(self, user, daten, postfach, page, login):
    Seite.__init__(self, user, daten, postfach, page, login)
    self.page = "Welcome"

  def showPostfachBox(self):
    print("Hello my name is " + self.name)

class Events(Seite):
  def __init__(self, user, daten, postfach, page, login):
    Seite.__init__(self, user, daten, postfach, page, login)
    self.page = "Events"

class News(Seite):
  def __init__(self, user, daten, postfach, page, login):
    Seite.__init__(self, user, daten, postfach, page, login)
    self.page = "News"

class Patienten(Seite):
  def __init__(self, user, daten, postfach, page, login, Tagebuch, Medikamente, Werte):
    Seite.__init__(self, user, daten, postfach, page, login)
    self.page = "Patienten"
  def setTagebuch(self, Tagebuch):
    self.Tagebuch = Tagebuch
  def getTagebuch(self):
    return self.Tagebuch
  def alarmWerte(self):
    print("Alarm")
  def notificationChangeLocation(self):
    print("Location changed")
  def notificationDied(self):
    print("Gestorben")

class Mitarbeiter(Seite):
  def __init__(self, user, daten, postfach, page, login):
    Seite.__init__(self, user, daten, postfach, page, login)
    self.page = "Mitarbeiter"
  def setPatient(self, Patienten):
    print("Patienten")
  def notificationNoWorker(self):
    print("NoWorker")
  def proofEnoughWorker(self):
    print("ProofEnoughWorker")

class Heime(Seite):
  def __init__(self, user, daten, postfach, page, login):
    Seite.__init__(self, user, daten, postfach, page, login)
    self.page = "Heime"
  def notificationFullHeime(self):
    print("FullHeime")
  def proofEnoughHeime(self):
    print("ProofEnoughHeime")

#--------------------------------------------------------------------------------------------
class Postfach:
  def __init__(self, user, postfachInhalt):
    self.user = user                        # Rolle
    self.postfachInhalt = postfachInhalt

  def searchUserVornameNachname(self):
    ID = self.user
    Vorname = ""
    Nachname = ""


    return Vorname, Nachname

  def searchUserID(self, Name):
    Vorname = Name.split(" ")[0]
    Nachname = Name.split(" ")[1]
    ID = ""

    return ID

  def setNachricht(self):
    Datum = datetime.strftime("%m/%d/%Y")
    Uhrzeit = datetime.strptime("%H:%M:%S")
    Von = self.user #User-ID
    Vorname, Nachname = self.searchUserVornameNachname()

    An = st.text_input("An: ", placeholder="Erika Mustermann", value="")
    Nachricht = st.text_input("Nachricht: ", placeholder="Mein Text an dich.", value="")

    df = {("Datum",Datum), ("Uhrzeit",Uhrzeit), ("Von_ID",Von), ("An_ID",An), ("Nachricht",Nachricht)}

    if An & Nachricht != "":
      Name = "Postfach"
      #engine = msql.connect()
      # In DB schreiben
      #if msql.writeStringtoDB(df, engine, Name):
        #st.success("Die Nachricht wurde erfolgreich versendet.")
      #else:
        #st.warning("Die Nachricht konnte nicht erfolgreich versendet werden.")

  def getNachricht(self):
    print("Hello my name is " + self.name)
  def showPostfachBox(self):
    print("Hello my name is " + self.name)

#--------------------------------------------------------------------------------------------
class User:
  def __init__(self, person, rubrik, daten, rolle):
    self.person = person
    self.rubrik = rubrik
    self.daten = daten
    self.rolle = rolle

  def setRolle(self, rolle):
    self.rolle = rolle #true or false
  def getRolle(self):
    return self.rolle
  def getData(self):
    print("Hello my name is " + self.name)

class Verwaltung(User):
  def __init__(self, person, daten, rolle):
    User.__init__(self, person, daten, rolle)
    self.rubrik = "Verwaltung"

class Angehoerige(User):
  def __init__(self, person, daten, rolle):
    User.__init__(self, person, daten, rolle)
    self.rubrik = "Angehoerige"

class sozialerDienst(User):
  def __init__(self, person, daten, rolle):
    User.__init__(self, person, daten, rolle)
    self.rubrik = "Sozialer Dienst"


#--------------------------------------------------------------------------------------------
class Datenbank:
  def __init__(self, df, abschnitt, data):
    self.df = df                          # Datenframe
    self.abschnitt = abschnitt            # Name des Abschnittes (Events oder News oder .. )
    self.data = data                      # noch unklar ???

  # CSV laden
  def getData(self):
    try:
      path = f"{self.abschnitt}.csv"
      self.df = pd.read_csv(path)
      #st.success(f"CSV-Datei '{path}' erfolgreich geladen.")
      return self.df
    except FileNotFoundError:
      st.error(f"Datei '{path}' nicht gefunden.")
      return pd.DataFrame()

  # CSV anzeigen & bearbeiten
  def showData(self):
    Name = f"{self.abschnitt}_table"
    if self.df.empty:
      st.warning("Keine Daten zum Anzeigen.")
      return self.df
    st.write("Vorschau und Bearbeitung der CSV-Daten:")
    edited_df = st.data_editor(
      self.df,
      use_container_width=True,
      num_rows="dynamic",
      key=Name,
    )
    return edited_df

  # CSV speichern
  def saveData(self):
    try:
      df = self.df
      path = f"{self.abschnitt}.csv"
      df.to_csv(path, index=False)
      st.success(f"CSV-Datei wurde erfolgreich gespeichert unter: {path}")
    except Exception as e:
      st.error(f"Fehler beim Speichern: {e}")

  def get_next_id(self, prefix):
    existing = self.df["Veranstaltungsnummer"].dropna().astype(str)
    filtered = [v for v in existing if v.startswith(prefix) and v[len(prefix):].isdigit()]
    numbers = [int(v[len(prefix):]) for v in filtered]
    next_num = max(numbers, default=0) + 1
    return f"{prefix}{next_num:04d}"  # z. B. E0007


  def selectData(self):
        st.write(f"Ausgewählte Zeilen zum Löschen: ")
        # Hier könntest du deleteData(selected_rows) aufrufen
        # eine Zeile -> ein Heim oder ein Patient
  def changeData(self):
    print("Hello my name is " + self.name)
      #code von Nech
  def deleteData(self):
    table = self.getData()
    st.session_state.df = pd.DataFrame(columns=st.session_state.df.columns)
    st.session_state.df_prev = st.session_state.df.copy()
    st.rerun()
      #code von Aleks




class MedikamenteDB(Datenbank):
  def __init__(self, df, abschnitt, data):
    #df = CSV Daten
    #abschnitt = Name, bsp: "Medikamente.csv"
    #data = ...
    Datenbank.__init__(self, df, abschnitt, data)
    self.abschnitt = "Medikamente"

class LoginDB(Datenbank):
  def __init__(self, df, abschnitt, data):
    Datenbank.__init__(self, df, abschnitt, data)
    self.abschnitt = "Login"

class TagebuchDB(Datenbank):
  def __init__(self, df, abschnitt, data):
    Datenbank.__init__(self, df, abschnitt, data)
    self.abschnitt = "Tagebuch"

class PatientenDB(Datenbank):
  def __init__(self, df, abschnitt, data):
    Datenbank.__init__(self, df, abschnitt, data)
    self.abschnitt = "Patienten"

class WerteDB(Datenbank):
  def __init__(self, df, abschnitt, data, Gesundheitsparameter):
    Datenbank.__init__(self, df, abschnitt, data)
    self.abschnitt = "Werte"
  def getSensorData(self):
    print("Sensorwerte")
  def setSensorData(self):
    print("Sensorwerte")

class HeimeDB(Datenbank):
  def __init__(self, df, abschnitt, data):
    Datenbank.__init__(self, df, abschnitt, data)
    self.abschnitt = "Heime"

class MitarbeiterDB(Datenbank):
  def __init__(self, df, abschnitt, data):
    Datenbank.__init__(self, df, abschnitt, data)
    self.abschnitt = "Mitarbeiter"

class AngehoerigeDB(Datenbank):
  def __init__(self, df, abschnitt, data):
    Datenbank.__init__(self, df, abschnitt, data)
    self.abschnitt = "Angehoerige"

class EventsDB(Datenbank):
  def __init__(self, df, abschnitt, data):
    Datenbank.__init__(self, df, abschnitt, data)
    self.abschnitt = "Events"

class NewsDB(Datenbank):
  def __init__(self, df, abschnitt, data):
    Datenbank.__init__(self, df, abschnitt, data)
    self.abschnitt = "News"

class PostfachDB(Datenbank):
  def __init__(self, df, abschnitt, data):
    Datenbank.__init__(self, df, abschnitt, data)
    self.abschnitt = "Postfach"


#--------------------------------------------------------------------------------------------
class Gesundheitsparamater:
  def __init__(self, blutwerte, blutdruck, puls, atmung, temperatur, blutzucker, sturz):
    self.blutwerte = blutwerte
    self.blutdruck = blutdruck
    self.puls = puls
    self.atmung = atmung
    self.temperatur = temperatur
    self.blutzucker = blutzucker
    self.sturz = sturz

  def getData(self):
    print("Hello my name is " + self.name)

  def setData(self):
    print("Hello my name is " + self.name)

  def getSturz(self):
    print("Hello my name is " + self.name)

  def deleteData(self):
    print("Delete my data")

  def setSturz(self):
    print("Delete my data")


#------------------------------------------------------------------------------------
# Allgemeine Funktionen
#------------------------------------------------------------------------------------

def get_next_ID(self):
  columns = self.df.columns
  ID_str = str(columns[0])
  # Hole alle bestehenden Nummern aus der Spalte
  existing = self.df[ID_str].dropna().astype(str)
  st.write(existing)

  # Extrahiere nur die numerischen Teile (z. B. "V001" → 1)
  numbers = [int(v[1:]) for v in existing if v.startswith("V") and v[1:].isdigit()]

  # Finde das Maximum + 1
  next_num = max(numbers, default=0) + 1

  # Formatiere es mit führenden Nullen (z. B. 4 → "V004")
  return f"V{next_num:03d}"