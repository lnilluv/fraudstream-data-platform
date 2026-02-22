import pathlib
import unittest


class DbtProjectScaffoldTestCase(unittest.TestCase):
    def test_dbt_project_file_exists(self) -> None:
        project_file = pathlib.Path("analytics/dbt/dbt_project.yml")
        self.assertTrue(project_file.exists())

    def test_silver_model_uses_bronze_source(self) -> None:
        silver_model = pathlib.Path("analytics/dbt/models/silver/stg_transactions.sql")
        self.assertTrue(silver_model.exists())
        self.assertIn("source('bronze', 'transactions_raw')", silver_model.read_text())

    def test_gold_model_uses_silver_reference(self) -> None:
        gold_model = pathlib.Path("analytics/dbt/models/gold/fct_fraud_scores.sql")
        self.assertTrue(gold_model.exists())
        self.assertIn("ref('stg_transactions')", gold_model.read_text())


if __name__ == "__main__":
    unittest.main()
