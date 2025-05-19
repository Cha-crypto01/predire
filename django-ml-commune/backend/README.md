# Projet Django de Prédiction des Recettes et Dépenses d'une Commune

Ce projet est une application web développée avec Django et intégrant un modèle de Machine Learning pour prédire les recettes et dépenses d'une commune. L'application utilise Django REST Framework pour exposer une API qui permet d'interagir avec le modèle de prédiction.

## Arborescence du Projet

```
django-ml-commune
├── backend
│   ├── manage.py
│   ├── requirements.txt
│   ├── README.md
│   ├── django_ml_commune
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── prediction
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── migrations
│       │   └── __init__.py
│       ├── models.py
│       ├── serializers.py
│       ├── tests.py
│       ├── urls.py
│       ├── views.py
│       └── ml
│           ├── prepare_data.py
│           ├── train_model.py
│           └── model.pkl
├── frontend
│   ├── package.json
│   ├── README.md
│   ├── public
│   │   └── index.html
│   └── src
│       ├── App.js
│       ├── index.js
│       └── components
│           └── PredictionForm.js
└── README.md
```

## Installation

1. **Clone le dépôt :**
   ```
   git clone <url_du_dépôt>
   cd django-ml-commune/backend
   ```

2. **Installer les dépendances :**
   ```
   pip install -r requirements.txt
   ```

3. **Configurer la base de données :**
   Modifiez le fichier `settings.py` pour configurer votre base de données.

4. **Migrer la base de données :**
   ```
   python manage.py migrate
   ```

5. **Lancer le serveur :**
   ```
   python manage.py runserver
   ```

## Utilisation de l'API

L'API est accessible à l'adresse `http://localhost:8000/api/prediction/`. Vous pouvez envoyer des requêtes POST avec les données nécessaires pour obtenir des prédictions sur les recettes et dépenses.

## Scripts de Machine Learning

Les scripts pour préparer les données et entraîner le modèle se trouvent dans le répertoire `backend/prediction/ml/`. 

- `prepare_data.py` : Prépare et nettoie les données à partir d'un fichier CSV.
- `train_model.py` : Entraîne le modèle de Machine Learning et sauvegarde le modèle entraîné sous `model.pkl`.

## Tests

Des tests unitaires sont inclus dans le fichier `backend/prediction/tests.py`. Vous pouvez les exécuter avec la commande suivante :

```
python manage.py test
```

## Contribuer

Les contributions sont les bienvenues ! Veuillez soumettre une demande de tirage pour toute amélioration ou correction.

## License

Ce projet est sous licence MIT. Veuillez consulter le fichier LICENSE pour plus de détails.