from django.contrib import admin
from observation.models import Observation, Species, ObservationImport
from django.utils.safestring import mark_safe
from django.urls import reverse

# Register your models here.
def train_estimator(modeladmin, request, queryset):
    ## passing the quertsets to other views which is doing the training
    # for item in queryset:
    #     print(item.ufi)
    return
    
def ipdb_helper(modeladmin, request, queryset):
    import ipdb; ipdb.set_trace()
    return

class ObservationAdmin(admin.ModelAdmin):
    list_display = ['ufi', 'species', 'observation_import_link', 'date_added']

    def observation_import_link(self, observation):
        url = reverse('admin:observation_observationimport_change', args=[observation.observation_import.id])
        try:
            link = '<a href="%s">%s</a>' % (url, observation.observation_import.id)
        except AttributeError:
            link = 'No associated imports'
        return mark_safe(link)
    observation_import_link.short_description = 'Associated import'

admin.site.register(Observation, ObservationAdmin)
admin.site.register(Species)
admin.site.register(ObservationImport)