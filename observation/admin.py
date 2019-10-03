from django.contrib import admin
from observation.models import Observation, Species
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .views import train_estimator_view

# Register your models here.
def train_estimator(modeladmin, request, queryset):
    if 'apply' in request.POST:
        '''
        this function will handle all the user inputs
        '''
        ## get json data
        data = request.POST # pseudocode
        train_estimator_view(data)
        return
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
    actions = [train_estimator]

admin.site.register(Observation, ObservationAdmin)
admin.site.register(Species)