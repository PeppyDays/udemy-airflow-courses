from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup


with DAG(
    dag_id="parallel_running",
    start_date=datetime(2022, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args={},
) as dag:
    task_1 = BashOperator(task_id="task_1", bash_command="sleep 3")

    with TaskGroup("processing_tasks") as processing_tasks:
        task_2 = BashOperator(task_id="task_2", bash_command="sleep 3")
        task_3 = BashOperator(task_id="task_3", bash_command="sleep 3")

    task_4 = BashOperator(task_id="task_4", bash_command="sleep 3")

    task_1 >> processing_tasks >> task_4
