from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
except ImportError:  # pragma: no cover
    class DAG:  # type: ignore[override]
        def __init__(self, dag_id: str, **_: object) -> None:
            self.dag_id = dag_id
            self.task_dict: dict[str, object] = {}

    class PythonOperator:  # type: ignore[override]
        def __init__(self, task_id: str, dag: DAG, **_: object) -> None:
            self.task_id = task_id
            dag.task_dict[task_id] = self

        def __rshift__(self, other: object) -> object:
            return other


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.application.use_cases.evaluate_transaction import evaluate_transaction


def run_ingest_to_bronze() -> str:
    return "ingested"


def run_dbt_build() -> str:
    return "dbt_build_ok"


def validate_data_quality() -> str:
    return "quality_ok"


def run_fraud_scoring() -> str:
    prediction = evaluate_transaction(0)
    return prediction.value


dag = DAG(
    dag_id="fraud_scoring_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="*/15 * * * *",
    catchup=False,
    tags=["fraud", "streaming", "portfolio"],
)

ingest_kafka_to_bronze = PythonOperator(
    task_id="ingest_kafka_to_bronze",
    python_callable=run_ingest_to_bronze,
    dag=dag,
)

run_dbt_build_task = PythonOperator(
    task_id="run_dbt_build",
    python_callable=run_dbt_build,
    dag=dag,
)

validate_data_quality_task = PythonOperator(
    task_id="validate_data_quality",
    python_callable=validate_data_quality,
    dag=dag,
)

run_scoring = PythonOperator(
    task_id="run_scoring",
    python_callable=run_fraud_scoring,
    dag=dag,
)


ingest_kafka_to_bronze >> run_dbt_build_task >> validate_data_quality_task >> run_scoring
