from observation.models import Observation, Species
from django.contrib import admin
from datetime import date


class ObservationListFilter(admin.SimpleListFilter):
    title = 'Species'

    parameter_name = 'species'

    def lookups(self, request, model_admin):
        list_of_species = []
        queryset = Species.objects.all()
        for species in queryset:
            list_of_species.append((str(species.id), species.scientific_display_nme))
        return list_of_species

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(species_id=self.value())
        return queryset

class TimeListFilter(admin.SimpleListFilter):
    title = 'Time'
    parameter_name = 'date_added'

    def lookups(self, request, model_admin):
        list_of_time = []
        list_of_time.append(('today', 'today'))
        list_of_time.append(('thismonth', 'this month'))
        list_of_time.append(('thisyear', 'this year'))
        return list_of_time


    def queryset(self, request, queryset):
        today = date.today()
        month = today.month
        year = today.year

        if self.value() == 'today':
            return queryset.filter(date_added=today)
        elif self.value() == 'thismonth':
            return queryset.filter(date_added__year=year, date_added__month=month)
        elif self.value() == 'thisyear':
            return queryset.filter(date_added__year=year)
        return queryset


