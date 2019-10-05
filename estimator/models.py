from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django import forms

import uuid

class Estimator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)

    # scaler options
    NONE = 'none'
    STANDARD = 'standard'
    MINMAX = 'minmax'
    QUANTILE = 'quantile'
    SCALER_OPTIONS = (
        (STANDARD, 'standard'),
        (MINMAX, 'minmax'),
        (QUANTILE, 'quantile'),
        (NONE, 'none'),
    )
    scaler_set = models.CharField('scaler', choices=SCALER_OPTIONS, default=NONE, max_length=10)

    # dimensionality reduction options
    # TODO: handle dimensionality reduction of N components i.e {'reduce_dim__n_components': [10, 20, 50, 100]}
    NONE = 'none'
    PCA = 'pca'
    RANDOM = 'randomized'
    DIMENSIONALITY_REDUCTION_OPTIONS = (
        (PCA, 'pca'),
        (RANDOM, 'random'),
        (NONE, 'none'),
    )
    dimensionality_reduction_set = models.CharField('reduce_dim', choices=DIMENSIONALITY_REDUCTION_OPTIONS, default=NONE, max_length=10)

    # train-test-split options
    TRAIN_ONLY = 'none'
    TRAIN_TEST = 'tt'
    TRAIN_TEST_VALIDATE = 'tvt'
    TRAIN_TEST_SPLIT_OPTIONS = (
        (TRAIN_ONLY, 'train'),
        (TRAIN_TEST, 'train-test'),
        (TRAIN_TEST_VALIDATE, 'train-test-validate'),
    )
    split_type = models.CharField('tt_split', choices=TRAIN_TEST_SPLIT_OPTIONS, default=NONE, max_length=10)
    test_size = models.FloatField('test')
    validate_size = models.FloatField('validate')

    dataset = ArrayField(models.UUIDField(null=True))

class TrainedEstimator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    pickled_estimator = models.BinaryField('pickled_estimator')