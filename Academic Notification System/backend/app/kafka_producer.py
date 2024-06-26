
from notification_pb2 import Notification as ProtobufNotification
from aiokafka import AIOKafkaProducer

async def send_notification(notification):
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092',
        max_request_size=209715200  # 200 MB
    )
    await producer.start()
    try:
        notification_bytes = notification.SerializeToString()
        await producer.send_and_wait(KAFKA_TOPIC, notification_bytes)
    finally:
        await producer.stop()
