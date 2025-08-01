#!/bin/bash

echo "🐄 SmartBétail - Démarrage de l'application"
echo "============================================"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 n'est pas installé. Veuillez l'installer avant de continuer."
    exit 1
fi

# Vérifier si Node.js est installé
if ! command -v node &> /dev/null; then
    print_error "Node.js n'est pas installé. Veuillez l'installer avant de continuer."
    exit 1
fi

print_status "Démarrage du backend Django..."

# Configuration du backend
cd backend

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    print_status "Création de l'environnement virtuel Python..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
print_status "Installation des dépendances Python..."
pip install -r requirements.txt

# Effectuer les migrations
print_status "Application des migrations de base de données..."
python manage.py migrate

# Vérifier si les données d'exemple et le modèle existent
if [ ! -f "ml_model/model.pkl" ]; then
    print_status "Configuration des données d'exemple et entraînement du modèle IA..."
    python train_model.py
else
    print_success "Modèle IA déjà entraîné"
fi

# Démarrer le serveur Django en arrière-plan
print_status "Démarrage du serveur Django sur http://localhost:8000..."
python manage.py runserver &
DJANGO_PID=$!

# Attendre que Django soit prêt
sleep 5

# Configuration du frontend
cd ../frontend

# Installer les dépendances Node.js
print_status "Installation des dépendances Node.js..."
npm install

# Démarrer le serveur Vite
print_status "Démarrage du serveur frontend sur http://localhost:5173..."
npm run dev &
VITE_PID=$!

# Attendre que tout soit prêt
sleep 3

echo ""
print_success "🎉 SmartBétail est maintenant en cours d'exécution !"
echo ""
echo "📍 Accès à l'application :"
echo "   🌐 Frontend React    : http://localhost:5173"
echo "   🔌 API Django       : http://localhost:8000/api/"
echo "   ⚙️  Admin Django     : http://localhost:8000/admin/"
echo ""
echo "👤 Comptes de test :"
echo "   Admin         : admin / admin123"
echo "   Vétérinaire   : veterinaire / vet123"
echo ""
echo "⏹️  Pour arrêter l'application, appuyez sur Ctrl+C"

# Fonction pour nettoyer les processus à l'arrêt
cleanup() {
    print_warning "Arrêt de l'application..."
    kill $DJANGO_PID $VITE_PID 2>/dev/null
    print_success "Application arrêtée"
    exit 0
}

# Capturer le signal d'interruption
trap cleanup INT

# Attendre indéfiniment
wait