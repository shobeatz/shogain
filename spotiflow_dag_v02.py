# from imports import *
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
# from airflow.operators.empty import EmptyOperator
# from pathlib import Path
from spotify_load_v02 import spotiflow_main


# Default parameters for the workflow
default_args = {
    'depends_on_past': False,
    'owner': 'airflow',
    'start_date': datetime(2024, 4, 7),            # always make this one dat before today
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
        'spotiflow_dag',                            # Name of the DAG / workflow
        default_args=default_args,
        # catchup=False,
        description='Runs Spotiflow everyday',
        schedule='5 12 * * *'                      # cron job for scheduling in UTC
)

run_spotiflow = PythonOperator(
        task_id='spotiflow_v02',                     # could be anything
        python_callable=spotiflow_main,             # main function of py file
        dag=dag
)

run_spotiflow