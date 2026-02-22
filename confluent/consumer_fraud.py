import json
import os
import time

import pandas as pd
import requests
from confluent_kafka import Consumer, Producer
from joblib import load as load_joblib

import ccloud_lib
from kafka_runtime import build_consumer_config, build_producer_config, get_topic_names

# Initialize configurations from "python.config" file
KAFKA_CONFIG_FILE = os.getenv("KAFKA_CONFIG_FILE", "python.config")
CONF = ccloud_lib.read_ccloud_config(KAFKA_CONFIG_FILE)
TOPIC_NAMES = get_topic_names(os.getenv("KAFKA_MAIN_TOPIC", "fraud_detection.v1"))

consumer_conf = build_consumer_config(
    ccloud_lib.pop_schema_registry_params_from_config(CONF),
    group_id=os.getenv("KAFKA_CONSUMER_GROUP", "fraud_detection_consumer"),
)
consumer = Consumer(consumer_conf)
dlq_producer = Producer(build_producer_config(ccloud_lib.pop_schema_registry_params_from_config(CONF)))

# Subscribe to topic
consumer.subscribe([TOPIC_NAMES.main])

model = load_joblib("model_xg_new.joblib")
preprocessor = load_joblib("preprocessor.pkl")

# dataframe
df = pd.DataFrame(columns=["data"])

# discord webhook
webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

def send_to_dlq(raw_message: str, reason: str) -> None:
    payload = json.dumps({"reason": reason, "message": raw_message})
    dlq_producer.produce(TOPIC_NAMES.dlq, value=payload)
    dlq_producer.flush(5)


try:
    while True:
        msg = consumer.poll(1.0)
        print("Message")
        print(msg)
        if msg is None:
            print("Waiting for message or event/error in poll()")
            continue
        elif msg.error():
            print(f'error: {msg.error()}')
        else:
            raw_value = msg.value().decode("utf-8")
            try:
                record_key = msg.key()
                print("Record Key")
                print(record_key)
                record_value = json.loads(raw_value)
                df_cols = [
                    "cc_num",
                    "merchant",
                    "category",
                    "amt",
                    "first",
                    "last",
                    "gender",
                    "street",
                    "city",
                    "state",
                    "zip",
                    "lat",
                    "long",
                    "city_pop",
                    "job",
                    "dob",
                    "trans_num",
                    "merch_lat",
                    "merch_long",
                    "is_fraud",
                    "unix_time",
                ]
                df = pd.DataFrame.from_dict(record_value["data"], orient="columns")
                df.columns = df_cols
                df.drop("is_fraud", axis=1, inplace=True)
                df_transformed = preprocessor.transform(df)

                prediction = model.predict(df_transformed)
                prediction_value = int(prediction[0])

                if prediction_value == 0 and webhook_url:
                    print("Predicted fraud")
                    message = "A new transaction has been flagged as fraudulent. Call the FBI."
                    headers = {"Content-Type": "application/json"}
                    payload = {"content": message}
                    requests.post(webhook_url, headers=headers, json=payload, timeout=10)

                consumer.commit(message=msg, asynchronous=False)
            except Exception as exc:
                send_to_dlq(raw_value, str(exc))
                consumer.commit(message=msg, asynchronous=False)

            time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    dlq_producer.flush()
    consumer.close()
