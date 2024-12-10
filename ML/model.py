import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import streamlit as st

data_2018 = "C:/CEDT/Semester_3/2110403/DSDE_project2024/json_data/information.csv"  # ข้อมูลปี 2018-2023
data_2024 = "C:/CEDT/Semester_3/2110403/DSDE_project2024/web_scraping/scopus_trend_2024.csv"  # ข้อมูลปี 2024
df = pd.read_csv(data_2018)
df_2024 = pd.read_csv(data_2024)
df[['Abstract', 'Subject Areas']] = df[['Abstract', 'Subject Areas']].astype(str)
df_2024[['Abstract', 'Subject Areas']] = df_2024[['Abstract', 'Subject Areas']].astype(str)
df = pd.merge(df, df_2024, how='outer')

# Features for Clustering
X = df[['Year', 'Citation Count']]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#Streamlit

st.title("Clustering Analysis of 2018-2024 Data")

st.sidebar.title('Clustering Selector')
n_cluster = st.sidebar.slider("Number of Clustering", 2, 10, 3)

kmeans = KMeans(n_clusters=n_cluster, random_state=42)
kmeans.fit(X_scaled)
df['cluster'] = kmeans.labels_

fig = px.scatter(
    df, 
    x='Year', 
    y='Citation Count', 
    color='cluster', 
    size='Citation Count',
    hover_data=['Title'],
    title='Enhanced Cluster Visualization'
)

st.plotly_chart(fig)