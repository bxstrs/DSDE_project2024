import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px

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

kmeans = KMeans(n_clusters=3, random_state=42)  # กำหนดจำนวนคลัสเตอร์เป็น 3
kmeans.fit(X_scaled)
df['cluster'] = kmeans.labels_

fig = px.scatter(
    df, 
    x='Year', 
    y='Citation Count', 
    color='cluster', 
    size='Citation Count',  # Optional: size of the points
    hover_data=['Title'],  # Optional: display extra information on hover
    title='Enhanced Cluster Visualization'
)
fig.show()