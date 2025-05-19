# Prédiction des Recettes et Dépenses d'une Commune

Application web Django + Machine Learning pour prédire les recettes et dépenses d'une commune française à partir de données historiques.

---

## Fonctionnalités

- Sélection d'une commune et d'une année future
- Prédiction des recettes et dépenses via un modèle RandomForest
- Visualisation graphique de l’historique et de la prédiction
- API RESTful pour intégration externe

---

## Installation

### 1. Cloner le dépôt

```bash
git clone <url-du-repo>
cd django-ml-commune/backend
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Préparer les données

Place ton fichier Excel source dans le dossier voulu, puis exécute :

```bash
python prediction/ml/prepare_data.py
```

### 4. Entraîner le modèle

```bash
python prediction/ml/train_model.py
```

### 5. Appliquer les migrations Django

```bash
python manage.py migrate
```

### 6. Lancer le serveur

```bash
python manage.py runserver
```

---

## Utilisation

- Accède à l’interface web : [http://localhost:8000/api/form/](http://localhost:8000/api/form/)
- Utilise l’API REST :  
  - Endpoint : `POST /api/predict/`
  - Exemple de requête :
    ```json
    {
      "commune": "Marseille",
      "annee": 2026
    }
    ```
  - Réponse :
    ```json
    {
      "recettes": 45.2,
      "depenses": 41.8
    }
    ```

---

## Arborescence

```
backend/
├── manage.py
├── django_ml_commune/
│   └── settings.py
├── prediction/
│   ├── ml/
│   │   ├── prepare_data.py
│   │   ├── train_model.py
│   │   ├── donnees_communes.csv
│   │   ├── model_rf.pkl
│   │   └── label_encoder.pkl
│   ├── templates/
│   │   └── prediction/
│   │       └── predict.html
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── ...
```

---

## Dépendances principales

- Django
- djangorestframework
- pandas
- scikit-learn
- joblib
- chart.js (frontend)

---

## Déploiement

Pour déployer en ligne (Render, Railway, etc.), pense à :
- Adapter `ALLOWED_HOSTS` et `DEBUG`
- Générer une vraie `SECRET_KEY`
- Gérer les fichiers statiques (`collectstatic`)
- Ajouter un fichier `requirements.txt` et éventuellement `Procfile`

---

## Auteur

Projet réalisé par ASSA NDIAYE 
Contact : [nassa3986@gmail.com]

---

## Licence

MIT

---

## Personnalisation graphique et logo

### Ajout du logo

Pour afficher un logo sur toutes les pages :

1. Place ton image (par exemple `logo2.png`) dans le dossier :
   ```
   backend/prediction/static/prediction/logo2.png
   ```

2. Dans tes templates HTML (par exemple `home.html` ou `predict.html`), ajoute ce code juste après `<body>` :
   ```html
   <div class="logo-container">
       <img src="{% static 'prediction/logo2.png' %}" alt="Logo" style="display:block;margin:30px auto 10px auto;width:80px;">
   </div>
   ```

3. Assure-toi d’avoir en haut du fichier :
   ```django
   {% load static %}
   ```

---

### Style moderne

- Le fichier CSS principal est :  
  ```
  backend/prediction/static/prediction/styles.css
  ```
- Il est chargé dans chaque template avec :
  ```html
  <link rel="stylesheet" href="{% static 'prediction/styles.css' %}">
  ```

- Ce CSS donne un look moderne : fond doux, boutons arrondis, formulaire centré, responsive, etc.

---

### Footer

Un pied de page est ajouté à la fin de chaque page :
```html
<footer>
    &copy; 2025 Prédiction Commune
</footer>
```

---

### Exemple de début de `home.html`

```html
{% load static %}
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Accueil - Prédiction Commune</title>
    <link rel="stylesheet" href="{% static 'prediction/styles.css' %}">
</head>
<body>
    <div class="logo-container">
        <img src="{% static 'prediction/logo2.png' %}" alt="Logo" style="display:block;margin:30px auto 10px auto;width:80px;">
    </div>
    <h1>Bienvenue sur l’application de prédiction des recettes et dépenses d’une commune</h1>
    <ul>
        <li><a href="/api/form/">Formulaire de prédiction (Django)</a></li>
        <li><a href="/api/predict/">API REST (POST uniquement)</a></li>
    </ul>
    <footer>
        &copy; 2025 Prédiction Commune
    </footer>
</body>
</html>
```

---

