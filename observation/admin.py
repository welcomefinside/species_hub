from django.contrib import admin
from observation.models import Observation, Species, ObservationImport
from django.utils.safestring import mark_safe
from django.urls import reverse
from estimator.models import Estimator
import uuid
from observation.list_filters import ObservationListFilter, TimeListFilter


def create_estimator(queryset):
    observation_id = []
    for observation in queryset:
        observation_id.append(observation.id)

    new_estimator = Estimator.objects.update_or_create(
        id=uuid.uuid4(),
        dataset=observation_id,
    )

    new_estimator[0].save()
    return

# Register your models here.
def create_estimator_by_observations(modeladmin, request, queryset):
    create_estimator(queryset)
    return

def create_estimator_by_csv(modeladmin, request, queryset):
    csv_list = []
    for csv in queryset:
        csv_list.append(csv.id)

    create_estimator(Observation.objects.all().filter(observation_import__in=csv_list))
    return

def create_estimator_by_species(modeladmin, request, queryset):
    species_list = []
    for species in queryset:
        species_list.append(species.id)
    
    create_estimator(Observation.objects.all().filter(species__in=species_list))
    return

class ObservationAdmin(admin.ModelAdmin):
    list_display = ['ufi', 'species', 'date_added', 'latitudedd_num', 'longitudedd_num',
       'lat_long_accuracydd_int', 'sampling_method_desc', 'record_type',
       'sv_record_count', 'lga_ufi', 'cma_no', 'park_id', 'survey_id',
       'reliability', 'reliability_txt', 'rating_int']
    actions = [create_estimator_by_observations,]
    list_filter = [ObservationListFilter, TimeListFilter,]

    def observation_import_link(self, observation):
        url = reverse('admin:observation_observationimport_change', args=[observation.observation_import.id])
        try:
            link = '<a href="%s">%s</a>' % (url, observation.observation_import.id)
        except AttributeError:
            link = 'No associated imports'
        return mark_safe(link)
    observation_import_link.short_description = 'Associated import'

admin.site.register(Observation, ObservationAdmin)

class SpeciesAdmin(admin.ModelAdmin):
    actions = [create_estimator_by_species,]

admin.site.register(Species, SpeciesAdmin)


class ObservationImportAdmin(admin.ModelAdmin):
    actions = [create_estimator_by_csv,]
    list_filter = [TimeListFilter,]

admin.site.register(ObservationImport, ObservationImportAdmin)