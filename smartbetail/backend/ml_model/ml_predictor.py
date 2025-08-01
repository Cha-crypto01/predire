import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from django.conf import settings


class LivestockMLPredictor:
    """
    Modèle de machine learning pour prédire les maladies du bétail
    basé sur les symptômes et données de capteurs
    """
    
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.feature_names = [
            'temperature', 'frequence_cardiaque', 'frequence_respiratoire',
            'niveau_activite', 'appetit', 'fievre', 'toux', 'diarrhee',
            'ecoulement_nasal', 'boiterie', 'abattement', 'perte_poids'
        ]
        self.disease_mapping = {
            'pneumonie': {
                'nom': 'Pneumonie',
                'description': 'Infection respiratoire grave',
                'symptomes_typiques': 'Toux, fièvre, difficultés respiratoires',
                'gravite': 'élevée'
            },
            'diarrhee_infectieuse': {
                'nom': 'Diarrhée infectieuse',
                'description': 'Infection gastro-intestinale',
                'symptomes_typiques': 'Diarrhée, déshydratation, perte d\'appétit',
                'gravite': 'modérée'
            },
            'fievre_aphteuse': {
                'nom': 'Fièvre aphteuse',
                'description': 'Maladie virale contagieuse',
                'symptomes_typiques': 'Fièvre, aphtes, boiterie',
                'gravite': 'critique'
            },
            'mastite': {
                'nom': 'Mastite',
                'description': 'Inflammation des mamelles',
                'symptomes_typiques': 'Gonflement des mamelles, fièvre',
                'gravite': 'modérée'
            },
            'parasitisme': {
                'nom': 'Parasitisme',
                'description': 'Infestation par des parasites',
                'symptomes_typiques': 'Perte de poids, abattement, diarrhée',
                'gravite': 'faible'
            },
            'acidose_ruminale': {
                'nom': 'Acidose ruminale',
                'description': 'Déséquilibre du pH ruminal',
                'symptomes_typiques': 'Perte d\'appétit, abattement, diarrhée',
                'gravite': 'modérée'
            },
            'metrite': {
                'nom': 'Métrite',
                'description': 'Infection utérine post-partum',
                'symptomes_typiques': 'Fièvre, écoulements, perte d\'appétit',
                'gravite': 'élevée'
            },
            'bonne_sante': {
                'nom': 'Bonne santé',
                'description': 'Animal en bonne santé',
                'symptomes_typiques': 'Aucun symptôme particulier',
                'gravite': 'faible'
            }
        }
    
    def generate_training_data(self, n_samples=1000):
        """
        Génère un dataset fictif mais réaliste pour l'entraînement
        """
        np.random.seed(42)  # Pour la reproductibilité
        
        data = []
        
        # Générer des données pour chaque maladie
        diseases = list(self.disease_mapping.keys())
        samples_per_disease = n_samples // len(diseases)
        
        for disease in diseases:
            for _ in range(samples_per_disease):
                sample = self._generate_sample_for_disease(disease)
                sample['maladie'] = disease
                data.append(sample)
        
        # Ajouter quelques échantillons aléatoires
        remaining_samples = n_samples - len(data)
        for _ in range(remaining_samples):
            disease = np.random.choice(diseases)
            sample = self._generate_sample_for_disease(disease)
            sample['maladie'] = disease
            data.append(sample)
        
        return pd.DataFrame(data)
    
    def _generate_sample_for_disease(self, disease):
        """
        Génère un échantillon de données pour une maladie spécifique
        """
        # Valeurs de base normales
        sample = {
            'temperature': np.random.normal(38.5, 0.5),  # Température normale bovine
            'frequence_cardiaque': np.random.normal(70, 10),
            'frequence_respiratoire': np.random.normal(25, 5),
            'niveau_activite': 3,
            'appetit': 3,
            'fievre': False,
            'toux': False,
            'diarrhee': False,
            'ecoulement_nasal': False,
            'boiterie': False,
            'abattement': False,
            'perte_poids': False
        }
        
        # Modifier les valeurs selon la maladie
        if disease == 'pneumonie':
            sample['temperature'] = np.random.normal(40.0, 1.0)
            sample['frequence_respiratoire'] = np.random.normal(35, 8)
            sample['toux'] = np.random.choice([True, False], p=[0.9, 0.1])
            sample['fievre'] = np.random.choice([True, False], p=[0.8, 0.2])
            sample['niveau_activite'] = np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])
            sample['appetit'] = np.random.choice([1, 2, 3], p=[0.5, 0.3, 0.2])
            sample['ecoulement_nasal'] = np.random.choice([True, False], p=[0.7, 0.3])
            
        elif disease == 'diarrhee_infectieuse':
            sample['temperature'] = np.random.normal(39.2, 0.8)
            sample['diarrhee'] = True
            sample['appetit'] = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])
            sample['abattement'] = np.random.choice([True, False], p=[0.8, 0.2])
            sample['niveau_activite'] = np.random.choice([1, 2, 3], p=[0.5, 0.4, 0.1])
            
        elif disease == 'fievre_aphteuse':
            sample['temperature'] = np.random.normal(41.0, 1.2)
            sample['fievre'] = True
            sample['boiterie'] = np.random.choice([True, False], p=[0.9, 0.1])
            sample['appetit'] = np.random.choice([1, 2], p=[0.8, 0.2])
            sample['niveau_activite'] = np.random.choice([1, 2], p=[0.7, 0.3])
            sample['abattement'] = np.random.choice([True, False], p=[0.9, 0.1])
            
        elif disease == 'mastite':
            sample['temperature'] = np.random.normal(39.8, 0.8)
            sample['fievre'] = np.random.choice([True, False], p=[0.7, 0.3])
            sample['appetit'] = np.random.choice([2, 3, 4], p=[0.5, 0.3, 0.2])
            sample['abattement'] = np.random.choice([True, False], p=[0.6, 0.4])
            
        elif disease == 'parasitisme':
            sample['perte_poids'] = np.random.choice([True, False], p=[0.8, 0.2])
            sample['abattement'] = np.random.choice([True, False], p=[0.7, 0.3])
            sample['diarrhee'] = np.random.choice([True, False], p=[0.6, 0.4])
            sample['appetit'] = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
            sample['niveau_activite'] = np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2])
            
        elif disease == 'acidose_ruminale':
            sample['appetit'] = np.random.choice([1, 2], p=[0.8, 0.2])
            sample['abattement'] = np.random.choice([True, False], p=[0.8, 0.2])
            sample['diarrhee'] = np.random.choice([True, False], p=[0.7, 0.3])
            sample['niveau_activite'] = np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])
            
        elif disease == 'metrite':
            sample['temperature'] = np.random.normal(40.2, 1.0)
            sample['fievre'] = np.random.choice([True, False], p=[0.8, 0.2])
            sample['appetit'] = np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])
            sample['abattement'] = np.random.choice([True, False], p=[0.7, 0.3])
            
        elif disease == 'bonne_sante':
            # Garder les valeurs normales avec peu de variations
            sample['niveau_activite'] = np.random.choice([3, 4, 5], p=[0.4, 0.4, 0.2])
            sample['appetit'] = np.random.choice([3, 4, 5], p=[0.4, 0.4, 0.2])
        
        # Limiter les valeurs dans des plages réalistes
        sample['temperature'] = max(36.0, min(45.0, sample['temperature']))
        sample['frequence_cardiaque'] = max(40, min(120, int(sample['frequence_cardiaque'])))
        sample['frequence_respiratoire'] = max(10, min(60, int(sample['frequence_respiratoire'])))
        
        return sample
    
    def train_model(self, df=None):
        """
        Entraîne le modèle de classification
        """
        if df is None:
            df = self.generate_training_data()
        
        # Préparer les features
        X = df[self.feature_names].copy()
        y = df['maladie']
        
        # Encoder les labels
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Division train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Entraîner le modèle
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2
        )
        
        self.model.fit(X_train, y_train)
        
        # Évaluer le modèle
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Précision du modèle : {accuracy:.2f}")
        print("\nRapport de classification :")
        print(classification_report(y_test, y_pred, target_names=self.label_encoder.classes_))
        
        return accuracy
    
    def predict(self, symptoms_data):
        """
        Prédit la maladie basée sur les symptômes
        """
        if self.model is None:
            raise ValueError("Le modèle n'est pas entraîné")
        
        # Préparer les données d'entrée
        features = []
        for feature in self.feature_names:
            value = symptoms_data.get(feature, 0)
            if isinstance(value, bool):
                value = int(value)
            features.append(value)
        
        features_array = np.array(features).reshape(1, -1)
        
        # Prédiction
        prediction = self.model.predict(features_array)[0]
        probabilities = self.model.predict_proba(features_array)[0]
        
        # Récupérer le nom de la maladie
        disease_name = self.label_encoder.inverse_transform([prediction])[0]
        confidence = probabilities[prediction]
        
        # Obtenir toutes les probabilités
        all_predictions = []
        for i, prob in enumerate(probabilities):
            disease = self.label_encoder.inverse_transform([i])[0]
            all_predictions.append({
                'disease': disease,
                'probability': prob,
                'disease_info': self.disease_mapping.get(disease, {})
            })
        
        # Trier par probabilité décroissante
        all_predictions.sort(key=lambda x: x['probability'], reverse=True)
        
        return {
            'predicted_disease': disease_name,
            'confidence': confidence,
            'disease_info': self.disease_mapping.get(disease_name, {}),
            'all_predictions': all_predictions
        }
    
    def save_model(self, filepath=None):
        """
        Sauvegarde le modèle entraîné
        """
        if filepath is None:
            filepath = getattr(settings, 'ML_MODEL_PATH', 'ml_model/model.pkl')
        
        model_data = {
            'model': self.model,
            'label_encoder': self.label_encoder,
            'feature_names': self.feature_names,
            'disease_mapping': self.disease_mapping
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(model_data, filepath)
        print(f"Modèle sauvegardé dans {filepath}")
    
    def load_model(self, filepath=None):
        """
        Charge un modèle pré-entraîné
        """
        if filepath is None:
            filepath = getattr(settings, 'ML_MODEL_PATH', 'ml_model/model.pkl')
        
        if not os.path.exists(filepath):
            print(f"Fichier de modèle non trouvé : {filepath}")
            print("Entraînement d'un nouveau modèle...")
            self.train_model()
            self.save_model(filepath)
            return
        
        try:
            model_data = joblib.load(filepath)
            self.model = model_data['model']
            self.label_encoder = model_data['label_encoder']
            self.feature_names = model_data['feature_names']
            self.disease_mapping = model_data['disease_mapping']
            print(f"Modèle chargé depuis {filepath}")
        except Exception as e:
            print(f"Erreur lors du chargement du modèle : {e}")
            print("Entraînement d'un nouveau modèle...")
            self.train_model()
            self.save_model(filepath)
    
    def get_feature_importance(self):
        """
        Retourne l'importance des features
        """
        if self.model is None:
            return None
        
        importance = self.model.feature_importances_
        feature_importance = dict(zip(self.feature_names, importance))
        
        # Trier par importance décroissante
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_features


# Instance globale du prédicteur
predictor = LivestockMLPredictor()


def get_predictor():
    """
    Fonction pour obtenir l'instance du prédicteur
    """
    global predictor
    if predictor.model is None:
        predictor.load_model()
    return predictor


if __name__ == "__main__":
    # Test du modèle
    predictor = LivestockMLPredictor()
    
    # Entraîner le modèle
    accuracy = predictor.train_model()
    
    # Sauvegarder le modèle
    predictor.save_model()
    
    # Test de prédiction
    test_symptoms = {
        'temperature': 40.2,
        'frequence_cardiaque': 85,
        'frequence_respiratoire': 35,
        'niveau_activite': 1,
        'appetit': 2,
        'fievre': True,
        'toux': True,
        'diarrhee': False,
        'ecoulement_nasal': True,
        'boiterie': False,
        'abattement': True,
        'perte_poids': False
    }
    
    result = predictor.predict(test_symptoms)
    print(f"\nPrédiction pour les symptômes de test :")
    print(f"Maladie prédite : {result['predicted_disease']}")
    print(f"Confiance : {result['confidence']:.2f}")
    
    print("\nImportance des features :")
    for feature, importance in predictor.get_feature_importance():
        print(f"{feature}: {importance:.3f}")