from kafka import KafkaProducer
import json
import time
import requests

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
SYMBOL = 'IBM'
KAFKA_TOPIC = 'financial-data'
KAFKA_SERVER = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_stock_data():
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={SYMBOL}&interval=1min&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'Time Series (1min)' in data:
        return data['Time Series (1min)']
    return None

while True:
    stock_data = fetch_stock_data()
    if stock_data:
        for timestamp, values in stock_data.items():
            data = {
                'timestamp': timestamp,
                'open': values['1. open'],
                'high': values['2. high'],
                'low': values['3. low'],
                'close': values['4. close'],
                'volume': values['5. volume']
            }
            producer.send(KAFKA_TOPIC, value=data)
            print(f"Produced message: {data}")
    time.sleep(60)
