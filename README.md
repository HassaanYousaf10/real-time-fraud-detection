# Real-Time Fraud Detection

Built on top of [**Apache Spark**](https://spark.apache.org/), which powers big data solutions.

**Real-Time Fraud Detection** is a **framework** aimed at ingesting continuous transaction data, filtering out fraudulent events (where `is_fraud = 1`), and deploying the solution on Kubernetes via Helm. This solution is **Ilum-compatible** because it leverages a Helm-based orchestration architecture similar to Ilum's.

---

## How Does It Work?

1. **Transaction Producer**  
   A Python script continuously generates synthetic transaction events (fields include `card_number`, `amount`, `timestamp`, and `is_fraud`) and publishes them to a Kafka topic (`fraud_transactions`).

2. **Spark Structured Streaming**  
   A Spark job reads from Kafka, filters for records where `is_fraud == 1`, and logs or outputs these events.

3. **Helm + Kubernetes**  
   The containerized Spark job is deployed with a Helm chart on Kubernetes. This Helm-based approach makes the pipeline Ilum-compatible by following the same orchestration practices.

---

## What Is the Main Idea Behind Real-Time Fraud Detection?

- **Abstraction:** Data scientists focus only on input data, output data, and transformation logic while the underlying deployment, scaling, and cluster management is handled declaratively.
- **Separation of Concerns:**  
  - **Producer:** Pushes raw transaction data into Kafka.  
  - **Processor:** Spark job filters and logs flagged transactions.
- **Flexibility:** The system is independent of the underlying storage or streaming technology, allowing for quick adaptations via Helm updates.

---

## Quick Start

1. **Start Minikube** (example configuration):
   ```bash
   minikube start --cpus 4 --memory 8192 --addons metrics-server
Deploy Kafka using Docker Compose (for local testing):

bash
Copy
docker-compose up -d
Kafka broker is available at localhost:9092

Zookeeper at localhost:2181

Build & Push Docker Image:

bash
Copy
docker build -t <DOCKER_USER>/fraud-detection-spark:latest .
docker push <DOCKER_USER>/fraud-detection-spark:latest
(Replace <DOCKER_USER> with your Docker Hub username.)

Deploy with Helm:

bash
Copy
cd fraud-detection-chart
helm package .
cd ..
helm upgrade --install fraud-detection ./fraud-detection-0.1.0.tgz
(Alternatively, apply using kubectl apply -f fraud-detection-chart/templates/deployment.yaml.)

Run the Transaction Producer:

bash
Copy
cd data_generator
python transaction_producer.py
This continuously sends random transactions (with some is_fraud = 1) to the Kafka topic.

Monitor Spark Streaming:

bash
Copy
kubectl get pods
kubectl logs <spark-driver-pod>
Look for log entries showing:

bash
Copy
Uploading file: /app/fraud_detection_streaming.py ...
Fraud transaction detected => { ... , is_fraud = 1, ... }
Ilum Compatibility
Helm charts in this project define the container image, environment, and deployment configuration in a declarative manner—exactly how Ilum orchestrates containerized Spark jobs.

Docker packaging ensures that the environment is reproducible.

The deployment approach makes the pipeline drop-in compatible with Ilum’s job management system.

Code Snippets
Fraud Detection Logic (Spark Streaming)
python
Copy
# spark_jobs/fraud_detection_streaming.py

fraud_df = df_parsed.filter(col("is_fraud") == 1)
fraud_df.writeStream \
    .format("console") \
    .option("truncate", "false") \
    .start() \
    .awaitTermination()
Transaction Producer
python
Copy
# data_generator/transaction_producer.py

import json, time, random
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
while True:
    transaction = {
        "card_number": random.randint(1_000_000_000_000_000, 9_999_999_999_999_999),
        "amount": round(random.uniform(1.0, 3000.0), 2),
        "timestamp": time.time(),
        "is_fraud": random.choice([0, 1, 0, 0])
    }
    producer.send('fraud_transactions', json.dumps(transaction).encode('utf-8'))
    time.sleep(1)
Contribution
How to Contribute:

Clone the Repository:

bash
Copy
git clone https://github.com/YourUsername/real-time-fraud-detection.git
cd real-time-fraud-detection
Enhance the Pipeline:

Improve the fraud detection logic (add advanced rules, Spark ML, etc.).

Extend the Docker and Helm configuration for additional features.

Integrate additional output sinks (databases, dashboards).

Submit a Pull Request to the main branch with your improvements.

Final Notes
Abstraction: The pipeline allows data scientists to focus solely on algorithms without worrying about cluster details.

Flexibility: The entire system is independent of the underlying infrastructure and is easily configurable via Helm.

Ilum-Ready: Using Docker + Helm, this solution is designed for integration into a production Ilum environment.
