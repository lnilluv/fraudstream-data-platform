import unittest

from src.adapters.lakehouse.layout import dataset_uri, table_name


class LakehouseLayoutTestCase(unittest.TestCase):
    def test_dataset_uri_formats_bucket_and_zone(self) -> None:
        uri = dataset_uri("lakehouse", "bronze", "transactions")
        self.assertEqual(uri, "s3a://lakehouse/bronze/transactions")

    def test_table_name_formats_zone_and_dataset(self) -> None:
        self.assertEqual(table_name("silver", "fraud_scores"), "silver_fraud_scores")


if __name__ == "__main__":
    unittest.main()
