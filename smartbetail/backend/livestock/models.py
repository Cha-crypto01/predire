from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


class Animal(models.Model):
    """Modèle représentant un animal du bétail"""
    ANIMAL_TYPES = [
        ('bovin', 'Bovin'),
        ('ovin', 'Ovin'),
        ('caprin', 'Caprin'),
        ('porcin', 'Porcin'),
        ('équidé', 'Équidé'),
    ]
    
    SEXES = [
        ('M', 'Mâle'),
        ('F', 'Femelle'),
    ]
    
    nom = models.CharField(max_length=100, verbose_name="Nom de l'animal")
    numero_identification = models.CharField(max_length=50, unique=True, verbose_name="Numéro d'identification")
    type_animal = models.CharField(max_length=20, choices=ANIMAL_TYPES, verbose_name="Type d'animal")
    race = models.CharField(max_length=100, verbose_name="Race")
    sexe = models.CharField(max_length=1, choices=SEXES, verbose_name="Sexe")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    poids = models.FloatField(null=True, blank=True, verbose_name="Poids (kg)")
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Propriétaire")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animaux"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.numero_identification})"
    
    @property
    def age_months(self):
        """Calcule l'âge en mois"""
        today = timezone.now().date()
        age = today - self.date_naissance
        return age.days // 30


class Maladie(models.Model):
    """Modèle représentant les maladies possibles"""
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la maladie")
    description = models.TextField(verbose_name="Description")
    symptomes_typiques = models.TextField(verbose_name="Symptômes typiques")
    gravite = models.CharField(max_length=20, choices=[
        ('faible', 'Faible'),
        ('modérée', 'Modérée'),
        ('élevée', 'Élevée'),
        ('critique', 'Critique'),
    ], default='modérée', verbose_name="Gravité")
    
    class Meta:
        verbose_name = "Maladie"
        verbose_name_plural = "Maladies"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Traitement(models.Model):
    """Modèle représentant les traitements possibles"""
    nom = models.CharField(max_length=100, verbose_name="Nom du traitement")
    description = models.TextField(verbose_name="Description du traitement")
    dosage = models.CharField(max_length=200, verbose_name="Dosage recommandé")
    duree_jours = models.IntegerField(verbose_name="Durée en jours")
    contre_indications = models.TextField(blank=True, verbose_name="Contre-indications")
    maladies = models.ManyToManyField(Maladie, related_name='traitements', verbose_name="Maladies traitées")
    
    class Meta:
        verbose_name = "Traitement"
        verbose_name_plural = "Traitements"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class SymptomeObserve(models.Model):
    """Modèle pour enregistrer les symptômes observés sur un animal"""
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='symptomes_observes')
    temperature = models.FloatField(null=True, blank=True, verbose_name="Température (°C)")
    frequence_cardiaque = models.IntegerField(null=True, blank=True, verbose_name="Fréquence cardiaque (bpm)")
    frequence_respiratoire = models.IntegerField(null=True, blank=True, verbose_name="Fréquence respiratoire")
    niveau_activite = models.IntegerField(choices=[
        (1, 'Très faible'),
        (2, 'Faible'),
        (3, 'Normal'),
        (4, 'Élevé'),
        (5, 'Très élevé'),
    ], default=3, verbose_name="Niveau d'activité")
    appetit = models.IntegerField(choices=[
        (1, 'Aucun appétit'),
        (2, 'Appétit faible'),
        (3, 'Appétit normal'),
        (4, 'Bon appétit'),
        (5, 'Appétit excessif'),
    ], default=3, verbose_name="Appétit")
    
    # Symptômes observables (booléens)
    fievre = models.BooleanField(default=False, verbose_name="Fièvre")
    toux = models.BooleanField(default=False, verbose_name="Toux")
    diarrhee = models.BooleanField(default=False, verbose_name="Diarrhée")
    ecoulement_nasal = models.BooleanField(default=False, verbose_name="Écoulement nasal")
    boiterie = models.BooleanField(default=False, verbose_name="Boiterie")
    abattement = models.BooleanField(default=False, verbose_name="Abattement")
    perte_poids = models.BooleanField(default=False, verbose_name="Perte de poids")
    
    notes_veterinaire = models.TextField(blank=True, verbose_name="Notes vétérinaire")
    date_observation = models.DateTimeField(auto_now_add=True, verbose_name="Date d'observation")
    
    class Meta:
        verbose_name = "Symptôme observé"
        verbose_name_plural = "Symptômes observés"
        ordering = ['-date_observation']
    
    def __str__(self):
        return f"Symptômes de {self.animal.nom} - {self.date_observation.strftime('%d/%m/%Y')}"


class Diagnostic(models.Model):
    """Modèle pour enregistrer les diagnostics (prédictions IA + validation vétérinaire)"""
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='diagnostics')
    symptome_observe = models.ForeignKey(SymptomeObserve, on_delete=models.CASCADE)
    maladie_predite = models.ForeignKey(Maladie, on_delete=models.CASCADE, related_name='diagnostics_predits')
    probabilite = models.FloatField(verbose_name="Probabilité de la prédiction")
    confirme_par_veterinaire = models.BooleanField(default=False, verbose_name="Confirmé par vétérinaire")
    veterinaire = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    traitement_recommande = models.ForeignKey(Traitement, on_delete=models.SET_NULL, null=True, blank=True)
    notes_diagnostic = models.TextField(blank=True, verbose_name="Notes du diagnostic")
    date_diagnostic = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Diagnostic"
        verbose_name_plural = "Diagnostics"
        ordering = ['-date_diagnostic']
    
    def __str__(self):
        return f"Diagnostic {self.animal.nom} - {self.maladie_predite.nom} ({self.probabilite:.1%})"


class PlanificationSoin(models.Model):
    """Modèle pour planifier les vaccinations et soins préventifs"""
    TYPE_SOIN = [
        ('vaccination', 'Vaccination'),
        ('vermifuge', 'Vermifuge'),
        ('controle', 'Contrôle vétérinaire'),
        ('traitement', 'Traitement'),
        ('autre', 'Autre'),
    ]
    
    STATUT = [
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('reporte', 'Reporté'),
        ('annule', 'Annulé'),
    ]
    
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='soins_planifies')
    type_soin = models.CharField(max_length=20, choices=TYPE_SOIN, verbose_name="Type de soin")
    nom_soin = models.CharField(max_length=200, verbose_name="Nom du soin")
    description = models.TextField(blank=True, verbose_name="Description")
    date_prevue = models.DateTimeField(verbose_name="Date prévue")
    date_realisation = models.DateTimeField(null=True, blank=True, verbose_name="Date de réalisation")
    statut = models.CharField(max_length=20, choices=STATUT, default='planifie', verbose_name="Statut")
    veterinaire_responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rappel_envoye = models.BooleanField(default=False, verbose_name="Rappel envoyé")
    notes = models.TextField(blank=True, verbose_name="Notes")
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Planification de soin"
        verbose_name_plural = "Planifications de soins"
        ordering = ['date_prevue']
    
    def __str__(self):
        return f"{self.nom_soin} - {self.animal.nom} ({self.date_prevue.strftime('%d/%m/%Y')})"
    
    @property
    def est_en_retard(self):
        """Vérifie si le soin est en retard"""
        return self.statut == 'planifie' and self.date_prevue < timezone.now()
    
    @property
    def jours_jusqu_echeance(self):
        """Calcule le nombre de jours jusqu'à l'échéance"""
        if self.statut != 'planifie':
            return None
        delta = self.date_prevue - timezone.now()
        return delta.days
