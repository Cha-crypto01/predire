from django.db import models

class Commune(models.Model):
    name = models.CharField(max_length=100, unique=True)
    population = models.IntegerField()
    area = models.FloatField()

    def __str__(self):
        return self.name

class Prediction(models.Model):
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)
    year = models.IntegerField()
    predicted_revenue = models.FloatField()
    predicted_expense = models.FloatField()

    def __str__(self):
        return f"Prediction for {self.commune.name} in {self.year}"