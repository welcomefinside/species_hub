from observation.models import Observation, Species
from django.contrib import admin


class ObservationListFilter(admin.SimpleListFilter):
    title = 'Species'

    parameter_name = 'species'

    def lookups(self, request, model_admin):
        list_of_observations = []
        queryset = Species.objects.all()
        for species in queryset:
            list_of_observations.append((str(species.id), species.scientific_display_nme))
        return list_of_observations

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(species_id=self.value())
        return queryset
