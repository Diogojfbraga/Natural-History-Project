import os
import sys
import django
import csv
from collections import defaultdict
from django.db import transaction  # Imports the transaction module

# Sets up django environment
sys.path.append("/natural_history_project")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'natural_history_project.settings')
django.setup()

# Imports Django models
from specimen_catalog.models import *

def run():
    # Path to the CSV file
    data_file = 'specimen_catalog/scripts/resource.csv'

    # Opens the CSV file
    with open(data_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Initializes a counter for tracking progress
        count = 0

        try:
            # Starts a database transaction
            with transaction.atomic():
                # Iterates over each row
                for row in csv_reader:
                    count += 1

                    # The following code retrieves or creates instances from the database
                    # and assigns each field from the CSV file to the model

                    # Expedition table
                    expedition, created = Expedition.objects.get_or_create(
                        expedition=row['expedition'],
                        continent=row['continent'],
                        country=row['country'],
                    )

                    # Taxonomy table
                    taxonomy, created = Taxonomy.objects.get_or_create(
                        kingdom=row['higherClassification'],
                        phylum=row['phylum'],
                        highest_biostratigraphic_zone=row['highestBiostratigraphicZone'],
                        class_name=row['class'],
                        identification_description=row['identificationDescription'],
                        family=row['family'],
                        genus=row['genus'],
                        species=row['determinationNames'],
                    )

                    # Specimen table
                    specimen, created = Specimen.objects.get_or_create(
                        specimen_id=row['_id'],  # Takes the CSV index column
                        defaults={
                            'catalog_number': row['catalogNumber'],
                            'expedition': expedition,
                            'taxonomy': taxonomy,
                        }
                    )

                    # Print progress
                    print(f"Adding record {count} (ID {row['_id']}): {'Created' if created else 'Retrieved'} successfully.")

            # Prints a final message when the migration is completed
            print("Data import complete.")

        except Exception as e:
            # If an exception occurs, print an error message
            print(f"Error during data import: {e}")

# Check if the script is being run directly
if __name__ == "__main__":
    run()
