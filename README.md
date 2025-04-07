# Real-Time Fraud Detection – Spark + Kafka + Helm (Ilum-Compatible)

A streamlined **Spark Structured Streaming** pipeline that ingests simulated transaction data from **Kafka**, filters fraudulent transactions (`is_fraud = 1`), and runs on **Kubernetes** via **Helm**. Designed to be **Ilum-compatible** because Ilum uses Helm-based orchestration.

---

## Architecture Overview

[ Transaction Producer ] --> [ Kafka Broker ] --> [ Spark Streaming Job ] (Python) (Docker) (Docker + Helm/K8s)

yaml
Copy
Edit

- **Producer**: sends random transactions to the `fraud_transactions` topic.
- **Spark**: reads, filters `is_fraud == 1`, logs them.
- **Deployment**: Docker (image) + Helm (charts) on Kubernetes.

---

## Repository Structure

real-time-fraud-detection/ ├── data_generator/ │ └── transaction_producer.py # Generates synthetic transactions → Kafka ├── spark_jobs/ │ └── fraud_detection_streaming.py # Spark Structured Streaming logic ├── fraud-detection-chart/ │ ├── Chart.yaml │ └── templates/ │ └── deployment.yaml # Helm-based K8s Deployment ├── Dockerfile # Spark job Docker build ├── docker-compose.yml # Local Kafka setup └── README.md # This file

yaml
Copy
Edit

---

## 1) Local Kafka Setup

**Option A**: Docker Compose

```bash
docker-compose up -d
Kafka broker on localhost:9092

Zookeeper on localhost:2181

2) Docker Build & Push
bash
Copy
Edit
docker build -t <DOCKER_USER>/fraud-detection-spark:latest .
docker push <DOCKER_USER>/fraud-detection-spark:latest
(Replace <DOCKER_USER> with your Docker Hub username.)

3) Helm (Ilum-Compatible) Deployment
Package the Chart:

bash
Copy
Edit
cd fraud-detection-chart
helm package .
cd ..
Generates fraud-detection-0.1.0.tgz.

Deploy:

bash
Copy
Edit
helm upgrade --install fraud-detection ./fraud-detection-0.1.0.tgz
(Or apply the deployment YAML directly if you prefer kubectl.)

4) Run the Transaction Producer
bash
Copy
Edit
cd data_generator
python transaction_producer.py
Sends random transactions to fraud_transactions in Kafka.

5) Monitor Spark Streaming
Get the Spark driver pod:

bash
Copy
Edit
kubectl get pods
Check logs:

bash
Copy
Edit
kubectl logs <spark-driver-pod>
You should see output like:

yaml
Copy
Edit
Uploading file: /app/fraud_detection_streaming.py ...
Fraud transaction: ID=..., is_fraud=1 ...
Ilum Compatibility
Helm defines container images and environment, exactly how Ilum expects.

Docker packaging ensures the Spark job is portable.

Declarative approach allows the same Helm chart to be ingested by Ilum’s orchestrator.

Fraud Logic Snippet
python
Copy
Edit
fraud_df = df_parsed.filter(col("is_fraud") == 1)
fraud_df.writeStream \
    .format("console") \
    .option("truncate","false") \
    .start() \
    .awaitTermination()
Basic filter—easily extended with ML or advanced rules.

Improvements
Persist fraud alerts to a DB

Dashboards for real-time metrics

CI/CD with GitHub Actions

Spark ML for dynamic detection
