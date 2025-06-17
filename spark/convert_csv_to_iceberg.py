import os
from pyspark.sql import SparkSession

warehouse = os.environ.get("SPARK_WAREHOUSE", "s3a://warehouse")
bronze = os.environ.get("BRONZE_PATH", "s3a://bronze")

spark = (SparkSession.builder.appName("csv2iceberg")
         .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog")
         .config("spark.sql.catalog.local.type", "hadoop")
         .config("spark.sql.catalog.local.warehouse", warehouse)
         .getOrCreate())

# Example: convert orders CSV to Iceberg table
orders_csv = f"{bronze}/orders.csv"

df = spark.read.option("header", True).csv(orders_csv)

df.writeTo("local.db.orders").createOrReplace()

spark.stop()
