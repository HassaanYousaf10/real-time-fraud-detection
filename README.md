Real-Time Fraud Detection – Spark + Kafka + Helm (Ilum-Compatible)
A streamlined Spark Structured Streaming pipeline that ingests simulated transaction data from Kafka, filters fraudulent transactions (is_fraud = 1), and runs on Kubernetes via Helm. This design is Ilum-compatible because Ilum uses Helm-based orchestration under the hood.

Architecture Overview
scss
Copy
Edit
[ Transaction Producer ] --> [ Kafka Broker ] --> [ Spark Streaming Job ]
       (Python)                (Docker)            (Docker + Helm/K8s)
Producer: sends random transactions to the fraud_transactions topic.

Spark: reads, filters is_fraud == 1, and logs them.

Helm/Kubernetes: orchestrates the containerized Spark job. Ilum can reuse these definitions.

Repository Structure
perl
Copy
Edit
real-time-fraud-detection/
├── data_generator/
│   └── transaction_producer.py       # Python script simulating transactions
├── spark_jobs/
│   └── fraud_detection_streaming.py  # Spark Structured Streaming logic
├── fraud-detection-chart/
│   ├── Chart.yaml
│   └── templates/
│       └── deployment.yaml           # Helm-based K8s Deployment
├── Dockerfile                        # Builds the Spark job container
├── docker-compose.yml                # Local Kafka/Zookeeper setup
└── README.md                         # You are here
1) Local Kafka Setup
Option A: Docker Compose

bash
Copy
Edit
docker-compose up -d
Kafka broker at localhost:9092

Zookeeper at localhost:2181

(Or use your existing Kafka cluster. Update references accordingly.)

2) Docker Build & Push
bash
Copy
Edit
docker build -t <DOCKER_USER>/fraud-detection-spark:latest .
docker push <DOCKER_USER>/fraud-detection-spark:latest
Replace <DOCKER_USER> with your Docker Hub username.

3) Helm (Ilum-Compatible) Deployment
Package the Chart
bash
Copy
Edit
cd fraud-detection-chart
helm package .
cd ..
Generates fraud-detection-0.1.0.tgz.

Deploy
bash
Copy
Edit
helm upgrade --install fraud-detection ./fraud-detection-0.1.0.tgz
Or apply the deployment.yaml directly:

bash
Copy
Edit
kubectl apply -f fraud-detection-chart/templates/deployment.yaml
4) Run the Transaction Producer
bash
Copy
Edit
cd data_generator
python transaction_producer.py
Generates transactions with some marked as is_fraud=1, publishing to fraud_transactions topic.

5) Monitor Spark Streaming
Check pods:

bash
Copy
Edit
kubectl get pods
Logs:

bash
Copy
Edit
kubectl logs <spark-driver-pod>
Expected:

bash
Copy
Edit
Uploading file: /app/fraud_detection_streaming.py ...
Found fraud => {card_number=..., amount=..., is_fraud=1}
Ilum Compatibility
Helm charts define container images, environment, and orchestrations exactly how Ilum expects.

Docker ensures a reproducible environment for the Spark job.

Declarative approach can be directly managed by Ilum’s job manager.

Fraud Logic Snippet
python
Copy
Edit
# spark_jobs/fraud_detection_streaming.py

fraud_df = df_parsed.filter(col("is_fraud") == 1)
fraud_df.writeStream \
    .format("console") \
    .start() \
    .awaitTermination()
Currently a simple filter; can be extended with ML or advanced rules.

Improvements
Persist flagged fraud to a data lake or DB.

Real-time dashboards (Prometheus, Grafana).

CI/CD (GitHub Actions) to automate container + Helm updates.

Spark ML for more robust detection than boolean flags.
