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


if __name__ == "__main__":
    unittest.main()
