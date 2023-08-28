from flask import Blueprint,request,jsonify
import numpy as np
import pickle
import joblib
import json
from validation.pick import validate_pick

picking= Blueprint('picking',__name__,url_prefix='/api')

@picking.route('/counter',methods=['POST'])
def counter():
   try:
        data = request.json
        hero_array = data['hero']
        validate_pick(data)
        with open('gmm_clustering/gmm_model.pkl', 'rb') as f:
            gmm = joblib.load(f)
  
        with open ('gmm_clustering/cluster_info.pkl', 'rb') as f:
            cluster_info = pickle.load(f)
 
        predicted_cluster = gmm.predict(np.array(hero_array).reshape(1, -1))
        int64_array = np.array(cluster_info[f"Cluster {predicted_cluster[0] + 1}"], dtype=np.int64)
        response = {
        'prediction': json.dumps(int64_array.tolist())
        }

        return jsonify(response),200
   except (ValueError, TypeError) as ve_te:
        return jsonify({'error': 'Invalid data format: ' + str(ve_te)}), 400
   except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500