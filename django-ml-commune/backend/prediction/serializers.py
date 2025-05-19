from rest_framework import serializers
from .models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'

class PredictionRequestSerializer(serializers.Serializer):
    commune = serializers.CharField()
    annee = serializers.IntegerField()