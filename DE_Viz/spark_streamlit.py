import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import plotly.express as px
import altair as alt

# Title and Description
st.title("Research Trend Analysis")
st.write("""
This application analyzes research trends using clustering, citation predictions, and data visualization. 
Explore citation trends and predictive insights for research papers!
""")

# Load Data
st.header("Load and Explore Data")
data_2018_2023 = pd.read_csv(r"C:\vscode chula\dsde_pj\DSDE_project2024\DE_Viz\merged_output.csv")
data_2024 = pd.read_csv(r"C:\vscode chula\dsde_pj\DSDE_project2024\web_scraping\scopus_trend_2024.csv")

st.write("First few rows of 2018-2023 data:", data_2018_2023.head())
st.write("First few rows of 2024 data:", data_2024.head())

# Preprocessing
data_2018_2023['subject_area_index'] = data_2018_2023['Subject Areas'].astype('category').cat.codes
data_2024['subject_area_index'] = data_2024['Subject Areas'].astype('category').cat.codes

# Clustering
st.header("Clustering Analysis")
X = data_2018_2023[['Year', 'Citation Count']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X_scaled)
data_2018_2023['Cluster'] = kmeans.labels_

# Interactive Clustering Scatter Plot
year_min, year_max = int(data_2018_2023['Year'].min()), int(data_2018_2023['Year'].max())
selected_years = st.slider("Select Year Range for Clustering", min_value=year_min, max_value=year_max, value=(year_min, year_max))
filtered_data = data_2018_2023[(data_2018_2023['Year'] >= selected_years[0]) & (data_2018_2023['Year'] <= selected_years[1])]

fig = px.scatter(filtered_data, 
                 x='Year', 
                 y='Citation Count', 
                 color='Cluster', 
                 title="Cluster Visualization: Year vs Citation Count",
                 hover_data=['Title', 'Authors', 'Subject Areas'])
st.plotly_chart(fig)

# Citation Trends
st.header("Citation Trends Over Time")
trend_data = data_2018_2023.groupby(['Year', 'Cluster'])['Citation Count'].mean().reset_index()
line_chart = px.line(trend_data, 
                     x='Year', 
                     y='Citation Count', 
                     color='Cluster', 
                     title="Average Citation Count Over Years by Cluster",
                     markers=True)
st.plotly_chart(line_chart)

# Citation Prediction for 2024
st.header("Citation Prediction for 2024")
X_train, X_test, y_train, y_test = train_test_split(
    data_2018_2023[['Year', 'subject_area_index']], 
    data_2018_2023['Citation Count'], 
    test_size=0.2, 
    random_state=1234
)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)
st.write(f"Root Mean Squared Error (RMSE) on test data: {rmse}")

X_2024 = data_2024[['Year', 'subject_area_index']]
data_2024['predicted_citation_count'] = model.predict(X_2024)

# Bar Chart for Predictions using Altair
st.subheader("Predicted Citation Trends for 2024")
bar_chart = alt.Chart(data_2024).mark_bar().encode(
    x=alt.X('Title:N', sort='-y', axis=alt.Axis(title="Title", labelAngle=-45)),
    y=alt.Y('predicted_citation_count:Q', axis=alt.Axis(title="Predicted Citation Count")),
    color='subject_area_index:N',
    tooltip=['Title', 'Authors', 'predicted_citation_count', 'subject_area_index']
).properties(title="Predicted Citation Trends for 2024", width=800, height=400)

st.altair_chart(bar_chart, use_container_width=True)

# Interactive Table
st.header("Explore Data by Cluster")
filter_cluster = st.selectbox("Filter by Cluster", options=sorted(data_2018_2023['Cluster'].unique()))
filtered_table = data_2018_2023[data_2018_2023['Cluster'] == filter_cluster]
st.write(filtered_table[['Title', 'Authors', 'Year', 'Citation Count', 'Cluster']])

# Raw Predictions Data
st.header("Raw Predictions for 2024")
st.write(data_2024[['Title', 'Authors', 'Year', 'predicted_citation_count']])
