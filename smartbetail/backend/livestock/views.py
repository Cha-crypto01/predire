from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User

from .models import (
    Animal, Maladie, Traitement, SymptomeObserve, 
    Diagnostic, PlanificationSoin
)
from .serializers import (
    AnimalSerializer, MaladieSerializer, TraitementSerializer,
    SymptomeObserveSerializer, DiagnosticSerializer, PlanificationSoinSerializer,
    PredictionInputSerializer, PredictionOutputSerializer, RecommendationInputSerializer,
    DashboardSerializer, UserSerializer
)
from ml_model.ml_predictor import get_predictor


class AnimalViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les animaux
    """
    serializer_class = AnimalSerializer
    permission_classes = []  # Temporairement ouvert pour les tests
    
    def get_queryset(self):
        queryset = Animal.objects.all().select_related('proprietaire')
        # Filtrer par propriétaire si l'utilisateur est connecté
        if self.request.user.is_authenticated:
            queryset = queryset.filter(proprietaire=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        # Associer l'animal au propriétaire connecté
        if self.request.user.is_authenticated:
            serializer.save(proprietaire=self.request.user)
        else:
            # Pour les tests, créer un utilisateur par défaut
            user, created = User.objects.get_or_create(
                username='admin',
                defaults={'email': 'admin@smartbetail.com'}
            )
            serializer.save(proprietaire=user)


class MaladieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet en lecture seule pour les maladies
    """
    queryset = Maladie.objects.all()
    serializer_class = MaladieSerializer
    permission_classes = []


class TraitementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet en lecture seule pour les traitements
    """
    queryset = Traitement.objects.all().prefetch_related('maladies')
    serializer_class = TraitementSerializer
    permission_classes = []


class SymptomeObserveViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les observations de symptômes
    """
    serializer_class = SymptomeObserveSerializer
    permission_classes = []
    
    def get_queryset(self):
        queryset = SymptomeObserve.objects.all().select_related('animal')
        
        # Filtrer par animal si spécifié
        animal_id = self.request.query_params.get('animal_id')
        if animal_id:
            queryset = queryset.filter(animal_id=animal_id)
        
        return queryset.order_by('-date_observation')


class DiagnosticViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les diagnostics
    """
    serializer_class = DiagnosticSerializer
    permission_classes = []
    
    def get_queryset(self):
        queryset = Diagnostic.objects.all().select_related(
            'animal', 'maladie_predite', 'traitement_recommande', 'veterinaire'
        )
        
        # Filtrer par animal si spécifié
        animal_id = self.request.query_params.get('animal_id')
        if animal_id:
            queryset = queryset.filter(animal_id=animal_id)
        
        return queryset.order_by('-date_diagnostic')


class PlanificationSoinViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer la planification des soins
    """
    serializer_class = PlanificationSoinSerializer
    permission_classes = []
    
    def get_queryset(self):
        queryset = PlanificationSoin.objects.all().select_related(
            'animal', 'veterinaire_responsable'
        )
        
        # Filtrer par animal si spécifié
        animal_id = self.request.query_params.get('animal_id')
        if animal_id:
            queryset = queryset.filter(animal_id=animal_id)
        
        # Filtrer par statut
        statut = self.request.query_params.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        
        # Filtrer les soins en retard
        en_retard = self.request.query_params.get('en_retard')
        if en_retard == 'true':
            queryset = queryset.filter(
                statut='planifie',
                date_prevue__lt=timezone.now()
            )
        
        return queryset.order_by('date_prevue')
    
    @action(detail=False, methods=['get'])
    def en_retard(self, request):
        """
        Endpoint pour récupérer les soins en retard
        """
        soins_retard = self.get_queryset().filter(
            statut='planifie',
            date_prevue__lt=timezone.now()
        )
        serializer = self.get_serializer(soins_retard, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def cette_semaine(self, request):
        """
        Endpoint pour récupérer les soins de cette semaine
        """
        aujourd_hui = timezone.now().date()
        fin_semaine = aujourd_hui + timedelta(days=7)
        
        soins_semaine = self.get_queryset().filter(
            statut='planifie',
            date_prevue__date__range=[aujourd_hui, fin_semaine]
        )
        serializer = self.get_serializer(soins_semaine, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def predict_disease(request):
    """
    Endpoint pour prédire une maladie basée sur les symptômes
    URL: /api/predict/
    """
    serializer = PredictionInputSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'errors': serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Récupérer les données validées
        validated_data = serializer.validated_data
        animal_id = validated_data.pop('animal_id')
        notes_veterinaire = validated_data.pop('notes_veterinaire', '')
        
        # Récupérer l'animal
        animal = get_object_or_404(Animal, id=animal_id)
        
        # Créer l'observation de symptômes
        symptome_data = validated_data.copy()
        symptome_data['animal_id'] = animal_id
        symptome_data['notes_veterinaire'] = notes_veterinaire
        
        symptome_serializer = SymptomeObserveSerializer(data=symptome_data)
        if symptome_serializer.is_valid():
            symptome_observe = symptome_serializer.save()
        else:
            return Response(
                {'errors': symptome_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Utiliser le modèle ML pour la prédiction
        predictor = get_predictor()
        prediction_result = predictor.predict(validated_data)
        
        # Récupérer ou créer la maladie prédite
        disease_name = prediction_result['predicted_disease']
        disease_info = prediction_result['disease_info']
        
        maladie, created = Maladie.objects.get_or_create(
            nom=disease_info.get('nom', disease_name),
            defaults={
                'description': disease_info.get('description', ''),
                'symptomes_typiques': disease_info.get('symptomes_typiques', ''),
                'gravite': disease_info.get('gravite', 'modérée')
            }
        )
        
        # Créer le diagnostic
        diagnostic = Diagnostic.objects.create(
            animal=animal,
            symptome_observe=symptome_observe,
            maladie_predite=maladie,
            probabilite=prediction_result['confidence']
        )
        
        # Chercher un traitement recommandé
        traitement_recommande = None
        if maladie.traitements.exists():
            traitement_recommande = maladie.traitements.first()
            diagnostic.traitement_recommande = traitement_recommande
            diagnostic.save()
        
        # Déterminer le niveau de confiance
        confidence = prediction_result['confidence']
        if confidence >= 0.8:
            niveau_confiance = 'Très élevé'
        elif confidence >= 0.6:
            niveau_confiance = 'Élevé'
        elif confidence >= 0.4:
            niveau_confiance = 'Modéré'
        else:
            niveau_confiance = 'Faible'
        
        # Générer des recommandations
        recommandations = []
        if confidence < 0.6:
            recommandations.append("Consulter un vétérinaire pour confirmation")
        
        if maladie.gravite in ['élevée', 'critique']:
            recommandations.append("Isoler l'animal si nécessaire")
            recommandations.append("Surveillance rapprochée recommandée")
        
        if traitement_recommande:
            recommandations.append(f"Traitement suggéré : {traitement_recommande.nom}")
        
        if not recommandations:
            recommandations.append("Continuer la surveillance régulière")
        
        # Préparer la réponse
        response_data = {
            'maladie_predite': MaladieSerializer(maladie).data,
            'probabilite': confidence,
            'traitement_recommande': TraitementSerializer(traitement_recommande).data if traitement_recommande else None,
            'niveau_confiance': niveau_confiance,
            'recommandations': recommandations,
            'diagnostic_id': diagnostic.id,
            'symptome_observe_id': symptome_observe.id
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la prédiction : {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def recommend_treatment(request):
    """
    Endpoint pour recommander un traitement basé sur une maladie
    URL: /api/recommend/
    """
    serializer = RecommendationInputSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        maladie_id = serializer.validated_data['maladie_id']
        animal_id = serializer.validated_data['animal_id']
        
        # Récupérer la maladie et l'animal
        maladie = get_object_or_404(Maladie, id=maladie_id)
        animal = get_object_or_404(Animal, id=animal_id)
        
        # Récupérer les traitements associés à cette maladie
        traitements = maladie.traitements.all()
        
        if not traitements.exists():
            return Response(
                {'message': 'Aucun traitement spécifique trouvé pour cette maladie'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Sérialiser les traitements
        traitements_data = TraitementSerializer(traitements, many=True).data
        
        # Recommandations générales basées sur la gravité
        recommandations_generales = []
        
        if maladie.gravite == 'critique':
            recommandations_generales.extend([
                "Intervention vétérinaire urgente requise",
                "Isoler l'animal immédiatement",
                "Surveiller les signes vitaux en continu"
            ])
        elif maladie.gravite == 'élevée':
            recommandations_generales.extend([
                "Consulter un vétérinaire dans les 24h",
                "Surveillance rapprochée recommandée",
                "Éviter le stress de l'animal"
            ])
        elif maladie.gravite == 'modérée':
            recommandations_generales.extend([
                "Surveillance quotidienne",
                "Consulter un vétérinaire si aggravation",
                "Maintenir l'animal au calme"
            ])
        else:  # faible
            recommandations_generales.extend([
                "Surveillance régulière",
                "Traitement préventif possible",
                "Améliorer les conditions d'élevage"
            ])
        
        # Recommandations spécifiques à l'animal
        recommandations_specifiques = []
        if animal.age_months < 6:
            recommandations_specifiques.append("Dosage adapté aux jeunes animaux")
        elif animal.age_months > 60:
            recommandations_specifiques.append("Surveillance renforcée pour les animaux âgés")
        
        if animal.poids:
            recommandations_specifiques.append(f"Adapter le dosage au poids : {animal.poids} kg")
        
        response_data = {
            'maladie': MaladieSerializer(maladie).data,
            'animal': AnimalSerializer(animal).data,
            'traitements_recommandes': traitements_data,
            'recommandations_generales': recommandations_generales,
            'recommandations_specifiques': recommandations_specifiques,
            'priorite': maladie.gravite
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la recommandation : {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def dashboard_data(request):
    """
    Endpoint pour récupérer les données du dashboard
    URL: /api/dashboard/
    """
    try:
        # Statistiques générales
        total_animaux = Animal.objects.count()
        
        # Animaux avec diagnostics récents (dernières 30 jours)
        date_limite = timezone.now() - timedelta(days=30)
        animaux_malades = Diagnostic.objects.filter(
            date_diagnostic__gte=date_limite,
            confirme_par_veterinaire=False
        ).values('animal').distinct().count()
        
        # Soins en retard
        soins_en_retard = PlanificationSoin.objects.filter(
            statut='planifie',
            date_prevue__lt=timezone.now()
        ).count()
        
        # Soins cette semaine
        aujourd_hui = timezone.now().date()
        fin_semaine = aujourd_hui + timedelta(days=7)
        soins_cette_semaine = PlanificationSoin.objects.filter(
            statut='planifie',
            date_prevue__date__range=[aujourd_hui, fin_semaine]
        ).count()
        
        # Diagnostics récents (5 derniers)
        diagnostics_recents = Diagnostic.objects.select_related(
            'animal', 'maladie_predite', 'traitement_recommande'
        ).order_by('-date_diagnostic')[:5]
        
        # Soins urgents (en retard + prochains 3 jours)
        date_limite_urgence = aujourd_hui + timedelta(days=3)
        soins_urgents = PlanificationSoin.objects.filter(
            statut='planifie',
            date_prevue__date__lte=date_limite_urgence
        ).select_related('animal').order_by('date_prevue')[:10]
        
        # Répartition des maladies (30 derniers jours)
        repartition_maladies = {}
        maladies_stats = Diagnostic.objects.filter(
            date_diagnostic__gte=date_limite
        ).values('maladie_predite__nom').annotate(
            count=Count('id')
        ).order_by('-count')
        
        for stat in maladies_stats:
            repartition_maladies[stat['maladie_predite__nom']] = stat['count']
        
        # Répartition par type d'animal
        repartition_types_animaux = {}
        types_stats = Animal.objects.values('type_animal').annotate(
            count=Count('id')
        ).order_by('-count')
        
        for stat in types_stats:
            repartition_types_animaux[stat['type_animal']] = stat['count']
        
        # Préparer les données de réponse
        dashboard_data = {
            'total_animaux': total_animaux,
            'animaux_malades': animaux_malades,
            'soins_en_retard': soins_en_retard,
            'soins_cette_semaine': soins_cette_semaine,
            'diagnostics_recents': DiagnosticSerializer(diagnostics_recents, many=True).data,
            'soins_urgents': PlanificationSoinSerializer(soins_urgents, many=True).data,
            'repartition_maladies': repartition_maladies,
            'repartition_types_animaux': repartition_types_animaux
        }
        
        return Response(dashboard_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la récupération des données du dashboard : {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def health_check(request):
    """
    Endpoint de vérification de santé de l'API
    """
    try:
        # Vérifier que le modèle ML est chargé
        predictor = get_predictor()
        model_loaded = predictor.model is not None
        
        # Statistiques de base
        stats = {
            'api_status': 'OK',
            'model_loaded': model_loaded,
            'total_animals': Animal.objects.count(),
            'total_diseases': Maladie.objects.count(),
            'total_treatments': Traitement.objects.count(),
            'total_diagnostics': Diagnostic.objects.count(),
            'timestamp': timezone.now().isoformat()
        }
        
        return Response(stats, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e), 'api_status': 'ERROR'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
