import importlib.util
import pathlib
import unittest


class AirflowDagTestCase(unittest.TestCase):
    def test_fraud_pipeline_dag_id(self) -> None:
        dag_path = pathlib.Path("orchestration/airflow/dags/fraud_pipeline.py")
        spec = importlib.util.spec_from_file_location("fraud_pipeline", dag_path)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        self.assertEqual(module.dag.dag_id, "fraud_scoring_pipeline")

    def test_fraud_pipeline_has_expected_task_ids(self) -> None:
        dag_path = pathlib.Path("orchestration/airflow/dags/fraud_pipeline.py")
        spec = importlib.util.spec_from_file_location("fraud_pipeline", dag_path)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        task_ids = set(module.dag.task_dict.keys())
        self.assertSetEqual(
            task_ids,
            {
                "ingest_kafka_to_bronze",
                "run_dbt_build",
                "validate_data_quality",
                "run_scoring",
            },
        )


if __name__ == "__main__":
    unittest.main()
