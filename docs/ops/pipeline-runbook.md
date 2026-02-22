# Pipeline Runbook

## Scope

This runbook covers the fraud data platform path:

1. Kafka ingestion
2. Bronze/Silver/Gold transformations
3. Airflow orchestration
4. Serving handoff to API/analytics consumers

## Daily Checks

1. Verify Airflow DAG state for `fraud_scoring_pipeline`.
2. Verify Kafka lag and DLQ metrics on Grafana dashboard `Fraud Pipeline Overview`.
3. Verify Trino and MinIO service health in Docker Compose.
4. Verify dbt model test status for Silver and Gold models.

## Incident Triage

1. Determine failure domain: Kafka, lakehouse, dbt contract, or Airflow orchestration.
2. If Kafka lag is growing, pause non-critical consumers and inspect consumer group offsets.
3. If dbt contracts fail, block promotion and inspect offending source fields.
4. If Airflow task fails, retry once; if repeated, open incident with failing task logs.

## Recovery Commands

```bash
python3 -m unittest tests/test_evaluate_transaction.py tests/test_airflow_dag.py tests/test_kafka_runtime.py tests/test_lakehouse_layout.py tests/test_dbt_project_scaffold.py tests/test_kafka_message_contract.py
docker compose -f deploy/compose/docker-compose.yml --profile observability --profile lakehouse config --services
```

## Escalation

- P1: end-to-end pipeline stopped for more than 30 minutes.
- P2: DLQ above baseline for more than 15 minutes.
- P3: non-blocking freshness warnings.
