from confluent_kafka import DeserializingConsumer
from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

schema_registry_conf = {"url": "http://localhost:8081"}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

avro_deserializer = AvroDeserializer(
    schema_registry_client=schema_registry_client,
    schema_str=None,
    from_dict=lambda obj, ctx: obj
)

consumer_conf = {
    "bootstrap.servers": "localhost:9092",
    "key.deserializer": StringDeserializer("utf_8"),
    "value.deserializer": avro_deserializer,
    "group.id": "payment-consumers",
    "auto.offset.reset": "earliest"
}

consumer = DeserializingConsumer(consumer_conf)
consumer.subscribe(["transactions"])

print("👀 Listening for payments... (Ctrl+C to exit)")

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error:", msg.error())
        continue

    print(f"💡 Consumed record: key={msg.key()}, value={msg.value()}")
