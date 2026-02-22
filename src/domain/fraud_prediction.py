from enum import Enum


class FraudPrediction(str, Enum):
    FRAUD = "fraud"
    LEGITIMATE = "legitimate"
