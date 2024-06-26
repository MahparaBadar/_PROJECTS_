from notification_pb2 import Notification as ProtobufNotification
from aiokafka import AIOKafkaConsumer

async def consume_notifications():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers='kafka:9092',
        group_id="notification_group",
        value_deserializer=lambda m: ProtobufNotification.FromString(m),
        max_partition_fetch_bytes=209715200  # 200 MB
    )
    await consumer.start()
    try:
        async for msg in consumer:
            notification = msg.value
            print("Consumed message:", notification)
    finally:
        await consumer.stop()

