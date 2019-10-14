import sys, os

sys.path.append(os.path.abspath("../engine_1858"))

from django.contrib import admin
from .models import Estimator, TrainedEstimator
from observation.models import Observation, Species, ObservationImport
from django_pandas.io import read_frame
import uuid
import pickle
from engine_1858.estimator import DWELPModel
import sample_models
import pandas as pd
import numpy as np
from functools import reduce
from io import BytesIO

# class EstimatorAdmin(admin.ModelAdmin):
# def save_model(self, request, obj, form, change):
#     if not obj.scaler_set:
#         super().save_model(self, request, obj, form, change)

# admin.site.register(Estimator, EstimatorAdmin)


def train_estimator(modeladmin, request, queryset):
    print("Training estimator...")
    estimator_obj = queryset[0]
    ## 1. data
    print("Reading data from selected observations...")
    id_list = estimator_obj.dataset
    data = read_frame(
        Observation.objects.filter(id__in=id_list),
        fieldnames=(
            "ufi",
            "species",
            "latitudedd_num",
            "longitudedd_num",
            "lat_long_accuracydd_int",
            "sampling_method_desc",
            "record_type",
            "sv_record_count",
            "lga_ufi",
            "cma_no",
            "park_id",
            "survey_id",
            "reliability",
            "reliability_txt",
            "rating_int",
        ),
    )
    data = data.replace(to_replace="nan", value="")

    ## add related species
    related_species = []
    for observation in Observation.objects.filter(id__in=id_list).values('species').distinct():
        related_species.append(observation['species'])

    ## 2. tag dictionary
    print("Preparing tag dictionary...")
    binary_columns = ["sampling_method_desc", "record_type", "lga_ufi", "cma_no"]
    integer_columns = ["lat_long_accuracydd_int", "sv_record_count"]
    target_column = ["reliability"]
    tag_dict = {
        "id": ["species"],
        "binary": binary_columns,
        "integer": integer_columns,
        "target": target_column,
    }

    ## 3. configuration_dict
    print("Preparing configuration dictionary...")
    # search_parameters
    search_parameters = dict(
        scoring="roc_auc",
        n_jobs=4,
        n_iter=5,
        verbose=2,
        cv=3,
        refit=True,
        return_train_score=True,
    )

    # scaler_set
    scaler = estimator_obj.scaler_set
    scaler_set = {"scaler": [scaler]}

    # dimensionality_reduction_set
    reduce_dim = estimator_obj.dimensionality_reduction_set
    if reduce_dim == "none":
        dimensionality_reduction_set = {"reduce_dim": ["none"]}
    else:
        dimensionality_reduction_set = {
            "reduce_dim": [reduce_dim],
            "reduce_dim__n_components": [10],
        }

    configuration_dict = {
        "search_parameters": search_parameters,
        "scaler_set": scaler_set,
        "dimensionality_reduction_set": dimensionality_reduction_set,
        "model_config_list": sample_models.models,
    }

    ## 4. cc_pipe_kwargs
    print("Preparing cleanse and consolidation pipe arguments...")
    cond_imp_args = dict(tag_dict=tag_dict, conditioning_column=tag_dict["id"][0])

    binariser_args = dict(binary_columns=tag_dict["binary"], id_col="species")

    cc_pipe_kwargs = dict(fit_arg_list=[cond_imp_args, binariser_args])

    ## 5. split_type
    print("Preparing split dictionary...")
    split_type = estimator_obj.split_type

    # 6. split_kwargs

    if split_type == "none":
        split_kwargs = {
            "test_size": 0.33,
            "stratify": ["species", "reliability"],
        }
    else:
        split_kwargs = {
            "test_size": estimator_obj.test_size,
            "stratify": ["species", "reliability"],
        }
    
    print("Initializing estimator...")
    delwp_estimator = DWELPModel(
        data, tag_dict, configuration_dict, cc_pipe_kwargs, split_type, split_kwargs
    )
    delwp_estimator.train()

    print("Pickling estimator...")
    estimator_file_name = "estimator.pkl"
    estimator_pkl = pickle.dumps(delwp_estimator)

    print("Creating TrainedEstimator object...")
    trained_estimator_object, created = TrainedEstimator.objects.update_or_create(
        id=uuid.uuid4(), 
        pickled_estimator=estimator_pkl,
        relatived_species = related_species
    )

    print("Saving TrainedEstimator object...")
    trained_estimator_object.save()
    return


class EstimatorAdmin(admin.ModelAdmin):
    actions = [train_estimator]

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

    observation_queryset = Observation.objects.filter(
        observation_import__in=csv_id_list)

    for estimator in queryset:
        load_estimator = pickle.loads(estimator.pickled_estimator)
        trained_observation_list = estimator.trained_observation
        related_species_list = estimator.relatived_species

        ob_set = observation_queryset.filter(species__in=related_species_list)
        if trained_observation_list is not None:
            ob_set = ob_set.exclude(id__in=trained_observation_list)

        data = read_frame(
            ob_set,
            fieldnames=(
                # "ufi",
                "species",
                "latitudedd_num",
                "longitudedd_num",
                "lat_long_accuracydd_int",
                "sampling_method_desc",
                # "record_type",
                "sv_record_count",
                "lga_ufi",
                "cma_no",
                # "park_id",
                # "survey_id",
                "reliability",
                # "reliability_txt",
                "rating_int",
            ),
        )
        data = data.replace(to_replace="nan", value="")
        output_frame = load_estimator.predict(data, prediction_type='classification')




        ## final part to write all the data in the data base and finish the prediction
        for i in range(output_frame['ufi'].count()):
            observation = Observation.objects.filter(ufi=output_frame['ufi'][i])[0]
            estimator.trianed_observation.append(observation.id)
            observation.reliability = output_frame['re']


    return


class TrainEstimatorAdmin(admin.ModelAdmin):
    actions = [predict, ]


admin.site.register(TrainedEstimator, TrainEstimatorAdmin)
