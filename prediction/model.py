import numpy as np
import tensorflow as tf
import pandas as pd
from tensorflow import keras
from sklearn.model_selection import KFold, train_test_split
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dropout
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score

encoded = pd.read_csv('cleaned_data_with_encoding.csv')

for i in range(1,6):
    encoded = encoded.drop(columns=['radiant_player_'+str(i)+'_id','dire_player_'+str(i)+'_id'])


X = encoded.drop(['radiant_team_id', 'dire_team_id', 'match_duration_seconds', 'winner_id'], axis=1)
y = encoded['winner_id']

X = X.to_numpy().astype('float32')
y = y.to_numpy().astype('float32')

n_splits = 2
roc_auc_scores = []
f1_scores = []
accuracy_scores = []  

kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)


X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

model = keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(308)),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

print(model.summary())

optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)

model.compile(optimizer=optimizer,
                loss=tf.keras.losses.BinaryCrossentropy(),
                metrics=['accuracy'])

early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

model.fit(X_train,
            y_train,
            epochs=100,
            batch_size=64,
            validation_data=(X_val, y_val),
            verbose=1)

eval_results = model.evaluate(X_val, y_val)
accuracy = eval_results[1]

y_pred = model.predict(X_val)
roc_auc = roc_auc_score(y_val, y_pred)
f1 = f1_score(y_val, (y_pred > 0.5).astype(int))

accuracy_scores.append(accuracy)  
roc_auc_scores.append(roc_auc)
f1_scores.append(f1)

mean_accuracy = np.mean(accuracy_scores) 
mean_roc_auc = np.mean(roc_auc_scores)
mean_f1 = np.mean(f1_scores)

print(f"Mean Accuracy Across {n_splits} Folds: {mean_accuracy:.4f}")
print(f"Mean ROC-AUC Across {n_splits} Folds: {mean_roc_auc:.4f}")
print(f"Mean F1-Score Across {n_splits} Folds: {mean_f1:.4f}")

