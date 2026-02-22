import importlib
import os
import sys
import unittest
from pathlib import Path


FASTAPI_APP_ROOT = Path(__file__).resolve().parents[1] / "confluent" / "containers" / "app" / "fastapi"
if str(FASTAPI_APP_ROOT) not in sys.path:
    sys.path.insert(0, str(FASTAPI_APP_ROOT))


class FastApiDbApiTests(unittest.TestCase):
    def test_db_module_exposes_async_database_api(self):
        os.environ["DATABASE_URL"] = "postgresql://app_user:secret@postgresdb:5432/fraud_detection"

        db = importlib.import_module("app.db")
        db = importlib.reload(db)

        self.assertTrue(callable(db.init_db))
        self.assertTrue(callable(db.get_users))
        self.assertTrue(callable(db.get_or_create_user))
        self.assertEqual(db.User.__tablename__, "users")


if __name__ == "__main__":
    unittest.main()
