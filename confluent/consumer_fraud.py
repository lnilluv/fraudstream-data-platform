# Example written based on the official 
# Confluent Kakfa Get started guide https://github.com/confluentinc/examples/blob/7.1.1-post/clients/cloud/python/consumer.py

import json
import pickle
import time
import os
from pickle import load

import pandas as pd
import requests
from confluent_kafka import Consumer
from joblib import load

import ccloud_lib

# from oauth2client.service_account import ServiceAccountCredentials

# Initialize configurations from "python.config" file
KAFKA_CONFIG_FILE = os.getenv("KAFKA_CONFIG_FILE", "python.config")
CONF = ccloud_lib.read_ccloud_config(KAFKA_CONFIG_FILE)
TOPIC = "fraud_detection" 

# Create Consumer instance
# 'auto.offset.reset=earliest' to start reading from the beginning of the
# topic if no committed offsets exist
consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(CONF)
consumer_conf['group.id'] = 'fraud_detection_consumer'
consumer_conf['auto.offset.reset'] = 'earliest' # This means that you will consume latest messages that your script haven't consumed yet!
consumer = Consumer(consumer_conf)

# Subscribe to topic
consumer.subscribe([TOPIC])

# jobmodel loading

# model = pickle.load(open("finalized_model.sav", 'rb'))

model = load("model_xg_new.joblib")

# dataframe 
df = pd.DataFrame(columns=["data"])

# discord webhook
webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

# Process messages
try:
    while True:
        msg = consumer.poll(1.0) # Search for all non-consumed events. It times out after 1 second
        print("Message")
        print(msg)
        if msg is None:
            # No message available within timeout.
            # Initial message consumption may take up to
            # `session.timeout.ms` for the consumer group to
            # rebalance and start consuming
            print("Waiting for message or event/error in poll()")
            continue
        elif msg.error():
            print(f'error: {msg.error()}')
        else:
            # Check for Kafka message
            record_key = msg.key()
            print("Record Key")
            print(record_key)
            record_value = json.loads(msg.value())
            df_cols = ['cc_num','merchant','category','amt','first','last','gender','street','city','state','zip','lat','long','city_pop','job','dob','trans_num','merch_lat','merch_long','is_fraud','unix_time']
            df = pd.DataFrame.from_dict(record_value["data"], orient='columns')
            df.columns = df_cols
            df.drop("is_fraud", axis=1, inplace=True)
            preprocessor = load("preprocessor.pkl")
            df_transformed = preprocessor.transform(df)

            # df.drop("is_fraud", axis=1, inplace=True)
            # df = df.drop(["is_fraud"], axis=1)

            print("Record Value")
            prediction = model.predict(df_transformed)
            

            if prediction == 0 and webhook_url:
                print("Predicted fraud")
                message = "A new transaction has been flagged as fraudulent. Call the FBI."
                headers = {"Content-Type": "application/json"}
                payload = {"content": message}
                response = requests.post(webhook_url, headers=headers, json=payload)

            time.sleep(0.5) # Wait half a second
except KeyboardInterrupt:
    pass
finally:
    # Leave group and commit final offsets
    consumer.close()
