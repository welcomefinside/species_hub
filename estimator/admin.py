from django.contrib import admin
from .models import Estimator, TrainedEstimator

admin.site.register(Estimator)
admin.site.register(TrainedEstimator)