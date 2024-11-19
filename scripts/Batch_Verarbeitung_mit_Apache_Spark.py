from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType
import os

# Kafka-Server aus Umgebungsvariablen (Standardwert für Docker ist kafka:29092)
kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# Debugging: Log the Kafka bootstrap servers
print(f"Using Kafka bootstrap servers: {kafka_bootstrap_servers}")

# Schema für olympic_athletes_topic
athletes_schema = StructType() \
    .add("athlete_url", StringType()) \
    .add("athlete_full_name", StringType()) \
    .add("games_participations", StringType()) \
    .add("first_game", StringType()) \
    .add("athlete_year_birth", StringType()) \
    .add("athlete_medals", StringType()) \
    .add("bio", StringType())

# Schema für olympic_hosts_topic
hosts_schema = StructType() \
    .add("game_slug", StringType()) \
    .add("game_end_date", StringType()) \
    .add("game_start_date", StringType()) \
    .add("game_location", StringType()) \
    .add("game_name", StringType()) \
    .add("game_season", StringType()) \
    .add("game_year", StringType())

# Schema für olympic_medals_topic
medals_schema = StructType() \
    .add("discipline_title", StringType()) \
    .add("slug_game", StringType()) \
    .add("event_title", StringType()) \
    .add("event_gender", StringType()) \
    .add("medal_type", StringType()) \
    .add("participant_type", StringType()) \
    .add("participant_title", StringType()) \
    .add("athlete_url", StringType()) \
    .add("athlete_full_name", StringType()) \
    .add("country_name", StringType()) \
    .add("country_code", StringType())

# Schema für olympic_results_topic
results_schema = StructType() \
    .add("discipline_title", StringType()) \
    .add("slug_game", StringType()) \
    .add("event_title", StringType()) \
    .add("event_gender", StringType()) \
    .add("event_unit_title", StringType()) \
    .add("event_unit_gender", StringType()) \
    .add("event_status", StringType()) \
    .add("event_unit_medal", StringType()) \
    .add("event_unit_start_date", StringType()) \
    .add("event_unit_end_date", StringType())

# Spark Session erstellen
spark = SparkSession.builder \
    .appName("Kafka-Batch-Integration") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1") \
    .config("spark.hadoop.io.native.lib.available", "false") \
    .config("spark.hadoop.io.nativeio.nativeio", "false") \
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem") \
    .config("spark.hadoop.fs.hdfs.impl", "org.apache.hadoop.fs.HadoopFileSystem") \
    .config("spark.hadoop.fs.defaultFS", "file:///") \
    .getOrCreate()

print(f"Verarbeite Daten von Kafka-Broker: {kafka_bootstrap_servers}")

# Funktion zum Verarbeiten eines Batches
def process_batch(kafka_topic, schema):
    # Kafka-Themen dynamisch aus Umgebungsvariablen laden
    topic = os.getenv(f"TOPIC_{kafka_topic.upper()}", kafka_topic)

    # Read data from Kafka as a batch
    try:
        df = spark \
            .read \
            .format("kafka") \
            .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
            .option("subscribe", topic) \
            .load()

        # Convert Kafka data to a readable format (JSON)
        df = df.selectExpr("CAST(value AS STRING)")

        # Parse JSON data with the defined schema
        df = df.withColumn("jsonData", from_json(col("value"), schema))

        # Select the JSON columns you want to process
        df = df.select(col("jsonData.*"))

        # Show the output on the console (or perform any other actions, such as saving to a database)
        print(f"Batch data from topic '{topic}':")
        df.show(truncate=False)
    except Exception as e:
        print(f"Error processing Kafka topic '{kafka_topic}': {e}")

# Verarbeite Daten aus den definierten Topics
process_batch("olympic_athletes_topic", athletes_schema)
process_batch("olympic_hosts_topic", hosts_schema)
process_batch("olympic_medals_topic", medals_schema)
process_batch("olympic_results_topic", results_schema)

# Spark-Session nach Verarbeitung beenden
spark.stop()
