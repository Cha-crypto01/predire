import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

# Charger les données préparées
df = pd.read_csv('backend/prediction/ml/donnees_communes.csv')

# Encodage de la commune
le = LabelEncoder()
df['Commune_enc'] = le.fit_transform(df['Commune'])

# Features et cibles
X = df[['Commune_enc', 'Année']]
y = df[['Recettes (M€)', 'Dépenses (M€)']]

# Entraînement du modèle
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Sauvegarde du modèle et de l’encodeur
joblib.dump(model, 'backend/prediction/ml/model_rf.pkl')
joblib.dump(le, 'backend/prediction/ml/label_encoder.pkl')

print("✅ Modèle entraîné et sauvegardé dans backend/prediction/ml/model_rf.pkl")
