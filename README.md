# Real-Time Fraud Detection – Spark + Kafka + Helm (Ilum-Compatible)

Built on top of Apache Spark, which powers big data solutions.

**Real-Time Fraud Detection** is a framework that ingests continuous transaction data, filters out fraudulent events (`is_fraud = 1`), and deploys the solution on Kubernetes via Helm. This architecture is Ilum-compatible because it leverages a Helm-based deployment strategy similar to that used by Ilum.

---

## How Does It Work?

### Transaction Producer

A Python script continuously generates synthetic transactions (each including fields such as `card_number`, `amount`, `timestamp`, and `is_fraud`) and publishes them to a Kafka topic (`fraud_transactions`).

### Spark Structured Streaming

A Spark job reads from Kafka, filters records where `is_fraud == 1`, and logs or outputs these fraudulent transactions in real time.

### Helm + Kubernetes

The containerized Spark job is deployed with a Helm chart on Kubernetes. This declarative approach is fully compatible with Ilum’s orchestration model.

---

## Repository Structure

```
real-time-fraud-detection/
├── data_generator/
│   └── transaction_producer.py       # Python script simulating transactions
├── spark_jobs/
│   └── fraud_detection_streaming.py  # Spark Structured Streaming logic
├── fraud-detection-chart/
│   ├── Chart.yaml                    # Helm chart metadata
│   └── templates/
│       └── deployment.yaml           # Kubernetes Deployment (Helm)
├── Dockerfile                        # Builds the Spark job container
├── docker-compose.yml                # Local Kafka/Zookeeper setup
└── README.md                         # This file
```

---

## 1) Local Kafka Setup

### Option A: Docker Compose

```bash
docker-compose up -d
```

Kafka broker will be available at `localhost:9092`  
Zookeeper at `localhost:2181`

(Alternatively, connect to an external Kafka cluster and update configurations accordingly.)

---

## 2) Docker Build & Push

### Build the Docker image

```bash
docker build -t <DOCKER_USER>/fraud-detection-spark:latest .
```

### Push the image

Replace `<DOCKER_USER>` with your Docker Hub username:

```bash
docker push <DOCKER_USER>/fraud-detection-spark:latest
```

---

## 3) Helm (Ilum-Compatible) Deployment

### Package the Helm Chart

```bash
cd fraud-detection-chart
helm package .
cd ..
```

This command generates a package (e.g., `fraud-detection-0.1.0.tgz`).

### Deploy the Chart

```bash
helm upgrade --install fraud-detection ./fraud-detection-0.1.0.tgz
```

Or apply the deployment YAML directly:

```bash
kubectl apply -f fraud-detection-chart/templates/deployment.yaml
```

---

## 4) Run the Transaction Producer

Navigate to the producer directory and run:

```bash
cd data_generator
python transaction_producer.py
```

This script continuously sends synthetic transaction events (with some having `is_fraud = 1`) to the Kafka topic.

---

## 5) Monitor Spark Streaming

### List the running pods

```bash
kubectl get pods
```

### Check the logs of the Spark driver pod

```bash
kubectl logs <spark-driver-pod>
```

You should see log entries such as:

```bash
Uploading file: /app/fraud_detection_streaming.py ...
Fraud transaction detected => { ... "is_fraud": 1, ... }
```

---

## Ilum Compatibility

- Helm charts define the container image, environment, and orchestration in a declarative manner — precisely how Ilum orchestrates containerized Spark jobs.
- Docker ensures the environment is fully reproducible.
- This design is Ilum-compatible, making it a drop-in solution for environments that use Ilum for production deployment.

---

## Fraud Logic Snippet

Excerpt from `spark_jobs/fraud_detection_streaming.py`:

```python
# Filter fraudulent transactions
fraud_df = df_parsed.filter(col("is_fraud") == 1)

# Output to console (extendable with ML logic)
fraud_df.writeStream \
    .format("console") \
    .option("truncate", "false") \
    .start() \
    .awaitTermination()
```

---

## Improvements & Future Enhancements

- Persist fraudulent alerts to a database (e.g., PostgreSQL) or cloud storage (e.g., Amazon S3)
- Integrate real-time dashboards (Grafana, Prometheus)
- Implement CI/CD pipelines (GitHub Actions) for automated Docker builds and Helm deployments
- Enhance detection using Spark MLlib for advanced anomaly detection
