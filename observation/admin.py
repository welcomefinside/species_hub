from django.contrib import admin
from observation.models import Observation, Species, ObservationImport
from django.utils.safestring import mark_safe
from django.urls import reverse
from estimator.models import Estimator
import uuid

# Register your models here.
def create_estimator_by_observations(modeladmin, request, queryset):
    observation_id = []
    for observation in queryset:
        observation_id.append(observation.id)

    new_estimator = Estimator.objects.update_or_create(
        id=uuid.uuid4(),
        dataset=observation_id,
    )

    new_estimator[0].save()

    return
    
def ipdb_helper(modeladmin, request, queryset):
    import ipdb; ipdb.set_trace()
    return

class ObservationAdmin(admin.ModelAdmin):
    list_display = ['ufi', 'species', 'observation_import_link', 'date_added']
    actions = [create_estimator_by_observations,]

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