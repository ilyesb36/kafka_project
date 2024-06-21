from kafka import KafkaConsumer
from pymongo import MongoClient
import json

KAFKA_TOPIC = 'financial-data'
KAFKA_SERVER = 'localhost:9092'
MONGODB_URI = 'mongodb://localhost:27017/'
MONGODB_DATABASE = 'financial_data'
MONGODB_COLLECTION = 'stock_data'

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]
collection = db[MONGODB_COLLECTION]

for message in consumer:
    data = message.value
    collection.insert_one(data)
    print(f"Inserted message into MongoDB: {data}")
