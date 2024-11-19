from airflow import DAG
from airflow.operators.python import PythonOperator  
from datetime import datetime
import os

dag_folder = os.path.dirname(os.path.abspath(__file__))
scripts_folder = os.path.join(dag_folder, "../scripts")
script_path = os.path.join(scripts_folder, "Daten in PostgreSQL.py")

def ingest_to_postgres():
    os.system(f"python \"{script_path}\"")  

with DAG('data_ingestion_postgres_dag', start_date=datetime(2024, 1, 1), schedule_interval='@hourly', catchup=False) as dag:
    postgres_ingestion = PythonOperator(
        task_id='postgres_ingestion',
        python_callable=ingest_to_postgres
    )
