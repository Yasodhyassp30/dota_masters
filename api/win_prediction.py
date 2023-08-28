from flask import Blueprint,request,jsonify
import numpy as np
import tensorflow as tf
from validation.prediction import validate_prediction

prediction= Blueprint('prediction',__name__,url_prefix='/api')

@prediction.route('/predict',methods=['POST'])
def predict():
    team_array = list([0]*144)
    try:
        data=request.json
        validate_prediction(data)
        for i in range(5):
            team_array[i*2] = data['radiant'][i]['position']
            team_array[i*2+1] = data['radiant'][i]['gpm']
            team_array[data['radiant'][i]['id']+19] = 1
            team_array[i*2+10] = data['dire'][i]['position']
            team_array[i*2+11] = data['dire'][i]['gpm']
            team_array[data['dire'][i]['id']+19] = -1
       
        np_array = np.array(team_array).astype('float32')
        np_array = np_array.reshape(-1, 144)
        model = tf.keras.models.load_model('prediction/dota2_model.h5')
        prediction = model.predict(np_array)

        return jsonify({'prediction':str(prediction)}),200
    except (ValueError, TypeError) as ve_te:
        return jsonify({'error': 'Invalid data format: ' + str(ve_te)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500
    