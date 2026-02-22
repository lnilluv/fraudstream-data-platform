import json
import datetime
import os
import time

import requests
from confluent_kafka import Producer

import ccloud_lib
from kafka_runtime import build_producer_config, get_topic_names

# Initialize configurations from "python.config" file
KAFKA_CONFIG_FILE = os.getenv("KAFKA_CONFIG_FILE", "python.config")
CONF = ccloud_lib.read_ccloud_config(KAFKA_CONFIG_FILE)
TOPIC_NAMES = get_topic_names(os.getenv("KAFKA_MAIN_TOPIC", "fraud_detection.v1"))


# Create Producer instance
producer_conf = build_producer_config(ccloud_lib.pop_schema_registry_params_from_config(CONF))
producer = Producer(producer_conf)

# Create topics if they don't already exist
for topic_name in (TOPIC_NAMES.main, TOPIC_NAMES.retry, TOPIC_NAMES.dlq):
    ccloud_lib.create_topic(CONF, topic_name)

delivered_records = 0

# Callback called acked (triggered by poll() or flush())
# when a message has been successfully delivered or
# permanently failed delivery (after retries).
def acked(err, msg):
    global delivered_records
    # Delivery report handler called on successful or failed delivery of message
    if err is not None:
        print("Failed to deliver message: {}".format(err))
    else:
        delivered_records += 1
        print(
            "Produced record to topic {} partition [{}] @ offset {}".format(
                msg.topic(), msg.partition(), msg.offset()
            )
        )

try:
    while True:
        url = "https://real-time-payments-api.herokuapp.com/current-transactions"
        response = requests.get(url, timeout=10)
        transaction = json.loads(response.json())["data"]
        record_value = json.dumps({"data": transaction})
        record_key = str(datetime.datetime.now())
        print(record_key, record_value)

        # This will actually send data to your topic
        producer.produce(
            TOPIC_NAMES.main,
            key=record_key,
            value=record_value,
            on_delivery=acked,
        )
        producer.poll(0)
        time.sleep(12)

except KeyboardInterrupt:
    pass
finally:
    producer.flush()
