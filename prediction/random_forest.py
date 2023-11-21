import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
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

X_train, X_test, y_train, y_test = train_test_split(train, trainlabels, test_size=0.1, random_state=42)

random_forest_classifier = RandomForestClassifier(n_estimators=2000, random_state=42)
random_forest_classifier.fit(X_train, y_train)


y_pred = random_forest_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
