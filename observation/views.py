from django.shortcuts import render
from django.http import HttpResponse, request
from .models import *

import csv, io, datetime

# Create your views here.

def import_dataset(request):
    return render(request, 'observation/import_dataset.html')

def upload_csv(request):
    template = "upload_csv.html"
    prompt = {

    }

    if request.method == "GET":
        return(request, template, prompt)
    
    csv_file = request.FILES['csv_file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Not a .csv file')

    dataset = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(dataset)

    csv_string = csv.reader(io_string, delimiter=',', quotechar='|')
    # csv_array, an array[i][j] where i and j is the row and column index respectively
    csv_array = []
    for row in csv_string:
        csv_array.append(row)

    input_fields = csv_array[0]
    # field_dict, a dictionary that will store the column index of each field
    field_dict = {}
    for i, field in enumerate(input_fields):
        field_dict[field] = i
    
    species_fields = []
    for field in Species._meta.get_fields():
        species_fields.append(field.name)

    observation_fields = []
    for field in Observation._meta.get_fields():
        observation_fields.append(field.name)

    for row in csv_array[1::]:
    
        species_dict = {}
        observation_dict = {}
        data = {}

        for i, value in enumerate(row):
            this_field = input_fields[i]
            # if species information, check if already exists, if not initialize new species
            if this_field.lower() in species_fields:
                species_dict[this_field.lower()] = value
            elif this_field.lower() in observation_fields:
                observation_dict[this_field.lower()] = value
            
            else:
                data[this_field.lower()] = value
        
        observation_dict['data'] = data.__str__()
        
        if not Species.objects.filter(taxon_id=species_dict['taxon_id']):
            Species.objects.update_or_create(
                taxon_id = species_dict['taxon_id'],
                scientific_display_nme = species_dict['scientific_display_nme'],
                common_nme = species_dict['common_nme'],
                taxon_type = species_dict['taxon_type'],
                primary_cde = species_dict['primary_cde'],
            )

        Observation.objects.update_or_create(
            ufi = observation_dict['ufi'],
            species = Species.objects.filter(taxon_id=species_dict['taxon_id']).first(),
            survey_start_date = datetime.datetime.strptime(observation_dict['survey_start_date'], '%d/%b/%Y').strftime('%Y-%m-%d'),
            latitudedd_num = observation_dict['latitudedd_num'],
            longitudedd_num = observation_dict['longitudedd_num'],
            data = data,
            scraped = 'placeholder',
        )