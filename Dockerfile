FROM bitnami/spark:3.5.1

WORKDIR /app

COPY ./spark_jobs/fraud_detection_streaming.py /app/fraud_detection_streaming.py

USER root

# Create necessary directories and set permissions
RUN mkdir -p /tmp/app && chmod -R 777 /tmp/app \
    && mkdir -p /tmp/.ivy2 && chmod -R 777 /tmp/.ivy2 \
    && chmod +x /app/fraud_detection_streaming.py

# Install required Python packages
RUN pip install --no-cache-dir py4j==0.10.9.7 pyspark==3.5.1

# IMPORTANT: Explicitly add a user named "spark" with UID 1001
RUN useradd -m -u 1001 -s /bin/bash spark \
    && chown -R spark:spark /app /tmp/app /tmp/.ivy2

# Set environment variables explicitly
ENV HADOOP_USER_NAME=spark

# Switch to explicitly defined user
USER spark

CMD ["/bin/bash"]
