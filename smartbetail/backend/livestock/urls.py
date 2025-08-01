from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Créer le router pour les ViewSets
router = DefaultRouter()
router.register(r'animals', views.AnimalViewSet, basename='animal')
router.register(r'diseases', views.MaladieViewSet)
router.register(r'treatments', views.TraitementViewSet)
router.register(r'symptoms', views.SymptomeObserveViewSet, basename='symptome')
router.register(r'diagnostics', views.DiagnosticViewSet, basename='diagnostic')
router.register(r'schedule', views.PlanificationSoinViewSet, basename='planification')

urlpatterns = [
    # Routes du router
    path('', include(router.urls)),
    
    # Endpoints spéciaux pour l'IA
    path('predict/', views.predict_disease, name='predict-disease'),
    path('recommend/', views.recommend_treatment, name='recommend-treatment'),
    path('dashboard/', views.dashboard_data, name='dashboard-data'),
    path('health/', views.health_check, name='health-check'),
]