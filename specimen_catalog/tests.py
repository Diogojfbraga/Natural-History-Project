from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator
from django_filters.filters import BaseInFilter
from django_filters.filterset import FilterSet
from django.views.generic import ListView
from .models import Specimen, Expedition, Taxonomy
from .model_factories import SpecimenFactory, ExpeditionFactory, TaxonomyFactory
from .views import AllSpecimensView
from .filters import SpecimenFilter

class ExpeditionModelTestCase(TestCase):
    def test_expedition_str_method(self):
            """
            Test the __str__ method of the Expedition model.
            """
            expedition = ExpeditionFactory()

            # Check if the __str__ method returns the expected value
            self.assertEqual(str(expedition), expedition.expedition)

    def test_expedition_creation(self):
        """
        Test the creation of an Expedition instance.
        """
        expedition_data = ExpeditionFactory()

        # Retrieve the created instance from the database
        saved_expedition = Expedition.objects.get(expedition_id=expedition_data.expedition_id)

        # Check if the retrieved instance has the correct values
        self.assertEqual(saved_expedition.expedition, expedition_data.expedition)
        self.assertEqual(saved_expedition.continent, expedition_data.continent)
        self.assertEqual(saved_expedition.country, expedition_data.country)


class TaxonomyModelTestCase(TestCase):
    def test_taxonomy_str_method(self):
        """
        Test the __str__ method of the Taxonomy model.
        """
        taxonomy = TaxonomyFactory()

        # Check if the __str__ method returns the expected value
        expected_str = f"({taxonomy.kingdom}/{taxonomy.phylum}/" \
                       f"{taxonomy.highest_biostratigraphic_zone}/" \
                       f"{taxonomy.class_name}/{taxonomy.identification_description}/" \
                       f"{taxonomy.family}/{taxonomy.genus}/{taxonomy.species})"
        self.assertEqual(str(taxonomy), expected_str)

    def test_taxonomy_creation(self):
        """
        Test the creation of a Taxonomy instance.
        """
        taxonomy_data = TaxonomyFactory()

        # Retrieve the created instance from the database
        saved_taxonomy = Taxonomy.objects.get(taxonomy_id=taxonomy_data.taxonomy_id)

        # Check if the retrieved instance has the correct values
        self.assertEqual(saved_taxonomy.kingdom, taxonomy_data.kingdom)
        self.assertEqual(saved_taxonomy.phylum, taxonomy_data.phylum)
        self.assertEqual(saved_taxonomy.highest_biostratigraphic_zone, taxonomy_data.highest_biostratigraphic_zone)
        self.assertEqual(saved_taxonomy.class_name, taxonomy_data.class_name)
        self.assertEqual(saved_taxonomy.identification_description, taxonomy_data.identification_description)
        self.assertEqual(saved_taxonomy.family, taxonomy_data.family)
        self.assertEqual(saved_taxonomy.genus, taxonomy_data.genus)
        self.assertEqual(saved_taxonomy.species, taxonomy_data.species)


class SpecimenModelTestCase(TestCase):
    def test_specimen_str_method(self):
        """
        Test the __str__ method of the Specimen model.
        """
        specimen = SpecimenFactory()

        # Check if the __str__ method returns the expected value
        expected_str = f"Specimen {specimen.specimen_id}"
        self.assertEqual(str(specimen), expected_str)

    def test_specimen_creation(self):
        """
        Test the creation of a Specimen instance.
        """
        specimen_data = SpecimenFactory()

        # Retrieve the created instance from the database
        saved_specimen = Specimen.objects.get(specimen_id=specimen_data.specimen_id)

        # Check if the retrieved instance has the correct values
        self.assertEqual(saved_specimen.catalog_number, specimen_data.catalog_number)
        self.assertEqual(saved_specimen.expedition.expedition_id, specimen_data.expedition.expedition_id)
        self.assertEqual(saved_specimen.taxonomy.taxonomy_id, specimen_data.taxonomy.taxonomy_id)

class IndexViewTestCase(TestCase):
    def test_index_view(self):
        # Make a GET request to the index view
        response = self.client.get(reverse('index'))

        # Check if the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'specimen_catalog/index.html')

    def test_all_specimens_view(self):
        # Create some sample specimens for testing
        SpecimenFactory.create_batch(2)

        # Make a GET request to the all_specimens view
        response = self.client.get(reverse('all_specimens'))

        # Check if the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'specimen_catalog/all_specimens.html')

        # Check if specimens are present in the context
        self.assertIn('specimens', response.context)
        self.assertEqual(len(response.context['specimens']), 2)


class AllSpecimensViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = RequestFactory()

    def setUp(self):
        # Create some sample specimens for testing
        SpecimenFactory.create_batch(30)

    def test_all_specimens_view_default(self):
        """
        Test the AllSpecimensView with default parameters.
        """
        url = reverse('all_specimens')
        response = self.client.get(url)

        # Check if the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'specimen_catalog/all_specimens.html')

        # Check if specimens are present in the context
        self.assertIn('specimens', response.context)
        self.assertEqual(len(response.context['specimens']), 20)  # Default page size is 20

    def test_all_specimens_view_filtered(self):
        """
        Test the AllSpecimensView with filter parameters.
        """
        # Create specimens with specific expedition continent and country
        SpecimenFactory.create_batch(10, expedition__continent='Asia', expedition__country='China')
        SpecimenFactory.create_batch(5, expedition__continent='Europe', expedition__country='France')

        url = reverse('all_specimens') + '?expedition__continent=Asia&expedition__country=China'
        response = self.client.get(url)

        # Check if the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'specimen_catalog/all_specimens.html')

        # Check if specimens are present in the context
        self.assertIn('specimens', response.context)
        self.assertEqual(len(response.context['specimens']), 10)


class ExpeditionAdminTestCase(TestCase):
    def setUp(self):
        # Create a superuser
        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')

        # Create an Expedition instance
        self.expedition = Expedition.objects.create(
            expedition='Test Expedition',
            continent='Test Continent',
            country='Test Country'
        )

        # Create a client and log in as the superuser
        self.client = Client()
        self.client.login(username='admin', password='adminpass')

    def test_expedition_admin_list_view(self):
        # URL for the Expedition admin list view
        url = reverse('admin:specimen_catalog_expedition_changelist')

        # Ensure the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensure the expedition data is present in the response
        self.assertContains(response, self.expedition.expedition)
        self.assertContains(response, self.expedition.continent)
        self.assertContains(response, self.expedition.country)

    def test_expedition_admin_detail_view(self):
        # URL for the Expedition admin detail view
        url = reverse('admin:specimen_catalog_expedition_change', args=[self.expedition.expedition_id])

        # Ensure the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensure the expedition data is present in the response
        self.assertContains(response, self.expedition.expedition)
        self.assertContains(response, self.expedition.continent)
        self.assertContains(response, self.expedition.country)

    def test_expedition_admin_add_view(self):
        # URL for the Expedition admin add view
        url = reverse('admin:specimen_catalog_expedition_add')

        # Ensure the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensure the form is present in the response
        self.assertContains(response, 'form')

    def test_expedition_admin_change_view(self):
        # URL for the Expedition admin change view
        url = reverse('admin:specimen_catalog_expedition_change', args=[self.expedition.expedition_id])

        # Ensure the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensure the form is present in the response
        self.assertContains(response, 'form')


class TaxonomyAdminTestCase(TestCase):
    def setUp(self):
        # Create a superuser
        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')

        # Create a Taxonomy instance using the factory
        self.taxonomy = TaxonomyFactory()

        # Create a client and log in as the superuser
        self.client = Client()
        self.client.login(username='admin', password='adminpass')

    def test_taxonomy_admin_list_view(self):
        # URL for the Taxonomy admin list view
        url = reverse('admin:specimen_catalog_taxonomy_changelist')

        # Ensure the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensure the taxonomy data is present in the response
        self.assertContains(response, self.taxonomy.kingdom)
        self.assertContains(response, self.taxonomy.phylum)
        self.assertContains(response, self.taxonomy.highest_biostratigraphic_zone)
        self.assertContains(response, self.taxonomy.class_name)
        self.assertContains(response, self.taxonomy.family)
        self.assertContains(response, self.taxonomy.genus)
        self.assertContains(response, self.taxonomy.species)

    def test_taxonomy_admin_detail_view(self):
        # URL for the Taxonomy admin detail view
        url = reverse('admin:specimen_catalog_taxonomy_change', args=[self.taxonomy.taxonomy_id])

        # Ensure the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensure the taxonomy data is present in the response
        self.assertContains(response, self.taxonomy.kingdom)
        self.assertContains(response, self.taxonomy.phylum)
        self.assertContains(response, self.taxonomy.highest_biostratigraphic_zone)
        self.assertContains(response, self.taxonomy.class_name)
        self.assertContains(response, self.taxonomy.family)
        self.assertContains(response, self.taxonomy.genus)
        self.assertContains(response, self.taxonomy.species)

    def test_taxonomy_admin_add_view(self):
        # URL for the Taxonomy admin add view
        url = reverse('admin:specimen_catalog_taxonomy_add')

        # Ensure the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensure the form is present in the response
        self.assertContains(response, 'form')

    def test_taxonomy_admin_change_view(self):
        # URL for the Taxonomy admin change view
        url = reverse('admin:specimen_catalog_taxonomy_change', args=[self.taxonomy.taxonomy_id])

        # Ensure the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensure the form is present in the response
        self.assertContains(response, 'form')

class SpecimenAdminTestCase(TestCase):
    def setUp(self):
        # Create a superuser
        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')

        # Create a Specimen instance using the factory
        self.specimen = SpecimenFactory()

        # Create a client and log in as the superuser
        self.client = Client()
        self.client.login(username='admin', password='adminpass')

    def test_specimen_list_view(self):
        # Access the Specimen list view in the admin
        url = reverse('admin:specimen_catalog_specimen_changelist')
        response = self.client.get(url)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the Specimen instance is present in the response
        self.assertContains(response, str(self.specimen.catalog_number))

    def test_specimen_detail_view(self):
        # Access the Specimen detail view in the admin
        url = reverse('admin:specimen_catalog_specimen_change', args=[self.specimen.pk])
        response = self.client.get(url)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the Specimen instance details are present in the response
        self.assertContains(response, str(self.specimen.catalog_number))
        self.assertContains(response, str(self.specimen.expedition))
        self.assertContains(response, str(self.specimen.taxonomy))

    def test_specimen_add_view(self):
        # Access the Specimen add view in the admin
        url = reverse('admin:specimen_catalog_specimen_add')
        response = self.client.get(url)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the form contains the expected fields
        self.assertContains(response, 'id_catalog_number')
        self.assertContains(response, 'id_expedition')
        self.assertContains(response, 'id_taxonomy')


