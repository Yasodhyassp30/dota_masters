import numpy as np
import tensorflow as tf
import pandas as pd
from tensorflow import keras


encoded =pd.read_csv('cleaned_data_with_encoding.csv')
encoded = encoded[encoded['match_duration_seconds'] > 2000]

row_count = len(encoded)
print("Row count:", row_count)


encoded =encoded.sample(frac=1) 
encoded.pop('radiant_team_id')
encoded.pop('dire_team_id')
encoded.pop('match_duration_seconds')
y_train = encoded.pop('winner_id')
train = encoded.to_numpy().astype('float32')
trainlabels = y_train.to_numpy().astype('float32')

model =keras.Sequential([ tf.keras.layers.InputLayer(input_shape=(144)),
                         keras.layers.Dense(128,activation ='relu'),
                         keras.layers.Dense(64,activation ='relu'),
                         keras.layers.Dense(32,activation ='relu'),
                         keras.layers.Dense(16,activation ='relu'),
                         keras.layers.Dense(1,activation ='sigmoid')]
                        )
model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(),
              metrics=['accuracy'])

model.fit(train,
          trainlabels,
          epochs=20,
          batch_size =200000,
          validation_split=0.3,
          verbose=1
         )


model.save('dota2_model.h5')
