import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

import joblib


# Load Dataset

data = pd.read_csv('dataset/crop_prediction.csv')


# Label Encoding

encoder_crop = LabelEncoder()
encoder_soil = LabelEncoder()
encoder_season = LabelEncoder()
encoder_result = LabelEncoder()


data['crop'] = encoder_crop.fit_transform(data['crop'])

data['soil'] = encoder_soil.fit_transform(data['soil'])

data['season'] = encoder_season.fit_transform(data['season'])

data['result'] = encoder_result.fit_transform(data['result'])


# Features & Target

X = data[['crop', 'soil', 'season',
          'temperature', 'humidity', 'rainfall']]

y = data['result']


# Train Test Split

X_train, X_test, y_train, y_test = train_test_split(

    X, y,

    test_size=0.2,

    random_state=42
)


# Random Forest Model

model = RandomForestClassifier(

    n_estimators=100,

    random_state=42
)


# Train Model

model.fit(X_train, y_train)


# Test Accuracy

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)


# Save Model

joblib.dump(model, 'models/crop_model.pkl')

joblib.dump(encoder_crop, 'models/encoder_crop.pkl')

joblib.dump(encoder_soil, 'models/encoder_soil.pkl')

joblib.dump(encoder_season, 'models/encoder_season.pkl')

joblib.dump(encoder_result, 'models/encoder_result.pkl')


print("Model Saved Successfully")