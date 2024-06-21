from kafka import KafkaConsumer
import json

KAFKA_TOPIC = 'financial-data'
KAFKA_SERVER = 'localhost:9092'

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

for message in consumer:
    print(f"Received message: {message.value}")
