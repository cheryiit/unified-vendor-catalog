import requests
from confluent_kafka import Producer
import json
import time

def fetch_and_send_to_kafka(producer, topic, vendor_api_url):
    while True:
        try:
            response = requests.get(vendor_api_url)
            if response.status_code == 200:
                products = response.json()
                for product in products:
                    producer.produce(topic, key=str(product['id']), value=json.dumps(product))
                producer.flush()
            else:
                print(f"Failed to fetch data: HTTP {response.status_code}")
        except Exception as e:
            print(f"Error occurred: {e}")
        
        time.sleep(60)  # 1 dakika bekle

if __name__ == "__main__":
    kafka_config = {
        'bootstrap.servers': 'localhost:9092'
    }
    producer = Producer(kafka_config)
    topic = 'product_updates'
    vendor_api_url = 'https://api.example.com/products'  # Örnek bir API URL'i
    fetch_and_send_to_kafka(producer, topic, vendor_api_url)