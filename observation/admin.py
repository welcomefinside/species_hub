from django.contrib import admin
from observation.models import Observation, Species
from django.shortcuts import render
from django.http import HttpResponseRedirect
from observation.list_filters import ObservationListFilter, TimeListFilter

# Register your models here.
def train_estimator(modeladmin, request, queryset):
    # passing the quertsets to other views which is doing the training
    variable_names = ['latitude', 'longtitude']
    species_names = []

    for item in queryset:
        if item.species not in species_names:
            species_names.append(item.species)

    for item in queryset[0].data.keys():
        variable_names.append(item)

    return render(request, 'admin/variable_selection.html', {'species_names':species_names, 'variable_names':variable_names})

class ObservationAdmin(admin.ModelAdmin):
    list_display = ['ufi', 'species', 'date_added', 'date_modified']
    actions = [train_estimator,]
    list_filter = [ObservationListFilter, TimeListFilter,]  ## one more date filter need to be done, i am on my way, it will be easy after i done the first filter

admin.site.register(Observation, ObservationAdmin)



def show_estimators(modeladmin, request, queryset):
    """
    this function is used to show the related estimators of species
    """
    return

class SpeciesAdmin(admin.ModelAdmin):
    list_display = ['scientific_display_nme', 'taxon_type', 'primary_cde']
    actions = [show_estimators,]

admin.site.register(Species, SpeciesAdmin)