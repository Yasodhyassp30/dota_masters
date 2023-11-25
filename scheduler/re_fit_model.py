import json
from bson import ObjectId,json_util
from flask import Blueprint, current_app,request,jsonify
import numpy as np
import pandas as pd
import tensorflow as tf
from validation.matches import validate_match

def refit_model():
    try:
        db = current_app.config['Mongo_db']
        results = list(db.matches.find())
        data_rows = []
        for row in results:
            team_array = list([0]*309)
            for i in range(5):
                if row["prediction"]["radient"]>= 50 and row["feedback"]==1:
                    team_array[0] =1
                else:
                    team_array[0]=0
                team_array[i] = row['radiant'][i]['gpm']
                team_array[10+ row['radiant'][i]['position'] +i*5] = 1
                team_array[row['radiant'][i]['id']+60] = 1
                team_array[i+6] = row['dire'][i]['gpm']
                team_array[35 + row['dire'][i]['position'] + i*5] = 1
                team_array[row['dire'][i]['id']+184] = 1
                data_rows.append(team_array)
        np_array = np.array(data_rows)
        columns = ["winner_id"]
        for i in range(1,6):
            columns.append("radiant_player_"+str(i)+"_networth")
            columns.append("radiant_player_"+str(i)+"_id")
        for i in range(1,6):
            columns.append("dire_player_"+str(i)+"_networth")
            columns.append("dire_player_"+str(i)+"_id")
        for i in range(1,6):
            for j in range(1,6):
                columns.append("radiant_player_"+str(i)+"position_"+str(j))
        for i in range(1,6):
            for j in range(1,6):
                columns.append("dire_player_"+str(i)+"position_"+str(j))
        for i in range(1,249):
            columns.append(str(i))
        
        empty_df = pd.DataFrame(columns=columns)
        empty_df = pd.DataFrame(np_array, columns=columns)
        
        X = empty_df.drop(['winner_id'], axis=1)
        y = empty_df['winner_id']

        X = X.to_numpy().astype('float32')
        y = y.to_numpy().astype('float32')
        model = tf.keras.models.load_model('prediction/dota2_model.h5')
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
        model.compile(optimizer=optimizer,
                loss=tf.keras.losses.BinaryCrossentropy(),
                metrics=['accuracy'])
        model.fit(X,
            y,
            epochs=100,
            batch_size=64,
            verbose=1)
        model.save('prediction/retrained_dota2_model.h5')
        
    except Exception as e:
        print(e)
