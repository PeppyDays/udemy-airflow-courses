from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator

from subdags.sub_parallel_running import sub_parallel_running


with DAG(
    dag_id="parallel_running",
    schedule_interval="@daily",
    default_args={
        "start_date": datetime(2022, 1, 1),
        "catchup": False,
    },
) as dag:
    task_1 = BashOperator(task_id="task_1", bash_command="sleep 3")
    processing = SubDagOperator(
        task_id="processing_tasks",
        subdag=sub_parallel_running(
            parent_dag_id=dag.dag_id,
            child_dag_id="processing_tasks",
            default_args=dag.default_args,
        ),
    )
    task_4 = BashOperator(task_id="task_4", bash_command="sleep 3")

    task_1 >> processing >> task_4
