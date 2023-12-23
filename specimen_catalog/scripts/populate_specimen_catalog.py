# I wrote this code #

import os
import sys
import django
import csv

# Sets up django environment 
from collections import defaultdict
sys.path.append("/home/dynos/University/AdvWebDev - Mid term project/natural_history_project")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'natural_history_project.settings')
django.setup()

#Imports django models
from specimen_catalog.models import *

#Path to the csv file
data_file = '/home/dynos/University/AdvWebDev - Mid term project/natural_history_project/scripts/dataset/resource.csv'

#Opens the csv file
with open(data_file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)


    # Initialize a counter for tracking progress
    count = 0

    #Iterates over each row
    for row in csv_reader:
        count += 1

        # The following code retrieves or creats instances from the database #
        # and assigns each field from the csv file to the model #

        # Expedition table 
        expedition, created = Expedition.objects.get_or_create(
            expedition = row['expedition'],
            continent = row['continent'],
            country = row['continent'],    
            state_province = row['stateProvince'],
            term = row['year'],             
        )

        # Taxonomy table 
        taxonomy, created = Taxonomy.objects.get_or_create(           
            kingdom = row['higherClassification'],
            phylum = row['phylum'],
            highest_biostratigraphic_zone = row['highestBiostratigraphicZone'],      
            class_name = row['class'],
            identification_description = row['identificationDescription'],
            family = row['family'],
            genus = row['genus'],
            species = row['determinationNames'],  
        )

        # Specimen table 
        specimen, created = Specimen.objects.get_or_create(
            specimen_id=row['_id'],     # Takes the csv index column
            defaults={
                'catalog_number': row['catalogNumber'],
                'created': row['created'],
                'expedition':  expedition,  
                'taxonomy': taxonomy, 
                            
            }
        )

        # Prints a message to track the progress
        print(f"Record {count} (ID {row['_id']}): {'Created' if created else 'Retrieved'} successfully.")

# Prints a final message when the migration is completed
print("Data import complete.")

# End of the code I wrote