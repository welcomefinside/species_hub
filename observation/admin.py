from django.contrib import admin
from observation.models import Observation, Species

# Register your models here.

admin.site.register(Observation)
admin.site.register(Species)