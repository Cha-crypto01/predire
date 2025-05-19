import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def preprocess_data(data):
    # Suppression des colonnes inutiles
    data = data.drop(columns=['unnecessary_column'], errors='ignore')
    # Traitement des valeurs manquantes
    data.fillna(method='ffill', inplace=True)
    return data

def train_model(data):
    # Encodage de la commune
    le = LabelEncoder()
    data['Commune_enc'] = le.fit_transform(data['Commune'])

    X = data[['Commune_enc', 'Année']]
    y = data[['Recettes (M€)', 'Dépenses (M€)']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model, le

def save_model(model, le, model_path, le_path):
    joblib.dump(model, model_path)
    joblib.dump(le, le_path)

if __name__ == "__main__":
    data = load_data('backend/prediction/ml/donnees_communes.csv')
    processed_data = preprocess_data(data)
    model, le = train_model(processed_data)
    save_model(model, le, 'backend/prediction/ml/model_rf.pkl', 'backend/prediction/ml/label_encoder.pkl')

    print("✅ Modèle entraîné et sauvegardé dans backend/prediction/ml/model_rf.pkl")