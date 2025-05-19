from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import joblib
import numpy as np
from .serializers import PredictionRequestSerializer
import os
from django.shortcuts import render
import pandas as pd
import json

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ml', 'model_rf.pkl')
ENCODER_PATH = os.path.join(os.path.dirname(__file__), 'ml', 'label_encoder.pkl')

class PredictAPIView(APIView):
    def post(self, request):
        serializer = PredictionRequestSerializer(data=request.data)
        if serializer.is_valid():
            commune = serializer.validated_data['commune']
            annee = serializer.validated_data['annee']

            # Charger le modèle et l'encodeur
            model = joblib.load(MODEL_PATH)
            le = joblib.load(ENCODER_PATH)

            # Vérifier si la commune existe dans l'encodeur
            if commune not in le.classes_:
                return Response(
                    {"error": "Commune inconnue."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            commune_enc = le.transform([commune])[0]
            X_pred = np.array([[commune_enc, annee]])
            y_pred = model.predict(X_pred)[0]

            return Response({
                "recettes": round(float(y_pred[0]), 2),
                "depenses": round(float(y_pred[1]), 2)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def predict_form(request):
    csv_path = os.path.join(os.path.dirname(__file__), 'ml', 'donnees_communes.csv')
    df = pd.read_csv(csv_path)
    communes = sorted(df['Commune'].unique())
    # Prépare un dict {commune: [{annee, recettes, depenses}, ...]}
    historique = {}
    for c in communes:
        rows = df[df['Commune'] == c][['Année', 'Recettes (M€)', 'Dépenses (M€)']].sort_values('Année')
        historique[c] = rows.to_dict(orient='records')
    return render(request, 'prediction/predict.html', {
        'communes': communes,
        'historique_json': json.dumps(historique)
    })

def home(request):
    return render(request, 'prediction/home.html')