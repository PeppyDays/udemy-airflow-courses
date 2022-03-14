from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from elasticsearch_plugin.hooks.elasticsearch_hook import ElasticsearchHook


def _print_es_info():
    hook = ElasticsearchHook()
    print(hook.info())


with DAG(
    dag_id="elasticsearch_dag",
    schedule_interval="@daily",
    start_date=datetime(2022, 1, 1),
    catchup=False,
    default_args={},
) as dag:
    print_es_info = PythonOperator(
        task_id="print_es_info",
        python_callable=_print_es_info,
    )
