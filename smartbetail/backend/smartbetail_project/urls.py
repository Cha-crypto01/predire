"""
URL configuration for smartbetail_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    """Endpoint racine de l'API avec documentation"""
    return JsonResponse({
        'message': 'Bienvenue sur l\'API SmartBétail',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'health': '/api/health/',
            'dashboard': '/api/dashboard/',
            'predict': '/api/predict/',
            'recommend': '/api/recommend/',
            'animals': '/api/animals/',
            'diseases': '/api/diseases/',
            'treatments': '/api/treatments/',
            'symptoms': '/api/symptoms/',
            'diagnostics': '/api/diagnostics/',
            'schedule': '/api/schedule/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('livestock.urls')),
    path('', api_root, name='api-root'),
]
