from typing import Any

from airflow.models import BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from elasticsearch_plugin.hooks.elasticsearch_hook import ElasticsearchHook

from contextlib import closing
import json


class PostgresToElasticsearchOperator(BaseOperator):
    sql: str
    index: str
    postgres_conn_id: str
    elasticsearch_conn_id: str

    def __init__(
        self,
        sql: str,
        index: str,
        postgres_conn_id: str = "postgres_default",
        elasticsearch_conn_id: str = "elasticsearch_default",
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.sql = sql
        self.index = index
        self.postgres_conn_id = postgres_conn_id
        self.elasticsearch_conn_id = elasticsearch_conn_id

    def execute(self, context: Any):
        es = ElasticsearchHook(conn_id=self.elasticsearch_conn_id)
        pg = PostgresHook(postgres_conn_id=self.postgres_conn_id)

        with closing(pg.get_conn()) as conn:
            with closing(conn.cursor()) as cur:
                cur.itersize = 1000
                cur.execute(self.sql)
                for row in cur:
                    document = json.dumps(row, indent=2)
                    es.add_doc(index=self.index, document=document)
