import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from scikeras.wrappers import KerasClassifier, KerasRegressor
from tensorflow import keras
from tensorflow.keras.layers import Dropout
from sklearn.metrics import make_scorer, roc_auc_score, f1_score, accuracy_score

# Load your dataset
encoded = pd.read_csv('cleaned_data_with_encoding.csv')
encoded = encoded[encoded['match_duration_seconds'] > 2000]

X = encoded.drop(['radiant_team_id', 'dire_team_id', 'match_duration_seconds', 'winner_id'], axis=1)
y = encoded['winner_id']

X = X.to_numpy().astype('float32')
y = y.to_numpy().astype('float32')


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


def create_model(optimizer='adam', dropout_rate=0.0):
    model = keras.Sequential([
        keras.layers.InputLayer(input_shape=(144)),
        keras.layers.Dense(256, activation='relu'),
        Dropout(dropout_rate),
        keras.layers.Dense(128, activation='relu'),
        Dropout(dropout_rate),
        keras.layers.Dense(64, activation='relu'),
        Dropout(dropout_rate),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer=optimizer,
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    return model


model = KerasClassifier(build_fn=create_model, verbose=0)

param_grid = {
    'batch_size': [128, 256],
    'epochs': [20, 30],
    'dropout_rate': [0.3, 0.5],
    'optimizer': ['adam', 'rmsprop']
}


scoring = {
    'roc_auc': make_scorer(roc_auc_score),
    'f1_score': make_scorer(f1_score),
    'accuracy': make_scorer(accuracy_score)
}


grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring=scoring, refit='roc_auc', cv=3, verbose=1)


grid_search.fit(X_train, y_train)


print("Best Parameters:", grid_search.best_params_)
print("Best ROC-AUC:", grid_search.best_score_)
print("Best F1-Score:", grid_search.cv_results_['mean_test_f1_score'][grid_search.best_index_])
print("Best Accuracy:", grid_search.cv_results_['mean_test_accuracy'][grid_search.best_index_])


best_model = grid_search.best_estimator_
test_predictions = best_model.predict(X_test)
test_roc_auc = roc_auc_score(y_test, test_predictions)
test_f1 = f1_score(y_test, test_predictions)
test_accuracy = accuracy_score(y_test, test_predictions)

print("Test ROC-AUC:", test_roc_auc)
print("Test F1-Score:", test_f1)
print("Test Accuracy:", test_accuracy)

