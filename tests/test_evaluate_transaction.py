import unittest

from src.application.use_cases.evaluate_transaction import evaluate_transaction
from src.domain.fraud_prediction import FraudPrediction


class EvaluateTransactionTestCase(unittest.TestCase):
    def test_labels_fraud_when_model_outputs_zero(self) -> None:
        prediction = evaluate_transaction(0)
        self.assertEqual(prediction, FraudPrediction.FRAUD)

    def test_labels_legitimate_when_model_outputs_one(self) -> None:
        prediction = evaluate_transaction(1)
        self.assertEqual(prediction, FraudPrediction.LEGITIMATE)


if __name__ == "__main__":
    unittest.main()
