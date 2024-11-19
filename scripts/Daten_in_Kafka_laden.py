import os
import pandas as pd
from confluent_kafka import Producer

# Kafka Producer Konfiguration
conf = {
    'bootstrap.servers': 'localhost:9092', 
    'client.id': 'olympic_data_producer'
}

# Initialisierung des Kafka-Producers
producer = Producer(conf)

# Funktion für das Lieferrückruf von Kafka-Nachrichten
def lieferbericht(err, msg):
    if err is not None:
        print(f'Nachrichtenzustellung fehlgeschlagen: {err}')
    else:
        print(f'Nachricht zugestellt an {msg.topic()} [{msg.partition()}]')

# Definiere den Pfad zum Verzeichnis, das die CSV-Dateien enthält
daten_verzeichnis = r'C:\Users\49176\batch_basierte_Datenarchitektur\olympic_data'

# Definiere das Kafka-Topic für jede Datei
dateien_themen = {
    'olympic_athletes.csv': 'olympic_athletes_topic',
    'olympic_hosts.csv': 'olympic_hosts_topic',
    'olympic_medals.csv': 'olympic_medals_topic',
    'olympic_results.csv': 'olympic_results_topic'
}

# Durchlaufe die Dateien und sende die Daten an Kafka
for datei_name, thema in dateien_themen.items():
    datei_pfad = os.path.join(daten_verzeichnis, datei_name)
    if os.path.isfile(datei_pfad):
        print(f'Datei wird verarbeitet: {datei_pfad}')
        df = pd.read_csv(datei_pfad)

        # Definiere die erwarteten Spalten für jedes Topic
        if thema == 'olympic_athletes_topic':
            expected_columns = ['athlete_url', 'athlete_full_name', 'games_participations', 'first_game', 'athlete_year_birth', 'athlete_medals', 'bio']
        elif thema == 'olympic_hosts_topic':
            expected_columns = ['game_slug', 'game_end_date', 'game_start_date', 'game_location', 'game_name', 'game_season', 'game_year']
        elif thema == 'olympic_medals_topic':
            expected_columns = ['discipline_title', 'slug_game', 'event_title', 'event_gender', 'medal_type', 'participant_type', 'participant_title', 'athlete_url', 'athlete_full_name', 'country_name', 'country_code']
        elif thema == 'olympic_results_topic':
            expected_columns = ['discipline_title', 'slug_game', 'event_title', 'event_gender', 'event_unit_title', 'event_unit_gender', 'event_status', 'event_unit_medal', 'event_unit_start_date', 'event_unit_end_date']

        # Fehlende Spalten mit Standardwerten auffüllen
        for column in expected_columns:
            if column not in df.columns:
                df[column] = None  # Setze fehlende Spalten auf None

        # Iteriere über die Zeilen und sende sie an Kafka
        for index, zeile in df.iterrows():
            nachricht = zeile.to_json()  # Konvertiere jede Zeile in das JSON-Format
            producer.produce(thema, key=str(index), value=nachricht, callback=lieferbericht)
            
            # Stelle sicher, dass der Producer gepollt wird, um Rückrufe zu bearbeiten und Pufferüberlauf zu vermeiden
            producer.poll(0)

            # Flush nach jeder 1000 Nachrichten, um Pufferüberlauf zu vermeiden
            if index % 1000 == 0:  # Flush nach jeder 1000. Nachricht
                producer.flush()

# Warten auf die Zustellung aller ausstehenden Nachrichten und Empfang der Lieferberichte
producer.flush()
