from django.contrib import admin
from observation.models import Observation, Species, ObservationImport
from estimator.models import RasterFileImport
from django.utils.safestring import mark_safe
from django.urls import reverse
from estimator.models import Estimator
from django_pandas.io import read_frame
import uuid
import rasterio
from engine_1858.spatial import make_environmental_df

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

def raster_data_calculate(modeladmin, request, queryset):
    '''
    In this function, it will take the entire csv file of observation to calculate the raster data
    '''
    # csv_id = queryset[0].id
    # observation_set = Observation.objects.filter(observation_import=csv_id)
    # observation_df = read_frame(observation_set)

    # raster_list = []
    # for raster in RasterFileImport.objects.all():
    #     raster_list.append(raster.raster_file_original.file)
    
    # ## error which the engine functions
    # land_df, indicies_list = make_environmental_df(observation_df, raster_list)

    ## not sure if only the land_df or both of them need to be store in model, currently, just make land_df stores in the model
    # queryset[0].land_df = land_df.values.tolist()
    # queryset[0].save()
    return

class ObservationImportAdmin(admin.ModelAdmin):
    actions = [raster_data_calculate]

admin.site.register(ObservationImport, ObservationImportAdmin)
admin.site.register(Species)