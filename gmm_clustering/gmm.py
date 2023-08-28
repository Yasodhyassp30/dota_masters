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