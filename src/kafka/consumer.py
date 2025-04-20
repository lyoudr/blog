from kafka import KafkaConsumer
import json
import time

TOPIC_NAME = "corning"
BOOTSTRAP_SERVERS = "localhost:9092"


def consumer():
    # Kafka consumer initialize
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="my-consumer-group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )
    print("Wating for messages...")
    for message in consumer:
        print(f"Received message: {message.value}")


if __name__ == "__main__":
    consumer()
