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

    class PythonOperator:  # type: ignore[override]
        def __init__(self, **_: object) -> None:
            pass

        def __rshift__(self, other: object) -> object:
            return other


PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.application.use_cases.evaluate_transaction import evaluate_transaction


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

run_scoring = PythonOperator(
    task_id="run_scoring",
    python_callable=run_fraud_scoring,
    dag=dag,
)
