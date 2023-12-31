from django.test import TestCase
from django.urls import reverse

class IndexViewTests(TestCase):
    # Test to check if the index view returns a 200 status code.
    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    # Test to check if the index view uses the correct template.
    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'specimen_catalog/index.html')

    # Test to check if the expected content is present in the index view.
    def test_index_view_content(self):
        response = self.client.get(reverse('index'))
        expected_content = 'Welcome to Natural History Project'
        self.assertContains(response, expected_content, status_code=200)

    # Test to check if the index view returns a 404 status code for an invalid URL.
    def test_index_view_returns_404(self):
        response = self.client.get('/invalid_url/')
        self.assertEqual(response.status_code, 404)

#Testing the filter from all specimens
class FilterFormTests(TestCase):
    def test_filter_form_rendering(self):
        # Test to check if the filter form is rendered successfully.
        response = self.client.get(reverse('all_specimens'))
        self.assertContains(response, 'Filter', status_code=200)
        self.assertContains(response, 'Reset Filters', status_code=200)

    def test_filter_form_submission(self):
        # Test to check if the filter form can be submitted successfully.
        data = {
            'taxonomy__kingdom': 'Sample Kingdom',
            'expedition__continent': 'Sample Continent',
            # Add more sample filter parameters as needed
        }
        response = self.client.get(reverse('all_specimens'), data=data)
        self.assertEqual(response.status_code, 200)  # You can update this based on your expected behavior

    def test_filter_form_reset(self):
        # Test to check if the reset button in the filter form works.
        data = {
            'taxonomy__kingdom': 'Sample Kingdom',
            'expedition__continent': 'Sample Continent',
            # Add more sample filter parameters as needed
        }
        response_with_data = self.client.get(reverse('all_specimens'), data=data)
        self.assertContains(response_with_data, 'Sample Kingdom', status_code=200)

        response_reset = self.client.get(reverse('all_specimens'), {'reset_filters': 'Reset Filters'})
        self.assertNotContains(response_reset, 'Sample Kingdom', status_code=200)


from django.test import TestCase
from django.urls import reverse
from django.core.paginator import Paginator

from .models import Expedition, Specimen
from django.core.paginator import Page
from .views import SpecimenDetailView

class AllSpecimensViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        expedition = Expedition.objects.create(expedition='Expedition Artic', continent='Europe', country='Spain')

        # Create some test specimens for pagination
        for i in range(30):
            Specimen.objects.create(catalog_number=f'Catalog{i}', expedition=expedition, created=i)

    def test_all_specimens_view(self):
        url = reverse('all_specimens')

        # Use the client to simulate a GET request to the view
        response = self.client.get(url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'specimen_catalog/all_specimens.html')

    def test_pagination(self):
        url = reverse('all_specimens')

        # Use the client to simulate a GET request to the view with page parameter
        response = self.client.get(url, {'page': 2})

        # Check that the specimens are paginated
        self.assertIsInstance(response.context['specimens'], Page)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'specimen_catalog/all_specimens.html')

    def test_filtering(self):
        url = reverse('all_specimens')

        # Use the client to simulate a GET request to the view with filter parameters
        response = self.client.get(url, {'expedition__continent': 'Europe'})

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'specimen_catalog/all_specimens.html')

from django.test import TestCase
from django.urls import reverse
from django.http import Http404
from django.contrib.messages import get_messages

from .models import Expedition, Specimen

class SpecimenDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a sample expedition
        expedition = Expedition.objects.create(expedition='Expedition Artic', continent='Europe', country='Spain')

        # Create a sample specimen
        cls.specimen = Specimen.objects.create(catalog_number='Catalog123', expedition=expedition)

    def test_specimen_detail_view_success(self):
        url = reverse('specimen_detail', kwargs={'pk': self.specimen.pk})
        response = self.client.get(url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'specimen_catalog/specimen_detail.html')

        # Check that the specimen is present in the context
        self.assertIn('specimen', response.context)
        self.assertEqual(response.context['specimen'], self.specimen)

def test_specimen_detail_view_not_found(self):
    # Create an invalid specimen ID that does not exist
    invalid_specimen_id = self.specimen.pk + 1

    url = reverse('specimen_detail', kwargs={'pk': invalid_specimen_id})
    response = self.client.get(url)

    # Check that the response status code is 404 (Not Found)
    self.assertEqual(response.status_code, 404)

    # Check that the expected template name is present in the response content
    self.assertContains(response, '404.html')
    self.assertContains(response, "Specimen not found")

    from unittest.mock import patch

    @patch('specimen_catalog.views.SpecimenDetailView.get_context_data')
    def test_specimen_detail_view_error_handling(self, mock_get_context_data):
        mock_get_context_data.side_effect = Exception("Mocked exception in get_context_data")

        url = reverse('specimen_detail', kwargs={'pk': self.specimen.pk})
        response = self.client.get(url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that an error message is added to the messages framework
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Error fetching specimen details", messages)

