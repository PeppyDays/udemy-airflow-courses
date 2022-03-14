from datetime import datetime
from random import uniform

from airflow import DAG
from airflow.models import TaskInstance
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

default_args = {"start_date": datetime(2020, 1, 1)}


def _training_model(ti: TaskInstance):
    accuracy = uniform(0.1, 10.0)
    print(f"model's accuracy: {accuracy}")
    # this will register the return value into XCom automatically
    # return accuracy
    # this will register the return value into XCom as you set
    ti.xcom_push(key="model_accuracy", value=accuracy)


def _choose_best_model(ti: TaskInstance):
    print("choose best model")
    accuracies = ti.xcom_pull(
        key="model_accuracy",
        task_ids=[
            "processing_tasks.training_model_a",
            "processing_tasks.training_model_b",
            "processing_tasks.training_model_c",
        ],
    )
    print(accuracies)


def _is_accurate():
    return "accurate"


with DAG(
    "xcom_dag", schedule_interval="@daily", default_args=default_args, catchup=False
) as dag:

    downloading_data = BashOperator(
        task_id="downloading_data",
        bash_command="sleep 3",
        do_xcom_push=False,
    )

    with TaskGroup("processing_tasks") as processing_tasks:
        training_model_a = PythonOperator(
            task_id="training_model_a", python_callable=_training_model
        )

        training_model_b = PythonOperator(
            task_id="training_model_b", python_callable=_training_model
        )

        training_model_c = PythonOperator(
            task_id="training_model_c", python_callable=_training_model
        )

    choose_model = PythonOperator(task_id="choose_model", python_callable=_choose_best_model)

    is_accurate = BranchPythonOperator(
        task_id="is_accurate",
        python_callable=_is_accurate
    )
    accurate = DummyOperator(task_id="accurate")
    inaccurate = DummyOperator(task_id="inaccurate")

    downloading_data >> processing_tasks >> choose_model
    choose_model >> is_accurate >> [accurate, inaccurate]
