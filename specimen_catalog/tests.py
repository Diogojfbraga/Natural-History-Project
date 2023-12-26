# specimen_catalog/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Expedition, Taxonomy, Specimen
from .forms import SpecimenForm, ExpeditionForm, TaxonomyForm, NewSpecimenForm
from .filters import SpecimenFilter

class ModelTestCase(TestCase):
    def test_expedition_model(self):
        # Test the Expedition model
        expedition = Expedition.objects.create(expedition="Test Expedition")
        self.assertEqual(str(expedition), "Test Expedition")  # Check if the string representation is correct

    def test_taxonomy_model(self):
        # Test the Taxonomy model
        taxonomy = Taxonomy.objects.create(species="Test Species")
        self.assertEqual(str(taxonomy), "Taxonomy Test Species")  # Check if the string representation is correct

    def test_specimen_model(self):
        # Test the Specimen model
        specimen = Specimen.objects.create(catalog_number='Test Catalog', created=20230101)
        self.assertEqual(str(specimen), f"Specimen {specimen.specimen_id}")  # Check if the string representation is correct


class FormTestCase(TestCase):
    def test_specimen_form(self):
        # Test the SpecimenForm
        form_data = {'catalog_number': 'Test Catalog', 'created': 2023}
        form = SpecimenForm(data=form_data)
        self.assertTrue(form.is_valid())  # Check if the form is valid

    def test_expedition_form(self):
        # Test the ExpeditionForm
        form_data = {'expedition': 'Test Expedition', 'continent': 'Test Continent'}
        form = ExpeditionForm(data=form_data)
        self.assertTrue(form.is_valid())  # Check if the form is valid

    def test_taxonomy_form(self):
        # Test the TaxonomyForm
        form_data = {'species': 'Test Species', 'kingdom': 'Test Kingdom'}
        form = TaxonomyForm(data=form_data)
        self.assertTrue(form.is_valid())  # Check if the form is valid

    def test_new_specimen_form(self):
        # Test the NewSpecimenForm
        form_data = {'catalog_number': 'Test Catalog', 'created': 2023, 'expedition': None, 'taxonomy': None}
        form = NewSpecimenForm(data=form_data)
        self.assertTrue(form.is_valid())  # Check if the form is valid


class ViewTestCase(TestCase):
    def test_index_view(self):
        # Test the 'index' view
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_all_specimens_view(self):
        # Test the 'all_specimens' view
        response = self.client.get(reverse('all_specimens'))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_specimen_detail_view(self):
        # Test the 'specimen_detail' view
        specimen = Specimen.objects.create(catalog_number="Test Catalog", created=2023)
        response = self.client.get(reverse('specimen_detail', kwargs={'pk': specimen.pk}))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_expedition_update_view(self):
        # Test the 'expedition_update' view
        expedition = Expedition.objects.create(expedition="Test Expedition")
        response = self.client.get(reverse('expedition_update', kwargs={'pk': expedition.pk}))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_taxonomy_update_view(self):
        # Test the 'taxonomy_update' view
        specimen = Specimen.objects.create(catalog_number="Test Catalog", created=2023)
        response = self.client.get(reverse('taxonomy_update', kwargs={'specimen_pk': specimen.pk}))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_specimen_update_view(self):
        # Test the 'specimen_update' view
        specimen = Specimen.objects.create(catalog_number="Test Catalog", created=2023)
        response = self.client.get(reverse('specimen_update', kwargs={'pk': specimen.pk}))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_specimen_delete_view(self):
        # Test the 'specimen_delete' view
        specimen = Specimen.objects.create(catalog_number="Test Catalog", created=2023)
        response = self.client.get(reverse('specimen_delete', kwargs={'pk': specimen.pk}))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_new_specimen_view(self):
        # Test the 'new_specimen' view
        response = self.client.get(reverse('new_specimen'))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_new_taxonomy_view(self):
        # Test the 'new_taxonomy' view
        response = self.client.get(reverse('new_taxonomy'))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_new_expedition_view(self):
        # Test the 'new_expedition' view
        response = self.client.get(reverse('new_expedition'))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_expedition_delete_view(self):
        # Test the 'expedition_delete' view
        expedition = Expedition.objects.create(expedition="Test Expedition")
        response = self.client.get(reverse('expedition_delete', kwargs={'pk': expedition.pk}))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_all_expeditions_view(self):
        # Test the 'all_expeditions' view
        response = self.client.get(reverse('all_expeditions'))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_taxonomy_delete_view(self):
        # Test the 'taxonomy_delete' view
        taxonomy = Taxonomy.objects.create(species="Test Species")
        response = self.client.get(reverse('taxonomy_delete', kwargs={'pk': taxonomy.pk}))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_all_taxonomies_view(self):
        # Test the 'all_taxonomies' view
        response = self.client.get(reverse('all_taxonomies'))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_specimen_filter_view(self):
        # Test the 'specimen_filter' view
        response = self.client.get(reverse('specimen_filter'))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_search_results_view(self):
        # Test the 'search_results' view
        response = self.client.get(reverse('search_results'))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_invalid_search_results_view(self):
        # Test the 'search_results' view with invalid search parameters
        response = self.client.get(reverse('search_results'), {'invalid_param': 'Invalid'})
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_invalid_specimen_detail_view(self):
        # Test the 'specimen_detail' view with an invalid specimen ID
        response = self.client.get(reverse('specimen_detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)  # Check if the response status code is 404 (Not Found)

    def test_invalid_expedition_update_view(self):
        # Test the 'expedition_update' view with an invalid expedition ID
        response = self.client.get(reverse('expedition_update', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)  # Check if the response status code is 404 (Not Found)

    def test_invalid_taxonomy_update_view(self):
        # Test the 'taxonomy_update' view with an invalid specimen ID
        response = self.client.get(reverse('taxonomy_update', kwargs={'specimen_pk': 999}))
        self.assertRedirects(response, '/path/to/redirect', status_code=302)

    def test_invalid_specimen_update_view(self):
        # Test the 'specimen_update' view with an invalid specimen ID
        response = self.client.get(reverse('specimen_update', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)  # Check if the response status code is 404 (Not Found)

    def test_invalid_specimen_delete_view(self):
        # Test the 'specimen_delete' view with an invalid specimen ID
        response = self.client.get(reverse('specimen_delete', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)  # Check if the response status code is 404 (Not Found)

    def test_invalid_expedition_delete_view(self):
        # Test the 'expedition_delete' view with an invalid expedition ID
        response = self.client.get(reverse('expedition_delete', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)  # Check if the response status code is 404 (Not Found)

    def test_invalid_all_expeditions_view(self):
        # Test the 'all_expeditions' view with an invalid expedition ID
        response = self.client.get(reverse('all_expeditions'))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_invalid_taxonomy_delete_view(self):
        # Test the 'taxonomy_delete' view with an invalid taxonomy ID
        response = self.client.get(reverse('taxonomy_delete', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)  # Check if the response status code is 404 (Not Found)

    def test_invalid_all_taxonomies_view(self):
        # Test the 'all_taxonomies' view with an invalid taxonomy ID
        response = self.client.get(reverse('all_taxonomies'))
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_invalid_specimen_filter_view(self):
        # Test the 'specimen_filter' view with invalid filter parameters
        response = self.client.get(reverse('specimen_filter'), {'invalid_param': 'Invalid'})
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_invalid_search_results_view(self):
        # Test the 'search_results' view with invalid search parameters
        response = self.client.get(reverse('search_results'), {'invalid_param': 'Invalid'})
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)
