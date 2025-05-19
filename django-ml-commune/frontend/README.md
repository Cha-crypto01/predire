# README for Frontend

## Description

Ce projet est une application web de prédiction des recettes et dépenses d’une commune, intégrant un modèle de Machine Learning via une API Django REST. Le frontend est développé en React et communique avec le backend pour fournir des prédictions basées sur les données saisies par l'utilisateur.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- Node.js (version 14 ou supérieure)
- npm (généralement installé avec Node.js)

## Installation

1. Clonez le dépôt :

   ```bash
   git clone <URL_DU_DEPOT>
   cd django-ml-commune/frontend
   ```

2. Installez les dépendances :

   ```bash
   npm install
   ```

## Démarrage de l'application

Pour démarrer l'application en mode développement, utilisez la commande suivante :

```bash
npm start
```

Cela lancera l'application et l'ouvrira dans votre navigateur par défaut à l'adresse `http://localhost:3000`.

## Structure du projet

- `public/index.html`: Point d'entrée HTML de l'application.
- `src/App.js`: Composant principal de l'application.
- `src/index.js`: Point d'entrée JavaScript de l'application.
- `src/components/PredictionForm.js`: Composant pour le formulaire de prédiction.

## Utilisation

1. Accédez à l'application via votre navigateur.
2. Remplissez le formulaire de prédiction en sélectionnant une commune et en entrant l'année.
3. Cliquez sur le bouton pour soumettre le formulaire et obtenir les prédictions.

## Contribuer

Les contributions sont les bienvenues ! Veuillez soumettre une demande de tirage (pull request) pour toute amélioration ou correction.

## License

Ce projet est sous licence MIT. Veuillez consulter le fichier LICENSE pour plus de détails.