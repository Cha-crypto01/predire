#!/usr/bin/env python3
"""
Script d'entraînement du modèle ML et de peuplement de la base de données
pour SmartBétail
"""

import os
import sys
import django
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartbetail_project.settings')
django.setup()

from django.contrib.auth.models import User
from livestock.models import Animal, Maladie, Traitement, PlanificationSoin
from ml_model.ml_predictor import LivestockMLPredictor
from datetime import datetime, timedelta
from django.utils import timezone


def create_sample_data():
    """Créer des données d'exemple pour tester l'application"""
    print("Création des données d'exemple...")
    
    # Créer un utilisateur admin
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@smartbetail.com',
            'first_name': 'Admin',
            'last_name': 'SmartBétail',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✓ Utilisateur admin créé (login: admin, password: admin123)")
    else:
        print(f"✓ Utilisateur admin existe déjà")
    
    # Créer un vétérinaire
    vet_user, created = User.objects.get_or_create(
        username='veterinaire',
        defaults={
            'email': 'vet@smartbetail.com',
            'first_name': 'Dr',
            'last_name': 'Vétérinaire',
            'is_staff': True
        }
    )
    if created:
        vet_user.set_password('vet123')
        vet_user.save()
        print(f"✓ Utilisateur vétérinaire créé (login: veterinaire, password: vet123)")
    
    # Créer les maladies
    maladies_data = [
        {
            'nom': 'Pneumonie',
            'description': 'Infection respiratoire grave affectant les poumons',
            'symptomes_typiques': 'Toux, fièvre, difficultés respiratoires, écoulement nasal',
            'gravite': 'élevée'
        },
        {
            'nom': 'Diarrhée infectieuse',
            'description': 'Infection gastro-intestinale causant des troubles digestifs',
            'symptomes_typiques': 'Diarrhée, déshydratation, perte d\'appétit, abattement',
            'gravite': 'modérée'
        },
        {
            'nom': 'Fièvre aphteuse',
            'description': 'Maladie virale contagieuse très grave',
            'symptomes_typiques': 'Fièvre élevée, aphtes, boiterie, abattement sévère',
            'gravite': 'critique'
        },
        {
            'nom': 'Mastite',
            'description': 'Inflammation des mamelles, courante chez les vaches laitières',
            'symptomes_typiques': 'Gonflement des mamelles, fièvre modérée, changement du lait',
            'gravite': 'modérée'
        },
        {
            'nom': 'Parasitisme',
            'description': 'Infestation par des parasites internes ou externes',
            'symptomes_typiques': 'Perte de poids, abattement, diarrhée intermittente, poil terne',
            'gravite': 'faible'
        },
        {
            'nom': 'Acidose ruminale',
            'description': 'Déséquilibre du pH ruminal dû à une alimentation inadéquate',
            'symptomes_typiques': 'Perte d\'appétit, abattement, diarrhée, diminution de production',
            'gravite': 'modérée'
        },
        {
            'nom': 'Métrite',
            'description': 'Infection utérine survenant après le vêlage',
            'symptomes_typiques': 'Fièvre, écoulements vaginaux, perte d\'appétit',
            'gravite': 'élevée'
        },
        {
            'nom': 'Bonne santé',
            'description': 'Animal en parfaite santé',
            'symptomes_typiques': 'Aucun symptôme, comportement normal, bon appétit',
            'gravite': 'faible'
        }
    ]
    
    for maladie_data in maladies_data:
        maladie, created = Maladie.objects.get_or_create(
            nom=maladie_data['nom'],
            defaults=maladie_data
        )
        if created:
            print(f"✓ Maladie créée : {maladie.nom}")
    
    # Créer les traitements
    traitements_data = [
        {
            'nom': 'Antibiotique respiratoire',
            'description': 'Traitement antibiotique spécialisé pour les infections respiratoires',
            'dosage': '20 mg/kg de poids vif, 2 fois par jour',
            'duree_jours': 7,
            'contre_indications': 'Allergie aux pénicillines, gestation avancée',
            'maladies': ['Pneumonie']
        },
        {
            'nom': 'Réhydratation orale',
            'description': 'Solution de réhydratation pour combattre la déshydratation',
            'dosage': '2-4 litres par jour selon le poids',
            'duree_jours': 3,
            'contre_indications': 'Vomissements persistants',
            'maladies': ['Diarrhée infectieuse']
        },
        {
            'nom': 'Antiviral d\'urgence',
            'description': 'Traitement antiviral pour les maladies virales graves',
            'dosage': 'Selon protocole vétérinaire strict',
            'duree_jours': 10,
            'contre_indications': 'Aucune connue en situation d\'urgence',
            'maladies': ['Fièvre aphteuse']
        },
        {
            'nom': 'Anti-inflammatoire mammaire',
            'description': 'Traitement local et systémique pour les inflammations mammaires',
            'dosage': 'Application locale 3 fois par jour + injection systémique',
            'duree_jours': 5,
            'contre_indications': 'Lait destiné à la consommation humaine',
            'maladies': ['Mastite']
        },
        {
            'nom': 'Vermifuge à large spectre',
            'description': 'Traitement antiparasitaire couvrant la plupart des parasites',
            'dosage': '10 mg/kg de poids vif, dose unique',
            'duree_jours': 1,
            'contre_indications': 'Jeunes animaux de moins de 2 mois',
            'maladies': ['Parasitisme']
        },
        {
            'nom': 'Régulateur ruminal',
            'description': 'Probiotiques et régulateurs pour rétablir l\'équilibre ruminal',
            'dosage': '50g matin et soir avec les aliments',
            'duree_jours': 10,
            'contre_indications': 'Aucune connue',
            'maladies': ['Acidose ruminale']
        },
        {
            'nom': 'Antibiotique utérin',
            'description': 'Traitement spécialisé pour les infections utérines',
            'dosage': 'Injection intramusculaire selon poids',
            'duree_jours': 5,
            'contre_indications': 'Gestation en cours',
            'maladies': ['Métrite']
        }
    ]
    
    for trait_data in traitements_data:
        maladies_noms = trait_data.pop('maladies')
        traitement, created = Traitement.objects.get_or_create(
            nom=trait_data['nom'],
            defaults=trait_data
        )
        if created:
            # Associer les maladies
            for maladie_nom in maladies_noms:
                try:
                    maladie = Maladie.objects.get(nom=maladie_nom)
                    traitement.maladies.add(maladie)
                except Maladie.DoesNotExist:
                    pass
            print(f"✓ Traitement créé : {traitement.nom}")
    
    # Créer des animaux d'exemple
    animaux_data = [
        {
            'nom': 'Bella',
            'numero_identification': 'FR-001-2023',
            'type_animal': 'bovin',
            'race': 'Holstein',
            'sexe': 'F',
            'date_naissance': datetime(2020, 3, 15).date(),
            'poids': 650.0,
            'proprietaire': admin_user
        },
        {
            'nom': 'Taureau Max',
            'numero_identification': 'FR-002-2023',
            'type_animal': 'bovin',
            'race': 'Charolais',
            'sexe': 'M',
            'date_naissance': datetime(2018, 8, 22).date(),
            'poids': 900.0,
            'proprietaire': admin_user
        },
        {
            'nom': 'Mouton Blanc',
            'numero_identification': 'FR-003-2023',
            'type_animal': 'ovin',
            'race': 'Mérinos',
            'sexe': 'M',
            'date_naissance': datetime(2021, 5, 10).date(),
            'poids': 75.0,
            'proprietaire': admin_user
        },
        {
            'nom': 'Chèvre Lili',
            'numero_identification': 'FR-004-2023',
            'type_animal': 'caprin',
            'race': 'Alpine',
            'sexe': 'F',
            'date_naissance': datetime(2019, 12, 3).date(),
            'poids': 55.0,
            'proprietaire': admin_user
        },
        {
            'nom': 'Cochon Rose',
            'numero_identification': 'FR-005-2023',
            'type_animal': 'porcin',
            'race': 'Large White',
            'sexe': 'F',
            'date_naissance': datetime(2022, 1, 18).date(),
            'poids': 180.0,
            'proprietaire': admin_user
        }
    ]
    
    for animal_data in animaux_data:
        animal, created = Animal.objects.get_or_create(
            numero_identification=animal_data['numero_identification'],
            defaults=animal_data
        )
        if created:
            print(f"✓ Animal créé : {animal.nom}")
    
    # Créer quelques planifications de soins
    if Animal.objects.exists():
        animals = list(Animal.objects.all())
        today = timezone.now().date()
        
        soins_data = [
            {
                'animal': animals[0],
                'type_soin': 'vaccination',
                'nom_soin': 'Vaccination annuelle BVD',
                'description': 'Vaccination contre la diarrhée virale bovine',
                'date_prevue': timezone.make_aware(datetime.combine(today + timedelta(days=7), datetime.min.time())),
                'veterinaire_responsable': vet_user,
                'statut': 'planifie'
            },
            {
                'animal': animals[1],
                'type_soin': 'controle',
                'nom_soin': 'Contrôle de santé général',
                'description': 'Examen vétérinaire complet',
                'date_prevue': timezone.make_aware(datetime.combine(today + timedelta(days=3), datetime.min.time())),
                'veterinaire_responsable': vet_user,
                'statut': 'planifie'
            },
            {
                'animal': animals[2],
                'type_soin': 'vermifuge',
                'nom_soin': 'Vermifugation printanière',
                'description': 'Traitement antiparasitaire saisonnier',
                'date_prevue': timezone.make_aware(datetime.combine(today - timedelta(days=2), datetime.min.time())),
                'veterinaire_responsable': vet_user,
                'statut': 'planifie'  # En retard volontairement pour les tests
            }
        ]
        
        for soin_data in soins_data:
            soin, created = PlanificationSoin.objects.get_or_create(
                animal=soin_data['animal'],
                nom_soin=soin_data['nom_soin'],
                defaults=soin_data
            )
            if created:
                print(f"✓ Soin planifié : {soin.nom_soin} pour {soin.animal.nom}")
    
    print("✓ Données d'exemple créées avec succès!")


def train_ml_model():
    """Entraîner le modèle de machine learning"""
    print("Entraînement du modèle de machine learning...")
    
    try:
        # Créer et entraîner le modèle
        predictor = LivestockMLPredictor()
        accuracy = predictor.train_model()
        
        # Sauvegarder le modèle
        predictor.save_model()
        
        print(f"✓ Modèle entraîné avec succès!")
        print(f"✓ Précision du modèle : {accuracy:.2%}")
        print(f"✓ Modèle sauvegardé dans : {settings.ML_MODEL_PATH}")
        
        # Afficher l'importance des features
        print("\n📊 Importance des caractéristiques :")
        for feature, importance in predictor.get_feature_importance()[:5]:
            print(f"  - {feature}: {importance:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'entraînement : {e}")
        return False


def test_prediction():
    """Tester une prédiction avec le modèle"""
    print("\nTest de prédiction...")
    
    try:
        predictor = LivestockMLPredictor()
        predictor.load_model()
        
        # Symptômes de test (pneumonie probable)
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
        
        print(f"✓ Prédiction test réussie :")
        print(f"  - Maladie prédite : {result['predicted_disease']}")
        print(f"  - Confiance : {result['confidence']:.2%}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        return False


def main():
    """Fonction principale"""
    print("🐄 Configuration de SmartBétail")
    print("=" * 50)
    
    # 1. Créer les données d'exemple
    create_sample_data()
    print()
    
    # 2. Entraîner le modèle ML
    if train_ml_model():
        print()
        # 3. Tester la prédiction
        test_prediction()
    
    print("\n" + "=" * 50)
    print("✅ Configuration terminée avec succès!")
    print("\n📋 Prochaines étapes :")
    print("  1. Démarrer le serveur : python manage.py runserver")
    print("  2. Accéder à l'admin : http://localhost:8000/admin/")
    print("  3. Tester l'API : http://localhost:8000/api/")
    print("  4. Login admin : admin / admin123")
    print("  5. Login vétérinaire : veterinaire / vet123")


if __name__ == "__main__":
    main()