from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

with open("avro_schemas/payment_v1.avsc") as f:
    schema_str = f.read()

schema_registry_conf = {"url": "http://localhost:8081"}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

avro_serializer = AvroSerializer(
    schema_registry_client=schema_registry_client,
    schema_str=schema_str,
    to_dict=lambda obj, ctx: obj
)

producer_conf = {
    "bootstrap.servers": "localhost:9092",
    "key.serializer": StringSerializer("utf_8"),
    "value.serializer": avro_serializer,
}

producer = SerializingProducer(producer_conf)
topic = "transactions"

for i in range(5):
    payment = {"id": f"id-{i}", "amount": 100.0 + i}
    producer.produce(topic=topic, key=payment["id"], value=payment)
    print(f"✅ Produced V1: {payment}")

producer.flush()
