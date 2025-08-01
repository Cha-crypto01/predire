from django.contrib import admin
from .models import Animal, Maladie, Traitement, SymptomeObserve, Diagnostic, PlanificationSoin


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    """Administration des animaux"""
    list_display = ['nom', 'numero_identification', 'type_animal', 'race', 'sexe', 'age_months', 'proprietaire']
    list_filter = ['type_animal', 'sexe', 'race', 'proprietaire']
    search_fields = ['nom', 'numero_identification', 'race']
    readonly_fields = ['age_months', 'date_creation', 'date_modification']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('nom', 'numero_identification', 'type_animal', 'race', 'sexe')
        }),
        ('Détails physiques', {
            'fields': ('date_naissance', 'poids', 'age_months')
        }),
        ('Propriété', {
            'fields': ('proprietaire',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Maladie)
class MaladieAdmin(admin.ModelAdmin):
    """Administration des maladies"""
    list_display = ['nom', 'gravite', 'nombre_traitements']
    list_filter = ['gravite']
    search_fields = ['nom', 'description', 'symptomes_typiques']
    
    def nombre_traitements(self, obj):
        return obj.traitements.count()
    nombre_traitements.short_description = 'Nb traitements'


@admin.register(Traitement)
class TraitementAdmin(admin.ModelAdmin):
    """Administration des traitements"""
    list_display = ['nom', 'duree_jours', 'nombre_maladies']
    list_filter = ['duree_jours']
    search_fields = ['nom', 'description', 'dosage']
    filter_horizontal = ['maladies']
    
    def nombre_maladies(self, obj):
        return obj.maladies.count()
    nombre_maladies.short_description = 'Nb maladies traitées'


@admin.register(SymptomeObserve)
class SymptomeObserveAdmin(admin.ModelAdmin):
    """Administration des symptômes observés"""
    list_display = ['animal', 'date_observation', 'temperature', 'niveau_activite', 'appetit', 'symptomes_presents']
    list_filter = ['date_observation', 'niveau_activite', 'appetit', 'fievre', 'toux', 'diarrhee']
    search_fields = ['animal__nom', 'animal__numero_identification', 'notes_veterinaire']
    readonly_fields = ['date_observation']
    date_hierarchy = 'date_observation'
    
    fieldsets = (
        ('Animal et date', {
            'fields': ('animal', 'date_observation')
        }),
        ('Données vitales', {
            'fields': ('temperature', 'frequence_cardiaque', 'frequence_respiratoire')
        }),
        ('Comportement', {
            'fields': ('niveau_activite', 'appetit')
        }),
        ('Symptômes observés', {
            'fields': ('fievre', 'toux', 'diarrhee', 'ecoulement_nasal', 'boiterie', 'abattement', 'perte_poids')
        }),
        ('Notes', {
            'fields': ('notes_veterinaire',)
        }),
    )
    
    def symptomes_presents(self, obj):
        symptomes = []
        if obj.fievre: symptomes.append('Fièvre')
        if obj.toux: symptomes.append('Toux')
        if obj.diarrhee: symptomes.append('Diarrhée')
        if obj.ecoulement_nasal: symptomes.append('Écoulement nasal')
        if obj.boiterie: symptomes.append('Boiterie')
        if obj.abattement: symptomes.append('Abattement')
        if obj.perte_poids: symptomes.append('Perte de poids')
        return ', '.join(symptomes) if symptomes else 'Aucun'
    symptomes_presents.short_description = 'Symptômes présents'


@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):
    """Administration des diagnostics"""
    list_display = ['animal', 'maladie_predite', 'probabilite_percent', 'confirme_par_veterinaire', 'date_diagnostic']
    list_filter = ['confirme_par_veterinaire', 'maladie_predite', 'date_diagnostic']
    search_fields = ['animal__nom', 'maladie_predite__nom', 'notes_diagnostic']
    readonly_fields = ['date_diagnostic', 'probabilite_percent']
    date_hierarchy = 'date_diagnostic'
    
    def probabilite_percent(self, obj):
        return f"{obj.probabilite:.1%}"
    probabilite_percent.short_description = 'Probabilité'
    
    fieldsets = (
        ('Diagnostic', {
            'fields': ('animal', 'symptome_observe', 'maladie_predite', 'probabilite', 'probabilite_percent')
        }),
        ('Validation', {
            'fields': ('confirme_par_veterinaire', 'veterinaire')
        }),
        ('Traitement', {
            'fields': ('traitement_recommande',)
        }),
        ('Notes et date', {
            'fields': ('notes_diagnostic', 'date_diagnostic')
        }),
    )


@admin.register(PlanificationSoin)
class PlanificationSoinAdmin(admin.ModelAdmin):
    """Administration de la planification des soins"""
    list_display = ['animal', 'nom_soin', 'type_soin', 'date_prevue', 'statut', 'est_en_retard_display', 'jours_echeance']
    list_filter = ['type_soin', 'statut', 'date_prevue']
    search_fields = ['animal__nom', 'nom_soin', 'description']
    readonly_fields = ['date_creation', 'est_en_retard', 'jours_jusqu_echeance']
    date_hierarchy = 'date_prevue'
    
    fieldsets = (
        ('Soin planifié', {
            'fields': ('animal', 'type_soin', 'nom_soin', 'description')
        }),
        ('Planification', {
            'fields': ('date_prevue', 'veterinaire_responsable', 'statut')
        }),
        ('Réalisation', {
            'fields': ('date_realisation', 'notes')
        }),
        ('Statut et rappels', {
            'fields': ('rappel_envoye', 'est_en_retard', 'jours_jusqu_echeance')
        }),
        ('Métadonnées', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        }),
    )
    
    def est_en_retard_display(self, obj):
        return obj.est_en_retard
    est_en_retard_display.short_description = 'En retard'
    est_en_retard_display.boolean = True
    
    def jours_echeance(self, obj):
        jours = obj.jours_jusqu_echeance
        if jours is None:
            return '-'
        elif jours < 0:
            return f"En retard de {abs(jours)} jour(s)"
        elif jours == 0:
            return "Aujourd'hui"
        else:
            return f"Dans {jours} jour(s)"
    jours_echeance.short_description = "Échéance"


# Configuration de l'admin
admin.site.site_header = "Administration SmartBétail"
admin.site.site_title = "SmartBétail Admin"
admin.site.index_title = "Gestion du bétail intelligent"
