import pickle
import joblib
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score


data = pd.read_csv('gmm_hero_weakness.csv')

names = data.iloc[:, 0].values
data_values = data.iloc[:, 1:].values

num_clusters = 15 
gmm = GaussianMixture(n_components=num_clusters, random_state=0)
gmm.fit(data_values)
cluster_assignments = gmm.predict(data_values)

silhouette_avg = silhouette_score(data_values, cluster_assignments)

cluster_counts = np.bincount(cluster_assignments)



print(f"Silhouette Score: {silhouette_avg}")

cluster_info = {}
for cluster_num in range(num_clusters):
    cluster_name = f"Cluster {cluster_num + 1}"
    
    cluster_data_points = [names[i] for i, assignment in enumerate(cluster_assignments) if assignment == cluster_num]
    
    cluster_info[cluster_name] = cluster_data_points
    

with open('cluster_info.pkl', 'wb') as f:
    pickle.dump(cluster_info, f)

new_data_point = np.array([0,1,0,1,1,1,1,1,0]) 

predicted_cluster = gmm.predict(new_data_point.reshape(1, -1))

print(f"Predicted cluster for new data point: {predicted_cluster[0] + 1}")
model_filename = 'gmm_model.pkl'
joblib.dump(gmm, model_filename)

print(f"GMM model exported as {model_filename}")

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 6))

colors = plt.cm.nipy_spectral(np.linspace(0, 1, num_clusters))

cluster_centers = gmm.means_


for cluster_num in range(num_clusters):
    cluster_name = f"Cluster {cluster_num + 1}"
    
    cluster_data_points = data_values[cluster_assignments == cluster_num]
    
    ax.scatter(cluster_data_points[:, 0], cluster_data_points[:, 1], label=cluster_name, c=colors[cluster_num], s=50)
    
    circle = plt.Circle((cluster_centers[cluster_num, 0], cluster_centers[cluster_num, 1]), radius=0.15, color=colors[cluster_num], fill=False)
    ax.add_artist(circle)


ax.set_title('Gaussian Mixture Model Clustering')
ax.set_xlabel('Feature 1')
ax.set_ylabel('Feature 2')
ax.legend()

plt.show()

