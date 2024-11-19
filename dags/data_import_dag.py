from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import os

# Dynamically calculate the path to the scripts folder
dag_folder = os.path.dirname(os.path.abspath(__file__))
scripts_folder = os.path.join(dag_folder, "../scripts")
script_path = os.path.join(scripts_folder, "Daten_Importieren.py")

def import_data():
    os.system(f"python {script_path}")

with DAG('data_import_dag', start_date=datetime(2024, 1, 1), schedule_interval='@daily', catchup=False) as dag:
    download_data = PythonOperator(
        task_id='download_data',
        python_callable=import_data
    )
