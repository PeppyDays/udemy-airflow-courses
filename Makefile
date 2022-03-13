export AIRFLOW_HOME=${PWD}

airflow-install:
	./install-airflow.sh

airflow-up:
	airflow standalone

pg-up:
	docker run --name airflow-metastore -p 5432:5432 -e POSTGRES_PASSWORD=welcome -d postgres

pg-down:
	docker rm airflow-metastore -f -v

pg-status:
	docker ps -f name=airflow-metastore
