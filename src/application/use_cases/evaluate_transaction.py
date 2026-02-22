from src.domain.fraud_prediction import FraudPrediction


def evaluate_transaction(model_prediction: int) -> FraudPrediction:
    if model_prediction == 0:
        return FraudPrediction.FRAUD
    return FraudPrediction.LEGITIMATE
