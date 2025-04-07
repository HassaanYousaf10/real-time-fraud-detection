from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def main():
    # ------------------------------------------------------------------
    # 1. CREATE SPARK SESSION
    # ------------------------------------------------------------------
    spark = (
        SparkSession.builder
        .appName("FraudDetectionJob")
        # Uncomment the next line if you want Spark to run locally on all cores:
        # .master("local[*]")
        .getOrCreate()
    )

    # ------------------------------------------------------------------
    # 2. READ THE CSV FILE
    # ------------------------------------------------------------------
    # Adjust the path if your CSV is in a different location
    input_csv_path = "data_generator/simulated_transactions.csv"


    # Read the CSV into a Spark DataFrame
    df = (
        spark.read
        .option("header", "true")    # CSV has headers
        .option("inferSchema", "true") 
        .csv(input_csv_path)
    )

    # ------------------------------------------------------------------
    # 3. EXAMINE THE DATA
    # ------------------------------------------------------------------
    print("\n=== DataFrame Schema ===")
    df.printSchema()

    print("\n=== Sample Rows ===")
    df.show(10, truncate=False)

    # ------------------------------------------------------------------
    # 4. CAST & TRANSFORM COLUMNS (OPTIONAL)
    # ------------------------------------------------------------------
    # For example, cast amount to DoubleType, is_fraud to IntegerType, etc.
    # Spark often does this automatically with inferSchema, but let's be explicit:
    df_transformed = (
        df
        .withColumn("amount", col("amount").cast("double"))
        .withColumn("is_fraud", col("is_fraud").cast("integer"))
        # Convert timestamp to Spark's timestamp type
        .withColumn("timestamp", col("timestamp").cast("timestamp"))
    )

    # Now let's do a quick check of how many fraud vs non-fraud we have
    df_transformed.groupBy("is_fraud").count().show()

    # ------------------------------------------------------------------
    # 5. WRITE RESULTS (OPTIONAL)
    # ------------------------------------------------------------------
    # Example: write out to a Parquet file or console
    # (We'll just show it on console for now)
    print("\n=== Transformed Data (first 5 rows) ===")
    df_transformed.show(5, truncate=False)

    # Stop the Spark session when done
    spark.stop()

if __name__ == "__main__":
    main()
