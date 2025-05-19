from django.urls import path
from .views import PredictAPIView, predict_form, home

urlpatterns = [
    path('', home, name='home'),
    path('predict/', PredictAPIView.as_view(), name='predict'),
    path('form/', predict_form, name='predict_form'),
]