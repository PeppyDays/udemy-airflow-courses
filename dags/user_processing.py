import json
from datetime import datetime

from airflow.models import DAG
from airflow.models import TaskInstance
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.sqlite.operators.sqlite import SqliteOperator


def _processing_user(ti: TaskInstance):
    users = ti.xcom_pull(task_ids=["extracting_user"])

    if not users or "results" not in users[0]:
        raise ValueError("User is empty")

    import csv

    user = users[0]["results"][0]
    processed_user = {
        "first_name": user["name"]["first"],
        "last_name": user["name"]["last"],
        "country": user["location"]["country"],
        "user_name": user["login"]["username"],
        "password": user["login"]["password"],
        "email": user["email"],
    }

    with open("/tmp/processed_user.csv", "w") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "first_name",
                "last_name",
                "country",
                "user_name",
                "password",
                "email",
            ],
        )
        writer.writerow(processed_user)


with DAG(
    dag_id="user_processing",
    schedule_interval="@daily",
    start_date=datetime(2022, 1, 1),
    catchup=False,
    default_args={},
) as dag:
    creating_table = SqliteOperator(
        task_id="creating_table",
        sqlite_conn_id="sample_sqlite",
        sql="""
            CREATE TABLE IF NOT EXISTS users (
                email TEXT NOT NULL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                country TEXT NOT NULL,
                user_name TEXT NOT NULL,
                password TEXT NOT NULL
            );
        """,
    )
    is_api_available = HttpSensor(
        task_id="is_api_available",
        http_conn_id="user_api",
        endpoint="api/",
    )
    extracting_user = SimpleHttpOperator(
        task_id="extracting_user",
        http_conn_id="user_api",
        endpoint="api/",
        method="GET",
        response_filter=lambda r: json.loads(r.text),
        log_response=True,
    )
    processing_user = PythonOperator(
        task_id="processing_user",
        python_callable=_processing_user,
    )
    storing_user = BashOperator(
        task_id="storing_user",
        bash_command="""echo -e ".separator ","\n.import /tmp/processed_user.csv users" | sqlite3 /Users/youdongk/Documents/Code/Learning/learn-airflow/udemy/sample.db""",
    )

    creating_table >> extracting_user
    is_api_available >> extracting_user
    extracting_user >> processing_user >> storing_user
