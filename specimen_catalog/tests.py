from django.test import TestCase
from .models import Expedition, Taxonomy, Specimen, Geography, Identification

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
        self.assertEqual(str(self.taxonomy), "Taxonomy 1")

    def test_specimen_creation(self):
        self.assertEqual(str(self.specimen), "Specimen 1")

class GeographyModelTest(TestCase):
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

        geography_data = {
            "specimen": self.specimen,
            "expedition": self.expedition,
        }
        self.geography = Geography.objects.create(**geography_data)

    def test_geography_creation(self):
        self.assertEqual(str(self.geography), "Geography 1")

class IdentificationModelTest(TestCase):
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

        identification_data = {
            "specimen": self.specimen,
            "identification_as_registered": "Test Registered",
            "identification_other": "Test Other",
            "identification_qualifier": "Test Qualifier",
            "identification_variety": "Test Variety",
            "identified_by": "Test Identifier",
        }
        self.identification = Identification.objects.create(**identification_data)

    def test_identification_creation(self):
        self.assertEqual(str(self.identification), "Identification 1")
