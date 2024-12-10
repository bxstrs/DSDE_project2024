from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, count, lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import pandas as pd
import os

#Initialize Spark session
spark = SparkSession.builder \
    .appName("Research Paper Trends") \
    .getOrCreate()

# Load datasets
data_2018_2023 = spark.read.csv(r"C:\desktop\workspace\university\dsde\DSDE_project2024\DE\merged_output.csv", header=True, inferSchema=True)
data_2024 = spark.read.csv(r"C:\desktop\workspace\university\dsde\DSDE_project2024\web_scraping\scopus_trend_2024.csv", header=True, inferSchema=True)

data_2018_2023 = data_2018_2023.withColumn("publication_year", col("publication_year").cast("int"))

# Calculate trends: Count the number of publications per subject area per year
trend_data_2018_2023 = data_2018_2023.groupBy("publication_year", "subject_area") \
    .agg(count(lit(1)).alias("publication_count")) \
    .orderBy("publication_year", "publication_count", ascending=[True, False])

trend_data_2018_2023.show(10)

# Calculate the average publication count per subject area over 2018-2023
avg_trends_2018_2023 = trend_data_2018_2023.groupBy("subject_area") \
    .agg({'publication_count': 'avg'}).withColumnRenamed('avg(publication_count)', 'predicted_2024')

# Show the predicted trends
avg_trends_2018_2023.show()