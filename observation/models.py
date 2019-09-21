from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

import uuid

# Create your models here

class Observation(models.Model):
    """Model representing specific observation instance"""
    # id = models.UUIDField(primary_key=True, default=uuid.uuid1(), editable=False)
    ufi = models.CharField('UFI', max_length=8)
    species = models.ForeignKey('Species', on_delete=models.SET_NULL, null=True,)
    date_added = models.DateField('DATE_ADDED', auto_now_add=True)
    date_modified = models.DateField('DATE_MODIFIED', auto_now=True)
    survey_start_date = models.DateField('SURVEY_START_DATE')
    latitudedd_num = models.FloatField('LATITUDEDD_NUM')
    longitudedd_num = models.FloatField('LONGITUDEDD_NUM')
    data = JSONField()
    scraped = JSONField()

    def __str__(self):
        """String representation of model"""
        return self.ufi

class Species(models.Model):
    """Model representing single species"""
    # id = models.UUIDField(primary_key=True, editable=False)
    taxon_id = models.CharField('TAXON_ID', max_length=8)
    scientific_display_nme = models.CharField('SCIENTIFIC_DISPLAY_NAME', max_length=100)
    common_nme = models.CharField('COMMON_NAME', max_length=100)
    taxon_type = models.CharField('TAXON_TYPE', max_length=30)
    primary_cde = models.CharField('PRIMARY_CDE', max_length=5)

    def __str__(self):
        return self.scientific_display_nme