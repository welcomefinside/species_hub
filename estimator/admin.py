from django.contrib import admin
from .models import Estimator, TrainedEstimator

# class EstimatorAdmin(admin.ModelAdmin):
    # def save_model(self, request, obj, form, change):
    #     if not obj.scaler_set:
    #         super().save_model(self, request, obj, form, change)

# admin.site.register(Estimator, EstimatorAdmin)
admin.site.register(Estimator)
admin.site.register(TrainedEstimator)