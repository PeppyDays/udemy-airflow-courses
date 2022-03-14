from typing import Any

from airflow.hooks.base import BaseHook

from elasticsearch import Elasticsearch


class ElasticsearchHook(BaseHook):
    es: Elasticsearch

    # the arguments users should give when instantiating
    def __init__(self, conn_id: str = "elasticsearch_default", *args, **kwargs):
        super().__init__(*args, **kwargs)

        conn = self.get_connection(conn_id)
        conn_info = {"hosts": [f"{conn.schema}://{host}:{conn.port}" for host in conn.host.split(",")]}
        if conn.login:
            conn_info["basic_auth"] = (conn.login, conn.password)
        self.es = Elasticsearch(**conn_info)

    def info(self):
        return self.es.info()

    def add_doc(self, index: str, document):
        res = self.es.index(index=index, document=document)
        return res

    def get_conn(self) -> Any:
        pass
