from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('prediction.urls')),
    path('', include('prediction.urls')),  # Ajoute cette ligne pour la racine
]