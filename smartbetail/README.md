# 🐄 SmartBétail - Suivi Sanitaire Intelligent du Bétail

SmartBétail est une application complète de gestion et de suivi sanitaire du bétail utilisant l'intelligence artificielle pour le diagnostic des maladies et la planification des soins préventifs.

## 🎯 Fonctionnalités

### 🤖 Intelligence Artificielle
- **Prédiction de maladies** basée sur les symptômes observés et données de capteurs
- **Modèle RandomForest** entraîné sur des données vétérinaires simulées
- **Recommandations de traitement** automatiques selon la maladie détectée
- **Niveau de confiance** pour chaque diagnostic

### 📊 Dashboard & Monitoring
- **Vue d'ensemble** de l'état de santé du troupeau
- **Statistiques en temps réel** (animaux malades, soins en retard, etc.)
- **Graphiques interactifs** de répartition des maladies et types d'animaux
- **Historique des diagnostics** récents

### 📅 Planification des Soins
- **Gestion des vaccinations** et soins préventifs
- **Système de rappels** pour les soins en retard
- **Calendrier des interventions** avec filtres et recherche
- **Suivi du statut** des soins (planifié, en cours, terminé)

### 🐾 Gestion du Troupeau
- **Fiche détaillée** de chaque animal (race, âge, poids, etc.)
- **Historique médical** complet par animal
- **Filtres et recherche** avancés
- **Interface d'administration** pour la gestion des données

## 🏗️ Architecture Technique

### Backend - Django REST Framework
- **API REST** complète avec endpoints pour toutes les fonctionnalités
- **Base de données SQLite** pour le développement (PostgreSQL pour la production)
- **Modèle ML intégré** avec scikit-learn
- **Interface d'administration** Django pour la gestion des données

### Frontend - React avec Vite
- **Interface moderne** et responsive avec TailwindCSS
- **Composants React** modulaires et réutilisables
- **Graphiques interactifs** avec Recharts
- **Navigation** avec React Router

### Machine Learning
- **RandomForestClassifier** pour la classification des maladies
- **Features d'entrée** : température, fréquence cardiaque, symptômes observés, etc.
- **Dataset synthétique** réaliste pour l'entraînement
- **Sauvegarde/chargement** automatique du modèle

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.8+ 
- Node.js 16+
- Git

### 1. Cloner le projet
```bash
git clone <repository-url>
cd smartbetail
```

### 2. Configuration du Backend

```bash
cd backend

# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
# Sur Linux/Mac:
source venv/bin/activate
# Sur Windows:
# venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Effectuer les migrations
python manage.py migrate

# Configurer les données et entraîner le modèle IA
python train_model.py

# Démarrer le serveur Django
python manage.py runserver
```

### 3. Configuration du Frontend

```bash
cd ../frontend

# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm run dev
```

### 4. Accès à l'Application

- **Frontend React** : http://localhost:5173
- **API Django** : http://localhost:8000/api/
- **Administration Django** : http://localhost:8000/admin/

#### Comptes par défaut :
- **Admin** : `admin` / `admin123`
- **Vétérinaire** : `veterinaire` / `vet123`

## 📋 Utilisation

### 1. Dashboard
Accédez au tableau de bord pour une vue d'ensemble :
- Statistiques générales du troupeau
- Graphiques de répartition des maladies
- Diagnostics récents
- Soins urgents à effectuer

### 2. Prédiction IA
Pour diagnostiquer un animal malade :
1. Sélectionnez l'animal concerné
2. Renseignez les données vitales (température, fréquences, etc.)
3. Évaluez le comportement (activité, appétit)
4. Cochez les symptômes observés
5. Lancez l'analyse IA
6. Consultez le diagnostic et les recommandations

### 3. Planification des Soins
Pour gérer les soins préventifs :
1. Cliquez sur "Nouveau Soin"
2. Sélectionnez l'animal et le type de soin
3. Définissez la date d'intervention
4. Suivez l'état d'avancement des soins

### 4. Gestion des Animaux
Consultez la liste complète du troupeau avec :
- Informations détaillées par animal
- Filtres par type (bovin, ovin, etc.)
- Statistiques par catégorie

## 🔗 API REST

### Endpoints Principaux

#### Dashboard
- `GET /api/dashboard/` - Données du tableau de bord

#### Prédiction IA
- `POST /api/predict/` - Prédire une maladie
- `POST /api/recommend/` - Recommander un traitement

#### Gestion des données
- `GET/POST /api/animals/` - Animaux
- `GET /api/diseases/` - Maladies
- `GET /api/treatments/` - Traitements
- `GET/POST/PUT/DELETE /api/schedule/` - Planification des soins

#### Health Check
- `GET /api/health/` - État de l'API et du modèle ML

### Exemple d'utilisation de l'API

```bash
# Prédiction de maladie
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "animal_id": 1,
    "temperature": 40.2,
    "niveau_activite": 1,
    "appetit": 2,
    "fievre": true,
    "toux": true,
    "abattement": true
  }'
```

## 🧠 Amélioration du Modèle IA

Le modèle peut être amélioré de plusieurs façons :

### 1. Apprentissage Continu
- Collecter les **feedbacks vétérinaires** sur les diagnostics
- **Réentraîner** le modèle avec les nouvelles données validées
- Ajuster les **poids des features** selon les retours d'expérience

### 2. Données Réelles
- Remplacer le dataset synthétique par des **données vétérinaires réelles**
- Intégrer des **historiques de cas cliniques**
- Collaborer avec des **vétérinaires experts** pour la validation

### 3. Features Avancées
- Ajouter des **données d'imagerie** (photos, radiographies)
- Intégrer des **capteurs IoT** pour le monitoring continu
- Utiliser des **données environnementales** (météo, alimentation)

### 4. Modèles Plus Sophistiqués
- Expérimenter avec des **réseaux de neurones** (TensorFlow/PyTorch)
- Implémenter des **modèles d'ensemble** pour améliorer la précision
- Utiliser des **techniques de NLP** pour analyser les notes vétérinaires

## 📁 Structure du Projet

```
smartbetail/
├── backend/                          # Backend Django
│   ├── smartbetail_project/          # Configuration Django
│   ├── livestock/                    # Application principale
│   │   ├── models.py                 # Modèles de données
│   │   ├── serializers.py            # Sérialiseurs REST
│   │   ├── views.py                  # Vues et endpoints
│   │   ├── urls.py                   # URLs de l'app
│   │   └── admin.py                  # Interface d'administration
│   ├── ml_model/                     # Module Machine Learning
│   │   ├── ml_predictor.py           # Modèle de prédiction
│   │   └── model.pkl                 # Modèle entraîné
│   ├── train_model.py                # Script d'entraînement
│   ├── requirements.txt              # Dépendances Python
│   └── manage.py                     # Script de gestion Django
├── frontend/                         # Frontend React
│   ├── src/
│   │   ├── components/               # Composants React
│   │   │   ├── Layout.jsx            # Layout principal
│   │   │   ├── Dashboard.jsx         # Tableau de bord
│   │   │   ├── Predict.jsx           # Prédiction IA
│   │   │   ├── Schedule.jsx          # Planification
│   │   │   └── Animals.jsx           # Gestion animaux
│   │   ├── services/
│   │   │   └── api.js                # Service API
│   │   ├── App.jsx                   # App principale
│   │   └── index.css                 # Styles TailwindCSS
│   ├── package.json                  # Dépendances Node.js
│   └── vite.config.js                # Configuration Vite
└── README.md                         # Documentation
```

## 🔧 Configuration pour la Production

### Backend
1. Changer la `SECRET_KEY` Django
2. Configurer `DEBUG = False`
3. Utiliser PostgreSQL au lieu de SQLite
4. Configurer les variables d'environnement
5. Utiliser un serveur WSGI (Gunicorn)

### Frontend
1. Builder l'application : `npm run build`
2. Servir les fichiers statiques avec Nginx
3. Configurer les URL d'API de production

### Base de Données
1. Migrer vers PostgreSQL :
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smartbetail_db',
        'USER': 'smartbetail_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- **Django REST Framework** pour l'API robuste
- **React et Vite** pour l'interface moderne
- **scikit-learn** pour le machine learning
- **TailwindCSS** pour le design
- **Recharts** pour les graphiques

---

**SmartBétail** - Révolutionner la santé animale avec l'IA 🚀