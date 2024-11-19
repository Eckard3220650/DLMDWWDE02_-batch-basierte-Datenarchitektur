from airflow import DAG
from airflow.operators import PythonOperator
from datetime import datetime
import os

def ingest_to_kafka():
    os.system("python C:/Users/49176/batch_basierte_Datenarchitektur/Daten in Kafka laden.py")

with DAG('data_ingestion_kafka_dag', start_date=datetime(2024, 1, 1), schedule_interval='@hourly', catchup=False) as dag:
    kafka_ingestion = PythonOperator(
        task_id='kafka_ingestion',
        python_callable=ingest_to_kafka
    )
