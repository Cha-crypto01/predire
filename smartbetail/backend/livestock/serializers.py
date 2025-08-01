from rest_framework import serializers
from .models import Animal, Maladie, Traitement, SymptomeObserve, Diagnostic, PlanificationSoin
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer pour les utilisateurs"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class MaladieSerializer(serializers.ModelSerializer):
    """Serializer pour les maladies"""
    class Meta:
        model = Maladie
        fields = ['id', 'nom', 'description', 'symptomes_typiques', 'gravite']


class TraitementSerializer(serializers.ModelSerializer):
    """Serializer pour les traitements"""
    maladies = MaladieSerializer(many=True, read_only=True)
    
    class Meta:
        model = Traitement
        fields = ['id', 'nom', 'description', 'dosage', 'duree_jours', 'contre_indications', 'maladies']


class AnimalSerializer(serializers.ModelSerializer):
    """Serializer pour les animaux"""
    proprietaire = UserSerializer(read_only=True)
    age_months = serializers.ReadOnlyField()
    
    class Meta:
        model = Animal
        fields = [
            'id', 'nom', 'numero_identification', 'type_animal', 'race', 
            'sexe', 'date_naissance', 'poids', 'proprietaire', 'age_months',
            'date_creation', 'date_modification'
        ]
        read_only_fields = ['date_creation', 'date_modification']


class SymptomeObserveSerializer(serializers.ModelSerializer):
    """Serializer pour les symptômes observés"""
    animal = AnimalSerializer(read_only=True)
    animal_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = SymptomeObserve
        fields = [
            'id', 'animal', 'animal_id', 'temperature', 'frequence_cardiaque',
            'frequence_respiratoire', 'niveau_activite', 'appetit', 'fievre',
            'toux', 'diarrhee', 'ecoulement_nasal', 'boiterie', 'abattement',
            'perte_poids', 'notes_veterinaire', 'date_observation'
        ]
        read_only_fields = ['date_observation']


class DiagnosticSerializer(serializers.ModelSerializer):
    """Serializer pour les diagnostics"""
    animal = AnimalSerializer(read_only=True)
    maladie_predite = MaladieSerializer(read_only=True)
    traitement_recommande = TraitementSerializer(read_only=True)
    veterinaire = UserSerializer(read_only=True)
    symptome_observe = SymptomeObserveSerializer(read_only=True)
    
    class Meta:
        model = Diagnostic
        fields = [
            'id', 'animal', 'symptome_observe', 'maladie_predite', 'probabilite',
            'confirme_par_veterinaire', 'veterinaire', 'traitement_recommande',
            'notes_diagnostic', 'date_diagnostic'
        ]
        read_only_fields = ['date_diagnostic']


class PlanificationSoinSerializer(serializers.ModelSerializer):
    """Serializer pour la planification des soins"""
    animal = AnimalSerializer(read_only=True)
    animal_id = serializers.IntegerField(write_only=True)
    veterinaire_responsable = UserSerializer(read_only=True)
    veterinaire_responsable_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    est_en_retard = serializers.ReadOnlyField()
    jours_jusqu_echeance = serializers.ReadOnlyField()
    
    class Meta:
        model = PlanificationSoin
        fields = [
            'id', 'animal', 'animal_id', 'type_soin', 'nom_soin', 'description',
            'date_prevue', 'date_realisation', 'statut', 'veterinaire_responsable',
            'veterinaire_responsable_id', 'rappel_envoye', 'notes', 'est_en_retard',
            'jours_jusqu_echeance', 'date_creation'
        ]
        read_only_fields = ['date_creation']


class PredictionInputSerializer(serializers.Serializer):
    """Serializer pour les données d'entrée de prédiction"""
    animal_id = serializers.IntegerField()
    temperature = serializers.FloatField(required=False, allow_null=True)
    frequence_cardiaque = serializers.IntegerField(required=False, allow_null=True)
    frequence_respiratoire = serializers.IntegerField(required=False, allow_null=True)
    niveau_activite = serializers.IntegerField(min_value=1, max_value=5)
    appetit = serializers.IntegerField(min_value=1, max_value=5)
    fievre = serializers.BooleanField(default=False)
    toux = serializers.BooleanField(default=False)
    diarrhee = serializers.BooleanField(default=False)
    ecoulement_nasal = serializers.BooleanField(default=False)
    boiterie = serializers.BooleanField(default=False)
    abattement = serializers.BooleanField(default=False)
    perte_poids = serializers.BooleanField(default=False)
    notes_veterinaire = serializers.CharField(required=False, allow_blank=True)
    
    def validate_animal_id(self, value):
        """Valide que l'animal existe"""
        try:
            Animal.objects.get(id=value)
        except Animal.DoesNotExist:
            raise serializers.ValidationError("Animal non trouvé")
        return value


class PredictionOutputSerializer(serializers.Serializer):
    """Serializer pour les résultats de prédiction"""
    maladie_predite = MaladieSerializer()
    probabilite = serializers.FloatField()
    traitement_recommande = TraitementSerializer(allow_null=True)
    niveau_confiance = serializers.CharField()
    recommandations = serializers.ListField(child=serializers.CharField())


class RecommendationInputSerializer(serializers.Serializer):
    """Serializer pour demander une recommandation de traitement"""
    maladie_id = serializers.IntegerField()
    animal_id = serializers.IntegerField()
    
    def validate_maladie_id(self, value):
        """Valide que la maladie existe"""
        try:
            Maladie.objects.get(id=value)
        except Maladie.DoesNotExist:
            raise serializers.ValidationError("Maladie non trouvée")
        return value
    
    def validate_animal_id(self, value):
        """Valide que l'animal existe"""
        try:
            Animal.objects.get(id=value)
        except Animal.DoesNotExist:
            raise serializers.ValidationError("Animal non trouvé")
        return value


class DashboardSerializer(serializers.Serializer):
    """Serializer pour les données du dashboard"""
    total_animaux = serializers.IntegerField()
    animaux_malades = serializers.IntegerField()
    soins_en_retard = serializers.IntegerField()
    soins_cette_semaine = serializers.IntegerField()
    diagnostics_recents = DiagnosticSerializer(many=True)
    soins_urgents = PlanificationSoinSerializer(many=True)
    repartition_maladies = serializers.DictField()
    repartition_types_animaux = serializers.DictField()