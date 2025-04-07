#!/usr/bin/env python3


from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType

def main():
    # -------------------------------
    # 1. CREATE SPARK SESSION
    # -------------------------------
    spark = (
        SparkSession.builder
        .appName("RealTimeFraudDetection")
        .master("local[*]")  # Use all available cores
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    
    # -------------------------------
    # 2. DEFINE THE SCHEMA FOR INCOMING DATA
    # -------------------------------
    schema = StructType([
        StructField("transaction_id", StringType(), True),
        StructField("card_number", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("merchant_id", StringType(), True),
        StructField("merchant_type", StringType(), True),
        StructField("is_fraud", IntegerType(), True),
        StructField("timestamp", StringType(), True)  # Parse later to timestamp
    ])
    
    # -------------------------------
    # 3. READ THE STREAM FROM KAFKA
    # -------------------------------
    kafka_bootstrap_servers = "localhost:9092"
    kafka_topic = "fraud_transactions"
    
    df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
        .option("subscribe", kafka_topic)
        .option("startingOffsets", "latest")
        .load()
    )
    
    # Convert the Kafka binary "value" to string
    df_json = df.selectExpr("CAST(value AS STRING) as json_str")
    
    # -------------------------------
    # 4. PARSE THE JSON AND APPLY THE SCHEMA
    # -------------------------------
    df_parsed = df_json.select(from_json(col("json_str"), schema).alias("data")).select("data.*")
    
    # Convert the timestamp string to an actual timestamp
    df_parsed = df_parsed.withColumn("timestamp", col("timestamp").cast(TimestampType()))
    
    # -------------------------------
    # 5. APPLY FRAUD DETECTION LOGIC
    # -------------------------------
    # For demonstration, simply filter transactions where is_fraud == 1.
    fraud_df = df_parsed.filter(col("is_fraud") == 1)
    
    # -------------------------------
    # 6. OUTPUT THE STREAM TO THE CONSOLE
    # -------------------------------
    query = fraud_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", "false") \
        .start()
    
    query.awaitTermination()

if __name__ == "__main__":
    main()
