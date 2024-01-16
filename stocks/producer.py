import os
from confluent_kafka import Producer
from dotenv import load_dotenv
from stocks.models import Crypto

load_dotenv()


class KafkaProducer:
    @staticmethod
    def publish():
        broker = os.getenv("KAFKA_BROKER_URL")
        topic = os.getenv("KAFKA_BROKER_PRODUCER_TOPIC")

        producer = Producer(**{'bootstrap.servers': broker})
        delivery_callback = lambda err, msg: print(err or msg)

        cryptos = Crypto.objects.all()
        crypto_list = []
        for crypto in cryptos:
            crypto_list.append(crypto.code + "USDT")

        try:
            producer.produce(topic, str(crypto_list), callback=delivery_callback)
        except BufferError:
            print("Local producer queue is full. try again")
        producer.poll(0)
        producer.flush()
