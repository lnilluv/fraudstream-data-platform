# FraudStream Data Platform

Production-oriented fraud detection data platform with Kafka ingestion, lakehouse analytics, data contracts, orchestration, and observability.

## What This Project Includes

- **Realtime ingestion layer:** Kafka producer/consumer flow with reliability defaults and retry/DLQ topic conventions.
- **Serving stack:** FastAPI app, Streamlit UI, and MLflow tracking service in Docker Compose.
- **Lakehouse foundation:** MinIO object storage + Trino query engine + Iceberg catalog configuration.
- **Analytics transforms:** dbt project with Bronze source, Silver staging model, and Gold fraud fact model.
- **Quality controls:** Payload contract validation in the consumer and dbt source freshness/model tests.
- **Orchestration:** Airflow DAG stages for ingest -> dbt build -> quality gate -> scoring.
- **Observability:** Prometheus, Grafana, Loki, Promtail, Node Exporter, and Kafka Exporter profile.
- **Ops hardening:** Runbooks and CI pipeline checks for unit tests + Compose configuration validation.

## End-to-End Flow

```text
External Kafka topic (fraud_detection.v1)
  -> Consumer validation + retry/DLQ routing
  -> Bronze lakehouse table (Iceberg on MinIO)
  -> dbt Silver model (normalized transactions)
  -> dbt Gold model (fraud scoring fact)
  -> Airflow orchestration and quality gates
  -> Serving/API/analytics consumers
```

## Repository Highlights

- `src/`: Hexagonal core (domain/application logic)
- `confluent/`: Kafka adapters and runtime contract checks
- `orchestration/airflow/dags/`: Airflow pipeline DAG
- `analytics/dbt/`: dbt project, sources, Silver/Gold models
- `deploy/compose/`: Docker Compose stack + lakehouse + observability configs
- `docs/ops/`: Runbooks (`pipeline-runbook.md`, `dlq-replay.md`)
- `.github/workflows/pipeline-quality.yml`: baseline CI quality gate

## Quick Start

### 1) Prerequisites

- Docker + Docker Compose
- Python 3.12+ for local tests
- External Kafka cluster credentials in `confluent/python.config`

Create your Kafka config from the example:

```bash
cp confluent/python.config.example confluent/python.config
```

### 2) Set environment variables

At minimum, define database and platform values used by Compose:

```bash
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_DB=fraud

export MYSQL_DATABASE=mlflowdb
export MYSQL_USER=mlflow
export MYSQL_PASSWORD=mlflow
export MYSQL_ROOT_PASSWORD=root

export AIRFLOW_FERNET_KEY=replace-with-a-real-key
export AIRFLOW_ADMIN_USERNAME=admin
export AIRFLOW_ADMIN_PASSWORD=admin
export AIRFLOW_UID=$(id -u)

export AWS_ACCESS_KEY_ID=dummy
export AWS_SECRET_ACCESS_KEY=dummy
export MLFLOW_TRACKING_URI=http://mlflow:5000

export MINIO_ROOT_USER=minioadmin
export MINIO_ROOT_PASSWORD=minioadmin
export LAKEHOUSE_BUCKET=lakehouse
export KAFKA_BOOTSTRAP_SERVERS=your-kafka-bootstrap:9092
```

### 3) Start base platform

```bash
docker compose -f deploy/compose/docker-compose.yml up -d postgresdb mysqldb fastapi mlflow streamlit kafka_worker
```

### 4) Start optional profiles

Lakehouse:

```bash
docker compose -f deploy/compose/docker-compose.yml --profile lakehouse up -d minio trino
```

Observability:

```bash
docker compose -f deploy/compose/docker-compose.yml --profile observability up -d
```

Airflow:

```bash
docker compose -f deploy/compose/docker-compose.yml --profile airflow up -d airflow-init airflow-webserver airflow-scheduler
```

Optional bucket bootstrap helper:

```bash
docker compose -f deploy/compose/docker-compose.yml --profile lakehouse-bootstrap up --abort-on-container-exit minio-init
```

## Operational Endpoints

- Airflow UI: `http://localhost:8080`
- Grafana: `http://localhost:3000`
- Prometheus: `http://localhost:9090`
- Loki API: `http://localhost:3100`
- MinIO API/Console: `http://localhost:9000` / `http://localhost:9001`
- Trino: `http://localhost:8081`

## Validation Commands

Run tests:

```bash
python3 -m unittest \
  tests/test_evaluate_transaction.py \
  tests/test_airflow_dag.py \
  tests/test_kafka_runtime.py \
  tests/test_lakehouse_layout.py \
  tests/test_dbt_project_scaffold.py \
  tests/test_kafka_message_contract.py
```

Validate Compose profiles:

```bash
docker compose -f deploy/compose/docker-compose.yml --profile observability --profile lakehouse config --services
```

## Architecture Note

Hexagonal architecture is preserved:

- **Domain/Application:** business logic remains framework-independent in `src/`.
- **Adapters:** Kafka, dbt/lakehouse, Airflow, and observability integrations are isolated in infrastructure-facing modules.
- **Composition root:** service wiring happens in `deploy/compose/docker-compose.yml`.

## Runbooks

- Pipeline operations: `docs/ops/pipeline-runbook.md`
- DLQ replay: `docs/ops/dlq-replay.md`
