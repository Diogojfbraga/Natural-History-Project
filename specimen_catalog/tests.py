# tests.py

from django.test import TestCase
from .models import Expedition, Taxonomy, Specimen

class SpecimenModelTest(TestCase):
    def setUp(self):
        # Create test data
        expedition_data = {
            "expedition": "Test Expedition",
            "continent": "Test Continent",
            "country": "Test Country",
            "state_province": "Test State",
            "term": "Test Term",
        }
        self.expedition = Expedition.objects.create(**expedition_data)

        taxonomy_data = {
            "kingdom": "Test Kingdom",
            "phylum": "Test Phylum",
            "highest_biostratigraphic_zone": "Test Zone",
            "class_name": "Test Class",
            "identification_description": "Test Description",
            "family": "Test Family",
            "genus": "Test Genus",
            "species": "Test Species",
        }
        self.taxonomy = Taxonomy.objects.create(**taxonomy_data)

        specimen_data = {
            "catalog_number": "Test Catalog Number",
            "created": 20221215,  # Adjust the date as needed
            "expedition": self.expedition,
            "taxonomy": self.taxonomy,
        }
        self.specimen = Specimen.objects.create(**specimen_data)

    def test_expedition_creation(self):
        self.assertEqual(str(self.expedition), "Test Expedition")

    def test_taxonomy_creation(self):
        # The expected value should reflect the actual species value
        self.assertEqual(str(self.taxonomy), "Taxonomy Test Species")

    def test_specimen_creation(self):
        self.assertEqual(str(self.specimen), "Specimen 1")

    # Additional tests
    def test_expedition_str_representation(self):
        self.assertEqual(str(self.expedition), "Test Expedition")

    def test_specimen_str_representation(self):
        self.assertEqual(str(self.specimen), "Specimen 1")

    def test_taxonomy_str_representation(self):
        # The expected value should reflect the actual species value
        self.assertEqual(str(self.taxonomy), "Taxonomy Test Species")

    def test_expedition_str_representation_multiple(self):
        # Test creating multiple Expedition instances
        expedition_2 = Expedition.objects.create(expedition="Test Expedition 2")
        self.assertEqual(str(expedition_2), "Test Expedition 2")

    def test_specimen_str_representation_multiple(self):
        # Test creating multiple Specimen instances
        specimen_2 = Specimen.objects.create(catalog_number="Test Catalog Number 2", created=20221216)
        self.assertEqual(str(specimen_2), "Specimen 2")

    def test_taxonomy_str_representation_multiple(self):
        # Test creating multiple Taxonomy instances
        taxonomy_2 = Taxonomy.objects.create(species="Test Species 2")
        self.assertEqual(str(taxonomy_2), "Taxonomy Test Species 2")

    # Write more tests as needed
