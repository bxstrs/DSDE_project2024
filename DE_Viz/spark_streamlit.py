import streamlit as st
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline
from pyspark.sql.functions import col
import altair as alt

spark = SparkSession.builder.appName("Research Trend Prediction").getOrCreate()
data_2018_2023 = spark.read.csv(r"C:\desktop\workspace\university\dsde\DSDE_project2024\DE_Viz\merged_output.csv", header=True, inferSchema=True)

# Data Preprocessing
# Convert publication year to integer and subject_area to numeric using StringIndexer
indexer = StringIndexer(inputCol="subject_area", outputCol="subject_area_index")
data_2018_2023 = indexer.fit(data_2018_2023).transform(data_2018_2023)

# Use VectorAssembler to combine features into a single feature vector
assembler = VectorAssembler(inputCols=["publication_year", "subject_area_index"], outputCol="features")
data_2018_2023 = assembler.transform(data_2018_2023)

# Select the features and label (publication count)
data_2018_2023 = data_2018_2023.select("features", "publication_count")

# Initialize Linear Regression model
lr = LinearRegression(featuresCol="features", labelCol="publication_count")

# Train-test split (80% for training, 20% for testing)
train_data, test_data = data_2018_2023.randomSplit([0.8, 0.2], seed=1234)

# Train the model
lr_model = lr.fit(train_data)

# Evaluate the model
test_results = lr_model.evaluate(test_data)
st.write("Root Mean Squared Error (RMSE) on test data:", test_results.rootMeanSquaredError)

# Load 2024 data (Assuming data for 2024 is available in a separate file)
data_2024 = spark.read.csv(r"C:\desktop\workspace\university\dsde\DSDE_project2024\web_scraping\scopus_trend_2024.csv", header=True, inferSchema=True)

#Preprocess 2024 data
data_2024 = indexer.transform(data_2024)
data_2024 = assembler.transform(data_2024)

#predictions for 2024
predictions = lr_model.transform(data_2024)

# Convert to Pandas for Streamlit
predictions_df = predictions.select("subject_area", "publication_year", "prediction").toPandas()

# Display predicted publication counts for 2024
st.write("Predicted Publication Counts for 2024", predictions_df)

# Create a bar chart visualization using Altair
bar_chart = alt.Chart(predictions_df).mark_bar().encode(
    x='subject_area',
    y='prediction',
    color='subject_area'
).properties(title="Predicted Publication Trends for 2024")

# Display the chart in Streamlit
st.altair_chart(bar_chart, use_container_width=True)

# Optionally, show the raw predictions data for debugging or analysis
st.write("Raw predictions data:", predictions_df)
