export AIRFLOW_HOME=${PWD}

airflow-home:
	export AIRFLOW_HOME=${PWD}

airflow-install:
	./install-airflow.sh

airflow-up:
	airflow scheduler -D
	airflow webserver -D

airflow-down:
	kill -9 $(shell cat airflow-scheduler.pid)
	rm -rf airflow-scheduler.*
	kill -9 $(shell cat airflow-webserver.pid)
	kill -9 $(shell cat airflow-webserver-monitor.pid)
	rm -rf airflow-webserver.*

airflow-logs:
	tail -f airflow-webserver.out airflow-scheduler.out

airflow-status:
	cat airflow-webserver.pid
	cat airflow-scheduler.pid

pg-up:
	docker run --name airflow-metastore -p 5432:5432 -e POSTGRES_PASSWORD=welcome -d postgres

pg-down:
	docker rm airflow-metastore -f -v

pg-logs:
	docker logs -f airflow-metastore

pg-status:
	docker ps -f name=airflow-metastore

redis-up:
	docker run --name airflow-queue -p 6379:6379 -d redis

redis-down:
	docker rm airflow-queue -f -v

redis-logs:
	docker logs -f airflow-queue

redis-status:
	docker ps -f name=airflow-queue

flower-up:
	airflow celery flower -D

flower-down:
	kill -9 $(shell cat airflow-flower.pid)
	rm -rf airflow-flower.*

flower-logs:
	tail -f airflow-flower.out

flower-status:
	cat airflow-flower.pid

worker-up:
	airflow celery worker -D

worker-down:
	kill -9 $(shell cat airflow-worker.pid)
	rm -rf airflow-worker.*

worker-logs:
	tail -f airflow-worker.out

worker-status:
	cat airflow-worker.pid

es-up:
	docker run --name airflow-es -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -d docker.elastic.co/elasticsearch/elasticsearch:7.17.1

es-down:
	docker rm airflow-es -f -v

es-logs:
	docker logs -f airflow-es

es-status:
	docker ps -f name=airflow-es
