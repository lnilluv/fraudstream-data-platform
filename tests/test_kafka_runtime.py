import unittest

from confluent.kafka_runtime import (
    build_consumer_config,
    build_producer_config,
    get_topic_names,
)


class KafkaRuntimeTestCase(unittest.TestCase):
    def test_get_topic_names_returns_main_retry_and_dlq(self) -> None:
        topic_names = get_topic_names("fraud_detection.v1")
        self.assertEqual(topic_names.main, "fraud_detection.v1")
        self.assertEqual(topic_names.retry, "fraud_detection.v1.retry")
        self.assertEqual(topic_names.dlq, "fraud_detection.v1.dlq")

    def test_build_producer_config_enables_reliability_defaults(self) -> None:
        config = build_producer_config({"bootstrap.servers": "example:9092"})
        self.assertEqual(config["enable.idempotence"], "true")
        self.assertEqual(config["acks"], "all")
        self.assertEqual(config["retries"], "10")
        self.assertEqual(config["retry.backoff.ms"], "500")

    def test_build_consumer_config_sets_manual_commit_strategy(self) -> None:
        config = build_consumer_config(
            {"bootstrap.servers": "example:9092"},
            group_id="fraud_detection_consumer",
        )
        self.assertEqual(config["group.id"], "fraud_detection_consumer")
        self.assertEqual(config["auto.offset.reset"], "earliest")
        self.assertEqual(config["enable.auto.commit"], "false")


if __name__ == "__main__":
    unittest.main()
