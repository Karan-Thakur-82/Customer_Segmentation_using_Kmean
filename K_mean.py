""" Import Libraries and Load Data """

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Create synthetic data for customer purchases
np.random.seed(42)
data = {
    'CustomerID': np.arange(1, 101),
    'TotalPurchaseAmount': np.random.randint(100, 10000, size=100),
    'NumTransactions': np.random.randint(1, 100, size=100),
    'AvgPurchaseValue': np.random.randint(10, 500, size=100),
    'Recency': np.random.randint(1, 365, size=100)
}

df = pd.DataFrame(data)
df.head()

""" Exploratory Data Analysis (EDA) """

# Pair plot to visualize relationships between features
sns.pairplot(df[['TotalPurchaseAmount', 'NumTransactions', 'AvgPurchaseValue', 'Recency']])
plt.show()

# Summary statistics
print(df.describe())

""" Data Preprocessing """

# Features for clustering
X = df[['TotalPurchaseAmount', 'NumTransactions', 'AvgPurchaseValue', 'Recency']]

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

""" Build the K-means Clustering Model """

# Elbow Method to find optimal k
wcss = []  # Within-Cluster Sum of Squares

for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

# Plotting the Elbow Graph
plt.plot(range(1, 11), wcss, marker='o')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of clusters (k)')
plt.ylabel('WCSS')
plt.show()

""" Train the K-means Model """

# Training K-means model with the optimal number of clusters (k=4)
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(X_scaled)

# Add cluster labels to the original data
df['Cluster'] = kmeans.labels_
df.head()

""" Analyze the Clusters """

# Group customers by cluster and calculate mean statistics for each group
cluster_summary = df.groupby('Cluster').mean()
print(cluster_summary)

""" Visualize the Clusters """

# Heatmap of Correlations within Each Cluster
# Compute correlations between features
corr = df[['TotalPurchaseAmount', 'NumTransactions', 'AvgPurchaseValue', 'Recency']].corr()

# Plot heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Feature Correlations Heatmap')
plt.show()