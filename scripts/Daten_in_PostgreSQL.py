from confluent_kafka import Consumer, KafkaError
import psycopg2
import json
import os
from dotenv import load_dotenv

# Speicherort des aktuellen Skripts
script_dir = os.path.dirname(os.path.abspath(__file__))

# Pfad zur .env-Datei relativ zum Skript
env_path = os.path.join(script_dir, '.env')

# Environment variables .env file
load_dotenv(dotenv_path=env_path)

# Debugging
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Estudiar1")
POSTGRES_DB = os.getenv("POSTGRES_DB", "olympic_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")

print(f"User: {POSTGRES_USER}, Password: {POSTGRES_PASSWORD}, DB: {POSTGRES_DB}, Host: {POSTGRES_HOST}")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")

# Kafka-Consumer-Konfiguration
conf = {
    'bootstrap.servers': "localhost:9092",
    'group.id': "consumer_group_1",
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['olympic_athletes_topic', 'olympic_hosts_topic', 'olympic_medals_topic', 'olympic_results_topic'])

# PostgreSQL-Verbindung
conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST
)
cur = conn.cursor()

# Funktion zum Erstellen der Tabellen, falls sie nicht existieren
def create_tables_if_not_exist():
    tables = {
        'olympic_hosts': """
            CREATE TABLE IF NOT EXISTS olympic_hosts (
                game_slug VARCHAR(100),
                game_end_date TIMESTAMP,
                game_start_date TIMESTAMP,
                game_location VARCHAR(100),
                game_name VARCHAR(100),
                game_season VARCHAR(10),
                game_year INT
            );
        """,
        'olympic_medals': """
            CREATE TABLE IF NOT EXISTS olympic_medals (
                discipline_title VARCHAR(100),
                slug_game VARCHAR(100),
                event_title VARCHAR(100),
                event_gender VARCHAR(10),
                medal_type VARCHAR(10),
                participant_type VARCHAR(50),
                participant_title VARCHAR(100),
                athlete_url TEXT,
                athlete_full_name VARCHAR(100),
                country_name VARCHAR(100),
                country_code VARCHAR(10)
            );
        """,
        'olympic_results': """
            CREATE TABLE IF NOT EXISTS olympic_results (
                discipline_title VARCHAR(100),
                slug_game VARCHAR(100),
                event_title VARCHAR(100),
                event_gender VARCHAR(10),
                event_unit_title VARCHAR(100),
                event_unit_gender VARCHAR(10),
                event_status VARCHAR(50),
                event_unit_medal BOOLEAN,
                event_unit_start_date TIMESTAMP,
                event_unit_end_date TIMESTAMP
            );
        """,
        'olympic_athletes': """
            CREATE TABLE IF NOT EXISTS olympic_athletes (
                athlete_url TEXT,
                athlete_full_name VARCHAR(100),
                games_participations INT,
                first_game VARCHAR(100),
                athlete_year_birth INT,
                athlete_medals VARCHAR(100),
                bio TEXT
            );
        """
    }

    for table_name, create_query in tables.items():
        try:
            cur.execute(create_query)
            conn.commit()
            print(f"Tabelle {table_name} erstellt oder existiert bereits.")
        except Exception as e:
            print(f"Fehler beim Erstellen der Tabelle {table_name}: {e}")
            conn.rollback()

# Rufe die Funktion auf, um alle Tabellen zu erstellen
create_tables_if_not_exist()

# Funktion zum Einfügen der Daten in PostgreSQL, je nach Thema
def insert_into_postgresql(data, topic):
    try:
        if topic == 'olympic_hosts_topic':
            insert_query = """
            INSERT INTO olympic_hosts (game_slug, game_end_date, game_start_date, game_location, game_name, game_season, game_year) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(insert_query, (
                data.get('game_slug'),
                data.get('game_end_date'),
                data.get('game_start_date'),
                data.get('game_location'),
                data.get('game_name'),
                data.get('game_season'),
                data.get('game_year')
            ))

        elif topic == 'olympic_medals_topic':
            insert_query = """
            INSERT INTO olympic_medals (discipline_title, slug_game, event_title, event_gender, medal_type, participant_type, participant_title, athlete_url, athlete_full_name, country_name, country_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(insert_query, (
                data.get('discipline_title'),
                data.get('slug_game'),
                data.get('event_title'),
                data.get('event_gender'),
                data.get('medal_type'),
                data.get('participant_type'),
                data.get('participant_title'),
                data.get('athlete_url'),
                data.get('athlete_full_name'),
                data.get('country_name'),
                data.get('country_code')
            ))

        elif topic == 'olympic_results_topic':
            insert_query = """
            INSERT INTO olympic_results (discipline_title, slug_game, event_title, event_gender, event_unit_title, event_unit_gender, event_status, event_unit_medal, event_unit_start_date, event_unit_end_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(insert_query, (
                data.get('discipline_title'),
                data.get('slug_game'),
                data.get('event_title'),
                data.get('event_gender'),
                data.get('event_unit_title'),
                data.get('event_unit_gender'),
                data.get('event_status'),
                data.get('event_unit_medal'),
                data.get('event_unit_start_date'),
                data.get('event_unit_end_date')
            ))

        elif topic == 'olympic_athletes_topic':
            insert_query = """
            INSERT INTO olympic_athletes (athlete_url, athlete_full_name, games_participations, first_game, athlete_year_birth, athlete_medals, bio)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(insert_query, (
                data.get('athlete_url'),
                data.get('athlete_full_name'),
                data.get('games_participations'),
                data.get('first_game'),
                data.get('athlete_year_birth'),
                data.get('athlete_medals'),
                data.get('bio')
            ))

        conn.commit()
        print(f"Daten in Tabelle {topic} eingefügt.")
    except Exception as e:
        print(f"Fehler beim Einfügen in PostgreSQL: {e}")
        conn.rollback()

# Hauptfunktion zum Konsumieren und Verarbeiten der Kafka-Nachrichten
try:
    max_empty_polls = 5  
    empty_poll_count = 0

    while empty_poll_count < max_empty_polls:
        # Nachricht von Kafka abholen
        msg = consumer.poll(timeout=5.0)
        if msg is None:
            print("Keine Nachrichten empfangen.")
            empty_poll_count += 1
            continue
        if msg.error():
            print(f"Kafka-Fehler: {msg.error()}")
            break

        # Reset empty_poll_count 
        empty_poll_count = 0

        # Nachricht dekodieren und JSON parsen
        try:
            data = msg.value().decode('utf-8')
            topic = msg.topic()  # Das Thema der empfangenen Nachricht

            # Debugging: Ausgabe der empfangenen Nachricht
            print(f"Empfangene Nachricht aus {topic}: {data}")

            # JSON in ein Python-Dictionary umwandeln
            parsed_data = json.loads(data)

            # Debugging: Struktur der empfangenen Nachricht anzeigen
            print(f"Schlüssel der empfangenen Nachricht: {parsed_data.keys()}")

            # Daten in PostgreSQL einfügen, je nach Kafka-Topic
            insert_into_postgresql(parsed_data, topic)

        except json.JSONDecodeError as e:
            print(f"Fehler beim Parsen der JSON-Daten: {e}")

    print("Beende das Skript: Alle Nachrichten verarbeitet oder keine neuen Nachrichten mehr verfügbar.")

except KeyboardInterrupt:
    print("Skript durch Benutzer gestoppt.")

finally:
    # Kafka-Consumer und PostgreSQL-Verbindung schließen
    consumer.close()
    cur.close()
    conn.close()
