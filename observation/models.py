from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

import os, uuid, pandas, numpy


# Create your models here

class Observation(models.Model):
    """Model representing specific observation instance"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    observation_import = models.ForeignKey(to='ObservationImport', on_delete=models.SET_NULL, null=True, editable=False)
    ufi = models.CharField('UFI', max_length=8)
    species = models.ForeignKey(to='Species', on_delete=models.SET_NULL, null=True,)
    date_added = models.DateField('DATE_ADDED', auto_now_add=True)
    date_modified = models.DateField('DATE_MODIFIED', auto_now=True)
    latitudedd_num = models.FloatField('LATITUDEDD_NUM')
    longitudedd_num = models.FloatField('LONGITUDEDD_NUM')
    lat_long_accuracydd_int = models.FloatField('LAT_LONG_ACCURACYDD_INT')
    sampling_method_desc = models.CharField('SAMPLING_METHOD_DESC', max_length=100)
    record_type = models.CharField('RECORD_TYPE', max_length=100, null=True, blank=True)
    sv_record_count = models.FloatField('SV_RECORD_COUNT', null=True, blank=True)
    lga_ufi = models.FloatField('LGA_UFI', null=True, blank=True)
    cma_no = models.FloatField('CMA_NO', null=True, blank=True)
    park_id = models.FloatField('PARK_ID', null=True, blank=True)
    survey_id = models.FloatField('SURVEY_ID', null=True, blank=True)

    # target variables
    reliability = models.CharField('RELIABILITY', max_length=20, null=True, blank=True)
    reliability_txt = models.CharField('RELIABILITY_TXT', max_length=20, null=True, blank=True)
    rating_int = models.FloatField('RATING_INT', null=True, blank=True)


    def __str__(self):
        """String representation of model"""
        return self.ufi

class Species(models.Model):
    """Model representing single species"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    taxon_id = models.CharField('TAXON_ID', max_length=8)
    scientific_display_nme = models.CharField('SCIENTIFIC_DISPLAY_NAME', max_length=100)
    common_nme = models.CharField('COMMON_NAME', max_length=100)
    taxon_type = models.CharField('TAXON_TYPE', max_length=30)
    primary_cde = models.CharField('PRIMARY_CDE', max_length=5)

    def __str__(self):
        return self.taxon_id

class ObservationImport(models.Model):
    """Model representing an entire batch import"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    csv = models.FileField('CSV FILE', upload_to='imports/%Y/%m/%d/', null=False)
    date_added = models.DateField('DATE ADDED', auto_now_add=True)
    date_modified = models.DateField('DATE MODIFIED', auto_now=True)
    remarks = models.TextField('REMARKS', null=True, blank=True)


@receiver(post_save, sender=ObservationImport, dispatch_uid="add_records_to_observation_from_import")
def add_records_to_observation_from_import(sender, instance, **kwargs):
    imported = instance.csv.name

    with open(imported) as f:
        data = pandas.read_csv(imported)
        # Lower column names
        cols = data.columns.tolist()

        for i, col in enumerate(cols):
            cols[i] = col.lower()
        
        data.columns = cols

        data['reliability'] = data['reliability'].replace(to_replace=numpy.nan, value='', regex=True)
        data['record_type'] = data['record_type'].replace(to_replace=numpy.nan, value='', regex=True)
        data = data.where(pandas.notnull(data), None)

        for index, row in data.iterrows():

            # check if species exists, if not create a species object
            if not Species.objects.filter(taxon_id=row['taxon_id']):
                Species.objects.update_or_create(
                    id = uuid.uuid4(),
                    taxon_id = row['taxon_id'],
                    scientific_display_nme = row['scientific_display_nme'],
                    common_nme = row['common_nme'],
                    taxon_type = row['taxon_type'],
                    primary_cde = row['primary_cde'],
                )

            Observation.objects.update_or_create(
                id = uuid.uuid4(),
                observation_import = instance,
                ufi = row['ufi'],
                species = Species.objects.filter(taxon_id=row['taxon_id']).first(),
                # survey_start_date = datetime.datetime.strptime(observation_dict['survey_start_date'], '%d-%b-%y').strftime('%Y-%m-%d'),
                latitudedd_num = row['latitudedd_num'],
                longitudedd_num = row['longitudedd_num'],
                lat_long_accuracydd_int = row['lat_long_accuracydd_int'],
                sampling_method_desc = row['sampling_method_desc'],
                record_type = row['record_type'],
                sv_record_count = row['sv_record_count'],
                lga_ufi = row['lga_ufi'],
                cma_no = row['cma_no'],
                park_id = row['park_id'],
                survey_id = row['survey_id'],

                reliability = row['reliability'],
                reliability_txt = row['reliability_txt'],
                rating_int = row['rating_int'],
            )