from airflow import DAG
from airflow.operators import PythonOperator
from datetime import datetime
import os

def process_with_spark():
    os.system("python C:/Users/49176/batch_basierte_Datenarchitektur/Batch-Verarbeitung mit Apache Spark.py")

with DAG('batch_processing_spark_dag', start_date=datetime(2024, 1, 1), schedule_interval='@daily', catchup=False) as dag:
    spark_processing = PythonOperator(
        task_id='spark_processing',
        python_callable=process_with_spark
    )
