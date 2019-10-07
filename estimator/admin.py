import sys, os
sys.path.append(os.path.abspath('../engine_1858'))

from django.contrib import admin
from .models import Estimator, TrainedEstimator
from observation.models import Observation, Species, ObservationImport
from django_pandas.io import read_frame
import uuid
import pickle
from engine_1858.estimator import DWELPModel


# class EstimatorAdmin(admin.ModelAdmin):
# def save_model(self, request, obj, form, change):
#     if not obj.scaler_set:
#         super().save_model(self, request, obj, form, change)

# admin.site.register(Estimator, EstimatorAdmin)


def train_estimator(modeladmin, request, queryset):
    estimator_obj = queryset[0]
    ## 1. data
    id_list = estimator_obj.dataset
    data = read_frame(Observation.objects.filter(pk__in=id_list))
    ## 2. tag_dic
    # Binary Columns
    binary_columns = ['sampling_method_desc',
                    'record_type',
                    'primary_cde',
                    'lga_ufi',
                    'cma_no']
    # Integer Columns
    integer_columns = ['lat_long_accuracydd_int',
                    'sv_record_count']
    # Target Columns
    target_column = ['reliability']

    tag_dict = {'id': ['common_nme'],
            'binary': binary_columns,
            'integer': integer_columns,
            'target': target_column}

    ## 3. configuration_dict
    # search_parameters
    search_parameters = dict(scoring='roc_auc',
                         n_jobs=4,
                         n_iter=5,
                         verbose=2,
                         cv=3,
                         refit=True,
                         return_train_score=True)
    # scaler_set
    # scaler = estimator_obj.scaler_set
    # scaler_set = {'scaler': [scaler]}
    scaler_set = {'scaler': ['none']}
    # dimensionality_reduction_set
    reduce_dim = estimator_obj.dimensionality_reduction_set
    if reduce_dim == 'none':
        dimensionality_reduction_set = {'reduce_dim': ['none']}
    else:
        dimensionality_reduction_set = {
            'reduce_dim':[reduce_dim],
            'reduce_dim__n_components': [10]
        }

    configuration_dict = {
        'search_parameters': search_parameters,
        'scaler_set': scaler_set,
        'dimensionality_reduction_set': dimensionality_reduction_set
    }

    ## 4. cc_pipe_kwargs
    cond_imp_args = dict(tag_dict=tag_dict,
                     conditioning_column=tag_dict['id'])

    binariser_args = dict(binary_columns=tag_dict['binary'])

    cc_pipe_kwargs = dict(fit_arg_list=[cond_imp_args, binariser_args])

    ## 5. split_type
    
    split_type = estimator_obj.split_type

    ## 6. split_kwargs

    # if split_type == 'none':
    #     split_kwargs={
    #         'test_size': 0.33, 
    #         'stratify': ['common_nme']
    #     }
    # elif split_type == 'tt':
    #     split_kwargs={
    #         'test_size': estimator_obj.test_size, 
    #         'stratify': ['common_nme']
    #     }
    # else:
    #     split_kwargs={
    #         'test_size': estimator_obj.test_size, 
    #         'validate_size': estimator_obj.validate_size,
    #         'stratify': ['common_nme']
    #     }

    split_kwargs={
        'test_size': 0.33,
        'stratify': ['common_nme']
    }
    
    # delwp_estimator = DWELPModel(
    #     data,
    #     tag_dict,
    #     configuration_dict,
    #     cc_pipe_kwargs,
    #     split_type,
    #     split_kwargs
    # )

    # estimator_file_name = "estimator.pkl"
    # estimator_pkl = open(estimator_file_name, 'wb')
    # pickle.dump(delwp_estimator, estimator_pkl)
    # estimator_pkl.close()

    # TrainedEstimator.objects.update_or_create(
    #     id=uuid.uuid4(),
    #     pickled_estimator=estimator_pkl
    # ).save()
    return


class EstimatorAdmin(admin.ModelAdmin):
    actions = [train_estimator, ]


admin.site.register(Estimator, EstimatorAdmin)


def predict(modeladmin, request, queryset):
    '''
    this function is used to predict all observations
    given a queryset of trained estimator
    if the observation is trained by the estimator or the species name relative is not trained by the model
    it will skip the observation,
    else predict the observation and add the observation id into train_observation array field
    '''
    csv_id_list = []
    for csv in ObservationImport.objects.all():
        csv_id_list.append(csv.id)
    
    observation_queryset = Observation.objects.filter(observation_import__in=csv_id_list)

    for estimator in queryset:
        load_estimator = pickle.loads(estimator.pickled_estimator)
        trained_observation_list = estimator.trained_observation
        related_species_list = estimator.relatived_species
        for observation in observation_queryset.filter()

    import ipdb; ipdb.set_trace()
    return

class TrainEstimatorAdmin(admin.ModelAdmin):
    actions = [predict]

admin.site.register(TrainedEstimator, TrainEstimatorAdmin)
