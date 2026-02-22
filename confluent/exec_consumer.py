import os
import subprocess


container = os.getenv("KAFKA_WORKER_CONTAINER", "fraud_worker")
subprocess.run(["docker", "exec", "-it", container, "python", "consumer_fraud.py"], check=True)
