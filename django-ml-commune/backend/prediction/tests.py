from django.test import TestCase
from .models import Prediction
from .serializers import PredictionSerializer

class PredictionModelTest(TestCase):
    def setUp(self):
        self.prediction = Prediction.objects.create(
            commune='Test Commune',
            year=2023,
            recette=100000,
            depense=80000
        )

    def test_prediction_creation(self):
        self.assertEqual(self.prediction.commune, 'Test Commune')
        self.assertEqual(self.prediction.year, 2023)
        self.assertEqual(self.prediction.recette, 100000)
        self.assertEqual(self.prediction.depense, 80000)

class PredictionSerializerTest(TestCase):
    def setUp(self):
        self.prediction = Prediction.objects.create(
            commune='Test Commune',
            year=2023,
            recette=100000,
            depense=80000
        )
        self.serializer = PredictionSerializer(instance=self.prediction)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'commune', 'year', 'recette', 'depense']))

    def test_serializer_field_values(self):
        data = self.serializer.data
        self.assertEqual(data['commune'], self.prediction.commune)
        self.assertEqual(data['year'], self.prediction.year)
        self.assertEqual(data['recette'], self.prediction.recette)
        self.assertEqual(data['depense'], self.prediction.depense)