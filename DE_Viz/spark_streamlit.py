import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import altair as alt

# Load 2018-2023 data
data_2018_2023 = pd.read_csv(r"D:\DSDE\DSDE_project2024\DE_Viz\merged_output.csv")

# Display some of the data to understand its structure (optional)
st.write("First few rows of 2018-2023 data:", data_2018_2023.head())

# Preprocessing the data
# Convert 'Subject Areas' into a numerical value using category codes
data_2018_2023['subject_area_index'] = data_2018_2023['Subject Areas'].astype('category').cat.codes

# Select features and labels
X = data_2018_2023[['Year', 'subject_area_index']]  # Using 'Year' and 'Subject Areas' as features
y = data_2018_2023['Citation Count']  # Assuming you want to predict 'Citation Count'

# Split the data into train and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)

# Initialize Linear Regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Evaluate the model on the test set
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)

# Display RMSE
st.write(f"Root Mean Squared Error (RMSE) on test data: {rmse}")

# Load 2024 data for predictions (assumed to be available in a separate file)
data_2024 = pd.read_csv(r"D:\DSDE\DSDE_project2024\web_scraping\scopus_trend_2024.csv")

# Display some of the 2024 data (optional)
st.write("First few rows of 2024 data:", data_2024.head())

# Preprocess 2024 data (similar to the 2018-2023 data)
data_2024['subject_area_index'] = data_2024['Subject Areas'].astype('category').cat.codes
X_2024 = data_2024[['Year', 'subject_area_index']]

# Predict citation counts for 2024 data
predictions = model.predict(X_2024)

# Add predictions to the dataframe
data_2024['predicted_citation_count'] = predictions

# Display the predicted citation counts for 2024
st.write("Predicted Citation Counts for 2024", data_2024[['Title', 'Authors', 'Year', 'predicted_citation_count']])

# Create a bar chart using Altair
bar_chart = alt.Chart(data_2024).mark_bar().encode(
    x='Title',
    y='predicted_citation_count',
    color='subject_area_index'
).properties(title="Predicted Citation Trends for 2024")

# Display the chart in Streamlit
st.altair_chart(bar_chart, use_container_width=True)

# Optionally, show the raw predictions data
st.write("Raw predictions data:", data_2024[['Title', 'Authors', 'Year', 'predicted_citation_count']])
