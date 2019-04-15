import json
from kafka import KafkaProducer

class KafkaConnector(object):

    def __init__(self, kafka_brokers):
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_brokers
        )

    def send(self, data, topic):
        self.producer.send(topic, bytes(data, 'utf-8'))
