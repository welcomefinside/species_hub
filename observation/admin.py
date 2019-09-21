from django.contrib import admin
from observation.models import Observation, Species

# Register your models here.
def train_estimator(modeladmin, request, queryset):
    ## passing the quertsets to other views which is doing the training
    # for item in queryset:
    #     print(item.ufi)
    return
    

class ObservationAdmin(admin.ModelAdmin):
    list_display = ['ufi', 'species', 'date_added', 'date_modified']
    actions = [train_estimator]

admin.site.register(Observation, ObservationAdmin)
admin.site.register(Species)