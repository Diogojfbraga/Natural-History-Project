from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator
from django_filters.filters import BaseInFilter
from django_filters.filterset import FilterSet
from django.views.generic import ListView

from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from specimen_catalog.forms import ExpeditionForm, NewSpecimenForm, TaxonomyForm
from specimen_catalog.models import Expedition, Specimen, Taxonomy
from specimen_catalog.views import AllSpecimensView, NewSpecimenView, SpecimenDeleteView
from specimen_catalog.model_factories import ExpeditionFactory, SpecimenFactory, TaxonomyFactory
from specimen_catalog.serializers import ExpeditionSerializer, SpecimenSerializer, TaxonomySerializer

from django.contrib.messages import get_messages

# Tests the Expedition Model
class ExpeditionModelTestCase(TestCase):
    def test_expedition_str_method(self):
            """
            Test the __str__ method of the Expedition model.
            """
            expedition = ExpeditionFactory()

            # Checks if the __str__ method returns the expected value
            self.assertEqual(str(expedition), expedition.expedition)

    def test_expedition_creation(self):
        """
        Test the creation of an Expedition instance.
        """
        expedition_data = ExpeditionFactory()

        # Retrieves the created instance from the database
        saved_expedition = Expedition.objects.get(expedition_id=expedition_data.expedition_id)

        # Checks if the retrieved instance has the correct values
        self.assertEqual(saved_expedition.expedition, expedition_data.expedition)
        self.assertEqual(saved_expedition.continent, expedition_data.continent)
        self.assertEqual(saved_expedition.country, expedition_data.country)

# Tests the Taxonomy Model
class TaxonomyModelTestCase(TestCase):
    def test_taxonomy_str_method(self):
        """
        Test the __str__ method of the Taxonomy model.
        """
        taxonomy = TaxonomyFactory()

        # Checks if the __str__ method returns the expected value
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

        # Retrieves the created instance from the database
        saved_taxonomy = Taxonomy.objects.get(taxonomy_id=taxonomy_data.taxonomy_id)

        # Checks if the retrieved instance has the correct values
        self.assertEqual(saved_taxonomy.kingdom, taxonomy_data.kingdom)
        self.assertEqual(saved_taxonomy.phylum, taxonomy_data.phylum)
        self.assertEqual(saved_taxonomy.highest_biostratigraphic_zone, taxonomy_data.highest_biostratigraphic_zone)
        self.assertEqual(saved_taxonomy.class_name, taxonomy_data.class_name)
        self.assertEqual(saved_taxonomy.identification_description, taxonomy_data.identification_description)
        self.assertEqual(saved_taxonomy.family, taxonomy_data.family)
        self.assertEqual(saved_taxonomy.genus, taxonomy_data.genus)
        self.assertEqual(saved_taxonomy.species, taxonomy_data.species)

# Tests the Specimen Model
class SpecimenModelTestCase(TestCase):
    def test_specimen_str_method(self):
        """
        Test the __str__ method of the Specimen model.
        """
        specimen = SpecimenFactory()

        # Checks if the __str__ method returns the expected value
        expected_str = f"Specimen {specimen.specimen_id}"
        self.assertEqual(str(specimen), expected_str)

    def test_specimen_creation(self):
        """
        Test the creation of a Specimen instance.
        """
        specimen_data = SpecimenFactory()

        # Retrieves the created instance from the database
        saved_specimen = Specimen.objects.get(specimen_id=specimen_data.specimen_id)

        # Checks if the retrieved instance has the correct values
        self.assertEqual(saved_specimen.catalog_number, specimen_data.catalog_number)
        self.assertEqual(saved_specimen.expedition.expedition_id, specimen_data.expedition.expedition_id)
        self.assertEqual(saved_specimen.taxonomy.taxonomy_id, specimen_data.taxonomy.taxonomy_id)

# Tests index view
class IndexViewTestCase(TestCase):
    def test_index_view(self):
        # Makes a GET request to the index view
        response = self.client.get(reverse('index'))

        # Checks if the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Checks if the correct template is used
        self.assertTemplateUsed(response, 'specimen_catalog/index.html')

    def test_all_specimens_view(self):
        # Creates some sample specimens for testing
        SpecimenFactory.create_batch(2)

        # Makes a GET request to the all_specimens view
        response = self.client.get(reverse('all_specimens'))

        # Checks if the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Checks if the correct template is used
        self.assertTemplateUsed(response, 'specimen_catalog/all_specimens.html')

        # Checks if specimens are present in the context
        self.assertIn('specimens', response.context)
        self.assertEqual(len(response.context['specimens']), 2)

#Tests the all_species view
class AllSpecimensViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = RequestFactory()

    def setUp(self):
        # Creates some sample specimens for testing
        SpecimenFactory.create_batch(30)

    def test_all_specimens_view_default(self):
        """
        Test the AllSpecimensView with default parameters.
        """
        url = reverse('all_specimens')
        response = self.client.get(url)

        # Checks if the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Checks if the correct template is used
        self.assertTemplateUsed(response, 'specimen_catalog/all_specimens.html')

        # Checks if specimens are present in the context
        self.assertIn('specimens', response.context)
        self.assertEqual(len(response.context['specimens']), 20)  # Default page size is 20

    def test_all_specimens_view_filtered(self):
        """
        Test the AllSpecimensView with filter parameters.
        """
        # Creates specimens with specific expedition continent and country
        SpecimenFactory.create_batch(10, expedition__continent='Asia', expedition__country='China')
        SpecimenFactory.create_batch(5, expedition__continent='Europe', expedition__country='France')

        url = reverse('all_specimens') + '?expedition__continent=Asia&expedition__country=China'
        response = self.client.get(url)

        # Checks if the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Checks if the correct template is used
        self.assertTemplateUsed(response, 'specimen_catalog/all_specimens.html')

        # Checks if specimens are present in the context
        self.assertIn('specimens', response.context)
        self.assertEqual(len(response.context['specimens']), 10)

# Tests the Expedition admin
class ExpeditionAdminTestCase(TestCase):
    def setUp(self):
        # Creates a superuser
        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')

        # Creates an Expedition instance
        self.expedition = Expedition.objects.create(
            expedition='Test Expedition',
            continent='Test Continent',
            country='Test Country'
        )

        # Creates a client and log in as the superuser
        self.client = Client()
        self.client.login(username='admin', password='adminpass')

    def test_expedition_admin_list_view(self):
        # URL for the Expedition admin list view
        url = reverse('admin:specimen_catalog_expedition_changelist')

        # Ensures the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensures the expedition data is present in the response
        self.assertContains(response, self.expedition.expedition)
        self.assertContains(response, self.expedition.continent)
        self.assertContains(response, self.expedition.country)

    def test_expedition_admin_detail_view(self):
        # URL for the Expedition admin detail view
        url = reverse('admin:specimen_catalog_expedition_change', args=[self.expedition.expedition_id])

        # Ensures the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensures the expedition data is present in the response
        self.assertContains(response, self.expedition.expedition)
        self.assertContains(response, self.expedition.continent)
        self.assertContains(response, self.expedition.country)

    def test_expedition_admin_add_view(self):
        # URL for the Expedition admin add view
        url = reverse('admin:specimen_catalog_expedition_add')

        # Ensures the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensures the form is present in the response
        self.assertContains(response, 'form')

    def test_expedition_admin_change_view(self):
        # URL for the Expedition admin change view
        url = reverse('admin:specimen_catalog_expedition_change', args=[self.expedition.expedition_id])

        # Ensures the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensures the form is present in the response
        self.assertContains(response, 'form')

# Tests the Taxonomy admin
class TaxonomyAdminTestCase(TestCase):
    def setUp(self):
        # Creates a superuser
        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')

        # Creates a Taxonomy instance using the factory
        self.taxonomy = TaxonomyFactory()

        # Creates a client and log in as the superuser
        self.client = Client()
        self.client.login(username='admin', password='adminpass')

    def test_taxonomy_admin_list_view(self):
        # URL for the Taxonomy admin list view
        url = reverse('admin:specimen_catalog_taxonomy_changelist')

        # Ensures the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensures the taxonomy data is present in the response
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

        # Ensures the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensures the taxonomy data is present in the response
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

        # Ensures the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensures the form is present in the response
        self.assertContains(response, 'form')

    def test_taxonomy_admin_change_view(self):
        # URL for the Taxonomy admin change view
        url = reverse('admin:specimen_catalog_taxonomy_change', args=[self.taxonomy.taxonomy_id])

        # Ensures the view returns a 200 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensures the form is present in the response
        self.assertContains(response, 'form')

# Tests the Specimen admin
class SpecimenAdminTestCase(TestCase):
    def setUp(self):
        # Creates a superuser
        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')

        # Creates a Specimen instance using the factory
        self.specimen = SpecimenFactory()

        # Creates a client and log in as the superuser
        self.client = Client()
        self.client.login(username='admin', password='adminpass')

    def test_specimen_list_view(self):
        # Access the Specimen list view in the admin
        url = reverse('admin:specimen_catalog_specimen_changelist')
        response = self.client.get(url)

        # Checks that the response is successful
        self.assertEqual(response.status_code, 200)

        # Checks that the Specimen instance is present in the response
        self.assertContains(response, str(self.specimen.catalog_number))

    def test_specimen_detail_view(self):
        # Access the Specimen detail view in the admin
        url = reverse('admin:specimen_catalog_specimen_change', args=[self.specimen.pk])
        response = self.client.get(url)

        # Checks that the response is successful
        self.assertEqual(response.status_code, 200)

        # Checks that the Specimen instance details are present in the response
        self.assertContains(response, str(self.specimen.catalog_number))
        self.assertContains(response, str(self.specimen.expedition))
        self.assertContains(response, str(self.specimen.taxonomy))

    def test_specimen_add_view(self):
        # Access the Specimen add view in the admin
        url = reverse('admin:specimen_catalog_specimen_add')
        response = self.client.get(url)

        # Checks that the response is successful
        self.assertEqual(response.status_code, 200)

        # Checks that the form contains the expected fields
        self.assertContains(response, 'id_catalog_number')
        self.assertContains(response, 'id_expedition')
        self.assertContains(response, 'id_taxonomy')

#Testing the Serializers
class SpecimenListAPIViewTestCase(APITestCase):
    def setUp(self):
        # Sets up data for the test case
        self.url = reverse('specimen-list')  # Sets the URL for the specimen-list endpoint
        expedition = ExpeditionFactory()  # Creates an expedition using the factory
        taxonomy = TaxonomyFactory()  # Creates a taxonomy using the factory
        self.specimen_data = {
            'catalog_number': 'Catalog-1',
            'expedition': expedition.pk,
            'taxonomy': taxonomy.pk
        }  # Data for creating a specimen

    def test_specimen_list_retrieve(self):
        # Tests retrieving a list of specimens using the API
        specimen = SpecimenFactory()  # Creates a specimen using the factory
        response = self.client.get(self.url)  # Makes a GET request to the specimen-list endpoint

        # Checks that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checks that there is one specimen in the response
        self.assertEqual(len(response.data), 1)

        # Checks that the catalog number in the response matches the created specimen's catalog number
        self.assertEqual(response.data[0]['catalog_number'], specimen.catalog_number)

class SpecimenDetailAPIViewTestCase(APITestCase):
    def setUp(self):
        # Sets up data for the test case
        self.specimen = SpecimenFactory()  # Creates a specimen using the factory
        self.url = reverse('specimen-detail', kwargs={'pk': self.specimen.pk})  # Sets the URL for the specimen-detail endpoint
        self.specimen_data = {'catalog_number': 'UpdatedCatalog-1'}  # Data for updating the specimen

    def test_specimen_detail_retrieve(self):
        # Tests retrieving details of a specimen using the API
        response = self.client.get(self.url)  # Makes a GET request to the specimen-detail endpoint

        # Checks that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checks that the catalog number in the response matches the specimen's catalog number
        self.assertEqual(response.data['catalog_number'], self.specimen.catalog_number)

    def test_specimen_detail_delete(self):
        # Test deleting a specimen using the API
        response = self.client.delete(self.url)  # Make a DELETE request to the specimen-detail endpoint

        # Checks that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Checks that there are no specimens in the database after deletion
        self.assertEqual(Specimen.objects.count(), 0)

class ExpeditionListAPIViewTestCase(APITestCase):
    def setUp(self):
        # Sets up data for the test case
        self.url = reverse('expedition-list')  # Set the URL for the expedition-list endpoint

    def test_expedition_list_create(self):
        # Tests creating a new expedition using the API
        expedition_data = {'field1': 'value1', 'field2': 'value2'}  # Data for creating a new expedition
        response = self.client.post(reverse('expedition-list'), data=expedition_data)  # Makes a POST request to the expedition-list endpoint

        # Prints the response content in case of failure (for debugging)
        if response.status_code != status.HTTP_201_CREATED:
            print(response.content)

        # Checks that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_expedition_list_retrieve(self):
        # Tests retrieving a list of expeditions using the API
        expedition = ExpeditionFactory()  # Creates an expedition using the factory
        response = self.client.get(self.url)  # Makes a GET request to the expedition-list endpoint

        # Checks that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checks that the number of expeditions in the response data is 1
        self.assertEqual(len(response.data), 1)

class ExpeditionDetailAPIViewTestCase(APITestCase):
    def setUp(self):
        # Sets up data for the test case
        self.expedition = ExpeditionFactory()  # Create an expedition using the factory
        self.url = reverse('expedition-detail', kwargs={'pk': self.expedition.pk})  # Sets the URL for the expedition-detail endpoint
        self.expedition_data = {'field1': 'updated_value1', 'field2': 'updated_value2'}  # Data for updating the expedition

    def test_expedition_detail_retrieve(self):
        # Tests retrieving expedition details using the API
        response = self.client.get(self.url)  # Makes a GET request to the expedition-detail endpoint

        # Checks that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_expedition_detail_update(self):
        # Tests updating expedition details using the API
        response = self.client.put(reverse('expedition-detail', kwargs={'pk': self.expedition.pk}), data=self.expedition_data)

        # Checks that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_expedition_detail_delete(self):
        # Tests deleting an expedition using the API
        response = self.client.delete(self.url)  # Make a DELETE request to the expedition-detail endpoint

        # Checks that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Checks that there are no more expeditions in the database after deletion
        self.assertEqual(Expedition.objects.count(), 0)

class SpecimenListAPIViewTestCase(APITestCase):
    def setUp(self):
        # Sets up data for the test case
        self.url = reverse('specimen-list')
        self.expedition = ExpeditionFactory()
        self.taxonomy = TaxonomyFactory()
        self.specimen_data = {
            'catalog_number': 'Catalog-1',
            'expedition': self.expedition.pk,
            'taxonomy': self.taxonomy.pk
        }

    def test_specimen_list_retrieve(self):
        # Tests retrieving a list of specimens using the API
        specimen = SpecimenFactory()  # Create a specimen using the factory
        response = self.client.get(self.url)  # Make a GET request to the 'specimen-list' endpoint

        # Checks that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check sthat the number of specimens in the response data is 1
        self.assertEqual(len(response.data), 1)
        
        # Checks that the catalog_number of the first specimen in the response matches the created specimen's catalog_number
        self.assertEqual(response.data[0]['catalog_number'], specimen.catalog_number) 

#Testing the New Expedition view
class NewExpeditionViewTestCase(TestCase):
    def test_get_request(self):
        # Tests a GET request to the 'new_expedition' view
        response = self.client.get(reverse('new_expedition'))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Checks that the 'expedition_form' in the context is an instance of ExpeditionForm
        self.assertIsInstance(response.context['expedition_form'], ExpeditionForm)
        
        # Checks that the template used is 'specimen_catalog/new_expedition.html'
        self.assertTemplateUsed(response, 'specimen_catalog/new_expedition.html')

    def test_post_request_invalid_data(self):
        # Tests a POST request to the 'new_expedition' view with invalid data
        invalid_expedition_data = {'field1': 'value1'}  
        response = self.client.post(reverse('new_expedition'), data=invalid_expedition_data)

        # Checks that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

#Testing the New taxonomy view
class NewTaxonomyViewTestCase(TestCase):
    def setUp(self):
        # Creates a test user if needed
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_get_request(self):
        # Tests the GET request to ensure the form is rendered
        response = self.client.get(reverse('new_taxonomy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'specimen_catalog/new_taxonomy.html')
        self.assertIsInstance(response.context['taxonomy_form'], TaxonomyForm)

    def test_post_request_invalid_data(self):
        # Tests the POST request with invalid data
        taxonomy_data = {'field1': 'value1'} 
        response = self.client.post(reverse('new_taxonomy'), data=taxonomy_data)

        # Checks that the form is not valid and errors are present in the response
        self.assertFalse(response.context['taxonomy_form'].is_valid())

# Testing the New Specimen View
class NewSpecimenViewTestCase(TestCase):
    def setUp(self):
        # Creates a test user if needed
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_get_request(self):
        # Tests the GET request to ensure the form is rendered
        response = self.client.get(reverse('new_specimen'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'specimen_catalog/new_specimen.html')
        self.assertIsInstance(response.context['form'], NewSpecimenForm)

# Testing the Delete Specimen View
class SpecimenDeleteViewTestCase(TestCase):
    def setUp(self):
        # Creates a test user if needed
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Creates a test specimen
        self.specimen = Specimen.objects.create(catalog_number='TestCatalog', expedition=None, taxonomy=None)

        # Login the user (if needed for views with login_required)
        self.client.login(username='testuser', password='testpassword')

    def test_get_request(self):
        # Tests the GET request to ensure the confirmation template is rendered
        response = self.client.get(reverse('specimen_delete', kwargs={'pk': self.specimen.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'specimen_catalog/specimen_delete_confirm.html')
        self.assertIsInstance(response.context['object'], Specimen)

    def test_get_request_specimen_not_found(self):
        # Tests the GET request when the specimen is not found
        response = self.client.get(reverse('specimen_delete', kwargs={'pk': 999})) 
        self.assertRedirects(response, reverse('all_specimens'))
        self.assertEqual(response.status_code, 302) 

        # Checks that an error message is present in the response
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(str(messages[0]), 'Specimen not found')

    def test_post_request_valid_data(self):
        # Tests the POST request with valid data (specimen deletion)
        response = self.client.post(reverse('specimen_delete', kwargs={'pk': self.specimen.pk}), follow=True)

        # Checks that the success message is present in the response
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(messages[0].tags, 'success')
        self.assertEqual(str(messages[0]), 'Specimen deleted successfully.')