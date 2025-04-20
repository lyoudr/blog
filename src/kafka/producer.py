from kafka import KafkaProducer, KafkaConsumer
import json
import time

TOPIC_NAME = "corning"
BOOTSTRAP_SERVERS = "localhost:9092"


def producer():
    # Kafka producer initialize
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    # Read local json file
    with open("/Users/annmac/Code/Ann/mind/static/billing.json", "r") as file:
        billing_data = json.load(file)

    # Loop through each billing data, send it to Kafka
    for record in billing_data:
        producer.send("corning", record)
        time.sleep(1)

    producer.flush()
    producer.close()


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
    producer()
