from flask import Blueprint,request,jsonify
import numpy as np
import tensorflow as tf
from validation.prediction import validate_prediction

prediction= Blueprint('prediction',__name__,url_prefix='/api')

@prediction.route('/predict',methods=['POST'])
def predict():
    team_array = list([0]*308)
    try:
        data=request.json
        validate_prediction(data)
        for i in range(5):
           
            team_array[i] = data['radiant'][i]['gpm']
            team_array[9+ data['radiant'][i]['position'] +i*5] = 1
            team_array[data['radiant'][i]['id']+59] = 1
            team_array[i+5] = data['dire'][i]['gpm']
            team_array[34 + data['dire'][i]['position'] + i*5] = 1
            team_array[data['dire'][i]['id']+183] = 1
       
        np_array = np.array(team_array).astype('float32')
        np_array = np_array.reshape(-1, 308)
        model = tf.keras.models.load_model('prediction/dota2_model.h5')
        prediction = model.predict(np_array)
        prediction =np.round(prediction, 4)
        prediction_list = prediction.tolist()
        
        prediction_list[0][0] = round(prediction_list[0][0],4)
        print(prediction_list)
        return jsonify({'prediction': str(prediction_list)}), 200
    except (ValueError, TypeError) as ve_te:
        print(ve_te)
        return jsonify({'error': 'Invalid data format: ' + str(ve_te)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500
    