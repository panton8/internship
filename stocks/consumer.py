import json
import os

from confluent_kafka import Consumer, KafkaException
from dotenv import load_dotenv

from stocks.models import Crypto

load_dotenv()


class KafkaConsumer:
    @staticmethod
    def subscribe():
        broker = os.getenv("KAFKA_BROKER_URL")
        topic = [os.getenv("KAFKA_BROKER_CONSUMER_TOPIC")]
        group = os.getenv("KAFKA_BROKER_GROUP")

        conf = {
            "bootstrap.servers": broker,
            "group.id": group,
            "auto.offset.reset": "latest",
        }

        consumer = Consumer(conf)
        consumer.subscribe(topic)
        try:
            while True:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    raise KafkaException(msg.error())
                else:
                    cryptos_data = json.loads(msg.value().decode("utf-8"))
                    for code, rate in cryptos_data.items():
                        crypto = Crypto.objects.get(code=code)
                        crypto.exchange_rate = rate
                        crypto.save()
        finally:
            consumer.close()
