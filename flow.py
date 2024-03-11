import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="my_dag_name",
    start_date=datetime.datetime(2021, 1, 1),
    schedule=datetime.timedelta(minutes=1),
    catchup=False
):
    EmptyOperator(task_id="task")