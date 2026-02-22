from dataclasses import dataclass


@dataclass(frozen=True)
class TopicNames:
    main: str
    retry: str
    dlq: str


def get_topic_names(main_topic: str) -> TopicNames:
    return TopicNames(
        main=main_topic,
        retry=f"{main_topic}.retry",
        dlq=f"{main_topic}.dlq",
    )


def build_producer_config(base_config: dict[str, str]) -> dict[str, str]:
    config = dict(base_config)
    config.setdefault("enable.idempotence", "true")
    config.setdefault("acks", "all")
    config.setdefault("retries", "10")
    config.setdefault("retry.backoff.ms", "500")
    return config


def build_consumer_config(base_config: dict[str, str], group_id: str) -> dict[str, str]:
    config = dict(base_config)
    config["group.id"] = group_id
    config.setdefault("auto.offset.reset", "earliest")
    config.setdefault("enable.auto.commit", "false")
    return config
