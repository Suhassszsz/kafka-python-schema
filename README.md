This project demonstrates how to use Apache Kafka with Confluent Schema Registry and Avro schemas in Python.
It covers producers, consumers, schema evolution, and compatibility modes.

📂 Project Structure
- kafka-python-schema/
  
│── avro_schemas/

   ├── payment_v1.avsc   

   └── payment_v2.avsc         

│── producer_v1.py       

│── producer_v2.py    

│── consumer.py       

│── requirements.txt  

│── docker-compose.yml      

│── images/                     


🚀 Setup Instructions

1. Start Kafka + Schema Registry

Make sure Docker and Docker Compose are installed. Then run:

- docker-compose up -d


This starts:

Zookeeper → localhost:2181

Kafka Broker → localhost:9092

Schema Registry → http://localhost:8081


2. Create the topic
- docker exec -it kafka-python-schema-broker-1 kafka-topics \
  --create --topic transactions \
  --bootstrap-server broker:29092 \
  --partitions 1 --replication-factor 1


3. Install Python dependencies
- pip install -r requirements.txt

4. Run Consumer

Start the consumer to watch messages:

- python3 consumer.py

5. Run Producers

In another terminal, run v1 producer:

- python3 producer_v1.py


Then run v2 producer:

- python3 producer_v2.py

📜 Schema Evolution & Compatibility

Schema v1 (payment_v1.avsc):

{"id": "string", "amount": "double"}


Schema v2 (payment_v2.avsc):

{"id": "string", "amount": "double", "currency": "string (default: USD)"}


Because currency has a default, this change is backward compatible:

Old consumers (v1) can still read new messages → they just ignore currency.

New consumers (v2) can read both old and new messages.

🔑
