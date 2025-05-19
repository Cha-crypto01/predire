from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('commune', 'year', 'predicted_revenue', 'predicted_expense')
    search_fields = ('commune',)
    list_filter = ('year',)