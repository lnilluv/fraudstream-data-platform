import importlib
import os
import sys
import unittest
from pathlib import Path


FASTAPI_APP_ROOT = Path(__file__).resolve().parents[1] / "confluent" / "containers" / "app" / "fastapi"
if str(FASTAPI_APP_ROOT) not in sys.path:
    sys.path.insert(0, str(FASTAPI_APP_ROOT))


class FastApiConfigUrlTests(unittest.TestCase):
    def test_settings_uses_pydantic_v2_model_config(self):
        os.environ["DATABASE_URL"] = "postgresql://app_user:secret@postgresdb:5432/fraud_detection"

        config = importlib.import_module("app.config")
        config = importlib.reload(config)

        self.assertTrue(hasattr(config.Settings, "model_config"))

    def test_builds_async_and_sync_db_urls_from_database_url(self):
        os.environ["DATABASE_URL"] = "postgresql://app_user:secret@postgresdb:5432/fraud_detection"

        config = importlib.import_module("app.config")
        config = importlib.reload(config)

        self.assertEqual(
            config.settings.async_db_url,
            "postgresql+asyncpg://app_user:secret@postgresdb:5432/fraud_detection",
        )
        self.assertEqual(
            config.settings.sync_db_url,
            "postgresql+psycopg2://app_user:secret@postgresdb:5432/fraud_detection",
        )


if __name__ == "__main__":
    unittest.main()
