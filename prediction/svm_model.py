import numpy as np
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


encoded = pd.read_csv('cleaned_data_with_encoding.csv')
encoded = encoded[encoded['match_duration_seconds'] > 2000]

encoded = encoded.sample(frac=1)
encoded.pop('radiant_team_id')
encoded.pop('dire_team_id')
encoded.pop('match_duration_seconds')
y_train = encoded.pop('winner_id')
train = encoded.to_numpy().astype('float32')
trainlabels = y_train.to_numpy().astype('float32')


X_train, X_test, y_train, y_test = train_test_split(train, trainlabels, test_size=0.3, random_state=42)


svm_classifier = SVC(kernel='linear') 
svm_classifier.fit(X_train, y_train)


y_pred = svm_classifier.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
