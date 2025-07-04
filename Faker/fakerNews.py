from datetime import datetime, timedelta
import pandas as pd
from faker import Faker
import random


fake = Faker('de_DE')
Faker.seed(42)
random.seed(42)

def generate_news(n):
    news = []
    for _ in range(n):
        datum = fake.date_between(start_date='-30d', end_date='today')
        uhrzeit = fake.time(pattern="%H:%M")
        titel = fake.sentence(nb_words=6)
        text = fake.paragraph(nb_sentences=5)

        news.append({
            "Datum": datum.strftime("%Y-%m-%d"),
            "Uhrzeit": uhrzeit,
            "Titel": titel,
            "Text": text
        })
    return news


# Erzeuge 10 News-Datensätze
news_df = pd.DataFrame(generate_news(10))

# Speichern als CSV
news_csv_path = "/streamlit/News.csv"
news_df.to_csv(news_csv_path, index=False)

