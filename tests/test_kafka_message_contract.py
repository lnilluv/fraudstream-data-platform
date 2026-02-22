import unittest

from confluent.message_contract import validate_transaction_payload


class KafkaMessageContractTestCase(unittest.TestCase):
    def test_validate_accepts_payload_with_required_keys(self) -> None:
        payload = {
            "data": {
                "trans_num": ["abc"],
                "unix_time": [123],
                "cc_num": ["1234"],
                "amt": [42.5],
                "is_fraud": [0],
            }
        }
        validate_transaction_payload(payload)

    def test_validate_rejects_missing_data_root(self) -> None:
        with self.assertRaises(ValueError):
            validate_transaction_payload({"unexpected": {}})

    def test_validate_rejects_missing_required_columns(self) -> None:
        payload = {
            "data": {
                "trans_num": ["abc"],
                "unix_time": [123],
            }
        }
        with self.assertRaises(ValueError):
            validate_transaction_payload(payload)


if __name__ == "__main__":
    unittest.main()
