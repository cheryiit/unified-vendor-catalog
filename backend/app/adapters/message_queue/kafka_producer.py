from confluent_kafka import Producer
from app.core.config import settings

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

class KafkaProducer:
    def __init__(self):
        self.producer = Producer({'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS})

    def send_message(self, topic, key, value):
        self.producer.produce(topic, key=key, value=value, callback=delivery_report)
        self.producer.flush()